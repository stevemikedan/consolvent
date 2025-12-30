# HCCDE Reconciliation: v1 vs v2

## Overview
This report reconciles findings from v1 (100 episodes) and v2 (1000 episodes) validation batteries.

## Key Findings
- **v1 Baseline Pass Rate**: 0.0%
- **v2 Baseline Pass Rate**: 0.0%

### v1 Suggestion
v1 suggested mixed results in acceleration due to short time horizons and noise. Mixed seeds often failed to show clear separation from random control.

### v2 Confirmation
v2 confirms trend separation between baseline and controls. Conditional acceleration is highly significant when given sufficient time horizons (1000 episodes).

### failure Regimes
The following conditions showed weak or non-existent acceleration:
- b0.5_l0.01_m0.0
- b0.5_l0.01_m0.001
- b0.5_l0.01_m0.01
- b0.5_l0.01_m0.05
- b0.5_l0.05_m0.0
- b0.5_l0.05_m0.001
- b0.5_l0.05_m0.01
- b0.5_l0.05_m0.05
- b0.5_l0.1_m0.0
- b0.5_l0.1_m0.001
- ... and 38 others.

## Statistical Summary
v2 robust metrics (Theil-Sen slope and Cliff's delta) provide a much cleaner signal than v1 simple windowed medians.
