"""MOCK implementation of IGotClient backed by synthetic fixtures.

*** ALL DATA RETURNED BY THIS CLIENT IS MOCK. ***
Nothing here comes from iGOT Karmayogi. Records are loaded from
data/samples/mock/MOCK_igot_fixtures.json, every record has
data_status == "MOCK", and the loader refuses any file not marked MOCK so
this client cannot be pointed at real learner data.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from clients.igot_client import (
    AuthorizationRequiredError,
    Completion,
    Course,
    CoursePage,
    Enrollment,
    IGotClient,
    LearningEvent,
    NotFoundError,
)

MOCK = "MOCK"
DEFAULT_FIXTURES = Path(__file__).resolve().parents[1] / "data" / "samples" / "mock" / "MOCK_igot_fixtures.json"


class MockIGotClient(IGotClient):
    """In-memory IGotClient over MOCK fixtures.

    acting_user_id simulates the authorization a real integration would
    enforce: when set, user-scoped calls for any other user raise
    AuthorizationRequiredError. When None, no check is applied.
    """

    def __init__(self, fixtures_path: Optional[Path] = None, acting_user_id: Optional[str] = None):
        data = json.loads(Path(fixtures_path or DEFAULT_FIXTURES).read_text(encoding="utf-8"))
        _require_mock(data)
        self.acting_user_id = acting_user_id
        self._courses = {c["course_id"]: c for c in data["courses"]}
        self._users = set(data["users"])
        self._enrollments = data["enrollments"]
        self._events = data["learning_events"]

    def list_courses(
        self,
        *,
        limit: int = 20,
        offset: int = 0,
        provider: Optional[str] = None,
        competency: Optional[str] = None,
    ) -> CoursePage:
        if limit < 1 or offset < 0:
            raise ValueError("limit must be >= 1 and offset must be >= 0")
        matches = [
            c for c in self._courses.values()
            if (provider is None or c["provider"] == provider)
            and (competency is None or competency in c["competencies"])
        ]
        page = matches[offset:offset + limit]
        return CoursePage(
            courses=tuple(_course(c) for c in page),
            total=len(matches),
            limit=limit,
            offset=offset,
            data_status=MOCK,
        )

    def get_course(self, course_id: str) -> Course:
        try:
            return _course(self._courses[course_id])
        except KeyError:
            raise NotFoundError(f"MOCK: no course {course_id!r}") from None

    def get_user_enrollments(self, user_id: str) -> list[Enrollment]:
        self._check_user(user_id)
        return [
            Enrollment(
                user_id=e["user_id"],
                course_id=e["course_id"],
                enrolled_on=e["enrolled_on"],
                status=e["status"],
                progress_percent=e["progress_percent"],
                data_status=MOCK,
            )
            for e in self._enrollments
            if e["user_id"] == user_id
        ]

    def get_user_completions(self, user_id: str) -> list[Completion]:
        self._check_user(user_id)
        return [
            Completion(
                user_id=e["user_id"],
                course_id=e["course_id"],
                completed_on=e["completed_on"],
                certificate_id=e["certificate_id"],
                data_status=MOCK,
            )
            for e in self._enrollments
            if e["user_id"] == user_id and e["status"] == "completed"
        ]

    def get_learning_history(self, user_id: str) -> list[LearningEvent]:
        self._check_user(user_id)
        events = sorted(
            (ev for ev in self._events if ev["user_id"] == user_id),
            key=lambda ev: ev["occurred_at"],
        )
        return [
            LearningEvent(
                user_id=ev["user_id"],
                course_id=ev["course_id"],
                event_type=ev["event_type"],
                occurred_at=ev["occurred_at"],
                progress_percent=ev["progress_percent"],
                data_status=MOCK,
            )
            for ev in events
        ]

    def _check_user(self, user_id: str) -> None:
        if self.acting_user_id is not None and user_id != self.acting_user_id:
            raise AuthorizationRequiredError(
                f"MOCK: {self.acting_user_id!r} is not authorized to read records of {user_id!r}"
            )
        if user_id not in self._users:
            raise NotFoundError(f"MOCK: no user {user_id!r}")


def _course(c: dict) -> Course:
    return Course(
        course_id=c["course_id"],
        title=c["title"],
        provider=c["provider"],
        description=c["description"],
        competencies=tuple(c["competencies"]),
        duration_minutes=c["duration_minutes"],
        languages=tuple(c["languages"]),
        data_status=MOCK,
    )


def _require_mock(data: dict) -> None:
    """Refuse to load anything that is not explicitly and fully marked MOCK."""
    if data.get("data_status") != MOCK:
        raise ValueError("Refusing to load fixtures: top-level data_status is not 'MOCK'")
    for section in ("courses", "enrollments", "learning_events"):
        for record in data[section]:
            if record.get("data_status") != MOCK:
                raise ValueError(f"Refusing to load fixtures: a record in {section!r} is not marked 'MOCK'")
    for user_id in data["users"]:
        if not user_id.startswith("MOCK-"):
            raise ValueError(f"Refusing to load fixtures: user id {user_id!r} is not a MOCK- identifier")
