"""Disagreement-only HCCDE scoreboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable


def load_run_records(run_log_dir: Path | str = Path("scoreboard/runs")) -> list[Dict[str, Any]]:
    path = Path(run_log_dir)
    if not path.exists():
        return []

    records = []
    for record_path in sorted(path.glob("*.json")):
        records.append(json.loads(record_path.read_text(encoding="utf-8")))
    return records


def build_scoreboard(records: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    totals: Dict[str, Dict[str, int]] = {}
    runs = []

    for record in records:
        spec = record["run_spec"]
        run_summary = {
            "run_id": spec["run_id"],
            "test_id": spec["test_id"],
            "rivals": {},
        }

        for rival_id, score in record.get("disagreement_scores", {}).items():
            totals.setdefault(rival_id, {"hccde_win": 0, "hccde_loss": 0, "tie": 0})
            totals[rival_id][score["result"]] += 1
            run_summary["rivals"][rival_id] = score["result"]

        runs.append(run_summary)

    return {
        "score_rule": "Only score HCCDE vs a rival on prediction keys where both models disagreed before the run.",
        "totals_by_rival": totals,
        "runs": runs,
    }


def rebuild_scoreboard(
    run_log_dir: Path | str = Path("scoreboard/runs"),
    output_path: Path | str = Path("scoreboard/results.json"),
) -> Dict[str, Any]:
    records = load_run_records(run_log_dir)
    scoreboard = build_scoreboard(records)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(scoreboard, indent=2, sort_keys=True), encoding="utf-8")
    return scoreboard

