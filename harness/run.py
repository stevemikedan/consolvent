"""Run pre-registered model predictions against toy-system outcomes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from models.attractor_model import AttractorPredictor
from models.base import Prediction, Predictor
from models.hccde import HCCDEPredictor
from models.memory_model import StoredMemoryPredictor
from registry.preregister import preregister_predictions
from scoreboard.scoreboard import rebuild_scoreboard
from sims.base import RunSpec, SimOutcome
from sims.history_gated_graph import HistoryGatedGraphSim


def default_specs() -> List[RunSpec]:
    return [
        RunSpec(
            test_id="memory_discriminator",
            run_id="memory_north_channel",
            sim_id=HistoryGatedGraphSim.sim_id,
            history="north_channel",
            current_state="pivot",
            dynamics="uniform_proposal",
            notes="HCCDE vs stored-memory model.",
        ),
        RunSpec(
            test_id="attractor_discriminator",
            run_id="attractor_north_vs_south",
            sim_id=HistoryGatedGraphSim.sim_id,
            history="north_channel",
            comparison_history="south_channel",
            current_state="pivot",
            dynamics="uniform_proposal",
            notes="Same state and dynamics, different histories.",
        ),
        RunSpec(
            test_id="hysteresis_without_storage",
            run_id="hysteresis_north_channel_removed",
            sim_id=HistoryGatedGraphSim.sim_id,
            history="north_channel",
            current_state="pivot",
            dynamics="uniform_proposal",
            remove_training_conditions=True,
            notes="Constraint should persist after training condition removal.",
        ),
    ]


def default_predictors_for(test_id: str) -> List[Predictor]:
    if test_id == "memory_discriminator":
        return [HCCDEPredictor(), StoredMemoryPredictor()]
    if test_id == "attractor_discriminator":
        return [HCCDEPredictor(), AttractorPredictor()]
    if test_id == "hysteresis_without_storage":
        return [HCCDEPredictor(), StoredMemoryPredictor(), AttractorPredictor()]
    return [HCCDEPredictor(), StoredMemoryPredictor(), AttractorPredictor()]


def run_spec(
    spec: RunSpec,
    predictors: Iterable[Predictor] | None = None,
    registry_dir: Path | str = Path("registry/predictions"),
    run_log_dir: Path | str = Path("scoreboard/runs"),
) -> Dict[str, Any]:
    selected_predictors = list(predictors) if predictors else default_predictors_for(spec.test_id)
    predictions = [predictor.predict(spec) for predictor in selected_predictors]

    preregistration = preregister_predictions(spec, predictions, registry_dir)
    outcome = HistoryGatedGraphSim().run(spec)
    run_record = build_run_record(spec, predictions, preregistration, outcome)

    run_log_path = Path(run_log_dir)
    run_log_path.mkdir(parents=True, exist_ok=True)
    record_path = run_log_path / f"{spec.run_id}.json"
    record_path.write_text(json.dumps(run_record, indent=2, sort_keys=True), encoding="utf-8")
    run_record["run_record_path"] = str(record_path)

    rebuild_scoreboard(run_log_dir=run_log_path)
    return run_record


def build_run_record(
    spec: RunSpec,
    predictions: List[Prediction],
    preregistration: Dict[str, Any],
    outcome: SimOutcome,
) -> Dict[str, Any]:
    prediction_results = {
        prediction.model_id: score_prediction(prediction, outcome) for prediction in predictions
    }
    disagreement_scores = score_hccde_disagreements(predictions, outcome)

    return {
        "record_type": "falsification_run",
        "run_spec": spec.to_dict(),
        "preregistration": preregistration,
        "outcome": outcome.to_dict(),
        "prediction_results": prediction_results,
        "disagreement_scores": disagreement_scores,
    }


def score_prediction(prediction: Prediction, outcome: SimOutcome) -> Dict[str, Any]:
    key_results = {}
    hits = 0
    misses = 0
    unknown = 0

    for key, expected in prediction.claims.items():
        if key not in outcome.observed:
            key_results[key] = {"status": "unknown", "expected": expected, "actual": None}
            unknown += 1
            continue
        actual = outcome.observed[key]
        status = "hit" if actual == expected else "miss"
        if status == "hit":
            hits += 1
        else:
            misses += 1
        key_results[key] = {"status": status, "expected": expected, "actual": actual}

    return {"hits": hits, "misses": misses, "unknown": unknown, "keys": key_results}


def score_hccde_disagreements(predictions: List[Prediction], outcome: SimOutcome) -> Dict[str, Any]:
    by_model = {prediction.model_id: prediction for prediction in predictions}
    if "hccde" not in by_model:
        return {}

    hccde = by_model["hccde"]
    scores = {}
    for model_id, rival in by_model.items():
        if model_id == "hccde":
            continue

        disagreement_keys = sorted(
            key
            for key in set(hccde.claims).intersection(rival.claims)
            if hccde.claims[key] != rival.claims[key]
        )
        if not disagreement_keys:
            continue

        hccde_hits = sum(outcome.observed.get(key) == hccde.claims[key] for key in disagreement_keys)
        rival_hits = sum(outcome.observed.get(key) == rival.claims[key] for key in disagreement_keys)
        if hccde_hits > rival_hits:
            result = "hccde_win"
        elif hccde_hits < rival_hits:
            result = "hccde_loss"
        else:
            result = "tie"

        scores[model_id] = {
            "result": result,
            "disagreement_keys": disagreement_keys,
            "hccde_hits": hccde_hits,
            "rival_hits": rival_hits,
        }

    return scores


def run_default_suite() -> List[Dict[str, Any]]:
    return [run_spec(spec) for spec in default_specs()]

