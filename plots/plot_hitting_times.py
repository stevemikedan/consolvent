import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import numpy as np

def load_and_average(base_dir: str):
    """Loads all seed directories in a base directory and averages hitting times."""
    seed_dirs = glob.glob(os.path.join(base_dir, "seed_*"))
    all_data = []
    for d in seed_dirs:
        csv_path = os.path.join(d, "episode_logs.csv")
        if os.path.exists(csv_path):
            all_data.append(pd.read_csv(csv_path))
    
    if not all_data:
        return None
    
    # Concatenate all seeds and groupby episode
    combined = pd.concat(all_data)
    averaged = combined.groupby("episode").mean().reset_index()
    return averaged

def plot_validation_results(output_dir: str = "paper_figures"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    plt.figure(figsize=(12, 8))
    
    # 1. Baseline
    baseline_avg = load_and_average("data/validation/baseline")
    if baseline_avg is not None:
        plt.plot(baseline_avg['episode'], baseline_avg['hitting_time'].rolling(window=10).mean(), 
                 label="Baseline (HCCDE) - Avg", linewidth=3, color='blue')
        
    # 2. Controls
    control_colors = {'no_evolution': 'red', 'random_evolution': 'green', 'high_decay': 'orange'}
    for control, color in control_colors.items():
        avg_df = load_and_average(f"data/validation/controls/{control}")
        if avg_df is not None:
            plt.plot(avg_df['episode'], avg_df['hitting_time'].rolling(window=10).mean(), 
                     label=f"Control: {control}", linestyle='--', color=color)

    plt.xlabel("Episode Index")
    plt.ylabel("Hitting Time (Steps)")
    plt.title("HCCDE Validation: Averaged Hitting Times")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, "validation_hitting_times_overlay.pdf"))
    plt.close()

    # 3. Individual Baseline Seeds Plot
    plt.figure(figsize=(10, 6))
    seed_dirs = glob.glob("data/validation/baseline/seed_*")
    for d in seed_dirs:
        seed_label = os.path.basename(d)
        df = pd.read_csv(os.path.join(d, "episode_logs.csv"))
        plt.plot(df['episode'], df['hitting_time'].rolling(window=10).mean(), label=seed_label, alpha=0.6)
    
    plt.xlabel("Episode Index")
    plt.ylabel("Hitting Time (Steps)")
    plt.title("Baseline Hitting Times (Per Seed)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, "baseline_seeds_hitting_times.pdf"))
    plt.close()

if __name__ == "__main__":
    plot_validation_results()
