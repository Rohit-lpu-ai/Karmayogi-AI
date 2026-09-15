"""rec-v1 ranking is deterministic, explainable and uses only the supplied (approved) mappings."""

from decimal import Decimal

import pytest

from app.modules.recommendation.rules import CourseMapping, GapInput, rank_courses

C1 = GapInput("c1", "DEMO-C1", "Descriptive", required_level=3, estimated_level=2, gap=1, max_level_span=3)
C2 = GapInput("c2", "DEMO-C2", "Percentages", required_level=3, estimated_level=1, gap=2, max_level_span=3)


def mapping(course, competency, relevance="primary", course_type="internal", days=None, title=None):
    return CourseMapping(course, title or f"Course {course}", course_type, days, competency, relevance)


def test_score_is_gap_share_times_relevance():
    ranked = rank_courses([C2], [mapping("a", "c2", "primary"), mapping("b", "c2", "secondary")])
    assert [(r.course_id, r.score) for r in ranked] == [("a", Decimal("0.66667")), ("b", Decimal("0.33333"))]


def test_every_recommendation_has_gap_and_mapping_reasons():
    ranked = rank_courses([C2], [mapping("a", "c2")])
    rules = [reason["rule"] for reason in ranked[0].reasons]
    assert rules == ["gap_match", "mapping"]
    assert ranked[0].reasons[0]["gap"] == 2


def test_only_gaps_produce_recommendations():
    no_gap = GapInput("c1", "DEMO-C1", "Descriptive", 3, 3, 0, 3)
    assert rank_courses([no_gap], [mapping("a", "c1")]) == []


def test_courses_for_other_competencies_ignored():
    assert rank_courses([C2], [mapping("a", "c1")]) == []


def test_tie_breaks_internal_then_shorter_then_title():
    ranked = rank_courses([C2], [
        mapping("listing", "c2", course_type="nssta_programme_listing", days=1, title="A"),
        mapping("long", "c2", days=5, title="A"),
        mapping("short-b", "c2", days=2, title="B"),
        mapping("short-a", "c2", days=2, title="A"),
    ])
    assert [r.course_id for r in ranked][:3] == ["short-a", "short-b", "long"]


def test_course_matching_two_gaps_keeps_best_score_and_all_reasons():
    ranked = rank_courses([C1, C2], [mapping("x", "c1", "secondary"), mapping("x", "c2", "secondary")])
    assert len(ranked) == 1
    assert ranked[0].score == Decimal("0.33333")  # max(1/3*0.5, 2/3*0.5)
    assert {r["competency_code"] for r in ranked[0].reasons if r["rule"] == "gap_match"} == {"DEMO-C1", "DEMO-C2"}


def test_at_most_three_per_gap():
    ranked = rank_courses([C2], [mapping(str(i), "c2", days=i) for i in range(1, 6)])
    assert [r.course_id for r in ranked] == ["1", "2", "3"]


def test_deterministic_regardless_of_input_order():
    mappings = [mapping("a", "c1"), mapping("b", "c2", "secondary"), mapping("c", "c2")]
    assert rank_courses([C1, C2], mappings) == rank_courses([C2, C1], list(reversed(mappings)))


def test_invalid_level_span_rejected():
    with pytest.raises(ValueError):
        rank_courses([GapInput("c", "X", "X", 3, 1, 2, 0)], [mapping("a", "c")])
