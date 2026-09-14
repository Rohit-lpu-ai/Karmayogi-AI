"""Deterministic course recommendation, rule version ``rec-v1`` (AI_SYSTEM_SPEC.md §26).

Pure functions: identical inputs give identical, identically ordered output.
Only reviewed courses with approved competency mappings are candidates.
Exclusions for completed or dismissed items arrive with progress tracking.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Decimal

RULE_VERSION = "rec-v1"
RELEVANCE_WEIGHTS = {"primary": Decimal("1.0"), "secondary": Decimal("0.5")}
SOURCE_PREFERENCE = {"internal": 0, "nssta_programme_listing": 1}
MAX_PER_GAP = 3
SCORE_QUANTUM = Decimal("0.00001")


@dataclass(frozen=True)
class GapInput:
    competency_id: str
    competency_code: str
    competency_name: str
    required_level: int
    estimated_level: int
    gap: int
    max_level_span: int


@dataclass(frozen=True)
class CourseMapping:
    course_id: str
    title: str
    course_type: str
    duration_days: int | None
    competency_id: str
    relevance: str


@dataclass(frozen=True)
class RankedCourse:
    course_id: str
    title: str
    course_type: str
    duration_days: int | None
    score: Decimal
    reasons: tuple[dict, ...]


def _sort_key(course: RankedCourse) -> tuple:
    return (
        -course.score,
        SOURCE_PREFERENCE.get(course.course_type, 99),
        course.duration_days if course.duration_days is not None else 10**6,
        course.title,
        course.course_id,
    )


def rank_courses(gaps: Sequence[GapInput], mappings: Sequence[CourseMapping]) -> list[RankedCourse]:
    gaps_by_competency = {gap.competency_id: gap for gap in gaps if gap.gap > 0}
    per_course: dict[str, RankedCourse] = {}

    for gap in sorted(gaps_by_competency.values(), key=lambda g: (-g.gap, g.competency_code)):
        if gap.max_level_span <= 0:
            raise ValueError("max_level_span must be positive")
        candidates = []
        for mapping in mappings:
            if mapping.competency_id != gap.competency_id:
                continue
            weight = RELEVANCE_WEIGHTS[mapping.relevance]
            score = (Decimal(gap.gap) / Decimal(gap.max_level_span) * weight).quantize(SCORE_QUANTUM, ROUND_HALF_EVEN)
            reasons = (
                {"rule": "gap_match", "competency_id": gap.competency_id, "competency_code": gap.competency_code,
                 "competency_name": gap.competency_name, "required": gap.required_level,
                 "estimated": gap.estimated_level, "gap": gap.gap},
                {"rule": "mapping", "relevance": mapping.relevance, "mapping_status": "approved"},
            )
            candidates.append(RankedCourse(mapping.course_id, mapping.title, mapping.course_type,
                                           mapping.duration_days, score, reasons))
        for candidate in sorted(candidates, key=_sort_key)[:MAX_PER_GAP]:
            existing = per_course.get(candidate.course_id)
            if existing is None:
                per_course[candidate.course_id] = candidate
            else:
                # A course addressing several gaps keeps its best score and lists every reason.
                per_course[candidate.course_id] = RankedCourse(
                    existing.course_id, existing.title, existing.course_type, existing.duration_days,
                    max(existing.score, candidate.score), existing.reasons + candidate.reasons,
                )

    return sorted(per_course.values(), key=_sort_key)
