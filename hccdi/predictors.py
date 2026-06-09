"""HCCDI and ordinary-bias predictions for the frame task."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from hccdi.frame_task import FrameTaskSpec


@dataclass(frozen=True)
class HCCDIPrediction:
    model_id: str
    run_id: str
    claims: Dict[str, Any]
    rationale: str
    falsifies_if: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HCCDIPredictor:
    model_id = "hccdi"

    def predict(self, spec: FrameTaskSpec) -> HCCDIPrediction:
        return HCCDIPrediction(
            model_id=self.model_id,
            run_id=spec.run_id,
            claims={
                "construal_direction": spec.prior,
                "truth_relation_correct": spec.prior == spec.ground_truth,
                "framed_collapse_rate_equals_unframed": False,
                "correction_resistance_increases_with_narrowing": True,
            },
            rationale=(
                "The frame narrows construal space before exposure. The construal can be "
                "scored against ground truth and should resist correction in proportion to narrowing."
            ),
            falsifies_if=[
                "Framed construals collapse to evidence as fast as unframed construals.",
                "Resistance to correction does not increase with narrowing strength.",
            ],
        )


class OrdinaryBiasPredictor:
    model_id = "ordinary_bias"

    def predict(self, spec: FrameTaskSpec) -> HCCDIPrediction:
        return HCCDIPrediction(
            model_id=self.model_id,
            run_id=spec.run_id,
            claims={
                "construal_direction": spec.prior,
                "framed_collapse_rate_equals_unframed": True,
                "correction_resistance_increases_with_narrowing": False,
            },
            rationale=(
                "The frame is a bias on initial interpretation. Sufficient evidence should correct "
                "it at the same rate as an unframed condition."
            ),
            falsifies_if=[
                "Correction remains slower after evidence is available.",
                "Alternatives become unavailable rather than merely less likely.",
            ],
        )

