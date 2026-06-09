# Models

Predictors implement the same interface and produce pre-registerable claims.

Current predictors:

- `HCCDEPredictor`: history narrows future transitions without readable storage.
- `StoredMemoryPredictor`: past trajectory should be readable; future transitions remain open.
- `AttractorPredictor`: current state and dynamics determine reachability; history should not reshape basins.

Predictors make claims from the run specification only. They must not call sim methods that expose the realized closure set or measured outcome.
