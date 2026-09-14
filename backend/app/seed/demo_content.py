"""Synthetic DEMO content for the vertical slice (DEC-045, DEC-046). Local and ci only.

Why this exists: no official functional competency framework, role mapping,
approved question or reviewed course mapping exists (DEC-013), so the
login → assessment → gap → recommendation journey cannot run on real data.

What it is:
- every code starts with ``DEMO-`` and every name/title with ``DEMO``;
- questions are self-contained arithmetic with mathematically certain keys, not
  statistical methodology, and not official assessment content;
- the framework stays ``draft``; thresholds stay ``provisional``;
- mappings, questions, the assessment and courses are marked approved/published by
  the seed on behalf of the synthetic competency admin. That is **not** human review
  (no ReviewTask/Approval records) and is recorded in the audit log as a demo seed action.

It is refused outside local and ci and never touches the imported official records.
"""

from __future__ import annotations

import hashlib
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import AppEnv
from app.modules.assessment.models import Assessment, AssessmentQuestion, Question, QuestionOption, QuestionVersion
from app.modules.competency.models import Competency, CompetencyFramework, CompetencyLevel, RoleCompetency
from app.modules.governance.service import record_audit
from app.modules.identity.models import User
from app.modules.organization.models import JobRole, Organization
from app.modules.recommendation.models import Course, CourseCompetency
from app.seed.canonical import SeedRefused
from app.seed.demo_users import demo_email

DEMO_ALLOWED_ENVS = {AppEnv.local, AppEnv.ci}
FRAMEWORK_CODE = "DEMO-FUNCTIONAL"
JOB_ROLE_CODE = "DEMO-ROLE-STAT-ASSISTANT"
ITEM_NOTE = "DEMO item: synthetic arithmetic for local testing, not an official assessment question."

LEVELS = (  # provisional demo thresholds (DEC-020 still undecided)
    (1, "Level 1", Decimal("0.00000")),
    (2, "Level 2", Decimal("0.40000")),
    (3, "Level 3", Decimal("0.60000")),
    (4, "Level 4", Decimal("0.80000")),
)

COMPETENCIES = (
    ("DEMO-C1", "DEMO - Descriptive statistics (synthetic)", 3),
    ("DEMO-C2", "DEMO - Percentages and proportions (synthetic)", 3),
)

# (competency code, difficulty, stem, [A, B, C, D], correct label, explanation)
ITEMS = (
    ("DEMO-C1", "foundational", "What is the arithmetic mean of 4, 8 and 12?", ["6", "8", "10", "12"], "B",
     "(4 + 8 + 12) / 3 = 24 / 3 = 8."),
    ("DEMO-C1", "foundational", "What is the median of 3, 9, 5, 7 and 11?", ["5", "7", "9", "35"], "B",
     "Sorted: 3, 5, 7, 9, 11. The middle (third) value is 7."),
    ("DEMO-C1", "intermediate", "What is the mode of 2, 4, 4, 5, 7, 7, 7?", ["4", "5", "7", "There is no mode"], "C",
     "7 appears three times, more often than any other value."),
    ("DEMO-C1", "intermediate", "What is the range of 12, 5, 20 and 9?", ["8", "11", "15", "20"], "C",
     "Range = maximum - minimum = 20 - 5 = 15."),
    ("DEMO-C1", "advanced", "The mean of five values is 10. Four of them are 8, 9, 11 and 12. What is the fifth value?",
     ["8", "10", "12", "50"], "B", "Total = 5 x 10 = 50. Known values sum to 40, so the fifth is 50 - 40 = 10."),
    ("DEMO-C2", "foundational", "What is 25% of 200?", ["25", "40", "50", "75"], "C", "0.25 x 200 = 50."),
    ("DEMO-C2", "foundational", "What proportion is 30 out of 120?", ["0.20", "0.25", "0.30", "0.40"], "B",
     "30 / 120 = 0.25."),
    ("DEMO-C2", "intermediate", "A value rises from 80 to 100. What is the percentage increase?",
     ["20%", "25%", "80%", "125%"], "B", "(100 - 80) / 80 = 20 / 80 = 25%."),
    ("DEMO-C2", "intermediate", "A value falls from 50 to 40. What is the percentage decrease?",
     ["10%", "20%", "25%", "80%"], "B", "(50 - 40) / 50 = 10 / 50 = 20%."),
    ("DEMO-C2", "advanced", "A value is increased by 10% and the result is then decreased by 10%. What is the net change?",
     ["No change", "1% decrease", "1% increase", "20% decrease"], "B",
     "1.10 x 0.90 = 0.99, which is a 1% decrease from the original value."),
)

COURSES = (
    # (external_ref, title, duration_days, [(competency code, relevance)])
    ("DEMO-COURSE-1", "DEMO - Working with averages (synthetic course)", 2, [("DEMO-C1", "primary")]),
    ("DEMO-COURSE-2", "DEMO - Percentages refresher (synthetic course)", 1, [("DEMO-C2", "primary")]),
    ("DEMO-COURSE-3", "DEMO - Reading simple data tables (synthetic course)", 3,
     [("DEMO-C1", "secondary"), ("DEMO-C2", "secondary")]),
)


