"""Measured toy graph for HCCDE discriminator tests.

This sim intentionally separates three things:

- history: an exposure script that trains the system before measurement
- current state: the node and any readable state carried into measurement
- dynamics: the update rule that turns exposure into later reachability

The observed values are measured from the generated system state. They are not
declared as HCCDE facts, and the predictors do not get access to the realized
constraint field before pre-registration.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Set, Tuple

from sims.base import RunSpec, SimOutcome, normalize_edges

Edge = Tuple[str, str]


@dataclass(frozen=True)
class CurrentState:
    node: str
    readable_memory: Optional[str] = None


class HistoryGatedGraphSim:
    """Toy graph with independent history, state, and dynamics knobs."""

    sim_id = "history_gated_graph"

    EDGES: Set[Edge] = {
        ("pivot", "north"),
        ("pivot", "south"),
        ("pivot", "east"),
        ("north", "north_goal"),
        ("south", "south_goal"),
        ("east", "east_goal"),
    }

    HISTORY_SCRIPTS: Dict[str, Tuple[Edge, ...]] = {
        "neutral": tuple(),
        "north_channel": (("pivot", "north"), ("north", "north_goal")),
        "south_channel": (("pivot", "south"), ("south", "south_goal")),
        "east_channel": (("pivot", "east"), ("east", "east_goal")),
    }

    def __init__(
        self,
        training_repetitions: int = 10,
        initial_constraint: float = 0.35,
        open_rate: float = 0.08,
        unused_close_rate: float = 0.04,
        closure_threshold: float = 0.70,
    ):
        self.training_repetitions = training_repetitions
        self.initial_constraint = initial_constraint
        self.open_rate = open_rate
        self.unused_close_rate = unused_close_rate
        self.closure_threshold = closure_threshold

    def run(self, spec: RunSpec) -> SimOutcome:
        if spec.sim_id != self.sim_id:
            raise ValueError(f"RunSpec sim_id {spec.sim_id!r} does not match {self.sim_id!r}.")

        current_state = self._parse_current_state(spec.current_state)
        constraints = self._generate_constraints(spec.history, spec.dynamics)
        closed_edges = self._measure_closed_edges(constraints)
        reachable_set = self._reachable_from(current_state.node, closed_edges)

        comparison_reachable_set = None
        reachable_differs = False
        if spec.comparison_history:
            comparison_constraints = self._generate_constraints(
                spec.comparison_history,
                spec.dynamics,
            )
            comparison_closed_edges = self._measure_closed_edges(comparison_constraints)
            comparison_reachable = self._reachable_from(current_state.node, comparison_closed_edges)
            comparison_reachable_set = sorted(comparison_reachable)
            reachable_differs = reachable_set != comparison_reachable

        decoded_history = self._decode_history_from_current_state(current_state)
        memory_present = decoded_history is not None
        future_closed = bool(closed_edges)

        observed = {
            "state_decoder_prediction": decoded_history,
            "state_decoder_correct": decoded_history == spec.history,
            "past_trajectory_reconstructable_from_current_state": decoded_history == spec.history,
            "readable_memory_value_present": memory_present,
            "future_transitions_closed": future_closed,
            "closed_transitions": normalize_edges(closed_edges),
            "reachable_set": sorted(reachable_set),
            "comparison_history": spec.comparison_history,
            "comparison_reachable_set": comparison_reachable_set,
            "reachable_set_differs_by_history": reachable_differs,
            "training_conditions_removed": spec.remove_training_conditions,
            "hysteresis_persists_after_condition_removed": bool(
                spec.remove_training_conditions and future_closed
            ),
            "narrowing_not_storage": bool(future_closed and not memory_present),
            "constraint_summary": self._constraint_summary(constraints),
        }

        return SimOutcome(
            run_id=spec.run_id,
            test_id=spec.test_id,
            sim_id=self.sim_id,
            observed=observed,
        )

    def _generate_constraints(self, history: str, dynamics: str) -> Dict[Edge, float]:
        if history not in self.HISTORY_SCRIPTS:
            known = ", ".join(sorted(self.HISTORY_SCRIPTS))
            raise ValueError(f"Unknown history {history!r}. Known histories: {known}")

        constraints = {edge: self.initial_constraint for edge in self.EDGES}

        if dynamics == "attractor_only":
            return constraints
        if dynamics != "uniform_proposal":
            raise ValueError("Supported dynamics: uniform_proposal, attractor_only")

        script = self.HISTORY_SCRIPTS[history]
        for _ in range(self.training_repetitions):
            used_edges = set(script)
            for edge in self.EDGES:
                if edge in used_edges:
                    constraints[edge] = max(0.0, constraints[edge] - self.open_rate)
                else:
                    constraints[edge] = min(1.0, constraints[edge] + self.unused_close_rate)

        return constraints

    def _measure_closed_edges(self, constraints: Dict[Edge, float]) -> Set[Edge]:
        return {edge for edge, value in constraints.items() if value >= self.closure_threshold}

    def _constraint_summary(self, constraints: Dict[Edge, float]) -> Dict[str, float]:
        values = list(constraints.values())
        return {
            "min": min(values),
            "max": max(values),
            "mean": sum(values) / len(values),
            "closure_threshold": self.closure_threshold,
        }

    def _parse_current_state(self, raw_state: str) -> CurrentState:
        node, _, raw_metadata = raw_state.partition("|")
        readable_memory = None
        if raw_metadata.startswith("memory="):
            readable_memory = raw_metadata.removeprefix("memory=")
        return CurrentState(node=node, readable_memory=readable_memory)

    def _decode_history_from_current_state(self, state: CurrentState) -> Optional[str]:
        if state.readable_memory in self.HISTORY_SCRIPTS:
            return state.readable_memory
        return None

    @classmethod
    def _reachable_from(cls, start: str, closed_edges: Iterable[Edge]) -> Set[str]:
        closed = set(closed_edges)
        reachable = {start}
        queue = deque([start])

        while queue:
            node = queue.popleft()
            for source, target in cls.EDGES:
                if source != node or (source, target) in closed:
                    continue
                if target not in reachable:
                    reachable.add(target)
                    queue.append(target)

        return reachable
