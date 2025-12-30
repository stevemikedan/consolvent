import os
import json
import pandas as pd
import numpy as np
from typing import List
from experiments.run_episodes import Simulator

def run_validation_battery():
    # 0. Configuration
    baseline_params = {"beta": 1.0, "lmbda": 0.05, "mu": 0.001}
    seeds = [1, 2, 3, 4, 5]
    num_episodes = 100
    snapshot_episodes = [0, 24, 49, 99] # 1, 25, 50, 100 in 0-indexed
    
    print("Starting HCCDE Validation Battery...")
    print("Guardrail: No parameter optimization. Using fixed ranges.")
    
    all_manifest = []
    
    # 1. Baseline Runs
    for seed in seeds:
        print(f"\n--- Running Baseline Seed {seed} ---")
        sim = Simulator(**baseline_params, seed=seed, snapshot_episodes=snapshot_episodes, validation_version="v1", condition="baseline")
        seed_dir = f"data/validation/baseline/seed_{seed}"
        sim.run_simulation(num_episodes=num_episodes, output_dir=seed_dir)
        all_manifest.append({
            "phase": "baseline",
            "condition": "baseline",
            "seed": seed,
            "output_dir": seed_dir,
            "topology": "random_regular"
        })
        
    # 2. Control Runs
    controls = [
        {"name": "no_evolution", "params": {**baseline_params, "lmbda": 0, "evolution_mode": "none"}},
        {"name": "random_evolution", "params": {**baseline_params, "evolution_mode": "random"}},
        {"name": "high_decay", "params": {**baseline_params, "mu": 0.2, "evolution_mode": "standard"}}
    ]
    
    for control in controls:
        for seed in seeds:
            print(f"\n--- Running Control {control['name']} Seed {seed} ---")
            sim = Simulator(**control['params'], seed=seed, validation_version="v1", condition=control['name'])
            seed_dir = f"data/validation/controls/{control['name']}/seed_{seed}"
            sim.run_simulation(num_episodes=num_episodes, output_dir=seed_dir)
            all_manifest.append({
                "phase": "control",
                "condition": control['name'],
                "seed": seed,
                "output_dir": seed_dir,
                "topology": "random_regular"
            })
            
    # 3. Parameter Sweep
    lmbdas = [0.01, 0.05, 0.1]
    mus = [0.0, 0.01, 0.05]
    betas = [0.5, 1.0, 1.5]
    
    sweep_results = []
    
    print("\n--- Running Parameter Sweep ---")
    for b in betas:
        for l in lmbdas:
            for m in mus:
                run_name = f"beta_{b}_lambda_{l}_mu_{m}"
                print(f"Sweep: {run_name}")
                sim = Simulator(beta=b, lmbda=l, mu=m, seed=42, validation_version="v1", condition=run_name) # One seed per combination
                seed_dir = f"data/validation/sweep/{run_name}"
                sim.run_simulation(num_episodes=num_episodes, output_dir=seed_dir)
                all_manifest.append({
                    "phase": "sweep",
                    "condition": run_name,
                    "seed": 42,
                    "output_dir": seed_dir,
                    "topology": "random_regular",
                    "params": {"beta": b, "lambda": l, "mu": m}
                })
                
                # Extract metrics for table
                df = pd.DataFrame(sim.episode_logs)
                last_20 = df.tail(20)
                mean_ht = float(last_20['hitting_time'].median())
                
                # Entropy change rate (simple slope)
                entropy_slope = float(np.polyfit(df['episode'], df['entropy'], 1)[0])
                
                sweep_results.append({
                    "beta": b,
                    "lambda": l,
                    "mu": m,
                    "mean_hitting_time_last_20": mean_ht,
                    "entropy_slope": entropy_slope
                })
                
    # Save sweep table
    pd.DataFrame(sweep_results).to_csv("data/validation/sweep_summary.csv", index=False)
    print("\nParameter Sweep Summary saved to data/validation/sweep_summary.csv")
    
    os.makedirs(os.path.join("data", "v1"), exist_ok=True)
    with open(os.path.join("data", "v1", "run_manifest.json"), 'w') as f:
        json.dump(all_manifest, f, indent=4)
    print(f"Manifest saved to {os.path.join('data', 'v1', 'run_manifest.json')}")

if __name__ == "__main__":
    run_validation_battery()
