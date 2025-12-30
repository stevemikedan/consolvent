import random
import numpy as np
from .state_space import StateSpace
from .constraints import ConstraintField

class Dynamics:
    """
    Implements the fixed proposal dynamics and constraint-gated acceptance rule.
    """
    def __init__(self, beta: float = 5.0):
        self.beta = beta

    def propose(self, state_space: StateSpace, current_node: int) -> int:
        """
        Proposes a transition to a neighbor using a fixed uniform distribution.
        Micro-dynamics invariance: This distribution never changes.
        """
        neighbors = state_space.get_neighbors(current_node)
        if not neighbors:
            return current_node
        return random.choice(neighbors)

    def evaluate_acceptance(self, u: int, v: int, constraints: ConstraintField) -> bool:
        """
        Acceptance rule (Constraint-Gated):
        P(accept) = exp(-beta * C_{i -> j})
        """
        c_val = constraints.get_constraint(u, v)
        p_accept = np.exp(-self.beta * c_val)
        return random.random() < p_accept

    def step(self, state_space: StateSpace, constraints: ConstraintField) -> tuple[int, int, bool]:
        """
        Performs one step: propose then evaluate acceptance.
        Returns (current_node, proposed_node, accepted).
        """
        u = state_space.current_state
        v = self.propose(state_space, u)
        accepted = self.evaluate_acceptance(u, v, constraints)
        
        if accepted:
            state_space.set_state(v)
            
        return u, v, accepted
