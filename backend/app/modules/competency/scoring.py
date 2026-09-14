"""Deterministic competency estimation, method ``score-v1`` (AI_SYSTEM_SPEC.md §25).

Pure functions only: no database, no clock, no randomness, no AI. The same
evidence and levels always produce the same estimate. Parameters are
provisional until approved (DEC-020) and changing any of them requires a new
``METHOD_VERSION``.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from decimal import ROUND_HALF_EVEN, Decimal

METHOD_VERSION = "score-v1"

DIFFICULTY_WEIGHTS: dict[str, Decimal] = {
    "foundational": Decimal("1.0"),
    "intermediate": Decimal("1.5"),
    "advanced": Decimal("2.0"),
}

# Evidence bands by item count (provisional, DEC-020): insufficient < 3 <= low < 5 <= medium < 10 <= high.
BAND_THRESHOLDS: tuple[tuple[int, str], ...] = ((10, "high"), (5, "medium"), (3, "low"), (0, "insufficient"))
BAND_ORDER = {"insufficient": 0, "low": 1, "medium": 2, "high": 3}
GAP_MINIMUM_BAND = "medium"

SCORE_QUANTUM = Decimal("0.00001")  # numeric(6,5)

LIMITATIONS_BASE = (
    "Measures knowledge assessed by multiple-choice questions only.",
    "This is development guidance, not an appraisal, promotion or eligibility decision.",
)


@dataclass(frozen=True)
class EvidenceItem:
    question_version_id: str
    difficulty: str
    is_correct: bool


@dataclass(frozen=True)
class LevelThreshold:
    level_number: int
    label: str
    min_score: Decimal | None
    threshold_status: str


@dataclass(frozen=True)
class Estimate:
    score: Decimal | None
    level_number: int | None
    evidence_band: str
    evidence_count: int
    thresholds_status: str
    items: tuple[dict, ...] = field(default=())
    method_version: str = METHOD_VERSION


def weight_for(difficulty: str) -> Decimal:
    try:
        return DIFFICULTY_WEIGHTS[difficulty]
    except KeyError:
        raise ValueError(f"unknown difficulty {difficulty!r}") from None


def evidence_band(count: int) -> str:
    if count < 0:
        raise ValueError("evidence count cannot be negative")
    for minimum, band in BAND_THRESHOLDS:
        if count >= minimum:
            return band
    return "insufficient"  # pragma: no cover - (0, "insufficient") always matches


def thresholds_status(levels: Sequence[LevelThreshold]) -> str:
    configured = [lvl for lvl in levels if lvl.min_score is not None]
    if not configured:
        return "not_configured"
    return "approved" if all(lvl.threshold_status == "approved" for lvl in configured) else "provisional"


def level_for(score: Decimal, levels: Sequence[LevelThreshold]) -> int | None:
    """Highest level whose min_score <= score; None when thresholds are not configured or none is reached."""
    reached = [lvl.level_number for lvl in levels if lvl.min_score is not None and lvl.min_score <= score]
    return max(reached) if reached else None


def compute_estimate(items: Iterable[EvidenceItem], levels: Sequence[LevelThreshold]) -> Estimate:
    ordered = sorted(items, key=lambda item: item.question_version_id)
    count = len(ordered)
    status = thresholds_status(levels)
    if count == 0:
        return Estimate(score=None, level_number=None, evidence_band="insufficient", evidence_count=0,
                        thresholds_status=status)
    total_weight = sum((weight_for(item.difficulty) for item in ordered), Decimal("0"))
    earned = sum((weight_for(item.difficulty) for item in ordered if item.is_correct), Decimal("0"))
    score = (earned / total_weight).quantize(SCORE_QUANTUM, rounding=ROUND_HALF_EVEN)
    detail = tuple(
        {"question_version_id": item.question_version_id, "difficulty": item.difficulty,
         "weight": str(weight_for(item.difficulty)), "correct": item.is_correct}
        for item in ordered
    )
    return Estimate(score=score, level_number=level_for(score, levels), evidence_band=evidence_band(count),
                    evidence_count=count, thresholds_status=status, items=detail)


def explanation(estimate: Estimate, attempt_id: str | None) -> dict:
    limitations = []
    if estimate.evidence_count:
        limitations.append(f"Based on one assessment attempt with {estimate.evidence_count} question(s) for this competency.")
    if estimate.thresholds_status != "approved":
        limitations.append("Level thresholds are provisional and have not been statistically validated.")
    if BAND_ORDER[estimate.evidence_band] < BAND_ORDER[GAP_MINIMUM_BAND]:
        limitations.append("Evidence is not sufficient to confirm a gap; reassess to confirm.")
    limitations.extend(LIMITATIONS_BASE)
    return {
        "method_version": estimate.method_version,
        "attempt_id": attempt_id,
        "formula": "score = sum(weight x correct) / sum(weight); weights foundational 1.0, intermediate 1.5, advanced 2.0",
        "items": list(estimate.items),
        "score": str(estimate.score) if estimate.score is not None else None,
        "level_number": estimate.level_number,
        "thresholds_status": estimate.thresholds_status,
        "evidence_band": estimate.evidence_band,
        "evidence_count": estimate.evidence_count,
        "band_rule": "insufficient < 3 items <= low < 5 <= medium < 10 <= high",
        "adjustment": None,
        "limitations": limitations,
        "correction_route": "Request a review of this result (available in a later release)",
    }


@dataclass(frozen=True)
class GapResult:
    status: str  # gap | meets_requirement | insufficient_evidence | not_assessed | level_unavailable
    gap: int | None


def classify_gap(required_level: int, level_number: int | None, band: str | None) -> GapResult:
    """Gap rule: required - estimated level, only with evidence band >= medium and both levels known."""
    if band is None:
        return GapResult("not_assessed", None)
    if BAND_ORDER[band] < BAND_ORDER[GAP_MINIMUM_BAND]:
        return GapResult("insufficient_evidence", None)
    if level_number is None:
        return GapResult("level_unavailable", None)
    difference = required_level - level_number
    return GapResult("gap", difference) if difference > 0 else GapResult("meets_requirement", 0)
