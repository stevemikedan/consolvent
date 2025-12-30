import numpy as np
from scipy import stats
from sklearn.linear_model import TheilSenRegressor

def compute_theilsen_slope(x, y):
    """Computes the robust slope using Theil-Sen regression."""
    if len(x) < 2:
        return 0.0
    x = np.array(x).reshape(-1, 1)
    y = np.array(y)
    model = TheilSenRegressor(random_state=42)
    model.fit(x, y)
    return float(model.coef_[0])

def compute_cliffs_delta(x, y):
    """
    Computes Cliff's delta effect size.
    d = (number of times x_i > y_j - number of times x_i < y_j) / (n1 * n2)
    """
    n1 = len(x)
    n2 = len(y)
    if n1 == 0 or n2 == 0:
        return 0.0
    
    # Efficient calculation using broadcasting or loops
    # x is early, y is late. Cliffs logic in prompt: "late minus early" direction
    # Prompt says: "Cliff’s delta indicates late < early (negative in the 'late minus early' direction)"
    # Standard formula for d(X, Y) where X is group 1 and Y is group 2:
    # d = sum(sign(x_i - y_j)) / (n1 * n2)
    # If we want late < early to be negative:
    # d = sum(sign(y_j - x_i)) / (n1 * n2)  where x is early, y is late.
    
    diffs = np.subtract.outer(y, x)
    d = np.sum(np.sign(diffs)) / (n1 * n2)
    return float(d)

def compute_mann_whitney_u(x, y):
    """Computes Mann-Whitney U test p-value."""
    if len(x) == 0 or len(y) == 0:
        return 1.0
    res = stats.mannwhitneyu(x, y, alternative='two-sided')
    return float(res.pvalue)

def analyze_seed_data(df, early_frac=0.2, late_frac=0.2):
    """
    Performs the full suite of V2 metrics for a single seed's log.
    Uses proportional windows for early/late comparison.
    """
    episodes = df['episode_idx'].values
    ht = df['hitting_time'].values
    entropy = df['path_entropy'].values
    
    ht_slope = compute_theilsen_slope(episodes, ht)
    entropy_slope = compute_theilsen_slope(episodes, entropy)
    
    n_eps = len(episodes)
    n_early = int(n_eps * early_frac)
    n_late = int(n_eps * late_frac)
    
    early_ht = ht[:n_early]
    late_ht = ht[-n_late:]
    
    if len(early_ht) > 0 and len(late_ht) > 0:
        median_early = np.median(early_ht)
        median_late = np.median(late_ht)
        # Handle median_late = 0 (rare but possible)
        acc_ratio = median_early / median_late if median_late > 0 else (median_early + 1e-6)
        cliff_d = compute_cliffs_delta(early_ht, late_ht)
        mw_p = compute_mann_whitney_u(early_ht, late_ht)
    else:
        median_early = median_late = acc_ratio = cliff_d = mw_p = np.nan
        
    return {
        "ht_slope": ht_slope,
        "entropy_slope": entropy_slope,
        "median_early": median_early,
        "median_late": median_late,
        "acceleration_ratio": acc_ratio,
        "cliffs_delta": cliff_d,
        "mann_whitney_p": mw_p
    }
