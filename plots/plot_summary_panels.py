import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validation", type=str, choices=["v1", "v2"], default="v2")
    return parser.parse_args()

def plot_slopes(df, out_path):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="condition", y="ht_slope_theilsen", palette="husl")
    plt.axhline(0, color='red', linestyle='--', label='No trend')
    
    # Add numeric summary to title
    baseline_slope = df[df['condition'].str.contains('baseline', case=False, na=False)]['ht_slope_theilsen'].median()
    plt.title(f"Hitting Time Slopes by Condition\\nBaseline median slope = {baseline_slope:.4f}")
    plt.xlabel("Condition")
    plt.ylabel("Theil-Sen Slope")
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_effect_sizes(df, out_path):
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df, x="condition", y="cliffs_delta_ht", palette="husl")
    plt.axhline(0, color='red', linestyle='--', label='No effect')
    
    # Add numeric summary to title
    baseline_delta = df[df['condition'].str.contains('baseline', case=False, na=False)]['cliffs_delta_ht'].median()
    plt.title(f"Cliff's Delta Effect Sizes by Condition\\nBaseline median \u03b4 = {baseline_delta:.3f}")
    plt.xlabel("Condition")
    plt.ylabel("Cliff's Delta (late vs early)")
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_ecdf(version, out_path):
    # This requires reading individual log files. Let's pick baseline seed 1 and random_evolution seed 1
    baseline_path = f"data/episodes/{version}/baseline/{version}_baseline_s1_episodes.csv"
    random_path = f"data/episodes/{version}/random_evolution/{version}_random_evolution_s1_episodes.csv"
    
    if not os.path.exists(baseline_path) or not os.path.exists(random_path):
        print("Required logs for ECDF not found.")
        return
        
    df_b = pd.read_csv(baseline_path)
    df_r = pd.read_csv(random_path)
    
    if version == "v2":
        early_b = df_b.iloc[0:200]['hitting_time']
        late_b = df_b.iloc[800:1000]['hitting_time']
        early_r = df_r.iloc[0:200]['hitting_time']
        late_r = df_r.iloc[800:1000]['hitting_time']
    else:
        early_b = df_b.iloc[0:20]['hitting_time']
        late_b = df_b.iloc[80:100]['hitting_time']
        early_r = df_r.iloc[0:20]['hitting_time']
        late_r = df_r.iloc[80:100]['hitting_time']

    plt.figure(figsize=(10, 6))
    sns.ecdfplot(early_b, label="Baseline Early", color="blue", linestyle="--")
    sns.ecdfplot(late_b, label="Baseline Late", color="blue", linestyle="-")
    sns.ecdfplot(early_r, label="Random Early", color="gray", linestyle="--")
    sns.ecdfplot(late_r, label="Random Late", color="gray", linestyle="-")
    
    plt.title(f"ECDF: Early vs Late Hitting Times ({version})")
    plt.xlabel("Steps to Target")
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def main():
    args = parse_args()
    summary_path = f"analysis_outputs/{args.validation}/per_seed_summary.csv"
    if not os.path.exists(summary_path):
        print(f"Summary not found: {summary_path}")
        return
        
    df = pd.read_csv(summary_path)
    fig_dir = f"paper_figures/{args.validation}"
    os.makedirs(fig_dir, exist_ok=True)
    
    print("Generating slope panel...")
    plot_slopes(df, f"{fig_dir}/summary_panel_slopes.pdf")
    
    print("Generating effect size panel...")
    plot_effect_sizes(df, f"{fig_dir}/summary_panel_effect_sizes.pdf")
    
    print("Generating ECDF plot...")
    plot_ecdf(args.validation, f"{fig_dir}/summary_panel_ecdf_early_late.pdf")
    
    print("Done.")

if __name__ == "__main__":
    main()
