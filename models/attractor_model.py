"""Plain attractor rival model predictions."""

from __future__ import annotations

from models.base import Prediction
from sims.base import RunSpec


class AttractorPredictor:
    model_id = "plain_attractor"

    def predict(self, spec: RunSpec) -> Prediction:
        claims = {
            "future_transitions_closed": False,
        }

        if spec.comparison_history:
            claims["reachable_set_differs_by_history"] = False

        if spec.remove_training_conditions:
            claims["hysteresis_persists_after_condition_removed"] = False

        return Prediction(
            model_id=self.model_id,
            test_id=spec.test_id,
            run_id=spec.run_id,
            claims=claims,
            rationale=(
                "Reachability is determined by the present state and fixed dynamics. "
                "If those are identical, prior history should not reshape the basin."
            ),
            falsifies_if=[
                "Identical current state and dynamics produce history-specific reachable sets.",
                "Transitions remain closed after the training condition is removed.",
            ],
        )
