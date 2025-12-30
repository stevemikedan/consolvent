import os
import json
import pandas as pd
import numpy as np
import random
from typing import List, Dict, Any
from experiments.run_episodes import Simulator
from metrics.robust_metrics import analyze_seed_data

ROOT_DATA = "data/validation_v2"
ROOT_FIGURES = "paper_figures/validation_v2"

def ensure_dirs():
    for d in [ROOT_DATA, ROOT_FIGURES]:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

def run_power_upgrade():
    """A1 & A2: Power Upgrade - Baseline vs Controls."""
    print("\n--- A: Power Upgrade (Baseline vs Controls) ---")
    seeds = list(range(1, 31))
    episodes = 1000
    baseline_params = {"beta": 1.0, "lmbda": 0.05, "mu": 0.001}
    
    conditions = [
        {"name": "baseline", "params": {**baseline_params, "evolution_mode": "standard"}},
        {"name": "no_evolution", "params": {**baseline_params, "lmbda": 0, "evolution_mode": "none"}},
        {"name": "random_evolution", "params": {**baseline_params, "evolution_mode": "random"}},
        {"name": "high_decay", "params": {**baseline_params, "lmbda": 0.05, "mu": 0.2, "evolution_mode": "standard"}}
    ]
    
    manifest = []
    
    for cond in conditions:
        cond_dir = os.path.join(ROOT_DATA, "power_upgrade", cond['name'])
        for seed in seeds:
            seed_dir = os.path.join(cond_dir, f"seed_{seed}")
            print(f"Running {cond['name']} - Seed {seed}")
            sim = Simulator(**cond['params'], seed=seed, validation_version="v2", condition=cond['name'])
            sim.run_simulation(num_episodes=episodes, output_dir=seed_dir)
            manifest.append({
                "phase": "power_upgrade",
                "condition": cond['name'],
                "seed": seed,
                "output_dir": seed_dir,
                "topology": "random_regular"
            })
            
    return manifest

def run_topology_robustness():
    """B: Topology Robustness."""
    print("\n--- B: Topology Robustness ---")
    seeds = list(range(1, 21)) # Reduced from 30 for time
    episodes = 1000
    params = {"beta": 1.0, "lmbda": 0.05, "mu": 0.001}
    
    topologies = [
        {"name": "random_regular", "kwargs": {"topology": "random_regular"}},
        {"name": "erdos_renyi", "kwargs": {"topology": "erdos_renyi"}},
        {"name": "small_world", "kwargs": {"topology": "watts_strogatz"}}
    ]
    
    manifest = []
    for topo in topologies:
        for mode_name, evo_mode in [("baseline", "standard"), ("no_evolution", "none")]:
            cond_name = f"{topo['name']}_{mode_name}"
            cond_dir = os.path.join(ROOT_DATA, "topology_robustness", cond_name)
            
            p = {**params, "evolution_mode": evo_mode}
            if evo_mode == "none": p["lmbda"] = 0
            
            for seed in seeds:
                print(f"Running Topology {topo['name']} {mode_name} - Seed {seed}")
                sim = Simulator(**p, **topo['kwargs'], seed=seed, validation_version="v2", condition=cond_name)
                sim_seed_dir = os.path.join(cond_dir, f"seed_{seed}")
                sim.run_simulation(num_episodes=episodes, output_dir=sim_seed_dir)
                manifest.append({
                    "phase": "topology_robustness",
                    "condition": cond_name,
                    "seed": seed,
                    "output_dir": sim_seed_dir,
                    "topology": topo['name']
                })
    return manifest

