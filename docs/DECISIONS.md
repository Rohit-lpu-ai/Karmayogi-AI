# Decision Log

| Field | Value |
|---|---|
| **Version** | 1.0.0-draft |
| **Last updated** | 2026-09-14 |
| **Related** | [ASSUMPTIONS_AND_OPEN_QUESTIONS.md](ASSUMPTIONS_AND_OPEN_QUESTIONS.md) · [AGENT_CONTEXT.md](AGENT_CONTEXT.md) · [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) |

Architecture decision records in lightweight form.

**Status values**

| Status | Meaning |
|---|---|
| `Accepted` | Decided and in effect |
| `Proposed` | Recommended in this documentation package; becomes Accepted when the package is approved |
| `Decision required` | Blocks the listed phase; needs an owner's decision |
| `Superseded` | Replaced by a later decision |

**Rules**
- New decisions get the next free number. Numbers are never reused.
- A changed decision is marked `Superseded` with a pointer to its replacement.
- Conflicts between existing repository documents and new direction are recorded here instead of silently overwriting documents (§2).

## 1. Decision register

| ID | Title | Status | Blocks |
|---|---|---|---|
| DEC-001 | Product name | Decision required (interim working name: DEC-053) | Branding, UI copy |
| DEC-002 | Modular monolith architecture | Proposed | Phase 2 |
| DEC-003 | PostgreSQL with pgvector as the single data store | Proposed | Phase 2 |
| DEC-004 | Background job system: Celery + Redis | Proposed | Phase 2 |
| DEC-005 | LLM provider and data-processing terms | Decision required | Phases 5–6 (real provider use) |
| DEC-006 | Embedding provider, model and dimension | Decision required | Phase 5 |
| DEC-007 | Server-side cookie sessions instead of JWT for the web app | Proposed | Phase 3 |
| DEC-008 | Object storage: local filesystem in dev, S3-compatible in staging/pilot | Proposed | Phase 5 |
| DEC-009 | Hosting and deployment environment | Decision required | Phase 12 |
| DEC-010 | Document parsers: pypdf and python-docx; PyMuPDF not adopted | Proposed | Phase 5 |
| DEC-011 | Frontend build: React SPA with Vite | Proposed | Phase 8 |
| DEC-012 | Name the brief's "Role" entity `JobRole`; access roles separate | Proposed | Phase 2 |
| DEC-013 | Source of the functional competency framework and role mappings | Decision required | Phase 4 |
| DEC-014 | Mock iGOT in MVP only with labels and feature flag | Proposed | Phase 10 |
| DEC-015 | Relationship of existing root documents to the new package | Proposed | — |
| DEC-016 | Scope of rule R3 ("no personal data") versus application user data | Proposed (legal review required) | Phase 3 |
| DEC-017 | Two separate status vocabularies (data provenance vs implementation) | Proposed | — |
| DEC-018 | Feature catalogue generated from a structured registry | Accepted | — |
| DEC-019 | Branch strategy and merge of Phase 1 work | Decision required | Phase 2 |
| DEC-020 | Competency scoring parameters (weights, thresholds, evidence bands, evidence window) | Decision required | Phase 4 |
| DEC-021 | Move and extend the iGOT client interface | Proposed | Phase 10 |
| DEC-022 | Repository layout for backend and frontend | Proposed | Phase 2 |
| DEC-023 | Licence gate for AI generation and learner display | Proposed | Phases 5–6 |
| DEC-024 | Tenant isolation: repository-layer scoping now, row-level security before production | Proposed | Phase 12 |
| DEC-025 | Python version and environment tooling | Decision required | Phase 2 |
| DEC-026 | Accessibility target: WCAG 2.1 AA; GIGW applicability to be confirmed | Proposed | Phase 8 |
| DEC-027 | Lawful basis, privacy notice and retention periods | Decision required | Pilot |
| DEC-028 | Structured logging library | Proposed | Phase 2 |
| DEC-029 | Enumerations as text + CHECK constraints | Proposed | Phase 2 |
| DEC-030 | OpenAPI document access outside local | Proposed | Phase 2 |
| DEC-031 | Rate-limiter failure mode | Proposed | Phase 3 |
| DEC-032 | Generate the missing IMPLEMENTATION_ROADMAP.md and AGENT_CONTEXT.md | Accepted | — |
| DEC-033 | Question approval core moves into Phase 4 | Proposed | Phase 4 |
| DEC-034 | Draft demo competency framework for local development | Decision required | Phase 4 exit |
| DEC-035 | PostgreSQL-backed job runner until Redis is available | Proposed (conflicts with DEC-004) | Phase 5 |
| DEC-036 | iGOT deep-link placeholders and sync logs in MVP | Proposed | Phase 10 |
| DEC-037 | Local development database: Docker `pgvector/pgvector:pg17` | Proposed | Phase 2 |
| DEC-038 | No vector columns before Phase 5 | Proposed | Phase 5 |
| DEC-039 | Nine referenced documents are missing | Decision required | — |
| DEC-040 | Canonical dataset to database mapping | Proposed | Phase 2 |
| DEC-041 | Provisional Python tooling: 3.11, venv, pinned requirements | Proposed (resolves DEC-025 provisionally) | Phase 2 |
| DEC-042 | README "current phase" statement is outdated | Proposed | — |
| DEC-043 | MVP schema excludes `course_type='external_igot'` | Proposed | — |
| DEC-044 | CSCD competency 4.8 lists four proficiency levels | Decision required | Use of CSCD in role mappings |
| DEC-045 | Synthetic DEMO content seed for vertical slice 1 | Proposed (local/ci only; owner confirmation needed beyond local) | Pilot use of the slice |
| DEC-046 | Demo question origin and deferred AI/citation columns | Proposed | Phase 6 |
| DEC-047 | Vertical slice 1 simplifications | Proposed | Phases 3, 4, 7 completion |
| DEC-048 | Frontend stack for vertical slice 1 | Superseded in part by DEC-050 (styling) | Phase 8 |
| DEC-049 | Synthetic in-app course content (modules, lessons, learning player) | Accepted by product owner 2026-09-15 (local/ci DEMO content only) | Course experience |
| DEC-050 | UI foundation: Tailwind CSS + shadcn/ui, migrated screen by screen | Accepted by product owner 2026-09-15 | Design foundation |
| DEC-051 | Descriptive course difficulty and learning objectives (display and filtering only) | Accepted by product owner 2026-09-15 | Course catalogue |
| DEC-052 | Versioned DEMO seed packs and local demo reset by voiding | Accepted by product owner 2026-09-15 (local/ci only) | Richer demo content |
| DEC-053 | Interim product name "Competency Learning Platform" | Accepted by product owner 2026-09-15 (until DEC-001) | — |
| DEC-054 | DEMO pack `demo-2`: synthetic statistical-practice content | Proposed (local/ci only; under DEC-045/DEC-052) | Phase C demo quality |
| DEC-055 | Learner-facing display names and recommendation emphasis | Proposed | — |
| DEC-056 | Phase C scope conflicts awaiting the product owner (readiness score, learning evidence, lessons schema, demo-1 retirement, SIH mention) | Decision required | C7 and later |

