"""HCCDE predictions for discriminator tests."""

from __future__ import annotations

from models.base import Prediction
from sims.base import RunSpec


class HCCDEPredictor:
    model_id = "hccde"

    def predict(self, spec: RunSpec) -> Prediction:
        claims = {
            "past_trajectory_reconstructable_from_current_state": False,
            "readable_memory_value_present": False,
            "future_transitions_closed": spec.history != "neutral",
        }

        if spec.comparison_history:
            claims["reachable_set_differs_by_history"] = spec.history != spec.comparison_history

        if spec.remove_training_conditions:
            claims["hysteresis_persists_after_condition_removed"] = spec.history != "neutral"
            claims["narrowing_not_storage"] = spec.history != "neutral"

        return Prediction(
            model_id=self.model_id,
            test_id=spec.test_id,
            run_id=spec.run_id,
            claims=claims,
            rationale=(
                "History should alter constraints, not leave a retrievable record. "
                "The current state can remain identical while future transitions narrow."
            ),
            falsifies_if=[
                "Past trajectory is reconstructable from current state.",
                "History-conditioned closures do not appear in future transitions.",
                "Different histories under identical dynamics do not change reachable sets.",
            ],
        )
