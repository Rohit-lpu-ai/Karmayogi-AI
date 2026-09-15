"""Loading and gating of the Phase 1 canonical datasets (DATA_MODEL.md §15).

The existing validator (``scripts/validators/validate_canonical_datasets.py``)
is reused, not reimplemented: an ``INVALID`` verdict refuses the import.
"""

from __future__ import annotations

import hashlib
import importlib.util
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from app.core.config import REPO_ROOT

PROCESSED_DIR = REPO_ROOT / "data" / "processed"
VALIDATOR_PATH = REPO_ROOT / "scripts" / "validators" / "validate_canonical_datasets.py"
SEED_DATASETS = ("topics", "documents", "competency_framework", "training_programmes")


class SeedRefused(Exception):
    """The canonical data failed a gate; nothing was imported."""


@dataclass(frozen=True)
class CanonicalBundle:
    datasets: dict[str, dict[str, Any]]
    file_sha256: dict[str, str]
    verdict: str


def _load_validator() -> ModuleType:
    spec = importlib.util.spec_from_file_location("validate_canonical_datasets", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise SeedRefused(f"Canonical dataset validator not found at {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_canonical_bundle(processed_dir: Path = PROCESSED_DIR) -> CanonicalBundle:
    validator = _load_validator()
    datasets = validator.load_datasets(processed_dir)
    report = validator.validate_datasets(datasets)
    hashes = {name: sha256_file(processed_dir / f"{name}.json") for name in SEED_DATASETS}
    return CanonicalBundle(datasets=datasets, file_sha256=hashes, verdict=report["verdict"])


def require_importable(bundle: CanonicalBundle) -> None:
    if bundle.verdict == "INVALID":
        raise SeedRefused("Canonical dataset validator verdict is INVALID; fix the datasets before importing")
    for name in SEED_DATASETS:
        if name not in bundle.datasets:
            raise SeedRefused(f"Canonical dataset {name!r} is missing")
