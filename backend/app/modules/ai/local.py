"""Deterministic local implementations of the AI capability interfaces. Rule-based; no model, no network, no keys.

Each implementation reports ``method`` so that nothing produced here can be mistaken for AI output.
"""

from __future__ import annotations

import re
from collections import Counter

from app.modules.ai.interfaces import (
    Explanation,
    QuestionDraft,
    RetrievedPassage,
    TutorReply,
    ValidationFinding,
)

_WORD = re.compile(r"[a-z0-9]+")
_STOP = frozenset("a an and are as at be by for from how in is it of on or that the this to was what when where which why with you your".split())


def _tokens(text: str) -> list[str]:
    return [w for w in _WORD.findall(text.lower()) if w not in _STOP and len(w) > 1]


class TemplateCompetencyInterpreter:
    method = "template-v1"

    def describe_requirement(self, competency_name: str, level_label: str, level_description: str | None) -> Explanation:
        detail = f" {level_description.strip()}" if level_description else ""
        return Explanation(f"Your role asks for {competency_name} at {level_label}.{detail}", self.method)


class TemplateRecommendationExplainer:
    method = "template-v1"

    def explain(self, competency_name: str, estimated_level: int, required_level: int, course_title: str, relevance: str) -> Explanation:
        gap = required_level - estimated_level
        focus = "focuses on" if relevance == "primary" else "also covers"
        text = (f"Your estimated level in {competency_name} is {estimated_level} and your role needs {required_level} "
                f"({gap} level{'s' if gap != 1 else ''} to go). {course_title} {focus} this competency.")
        return Explanation(text, self.method, ("rule:rec-v1",))


class KeywordContentRetriever:
    """Term-overlap scoring over lesson titles and bodies (title matches count double). Deterministic ordering."""

    method = "keyword-v1"

    def search(self, query: str, lessons: list[dict], limit: int = 5) -> list[RetrievedPassage]:
        terms = set(_tokens(query))
        if not terms:
            return []
        results = []
        for lesson in lessons:
            body = lesson.get("body_markdown") or ""
            title_hits = sum(1 for t in _tokens(lesson["title"]) if t in terms)
            body_counts = Counter(t for t in _tokens(body) if t in terms)
            score = 2.0 * title_hits + sum(min(c, 3) for c in body_counts.values())
            if score <= 0:
                continue
            paragraph = next((p for p in re.split(r"\n\s*\n", body) if any(t in _tokens(p) for t in terms)), body)
            excerpt = re.sub(r"[#*`>|]", "", paragraph).strip()
            results.append(RetrievedPassage(str(lesson["id"]), str(lesson["course_id"]), lesson["title"],
                                            excerpt[:280] + ("..." if len(excerpt) > 280 else ""), score))
        results.sort(key=lambda r: (-r.score, r.title, r.lesson_id))
        return results[:limit]


class StructuralQuestionValidator:
    method = "structure-v1"

    def validate(self, stem: str, options: list[str], correct_index: int | None, explanation: str) -> list[ValidationFinding]:
        findings: list[ValidationFinding] = []
        cleaned = [" ".join(o.lower().split()) for o in options]
        if not 3 <= len(options) <= 5:
            findings.append(ValidationFinding("OPTION_COUNT", "error", "Give 3 to 5 answer options."))
        if correct_index is None or not 0 <= correct_index < len(options):
            findings.append(ValidationFinding("ONE_CORRECT", "error", "Mark exactly one option as correct."))
        if len(set(cleaned)) != len(cleaned):
            findings.append(ValidationFinding("DUPLICATE_OPTIONS", "error", "Options must be different."))
        if any(o in ("all of the above", "none of the above") for o in cleaned):
            findings.append(ValidationFinding("ALL_NONE_OF_THE_ABOVE", "warning",
                                              "Avoid 'all/none of the above'; they reward test-taking tricks."))
        if len(stem.strip()) < 20:
            findings.append(ValidationFinding("STEM_TOO_SHORT", "warning", "The question may be too short to give context."))
        if re.search(r"\bnot\b|\bexcept\b", stem, re.IGNORECASE) and not re.search(r"\bNOT\b|\bEXCEPT\b", stem):
            findings.append(ValidationFinding("NEGATIVE_STEM", "warning", "Negative wording is easy to miss; write NOT or EXCEPT in capitals."))
        if correct_index is not None and 0 <= correct_index < len(options) and len(options) >= 3:
            lengths = [len(o) for o in options]
            if lengths[correct_index] > 1.8 * (sum(lengths) - lengths[correct_index]) / (len(lengths) - 1):
                findings.append(ValidationFinding("CORRECT_OPTION_LONGEST", "warning",
                                                  "The correct option is much longer than the others, which can give it away."))
        if len(explanation.strip()) < 20:
            findings.append(ValidationFinding("EXPLANATION_SHORT", "warning", "Explain why the answer is right, not only which."))
        return findings


class NoQuestionGenerator:
    """Local stand-in: question generation needs a language model and is not available without a recorded decision."""

    method = "not-available"

    def propose(self, competency_code: str, competency_name: str, difficulty: str, count: int) -> list[QuestionDraft]:
        return []


class RetrievalOnlyTutor:
    """Answers only by pointing to matching lesson passages; never composes new explanations."""

    method = "retrieval-only-v1"

    def __init__(self, retriever: KeywordContentRetriever | None = None) -> None:
        self.retriever = retriever or KeywordContentRetriever()

    def answer(self, question: str, lessons: list[dict]) -> TutorReply:
        passages = tuple(self.retriever.search(question, lessons, limit=3))
        if not passages:
            return TutorReply("No lesson in your courses covers this yet. Try different words, or ask your trainer.", self.method, refused=True)
        titles = "; ".join(p.title for p in passages)
        return TutorReply(f"These lessons look relevant: {titles}.", self.method, passages)
