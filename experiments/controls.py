from experiments.run_episodes import Simulator
import os

def run_controls():
    num_episodes = 100
    
    # Control 1: No Evolution
    print("\n--- Running Control: No Evolution ---")
    sim_no_evo = Simulator(evolution_mode="none", seed=42)
    sim_no_evo.run_simulation(num_episodes=num_episodes)
    sim_no_evo.save_results(output_dir="data/control_no_evolution")
    
    # Control 2: Random Evolution
    print("\n--- Running Control: Random Evolution ---")
    sim_rand = Simulator(evolution_mode="random", lmbda=0.1, mu=0.01, seed=42)
    sim_rand.run_simulation(num_episodes=num_episodes)
    sim_rand.save_results(output_dir="data/control_random_evolution")
    
    # Control 3: High Decay (High Mu)
    print("\n--- Running Control: High Decay ---")
    sim_high_mu = Simulator(evolution_mode="standard", lmbda=0.1, mu=0.8, seed=42)
    sim_high_mu.run_simulation(num_episodes=num_episodes)
    sim_high_mu.save_results(output_dir="data/control_high_decay")

if __name__ == "__main__":
    run_controls()
