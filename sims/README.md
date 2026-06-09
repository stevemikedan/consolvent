# Sims

Toy systems expose history, current state, and dynamics as independent knobs.

The first discriminator sim is `HistoryGatedGraphSim`:

- `history`: `neutral`, `north_channel`, `south_channel`, `east_channel`
- `current_state`: normally `pivot`; storage controls can use `pivot|memory=<history>`
- `dynamics`: `uniform_proposal` for constraint training, `attractor_only` for controls

The sim does not use a history-to-closure lookup table. It trains a constraint field from an exposure script, measures which transitions cross the closure threshold, computes reachability from those measured closures, and separately runs a decoder against current-state memory.

That means HCCDE can lose:

- if current state contains readable storage, the decoder can reconstruct history;
- if `attractor_only` dynamics are used, histories do not reshape reachable sets.
