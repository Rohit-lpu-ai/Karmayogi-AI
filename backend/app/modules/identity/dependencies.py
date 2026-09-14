"""FastAPI dependencies enforcing authentication, CSRF and access roles on the server (NR-08)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Depends, Request
from sqlalchemy.orm import Session as DbSession

from app.core.config import Settings
from app.core.db import get_db
from app.core.errors import ProblemError
from app.modules.identity import service
from app.modules.identity.models import Session, User
from app.modules.identity.security import csrf_matches, csrf_token_for

CSRF_HEADER = "X-CSRF-Token"

# Permission matrix (SECURITY_RESPONSIBLE_AI.md §4): auditors and platform admins do not take assessments
# or hold personal competency data.
SELF_LEARNING_ROLES = frozenset({
    "learner", "trainer", "department_admin", "org_admin", "competency_admin", "training_manager",
})


@dataclass(frozen=True)
class CurrentUser:
    user: User
    session: Session
    roles: frozenset[str]
    csrf_token: str


def get_settings_dep(request: Request) -> Settings:
    return request.app.state.settings


def get_current_user(
    request: Request, db: DbSession = Depends(get_db), settings: Settings = Depends(get_settings_dep)
) -> CurrentUser:
    token = request.cookies.get(settings.session_cookie_name)
    resolved = service.resolve_session(db, settings, token) if token else None
    if resolved is None:
        raise ProblemError(401, "UNAUTHENTICATED", "Authentication required", "Sign in to continue.")
    session, user = resolved
    return CurrentUser(
        user=user,
        session=session,
        roles=frozenset(service.access_roles(db, user)),
        csrf_token=csrf_token_for(settings.session_secret.get_secret_value(), token),
    )


def require_csrf(
    request: Request, current: CurrentUser = Depends(get_current_user), settings: Settings = Depends(get_settings_dep)
) -> CurrentUser:
    token = request.cookies.get(settings.session_cookie_name, "")
    if not csrf_matches(settings.session_secret.get_secret_value(), token, request.headers.get(CSRF_HEADER)):
        raise ProblemError(403, "CSRF_FAILED", "Request blocked", "Missing or invalid CSRF token. Reload and try again.")
    return current


def require_any_role(roles: frozenset[str], *, csrf: bool = False) -> Callable[..., CurrentUser]:
    base = require_csrf if csrf else get_current_user

    def dependency(current: CurrentUser = Depends(base)) -> CurrentUser:
        if not current.roles & roles:
            raise ProblemError(403, "FORBIDDEN", "Forbidden", "Your access role does not permit this action.")
        return current

    return dependency
