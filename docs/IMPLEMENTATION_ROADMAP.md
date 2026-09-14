# Implementation Roadmap

| Field | Value |
|---|---|
| **Version** | 1.0.0 |
| **Status** | Active. Phase 1 complete; Phase 2 complete for local development; vertical slice 1 (cutting across Phases 3, 4, 7, 8) implemented on DEMO content (see [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md), [VERTICAL_SLICE_1_PLAN.md](VERTICAL_SLICE_1_PLAN.md)) |
| **Last updated** | 2026-09-14 |
| **Related** | [PRD.md](PRD.md) · [MVP_SCOPE.md](MVP_SCOPE.md) · [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) · [DATA_MODEL.md](DATA_MODEL.md) · [AGENT_CONTEXT.md](AGENT_CONTEXT.md) · [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) · [DECISIONS.md](DECISIONS.md) |

This document was **missing** when implementation started, although PRD, MVP_SCOPE, DATA_MODEL and DECISIONS already cite it by phase number. It was generated on 2026-09-14 from those citations so the existing references stay correct (DEC-032).

## Table of contents

1. [Rules](#1-rules)
2. [Phase overview](#2-phase-overview)
3. [Mapping to the execution brief](#3-mapping-to-the-execution-brief)
4. [Phase details](#4-phase-details)
5. [Critical end-to-end journeys](#5-critical-end-to-end-journeys)
6. [Blocking decisions by phase](#6-blocking-decisions-by-phase)

---

## 1. Rules

1. **MVP boundary.** Phases 2–12 implement only P0 features ([MVP_SCOPE.md](MVP_SCOPE.md)). Phases 13–14 are P1/P2 and need explicit approval before any work starts.
2. **Exit criteria are gates.** A phase is complete only when every exit criterion holds and its tests pass. Partial completion is reported as partial in [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md).
3. **Every phase starts with a plan.** State the intended changes, affected files, database changes, API changes and risks before implementing.
4. **Every phase ends with documentation.** Update IMPLEMENTATION_STATUS.md, DATA_MODEL.md (schema), API_INTEGRATION_SPEC.md (endpoints), DECISIONS.md (new decisions or conflicts) and the threat model in SECURITY_RESPONSIBLE_AI.md §2.
5. **Conflicts stop work.** A conflict between documentation and the repository is recorded in DECISIONS.md before proceeding.
6. **Small increments.** Each phase is delivered as reviewable commits; no uncontrolled rewrites.

## 2. Phase overview

| Phase | Name | MVP capabilities | Status |
|---|---|---|---|
| 1 | Discovery and data collection | — (datasets, iGOT interface + mock) | **Complete** (commit `35d10a9`) |
| 2 | Backend foundation and reference schema | MVP-F1 (part), MVP-F2 (part), MVP-22 (logging) | Complete for local development |
| 3 | Authentication, RBAC and audit | MVP-01, MVP-02, MVP-03 (API), MVP-22 (events) | Partially implemented (vertical slice 1) |
| 4 | Competency engine and assessments | MVP-04, MVP-05, MVP-06, MVP-07, MVP-08 | Partially implemented (vertical slice 1, DEMO content) |
| 5 | Content pipeline and RAG | MVP-09, MVP-10, MVP-11, MVP-12, MVP-13, MVP-23 (controls) | Planned |
| 6 | Question generation, validation and review | MVP-14, MVP-15, MVP-16 (API), MVP-23 (controls) | Planned |
| 7 | Recommendations and learning paths | MVP-17, MVP-18, MVP-24 (API) | Partially implemented (vertical slice 1) |
| 8 | Learner web application | MVP-03 (UI), MVP-19, MVP-24 (UI), MVP-F3, MVP-F4 | Partially implemented (vertical slice 1) |
| 9 | Trainer and admin web application, reports | MVP-16 (UI), MVP-20, MVP-25 | Planned |
| 10 | Mock iGOT integration | MVP-21 | Planned |
| 11 | Governance and audit completeness | MVP-22 (UI, completeness), MVP-23 (governance) | Planned |
| 12 | Hardening, accessibility, demo readiness | MVP-F1, MVP-F4 (audit), MVP exit | Planned |
| 13 | P1 roadmap | PRD-FR-101 to 115 | **Not authorised** |
| 14 | P2 roadmap | PRD-FR-201 to 206 | **Not authorised** |

## 3. Mapping to the execution brief

The implementation brief of 2026-09-14 lists ten execution phases. They map onto this roadmap as follows. Work follows the brief's order, and progress is reported against both numbers.

| Brief phase | Brief scope | Roadmap phase |
|---|---|---|
| 1 | Backend foundation, configuration, logging, errors, health, PostgreSQL, Alembic, SQLAlchemy base | 2 (part A) |
| 2 | Organisations, departments, users, roles, competencies, levels, role requirements, course catalogue, seed data | 2 (part B: schema and seeds); CRUD APIs in 4 and 7 once authorisation exists |
| 3 | Authentication, sessions, RBAC, protected endpoints, audit events | 3 |
| 4 | Profile, role selection, assessment, attempts, scoring, gaps, evidence, explanations | 4 |
| 5 | Upload, validation, extraction, chunking, embeddings, pgvector, retrieval, grounded Q&A, citations, ACL | 5 |
| 6 | MCQ generation, validation, source evidence, duplicates, review, quiz attempts, feedback | 6 |
| 7 | Course-competency mapping, recommendations, role filtering, learning paths, progress | 7 |
| 8 | React shell, auth UI, learner, competency, assessment, gap, path, Q&A, trainer review, admin pages | 8 and 9 |
| 9 | Mock iGOT adapter, integration status, deep-link placeholders, sync logs, health endpoint | 10 |
| 10 | Testing, security hardening, accessibility, audit verification, docs, demo | 11 and 12 |

**Brief items that need care** (recorded in DECISIONS.md):
- *"Secure sessions or JWT architecture"* → server-side cookie sessions per DEC-007.
- *"Course deep-link placeholders"* → iGOT deep links are P1 and the URL pattern is unverified (IGOT-004). MVP shows a labelled "no verified link" placeholder only; no URL is constructed (DEC-036).
- *"Sync logs"* → `IntegrationSyncJob` is a P1 reserved table. MVP reports "no sync (mock mode)" and creates no sync records (DEC-036).
- *Assessment in brief phase 4 depends on approved questions*, which the brief places in phase 6. Phase 4 therefore includes manual question authoring and the core single-reviewer approval workflow; phase 6 adds AI generation, validators and the full policy (DEC-033).

## 4. Phase details

### Phase 1 - Discovery and data collection (complete)

- **Delivered:** 19 collected official documents (raw PDFs local-only), five canonical datasets in `data/processed/`, JSON Schema, validator (verdict `VALID_FOR_DEVELOPMENT_NOT_RELEASABLE`), `IGotClient` interface and `MockIGotClient`, 35 passing `unittest` tests.
- **Evidence:** commit `35d10a9`; `python -m unittest discover -s tests -t .`.

### Phase 2 - Backend foundation and reference schema

**Part A - foundation**
- `backend/` FastAPI modular monolith skeleton with app factory ([SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) §6).
- Typed settings (Pydantic Settings), startup validation, no secrets in code.
- Structured JSON logging with correlation IDs and redaction (DEC-028).
- RFC 9457 problem responses with error codes; no stack traces in responses.
- `GET /healthz`, `GET /readyz` (database check).
- SQLAlchemy 2.x engine and session management; declarative base with standard-column mixins (UUID PK, timestamps, `organization_id`, `row_version`).
- Alembic configured; initial migration.
- Dependency manifest (`backend/pyproject.toml` with pinned requirements); `scripts/` manifest (DEC-025).
- pytest suite; existing `unittest` tests keep running unchanged.

**Part B - reference schema and seeds**
- Tables: Organization, Department, User, UserAccessRole, JobRole, CompetencyFramework, CompetencyCluster, Competency, CompetencyLevel, RoleCompetency, Topic, SourceRecord, Course, CourseTopic, CourseCompetency, AuditLog.
- Seed command that runs the canonical dataset validator first, refuses an `INVALID` verdict, and imports idempotently: topics, CSCD structure (no definitions), NSSTA programme listings (unreviewed, dates null), one organisation and synthetic demo users (`local` only).

**Exit criteria**
- `alembic upgrade head` succeeds on an empty PostgreSQL database; `alembic downgrade base` succeeds.
- Models and migrations are in sync (autogenerate produces no diff).
- `/healthz` returns 200; `/readyz` returns 200 with a reachable database and 503 without one.
- Every error response is `application/problem+json` with a correlation ID.
- Seed import is idempotent (second run changes nothing), refuses an `INVALID` dataset, stores no CSCD definition text and no MOCK records.
- Database tests cover constraints (tenant uniqueness, CHECK enumerations, restricted definitions, `min_score` ordering).
- Existing 35 tests still pass.

### Phase 3 - Authentication, RBAC and audit

- Argon2id password hashing; login, logout, session, password change, re-authentication, revoke-all ([MVP_SCOPE.md](MVP_SCOPE.md) MVP-01).
- Session table with hashed tokens, idle and absolute timeouts, rotation; CSRF double-submit token.
- Login rate limiting and lockout (DEC-031 failure mode).
- Permission policy as code (`identity/policy.py`) implementing [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §4; default deny; route dependencies.
- Organisation-scoped repository layer (DEC-024).
- Users API, access-role assignment, last-org-admin guard.
- `GET/PATCH /me`, notice acknowledgement.
- AuditLog writes in the same transaction as the action (fail closed) for the §11 catalogue entries in scope.

**Exit criteria:** authorisation test matrix (endpoint × role, allowed and denied) passes; CSRF, lockout, timeout and revocation tests pass; audit emission and fail-closed tests pass; no credential appears in logs (redaction test).

### Phase 4 - Competency engine and assessments

- Departments and job roles CRUD with soft deactivation; `PUT /me/job-role`.
- Framework, competency, level and role-mapping APIs with draft/approved gating; restricted-definition guard.
- Question bank (manual authoring with mandatory citation), immutable versions, core review task with single-reviewer approval (DEC-033).
- Assessment blueprints and publishing guards; attempts with stored seed, resumable, key-free responses; server-side scoring.
- Append-only evidence ledger; deterministic `score-v1` estimation, evidence bands, explanations, snapshots and immutable baseline ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §25).
- Gap detection (band ≥ medium only); human adjustments with reason; correction request intake.

**Exit criteria:** key-leak tests on every attempt endpoint; seed reproducibility; determinism property tests (identical evidence → identical score); golden scoring fixtures; publishing guard tests; gap fixtures; wording lint on result copy. **Blocked for pilot** until DEC-013 (framework source) and DEC-020 (scoring parameters) are decided; a clearly labelled draft demo framework may be used in `local` only (DEC-034).

### Phase 5 - Content pipeline and RAG

- Storage interface (local filesystem backend), upload validation (type, signature, size, macro DOCX, zip limits), SHA-256 duplicate detection, attestation, malware-scan placeholder.
- Background job infrastructure: `BackgroundJob` table as source of truth, retries, dead-letter, idempotency keys (DEC-035).
- Extraction (pypdf, python-docx, UTF-8 text), cleaning, page-preserving chunking (`chunk-v1`), `needs_ocr` handling.
- `EmbeddingProvider` and `LLMProvider` interfaces with deterministic fakes; pgvector storage; keyword full-text search; ACL-first retrieval.
- Prompt registry (files → tables), grounded Q&A with citation verification, abstention, confidence bands, redaction, injection screening, `AIInteractionLog` before output.

**Exit criteria:** pipeline idempotency (reprocess never duplicates); scanned seeds end `needs_ocr`; ACL retrieval tests with multi-scope fixtures; citation span-match tests; abstention tests; injection and redaction suites pass with fake providers; invariant M-09 and M-12 tests. **Blocked for real providers** until DEC-005 and DEC-006.

### Phase 6 - Question generation, validation and review

- Generation jobs with licence gate (DEC-023), structured output, schema re-validation, full AI metadata.
- Validators: schema, structure, span match, exact duplicate, near duplicate, key check, support check.
- Review queue decisions: approve, reject with reason, edit → new version, override with reason, reassign, two-reviewer policy.
- Learner quiz attempts on approved questions reuse the Phase 4 attempt engine.

**Exit criteria:** crafted bad-question validator tests; no question with an unmatched span reaches review; review state-machine and policy tests; invariant M-11 test.

### Phase 7 - Recommendations and learning paths

- Course and material mapping review; deterministic `rec-v1` ranking with reason objects; dismissal and acceptance feedback.
- Learning path `path-v1` with placeholders for gaps without content; status updates; progress records and learning activities.

**Exit criteria:** ranking fixtures; unreviewed mappings have no influence; regeneration determinism and completed-item persistence; progress source labelling.

### Phase 8 - Learner web application

- React + TypeScript + Vite SPA (DEC-011), Tailwind, shadcn/ui, TanStack Query, React Router, i18n catalogue.
- App shell, login, onboarding, learner dashboard, competency profile, gap analysis, assessment and results, learning path, library and document viewer, Ask the documents, progress, settings.
- Shared empty, loading and error states mapped to problem codes.

**Exit criteria:** every screen wired to a real endpoint or explicitly marked placeholder; component tests; Playwright journeys J-01 to J-07; axe checks with zero serious or critical violations.

### Phase 9 - Trainer and admin web application, reports

- Trainer dashboard, quiz builder, quiz review, admin dashboard sections, settings admin sections, reports screen and report generation API with CSV escaping.

**Exit criteria:** journeys J-08 to J-11, J-14, J-16; report authorisation and CSV escaping tests.

### Phase 10 - Mock iGOT integration

- Move `clients/` iGOT interface and mock into `backend/app/modules/integrations/igot/` keeping behaviour and tests (DEC-021); add `mode` and `health()`.
- Adapter registry, feature flag `igot_mock_source_visible`, `IntegrationConnection`, integration health endpoints, provenance on every payload, MOCK labels.

**Exit criteria:** existing 14 mock tests migrated and passing; shared contract suite; mock never reports `connected`; `live` refused; invariant M-13 tests.

### Phase 11 - Governance and audit completeness

- Audit log and AI interaction search APIs and UI; correlation-ID trace; access to logs itself audited; correction-request workflow completion; prompt registry UI; evaluation harness and gate.

**Exit criteria:** audit catalogue coverage test; auditor read-only tests; evaluation gate prevents enabling AI flags without a passing run.

### Phase 12 - Hardening, accessibility and demo readiness

- Security headers and CSP, dependency and secret scanning, threat model review, manual keyboard and screen-reader checks of J-01 to J-07, performance smoke, demo seed and script.

**Exit criteria:** [PRD.md](PRD.md) §24 acceptance criteria and [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §16 checklist items achievable without pilot-only decisions.

### Phases 13-14 - P1 and P2

Not authorised. See [PRD.md](PRD.md) §17. No routes, screens or behaviour may be added during MVP.

## 5. Critical end-to-end journeys

| # | Journey step | First phase where testable end to end |
|---|---|---|
| 1 | User logs in | 3 (API), 8 (UI) |
| 2 | User selects a role | 4 (API), 8 (UI) |
| 3 | User completes an assessment | 4 (API), 8 (UI) |
| 4 | System calculates competency gaps | 4 |
| 5 | System recommends learning | 7 |
| 6 | User uploads a document | 5 |
| 7 | System processes the document | 5 |
| 8 | User asks a grounded question | 5 |
| 9 | System returns an answer with citations | 5 |
| 10 | Trainer reviews an AI-generated question | 6 (API), 9 (UI) |
| 11 | Trainer approves the question | 6 (API), 9 (UI) |
| 12 | Learner attempts the quiz | 6 |
| 13 | System records progress | 7 |
| 14 | User views improvement data | 8 (basic: baseline vs current per competency; before-vs-after comparison is P1) |

## 6. Blocking decisions by phase

| Phase | Decision | Effect if undecided |
|---|---|---|
| 2 | DEC-019 branch strategy; DEC-025 Python tooling | Work proceeds on branch `Diw` with pip-pinned requirements (provisional) |
| 2 | DEC-037 local database environment | Database tests cannot run until a PostgreSQL instance with credentials is available |
| 4 | DEC-013 framework source; DEC-020 scoring parameters | Draft demo framework in `local` only; values labelled provisional |
| 5 | DEC-005 LLM provider; DEC-006 embedding model and dimension | Fake providers only; embedding dimension fixed at migration time for the fake (DEC-038) |
| 5 | DEC-004 job system | PostgreSQL-backed job runner (DEC-035) until Redis is available and approved |
| 12 | DEC-009 hosting; DEC-027 lawful basis and retention | Pilot blocked |
