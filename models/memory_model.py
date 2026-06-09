"""Stored-memory rival model predictions."""

from __future__ import annotations

from models.base import Prediction
from sims.base import RunSpec


class StoredMemoryPredictor:
    model_id = "stored_memory"

    def predict(self, spec: RunSpec) -> Prediction:
        should_store_history = spec.history != "neutral"
        claims = {
            "past_trajectory_reconstructable_from_current_state": should_store_history,
            "readable_memory_value_present": should_store_history,
            "future_transitions_closed": False,
        }

        if spec.remove_training_conditions:
            claims["hysteresis_persists_after_condition_removed"] = True
            claims["narrowing_not_storage"] = False

        return Prediction(
            model_id=self.model_id,
            test_id=spec.test_id,
            run_id=spec.run_id,
            claims=claims,
            rationale=(
                "The effect is attributed to a stored record. The past should be readable, "
                "and future transitions remain open unless the stored value drives choice."
            ),
            falsifies_if=[
                "No readable record is present.",
                "Future transitions are physically or logically closed rather than merely selected against.",
            ],
        )
