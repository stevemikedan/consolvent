"""Frame/prior construal test with a truth relation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class FrameTaskSpec:
    run_id: str
    prior: str
    ambiguous_stimulus: str
    ground_truth: str
    narrowing_strength: float
    evidence_steps: int
    evidence_strength: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FrameTaskOutcome:
    run_id: str
    observed: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FrameConstrueSim:
    """Toy HCCDI task: prior sets construal, evidence tests correction resistance."""

    def run(self, spec: FrameTaskSpec) -> FrameTaskOutcome:
        if spec.prior not in {"threat", "benign"}:
            raise ValueError("prior must be 'threat' or 'benign'.")
        if spec.ground_truth not in {"threat", "benign"}:
            raise ValueError("ground_truth must be 'threat' or 'benign'.")
        if not 0.0 <= spec.narrowing_strength <= 1.0:
            raise ValueError("narrowing_strength must be between 0 and 1.")

        unframed_correction_steps = self._correction_steps(
            prior=None,
            ground_truth=spec.ground_truth,
            evidence_steps=spec.evidence_steps,
            evidence_strength=spec.evidence_strength,
        )
        framed_correction_steps = self._correction_steps(
            prior=spec.prior,
            ground_truth=spec.ground_truth,
            evidence_steps=spec.evidence_steps,
            evidence_strength=spec.evidence_strength,
            narrowing_strength=spec.narrowing_strength,
        )

        observed = {
            "construal_direction": spec.prior,
            "truth_relation_correct": spec.prior == spec.ground_truth,
            "framed_correction_steps": framed_correction_steps,
            "unframed_correction_steps": unframed_correction_steps,
            "framed_collapse_rate_equals_unframed": framed_correction_steps == unframed_correction_steps,
            "correction_resistance_increases_with_narrowing": framed_correction_steps > unframed_correction_steps,
        }
        return FrameTaskOutcome(run_id=spec.run_id, observed=observed)

    def _correction_steps(
        self,
        prior: str | None,
        ground_truth: str,
        evidence_steps: int,
        evidence_strength: float,
        narrowing_strength: float = 0.0,
    ) -> int:
        """Measure correction by iterating log-odds updates from evidence."""

        log_odds_threat = 0.0
        if prior == "threat":
            log_odds_threat = 3.0 * narrowing_strength
        elif prior == "benign":
            log_odds_threat = -3.0 * narrowing_strength

        target_is_threat = ground_truth == "threat"
        for step in range(1, evidence_steps + 1):
            if target_is_threat:
                log_odds_threat += evidence_strength
                if log_odds_threat > 0:
                    return step
            else:
                log_odds_threat -= evidence_strength
                if log_odds_threat < 0:
                    return step
        return evidence_steps + 1


def default_hccdi_spec() -> FrameTaskSpec:
    return FrameTaskSpec(
        run_id="hccdi_threat_frame_false_alarm",
        prior="threat",
        ambiguous_stimulus="ambiguous_signal",
        ground_truth="benign",
        narrowing_strength=0.8,
        evidence_steps=5,
    )


if __name__ == "__main__":
    import json

    print(json.dumps(FrameConstrueSim().run(default_hccdi_spec()).to_dict(), indent=2))
