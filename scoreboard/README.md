# Scoreboard

The scoreboard tracks HCCDE against rivals only where they made different pre-run predictions.

`scoreboard/runs/` contains individual run records. `scoreboard/results.json` is rebuilt from those records.

Counts:

- `hccde_win`: HCCDE had more correct disagreement keys than the rival.
- `hccde_loss`: the rival had more correct disagreement keys than HCCDE.
- `tie`: neither model separated on the observed disagreement keys.

