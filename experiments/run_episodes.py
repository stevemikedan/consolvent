import os
import random
import json
import pandas as pd
import numpy as np
from typing import List, Set, Optional, Dict, Any

from model.state_space import StateSpace
from model.constraints import ConstraintField
from model.dynamics import Dynamics
from metrics.hitting_time import HittingTimeTracker
from metrics.path_entropy import PathEntropyTracker
from metrics.constraint_stats import ConstraintStatsTracker

class Simulator:
    """
    Orchestrates the HCCDE toy model simulation.
    """
    def __init__(self, size: int = 100, beta: float = 5.0, lmbda: float = 0.1, mu: float = 0.0,
                 target_size: int = 5, seed: int = 42, evolution_mode: str = "standard",
                 snapshot_episodes: List[int] = None, topology: str = "random_regular",
                 topology_kwargs: Dict[str, Any] = None,
                 validation_version: str = "v2", condition: str = "unknown",
                 run_id: str = None):
        self.seed = seed
        self.size = size
        self.topology = topology
        self.validation_version = validation_version
        self.condition = condition
        self.run_id = run_id or f"{validation_version}_{condition}_s{seed}"
        
        random.seed(seed)
        np.random.seed(seed)
        
        topo_args = topology_kwargs or {}
        self.state_space = StateSpace(size=size, topology=topology, **topo_args)
        # Degree might vary if not regular, but for regular it's topo_args.get('k', 4)
        self.degree = topo_args.get('k', 4) if topology == 'random_regular' else "variable"
        
        self.constraints = ConstraintField(self.state_space.get_edges())
        self.dynamics = Dynamics(beta=beta)
        
        self.lmbda = lmbda
        self.mu = mu
        self.evolution_mode = evolution_mode # 'standard', 'random', 'none'
        self.snapshot_episodes = snapshot_episodes or []
        self.constraints_frozen = False
        
        # Define target set A (macro-target)
        self.target_size = target_size
        self._init_target(target_size)
        
        self.hitting_tracker = HittingTimeTracker()
        self.entropy_tracker = PathEntropyTracker()
        self.stats_tracker = ConstraintStatsTracker()
        self.episode_logs = []

    def _init_target(self, target_size: int, exclude: Set[int] = None):
        all_nodes = list(self.state_space.graph.nodes)
        if exclude:
            available = [n for n in all_nodes if n not in exclude]
        else:
            available = all_nodes
            
        self.target_set: Set[int] = set(random.sample(available, target_size))

    def relocate_target(self, new_target_size: int = None, disjoint: bool = True):
        """Relocates the target set, optionally ensuring it is disjoint from the current one."""
        size = new_target_size if new_target_size is not None else self.target_size
        exclude = self.target_set if disjoint else None
        self._init_target(size, exclude=exclude)
        print(f"Target relocated. New target set size: {len(self.target_set)}")

    def set_constraints_frozen(self, frozen: bool):
        """Freezes or unfreezes constraint evolution."""
        self.constraints_frozen = frozen
        print(f"Constraints {'frozen' if frozen else 'unfrozen'}")

    def run_episode(self, episode_idx: int, max_steps: int = 10000) -> dict:
        """Runs a single episode until the target set A is hit."""
        start_node = self.state_space.reset()
        current_node = start_node
        steps = 0
        transitions = []
        
        while current_node not in self.target_set and steps < max_steps:
            u, v, accepted = self.dynamics.step(self.state_space, self.constraints)
            if accepted:
                transitions.append((u, v))
                # HCCDE Core: Constraint evolution
                if not self.constraints_frozen:
                    if self.evolution_mode == "standard":
                        self.constraints.update_local(u, v, self.lmbda)
                        self.constraints.update_global(u, v, self.mu)
                    elif self.evolution_mode == "random":
                        # Relax a randomly chosen edge instead of the used one
                        all_edges = list(self.constraints.constraints.keys())
                        rand_edge = random.choice(all_edges)
                        self.constraints.update_local(rand_edge[0], rand_edge[1], self.lmbda)
                        self.constraints.update_global(rand_edge[0], rand_edge[1], self.mu)
                # 'none' mode or frozen state does nothing
                
                current_node = v
            steps += 1
            
        # Logging
        self.hitting_tracker.record(steps)
        entropy = self.entropy_tracker.record_episode(transitions)
        stats = self.constraints.get_summary_stats()
        self.stats_tracker.record(episode_idx, stats)
        
        log_entry = {
            "run_id": self.run_id,
            "validation_version": self.validation_version,
            "condition": self.condition,
            "seed": self.seed,
            "topology": self.topology,
            "n_nodes": self.size,
            "degree": self.degree,
            "episode_idx": episode_idx,
            "hitting_time": steps,
            "path_entropy": entropy,
            "accepted_moves": len(transitions),
            "attempted_moves": steps,
            "accept_rate": len(transitions) / steps if steps > 0 else 0.0,
            "start_node": start_node,
            "final_node": current_node
        }
        self.episode_logs.append(log_entry)
        
        # Snapshots
        if episode_idx in self.snapshot_episodes:
            self.last_snapshot_path = None # Will be set during save if called manually, 
                                          # but let's handle it in run_simulation
        return log_entry

    def run_simulation(self, num_episodes: int = 100, output_dir: str = "data", start_episode: int = 0):
        """Runs multiple episodes sequentially. start_episode allows continuing logs correctly."""
        print(f"Starting simulation: {num_episodes} episodes from {start_episode}, λ={self.lmbda}, μ={self.mu}, mode={self.evolution_mode}, seed={self.seed}")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        for i in range(num_episodes):
            eps_idx = start_episode + i
            log = self.run_episode(eps_idx)
            
            if eps_idx in self.snapshot_episodes:
                snapshot_path = os.path.join(output_dir, f"constraints_ep_{eps_idx}.json")
                self.constraints.save_constraints(snapshot_path)
            
            if eps_idx % 100 == 0:
                print(f"Episode {eps_idx}: Hitting Time = {log['hitting_time']}")
        
        # Save final results
        self.save_results(output_dir)

    def save_results(self, output_dir: str = "data"):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            
        pd.DataFrame(self.episode_logs).to_csv(os.path.join(output_dir, "episode_logs.csv"), index=False)
        
        # Also save to standardized path if possible
        std_dir = os.path.join("data", "episodes", self.validation_version, self.condition)
        os.makedirs(std_dir, exist_ok=True)
        pd.DataFrame(self.episode_logs).to_csv(os.path.join(std_dir, f"{self.run_id}_episodes.csv"), index=False)
        
        self.stats_tracker.get_dataframe().to_csv(os.path.join(output_dir, "constraint_stats.csv"), index=False)
        
        # Snapshot of final constraints
        with open(os.path.join(output_dir, "final_constraints.json"), 'w') as f:
            # Convert tuple keys to strings for JSON
            serializable_constraints = {f"{k[0]}->{k[1]}": v for k, v in self.constraints.constraints.items()}
            json.dump(serializable_constraints, f)

if __name__ == "__main__":
    # Example run
    sim = Simulator(lmbda=0.1, mu=0.01)
    sim.run_simulation(num_episodes=100)
    print("Simulation complete. Data saved to /data.")
