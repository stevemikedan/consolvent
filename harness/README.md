# Harness

Run the default falsification suite:

```bash
python -m harness.cli --test all
```

Run one discriminator:

```bash
python -m harness.cli --test memory_discriminator
python -m harness.cli --test storage_positive_control
python -m harness.cli --test attractor_discriminator
python -m harness.cli --test attractor_positive_control
python -m harness.cli --test hysteresis_without_storage
```

For each run, the harness:

1. Builds model predictions from the run spec.
2. Writes a hash and timestamped pre-registration record.
3. Executes the sim.
4. Logs the outcome.
5. Rebuilds the disagreement-only scoreboard.

The positive controls are intentional. They prove the harness can record HCCDE losses when the generated system contains readable storage or attractor-only reachability.
