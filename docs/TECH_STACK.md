# Technology Stack

| Field | Value |
|---|---|
| **Version** | 1.0.0-draft |
| **Status** | Proposed - no dependencies installed for the application |
| **Last updated** | 2026-09-14 |
| **Related** | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) · [AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) · [DECISIONS.md](DECISIONS.md) · [TESTING_STRATEGY.md](TESTING_STRATEGY.md) · [OBSERVABILITY_SPEC.md](OBSERVABILITY_SPEC.md) |

## Table of contents

1. [Rules for this document](#1-rules-for-this-document)
2. [What the repository uses today](#2-what-the-repository-uses-today)
3. [Frontend](#3-frontend)
4. [Backend](#4-backend)
5. [Database and vector search](#5-database-and-vector-search)
6. [Object storage](#6-object-storage)
7. [Queue and background jobs](#7-queue-and-background-jobs)
8. [Authentication](#8-authentication)
9. [AI providers](#9-ai-providers)
10. [Embedding providers](#10-embedding-providers)
11. [OCR](#11-ocr)
12. [Document parsers](#12-document-parsers)
13. [Testing tools](#13-testing-tools)
14. [Logging and monitoring](#14-logging-and-monitoring)
15. [CI/CD](#15-cicd)
16. [Deployment](#16-deployment)
17. [Environment and dependency management](#17-environment-and-dependency-management)
18. [Dependency admission rules](#18-dependency-admission-rules)

## 1. Rules for this document

- **Choices here are proposals** until approved and recorded in [DECISIONS.md](DECISIONS.md).
- **Versions are not pinned here.** Pin exact versions in manifests when Phase 2 starts, after checking the current stable releases and their licences.
- **Every dependency needs a stated purpose.** A dependency without one is rejected (§18).
- **Some items read "Decision required".** Those items block the phases listed against them.

## 2. What the repository uses today

| Technology | Evidence | Purpose |
|---|---|---|
| Python 3.11.9 | `python --version` | Data tooling and tests |
| `pypdf` 6.18.1 | Imported by `scripts/utils/extract_pdf_metadata.py`; installed per-user; **no manifest** | PDF text and metadata extraction |
| `jsonschema` 4.26.0 | Imported by `scripts/validators/validate_canonical_datasets.py`; **no manifest** | Canonical dataset validation |
| Python standard library (`unittest`, `urllib`, `csv`, `hashlib`, …) | All scripts and tests | Collection, processing, tests |
| Git + GitHub | Remote `https://github.com/Rohit-lpu-ai/Karmayogi-AI.git`; branches `main`, `Diw` | Version control |

**Update (Phase 2):** The backend now has `backend/pyproject.toml` and `backend/requirements.lock` in a project virtual environment (DEC-041). Pinned direct dependencies: `fastapi` 0.141.1, `uvicorn` 0.53.0, `pydantic` 2.13.5, `pydantic-settings` 2.15.0, `SQLAlchemy` 2.0.52, `alembic` 1.20.0, `psycopg[binary]` 3.3.5 (PostgreSQL driver), `jsonschema` 4.26.0 (seed gate reuses the canonical validator); tests: `pytest` 9.1.1, `httpx` 0.28.1. Logging uses the standard library (DEC-028). The local database is `pgvector/pgvector:pg17` in Docker (DEC-037). The `scripts/` tooling still has no manifest.

## 3. Frontend

| Technology | Why selected | Alternatives | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|---|
| **React** | Brief baseline; large ecosystem; accessible component libraries | Vue, Svelte, Angular | Needs discipline for state and data fetching | High | Low (industry standard) |
| **TypeScript** | Type safety across API contracts; fewer runtime errors | JavaScript | Build step, typing effort | High | Low |
| **Vite** (build tool, proposed) | Fast dev server; simple SPA builds; no SSR needed because FastAPI is the backend (DEC-011) | Next.js (SSR/RSC), Create React App (deprecated) | No server-side rendering; SEO irrelevant for an authenticated app | High | Low: moving to a meta-framework later is contained |
| **React Router** (proposed) | Standard client-side routing for SPA screens in [UI_UX_SPEC.md](UI_UX_SPEC.md) | TanStack Router | — | High | Low |
| **Tailwind CSS** | Brief baseline; consistent design tokens; small CSS output | CSS Modules, styled-components | Utility-class verbosity | High | Medium (class-heavy markup) |
| **shadcn/ui** | Brief baseline; copy-in components built on accessible Radix primitives; full control of markup | MUI, Chakra, Ant Design | Components owned by the project and maintained locally | High | Low (code is in-repo) |
| **TanStack Query (React Query)** | Brief baseline; server-state caching, retries, polling for job status | SWR, RTK Query | Another abstraction to learn | High | Low |
| **React Hook Form** + **Zod** (proposed) | Brief baseline for forms; Zod shares schemas with generated API types | Formik, Yup | Schema duplication unless generated from OpenAPI | High | Low |
| **Recharts** | Brief baseline; composable charts; tables provided separately for accessibility | Visx, Chart.js, ECharts | Accessibility of SVG charts needs manual work (ACC-015) | Medium-high | Low |
| **i18next / react-i18next** (proposed) | Externalised strings for ACC-003; Hindi in P1 | FormatJS (react-intl), Lingui | Runtime loading of catalogues | High | Low |
| **OpenAPI TypeScript client generation** (tool TBD, e.g. `openapi-typescript`) | Keeps frontend types in sync with FastAPI's OpenAPI | Hand-written types | Generation step in CI | High | Low |

## 4. Backend

| Technology | Why selected | Alternatives | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|---|
| **Python** (3.11 today; confirm 3.11 vs 3.12 in Phase 2, DEC-025) | Existing tooling is Python; strongest AI/document-processing ecosystem | Node.js, Go, Java | Lower raw throughput than Go/Java; mitigated by async I/O and workers | High | Low |
| **FastAPI** | Brief baseline; async; Pydantic integration; automatic OpenAPI | Django + DRF, Flask, Litestar | Fewer batteries than Django (admin, auth); those are built explicitly | High | Medium (framework-coupled routing) |
| **Pydantic v2** (+ Pydantic Settings) | Request/response validation (SEC-015/016); typed settings; AI structured-output validation | attrs + marshmallow | — | High | Low |
| **SQLAlchemy 2.x** | Brief baseline; mature ORM with explicit transactions; pgvector support via `pgvector` Python package | Django ORM, SQLModel, raw SQL | Verbosity | High | Low-medium |
| **Alembic** | Brief baseline; migrations for every schema change (agent rule 19) | Django migrations | Manual review of autogenerated migrations required | High | Low |
| **Uvicorn** (ASGI server; Gunicorn process manager in production, proposed) | Standard for FastAPI | Hypercorn | — | High | Low |
| **httpx** (proposed) | Async HTTP client for adapters with timeouts; test client | requests, aiohttp | — | High | Low |
| **argon2-cffi** (proposed) | Password hashing with Argon2id (SEC-001) | bcrypt | Memory-hard parameters need tuning | High | Low |
| **python-multipart** (proposed) | Multipart upload parsing required by FastAPI | — | — | High | Low |

## 5. Database and vector search

| Technology | Why selected | Alternatives | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|---|
| **PostgreSQL** (16+ proposed) | Mandated application database; relational integrity for evidence, versions and audit; full-text search for keyword mode (MAT-015) | MySQL, SQL Server | Operational expertise needed for tuning | High | Low |
| **pgvector** | Brief baseline; vectors next to relational data, so ACL filters and joins stay in one query; HNSW indexes | Qdrant, Weaviate, Milvus, OpenSearch | Scale ceiling lower than dedicated stores; index build memory; one embedding dimension per column | High for pilot scale | Medium: moving to a dedicated store needs dual-write and re-indexing ([SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) §17) |
| **PostgreSQL full-text search** (`tsvector`) | Keyword search without another service | OpenSearch/Elasticsearch | Weaker relevance tuning; Hindi configuration needs work (P1) | High | Low-medium |

## 6. Object storage

| Technology | Why selected | Alternatives | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|---|
| **Local filesystem** (dev/CI) | Zero setup | MinIO locally | Not representative of production permissions | High (dev only) | None: behind the storage interface |
| **S3-compatible object storage** (staging/pilot; provider per hosting decision DEC-009) | Standard API, encryption at rest, lifecycle policies | Database BLOBs, network file shares | Additional service | High | Low (storage interface) |
| **MinIO** (optional local S3 emulation) | Tests S3 code paths locally | LocalStack | Extra container; licence terms to check before use | Optional | Low |

Access goes through a `StorageBackend` interface (`put`, `get`, `delete`, `exists`), with opaque object keys and no public buckets.

## 7. Queue and background jobs

| Technology | Why selected | Alternatives | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|---|
| **Celery** with **Redis** broker (proposed, DEC-004) | Mature retries and backoff, late acknowledgement, per-queue workers (ingestion / ai / default), scheduled tasks later (P1) | RQ (simpler; fewer routing features), Dramatiq, arq (async), PostgreSQL-backed queues such as Procrastinate (no Redis) | Celery configuration complexity; Redis becomes a required service | Medium-high | Medium: job handlers written against a thin `jobs` interface to allow switching |
| **Redis** | Broker for Celery; rate-limit counters (SEC-014); short-lived caches | PostgreSQL for rate limits, Memcached | Another stateful service; not the system of record | High | Low |

The **source of truth for job state** is the `BackgroundJob` table in PostgreSQL, not Redis. If Redis loses queued messages, jobs can be re-enqueued from the database.

## 8. Authentication

| Technology | Why selected | Alternatives | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|---|
| **Server-side sessions** (session ID in HttpOnly/Secure/SameSite cookie; session store in PostgreSQL or Redis) (DEC-007) | Immediate revocation; no token handling in the browser; fits a same-site SPA | JWT access + refresh tokens | Needs CSRF protection and a session store | High | Low |
| **CSRF protection** (double-submit token) | Required with cookie sessions | SameSite-only | — | High | Low |
| **Authlib** (P1, proposed) | OIDC/OAuth client for future SSO (SEC-004, IGOT-009) | python-social-auth | — | Deferred | Low |
| **MFA** (TOTP, P1 decision) | Stronger admin authentication (SEC-005) | WebAuthn | Enrolment UX | Deferred | Low |

**Not selected for MVP:** third-party identity services. Government SSO options are Decision required (Q-011).

## 9. AI providers

All provider access is behind `LLMProvider` ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §1). **Provider selection is Decision required (DEC-005)**, and it depends on legal and data-residency approval for government data.

| Option | Why considered | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|
| **Fake deterministic provider** (in-repo) | Tests, CI and demos with no data egress | No real language capability | Required for all environments | None |
| **Anthropic Claude API** (candidate) | Strong reasoning for generation and validation. Documented structured outputs (`output_config.format`). Native citations for document content blocks, including page locations for PDFs. Current model IDs: `claude-opus-5` (default for generation and validation), `claude-sonnet-5`, `claude-haiku-4-5` (cheaper tiers only if evaluation shows quality holds) | External data processing; retention and region terms must be verified for government use; native citations cannot be combined with `output_config.format` in the same request (AI_SYSTEM_SPEC.md §16); cost | Candidate after DEC-005 | Low (behind interface) |
| **Claude via cloud platforms** (Amazon Bedrock, Google Vertex AI, Microsoft Foundry) (candidate) | May align with a chosen hosting provider's regions and contracts | Feature availability differs per platform and must be checked; separate pricing | Candidate | Low |
| **Other commercial LLM APIs** | Competitive options | Same data-processing concerns; different structured-output and citation features | Candidate | Low |
| **Self-hosted open-weight models** (on approved government or empanelled infrastructure) | Data stays within controlled infrastructure; potentially required for sensitive workloads | GPU infrastructure, operations effort, likely lower quality on complex validation; separate evaluation needed | Candidate for sensitive paths | Low (behind interface) |

**Verification required before selection:**
- data retention and zero-data-retention availability for the chosen model;
- processing region (India availability not verified);
- terms for government use;
- rate limits;
- feature parity on the chosen platform.

**Cost and quota controls are mandatory** whichever provider is chosen. No model-tier downgrade for cost is made without evaluation evidence (RAI-012).

## 10. Embedding providers

Access is behind `EmbeddingProvider`. **Selection is Decision required (DEC-006).** The model must handle English and, from P1, Hindi.

| Option | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|
| **Fake deterministic embedder** | Tests only | Required for CI | None |
| **Self-hosted open-source multilingual embedding model** (served through a small inference service or in-process) | No data egress; CPU/GPU cost; model quality and licence must be checked; dimension fixed per model | Candidate | Medium: changing models needs full re-embedding (supported by the `Embedding` table design) |
| **Hosted embedding API** (from the chosen AI vendor or another provider; availability and terms not verified here) | Simple operations; data egress; per-token cost | Candidate | Medium (re-embedding) |

Selection must be based on an evaluation of retrieval quality over the collected MoSPI/NSSTA corpus ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §31–33).

## 11. OCR

| Option | Why considered | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|
| **None in MVP** | Scope control; scanned files flagged `needs_ocr` | Two collected documents unreadable | Selected for MVP | — |
| **Tesseract** (P1 candidate) | Open source; runs locally; Hindi language data available | Accuracy on complex layouts; system binary dependency | P1 | Low |
| **Cloud OCR services** (P1 candidate) | Higher accuracy on tables and layouts | Data egress; cost; terms | P1 decision | Low |

## 12. Document parsers

| Technology | Why selected | Alternatives | Trade-offs | MVP suitability | Migration risk |
|---|---|---|---|---|---|
| **pypdf** (already used) | Pure Python; permissive licence (BSD); proven on the collected corpus (17 of 19 documents extracted) | pdfplumber, pdfminer.six, PyMuPDF | Weaker layout and table extraction | High | Low |
| **PyMuPDF** (not selected) | Better layout extraction | AGPL/commercial licensing obligations | Rejected for MVP pending licence review | — | — |
| **python-docx** (proposed) | DOCX text extraction (MAT-002) | docx2txt, LibreOffice conversion | No layout fidelity | High | Low |
| **python-pptx** (P1) | Slide text extraction (MAT-003) | LibreOffice conversion | — | Deferred | Low |
| **python-magic / libmagic** (proposed) | MIME detection by content (SEC-015) | `filetype` (pure Python) | System library dependency on some platforms | High | Low |

## 13. Testing tools

| Technology | Purpose | Alternatives | Notes |
|---|---|---|---|
| **unittest** (existing) | Existing 35 dataset and mock tests | — | Kept and run under pytest |
| **pytest** (proposed) | Backend unit, integration, contract, authorisation, AI-evaluation tests | unittest only | pytest runs existing unittest suites unchanged |
| **Hypothesis** (proposed) | Property-based tests for scoring determinism and parsers | — | — |
| **Testcontainers** or compose-based PostgreSQL (proposed) | Integration tests against real PostgreSQL + pgvector | SQLite (rejected: no pgvector, different SQL) | — |
| **Vitest** + **Testing Library** (proposed) | Frontend unit and component tests | Jest | — |
| **Playwright** (proposed) | End-to-end journeys and responsive checks | Cypress | — |
| **axe-core** (via Playwright) (proposed) | Automated accessibility checks (M-14) | Pa11y, Lighthouse | Manual testing still required |
| **Schemathesis** (optional) | OpenAPI-driven API fuzzing | — | Phase 12 |

## 14. Logging and monitoring

| Technology | Purpose | Alternatives | Trade-offs |
|---|---|---|---|
| **structlog** or stdlib `logging` with JSON formatter (DEC-028) | Structured, redacted logs with correlation IDs | loguru | — |
| **OpenTelemetry** (API, SDK, FastAPI/SQLAlchemy/Celery/httpx instrumentation) | Vendor-neutral traces and metrics | Vendor agents | Setup effort |
| **Prometheus** + **Grafana** (proposed defaults; or the hosting provider's managed equivalents) | Metrics, dashboards, alerts | Cloud-native monitoring | Operating the stack |
| **Sentry or equivalent error tracking** (optional, decision) | Exception aggregation | — | Data egress: personal data scrubbing required |

## 15. CI/CD

| Technology | Why selected | Alternatives | Notes |
|---|---|---|---|
| **GitHub Actions** (proposed) | Repository is hosted on GitHub (verified remote) | GitLab CI, Jenkins | Required checks listed in [TESTING_STRATEGY.md](TESTING_STRATEGY.md) §CI gates |
| **Secret scanning** (e.g. gitleaks) (proposed) | SEC-017 | GitHub secret scanning | — |
| **Dependency vulnerability scanning** (e.g. pip-audit, npm audit / Dependabot) | Supply-chain risk | — | — |
| **Linters/formatters** (Ruff for Python; ESLint + Prettier for TypeScript) (proposed) | Consistent code | Black + Flake8 | — |
| **Type checking** (mypy or pyright; `tsc`) (proposed) | Contract safety | — | — |

## 16. Deployment

| Item | Proposal | Status |
|---|---|---|
| Containers | Container images for `api`, `worker`, `frontend` (static build served by reverse proxy) | Proposed |
| Local orchestration | Docker Compose: postgres+pgvector, redis, api, worker, optional MinIO | Proposed |
| Hosting | Decision required (DEC-009). Consider government hosting requirements for official data (e.g. approved or empanelled cloud providers); to be confirmed with stakeholders | Decision required |
| Reverse proxy / TLS | Managed load balancer or Nginx/Caddy | Proposed |
| Database | Managed PostgreSQL with pgvector support, encryption at rest, automated backups | Proposed; provider must support pgvector |
| Infrastructure as code | Decision required (e.g. Terraform) | Deferred to Phase 12 |

No production infrastructure exists or is claimed.

## 17. Environment and dependency management

| Item | Proposal | Alternatives | Notes |
|---|---|---|---|
| Python project definition | `backend/pyproject.toml` with pinned lock file | `requirements.txt` + pip-tools | Also add a manifest for `scripts/` (pypdf, jsonschema) in Phase 2 to close the current gap |
| Python environment tool | **uv** or **pip-tools** (DEC-025) | Poetry | Decision required |
| Node package manager | **pnpm** (proposed) | npm, yarn | — |
| Settings | Pydantic Settings reading environment variables; `.env` for local only (git-ignored) | dynaconf | Startup validation |
| Environments | `local`, `ci`, `staging`, `pilot` ([SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) §7) | — | — |

## 18. Dependency admission rules

A new dependency may be added only when **all** of these hold:

1. Its purpose maps to a documented requirement or feature ID.
2. Its licence is compatible with the project (AGPL and other copyleft licences need an explicit decision).
3. It is actively maintained and has no known unpatched critical vulnerabilities.
4. It is pinned in a lock file.
5. It is recorded in this document (or in [DECISIONS.md](DECISIONS.md) if it changes architecture).
6. For AI or external services, it sits behind the relevant interface and passes contract tests.
