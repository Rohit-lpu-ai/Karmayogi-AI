"""Local AI-boundary implementations: interface conformance, determinism, and honesty about method."""

from __future__ import annotations

from app.modules.ai import interfaces as i
from app.modules.ai import local

LESSONS = [
    {"id": "l1", "course_id": "c1", "title": "Percentage change versus percentage points",
     "body_markdown": "## Example\n\nA rate rises from 40% to 50%.\n\nThe change is 10 percentage points and a 25% percentage change."},
    {"id": "l2", "course_id": "c1", "title": "Reading a table", "body_markdown": "Check the unit and footnotes first."},
]


def test_local_implementations_satisfy_the_interfaces():
    assert isinstance(local.TemplateCompetencyInterpreter(), i.CompetencyInterpreter)
    assert isinstance(local.TemplateRecommendationExplainer(), i.RecommendationExplainer)
    assert isinstance(local.KeywordContentRetriever(), i.LearningContentRetriever)
    assert isinstance(local.NoQuestionGenerator(), i.QuestionGenerator)
    assert isinstance(local.StructuralQuestionValidator(), i.QuestionValidator)
    assert isinstance(local.RetrievalOnlyTutor(), i.LearningTutor)


def test_explainer_reflects_the_rule_and_says_it_is_a_template():
    out = local.TemplateRecommendationExplainer().explain("Reading tables", 1, 3, "Reading tables critically", "primary")
    assert "estimated level in Reading tables is 1" in out.text and "2 levels to go" in out.text
    assert out.method == "template-v1" and out.sources == ("rule:rec-v1",)


def test_retriever_is_deterministic_and_ranks_title_matches_first():
    retriever = local.KeywordContentRetriever()
    first = retriever.search("difference between percentage points and percentage change", LESSONS)
    assert [p.lesson_id for p in first] == ["l1"]
    assert "percentage points" in first[0].excerpt and "#" not in first[0].excerpt
    assert first == retriever.search("difference between percentage points and percentage change", LESSONS)
    assert retriever.search("the and of", LESSONS) == []


def test_validator_blocks_structural_errors_and_warns_on_style():
    v = local.StructuralQuestionValidator()
    codes = {f.code: f.severity for f in v.validate("Which is not a rate?", ["A", "A", "None of the above"], None, "Short")}
    assert codes["ONE_CORRECT"] == "error" and codes["DUPLICATE_OPTIONS"] == "error"
    assert codes["NEGATIVE_STEM"] == "warning" and codes["ALL_NONE_OF_THE_ABOVE"] == "warning"
    clean = v.validate("A table reports enrolment in thousands. What does 12.5 represent?",
                       ["12.5 people", "12,500 people", "125 people"], 1, "The unit is thousands, so 12.5 is 12,500 people.")
    assert clean == []


def test_generator_is_not_available_and_tutor_only_points_to_lessons():
    assert local.NoQuestionGenerator().propose("X", "X", "foundational", 3) == []
    reply = local.RetrievalOnlyTutor().answer("percentage points", LESSONS)
    assert not reply.refused and reply.passages[0].lesson_id == "l1" and reply.method == "retrieval-only-v1"
    refused = local.RetrievalOnlyTutor().answer("quantum chromodynamics", LESSONS)
    assert refused.refused and refused.passages == ()
