"""Shared prediction model interface."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Protocol

from sims.base import RunSpec


@dataclass(frozen=True)
class Prediction:
    """A model prediction that can be pre-registered before a sim runs."""

    model_id: str
    test_id: str
    run_id: str
    claims: Dict[str, Any]
    rationale: str
    falsifies_if: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class Predictor(Protocol):
    model_id: str

    def predict(self, spec: RunSpec) -> Prediction:
        ...

