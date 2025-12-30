import pandas as pd
import numpy as np
import json
import os

def analyze_and_log():
    results = {}
    dirs = {
        "standard": "data",
        "no_evolution": "data/control_no_evolution",
        "random_evolution": "data/control_random_evolution",
        "high_decay": "data/control_high_decay"
    }
    
    for key, d in dirs.items():
        csv_path = os.path.join(d, "episode_logs.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            # Simple linear regression slope to check for acceleration (negative slope)
            if len(df) > 1:
                slope = np.polyfit(df['episode'], df['hitting_time'], 1)[0]
                results[key] = {
                    "slope": float(slope),
                    "acceleration_detected": bool(slope < 0),
                    "mean_hitting_time": float(df['hitting_time'].mean())
                }
    
    failure_log = {
        "parameter_regimes": {
            "size": 100,
            "beta": 5.0,
            "lambda": 0.1,
            "mu_standard": 0.01,
            "mu_high_decay": 0.8
        },
        "results": results,
        "interpretations": {
            "standard": "Expect negative slope (acceleration). Possible saturation if episodes > 500.",
            "no_evolution": "Expect near-zero slope. No mechanism for acceleration.",
            "random_evolution": "Expect near-zero slope. Relaxation not tied to usage.",
            "high_decay": "Expect near-zero or positive slope. History erased by high stabilization."
        }
    }
    
    with open("data/failure_modes.json", 'w') as f:
        json.dump(failure_log, f, indent=4)
    print("Failure modes logged to data/failure_modes.json")

if __name__ == "__main__":
    analyze_and_log()
