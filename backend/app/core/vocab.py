"""Shared enumerations used in CHECK constraints and schemas (DEC-029)."""

from __future__ import annotations

# Data provenance statuses (STATUS_VOCABULARY.md, plus NOT_APPLICABLE per DATA_MODEL.md §1.3).
DATA_STATUSES: tuple[str, ...] = (
    "VERIFIED",
    "UNKNOWN",
    "UNAVAILABLE",
    "MOCK",
    "ASSUMED",
    "MACHINE_OBSERVED",
    "UNVERIFIED_SECONDHAND",
    "EXCLUDED_BY_POLICY",
    "NOT_APPLICABLE",
)

# Statuses an automated import may write (STATUS_VOCABULARY.md rule 2): never VERIFIED or UNAVAILABLE.
MOCK = "MOCK"

ACCESS_ROLES: tuple[str, ...] = (
    "learner",
    "trainer",
    "department_admin",
    "org_admin",
    "competency_admin",
    "training_manager",
    "auditor",
    "platform_admin",
)

ACTIVE_INACTIVE: tuple[str, ...] = ("active", "inactive")
