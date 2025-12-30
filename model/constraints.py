import numpy as np
from typing import List, Tuple, Dict

class ConstraintField:
    """
    Manages the edge-based constraint matrix C_{i -> j}.
    Constraints gate transition acceptance and evolve based on history.
    """
    def __init__(self, edges: List[Tuple[int, int]], c_min: float = 0.1, c_max: float = 1.0, 
                 initial_val: float = None):
        self.c_min = c_min
        self.c_max = c_max
        # Map edge tuples to indices for efficient matrix/array operations if needed, 
        # but for clarity let's use a dictionary or a sparse-like structure
        self.constraints: Dict[Tuple[int, int], float] = {}
        
        default_val = initial_val if initial_val is not None else c_max
        for edge in edges:
            self.constraints[edge] = default_val

    def get_constraint(self, u: int, v: int) -> float:
        """Returns the constraint value for edge (u -> v)."""
        return self.constraints.get((u, v), self.c_max)

    def update_local(self, u: int, v: int, lmbda: float):
        """
        Local relaxation (channel carving):
        C_{i -> j} <- (1 - lambda) * C_{i -> j} + lambda * C_min
        """
        if (u, v) in self.constraints:
            old_val = self.constraints[(u, v)]
            self.constraints[(u, v)] = (1 - lmbda) * old_val + lmbda * self.c_min

    def update_global(self, accepted_u: int, accepted_v: int, mu: float):
        """
        Optional global stabilization (non-used edges):
        C_{u -> v} <- (1 - mu) * C_{u -> v} + mu * C_max for (u -> v) != (i -> j)
        """
        if mu <= 0:
            return
            
        for edge in self.constraints:
            if edge != (accepted_u, accepted_v):
                old_val = self.constraints[edge]
                self.constraints[edge] = (1 - mu) * old_val + mu * self.c_max

    def get_all_constraints(self) -> Dict[Tuple[int, int], float]:
        """Returns a copy of all current constraints."""
        return self.constraints.copy()

    def get_summary_stats(self) -> Dict[str, float]:
        """Returns summary statistics of the constraint field."""
        vals = list(self.constraints.values())
        return {
            "mean": float(np.mean(vals)),
            "std": float(np.std(vals)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals)),
            "entropy": float(self.calculate_field_entropy())
        }

    def calculate_field_entropy(self) -> float:
        """Calculates Shannon entropy of the constraint distribution itself."""
        vals = np.array(list(self.constraints.values()))
        # Normalize to a distribution for entropy calculation
        if vals.sum() == 0: return 0.0
        probs = vals / vals.sum()
        entropy = -np.sum(probs * np.log(probs + 1e-12))
        return float(entropy)

    def save_constraints(self, filepath: str):
        """Saves current constraints to a JSON file."""
        import json
        serializable = {f"{k[0]}->{k[1]}": v for k, v in self.constraints.items()}
        with open(filepath, 'w') as f:
            json.dump(serializable, f)
