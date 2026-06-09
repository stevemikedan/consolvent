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

        unframed_correction_steps = 1
        framed_correction_steps = max(
            1,
            int(round(unframed_correction_steps + spec.narrowing_strength * spec.evidence_steps)),
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

