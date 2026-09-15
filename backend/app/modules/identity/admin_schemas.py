"""Administration schemas for users and departments (Phase 4A). Password hashes and token hashes are never serialised."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.modules.identity.models import REGISTRATION_ID_PATTERN
from app.modules.identity.schemas import DepartmentRef, RequestModel

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class RoleAssignment(BaseModel):
    role: str
    department_scope_id: uuid.UUID | None = None


class RoleAssignmentRequest(RequestModel):
    role: str = Field(min_length=3, max_length=40)
    department_scope_id: uuid.UUID | None = None


class NamedRef(BaseModel):
    id: uuid.UUID
    name: str


class AdminUser(BaseModel):
    id: uuid.UUID
    display_name: str
    email: str
    registration_id: str | None
    designation: str | None
    status: str
    department: DepartmentRef | None
    job_role: NamedRef | None
    roles: list[RoleAssignment]
    is_synthetic: bool
    has_password: bool
    last_login_at: datetime | None
    created_at: datetime
    row_version: int


class AdminUserPage(BaseModel):
    items: list[AdminUser]
    total: int
    page: int
    page_size: int


class AdminUserCreateRequest(RequestModel):
    display_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=3, max_length=254, pattern=EMAIL_PATTERN)
    registration_id: str | None = Field(default=None, pattern=REGISTRATION_ID_PATTERN)
    designation: str | None = Field(default=None, max_length=120)
    department_id: uuid.UUID | None = None
    job_role_id: uuid.UUID | None = None
    roles: list[RoleAssignmentRequest] = Field(default_factory=lambda: [RoleAssignmentRequest(role="learner")],
                                               min_length=1, max_length=8)


class AdminUserUpdateRequest(RequestModel):
    row_version: int = Field(ge=1)
    display_name: str | None = Field(default=None, min_length=2, max_length=120)
    registration_id: str | None = Field(default=None, pattern=REGISTRATION_ID_PATTERN)
    designation: str | None = Field(default=None, max_length=120)
    department_id: uuid.UUID | None = None
    job_role_id: uuid.UUID | None = None
    status: Literal["active", "inactive"] | None = None
    roles: list[RoleAssignmentRequest] | None = Field(default=None, min_length=1, max_length=8)


class PasswordLink(BaseModel):
    """A one-time token, returned once to the administrator who issued it. It is never stored in plain text."""

    purpose: str
    token: str
    expires_at: datetime


class AdminUserCreated(BaseModel):
    user: AdminUser
    setup: PasswordLink


class AdminDepartment(BaseModel):
    id: uuid.UUID
    name: str
    code: str | None
    status: str
    user_count: int


class DepartmentCreateRequest(RequestModel):
    name: str = Field(min_length=2, max_length=120)
    code: str | None = Field(default=None, min_length=2, max_length=40, pattern=r"^[a-z0-9][a-z0-9-]+$")


class DepartmentUpdateRequest(RequestModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    code: str | None = Field(default=None, min_length=2, max_length=40, pattern=r"^[a-z0-9][a-z0-9-]+$")
    status: Literal["active", "inactive"] | None = None


class AdminRole(BaseModel):
    role: str
    label: str
    description: str
    capabilities: list[str]
    user_count: int
    department_scoped: bool
