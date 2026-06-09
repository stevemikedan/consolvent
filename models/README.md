# Models

Predictors implement the same interface and produce pre-registerable claims.

Current predictors:

- `HCCDEPredictor`: history narrows future transitions without readable storage.
- `StoredMemoryPredictor`: past trajectory should be readable; future transitions remain open.
- `AttractorPredictor`: current state and dynamics determine reachability; history should not reshape basins.