def run_target_relocation():
    """C: Target Relocation Test."""
    print("\n--- C: Target Relocation Test ---")
    seeds = list(range(1, 21))
    episodes_per_phase = 500
    params = {"beta": 1.0, "lmbda": 0.05, "mu": 0.001}
    manifest = []
    
    for seed in seeds:
        print(f"Running Target Relocation - Seed {seed}")
        cond_dir = os.path.join(ROOT_DATA, "target_relocation", f"seed_{seed}")
        sim = Simulator(**params, seed=seed, validation_version="v2", condition="target_relocation")
        
        # Phase 1: Target A1
        sim.run_simulation(num_episodes=episodes_per_phase, output_dir=cond_dir, start_episode=0)
        # Relocate Target
        sim.relocate_target(disjoint=True)
        # Phase 2: Target A2
        sim.run_simulation(num_episodes=episodes_per_phase, output_dir=cond_dir, start_episode=episodes_per_phase)
        manifest.append({
            "phase": "target_relocation",
            "condition": "target_relocation",
            "seed": seed,
            "output_dir": cond_dir,
            "topology": "random_regular"
        })
    return manifest

def run_freeze_constraints():
    """D: Freeze Constraints Diagnostic."""
    print("\n--- D: Freeze Constraints Diagnostic ---")
    seeds = list(range(1, 21))
    episodes_per_phase = 500
    params = {"beta": 1.0, "lmbda": 0.05, "mu": 0.001}
    manifest = []
    
    for seed in seeds:
        print(f"Running Freeze Constraints - Seed {seed}")
        cond_dir = os.path.join(ROOT_DATA, "freeze_constraints", f"seed_{seed}")
        sim = Simulator(**params, seed=seed, validation_version="v2", condition="freeze_constraints")
        
        # Phase 1: Evolution On
        sim.run_simulation(num_episodes=episodes_per_phase, output_dir=cond_dir, start_episode=0)
        # Freeze
        sim.set_constraints_frozen(True)
        # Phase 2: Evolution Off
        sim.run_simulation(num_episodes=episodes_per_phase, output_dir=cond_dir, start_episode=episodes_per_phase)
        manifest.append({
            "phase": "freeze_constraints",
            "condition": "freeze_constraints",
            "seed": seed,
            "output_dir": cond_dir,
            "topology": "random_regular"
        })
    return manifest

def run_parameter_map():
    """E: Robust Parameter Map."""
    print("\n--- E: Robust Parameter Map ---")
    betas = [0.5, 1.0, 1.5]
    lmbdas = [0.01, 0.05, 0.1]
    mus = [0.0, 0.001, 0.01, 0.05]
    seeds = list(range(1, 6))
    episodes = 500
    manifest = []
    
    for b in betas:
        for l in lmbdas:
            for m in mus:
                cond_name = f"b{b}_l{l}_m{m}"
                cond_dir = os.path.join(ROOT_DATA, "parameter_map", cond_name)
                for seed in seeds:
                    print(f"Running ParaMap {cond_name} - Seed {seed}")
                    sim = Simulator(beta=b, lmbda=l, mu=m, seed=seed, validation_version="v2", condition=cond_name)
                    sim_seed_dir = os.path.join(cond_dir, f"seed_{seed}")
                    sim.run_simulation(num_episodes=episodes, output_dir=sim_seed_dir)
                    manifest.append({
                        "phase": "parameter_map",
                        "condition": cond_name,
                        "seed": seed,
                        "output_dir": sim_seed_dir,
                        "topology": "random_regular",
                        "params": {"beta": b, "lambda": l, "mu": m}
                    })
    return manifest

def main():
    ensure_dirs()
    all_manifest = []
    all_manifest.extend(run_power_upgrade())
    all_manifest.extend(run_topology_robustness())
    all_manifest.extend(run_target_relocation())
    all_manifest.extend(run_freeze_constraints())
    all_manifest.extend(run_parameter_map())
    
    os.makedirs(os.path.join("data", "v2"), exist_ok=True)
    with open(os.path.join("data", "v2", "run_manifest.json"), 'w') as f:
        json.dump(all_manifest, f, indent=4)
    print(f"\nManifest saved to {os.path.join('data', 'v2', 'run_manifest.json')}")

if __name__ == "__main__":
    main()