---

## 2. Records

### DEC-001 Product name

- **Status:** Decision required.
- **Context:** The repository shows three names. The first commit is titled "AURA - Where AI Turns Intent Into Action" (21aaba5, 2026-08-26). The GitHub repository is `Rohit-lpu-ai/Karmayogi-AI`, with the README tagline "Empowering Every Karmayogi with AI". The local folder is `KaramYogiAI`.
- **Considerations:**
  - A name built on "Karmayogi" may imply official association with Mission Karmayogi or Karmayogi Bharat, which the project does not have ([IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md)).
  - UI must not imitate official branding ([UI_UX_SPEC.md](UI_UX_SPEC.md) §1).
- **Options:** "AURA"; "Karmayogi AI" (with a clear non-affiliation statement); another neutral name.
- **Until decided:** Documents use "the platform".

### DEC-002 Modular monolith architecture

- **Status:** Proposed.
- **Decision:** One FastAPI backend codebase deployed as `api` and `worker` processes. Modules communicate through service interfaces.
- **Rationale:** Small team; no evidence of independent scaling needs; one database; lower operational cost ([SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) §3).
- **Consequences:** Module boundary rules must be enforced by code review and import-lint checks. Extraction criteria are defined in [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) §21.

### DEC-003 PostgreSQL with pgvector as the single data store

- **Status:** Proposed (PostgreSQL is mandated by the brief).
- **Decision:** Relational data, full-text search and vectors all live in PostgreSQL with pgvector. Redis is not a system of record.
- **Rationale:** ACL filters and joins in one query; transactional integrity of evidence and audit; pilot scale is small.
- **Consequences:** The hosting provider must support the `vector`, `pgcrypto` and `citext` extensions. The migration path to a dedicated vector store is documented.

### DEC-004 Background job system: Celery + Redis

- **Status:** Proposed.
- **Alternatives:** RQ, Dramatiq, arq, PostgreSQL-backed queues (no Redis).
- **Rationale:** Mature retries, late acknowledgement, per-queue workers, scheduling later.
- **Consequences:** Redis becomes required. Job state is persisted in `BackgroundJob` so the queue can be switched. Revisit if Redis is undesirable in the chosen hosting.

### DEC-005 LLM provider and data-processing terms

- **Status:** Decision required.
- **Context:** No AI code exists. Government data sensitivity applies, and region and retention requirements are unverified.
- **Candidates:** Anthropic Claude API (candidate default models: `claude-opus-5` for generation and validation); Claude via a cloud platform; other commercial providers; self-hosted open-weight models ([TECH_STACK.md](TECH_STACK.md) §9).
- **Required before decision:**
  - verified retention and zero-data-retention terms for the chosen model;
  - processing region;
  - government-use terms;
  - legal approval;
  - evaluation on golden datasets.
- **Interim rule:** Fake providers everywhere. External providers only with public-source documents and synthetic data ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §38).

### DEC-006 Embedding provider, model and dimension

- **Status:** Decision required.
- **Context:** Vector dimension fixes the pgvector column type. Hindi support is needed from P1.
- **Process:** Evaluate candidate models on retrieval metrics over the collected corpus ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §31). Record the model ID, dimension and licence here.

### DEC-007 Server-side cookie sessions instead of JWT

- **Status:** Proposed.
- **Rationale:** Immediate revocation; no tokens in browser storage; same-site SPA.
- **Consequences:** CSRF protection is required. Machine-to-machine tokens are deferred.

### DEC-008 Object storage

- **Status:** Proposed.
- **Decision:** Storage interface with a local filesystem backend in dev and CI, and an S3-compatible backend in staging and pilot. The provider follows DEC-009.

### DEC-009 Hosting and deployment environment

- **Status:** Decision required.
- **Considerations:**
  - government hosting requirements for official data (e.g. approved or empanelled cloud providers), to be confirmed with stakeholders;
  - managed PostgreSQL with pgvector;
  - data residency;
  - cost;
  - team skills.

### DEC-010 Document parsers

- **Status:** Proposed.
- **Decision:** `pypdf` (already used successfully on 17 of 19 collected documents) for PDF; `python-docx` for DOCX; UTF-8 text for TXT.
- **Not adopted:** PyMuPDF, pending licence review (AGPL/commercial licensing).
- **Deferred to P1:** OCR (candidate: Tesseract).

### DEC-011 Frontend build: React SPA with Vite

- **Status:** Proposed.
- **Rationale:** SSR is not needed for an authenticated app with a FastAPI backend. Simple builds.
- **Alternative:** Next.js (rejected for MVP complexity).

### DEC-012 `JobRole` naming

- **Status:** Proposed.
- **Context:** The brief lists an entity named "Role" meaning job role, while RBAC also uses "roles".
- **Decision:** The entity and API use `JobRole` / `/job-roles`. RBAC uses "access roles" (`UserAccessRole`). UI copy says "Job role" and "Access role".

### DEC-013 Source of the functional competency framework and role mappings

