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


class SessionResponse(BaseModel):
    csrf_token: str
    idle_expires_at: datetime
    absolute_expires_at: datetime
    user: MeResponse


class NoticeAcknowledgementRequest(RequestModel):
    notice_version: str = Field(min_length=1, max_length=64)


class JobRoleSelectionRequest(RequestModel):
    job_role_id: uuid.UUID
