# Sims

Toy systems expose history, current state, and dynamics as independent knobs.

The first discriminator sim is `HistoryGatedGraphSim`:

- `history`: `neutral`, `north_channel`, `south_channel`, `east_channel`
- `current_state`: normally `pivot`
- `dynamics`: currently fixed as `uniform_proposal`

The current state does not store a readable trajectory. History changes which future transitions are closed.