- **Status:** Decision required.
- **Facts:**
  - The only collected framework is the DoPT CSCD. It is behavioural (4 clusters, 25 competencies), and definitions cannot be reproduced without DoPT permission.
  - No functional statistical competency framework or role-to-competency mapping was found.
  - The FRAC page is unreachable ([DATA_COLLECTION_RESULTS.md](DATA_COLLECTION_RESULTS.md)).
- **Options:**
  1. SMEs (e.g. NSSTA faculty) author a functional framework on the platform.
  2. Obtain an official framework from MoSPI/NSSTA or iGOT FRAC with permission.
  3. Pilot with a clearly labelled draft framework.
- **Consequence:** Phase 4 cannot exit without an approved framework or an explicit demo-mode decision.

### DEC-014 Mock iGOT in MVP

- **Status:** Proposed.
- **Decision:** The existing mock adapter is used behind a feature flag (default off outside local/staging).
- **Rules:** Mock data is never persisted as application data, always labelled "MOCK - not real iGOT data", and the integration health shows mode `mock`.

### DEC-015 Relationship of existing root documents to the new package

- **Status:** Proposed. Records conflicts rather than overwriting.

| Existing document | Conflict / overlap with brief | Resolution |
|---|---|---|
| `README.md` ("Current phase: data and API discovery. Not platform development.") | Brief moves the project to product documentation before implementation | README "current phase" line updated to point to this package; discovery content preserved |
| `API_REQUIREMENTS.md` (root; source discovery requirements and iGOT §6) | Overlaps with `docs/API_INTEGRATION_SPEC.md` | Root file remains authoritative for **external source and iGOT access requirements**; `docs/API_INTEGRATION_SPEC.md` is authoritative for **the platform's own API and adapters**; cross-linked |
| `DATA_DICTIONARY.md` (root; statistical observation schema, "proposed canonical schema for data/processed/") | Brief requires an application data model; the actual `data/processed/` datasets use `schemas/canonical_datasets.schema.json`, not the observation schema | `DATA_DICTIONARY.md` remains the schema for future statistical observation data (none collected); `schemas/canonical_datasets.schema.json` governs current processed datasets; `docs/DATA_MODEL.md` governs the application database. README description corrected |
| `DATA_COLLECTION_CHECKLIST.md` rule R1 ("do not scrape") and R3 ("no personal data") | Application must hold user accounts and competency data | See DEC-016; R1 unchanged (still applies to external collection) |
| `docs/LEARNING_PLATFORM_DATA_REQUIREMENTS.md` (LP-01–LP-21) | Brief adds PRD-level requirements | LP requirements remain the dataset-level contract enforced by the validator; PRD references them |
| `STATUS_VOCABULARY.md` | Brief introduces implementation statuses | See DEC-017 |

### DEC-016 Scope of rule R3 versus application user data

- **Status:** Proposed. **Legal review required.**
- **Context:** `DATA_COLLECTION_CHECKLIST.md` R3 and `DATA_DICTIONARY.md` §7 prohibit personal data in collected datasets and describe learner data as "a separate system with a separate assessment". The platform must process officials' account, assessment and competency data.
- **Decision:** R3 continues to govern **externally collected datasets** (`data/raw`, `data/interim`, `data/processed`). Application personal data is governed by [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §12, and requires the separate assessment and approvals in DEC-027 before any real user data is processed.

### DEC-017 Two status vocabularies

- **Status:** Proposed.
- **Decision:** Data and provenance facts use [STATUS_VOCABULARY.md](../STATUS_VOCABULARY.md) (`VERIFIED`, `MACHINE_OBSERVED`, `MOCK`, …). Feature implementation uses: Implemented, Partially implemented, Mocked, Planned, Unknown, Blocked by external access, Requires human confirmation ([DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)). The two are never mixed in one field.

### DEC-018 Feature catalogue generated from a structured registry

- **Status:** Accepted (used to produce this package).
- **Decision:** `docs/FEATURE_CATALOG.md` and `docs/feature_registry.json` are generated from `scripts/docs/registry_*.py` by `scripts/docs/generate_feature_catalog.py`. Consistency checks run via `scripts/docs/check_docs_consistency.py`.
- **Rationale:** 370 features × 19 fields must stay consistent with PRD, MVP scope and roadmap. A generator validates IDs and cross-references.
- **Note:** This is documentation tooling, not application code. Edit the registry, not the generated Markdown.

### DEC-019 Branch strategy and merge of Phase 1

- **Status:** Decision required.
- **Facts:** Phase 1 work (commit `35d10a9`, 117 files) is on branch `Diw` and not merged into `origin/main`, which has two README-only commits.
- **Proposal:**
  1. Open a pull request from `Diw` to `main` with review.
  2. Adopt short-lived feature branches plus pull requests.
  3. Protect `main` with required CI checks once CI exists.

### DEC-020 Competency scoring parameters

- **Status:** Decision required.
- **Proposal (method `score-v1`):**
  - difficulty weights 1.0 / 1.5 / 2.0;
  - evidence window: the most recent scored attempt containing the competency;
  - evidence bands at item counts 3 / 5 / 10;
  - level thresholds set per framework by a competency admin (provisional until approved).
- **Required:** SME and competency-admin approval. Values are labelled provisional in the UI until approved ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §25).

### DEC-021 Move and extend the iGOT client interface

- **Status:** Proposed.
- **Decision:** In Phase 10, move `clients/igot_client.py` and `clients/mock_igot_client.py` into `backend/app/modules/integrations/igot/`. Keep behaviour and tests. Add a `mode` property and a `health()` method. Keep the interface synchronous (called from a thread pool) unless async is justified. No real implementation.
- **Consequence:** Existing tests are migrated, not deleted (agent rule 14).

### DEC-022 Repository layout

- **Status:** Proposed.
- **Decision:** Add `backend/`, `frontend/` and `deploy/`. Keep existing `scripts/`, `data/`, `schemas/`, `registry/`, `tests/`, `clients/` (until DEC-021) and `docs/` ([SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) §6).

### DEC-023 Licence gate for AI generation and learner display

