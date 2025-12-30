import json
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns

def plot_constraint_heatmaps(data_dir: str, output_dir: str = "paper_figures"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    snapshot_files = sorted([f for f in os.listdir(data_dir) if f.startswith("constraints_ep")])
    if not snapshot_files:
        print(f"No snapshots found in {data_dir}")
        return

    fig, axes = plt.subplots(1, len(snapshot_files), figsize=(5 * len(snapshot_files), 5))
    if len(snapshot_files) == 1:
        axes = [axes]

    for i, f in enumerate(snapshot_files):
        with open(os.path.join(data_dir, f), 'r') as file:
            constraints = json.load(file)
        
        vals = list(constraints.values())
        
        # Distribution plot for each snapshot
        sns.histplot(vals, bins=30, ax=axes[i], kde=True)
        axes[i].set_title(f"Snapshot: {f.split('_')[-1].split('.')[0]}")
        axes[i].set_xlabel("Constraint Value")
        axes[i].set_xlim(0, 1.1)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "constraint_evolution_hist.pdf"))
    plt.close()

def identify_corridors(data_dir: str, threshold: float = 0.3):
    """Summarizes low-barrier edges from the final snapshot."""
    final_file = "constraints_ep_99.json"
    path = os.path.join(data_dir, final_file)
    if not os.path.exists(path):
        return None

    with open(path, 'r') as f:
        constraints = json.load(f)
    
    low_barrier = {k: v for k, v in constraints.items() if v < threshold}
    return low_barrier

if __name__ == "__main__":
    # Example for one seed
    plot_constraint_heatmaps("data/validation/baseline/seed_1", "paper_figures")
