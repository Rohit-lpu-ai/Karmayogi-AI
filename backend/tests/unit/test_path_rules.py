"""path-v1: deterministic ordering, prerequisites, placeholders and completed carry-over."""

from __future__ import annotations

from app.modules.learning import path_rules as r


def gap(cid: str, size: int, code: str | None = None) -> r.PathGap:
    return r.PathGap(cid, code or cid.upper(), f"Competency {cid}", 3, 3 - size, size)


def course(cid: str, difficulty: str | None, rank: int, gaps: tuple[str, ...]) -> r.PathCourse:
    return r.PathCourse(cid, f"Course {cid}", difficulty, rank, {g: ({"rule": "gap_match", "competency_id": g},) for g in gaps})


def ids(items):
    return [(i.item_type, i.course_id, i.gap_competency_id) for i in items]


def test_largest_gap_first_and_foundational_before_advanced_within_a_gap():
    gaps = [gap("a", 1), gap("b", 2)]
    recommended = [course("adv", "advanced", 1, ("b",)), course("found", "foundational", 2, ("b",)),
                   course("mid", "intermediate", 3, ("a",))]
    visible = {c.course_id: c for c in recommended}
    assert ids(r.build_path(gaps, recommended, {}, visible)) == [
        ("course", "found", "b"), ("course", "adv", "b"), ("course", "mid", "a")]


def test_ties_use_recommendation_rank_and_unknown_difficulty_sits_with_intermediate():
    gaps = [gap("a", 2)]
    recommended = [course("x", None, 2, ("a",)), course("y", "intermediate", 1, ("a",)), course("z", "foundational", 3, ("a",))]
    visible = {c.course_id: c for c in recommended}
    assert [i.course_id for i in r.build_path(gaps, recommended, {}, visible)] == ["z", "y", "x"]


def test_prerequisites_come_first_even_when_not_recommended_and_only_once():
    gaps = [gap("a", 2), gap("b", 1)]
    base = r.PathCourse("base", "Base course", "foundational", 0)
    recommended = [course("adv", "advanced", 1, ("a",)), course("adv2", "advanced", 2, ("b",))]
    visible = {c.course_id: c for c in [*recommended, base]}
    items = r.build_path(gaps, recommended, {"adv": ["base"], "adv2": ["base"]}, visible)
    assert [i.course_id for i in items] == ["base", "adv", "adv2"]
    assert items[0].reasons[0] == {"rule": "prerequisite", "for_course_id": "adv", "for_course_title": "Course adv"}


def test_invisible_prerequisites_are_skipped():
    gaps = [gap("a", 2)]
    recommended = [course("adv", "advanced", 1, ("a",))]
    items = r.build_path(gaps, recommended, {"adv": ["hidden"]}, {"adv": recommended[0]})
    assert [i.course_id for i in items] == ["adv"]


def test_course_matching_two_gaps_appears_once_under_the_larger_gap():
    gaps = [gap("a", 1), gap("b", 2)]
    shared = course("shared", "foundational", 1, ("a", "b"))
    items = r.build_path(gaps, [shared], {}, {"shared": shared})
    assert ids(items) == [("course", "shared", "b")]


def test_gap_without_content_gets_a_placeholder_and_closed_gaps_are_ignored():
    gaps = [gap("a", 2), gap("closed", 0)]
    items = r.build_path(gaps, [], {}, {})
    assert ids(items) == [("no_content_placeholder", None, "a")]
    assert items[0].reasons[0]["rule"] == "no_approved_content"


def test_completed_earlier_courses_are_kept_at_the_end():
    gaps = [gap("a", 2)]
    now = course("now", "foundational", 1, ("a",))
    old = r.PathCourse("old", "Old", "foundational", 0)
    items = r.build_path(gaps, [now], {}, {"now": now, "old": old}, completed_earlier=["old", "now"])
    assert ids(items) == [("course", "now", "a"), ("course", "old", None)]


def test_output_and_hash_are_deterministic_and_sensitive_to_inputs():
    gaps = [gap("a", 2), gap("b", 2)]
    recommended = [course("c1", "foundational", 1, ("a",)), course("c2", "advanced", 2, ("b",))]
    visible = {c.course_id: c for c in recommended}
    assert r.build_path(gaps, recommended, {}, visible) == r.build_path(list(reversed(gaps)), list(reversed(recommended)), {}, visible)
    h1 = r.input_hash("role", gaps, recommended, {})
    assert h1 == r.input_hash("role", list(reversed(gaps)), recommended, {}) and len(h1) == 64
    assert h1 != r.input_hash("role", [gap("a", 1), gap("b", 2)], recommended, {})
    assert h1 != r.input_hash("role", gaps, recommended, {"c2": ["c1"]})
    assert h1 != r.input_hash("other-role", gaps, recommended, {})
