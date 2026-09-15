from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RequestModel(BaseModel):
    """Requests reject unknown fields (API_INTEGRATION_SPEC.md §1.8, no mass assignment)."""

    model_config = ConfigDict(extra="forbid")


class LoginRequest(RequestModel):
    email: str = Field(min_length=3, max_length=254, pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    password: str = Field(min_length=1, max_length=256)
    organization_code: str | None = Field(default=None, min_length=2, max_length=63, pattern=r"^[a-z0-9][a-z0-9-]+$")


class JobRoleRef(BaseModel):
    id: uuid.UUID
    name: str
    code: str | None
    is_demo: bool


class NoticeState(BaseModel):
    notice_type: str
    version: str
    status: str
    text: str
    acknowledged_at: datetime | None


class DepartmentRef(BaseModel):
    id: uuid.UUID
    name: str
    code: str | None


class MeResponse(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str
    designation: str | None
    organization_id: uuid.UUID
    access_roles: list[str]
    can_take_assessments: bool
    job_role: JobRoleRef | None
    notice: NoticeState
    is_synthetic: bool
    # Phase 4A (optional fields, non-breaking)
    registration_id: str | None = None
    department: DepartmentRef | None = None
    must_change_password: bool = False
    admin_capabilities: list[str] = []
    last_login_at: datetime | None = None


class SessionResponse(BaseModel):
    csrf_token: str
    idle_expires_at: datetime
    absolute_expires_at: datetime
    user: MeResponse


class NoticeAcknowledgementRequest(RequestModel):
    notice_version: str = Field(min_length=1, max_length=64)


class JobRoleSelectionRequest(RequestModel):
    job_role_id: uuid.UUID


REGISTRATION_ID = r"^[A-Za-z0-9][A-Za-z0-9/-]{2,39}$"
EMAIL = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class RegisterRequest(RequestModel):
    display_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=3, max_length=254, pattern=EMAIL)
    password: str = Field(min_length=12, max_length=256)
    registration_id: str = Field(min_length=3, max_length=40, pattern=REGISTRATION_ID)
    department_id: uuid.UUID | None = None
    job_role_id: uuid.UUID | None = None
    organization_code: str | None = Field(default=None, min_length=2, max_length=63, pattern=r"^[a-z0-9][a-z0-9-]+$")


class RegistrationOption(BaseModel):
    id: uuid.UUID
    name: str


class RegistrationOptions(BaseModel):
    enabled: bool
    organization_name: str | None = None
    departments: list[RegistrationOption] = []
    job_roles: list[RegistrationOption] = []


class PasswordChangeRequest(RequestModel):
    current_password: str = Field(min_length=1, max_length=256)
    new_password: str = Field(min_length=12, max_length=256)


class PasswordSetRequest(RequestModel):
    token: str = Field(min_length=20, max_length=200)
    new_password: str = Field(min_length=12, max_length=256)


class ProfileUpdateRequest(RequestModel):
    display_name: str | None = Field(default=None, min_length=2, max_length=120)
    designation: str | None = Field(default=None, max_length=120)
    department_id: uuid.UUID | None = None
