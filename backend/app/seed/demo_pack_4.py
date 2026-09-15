"""DEMO pack ``demo-4``: a synthetic learner cohort for aggregated insight (Phase 4D; plan A-3). Local and ci only.

Why: department skill-gap and training-needs views are only meaningful with many learners. Rather than writing
estimates directly, every cohort learner goes through the real pipeline - notice acknowledgement, job role, the
published baseline assessment scored by ``score-v1``, and (for some) lesson completion - so every figure an
administrator sees is derived from recorded evidence.

What it creates (all synthetic, emails ``cohort-...@example.invalid``, no passwords, so nobody can sign in as them):
- three departments named "DEMO ... (synthetic)";
- 38 learners: 18 in the survey division, 16 in the prices division and 4 in data services. The small department is
  deliberate: its cells are suppressed in every aggregate (fewer than 5 learners);
- answers chosen by a seeded random generator from invented per-department accuracy profiles, so gaps differ by
  department in a plausible but entirely made-up way;
- lesson progress for some learners on the first course of their learning path.

The pack is additive: learners that already exist are skipped. Cohort accounts are excluded from
``demo_reset --all-synthetic`` so a demo reset does not empty the insight views.
"""

from __future__ import annotations

import random
from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import AppEnv
from app.modules.assessment import service as assessment_service
from app.modules.assessment.models import AttemptQuestion, QuestionOption, QuestionVersion
from app.modules.competency.models import Competency
from app.modules.identity import service as identity_service
from app.modules.identity.models import User, UserAccessRole
from app.modules.learning import service as learning_service
from app.modules.organization.models import Department, JobRole, Organization
from app.seed.canonical import SeedRefused

ALLOWED_ENVS = {AppEnv.local, AppEnv.ci}
COHORT_PREFIX = "cohort-"

# (department code, name, job role code, learners, accuracy by competency code; default 0.55). Invented profiles.
DEPARTMENTS = (
    ("demo-survey", "DEMO Survey Operations Division (synthetic)", "DEMO-ROLE-SURVEY", 18,
     {"DEMO-SP-SAMPLING": 0.35, "DEMO-SP-QUALITY": 0.45, "DEMO-SP-TABLES": 0.7, "DEMO-SP-DIST": 0.5}),
    ("demo-prices", "DEMO Price Statistics Division (synthetic)", "DEMO-ROLE-PRICES", 16,
     {"DEMO-SP-INDEX": 0.4, "DEMO-SP-RATES": 0.55, "DEMO-SP-DIST": 0.45, "DEMO-SP-COMM": 0.35}),
    ("demo-data", "DEMO Data Services Unit (synthetic)", "DEMO-ROLE-JSO", 4,
     {"DEMO-SP-DESC": 0.5, "DEMO-SP-TABLES": 0.4, "DEMO-SP-RATES": 0.45, "DEMO-SP-QUALITY": 0.6}),
)


def is_cohort_email(email: str) -> bool:
    return email.lower().startswith(COHORT_PREFIX)


def seed_demo_pack_4(session: Session, org: Organization, app_env: AppEnv) -> Counter:
    if app_env not in ALLOWED_ENVS:
        raise SeedRefused(f"DEMO pack demo-4 is not allowed in {app_env.value}")
    created: Counter = Counter()
    competencies = {c.id: c.code for c in session.scalars(select(Competency).where(Competency.organization_id == org.id))}

    for dept_code, dept_name, role_code, size, profile in DEPARTMENTS:
        role = session.scalar(select(JobRole).where(JobRole.organization_id == org.id, JobRole.code == role_code))
        if role is None:
            raise SeedRefused(f"demo-4 needs pack demo-2 first; job role {role_code} is missing")
        department = session.scalar(select(Department).where(Department.organization_id == org.id, Department.code == dept_code))
        if department is None:
            department = Department(organization_id=org.id, name=dept_name, code=dept_code, status="active")
            session.add(department)
            session.flush()
            created["departments"] += 1

        for n in range(1, size + 1):
            email = f"{COHORT_PREFIX}{dept_code.removeprefix('demo-')}-{n:02d}@example.invalid"
            if session.scalar(select(User.id).where(User.organization_id == org.id, User.email == email)) is not None:
                continue
            rng = random.Random(f"demo-4:{email}")  # deterministic per learner
            user = User(organization_id=org.id, email=email, display_name=f"DEMO Cohort Learner {dept_code[5:]} {n:02d} (synthetic)",
                        department_id=department.id, status="active", is_synthetic=True,
                        registration_id=f"DEMO-COHORT-{dept_code[5:].upper()}-{n:02d}")
            session.add(user)
            session.flush()
            session.add(UserAccessRole(organization_id=org.id, user_id=user.id, role="learner"))
            session.flush()
            identity_service.acknowledge_notice(session, user, identity_service.NOTICE_VERSION)
            identity_service.select_job_role(session, user, role.id)
            user.job_role_id = role.id

            assessments = assessment_service.available_assessments(session, user)
            if not assessments:
                raise SeedRefused(f"demo-4 needs a published baseline for {role_code}")
            attempt, _ = assessment_service.start_or_resume(session, user, assessments[0]["id"])
            skill = rng.uniform(-0.15, 0.15)  # individual variation around the department profile
            for delivered in session.scalars(select(AttemptQuestion).where(AttemptQuestion.attempt_id == attempt.id)):
                version = session.get(QuestionVersion, delivered.question_version_id)
                options = list(session.scalars(select(QuestionOption).where(QuestionOption.question_version_id == version.id)))
                accuracy = min(0.95, max(0.05, profile.get(competencies.get(version.competency_id, ""), 0.55) + skill))
                correct = next(o for o in options if o.is_correct)
                wrong = [o for o in options if not o.is_correct]
                choice = correct if rng.random() < accuracy else rng.choice(wrong)
                assessment_service.save_answer(session, user, attempt.id, version.id, choice.id)
            assessment_service.submit(session, user, attempt.id, ["learner"])
            created["learners"] += 1
            created["baselines_scored"] += 1

            # Some learners start their learning path: about a third complete the first course, a third start it.
            path = learning_service.learning_path(session, user)
            first = next((i for g in path["groups"] for i in g["items"] if i["course"]), None)
            roll = rng.random()
            if first and roll < 0.66:
                outline = learning_service.course_outline(session, user, first["course"]["id"])
                lessons = [lesson["id"] for m in outline["modules"] for lesson in m["lessons"]]
                count = len(lessons) if roll < 0.33 else 1
                for lesson_id in lessons[:count]:
                    learning_service.set_lesson_progress(session, user, lesson_id, "completed")
                    created["lessons_completed"] += 1
                created["courses_completed" if roll < 0.33 and lessons else "courses_started"] += 1
    session.flush()
    return created
