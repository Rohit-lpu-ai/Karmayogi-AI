"""DEMO pack ``demo-3``: lessons for the ``demo-2`` courses (Phase 4B; DEC-045, DEC-052). Local and ci only.

Adds, for each of the twelve ``demo-2`` internal courses: two modules with two lessons each (reading, worked example,
practice check), a completion criterion, and four advisory prerequisites. Lesson text is synthetic, written for
product evaluation; every figure in it is invented. The pack is additive: it creates only what is missing, so a
course that already has modules is left untouched.
"""

from __future__ import annotations

from collections import Counter

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import AppEnv
from app.modules.learning.models import CourseModule, CoursePrerequisite, Lesson
from app.modules.organization.models import Organization
from app.modules.recommendation.models import Course
from app.seed.canonical import SeedRefused
from app.seed.demo_pack_3_lessons import CONTENT, PREREQUISITES

ALLOWED_ENVS = {AppEnv.local, AppEnv.ci}


def completion_criteria(lesson_count: int) -> str:
    return (f"Open and mark all {lesson_count} lessons as complete. Completion is recorded by you and does not change "
            "your competency estimate; only assessment evidence does.")


def seed_demo_pack_3(session: Session, org: Organization, app_env: AppEnv) -> Counter:
    if app_env not in ALLOWED_ENVS:
        raise SeedRefused(f"DEMO pack demo-3 is not allowed in {app_env.value}")
    created: Counter = Counter()
    courses = {c.external_ref: c for c in session.scalars(
        select(Course).where(Course.organization_id == org.id, Course.external_ref.in_(list(CONTENT))))}
    missing = sorted(set(CONTENT) - set(courses))
    if missing:
        raise SeedRefused(f"demo-3 needs the demo-2 courses first; missing {', '.join(missing)}")

    for ref, modules in CONTENT.items():
        course = courses[ref]
        has_modules = session.scalar(select(CourseModule.id).where(CourseModule.course_id == course.id).limit(1))
        if has_modules is None:
            for m_pos, (title, summary, lessons) in enumerate(modules, start=1):
                module = CourseModule(organization_id=org.id, course_id=course.id, position=m_pos, title=title,
                                      summary=summary)
                session.add(module)
                session.flush()
                created["course_modules"] += 1
                for l_pos, (l_title, l_type, minutes, body) in enumerate(lessons, start=1):
                    session.add(Lesson(organization_id=org.id, module_id=module.id, course_id=course.id, position=l_pos,
                                       title=l_title, lesson_type=l_type, estimated_minutes=minutes,
                                       content_kind="inline_markdown", body_markdown=body.strip() + "\n"))
                    created["lessons"] += 1
        if course.completion_criteria is None:
            course.completion_criteria = completion_criteria(sum(len(m[2]) for m in modules))
            created["completion_criteria"] += 1
        if course.content_origin != "synthetic":
            course.content_origin = "synthetic"

    for course_ref, prerequisite_ref in PREREQUISITES:
        course, prerequisite = courses[course_ref], courses[prerequisite_ref]
        exists = session.scalar(select(CoursePrerequisite.id).where(
            CoursePrerequisite.course_id == course.id, CoursePrerequisite.prerequisite_course_id == prerequisite.id))
        if exists is None:
            session.add(CoursePrerequisite(organization_id=org.id, course_id=course.id,
                                           prerequisite_course_id=prerequisite.id))
            created["course_prerequisites"] += 1
    session.flush()
    return created
