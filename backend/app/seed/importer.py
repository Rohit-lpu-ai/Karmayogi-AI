"""Idempotent import of canonical datasets into the reference tables.

Rules (DATA_MODEL.md §15, DEC-040):
- keyed by (canonical_dataset, canonical_record_id): a second run creates nothing;
- provenance is preserved in SourceRecord for every imported record;
- nothing is marked VERIFIED, no CSCD definition text is stored, MOCK is refused;
- programme dates are never invented; topic tags are imported as suggestions;
- one ``seed.import`` audit event per dataset that created rows.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.vocab import MOCK
from app.modules.competency.models import Competency, CompetencyCluster, CompetencyFramework, CompetencyLevel
from app.modules.content.models import SourceRecord
from app.modules.governance.service import record_audit
from app.modules.organization.models import Organization
from app.modules.platform.models import Topic
from app.modules.recommendation.models import Course, CourseTopic
from app.seed.canonical import CanonicalBundle, SeedRefused, require_importable

CSCD_FRAMEWORK_VERSION_LABEL = "2014"  # from the dataset framework id "CSCD-2014" (DEC-040)
FORBIDDEN_AUTOMATED_STATUSES = {"VERIFIED", "UNAVAILABLE"}  # STATUS_VOCABULARY.md rule 2


@dataclass
class ImportReport:
    created: Counter = field(default_factory=Counter)
    skipped: Counter = field(default_factory=Counter)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {"created": dict(self.created), "skipped": dict(self.skipped), "warnings": list(self.warnings)}


def _refuse_mock(dataset: str, record_id: str, *statuses: str | None) -> None:
    if MOCK in statuses:
        raise SeedRefused(f"{dataset} record {record_id} is marked MOCK; mock data is never imported")


def _parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def _source_record(
    session: Session, org: Organization, dataset: str, record_id: str, dataset_sha: str, record: dict[str, Any]
) -> tuple[SourceRecord, bool]:
    existing = session.scalar(
        select(SourceRecord).where(
            SourceRecord.organization_id == org.id,
            SourceRecord.canonical_dataset == dataset,
            SourceRecord.canonical_record_id == record_id,
        )
    )
    if existing is not None:
        return existing, False
    provenance, licence, review = record["provenance"], record["licence"], record.get("review") or {}
    _refuse_mock(dataset, record_id, record.get("data_status"), licence.get("status"))
    source = SourceRecord(
        organization_id=org.id,
        registry_source_id=provenance["source_id"],
        source_document_id=provenance.get("source_document_id"),
        source_url=provenance["source_url"],
        source_organisation=provenance["source_organisation"],
        retrieval_date=_parse_date(provenance.get("retrieval_date")),
        access_method=provenance["access_method"],
        source_sha256=provenance.get("source_sha256"),
        raw_local_path=provenance.get("local_file_path"),
        canonical_dataset=dataset,
        canonical_record_id=record_id,
        canonical_dataset_sha256=dataset_sha,
        data_status=record["data_status"],
        licence_status=licence["status"],
        licence_notes=licence["usage_notes"],
        attribution_text=licence["attribution_text"],
        review_verified=bool(review.get("verified")),
    )
    session.add(source)
    session.flush()
    return source, True


def import_topics(session: Session, org: Organization, bundle: CanonicalBundle, report: ImportReport) -> dict[str, Topic]:
    dataset = bundle.datasets["topics"]
    existing = {t.code: t for t in session.scalars(select(Topic).where(Topic.organization_id == org.id))}
    for record in dataset["records"]:
        _refuse_mock("topics", record["id"], record["data_status"])
        if record["id"] in existing:
            report.skipped["topics"] += 1
            continue
        topic = Topic(
            organization_id=org.id,
            code=record["id"],
            label=record["label"],
            taxonomy_version=dataset["taxonomy_version"],
            data_status=record["data_status"],
            review_status="unreviewed",
        )
        session.add(topic)
        existing[topic.code] = topic
        report.created["topics"] += 1
    session.flush()
    return existing


def import_document_sources(session: Session, org: Organization, bundle: CanonicalBundle, report: ImportReport) -> None:
    """Phase 4C: every collected source document becomes a reference-only source record (plan K-6).

    Only provenance is stored - no document text. ``review_verified`` stays false until a person verifies the record,
    and nothing here makes content learner-visible.
    """
    dataset = bundle.datasets["documents"]
    for record in dataset["records"]:
        _, created = _source_record(session, org, "documents", record["id"], bundle.file_sha256["documents"], record)
        if created:
            report.created["source_records:documents"] += 1
        else:
            report.skipped["source_records:documents"] += 1


def import_cscd_framework(session: Session, org: Organization, bundle: CanonicalBundle, report: ImportReport) -> None:
    dataset = bundle.datasets["competency_framework"]
    meta = dataset["framework"]
    records = dataset["records"]
    if not records:
        raise SeedRefused("competency_framework dataset has no records")
    for record in records:
        # Licence guard (NR-11): definitions are never stored for the CSCD.
        if record.get("definition") is not None:
            raise SeedRefused(f"competency {record['id']} carries definition text; restricted content is not imported")
        _refuse_mock("competency_framework", record["id"], record["data_status"])

    framework = session.scalar(
        select(CompetencyFramework).where(
            CompetencyFramework.organization_id == org.id,
            CompetencyFramework.code == meta["id"],
            CompetencyFramework.version_label == CSCD_FRAMEWORK_VERSION_LABEL,
        )
    )
    if framework is None:
        # The framework-level provenance is shared by every record; the first record carries it.
        source, source_created = _source_record(
            session, org, "competency_framework", meta["id"], bundle.file_sha256["competency_framework"], records[0]
        )
        report.created["source_records:competency_framework"] += int(source_created)
        framework = CompetencyFramework(
            organization_id=org.id,
            name=meta["name"],
            code=meta["id"],
            framework_type="reference_behavioural",
            publisher=meta.get("publisher"),
            version_label=CSCD_FRAMEWORK_VERSION_LABEL,
            status="draft",
            definitions_restricted=True,
            source_record_id=source.id,
        )
        session.add(framework)
        session.flush()
        report.created["competency_frameworks"] += 1
    else:
        report.skipped["competency_frameworks"] += 1

    scale = meta["proficiency_scale"]
    levels = {lvl.level_number for lvl in session.scalars(
        select(CompetencyLevel).where(CompetencyLevel.framework_id == framework.id)
    )}
    for number, label in enumerate(scale, start=1):
        if number in levels:
            report.skipped["competency_levels"] += 1
            continue
        session.add(CompetencyLevel(
            organization_id=org.id, framework_id=framework.id, level_number=number, label=label,
            description=None, min_score=None, threshold_status="provisional",
        ))
        report.created["competency_levels"] += 1

    clusters = {c.code: c for c in session.scalars(
        select(CompetencyCluster).where(CompetencyCluster.framework_id == framework.id)
    )}
    cluster_by_dataset_id: dict[str, CompetencyCluster] = {}
    for meta_cluster in meta["clusters"]:
        cluster = clusters.get(meta_cluster["code"])
        if cluster is None:
            cluster = CompetencyCluster(
                organization_id=org.id, framework_id=framework.id, code=meta_cluster["code"],
                name=meta_cluster["name"], source_page=meta_cluster.get("source_page"),
            )
            session.add(cluster)
            report.created["competency_clusters"] += 1
        else:
            report.skipped["competency_clusters"] += 1
        cluster_by_dataset_id[meta_cluster["id"]] = cluster
    session.flush()

    competencies = {c.code for c in session.scalars(select(Competency).where(Competency.framework_id == framework.id))}
    for record in records:
        if not set(record["proficiency_levels"]) <= set(scale):
            raise SeedRefused(f"competency {record['id']} uses levels outside the framework scale")
        if record["proficiency_levels"] != scale:
            # Known extraction gap (DEC-044): stored nowhere, reported for human review.
            report.warnings.append(
                f"{record['id']}: source lists levels {record['proficiency_levels']} "
                f"(framework scale has {len(scale)}); status UNKNOWN, needs human check"
            )
        if record["code"] in competencies:
            report.skipped["competencies"] += 1
            continue
        cluster = cluster_by_dataset_id.get(record["cluster_id"])
        if cluster is None:
            raise SeedRefused(f"competency {record['id']} references unknown cluster {record['cluster_id']}")
        pages = record.get("source_pages") or {}
        session.add(Competency(
            organization_id=org.id, framework_id=framework.id, cluster_id=cluster.id,
            code=record["code"], name=record["name"], name_variants=list(record.get("name_variants") or []),
            description=None, definition_source_page=pages.get("definition"), detail_source_page=pages.get("detail"),
            status="active", data_status=record["data_status"],
        ))
        report.created["competencies"] += 1
    session.flush()


def import_programme_listings(
    session: Session, org: Organization, bundle: CanonicalBundle, topics: dict[str, Topic], report: ImportReport
) -> None:
    dataset = bundle.datasets["training_programmes"]
    for record in dataset["records"]:
        source, created = _source_record(
            session, org, "training_programmes", record["id"], bundle.file_sha256["training_programmes"], record
        )
        if not created:
            report.skipped["courses"] += 1
            continue
        delivery, schedule = record["delivery"], record["schedule"]
        batch = delivery.get("batch_size") or {}
        course = Course(
            organization_id=org.id,
            course_type="nssta_programme_listing",
            title=record["title"],
            description=None,
            provider_organisation=record["provider"],
            programme_family=record.get("programme_family"),
            cohort=record.get("cohort"),
            target_group=record.get("target_group"),
            duration_days=delivery.get("duration_days_per_occurrence"),
            batch_size_min=batch.get("min"),
            batch_size_max=batch.get("max"),
            venue=delivery.get("venue_as_printed"),
            fiscal_year=schedule.get("fiscal_year"),
            schedule_status=schedule.get("status_in_source"),
            external_ref=record["id"],
            external_url=None,
            source_record_id=source.id,
            data_status=record["data_status"],
            review_status="unreviewed",
            status="active",
        )
        session.add(course)
        session.flush()
        report.created["source_records:training_programmes"] += 1
        report.created["courses"] += 1
        for tag in record.get("topic_tags") or []:
            topic = topics.get(tag["topic_id"])
            if topic is None:
                raise SeedRefused(f"programme {record['id']} references unknown topic {tag['topic_id']}")
            session.add(CourseTopic(
                organization_id=org.id, course_id=course.id, topic_id=topic.id, method="keyword_rule", status="suggested",
            ))
            report.created["course_topics"] += 1
    session.flush()


def _assert_no_automated_verification(bundle: CanonicalBundle) -> None:
    for name in ("topics", "competency_framework", "training_programmes"):
        for record in bundle.datasets[name]["records"]:
            if record.get("data_status") in FORBIDDEN_AUTOMATED_STATUSES:
                raise SeedRefused(f"{name} record {record['id']} is {record['data_status']}; imports never carry human-only statuses")


def get_or_create_organization(session: Session, code: str, name: str) -> tuple[Organization, bool]:
    org = session.scalar(select(Organization).where(Organization.code == code))
    if org is not None:
        return org, False
    org = Organization(code=code, name=name, status="active")
    session.add(org)
    session.flush()
    return org, True


def import_canonical_datasets(session: Session, org: Organization, bundle: CanonicalBundle) -> ImportReport:
    """Import all seed datasets in the caller's transaction.

    Raises SeedRefused on any gate failure; the caller must roll back, so a refused import writes nothing.
    """
    require_importable(bundle)
    _assert_no_automated_verification(bundle)
    report = ImportReport()

    topics = import_topics(session, org, bundle, report)
    import_document_sources(session, org, bundle, report)
    import_cscd_framework(session, org, bundle, report)
    import_programme_listings(session, org, bundle, topics, report)

    per_dataset = {
        "topics": ("topics",),
        "documents": ("source_records:documents",),
        "competency_framework": (
            "source_records:competency_framework", "competency_frameworks", "competency_clusters",
            "competencies", "competency_levels",
        ),
        "training_programmes": ("source_records:training_programmes", "courses", "course_topics"),
    }
    for dataset, keys in per_dataset.items():
        created = {k: report.created[k] for k in keys if report.created[k]}
        if created:
            record_audit(
                session,
                organization_id=org.id,
                action="seed.import",
                target_type="canonical_dataset",
                target_id=dataset,
                after={"created": created, "dataset_sha256": bundle.file_sha256[dataset], "validator_verdict": bundle.verdict},
            )
    return report
