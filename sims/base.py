"""Shared data structures for falsification sims."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class RunSpec:
    """A pre-run specification with history, state, and dynamics as separate knobs."""

    test_id: str
    run_id: str
    sim_id: str
    history: str
    current_state: str
    dynamics: str
    comparison_history: Optional[str] = None
    remove_training_conditions: bool = False
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SimOutcome:
    """Observed result from a sim run."""

    run_id: str
    test_id: str
    sim_id: str
    observed: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def edge_id(source: str, target: str) -> str:
    return f"{source}->{target}"


def normalize_edges(edges: set[tuple[str, str]]) -> list[str]:
    return sorted(edge_id(source, target) for source, target in edges)

