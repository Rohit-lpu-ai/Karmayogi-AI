"""AI capability boundary (Phase 4 plan section 8). Interfaces only - no provider, no network, no API keys.

Every capability the product may later hand to a language model is expressed here as a narrow ``Protocol`` with a
deterministic local implementation in ``app.modules.ai.local``. Screens and services depend on these interfaces, so a
provider-backed implementation can be added behind a feature flag after a recorded decision, without changing callers.

Rules every implementation must keep (SECURITY_RESPONSIBLE_AI.md, AI_SYSTEM_SPEC.md):
- Outputs are suggestions with provenance; they never change scores, estimates, approvals or publication by themselves.
- No learner personal data leaves the platform without a recorded decision and a data-processing agreement.
- Local implementations must say they are rule-based (``method``); nothing may be presented as AI when it is not.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class Explanation:
    text: str
    method: str  # e.g. "template-v1" (rule-based) or a provider/model identifier later
    sources: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrievedPassage:
    lesson_id: str
    course_id: str
    title: str
    excerpt: str
    score: float


@dataclass(frozen=True)
class ValidationFinding:
    code: str
    severity: str  # "error" blocks review submission; "warning" is shown to the reviewer
    message: str


@dataclass(frozen=True)
class QuestionDraft:
    competency_code: str
    difficulty: str
    stem: str
    options: tuple[str, ...]
    correct_index: int
    explanation: str
    method: str
    source_note: str = "Draft for a human author. Must be reviewed before use."


@dataclass(frozen=True)
class TutorReply:
    text: str
    method: str
    passages: tuple[RetrievedPassage, ...] = field(default_factory=tuple)
    refused: bool = False


@runtime_checkable
class CompetencyInterpreter(Protocol):
    """Turns a competency and required level into a plain-language description of what the level looks like at work."""

    def describe_requirement(self, competency_name: str, level_label: str, level_description: str | None) -> Explanation: ...


@runtime_checkable
class RecommendationExplainer(Protocol):
    """Explains, in plain words, why a course is suggested for a learner's gap. Must reflect the deterministic rule."""

    def explain(self, competency_name: str, estimated_level: int, required_level: int, course_title: str, relevance: str) -> Explanation: ...


@runtime_checkable
class LearningContentRetriever(Protocol):
    """Finds passages in published lessons relevant to a query. Returns only content learners are allowed to see."""

    def search(self, query: str, lessons: list[dict], limit: int = 5) -> list[RetrievedPassage]: ...


@runtime_checkable
class QuestionGenerator(Protocol):
    """Proposes draft questions for a human author. Drafts are never saved as approved or shown to learners."""

    def propose(self, competency_code: str, competency_name: str, difficulty: str, count: int) -> list[QuestionDraft]: ...


@runtime_checkable
class QuestionValidator(Protocol):
    """Checks a question's structure and wording before review. Findings inform people; they do not approve."""

    def validate(self, stem: str, options: list[str], correct_index: int | None, explanation: str) -> list[ValidationFinding]: ...


@runtime_checkable
class LearningTutor(Protocol):
    """Answers a learner's question about lesson content, grounded in retrieved passages, or declines."""

    def answer(self, question: str, lessons: list[dict]) -> TutorReply: ...
