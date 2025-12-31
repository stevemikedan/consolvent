import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Any
from metrics.robust_metrics import analyze_seed_data
import gc

ROOT_DATA = "data/validation_v2"
ROOT_FIGURES = "paper_figures/validation_v2"

def ensure_dirs():
    if not os.path.exists(ROOT_FIGURES):
        os.makedirs(ROOT_FIGURES, exist_ok=True)

def load_all_runs(manifest_path: str):
    with open(manifest_path, 'r') as f:
        return json.load(f)

def get_seed_logs(run: Dict[str, Any]):
    csv_path = os.path.join(run['output_dir'], "episode_logs.csv")
    if os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    return None

def plot_hitting_times_overlay(all_runs: List[Dict[str, Any]], phase: str = "power_upgrade", stats_df: pd.DataFrame = None):
    """Generates overlay plots for hitting times with CI and IQR bands and robust stats."""
    print(f"Plotting overlay for phase: {phase}")
    phase_runs = [r for r in all_runs if r['phase'] == phase]
    conditions = sorted(list(set(r['condition'] for r in phase_runs)))
    
    plt.figure(figsize=(12, 7))
    colors = sns.color_palette("husl", len(conditions))
    
    for cond, color in zip(conditions, colors):
        cond_runs = [r for r in phase_runs if r['condition'] == cond]
        dfs = []
        for run in cond_runs:
            df = get_seed_logs(run)
            if df is not None:
                df = df[['episode_idx', 'hitting_time']].copy()
                df['hitting_time'] = df['hitting_time'].rolling(window=20).mean()
                dfs.append(df)
        
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            label = cond
            if stats_df is not None:
                cond_stats = stats_df[stats_df['condition'] == cond]
                if not cond_stats.empty:
                    slope = cond_stats['ht_slope'].mean()
                    delta = cond_stats['cliffs_delta'].mean()
                    label = f"{cond}\n(slope={slope:.3f}, δ={delta:.2f})"
            
            sns.lineplot(data=combined, x="episode_idx", y="hitting_time", label=label, color=color, errorbar="sd")
            del combined
            gc.collect()

    plt.title(f"Averaged Hitting Times - {phase.replace('_', ' ').capitalize()}")
    plt.xlabel("Episode")
    plt.ylabel("Hitting Time (Rolling Mean 20 eps)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(ROOT_FIGURES, f"overlay_hitting_times_{phase}_mean_sd.pdf"))
    plt.close()

def compute_v2_stats(all_runs: List[Dict[str, Any]]):
    """Computes V2 metrics for all runs and returns a summary DataFrame."""
    results = []
    for i, run in enumerate(all_runs):
        if i % 50 == 0:
            print(f"Analyzing run {i+1}/{len(all_runs)}: {run['condition']} seed {run['seed']}")
        df = get_seed_logs(run)
        if df is not None:
            stats = analyze_seed_data(df)
            
            passes_accel = (
                stats['ht_slope'] < 0 and 
                stats['cliffs_delta'] < 0 and 
                (not np.isnan(stats['acceleration_ratio']) and stats['acceleration_ratio'] >= 1.25)
            )
            
            # Flatten or remove the params dict to avoid issues with DataFrame processing
            clean_run = {k: v for k, v in run.items() if k != "params"}
            res = {**clean_run, **stats, "passes_v2": passes_accel}
            results.append(res)
            del df
            if i % 100 == 0:
                gc.collect()
    return pd.DataFrame(results)

def generate_summary_report(stats_df: pd.DataFrame):
    """Generates validation_v2_summary.md and other summary files."""
    summary_path = os.path.join("validation_v2_summary.md")
    
    # Ensure no duplicates that might cause issues
    stats_df = stats_df.reset_index(drop=True)
    
    with open(summary_path, 'w') as f:
        f.write("# HCCDE Deep Validation Battery v2 Summary\n\n")
        
        f.write("## Pass Rates per Condition\n")
        f.write("> [!NOTE]\n> Acceleration is confirmed per-seed if: slope < 0, Cliff's delta < 0, and median late < 0.8 * median early.\n\n")
        
        # Group by phase and condition
        groups = stats_df.groupby(["phase", "condition"])
        
        # Calculate pass rates
        pass_summary = groups["passes_v2"].agg(['mean', 'count']).reset_index()
        pass_summary.columns = ["Phase", "Condition", "Pass Rate", "N"]
        f.write(pass_summary.to_markdown(index=False) + "\n\n")
        
        f.write("## Robust Metric Averages\n")
        # Aggregating only numeric columns
        numeric_cols = ["ht_slope", "acceleration_ratio", "cliffs_delta"]
        agg = groups[numeric_cols].mean().reset_index()
        f.write(agg.to_markdown(index=False) + "\n\n")

    stats_df.to_csv(os.path.join(ROOT_DATA, "v2_aggregate_stats.csv"), index=False)

def main():
    ensure_dirs()
    manifest_path = os.path.join(ROOT_DATA, "run_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"Manifest not found: {manifest_path}")
        return
        
    all_runs = load_all_runs(manifest_path)
    
    print("Computing V2 Statistics...")
    stats_df = compute_v2_stats(all_runs)
    
    print("Generating Summary Report...")
    generate_summary_report(stats_df)
    
    print("Generating Plots...")
    important_phases = sorted(stats_df['phase'].unique())
    for phase in important_phases:
        plot_hitting_times_overlay(all_runs, phase=phase)
        
    # Boxplots for power upgrade
    if "power_upgrade" in stats_df['phase'].values:
        plt.figure(figsize=(12, 7))
        sns.boxplot(data=stats_df[stats_df['phase']=='power_upgrade'], x="condition", y="ht_slope")
        plt.xticks(rotation=15)
        plt.title("Hitting Time Slopes - Power Upgrade")
        plt.savefig(os.path.join(ROOT_FIGURES, "slopes_boxplot_hitting_time_pu.pdf"))
        plt.close()

    print("V2 Analysis and Plotting Complete.")

if __name__ == "__main__":
    main()
