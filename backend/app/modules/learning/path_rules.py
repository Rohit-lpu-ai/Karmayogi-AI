"""Deterministic learning path, rule version ``path-v1`` (Phase 4 plan K-5).

Pure functions: identical inputs give identical, identically ordered output. The rule is separate from ``rec-v1``:
``rec-v1`` decides *which* courses address a gap and ranks them (difficulty never affects that ranking, DEC-051);
``path-v1`` only decides the *order* in which a learner meets them.

Rule:
1. Gaps in order of size (largest first), ties by competency code.
2. Within a gap: the courses ``rec-v1`` matched to that gap, ordered foundational -> intermediate -> advanced
   (unknown difficulty sits with intermediate), ties by ``rec-v1`` rank.
3. A course's advisory prerequisites that are visible in the catalogue come immediately before it, even when
   ``rec-v1`` did not match them to the gap.
4. Each course appears once, at its first position. A gap with no matched course gets a placeholder item.
5. Courses completed from an earlier path that are no longer matched are kept at the end ("completed earlier").
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

RULE_VERSION = "path-v1"
RULE_TEXT = ("Gaps largest first; within a gap, courses matched by rec-v1 from foundational to advanced (ties by "
             "rec-v1 rank); advisory prerequisites placed just before the course; each course once; gaps without "
             "matched courses shown as placeholders.")
DIFFICULTY_ORDER = {"foundational": 0, "intermediate": 1, "advanced": 2}


@dataclass(frozen=True)
class PathGap:
    competency_id: str
    competency_code: str
    competency_name: str
    required_level: int
    estimated_level: int
    gap: int


@dataclass(frozen=True)
class PathCourse:
    course_id: str
    title: str
    difficulty: str | None
    rank: int  # rec-v1 rank; 0 when the course was not recommended (a prerequisite only)
    gap_reasons: Mapping[str, tuple[dict, ...]] = field(default_factory=dict)  # competency id -> rec-v1 reasons


@dataclass(frozen=True)
class PathItem:
    item_type: str  # course | no_content_placeholder
    course_id: str | None
    gap_competency_id: str | None
    reasons: tuple[dict, ...]


def _difficulty_key(course: PathCourse) -> int:
    return DIFFICULTY_ORDER.get(course.difficulty or "", 1)


def build_path(gaps: Sequence[PathGap], recommended: Sequence[PathCourse], prerequisites: Mapping[str, Sequence[str]],
               visible: Mapping[str, PathCourse], completed_earlier: Sequence[str] = ()) -> list[PathItem]:
    items: list[PathItem] = []
    placed: set[str] = set()

    for gap in sorted((g for g in gaps if g.gap > 0), key=lambda g: (-g.gap, g.competency_code)):
        matched = [c for c in recommended if gap.competency_id in c.gap_reasons]
        if not matched:
            items.append(PathItem("no_content_placeholder", None, gap.competency_id, (
                {"rule": "no_approved_content", "competency_id": gap.competency_id,
                 "competency_code": gap.competency_code, "competency_name": gap.competency_name, "gap": gap.gap},)))
            continue
        for course in sorted(matched, key=lambda c: (_difficulty_key(c), c.rank, c.title, c.course_id)):
            if course.course_id in placed:
                continue
            for prereq_id in sorted(prerequisites.get(course.course_id, ()),
                                    key=lambda pid: (_difficulty_key(visible[pid]), visible[pid].title, pid)
                                    if pid in visible else (9, "", pid)):
                if prereq_id in placed or prereq_id not in visible:
                    continue
                items.append(PathItem("course", prereq_id, gap.competency_id, (
                    {"rule": "prerequisite", "for_course_id": course.course_id, "for_course_title": course.title},)))
                placed.add(prereq_id)
            reasons = tuple(course.gap_reasons[gap.competency_id]) + (
                {"rule": "order", "difficulty": course.difficulty, "recommendation_rank": course.rank},)
            items.append(PathItem("course", course.course_id, gap.competency_id, reasons))
            placed.add(course.course_id)

    for course_id in sorted(completed_earlier):
        if course_id not in placed and course_id in visible:
            items.append(PathItem("course", course_id, None, ({"rule": "completed_earlier"},)))
            placed.add(course_id)
    return items


def input_hash(job_role_id: str | None, gaps: Sequence[PathGap], recommended: Sequence[PathCourse],
               prerequisites: Mapping[str, Sequence[str]]) -> str:
    """Fingerprint of everything the path depends on, so a stale path can be detected and regenerated."""
    payload = {
        "rule": RULE_VERSION,
        "job_role": job_role_id,
        "gaps": sorted((g.competency_id, g.gap) for g in gaps if g.gap > 0),
        "courses": sorted((c.course_id, c.rank, c.difficulty or "", sorted(c.gap_reasons)) for c in recommended),
        "prerequisites": sorted((k, sorted(v)) for k, v in prerequisites.items()),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()
