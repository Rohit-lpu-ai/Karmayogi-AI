"""Auth and self-service routes (API_INTEGRATION_SPEC.md §2.2-2.3)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session as DbSession

from app.core.config import Settings
from app.core.db import get_db
from app.core.demo import is_demo_code
from app.modules.identity import service
from app.modules.identity.dependencies import (
    SELF_LEARNING_ROLES,
    CurrentUser,
    get_current_user,
    get_settings_dep,
    require_csrf,
)
from app.modules.identity.models import User
from app.modules.identity.schemas import (
    JobRoleRef,
    JobRoleSelectionRequest,
    LoginRequest,
    MeResponse,
    NoticeAcknowledgementRequest,
    NoticeState,
    SessionResponse,
)
from app.modules.identity.security import csrf_token_for
from app.modules.organization.models import JobRole

router = APIRouter(prefix="/api/v1", tags=["identity"])

_ERRORS = {401: {"description": "Not signed in"}, 403: {"description": "CSRF or permission failure"}}


def build_me(db: DbSession, user: User) -> MeResponse:
    roles = service.access_roles(db, user)
    job_role = db.get(JobRole, user.job_role_id) if user.job_role_id else None
    return MeResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        designation=user.designation,
        organization_id=user.organization_id,
        access_roles=roles,
        can_take_assessments=bool(set(roles) & SELF_LEARNING_ROLES),
        job_role=JobRoleRef(id=job_role.id, name=job_role.name, code=job_role.code, is_demo=is_demo_code(job_role.code))
        if job_role else None,
        notice=NoticeState(
            notice_type=service.NOTICE_TYPE, version=service.NOTICE_VERSION, status="draft",
            text=service.NOTICE_TEXT, acknowledged_at=service.notice_acknowledged(db, user),
        ),
        is_synthetic=user.is_synthetic,
    )


@router.post(
    "/auth/login", operation_id="identity_post_login", response_model=SessionResponse,
    responses={401: {"description": "Invalid credentials"}, 423: {"description": "Account locked"}},
)
def login(
    body: LoginRequest, response: Response, db: DbSession = Depends(get_db), settings: Settings = Depends(get_settings_dep)
) -> SessionResponse:
    result = service.login(db, settings, body.email, body.password, body.organization_code)
    response.set_cookie(
        settings.session_cookie_name, result.token,
        max_age=settings.session_absolute_timeout_hours * 3600,
        httponly=True, secure=settings.session_cookie_secure, samesite="lax", path="/",
    )
    return SessionResponse(
        csrf_token=csrf_token_for(settings.session_secret.get_secret_value(), result.token),
        idle_expires_at=result.session.idle_expires_at,
        absolute_expires_at=result.session.absolute_expires_at,
        user=build_me(db, result.user),
    )


@router.post("/auth/logout", operation_id="identity_post_logout", status_code=204, responses=_ERRORS)
def logout(
    response: Response, current: CurrentUser = Depends(require_csrf), db: DbSession = Depends(get_db),
    settings: Settings = Depends(get_settings_dep),
) -> Response:
    service.logout(db, current.session, current.user)
    response.status_code = 204
    response.delete_cookie(settings.session_cookie_name, path="/")
    return response


@router.get("/auth/session", operation_id="identity_get_session", response_model=SessionResponse, responses=_ERRORS)
def get_session(current: CurrentUser = Depends(get_current_user), db: DbSession = Depends(get_db)) -> SessionResponse:
    return SessionResponse(
        csrf_token=current.csrf_token,
        idle_expires_at=current.session.idle_expires_at,
        absolute_expires_at=current.session.absolute_expires_at,
        user=build_me(db, current.user),
    )


@router.get("/me", operation_id="identity_get_me", response_model=MeResponse, responses=_ERRORS)
def get_me(current: CurrentUser = Depends(get_current_user), db: DbSession = Depends(get_db)) -> MeResponse:
    return build_me(db, current.user)


@router.post(
    "/me/notice-acknowledgements", operation_id="identity_post_notice_acknowledgement", response_model=MeResponse,
    responses={**_ERRORS, 409: {"description": "Notice version outdated"}},
)
def acknowledge_notice(
    body: NoticeAcknowledgementRequest, current: CurrentUser = Depends(require_csrf), db: DbSession = Depends(get_db)
) -> MeResponse:
    service.acknowledge_notice(db, current.user, body.notice_version)
    return build_me(db, current.user)


@router.put(
    "/me/job-role", operation_id="identity_put_job_role", response_model=MeResponse,
    responses={**_ERRORS, 404: {"description": "Job role not found"}, 409: {"description": "Job role inactive"}},
)
def select_job_role(
    body: JobRoleSelectionRequest, current: CurrentUser = Depends(require_csrf), db: DbSession = Depends(get_db)
) -> MeResponse:
    service.select_job_role(db, current.user, body.job_role_id)
    return build_me(db, current.user)
