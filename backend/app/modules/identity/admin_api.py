"""Administration routes for users and departments (Phase 4A). Every route checks a policy capability on the server."""

from __future__ import annotations

import uuid
from typing import Literal

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session as DbSession

from app.core.config import Settings
from app.core.db import get_db
from app.modules.identity import admin
from app.modules.identity.admin_schemas import (
    AdminDepartment,
    AdminRole,
    AdminUser,
    AdminUserCreated,
    AdminUserCreateRequest,
    AdminUserPage,
    AdminUserUpdateRequest,
    DepartmentCreateRequest,
    DepartmentUpdateRequest,
    PasswordLink,
)
from app.modules.identity.dependencies import CurrentUser, get_settings_dep, require_capability

router = APIRouter(prefix="/api/v1/admin", tags=["administration"])

_ERRORS = {401: {"description": "Not signed in"}, 403: {"description": "CSRF or permission failure"}}
_WRITE_ERRORS = {**_ERRORS, 404: {"description": "Not found"}, 409: {"description": "Conflict"},
                 422: {"description": "Validation failed"}}


@router.get("/users", operation_id="admin_list_users", response_model=AdminUserPage, responses=_ERRORS)
def list_users(
    q: str | None = Query(default=None, max_length=120),
    status: Literal["invited", "active", "locked", "inactive"] | None = None,
    role: str | None = Query(default=None, max_length=40),
    department_id: uuid.UUID | None = None,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=25, ge=1, le=100),
    current: CurrentUser = Depends(require_capability("users.view")),
    db: DbSession = Depends(get_db),
) -> AdminUserPage:
    items, total = admin.list_users(db, current, q=q, status=status, role=role, department_id=department_id,
                                    page=page, page_size=page_size)
    return AdminUserPage(items=items, total=total, page=page, page_size=page_size)


@router.post("/users", operation_id="admin_create_user", response_model=AdminUserCreated, status_code=201,
             responses=_WRITE_ERRORS)
def create_user(
    body: AdminUserCreateRequest,
    current: CurrentUser = Depends(require_capability("users.manage", csrf=True)),
    db: DbSession = Depends(get_db),
    settings: Settings = Depends(get_settings_dep),
) -> AdminUserCreated:
    user, token, expires_at = admin.create_user(db, settings, current, body)
    return AdminUserCreated(user=user, setup=PasswordLink(purpose="account_setup", token=token, expires_at=expires_at))


@router.get("/users/{user_id}", operation_id="admin_get_user", response_model=AdminUser,
            responses={**_ERRORS, 404: {"description": "Not found"}})
def get_user(user_id: uuid.UUID, current: CurrentUser = Depends(require_capability("users.view")),
             db: DbSession = Depends(get_db)) -> AdminUser:
    return admin.get_user(db, current, user_id)


@router.patch("/users/{user_id}", operation_id="admin_update_user", response_model=AdminUser, responses=_WRITE_ERRORS)
def update_user(user_id: uuid.UUID, body: AdminUserUpdateRequest,
                current: CurrentUser = Depends(require_capability("users.manage", csrf=True)),
                db: DbSession = Depends(get_db)) -> AdminUser:
    return admin.update_user(db, current, user_id, body)


@router.post("/users/{user_id}/password-link", operation_id="admin_issue_password_link", response_model=PasswordLink,
             status_code=201, responses=_WRITE_ERRORS)
def issue_password_link(user_id: uuid.UUID,
                        current: CurrentUser = Depends(require_capability("users.manage", csrf=True)),
                        db: DbSession = Depends(get_db), settings: Settings = Depends(get_settings_dep)) -> PasswordLink:
    purpose, token, expires_at = admin.issue_reset(db, settings, current, user_id)
    return PasswordLink(purpose=purpose, token=token, expires_at=expires_at)


@router.get("/roles", operation_id="admin_list_roles", response_model=list[AdminRole], responses=_ERRORS)
def list_roles(current: CurrentUser = Depends(require_capability("users.view")),
               db: DbSession = Depends(get_db)) -> list[AdminRole]:
    return admin.list_roles(db, current)


@router.get("/departments", operation_id="admin_list_departments", response_model=list[AdminDepartment], responses=_ERRORS)
def list_departments(current: CurrentUser = Depends(require_capability("users.view")),
                     db: DbSession = Depends(get_db)) -> list[AdminDepartment]:
    return admin.list_departments(db, current)


@router.post("/departments", operation_id="admin_create_department", response_model=AdminDepartment, status_code=201,
             responses=_WRITE_ERRORS)
def create_department(body: DepartmentCreateRequest,
                      current: CurrentUser = Depends(require_capability("departments.manage", csrf=True)),
                      db: DbSession = Depends(get_db)) -> AdminDepartment:
    return admin.create_department(db, current, body.name, body.code)


@router.patch("/departments/{department_id}", operation_id="admin_update_department", response_model=AdminDepartment,
              responses=_WRITE_ERRORS)
def update_department(department_id: uuid.UUID, body: DepartmentUpdateRequest,
                      current: CurrentUser = Depends(require_capability("departments.manage", csrf=True)),
                      db: DbSession = Depends(get_db)) -> AdminDepartment:
    return admin.update_department(db, current, department_id, body.model_dump(exclude_unset=True))
