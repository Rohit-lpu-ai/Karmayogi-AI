"""Interface for reading course and learner data from iGOT Karmayogi.

This module defines the contract only. There is deliberately no live
implementation: as of 2026-09-14 no public or partner API for iGOT Karmayogi
has been documented (see IGOT_ACCESS_STATUS.md), so any concrete endpoint
would be invented. Use ``clients.mock_igot_client.MockIGotClient`` until
the preconditions in API_REQUIREMENTS.md section 6.4 are met.

Rules for implementations:
- No endpoint, base URL or credential is hard-coded. Configuration comes from
  environment variables (IGOT_*) and credentials never enter source control.
- User-scoped methods return data for one user only and must only be called
  with that user's own authorization or a documented mandate.
- Every returned record sets ``data_status`` from STATUS_VOCABULARY.md.
"""

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


# --- Errors -----------------------------------------------------------------


class IGotError(Exception):
    """Base class for iGOT client errors."""


class NotFoundError(IGotError):
    """The requested course or user does not exist."""


class AuthorizationRequiredError(IGotError):
    """The caller is not authorized to read this user's records."""


class AccessNotVerifiedError(IGotError):
    """Live access was requested but has not been authorized or documented."""


# --- Records ----------------------------------------------------------------


@dataclass(frozen=True)
class Course:
    course_id: str
    title: str
    provider: str
    description: str
    competencies: tuple[str, ...]
    duration_minutes: Optional[int]
    languages: tuple[str, ...]
    data_status: str


@dataclass(frozen=True)
class CoursePage:
    courses: tuple[Course, ...]
    total: int
    limit: int
    offset: int
    data_status: str


@dataclass(frozen=True)
class Enrollment:
    user_id: str
    course_id: str
    enrolled_on: str  # ISO 8601 date
    status: str  # "not_started" | "in_progress" | "completed"
    progress_percent: int
    data_status: str


@dataclass(frozen=True)
class Completion:
    user_id: str
    course_id: str
    completed_on: str  # ISO 8601 date
    certificate_id: Optional[str]
    data_status: str


@dataclass(frozen=True)
class LearningEvent:
    user_id: str
    course_id: str
    event_type: str  # "enrolled" | "progress" | "completed"
    occurred_at: str  # ISO 8601 timestamp
    progress_percent: Optional[int]
    data_status: str
    details: dict = field(default_factory=dict, compare=False)


# --- Interface --------------------------------------------------------------


class IGotClient(ABC):
    """Read-only access to iGOT Karmayogi course and learner data."""

    @abstractmethod
    def list_courses(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        provider: Optional[str] = None,
        competency: Optional[str] = None,
    ) -> CoursePage:
        """Return a page of courses, optionally filtered by provider or competency."""

    @abstractmethod
    def get_course(self, course_id: str) -> Course:
        """Return one course. Raises NotFoundError if it does not exist."""

    @abstractmethod
    def get_user_enrollments(self, user_id: str) -> list[Enrollment]:
        """Return one user's enrolments. Personal data: requires authorization."""

    @abstractmethod
    def get_user_completions(self, user_id: str) -> list[Completion]:
        """Return one user's completed courses. Personal data: requires authorization."""

    @abstractmethod
    def get_learning_history(self, user_id: str) -> list[LearningEvent]:
        """Return one user's learning events, oldest first. Personal data: requires authorization."""


def create_igot_client() -> IGotClient:
    """Build the client selected by IGOT_CLIENT_MODE (default: "mock").

    "live" is refused until a documented, authorized integration exists.
    """
    mode = os.environ.get("IGOT_CLIENT_MODE", "mock").strip().lower()
    if mode == "mock":
        from clients.mock_igot_client import MockIGotClient

        return MockIGotClient()
    if mode == "live":
        raise AccessNotVerifiedError(
            "No live iGOT client exists: no public or partner API is documented and "
            "no access has been authorized. See API_REQUIREMENTS.md section 6.4."
        )
    raise ValueError(f"Unknown IGOT_CLIENT_MODE: {mode!r} (expected 'mock' or 'live')")