- **Status:** Proposed.
- **Decision:**
  - `LearningMaterial.generation_permitted` and `learner_display_permitted` default to false.
  - They may be set true only when licence status is `VERIFIED` by a human.
  - **Exception:** In `local` and `staging`, generation may run on public collected documents for development and evaluation only, with outputs never learner-visible in pilot.
  - CSCD material is always `generation_permitted=false`.

### DEC-024 Tenant isolation

- **Status:** Proposed.
- **Decision:** Mandatory `organization_id` scoping in the repository layer with tests (MVP). PostgreSQL row-level security added as defence in depth before production (Phase 12 evaluation).

### DEC-025 Python version and environment tooling

- **Status:** Decision required.
- **Facts:** Python 3.11.9 is used today. No dependency manifest exists.
- **Options:** Stay on 3.11 or move to 3.12; `uv` or `pip-tools` for locking.
- **Requirement:** Add manifests for `backend/` and for `scripts/` (pypdf, jsonschema) in Phase 2.

### DEC-026 Accessibility target

- **Status:** Proposed.
- **Decision:** WCAG 2.1 AA target for all P0 screens. Applicability of GIGW (Guidelines for Indian Government Websites) to be confirmed with stakeholders. No conformance is claimed until audited.

### DEC-027 Lawful basis, privacy notice and retention periods

- **Status:** Decision required. Legal review required.
- **Scope:**
  - lawful basis for processing officials' personal data (including under the Digital Personal Data Protection Act, 2023);
  - privacy and AI-use notice text;
  - retention periods per class ([DATA_MODEL.md](DATA_MODEL.md) §17);
  - incident notification obligations;
  - data protection impact assessment.
- **Blocks:** Any pilot with real users.

### DEC-028 Structured logging library

- **Status:** Proposed.
- **Decision:** structlog (or stdlib logging with a JSON formatter) with redaction processors and correlation ID context. Final choice in Phase 2.

### DEC-029 Enumerations as text + CHECK constraints

- **Status:** Proposed.
- **Rationale:** Native PostgreSQL enums complicate migrations; text + CHECK is easier to evolve.

### DEC-030 OpenAPI document access

- **Status:** Proposed.
- **Decision:** `/api/v1/openapi.json` is public in `local`, and requires authentication in `staging` and `pilot`.

### DEC-031 Rate-limiter failure mode

- **Status:** Proposed.
- **Decision:** If the rate-limit store is unavailable, fail closed for login and AI endpoints, and fail open with logging for read endpoints.

### DEC-032 Generate the missing IMPLEMENTATION_ROADMAP.md and AGENT_CONTEXT.md

- **Status:** Accepted (instruction of 2026-09-14: "If IMPLEMENTATION_ROADMAP.md or AGENT_CONTEXT.md is missing, stop and generate those documents first").
- **Conflict:** PRD, MVP_SCOPE, DATA_MODEL, TECH_STACK and this log cite both documents (roadmap Phases 2–14; "agent rule 1/14/19"; AGENT_CONTEXT §5), but neither existed.
- **Decision:** Both were generated to match the existing citations. The roadmap keeps the cited phase numbers and maps the ten execution phases of the implementation brief onto them ([IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) §3). Agent rule numbers 1, 14 and 19 keep the meanings other documents already assume.

### DEC-033 Question approval core moves into Phase 4

- **Status:** Proposed.
- **Conflict:** The brief places assessments in phase 4 and question review in phase 6. MVP-06 only allows approved question versions in assessments, so assessments cannot be tested end to end in phase 4 without some approval path.
- **Decision:** Phase 4 delivers manual question authoring (mandatory citation), immutable versions, `ReviewTask` and `Approval` with the single-reviewer policy. Phase 6 adds AI generation, automated validators, override, reassignment and the two-reviewer policy on the same tables.

### DEC-034 Draft demo competency framework for local development

- **Status:** Decision required (depends on DEC-013). **Update 2026-09-15:** the implementation brief for vertical slice 1 asked for explicitly labelled demo functionality; a local/ci-only demo seed was implemented under DEC-045. An official or SME-authored framework is still required for pilot.
- **Context:** No functional statistical competency framework or role mapping exists. The CSCD import is behavioural and structure-only.
- **Proposal:** For `local` only, a seed of a few functional competencies and one job role, every row named with a `DRAFT - DEMO` prefix, `status='draft'` until a competency admin approves it in the running app, `data_status='ASSUMED'`, `is_synthetic` demo users. It is never loaded in `staging` or `pilot`.
- **Needed from the owner:** approval of this demo route, or an SME-authored framework.

### DEC-035 PostgreSQL-backed job runner until Redis is available

- **Status:** Proposed. **Conflicts with DEC-004** (Celery + Redis).
- **Facts:** Redis is not installed on the development machine; `BackgroundJob` in PostgreSQL is already the source of truth for job state ([DATA_MODEL.md](DATA_MODEL.md) §10).
- **Proposal:** Implement the `jobs` interface with a worker that claims `BackgroundJob` rows using `SELECT … FOR UPDATE SKIP LOCKED`. Job handlers depend only on the interface, so Celery can replace the runner later without handler changes. Decide before Phase 5.

### DEC-036 iGOT deep-link placeholders and sync logs in MVP

- **Status:** Proposed.
- **Conflict:** The brief asks for "course deep-link placeholders" and "sync logs". Deep links are P1 with an unverified URL pattern (IGOT-004), and `IntegrationSyncJob` is a P1 reserved table.
- **Decision:** MVP shows a labelled "No verified iGOT link" placeholder and builds no URL. The integration health endpoint reports `sync: not_available_in_mock_mode`; no sync records are created.

### DEC-037 Local development database: Docker `pgvector/pgvector:pg17`

- **Status:** Proposed.
- **Facts (2026-09-14):** The host runs PostgreSQL 18 on port 5432 without the pgvector extension, and its credentials are not available to the agent. Docker Desktop is installed.
- **Decision:** `deploy/docker-compose.yml` runs `pgvector/pgvector:pg17` on host port **5433**, so it does not touch the existing host database. Credentials come from a git-ignored `.env`. PostgreSQL 17 satisfies the "16+" proposal in [TECH_STACK.md](TECH_STACK.md) §5.
- **Alternative:** install pgvector into the host PostgreSQL 18 and supply credentials.

