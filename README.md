# HCCDE: History-Conditioned Constraint-Driven Evolution

This repository contains the toy model and validation batteries for HCCDE.

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
