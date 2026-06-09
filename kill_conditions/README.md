# Kill Conditions

This project is a falsification harness, not an HCCDE illustration.

HCCDE should lose when an outcome is better explained by storage, ordinary attractors, or post-hoc interpretation. A run only counts on prediction keys that were pre-registered before execution.

## HCCDE Kill Conditions

1. **Storage kill condition**
   - HCCDE loses if the past trajectory is reconstructable from the current state.
   - Interpretation: the effect is stored memory, not history-conditioned constraint evolution.

2. **No history-shaped reachability kill condition**
   - HCCDE loses if different histories under identical current state and identical dynamics give identical reachable sets.
   - Interpretation: history did not reshape the future state space.

3. **Readable-value kill condition**
   - HCCDE loses if hysteresis is carried by a readable stored value rather than by transition narrowing.
   - Interpretation: the persistence is memory, not constraint closure.

## HCCDI Kill Condition

HCCDI loses if framed construals collapse to evidence as fast as unframed construals.

Interpretation: the frame caused ordinary bias, not narrowed construal space. Bias should bend to evidence; narrowed space should make alternatives unavailable or slower to recover.

## Operational Rule

Every falsification run must:

1. Separate history, current state, and dynamics in the sim setup.
2. Generate HCCDE and rival predictions before execution.
3. Write a hash and timestamped pre-registration record before observing the outcome.
4. Score HCCDE only against rivals that disagreed with it before the run.

