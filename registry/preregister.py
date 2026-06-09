"""Immutable prediction pre-registration records."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable

from models.base import Prediction
from sims.base import RunSpec


def canonical_json(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def payload_hash(payload: Dict[str, Any]) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def current_git_head() -> str:
    try:
        completed = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "unknown"
    return completed.stdout.strip()


def preregister_predictions(
    spec: RunSpec,
    predictions: Iterable[Prediction],
    registry_dir: Path | str = Path("registry/predictions"),
) -> Dict[str, Any]:
    """Write a timestamped prediction record before a run is executed."""

    registry_path = Path(registry_dir)
    registry_path.mkdir(parents=True, exist_ok=True)

    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    record = {
        "record_type": "prediction_preregistration",
        "created_at_utc": created_at,
        "git_head": current_git_head(),
        "run_spec": spec.to_dict(),
        "predictions": [prediction.to_dict() for prediction in predictions],
    }
    digest = payload_hash(record)
    record["record_hash"] = digest

    safe_timestamp = created_at.replace(":", "").replace("+", "Z")
    filename = f"{safe_timestamp}_{spec.run_id}_{digest[:12]}.json"
    path = registry_path / filename
    if path.exists():
        raise FileExistsError(f"Pre-registration already exists: {path}")

    path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    return {"path": str(path), "record_hash": digest, "created_at_utc": created_at}

