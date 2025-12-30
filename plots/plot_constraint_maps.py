import json
import networkx as nx
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_constraint_map(graph_data_path: str, constraint_path: str, output_path: str):
    # This script would ideally need the graph structure. 
    # Since we don't save the graph object, we'll re-init one or load if we saved it.
    # For now, let's assume we can reconstruct it or just show distribution.
    
    if not os.path.exists(constraint_path):
        print(f"Constraint file not found: {constraint_path}")
        return

    with open(constraint_path, 'r') as f:
        constraints = json.load(f)
    
    vals = list(constraints.values())
    
    plt.figure(figsize=(8, 5))
    plt.hist(vals, bins=30, color='skyblue', edgecolor='black')
    plt.axvline(np.mean(vals), color='red', linestyle='dashed', linewidth=1, label=f"Mean: {np.mean(vals):.2f}")
    plt.xlabel("Constraint Value (C_{i -> j})")
    plt.ylabel("Frequency")
    plt.title("Distribution of Constraints (Final State)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))
    plt.savefig(output_path)
    print(f"Constraint distribution plot saved to {output_path}")

if __name__ == "__main__":
    plot_constraint_map(None, "data/final_constraints.json", "paper_figures/fig3_constraint_dist.pdf")
