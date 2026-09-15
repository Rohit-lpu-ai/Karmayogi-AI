"""Capability policy: the SECURITY_RESPONSIBLE_AI.md §4 permission matrix as code.

Authorisation is decided here, on the server, for every administrative endpoint. The frontend only uses the
capability list returned by ``GET /me`` to decide which navigation to show.

Scopes: ``department_admin`` capabilities apply only inside the department in its ``department_scope_id``
(enforced by the calling service). Separation of duties: ``auditor`` is read-only; ``platform_admin`` does not
see learner competency data.
"""

from __future__ import annotations

from collections.abc import Iterable

CAPABILITIES: dict[str, frozenset[str]] = {
    # Users and organisation
    "users.view": frozenset({"org_admin", "platform_admin", "department_admin"}),
    "users.manage": frozenset({"org_admin", "platform_admin", "department_admin"}),  # department_admin: own dept
    "roles.assign": frozenset({"org_admin", "platform_admin"}),
    "departments.manage": frozenset({"org_admin", "platform_admin"}),
    # Competency structure
    "job_roles.manage": frozenset({"org_admin", "competency_admin"}),
    "frameworks.view": frozenset({"org_admin", "competency_admin", "training_manager", "auditor"}),
    "frameworks.manage": frozenset({"competency_admin"}),
    # Content
    "questions.author": frozenset({"trainer", "competency_admin"}),
    "questions.review": frozenset({"trainer", "competency_admin"}),
    "assessments.manage": frozenset({"trainer", "competency_admin"}),
    "courses.manage": frozenset({"org_admin", "competency_admin", "training_manager"}),
    "courses.review": frozenset({"org_admin", "training_manager", "competency_admin"}),
    "sources.view": frozenset({"org_admin", "competency_admin", "training_manager", "trainer"}),
    # Insight (aggregates only; P1 pull-forward under assumption A-3)
    "insight.view": frozenset({"org_admin", "competency_admin", "training_manager", "department_admin"}),
    # Governance
    "audit.view": frozenset({"auditor", "platform_admin", "org_admin"}),
}

ROLE_DESCRIPTIONS: dict[str, tuple[str, str]] = {
    "learner": ("Learner", "Takes assessments, sees their own gaps and follows recommended learning."),
    "trainer": ("Trainer", "Authors and reviews questions and assessments for their department."),
    "department_admin": ("Department administrator", "Manages learner accounts and sees aggregated insight for one department."),
    "org_admin": ("Organisation administrator", "Manages users, roles, departments, courses and organisation settings."),
    "competency_admin": ("Competency administrator", "Maintains frameworks, job-role requirements, questions and courses."),
    "training_manager": ("Training manager", "Manages the course catalogue and reads aggregated training needs."),
    "auditor": ("Auditor", "Read-only access to the audit trail and frameworks. Cannot change anything."),
    "platform_admin": ("Platform administrator", "Technical administration of accounts. No access to learner competency data."),
}

ADMIN_ROLES = frozenset({"trainer", "department_admin", "org_admin", "competency_admin", "training_manager",
                         "auditor", "platform_admin"})

# Roles an org_admin may grant; platform_admin may grant any role (SECURITY §4 "Assign access roles").
GRANTABLE_BY_ORG_ADMIN = frozenset({"learner", "trainer", "department_admin", "org_admin", "competency_admin",
                                    "training_manager", "auditor"})


def capabilities_for(roles: Iterable[str]) -> list[str]:
    held = set(roles)
    return sorted(name for name, allowed in CAPABILITIES.items() if held & allowed)


def has_capability(roles: Iterable[str], capability: str) -> bool:
    return bool(set(roles) & CAPABILITIES[capability])


def only_department_scoped(roles: Iterable[str], capability: str) -> bool:
    """True when the caller holds the capability solely through department_admin (so results must be scoped)."""
    granting = set(roles) & CAPABILITIES[capability]
    return granting == {"department_admin"}