### DEC-038 No vector columns before Phase 5

- **Status:** Proposed.
- **Context:** `vector(D)` needs a dimension, which depends on DEC-006.
- **Decision:** Phase 2 migrations create `pgcrypto` and `citext` only. The `vector` extension, `Embedding` table and `QuestionVersion.stem_embedding` arrive in Phase 5 migrations. The fake embedding provider's dimension is set then and recorded here; changing to a real model follows the expand/contract procedure in [DATA_MODEL.md](DATA_MODEL.md) §13.

### DEC-039 Nine referenced documents are missing

- **Status:** Decision required.
- **Facts:** `ERROR_HANDLING_SPEC.md`, `TESTING_STRATEGY.md`, `OBSERVABILITY_SPEC.md`, `DATA_PROVENANCE.md`, `DOCUMENTATION_INDEX.md`, `ASSUMPTIONS_AND_OPEN_QUESTIONS.md` and `DOCUMENTATION_VALIDATION_REPORT.md` are cited but absent. So is `scripts/docs/check_docs_consistency.py` (DEC-018). Roadmap and agent context were generated under DEC-032.
- **Interim rule:** Where implementation needs one of these (for example error codes), the code is the source and the codes are listed in [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) until the owner decides whether to author the missing documents.

### DEC-040 Canonical dataset to database mapping

- **Status:** Proposed.
- **Decision:** Field mapping as recorded in [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) §3. Key points:
  - canonical string IDs stay in `SourceRecord.canonical_record_id`; primary keys are database UUIDs;
  - competency `definition` maps to `description` and must be null;
  - `CompetencyFramework.version_label` for the CSCD import is `2014`, taken from the dataset's framework ID `CSCD-2014`;
  - programme fields without a model column (`programme_type_as_printed`, `topic_as_printed`, `occurrences_listed`, `total_days_listed`, `parse.confidence`) and the framework `publication_date` are not stored in MVP.
- **Open:** whether DATA_MODEL.md should add columns for the unstored fields.

### DEC-041 Provisional Python tooling

- **Status:** Proposed (provisional resolution of DEC-025).
- **Decision:** Python 3.11 (the installed version); a project virtual environment at `backend/.venv` (git-ignored); dependencies declared in `backend/pyproject.toml` and pinned in `backend/requirements.lock`. `uv` is not installed, so pip is used. Globally installed packages are not relied on.

### DEC-042 README "current phase" statement is outdated

- **Status:** Proposed.
- **Conflict:** `README.md` says "Current phase: data and API discovery. Not platform development" and describes directories as empty. DEC-015 planned to update this line. Phase 1 data now exists and implementation has started.
- **Decision:** Update the README status line and layout section at the end of Phase 2, keeping the discovery content.

### DEC-043 MVP schema excludes `course_type='external_igot'`

- **Status:** Proposed.
- **Conflict:** [DATA_MODEL.md](DATA_MODEL.md) `Course.course_type` lists `external_igot` (P1, "requires real adapter") and prohibits it in prose.
- **Decision:** The MVP CHECK constraint allows only `internal` and `nssta_programme_listing`, so the prohibition is enforced by the database rather than by service code alone. Adding `external_igot` in P1 is a one-line migration.

### DEC-044 CSCD competency 4.8 lists four proficiency levels

- **Status:** Decision required (human check of the source).
- **Facts:** `data/processed/competency_framework.json` lists Levels 1–4 for `CSCD-2014-4.8` (Problem Solving) and Levels 1–5 for the other 24 competencies. [DATA_COLLECTION_RESULTS.md](DATA_COLLECTION_RESULTS.md) §5 records that whether page 34 omits Level 5 is `UNKNOWN`.
- **Model gap:** `CompetencyLevel` is per framework; [DATA_MODEL.md](DATA_MODEL.md) has no per-competency level range, so a role mapping could require Level 5 for 4.8.
- **Interim decision:** The importer creates the five framework levels, stores nothing extra, and reports the discrepancy as a warning on every run. No role mapping uses the CSCD in MVP until it is approved.
- **Needed:** A human check of CSCD page 34. If the page really has four levels, decide whether to add `Competency.max_level_number` to DATA_MODEL.md.

### DEC-045 Synthetic DEMO content seed for vertical slice 1

- **Status:** Proposed. Local and ci only.
- **Context:** The slice (login → assessment → gaps → recommendations) needs an approved role mapping, approved questions and reviewed course mappings. None exist from any official source (DEC-013).
- **Decision:** `python -m app.seed … --demo-users --demo-content` creates, in one transaction and once per organisation:
  - one `draft` functional framework `DEMO-FUNCTIONAL` with four levels and provisional thresholds 0.0 / 0.4 / 0.6 / 0.8;
  - two competencies (`DEMO-C1`, `DEMO-C2`, `data_status='ASSUMED'`) and one job role `DEMO-ROLE-STAT-ASSISTANT` requiring Level 3 in each;
  - ten self-contained arithmetic items (five per competency) with mathematically certain keys, one published `pre` assessment;
  - three internal courses `DEMO-COURSE-1..3` with approved competency mappings (`method='demo_seed'`).
- **Labelling:** codes start with `DEMO-`, names with `DEMO`; every API object carries `is_demo`; the UI shows DEMO badges and a DEMO banner for synthetic users. Demo passwords come from `DEMO_USER_PASSWORD` in the git-ignored `.env`.
- **Honesty constraints:** approvals of mappings, questions, the assessment and courses are made by the seed on behalf of the synthetic competency admin. They are **not** human review, create no `ReviewTask`/`Approval` records, and are audited with that reason. Invariant M-11 is therefore not met for demo items. The seed is refused in staging, pilot and production.

### DEC-046 Demo question origin and deferred AI/citation columns

