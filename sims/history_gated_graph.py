"""A minimal sim where history, current state, and dynamics are separable.

The current state is deliberately uninformative about the prior trajectory. History
changes only the constraint field: it closes future transitions without exposing a
stored record. This makes it useful for discriminator tests, not as a proof of HCCDE.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, Set, Tuple

from sims.base import RunSpec, SimOutcome, normalize_edges

Edge = Tuple[str, str]


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

    HISTORY_CLOSURES: Dict[str, Set[Edge]] = {
        "neutral": set(),
        "north_channel": {("pivot", "south"), ("south", "south_goal")},
        "south_channel": {("pivot", "north"), ("north", "north_goal")},
        "east_channel": {("pivot", "north"), ("pivot", "south")},
    }

    def run(self, spec: RunSpec) -> SimOutcome:
        if spec.sim_id != self.sim_id:
            raise ValueError(f"RunSpec sim_id {spec.sim_id!r} does not match {self.sim_id!r}.")
        if spec.dynamics != "uniform_proposal":
            raise ValueError("This sim currently exposes one fixed dynamics profile: uniform_proposal.")

        closed_edges = self._closed_edges_for(spec.history)
        reachable_set = self._reachable_from(spec.current_state, closed_edges)

        comparison_reachable_set = None
        reachable_differs = False
        if spec.comparison_history:
            comparison_closed = self._closed_edges_for(spec.comparison_history)
            comparison_reachable = self._reachable_from(spec.current_state, comparison_closed)
            comparison_reachable_set = sorted(comparison_reachable)
            reachable_differs = reachable_set != comparison_reachable

        observed = {
            "past_trajectory_reconstructable_from_current_state": False,
            "readable_memory_value_present": False,
            "future_transitions_closed": bool(closed_edges),
            "closed_transitions": normalize_edges(closed_edges),
            "reachable_set": sorted(reachable_set),
            "comparison_history": spec.comparison_history,
            "comparison_reachable_set": comparison_reachable_set,
            "reachable_set_differs_by_history": reachable_differs,
            "training_conditions_removed": spec.remove_training_conditions,
            "hysteresis_persists_after_condition_removed": bool(
                spec.remove_training_conditions and closed_edges
            ),
            "narrowing_not_storage": bool(closed_edges),
        }

        return SimOutcome(
            run_id=spec.run_id,
            test_id=spec.test_id,
            sim_id=self.sim_id,
            observed=observed,
        )

    @classmethod
    def expected_closed_transitions(cls, history: str) -> list[str]:
        return normalize_edges(cls._closed_edges_for(history))

    @classmethod
    def _closed_edges_for(cls, history: str) -> Set[Edge]:
        if history not in cls.HISTORY_CLOSURES:
            known = ", ".join(sorted(cls.HISTORY_CLOSURES))
            raise ValueError(f"Unknown history {history!r}. Known histories: {known}")
        return set(cls.HISTORY_CLOSURES[history])

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

