"""Auth and self-service routes (API_INTEGRATION_SPEC.md §2.2-2.3)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session as DbSession

from app.core.config import AppEnv, Settings
from app.core.db import get_db
from app.core.demo import is_demo_code
from app.modules.identity import accounts, service
from app.modules.identity.policy import capabilities_for
from app.modules.identity.dependencies import (
    SELF_LEARNING_ROLES,
    CurrentUser,
    get_current_user,
    get_settings_dep,
    require_csrf,
)
from app.modules.identity.models import User
from app.modules.identity.schemas import (
    DepartmentRef,
    JobRoleRef,
    PasswordChangeRequest,
    PasswordSetRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    RegistrationOptions,
    JobRoleSelectionRequest,
    LoginRequest,
    MeResponse,
    NoticeAcknowledgementRequest,
    NoticeState,
    SessionResponse,
)
from app.modules.identity.security import csrf_token_for
from app.modules.organization.models import Department, JobRole

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
        registration_id=user.registration_id,
        department=_department_ref(db, user),
        must_change_password=user.must_change_password,
        admin_capabilities=capabilities_for(roles),
        last_login_at=user.last_login_at,
    )


def _department_ref(db: DbSession, user: User) -> DepartmentRef | None:
    department = db.get(Department, user.department_id) if user.department_id else None
    return DepartmentRef(id=department.id, name=department.name, code=department.code) if department else None


def _set_session_cookie(response: Response, settings: Settings, token: str) -> None:
    response.set_cookie(
        settings.session_cookie_name, token,
        max_age=settings.session_absolute_timeout_hours * 3600,
        httponly=True, secure=settings.session_cookie_secure, samesite="lax", path="/",
    )


@router.post(
    "/auth/login", operation_id="identity_post_login", response_model=SessionResponse,
    responses={401: {"description": "Invalid credentials"}, 423: {"description": "Account locked"}},
)
def login(
    body: LoginRequest, response: Response, db: DbSession = Depends(get_db), settings: Settings = Depends(get_settings_dep)
) -> SessionResponse:
    result = service.login(db, settings, body.email, body.password, body.organization_code)
    _set_session_cookie(response, settings, result.token)
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


# --- Phase 4A: registration, password flows, profile ------------------------------------------------------


@router.get("/auth/registration-options", operation_id="identity_get_registration_options", response_model=RegistrationOptions)
def get_registration_options(
    organization_code: str | None = Query(default=None, min_length=2, max_length=63, pattern=r"^[a-z0-9][a-z0-9-]+$"),
    db: DbSession = Depends(get_db), settings: Settings = Depends(get_settings_dep),
) -> RegistrationOptions:
    return RegistrationOptions(**accounts.registration_options(db, settings, organization_code))


@router.post(
    "/auth/register", operation_id="identity_post_register", response_model=SessionResponse, status_code=201,
    responses={403: {"description": "Registration disabled"}, 409: {"description": "Email or registration ID in use"},
               422: {"description": "Validation failed"}},
)
def register(body: RegisterRequest, response: Response, db: DbSession = Depends(get_db),
             settings: Settings = Depends(get_settings_dep)) -> SessionResponse:
    user = accounts.register_learner(db, settings, display_name=body.display_name, email=body.email, password=body.password,
                                     registration_id=body.registration_id, department_id=body.department_id,
                                     job_role_id=body.job_role_id, organization_code=body.organization_code)
    result = service.start_session(db, settings, user)
    db.commit()
    _set_session_cookie(response, settings, result.token)
    return SessionResponse(
        csrf_token=csrf_token_for(settings.session_secret.get_secret_value(), result.token),
        idle_expires_at=result.session.idle_expires_at, absolute_expires_at=result.session.absolute_expires_at,
        user=build_me(db, user),
    )


@router.post("/auth/password/change", operation_id="identity_post_password_change", status_code=204,
             responses={**_ERRORS, 422: {"description": "Current password incorrect or invalid new password"}})
def change_password(body: PasswordChangeRequest, current: CurrentUser = Depends(require_csrf),
                    db: DbSession = Depends(get_db)) -> Response:
    accounts.change_password(db, current.user, current.session, body.current_password, body.new_password)
    return Response(status_code=204)


@router.post("/auth/password/set", operation_id="identity_post_password_set", status_code=204,
             responses={400: {"description": "Token invalid, used or expired"}, 422: {"description": "Invalid password"}})
def set_password(body: PasswordSetRequest, db: DbSession = Depends(get_db)) -> Response:
    accounts.set_password_with_token(db, body.token, body.new_password)
    return Response(status_code=204)


@router.patch("/me", operation_id="identity_patch_me", response_model=MeResponse,
              responses={**_ERRORS, 422: {"description": "Validation failed"}})
def update_me(body: ProfileUpdateRequest, current: CurrentUser = Depends(require_csrf), db: DbSession = Depends(get_db)) -> MeResponse:
    accounts.update_profile(db, current.user, fields=body.model_dump(exclude_unset=True))
    return build_me(db, current.user)


class EnvironmentInfo(BaseModel):
    synthetic_data: bool
    self_registration_enabled: bool


@router.get("/environment", operation_id="platform_get_environment", response_model=EnvironmentInfo)
def get_environment(settings: Settings = Depends(get_settings_dep)) -> EnvironmentInfo:
    """Public flags the sign-in and shell screens need: whether this environment carries synthetic data (one banner,
    K-2) and whether learners may register. No configuration values are exposed."""
    return EnvironmentInfo(synthetic_data=settings.app_env in (AppEnv.local, AppEnv.ci, AppEnv.staging),
                           self_registration_enabled=settings.self_registration_enabled)


@router.get("/departments", operation_id="organization_list_departments", response_model=list[DepartmentRef], responses=_ERRORS)
def list_departments(current: CurrentUser = Depends(get_current_user), db: DbSession = Depends(get_db)) -> list[DepartmentRef]:
    """Active departments in the caller's organisation, for profile editing."""
    rows = db.scalars(select(Department).where(Department.organization_id == current.user.organization_id,
                                               Department.status == "active").order_by(Department.name))
    return [DepartmentRef(id=d.id, name=d.name, code=d.code) for d in rows]