- **Status:** Proposed.
- **Decision:** `questions.origin` allows `demo_seed` in addition to `ai_generated` and `human_authored`, so seeded items never claim either. `question_versions` omits `ai_interaction_id`, `prompt_template_version_id`, `model_id`, `generation_parameters` and `stem_embedding`, and `questions` omits `generation_job_id`, because the referenced tables (AIInteractionLog, PromptTemplateVersion, BackgroundJob) and the vector dimension (DEC-006) do not exist yet. They are added by migration in Phases 5-6. No `citations` table exists yet (it depends on Phase 5 content tables), so demo items carry no citation.

### DEC-047 Vertical slice 1 simplifications

- **Status:** Proposed. Each item must be revisited when its roadmap phase is completed.

| # | Specification | Slice implementation |
|---|---|---|
| 1 | Estimates recomputed by a background job | Recomputed synchronously inside the submit transaction from the just-scored attempt |
| 2 | `Recommendation` rows persisted with feedback | Computed on read (`rec-v1`), deterministic, not stored; no dismiss/accept |
| 3 | `Idempotency-Key` required on submit | Not enforced; a repeated submit returns 409 `ATTEMPT_NOT_IN_PROGRESS` |
| 4 | Login by email | Email is unique per organisation; optional `organization_code`; without it, login succeeds only if exactly one active organisation has the email |
| 5 | CSRF double-submit token bound to session | Token = HMAC-SHA256(`SESSION_SECRET`, raw session token); no stored column |
| 6 | Audit failed logins | Only for known accounts (tenant-scoped audit table); unknown emails produce a redacted application log |
| 7 | Baseline snapshot rows | `assessment_attempts.is_baseline` set on the first scored `pre` attempt; `user_competency_snapshots` not created |
| 8 | Login rate limiting (SEC-014) | Account lockout only (5 failures, 15 minutes); IP rate limiting deferred (no store) |
| 9 | Reassessment | Refused (409 `ASSESSMENT_ALREADY_COMPLETED`); post-assessment is P1 |
| 10 | `PUT /attempts/{id}/answers/{question_id}` | Path parameter is the delivered `question_version_id` |
| 11 | `/me/dashboard` aggregate endpoint | Not created; the dashboard calls profile, gaps and recommendations separately |
| 12 | Evidence set = most recent scored attempt containing the competency | Equivalent in the slice (one attempt per user) |

### DEC-048 Frontend stack for vertical slice 1

- **Status:** Proposed.
- **Decision:** `frontend/` uses React 18, TypeScript 5, Vite 8, React Router 7, Vitest 5, Testing Library and jsdom. Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form and i18next (TECH_STACK.md §3) are **not** adopted yet, to keep the slice small; styling uses plain CSS custom properties that mirror UI_UX_SPEC.md §5 tokens. Initial React Router 6 and Vitest 3 selections had moderate advisories in `npm audit` and were replaced by the fixed majors (audit: 0 vulnerabilities). Revisit the full stack at Phase 8 start.

### DEC-049 Synthetic in-app course content (modules, lessons, learning player)

- **Status:** Accepted by the product owner on 2026-09-15. Local and ci DEMO content only.
- **Context:** No document specified in-app course content. Courses are catalogue entries (MVP-17, S-09), learning material is uploaded documents (MVP-09), and progress is self-reported items (MVP-24). The product upgrade brief asks for a course detail page, modules, lessons and a learning player so the journey does not stop at recommendations. This is new scope (conflict C-3 in `docs/evidence/implementation/product-upgrade-baseline.md`).
- **Decision:** Build course structure (modules, lessons), a learning player and lesson completion using synthetic DEMO content delivered by a versioned demo pack (DEC-052).
- **Constraints:**
  - every synthetic course, module and lesson is labelled DEMO/synthetic in the API (`is_demo`) and the UI; nothing is presented as approved, official or iGOT content;
  - content is kept separate from structure so lesson bodies can later be replaced by references to reviewed `LearningMaterial` records, approved government or iGOT content, or cited retrieval results without changing progress records;
  - progress follows the specified `ProgressRecord`/`LearningActivity` entities (MVP-24) rather than ad-hoc tables;
  - no streaks, gamification, certificates, reassessment, time-spent metrics or other P1/P2 features (MVP_SCOPE.md §5).
- **Consequences:** The schema migration is proposed in writing before implementation. MVP_SCOPE.md is not changed; this record is the approval.

### DEC-050 UI foundation: Tailwind CSS + shadcn/ui

- **Status:** Accepted by the product owner on 2026-09-15. Supersedes the styling part of DEC-048.
- **Decision:** Adopt Tailwind CSS (v4, Vite plugin) and shadcn/ui-style components copied into `frontend/src/components/ui/` on Radix primitives, as proposed in TECH_STACK.md §3 and UI_UX_SPEC.md §5 and §7. Design tokens are CSS variables with the roles in UI_UX_SPEC.md §5.
- **Migration rule:** one screen at a time; existing page tests stay green at every step; no full rewrite. Screens not yet migrated keep the legacy stylesheet.
- **Dependencies:** each package is listed with its purpose in TECH_STACK.md §3 (admission rules §18).

### DEC-051 Descriptive course difficulty and learning objectives

- **Status:** Accepted by the product owner on 2026-09-15.
- **Decision:** Courses gain a descriptive `difficulty` and `learning_objectives` for display and catalogue filtering.
- **Constraint:** `rec-v1` ranking does not read either field. Using difficulty in ranking ("difficulty logic", P1) requires a separate, documented and approved decision and a new rule version. A test asserts that ranking is unchanged by difficulty.

### DEC-052 Versioned DEMO seed packs and local demo reset

