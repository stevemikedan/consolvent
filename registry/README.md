# Registry

`registry/predictions/` stores pre-registered prediction records.

The harness writes these records before executing a sim. Each record contains:

- UTC timestamp
- current git `HEAD`
- run specification
- model predictions
- SHA-256 hash over the canonical JSON payload

Do not edit records after a run. If a prediction changes, create a new run id and a new pre-registration record.

