#!/usr/bin/env python3
"""Smoke tests for the falsification harness."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

from hccdi.frame_task import FrameConstrueSim, FrameTaskSpec
from harness.run import run_spec, score_hccde_disagreements
from models.attractor_model import AttractorPredictor
from models.hccde import HCCDEPredictor
from models.memory_model import StoredMemoryPredictor
from sims.base import RunSpec
from sims.history_gated_graph import HistoryGatedGraphSim


def test_history_changes_reachable_set_without_changing_state_or_dynamics():
    sim = HistoryGatedGraphSim()
    spec = RunSpec(
        test_id="attractor_discriminator",
        run_id="test_attractor",
        sim_id=HistoryGatedGraphSim.sim_id,
        history="north_channel",
        comparison_history="south_channel",
        current_state="pivot",
        dynamics="uniform_proposal",
    )
    outcome = sim.run(spec)
    assert outcome.observed["reachable_set_differs_by_history"] is True
    assert outcome.observed["past_trajectory_reconstructable_from_current_state"] is False


def test_hccde_scores_only_on_disagreement_keys():
    spec = RunSpec(
        test_id="memory_discriminator",
        run_id="test_memory",
        sim_id=HistoryGatedGraphSim.sim_id,
        history="north_channel",
        current_state="pivot",
        dynamics="uniform_proposal",
    )
    outcome = HistoryGatedGraphSim().run(spec)
    predictions = [HCCDEPredictor().predict(spec), StoredMemoryPredictor().predict(spec)]
    scores = score_hccde_disagreements(predictions, outcome)
    assert scores["stored_memory"]["result"] == "hccde_win"
    assert "past_trajectory_reconstructable_from_current_state" in scores["stored_memory"]["disagreement_keys"]


def test_storage_positive_control_can_make_hccde_lose():
    spec = RunSpec(
        test_id="storage_positive_control",
        run_id="test_storage_positive_control",
        sim_id=HistoryGatedGraphSim.sim_id,
        history="north_channel",
        current_state="pivot|memory=north_channel",
        dynamics="attractor_only",
    )
    outcome = HistoryGatedGraphSim().run(spec)
    predictions = [HCCDEPredictor().predict(spec), StoredMemoryPredictor().predict(spec)]
    scores = score_hccde_disagreements(predictions, outcome)
    assert outcome.observed["past_trajectory_reconstructable_from_current_state"] is True
    assert scores["stored_memory"]["result"] == "hccde_loss"


def test_attractor_positive_control_can_make_hccde_lose():
    spec = RunSpec(
        test_id="attractor_positive_control",
        run_id="test_attractor_positive_control",
        sim_id=HistoryGatedGraphSim.sim_id,
        history="north_channel",
        comparison_history="south_channel",
        current_state="pivot",
        dynamics="attractor_only",
    )
    outcome = HistoryGatedGraphSim().run(spec)
    predictions = [HCCDEPredictor().predict(spec), AttractorPredictor().predict(spec)]
    scores = score_hccde_disagreements(predictions, outcome)
    assert outcome.observed["reachable_set_differs_by_history"] is False
    assert scores["plain_attractor"]["result"] == "hccde_loss"


def test_preregistration_is_written_before_run_record():
    spec = RunSpec(
        test_id="hysteresis_without_storage",
        run_id="test_hysteresis",
        sim_id=HistoryGatedGraphSim.sim_id,
        history="north_channel",
        current_state="pivot",
        dynamics="uniform_proposal",
        remove_training_conditions=True,
    )

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        record = run_spec(
            spec,
            predictors=[HCCDEPredictor(), StoredMemoryPredictor(), AttractorPredictor()],
            registry_dir=tmp_path / "registry",
            run_log_dir=tmp_path / "runs",
        )
        prereg_path = Path(record["preregistration"]["path"])
        run_path = Path(record["run_record_path"])
        assert prereg_path.exists()
        assert run_path.exists()
        prereg = json.loads(prereg_path.read_text(encoding="utf-8"))
        assert prereg["record_hash"] == record["preregistration"]["record_hash"]


def test_hccdi_can_collapse_to_evidence_like_ordinary_bias():
    spec = FrameTaskSpec(
        run_id="test_hccdi_fast_evidence",
        prior="threat",
        ambiguous_stimulus="ambiguous_signal",
        ground_truth="benign",
        narrowing_strength=0.8,
        evidence_steps=3,
        evidence_strength=10.0,
    )
    outcome = FrameConstrueSim().run(spec)
    assert outcome.observed["framed_collapse_rate_equals_unframed"] is True
    assert outcome.observed["correction_resistance_increases_with_narrowing"] is False


def run_all_tests():
    test_history_changes_reachable_set_without_changing_state_or_dynamics()
    test_hccde_scores_only_on_disagreement_keys()
    test_storage_positive_control_can_make_hccde_lose()
    test_attractor_positive_control_can_make_hccde_lose()
    test_preregistration_is_written_before_run_record()
    test_hccdi_can_collapse_to_evidence_like_ordinary_bias()
    print("falsification harness smoke tests passed")


if __name__ == "__main__":
    run_all_tests()