def content_hash(stem: str, options: list[str]) -> str:
    def norm(value: str) -> str:
        return " ".join(unicodedata.normalize("NFKC", value).lower().split())
    payload = "|".join([norm(stem), *sorted(norm(o) for o in options)])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def seed_demo_content(session: Session, org: Organization, app_env: AppEnv) -> Counter:
    if app_env not in DEMO_ALLOWED_ENVS:
        raise SeedRefused(f"DEMO content is not allowed in {app_env.value}")
    admin = session.scalar(select(User).where(User.organization_id == org.id, User.email == demo_email("competency_admin")))
    if admin is None:
        raise SeedRefused("DEMO content needs the synthetic demo users; run with --demo-users")
    created: Counter = Counter()
    now = datetime.now(timezone.utc)

    framework = session.scalar(select(CompetencyFramework).where(CompetencyFramework.organization_id == org.id,
                                                                 CompetencyFramework.code == FRAMEWORK_CODE))
    if framework is not None:
        return created  # idempotent: the demo set is created once, as a unit

    framework = CompetencyFramework(
        organization_id=org.id, name="DEMO - Synthetic functional framework (not official)", code=FRAMEWORK_CODE,
        framework_type="functional", publisher="DEMO (synthetic, local development only)", version_label="demo-1",
        status="draft", definitions_restricted=False, created_by=admin.id,
    )
    session.add(framework)
    session.flush()
    for number, label, min_score in LEVELS:
        session.add(CompetencyLevel(organization_id=org.id, framework_id=framework.id, level_number=number, label=label,
                                    min_score=min_score, threshold_status="provisional", created_by=admin.id))
    competencies = {}
    for code, name, _ in COMPETENCIES:
        competencies[code] = Competency(
            organization_id=org.id, framework_id=framework.id, code=code, name=name, data_status="ASSUMED",
            description="Synthetic demo competency for local testing. Not an official competency definition.",
            created_by=admin.id,
        )
        session.add(competencies[code])
    job_role = JobRole(organization_id=org.id, name="DEMO - Statistical Assistant (synthetic role)", code=JOB_ROLE_CODE,
                       description="Synthetic job role for local testing. Not an official role definition.",
                       created_by=admin.id)
    session.add(job_role)
    session.flush()
    created.update(competency_frameworks=1, competency_levels=len(LEVELS), competencies=len(COMPETENCIES), job_roles=1)

    for code, _, required in COMPETENCIES:
        session.add(RoleCompetency(organization_id=org.id, job_role_id=job_role.id, competency_id=competencies[code].id,
                                   required_level_number=required, status="approved", approved_by=admin.id,
                                   approved_at=now, created_by=admin.id))
        created["role_competencies"] += 1

    assessment = Assessment(
        organization_id=org.id, title="DEMO - Baseline assessment (synthetic arithmetic items)", purpose="pre",
        job_role_id=job_role.id, feedback_policy="correctness_and_explanations", status="published",
        published_at=now, published_by=admin.id, created_by=admin.id,
        blueprint={"demo_seed": True, "competencies": [c[0] for c in COMPETENCIES], "min_items_per_competency": 5},
    )
    session.add(assessment)
    session.flush()

    for code, difficulty, stem, options, correct, explanation in ITEMS:
        question = Question(organization_id=org.id, origin="demo_seed", status="pending_validation", created_by=admin.id)
        session.add(question)
        session.flush()
        version = QuestionVersion(
            organization_id=org.id, question_id=question.id, version_number=1, stem=stem,
            explanation=f"{explanation} ({ITEM_NOTE})", difficulty=difficulty, difficulty_confirmed=False,
            competency_id=competencies[code].id, content_hash=content_hash(stem, options), created_by=admin.id,
        )
        session.add(version)
        session.flush()
        for position, (label, text) in enumerate(zip("ABCD", options, strict=True), start=1):
            session.add(QuestionOption(organization_id=org.id, question_version_id=version.id, label=label, text=text,
                                       is_correct=label == correct, position=position))
        question.current_version_id = version.id
        question.approved_version_id = version.id
        question.status = "approved"
        session.add(AssessmentQuestion(organization_id=org.id, assessment_id=assessment.id,
                                       question_version_id=version.id, created_by=admin.id))
        created["questions"] += 1
    created["assessments"] = 1

    for ref, title, days, mappings in COURSES:
        course = Course(
            organization_id=org.id, course_type="internal", title=title, provider_organisation="DEMO provider (synthetic)",
            description="Synthetic course for local testing. Not a real training programme.", duration_days=days,
            external_ref=ref, data_status="ASSUMED", review_status="approved", status="active", created_by=admin.id,
        )
        session.add(course)
        session.flush()
        for code, relevance in mappings:
            session.add(CourseCompetency(organization_id=org.id, course_id=course.id, competency_id=competencies[code].id,
                                         relevance=relevance, method="demo_seed", status="approved", approved_by=admin.id,
                                         approved_at=now, created_by=admin.id))
            created["course_competencies"] += 1
        created["courses"] += 1

    record_audit(session, organization_id=org.id, action="seed.import", target_type="demo_content",
                 target_id=FRAMEWORK_CODE, after={"created": dict(created), "label": "DEMO synthetic content"},
                 reason="DEMO seed: synthetic approvals for local pipeline testing, not human review (DEC-045)")
    session.flush()
    return created
