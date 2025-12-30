import os
import json
import pandas as pd
import glob

def migrate_v1():
    print("Migrating v1 logs...")
    base_dir = "data/validation"
    out_base = "data/episodes/v1"
    manifest = []
    
    # Baseline
    for seed_dir in glob.glob(os.path.join(base_dir, "baseline", "seed_*")):
        seed = int(seed_dir.split("_")[-1])
        log_path = os.path.join(seed_dir, "episode_logs.csv")
        if os.path.exists(log_path):
            process_log(log_path, "v1", "baseline", "baseline", seed, "random_regular", out_base, manifest)
            
    # Controls
    for cond_dir in glob.glob(os.path.join(base_dir, "controls", "*")):
        cond = os.path.basename(cond_dir)
        for seed_dir in glob.glob(os.path.join(cond_dir, "seed_*")):
            seed = int(seed_dir.split("_")[-1])
            log_path = os.path.join(seed_dir, "episode_logs.csv")
            if os.path.exists(log_path):
                process_log(log_path, "v1", "control", cond, seed, "random_regular", out_base, manifest)
                
    # Sweep
    for sweep_dir in glob.glob(os.path.join(base_dir, "sweep", "*")):
        cond = os.path.basename(sweep_dir)
        log_path = os.path.join(sweep_dir, "episode_logs.csv")
        if os.path.exists(log_path):
            process_log(log_path, "v1", "sweep", cond, 42, "random_regular", out_base, manifest)

    os.makedirs("data/v1", exist_ok=True)
    with open("data/v1/run_manifest.json", 'w') as f:
        json.dump(manifest, f, indent=4)
    print(f"v1 migration complete. Manifest saved to data/v1/run_manifest.json")

def migrate_v2():
    print("Migrating v2 logs...")
    base_dir = "data/validation_v2"
    out_base = "data/episodes/v2"
    manifest = []
    
    # v2 has phases: power_upgrade, topology_robustness, target_relocation, freeze_constraints, parameter_map
    phases = ["power_upgrade", "topology_robustness", "target_relocation", "freeze_constraints", "parameter_map"]
    
    for phase in phases:
        phase_dir = os.path.join(base_dir, phase)
        if not os.path.exists(phase_dir): continue
        
        if phase in ["target_relocation", "freeze_constraints"]:
            # These have seeds directly under phase_dir
            for seed_dir in glob.glob(os.path.join(phase_dir, "seed_*")):
                seed = int(seed_dir.split("_")[-1])
                log_path = os.path.join(seed_dir, "episode_logs.csv")
                if os.path.exists(log_path):
                    process_log(log_path, "v2", phase, phase, seed, "random_regular", out_base, manifest)
        else:
            # These have conditions then seeds
            for cond_dir in glob.glob(os.path.join(phase_dir, "*")):
                cond = os.path.basename(cond_dir)
                for seed_dir in glob.glob(os.path.join(cond_dir, "seed_*")):
                    seed = int(seed_dir.split("_")[-1])
                    log_path = os.path.join(seed_dir, "episode_logs.csv")
                    if os.path.exists(log_path):
                        topo = "random_regular"
                        if "erdos_renyi" in cond: topo = "erdos_renyi"
                        elif "small_world" in cond: topo = "watts_strogatz"
                        process_log(log_path, "v2", phase, cond, seed, topo, out_base, manifest)

    os.makedirs("data/v2", exist_ok=True)
    with open("data/v2/run_manifest.json", 'w') as f:
        json.dump(manifest, f, indent=4)
    print(f"v2 migration complete. Manifest saved to data/v2/run_manifest.json")

def process_log(log_path, version, phase, condition, seed, topology, out_base, manifest):
    df = pd.read_csv(log_path)
    run_id = f"{version}_{condition}_s{seed}"
    
    # Map old names to new names if needed
    if 'episode' in df.columns and 'episode_idx' not in df.columns:
        df = df.rename(columns={'episode': 'episode_idx'})
    if 'num_transitions' in df.columns and 'accepted_moves' not in df.columns:
        df = df.rename(columns={'num_transitions': 'accepted_moves'})
    if 'entropy' in df.columns and 'path_entropy' not in df.columns:
        df = df.rename(columns={'entropy': 'path_entropy'})
        
    # Add missing metadata
    df['run_id'] = run_id
    df['validation_version'] = version
    df['condition'] = condition
    df['seed'] = seed
    df['topology'] = topology
    df['n_nodes'] = 100 # default
    df['degree'] = 4 # default for random_regular
    
    if 'attempted_moves' not in df.columns:
        df['attempted_moves'] = df['hitting_time']
    if 'accept_rate' not in df.columns:
        df['accept_rate'] = df['accepted_moves'] / df['attempted_moves']
        
    # Standardize column order
    cols = ['run_id', 'validation_version', 'condition', 'seed', 'topology', 'n_nodes', 
            'degree', 'episode_idx', 'hitting_time', 'path_entropy', 
            'accepted_moves', 'attempted_moves', 'accept_rate', 'start_node', 'final_node']
    # Filter to only those that exist
    cols = [c for c in cols if c in df.columns]
    df = df[cols]
    
    out_dir = os.path.join(out_base, condition)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{run_id}_episodes.csv")
    df.to_csv(out_path, index=False)
    
    manifest.append({
        "run_id": run_id,
        "phase": phase,
        "condition": condition,
        "seed": seed,
        "topology": topology,
        "output_dir": os.path.dirname(log_path),
        "standardized_log": out_path
    })

if __name__ == "__main__":
    migrate_v1()
    migrate_v2()
