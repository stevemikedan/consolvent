# Consolvent: HCCDE Falsification Harness

This repository tests History-Conditioned Constraint-Driven Evolution (HCCDE) by trying to kill it, not by illustrating it.

The core rule: if a run cannot produce a result that would make HCCDE lose to a rival model, the run does not count as evidence.

## Falsification Workflow

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the default discriminator suite:

```bash
python -m harness.cli --test all
```

The default suite contains both discriminator runs and positive controls:

- `memory_discriminator`: constraint dynamics with no readable storage.
- `storage_positive_control`: readable current-state memory with no transition closure, where HCCDE should lose to the memory model.
- `attractor_discriminator`: identical current state and dynamics with different histories, where measured reachability should differ if constraints narrow.
- `attractor_positive_control`: attractor-only dynamics, where HCCDE should lose if histories do not reshape reachability.
- `hysteresis_without_storage`: constraint persistence after the training condition is removed.

Run the smoke tests:

```bash
python test_falsification_harness.py
```

The harness:

1. Separates history, current state, and dynamics in each sim.
2. Generates side-by-side predictions from HCCDE and rivals.
3. Pre-registers predictions with a timestamp and hash before execution.
4. Runs the sim and logs the observed outcome.
5. Scores HCCDE against rivals only on disagreement cases.

The sim must measure observables from generated state. It must not declare HCCDE claims as ground truth, and predictors must not read the sim's realized answer key.

## Repository Map

- `sims/`: toy systems with history, state, and dynamics exposed as separate knobs.
- `models/`: HCCDE, stored-memory, attractor, and related predictors.
- `harness/`: pre-register, run, score, and log falsification tests.
- `registry/`: immutable prediction records written before runs.
- `scoreboard/`: HCCDE win/loss/tie results against rivals.
- `kill_conditions/`: written falsification conditions.
- `hccdi/`: separate frame/prior construal tests.
- `model/`, `experiments/`, `metrics/`, `analysis/`: earlier simulator, validation, and reporting code.

Generated experiment data, analysis outputs, and paper figures are local artifacts. The repo keeps README placeholders for those directories; regenerate bulk outputs instead of committing them by default.

## Kill Conditions

HCCDE loses if:

- the past trajectory is reconstructable from current state;
- different histories under identical dynamics give identical reachable sets;
- hysteresis is carried by a readable stored value rather than by transition narrowing.

HCCDI loses if framed construals collapse to evidence as fast as unframed construals.

## Analytics Upgrade Workflow

To update all standardized logs, generate summary tables, and produce summary plots, run:

```bash
make reify
```

Or run individual steps:

1. **Standardize Logs**: `make migrate`
2. **Generate Summaries**: `make all-analysis`
3. **Generate Plots**: `make plots`

### Analytics Outputs
- `analysis_outputs/v1/`: Per-seed and per-condition summaries for v1.
- `analysis_outputs/v2/`: Per-seed and per-condition summaries for v2.
- `analysis_outputs/reconciliation_v1_v2.md`: A summary reconciling v1 and v2 results.
- `paper_figures/`: Enhanced plots including slope panels and ECDF curves.