- **Status:** Accepted by the product owner on 2026-09-15. Local and ci only.
- **Context:** The DEC-045 seed is idempotent as a unit, so richer synthetic content could not reach existing databases (finding F-03). Each account can take the baseline once and there was no reset (F-02).
- **Decision (packs):** `backend/app/seed/demo_packs.py` registers ordered packs with a code and version. Table `seed_pack_applications` (migration `0004`) stores the applied version per organisation. `python -m app.seed ... --demo-content` applies missing or outdated packs; pack `apply` functions must be additive. A database that ran the pre-registry seed is adopted (`action: adopted`) without re-creating anything. Every application is audited (`seed.demo_pack.apply`).
- **Decision (reset):** `python -m app.seed.demo_reset --org-code ... (--email ... | --all-synthetic) [--clear-job-role]`, or `reset-demo.bat`. For synthetic users only: attempts become `voided` with `voided_at`/`void_reason`; evidence rows of those attempts are voided through their existing void-once columns; derived estimates (`user_competencies`) are removed; optionally the job role is cleared. Nothing is deleted from the attempt history or the evidence ledger. Notice acknowledgements stay (append-only). One audit record per user (`seed.demo_reset`).
- **Effects on the API:** voided attempts are ignored when listing, starting and baseline-flagging; reading, answering or submitting a voided attempt returns 409 `ATTEMPT_VOIDED`. The one-baseline index ignores voided attempts, so a reset learner receives a new baseline. The voided attempt keeps its original `is_baseline` value as history.
- **Not a product feature:** reassessment remains P1. The reset is refused outside local/ci and for non-synthetic accounts.

### DEC-053 Interim product name

- **Status:** Accepted by the product owner on 2026-09-15, until DEC-001 is decided.
- **Decision:** The UI uses the neutral working name "Competency Learning Platform", defined once in `frontend/src/config/product.ts` so it can be replaced in one place.
- **Constraints:** no official government, Mission Karmayogi, Karmayogi Bharat, MoSPI or NSSTA names as product branding, no emblems or logos, no claims of official endorsement (UI_UX_SPEC.md §1).

### DEC-054 DEMO pack `demo-2`

- **Status:** Proposed. Local and ci only, under DEC-045 (synthetic labelled content) and DEC-052 (versioned packs).
- **Decision:** `backend/app/seed/demo_pack_2.py` adds a `draft` framework `DEMO-STAT-PRACTICE` (4 provisional levels with plain-language descriptions), 8 competencies with descriptions, 3 job roles (4 competencies each), 40 scenario-style single-answer questions with invented figures (5 per competency, so evidence reaches "medium"), 3 published baseline assessments of 20 items, and 12 internal courses with difficulty, objectives and approved mappings. Codes start with `DEMO-`, names with `DEMO`, explanations end with a DEMO note. Seed "approvals" are not human review.
- **Not done:** the `demo-1` arithmetic role, assessment and courses remain active (see DEC-056 D-4).

### DEC-055 Learner-facing display names and recommendation emphasis

- **Status:** Proposed.
- **Decision:** Screens show names without the seed's `DEMO - ` prefix and `(synthetic …)` suffix (`cleanName`) only where a DEMO badge or the persistent DEMO notice labels the same content; stored names are unchanged. In the catalogue, courses with `rec-v1` rank 1-3 show "Top pick for you" and lower-ranked recommendations "Matches your gaps". Ranking itself is unchanged.
- **Reason:** Screenshot review showed repeated prefixes made every list hard to read, and with four gaps `rec-v1` recommends most of the catalogue, so a single "Recommended" badge carried no signal.

### DEC-056 Phase C conflicts awaiting the product owner

- **Status:** Decision required. Details in `docs/evidence/implementation/phase-c-plan.md` §2 and §4.
- **D-1** Single role-readiness score (ROLE-008 is P1) - not built; the dashboard shows "N of M at required level".
- **D-2** Learning activity or reassessment updating estimates (CMP-018, ASM-012 are P1) - not built; the journey marks those steps "later release".
- **D-3** Learning experience schema (DEC-049 requires a written proposal) - proposal written in `docs/evidence/implementation/phase-c-learning-experience-proposal.md`; no migration written.
- **D-4** Retire the `demo-1` arithmetic job role from the role picker.
- **D-5** Mention "Smart India Hackathon" in the UI (text only).
- **D-6** Manual screen-reader review needs a person (NVDA not installed; Narrator present but not operable from the agent).

### DEC-057 Accounts: learner self-registration, one-time password links, capability policy (Phase 4A)

- **Status:** Proposed. Implements Phase 4 plan assumptions A-1, K-8 and D4-2; D4-1 (registration outside local/ci) still needs the product owner.
- **Decision:**
  - Learners may register (`POST /api/v1/auth/register`) only when `LEARNER_SELF_REGISTRATION_ENABLED` resolves true: unset means on in `local`/`ci` and off elsewhere, and `true` is refused at startup outside `local`/`ci`. Registration creates an `active`, non-synthetic account with the `learner` role only; request bodies reject unknown fields, so roles cannot be mass-assigned. This supersedes MVP-01 "no self-registration" for local/ci only.
  - Administrators, trainers and auditors are always provisioned by an administrator. New accounts start `invited` with a one-time `account_setup` token; administrators never choose passwords. Reset issues a `password_reset` token. Tokens are 256-bit random, stored as SHA-256 only, expire after `PASSWORD_TOKEN_TTL_HOURS` (default 24), are single-use, and issuing a new one closes older ones. No email is sent: the link is shown once to the issuing administrator, and the token travels in the URL fragment so it never reaches server or proxy logs.
  - Setting a password with a token revokes all sessions; changing a password revokes the person's other sessions. Deactivation and access-role changes revoke all of the person's sessions.
  - `users.registration_id` (citext, optional, `^[A-Za-z0-9][A-Za-z0-9/-]{2,39}$`, unique per organisation) is personal data and redacted from logs.
  - Authorisation for administration is a capability matrix in `backend/app/modules/identity/policy.py` derived from SECURITY_RESPONSIBLE_AI.md section 4, checked by `require_capability` on every admin route. `department_admin` is limited to its department and to learner-only accounts; only `platform_admin` may grant or manage `platform_admin`; administrators cannot change their own roles or status. `GET /me` returns `admin_capabilities` for navigation only.
- **Alternatives rejected:** administrator-set temporary passwords (the administrator would know the secret); query-string tokens (logged by proxies).

### DEC-058 One environment-level synthetic-data banner

- **Status:** Proposed (Phase 4 plan K-2).
- **Decision:** The DEMO banner is shown when `GET /api/v1/environment` reports `synthetic_data` (app env local, ci or staging), for every visitor, instead of depending on whether the signed-in account is synthetic. Per-card DEMO badges are removed progressively (the top-bar job-role badge first); page-level notices stay where content is synthetic (catalogue, assessment). `is_demo` remains in every API payload.

### DEC-059 Learning experience, path rule `path-v1` and lesson rendering (Phase 4B)

- **Status:** Proposed. Implements the approved lessons proposal (DEC-049 follow-up) with the Phase 4 amendments; K-5 of the Phase 4 plan.
- **Decision:**
  - Migration 0007 adds `course_modules`, `lessons`, `course_prerequisites`, `progress_records` (with `course_id`, `started_at`, `resume_lesson_id`), append-only `learning_activities`, `learning_paths` and `learning_path_items`, plus `courses.content_origin` and `courses.completion_criteria`. The course lifecycle column set planned for 0007 moves to 4C with course administration, so learner visibility stays `review_status='approved' AND status='active'` for now.
  - Lesson completion is self-reported ("Mark as complete"), recorded with `status_source='self_reported'`, never downgraded by reopening, and never changes competency estimates or opens a reassessment (K-4 unchanged).
  - `path-v1` is a pure, documented rule separate from `rec-v1`: gaps largest first; within a gap the courses `rec-v1` matched, foundational to advanced, ties by `rec-v1` rank; advisory prerequisites placed just before the course; each course once; placeholders for gaps without content; completed courses from a superseded path kept at the end. The active path is regenerated when its input fingerprint changes or on request; completion facts live in `progress_records`, so nothing is lost.
  - Progress rows are created with `INSERT ... ON CONFLICT DO NOTHING` followed by a row lock, because opening and completing a lesson can race (found by the browser journey).
  - Lesson bodies use a small Markdown subset rendered to React elements by `frontend/src/components/product/Markdown.tsx` (no HTML parsing, no links or images). This replaces planned decision D4-7: no `react-markdown` dependency is added.
  - Pack `demo-3` adds synthetic lessons (2 modules, 4 lessons for each `demo-2` course, invented figures), completion criteria and four advisory prerequisites.
- **Not done:** A-6 (retiring the `demo-1` arithmetic role and courses) awaits the product owner (DEC-056 D-4); demo-1 courses have no lessons and show "No lessons yet".

### DEC-060 Content workflow: review policy, source metadata and publishing guards (Phase 4C)

- **Status:** Proposed. Implements Phase 4 plan K-6, K-7 and assumption A-5; the review policy needs product-owner confirmation (D4-5).
- **Decision:**
  - Review policy `single-reviewer-v1`: one recorded human decision (`approve`, `request_changes`, `reject`; a reason is required unless approving) closes a review task. The person who submitted the item, or wrote the question version under review, cannot decide it; attempts are refused and audited with outcome `denied`. Deciders need `questions.review` or `courses.review`. `approvals` are append-only. Nothing is approved automatically, and seed "approvals" remain labelled synthetic (DEC-045).
  - Questions authored in the platform follow `draft -> in_review -> approved | rejected`, with "request changes" returning them to `draft`. Every edit is a new immutable version; approval pins `approved_version_id`. A question cannot be sent for review without source metadata (`question_source_references`): a synthetic declaration (with a note), an imported source record, or an author-provided external reference, which is always shown as "author-provided, not verified" and never as a citation. Questions for licence-restricted frameworks cannot be authored. Approved questions used by a published assessment cannot be retired.
  - Courses: states derived from existing columns (`draft`, `in_review`, `approved`, `published`), so learner visibility stays `review_status='approved' AND status='active'`. Submitting needs a description, an active lesson and a competency link; publishing needs approval, an active lesson and an approved competency link (approved by the reviewer together with the course). Editing an approved course sends it back to draft; a published course must be unpublished (with a recorded reason) before editing. Imported programme listings are read-only here.
  - The 22 collected source documents are imported as reference-only `source_records` (provenance only, `review_verified=false`); no document text is stored.
  - Assessments: a read-only coverage and quality view (approved items, at least 5 items per required competency, source metadata). Assembling and versioning assessments from the UI is deferred.
- **Found during verification:** the running app did not import the full model registry, so the first question insert failed on a foreign key to `topics`; `app.main` now imports `app.models` (regression test added). Signing out could send the next person who signed in on the same browser to the previous user's page; sign-out now leaves protected pages before clearing the session.

### DEC-061 Aggregated insight with minimum group size, and a synthetic cohort (Phase 4D)

- **Status:** Proposed. P1 pull-forward under plan assumption A-3 (D4-3 needs the product owner).
- **Decision:**
  - `GET /api/v1/admin/insight/summary`, `/skill-gaps`, `/training-needs` (capability `insight.view`) return aggregates only. Any figure describing fewer than 5 learners is withheld (`suppressed`), including cells where fewer than 5 learners were assessed; training needs list only competencies where at least 5 learners share a gap. No names, emails, registration IDs or learner rows are returned. `department_admin` sees their own departments. Gaps use the same `score-v1` rule learners see (evidence at least medium).
  - Screens state that figures are development insight, not a performance measure, and not for appraisal or selection. There is no single readiness score.
  - Pack `demo-4` creates 38 synthetic learners in three synthetic departments (one deliberately below the group size) who go through the real pipeline (notice, job role, scored baseline, some lesson completion) with seeded answer patterns, so every figure is derived from recorded evidence. Cohort accounts have no passwords and are excluded from `demo_reset --all-synthetic`. `apply_demo_packs(..., CONTENT_PACKS)` lets tests skip the cohort.
- **Not done:** before/after comparison (reassessment remains P1, K-4).

### DEC-062 AI capability boundary stays local

- **Status:** Accepted for Phase 4 (brief: no external AI, no keys).
- **Decision:** Six interfaces (`CompetencyInterpreter`, `RecommendationExplainer`, `LearningContentRetriever`, `QuestionGenerator`, `QuestionValidator`, `LearningTutor`) with deterministic local implementations that report their `method`. Only the structural question validator is shown in the UI, labelled "fixed rules, not AI". The provider analysis is in `docs/evidence/implementation/phase-4-ai-boundary.md`; connecting any provider needs a new decision.
