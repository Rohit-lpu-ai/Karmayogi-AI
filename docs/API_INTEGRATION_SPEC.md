# API and Integration Specification

| Field | Value |
|---|---|
| **Version** | 1.0.0-draft |
| **Status** | Proposed. **Implemented so far:** health endpoints, OpenAPI (local/ci), problem responses (§1.4.1) and the 17 vertical slice 1 endpoints listed in §2.12. All other endpoints are planned ([IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md)) |
| **Last updated** | 2026-09-14 |
| **Related** | [PRD.md](PRD.md) · [MVP_SCOPE.md](MVP_SCOPE.md) · [DATA_MODEL.md](DATA_MODEL.md) · [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) · [ERROR_HANDLING_SPEC.md](ERROR_HANDLING_SPEC.md) · [AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) · [../API_REQUIREMENTS.md](../API_REQUIREMENTS.md) (external source and iGOT requirements) · [../IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md) |

> **External API rule.** This document defines **no external API endpoint**. The iGOT, SSO and course-provider sections define only *our* adapter interfaces.
>
> No real iGOT endpoint is known or documented ([../IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md)). Mock results must never be represented as real external results.

## Table of contents

1. [Conventions](#1-conventions)
2. [Endpoint catalogue - MVP](#2-endpoint-catalogue---mvp)
3. [Reserved endpoint groups - P1/P2](#3-reserved-endpoint-groups---p1p2)
4. [Adapter architecture](#4-adapter-architecture)
5. [iGOT integration](#5-igot-integration)
6. [Future SSO / OAuth adapter](#6-future-sso--oauth-adapter)
7. [Future government data refresh adapter](#7-future-government-data-refresh-adapter)
8. [Future course provider adapters](#8-future-course-provider-adapters)
9. [Future notification provider adapters](#9-future-notification-provider-adapters)
10. [Entity to API coverage](#10-entity-to-api-coverage)

---

## 1. Conventions

### 1.1 Versioning

- **Prefix:** Base path `/api/v1`. Health endpoints `/healthz` and `/readyz` are unversioned.
- **Additive changes** (new optional fields, new endpoints) stay in v1.
- **Breaking changes** (removing or renaming fields, changing semantics) require `/api/v2`, or a deprecation period of at least one release with a `Deprecation` header and changelog entry.
- **Deprecation notice:** Response header `Deprecation: true` plus a `Sunset` date on deprecated endpoints.

### 1.2 Authentication

- **Browser clients:** Session cookie (HttpOnly, Secure, SameSite=Lax or Strict per DEC-007) issued by `POST /api/v1/auth/login`.
- **CSRF:** State-changing requests (POST/PUT/PATCH/DELETE) require an `X-CSRF-Token` header matching the session's CSRF token.
- **Machine clients:** Service-to-service tokens are not in MVP.
- **Unauthenticated routes:** `POST /auth/login`, `GET /healthz`, `GET /readyz`. Every other route requires a valid session.

### 1.3 Authorisation

- **Enforcement:** Server-side by a policy dependency on every route, evaluating access role, organisation scope, department scope and resource ownership ([SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §4).
- **Not found vs forbidden:** Resources outside the organisation return `404` (existence not revealed). Resources inside the organisation without permission return `403`.
- **Test coverage:** Every endpoint in §2 has an authorisation test per access role.

Role abbreviations used below:

| Code | Role | | Code | Role |
|---|---|---|---|---|
| L | `learner` | | CA | `competency_admin` |
| T | `trainer` | | TM | `training_manager` |
| DA | `department_admin` | | AU | `auditor` |
| OA | `org_admin` | | PA | `platform_admin` |

"self" means the caller's own records; "scoped" means within the caller's department or assignment scope.

### 1.4 Error format

Errors use `application/problem+json` (RFC 9457) with extension members:

```json
{
  "type": "https://errors.<platform-domain>/validation-failed",
  "title": "Validation failed",
  "status": 422,
  "detail": "One or more fields are invalid.",
  "instance": "/api/v1/learning-materials/7b1e.../documents",
  "code": "VALIDATION_FAILED",
  "correlation_id": "01J9Z...",
  "errors": [{"field": "file", "code": "FILE_SIGNATURE_MISMATCH", "message": "File content is not a PDF."}]
}
```

- **Error code catalogue and UI mapping:** [ERROR_HANDLING_SPEC.md](ERROR_HANDLING_SPEC.md).
- **Never included in errors:** stack traces, SQL, provider raw errors or secrets.

#### 1.4.1 Implemented error codes (interim catalogue, DEC-039)

Implemented in `backend/app/core/errors.py` and `backend/app/core/middleware.py`. The `type` member is `urn:platform:problem:<code-in-kebab-case>` until a public error-documentation URL exists (DEC-001). Validation errors omit the rejected input value.

| HTTP | `code` | When |
|---|---|---|
| 400 | `BAD_REQUEST` | Malformed request |
| 401 | `UNAUTHENTICATED` | No valid session (Phase 3) |
| 403 | `FORBIDDEN` | Authenticated but not permitted (Phase 3) |
| 404 | `NOT_FOUND` | Unknown route or resource outside scope |
| 405 | `METHOD_NOT_ALLOWED` | Method not supported on the route |
| 409 | `CONFLICT` | State or optimistic-lock conflict |
| 413 | `PAYLOAD_TOO_LARGE` | Body above limit |
| 415 | `UNSUPPORTED_MEDIA_TYPE` | Content type not accepted |
| 422 | `VALIDATION_FAILED` | Schema validation failed; `errors[]` has `field`, `code`, `message` |
| 429 | `RATE_LIMITED` | Rate limit reached (Phase 3) |
| 500 | `INTERNAL_ERROR` | Unexpected error; details only in logs, correlated by `correlation_id` |
| 503 | `SERVICE_UNAVAILABLE` | A required dependency is unavailable (for example `/readyz` without a database) |
| 401 | `INVALID_CREDENTIALS` | Sign-in failed (same response for unknown email, wrong password or inactive account) |
| 423 | `ACCOUNT_LOCKED` | Too many failed sign-ins; `Retry-After` header |
| 403 | `CSRF_FAILED` | State-changing request without a valid `X-CSRF-Token` |
| 409 | `NOTICE_VERSION_OUTDATED` | Acknowledgement for a notice version that is not current |
| 409 | `NOTICE_NOT_ACKNOWLEDGED` | Assessment started before acknowledging the privacy and AI-use notice |
| 409 | `JOB_ROLE_REQUIRED` | Action needs a selected job role |
| 409 | `JOB_ROLE_INACTIVE` | Selected job role is inactive |
| 409 | `ASSESSMENT_NOT_FOR_JOB_ROLE` | Baseline assessment belongs to another job role |
| 409 | `ASSESSMENT_ALREADY_COMPLETED` | Second attempt at a completed `pre` assessment (reassessment is P1) |
| 409 | `ASSESSMENT_HAS_NO_QUESTIONS` | Published assessment has no approved questions |
| 409 | `ATTEMPT_NOT_IN_PROGRESS` | Answer or submit on a submitted attempt |
| 409 | `ATTEMPT_NOT_SCORED` | Result requested before submission |
| 409 | `ATTEMPT_VOIDED` | The attempt was withdrawn by a local/ci demo reset (DEC-052); start the assessment again |
| 422 | `INVALID_OPTION` | Selected option does not belong to the question |

Every response, including errors, carries `X-Correlation-ID` and the security headers `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Content-Security-Policy: default-src 'none'; frame-ancestors 'none'` and `Cache-Control: no-store`.

### 1.5 Pagination

- **Style:** Cursor-based. Query parameters `limit` (default 25, max 100) and `cursor` (opaque).
- **Response shape:** `{"items": [...], "next_cursor": "..." | null}`.
- **Totals:** `total` is included only where it is cheap and not sensitive (admin tables).

### 1.6 Filtering

- **Syntax:** Explicit, allow-listed query parameters per endpoint (e.g. `status`, `topic_id`, `department_id`, `created_from`, `created_to`).
- **Unknown parameters** return `422` `UNKNOWN_FILTER`.
- **Search endpoints** use request bodies (`POST /search`) to allow structured filters without leaking query text into access logs.

### 1.7 Sorting

- **Syntax:** `sort` parameter with comma-separated allow-listed fields; prefix `-` for descending (e.g. `sort=-created_at,title`).
- **Default order** is documented per endpoint.

### 1.8 Validation

- **Contracts:** Request and response bodies are defined by Pydantic models with `extra="forbid"` for requests (prevents mass assignment).
- **Limits:** String length, array size and numeric range limits on all fields.
- **Error codes:** Validation errors return `422` with field-level `errors[]`.

### 1.9 Idempotency

- **When required:** The `Idempotency-Key` header (UUID or 16–64 char token) is **required** on:
  - `POST /learning-materials/{id}/documents`
  - `POST /question-generation-jobs`
  - `POST /attempts/{id}/submit`
  - `POST /reports`
  - `POST /me/learning-path/regenerate`
  - `POST /correction-requests`
- **Where it is optional:** All other POSTs.
- **Replay:** The same key and payload within 24 h returns the stored response. The same key with a different payload returns `409 IDEMPOTENCY_KEY_REUSED` ([DATA_MODEL.md](DATA_MODEL.md) IdempotencyKey).

### 1.10 Rate limiting

| Scope | Endpoints | Limit (initial, provisional) | Response |
|---|---|---|---|
| Per IP + account | `POST /auth/login` | Strict; lockout after N failures | `429` + `Retry-After` |
| Per user | `POST /document-qa`, `POST /search` | Configurable per minute/day | `429 RATE_LIMITED` + `Retry-After` |
| Per organisation | AI purposes | Daily token/cost quota | `429 AI_QUOTA_EXCEEDED` |
| Per user | Other endpoints | Generous default | `429` |

### 1.11 Correlation IDs

- **Accepted:** `X-Correlation-ID` if it matches `^[A-Za-z0-9-]{8,64}$`; otherwise a new ID is generated.
- **Returned:** In every response header and in every problem body.
- **Propagated to:** logs, audit records, AI interaction logs, job payloads and outbound adapter calls (as a header where the external system permits).

### 1.12 Audit metadata

- **Recorded fields:** State-changing endpoints marked **A** in §2 write `AuditLog` entries with `action`, `target_type`, `target_id`, `outcome`, redacted `before`/`after` and `correlation_id` ([SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §11).
- **Reason capture:** Actions that require a reason accept it in the request body as `reason`.

### 1.13 OpenAPI expectations

- **Generation:** FastAPI generates the OpenAPI 3.1 document, served at `/api/v1/openapi.json`. Authentication is required outside `local` (decision recorded in DEC-030).
- **Documentation requirements:** Every operation has an `operationId` (`<module>_<verb>_<resource>`), a module tag, summary, request and response schemas, documented error responses (401/403/404/409/422/429/503 as applicable) and examples.
- **Client generation:** The frontend TypeScript client is generated from the OpenAPI document in CI. Drift fails the build.
- **Contract testing:** OpenAPI changes are reviewed in pull requests alongside this document.

### 1.14 Background-job APIs

- **Starting a job:** Endpoints that start long work return `202 Accepted` with `{"job_id": "...", "status": "queued", "status_url": "/api/v1/jobs/{job_id}"}`.
- **Status:** `GET /api/v1/jobs/{id}` returns `{id, job_type, status, progress: {current, total} | null, result: {...} | null, error: {code, message} | null, created_at, updated_at}`.
- **Visibility:** Jobs are visible to the requester and to roles with scope over the job's target.
- **Updates:** Clients poll (TanStack Query) with backoff. Push updates are P1.

### 1.15 File-upload APIs

- **Encoding:** `multipart/form-data` with fields:
  - `file` (required);
  - `attestation_right_to_use` (bool, required true);
  - `attestation_no_personal_data` (bool, required true);
  - `language` (optional).
- **Accepted types (MVP):** PDF, DOCX, TXT (UTF-8). Maximum size is `MAX_UPLOAD_BYTES` (initial proposal 25 MB, aligned with the existing collector cap).
- **Response:** `202` with `document_id` and job, or `200` with `duplicate_of` when identical bytes already exist in the organisation.
- **Downloads:** Authorised per request. `Content-Disposition: attachment` for non-PDF. PDF served to the in-app viewer with `nosniff`.

---

## 2. Endpoint catalogue - MVP

Columns:
- **Roles:** who may call the endpoint.
- **PRD:** functional requirement ([PRD.md](PRD.md) §14).
- **Features:** catalogue IDs.
- **Entities:** primary [DATA_MODEL.md](DATA_MODEL.md) entities.
- **Flags:** **A** audited, **I** idempotency key required, **J** returns job.

### 2.1 Health (unversioned)

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/healthz` | Liveness (**implemented**, `platform_get_healthz`) | public | PRD-FR-026 | SEC-008 | — | |
| GET | `/readyz` | Readiness (**implemented** for the database, `platform_get_readyz`; Redis and storage checks added when those services exist) | public (no details) | PRD-FR-026 | SEC-008, AUT-014 | — | |

### 2.2 Auth

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| POST | `/api/v1/auth/login` | Create session | public | PRD-FR-001 | SEC-001, SEC-014 | User, Session | A |
| POST | `/api/v1/auth/logout` | End session | any | PRD-FR-001 | SEC-001, SEC-013 | Session | A |
| GET | `/api/v1/auth/session` | Current session info and CSRF token | any | PRD-FR-001 | SEC-003 | Session | |
| POST | `/api/v1/auth/password/change` | Change own password | any | PRD-FR-001 | SEC-001 | User | A |
| POST | `/api/v1/auth/reauthenticate` | Refresh authentication for sensitive actions | any | PRD-FR-001 | SEC-005 | Session | A |
| POST | `/api/v1/auth/sessions/revoke-all` | Log out all own sessions | any | PRD-FR-001 | SEC-013 | Session | A |

### 2.3 Me (self-service)

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/me` | Own profile, roles, organisation, onboarding state | any | PRD-FR-003 | UX-021, UX-003 | User, UserAccessRole | |
| PATCH | `/api/v1/me` | Update permitted profile fields | any | PRD-FR-003 | UX-021 | User | A |
| PUT | `/api/v1/me/job-role` | Select or change job role and department | L (any) | PRD-FR-004 | ROLE-001, UX-015 | User, JobRole | A |
| POST | `/api/v1/me/notice-acknowledgements` | Acknowledge privacy/AI-use notice | any | PRD-FR-003 | UX-015 | NoticeAcknowledgement | |
| GET | `/api/v1/me/dashboard` | Aggregated learner dashboard | L | PRD-FR-019 | PER-001, UX-009 | read models | |
| GET | `/api/v1/me/competency-profile` | Own estimates, bands, explanations | L | PRD-FR-007, PRD-FR-008 | CMP-001, CMP-002, CMP-006, CMP-007, AI-018 | UserCompetency, UserCompetencySnapshot | |
| GET | `/api/v1/me/competency-gaps` | Own gaps | L | PRD-FR-008 | AI-002, CMP-004, CMP-008 | UserCompetency, RoleCompetency | |
| GET | `/api/v1/me/attempts` | Own attempt history and timeline | L | PRD-FR-006, PRD-FR-024 | ASM-032, PRO-002, PRO-013 | AssessmentAttempt | |
| GET | `/api/v1/me/recommendations` | Own recommendations (with MOCK provenance if enabled) | L | PRD-FR-017 | AI-005, AI-006, PER-009, PER-010, PRO-012 | Recommendation | |
| GET | `/api/v1/me/learning-path` | Active learning path | L | PRD-FR-018 | AI-004 | LearningPath, LearningPathItem | |
| POST | `/api/v1/me/learning-path/regenerate` | Recompute path | L | PRD-FR-018 | AI-004 | LearningPath, BackgroundJob | I, J |
| GET | `/api/v1/me/progress` | Progress lists (`status` filter) | L | PRD-FR-024 | PRO-001, PRO-003, PRO-010, PRO-011 | ProgressRecord | |
| GET | `/api/v1/me/progress/history` | Learning history | L | PRD-FR-024 | PRO-005, PRO-006 | ProgressRecord, AssessmentAttempt | |

### 2.4 Organisation, users and job roles

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/organizations/current` | Organisation details | any | PRD-FR-002 | ADM-014 | Organization | |
| GET | `/api/v1/users` | List users (scoped) | OA, DA (scoped), PA | PRD-FR-002 | ADM-001 | User | |
| POST | `/api/v1/users` | Provision user | OA, DA (scoped), PA | PRD-FR-002 | ADM-001 | User | A |
| GET | `/api/v1/users/{id}` | User detail | OA, DA (scoped), PA; T/TM (scoped, limited fields) | PRD-FR-002 | ADM-001 | User | |
| PATCH | `/api/v1/users/{id}` | Update user or status | OA, DA (scoped), PA | PRD-FR-002 | ADM-001 | User | A |
| PUT | `/api/v1/users/{id}/access-roles` | Replace access role assignments | OA, PA (PA-only for `platform_admin`) | PRD-FR-002 | SEC-002, ADM-001 | UserAccessRole | A |
| GET | `/api/v1/departments` | List departments | any | PRD-FR-004 | ADM-002 | Department | |
| POST | `/api/v1/departments` | Create department | OA | PRD-FR-004 | ADM-002 | Department | A |
| PATCH | `/api/v1/departments/{id}` | Update/deactivate department | OA | PRD-FR-004 | ADM-002 | Department | A |
| GET | `/api/v1/job-roles` | List job roles | any | PRD-FR-004 | ROLE-001, ADM-003 | JobRole | |
| POST | `/api/v1/job-roles` | Create job role | OA, CA | PRD-FR-004 | ADM-003 | JobRole | A |
| GET | `/api/v1/job-roles/{id}` | Job role detail | any | PRD-FR-004 | ADM-003 | JobRole | |
| PATCH | `/api/v1/job-roles/{id}` | Update/deactivate job role | OA, CA | PRD-FR-004 | ADM-003 | JobRole | A |
| GET | `/api/v1/job-roles/{id}/competencies` | Approved (and, for admins, draft) mappings | any (approved only for L) | PRD-FR-005 | ROLE-002 | RoleCompetency | |
| PUT | `/api/v1/job-roles/{id}/competencies` | Replace draft mapping set / approve | CA | PRD-FR-005 | ROLE-002 | RoleCompetency | A |
| GET | `/api/v1/job-roles/{id}/assessments` | Linked assessment blueprints | CA, T, OA | PRD-FR-005 | ROLE-004 | Assessment | |

### 2.5 Competencies and competency records

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/competency-frameworks` | List frameworks | any | PRD-FR-005 | ADM-004 | CompetencyFramework | |
| POST | `/api/v1/competency-frameworks` | Create framework (draft) | CA | PRD-FR-005 | ADM-004 | CompetencyFramework, CompetencyCluster, CompetencyLevel | A |
| GET | `/api/v1/competency-frameworks/{id}` | Framework with clusters, levels, competencies, provenance | any | PRD-FR-005 | ADM-004 | CompetencyFramework, CompetencyCluster, CompetencyLevel, SourceRecord | |
| POST | `/api/v1/competency-frameworks/{id}/approve` | Approve framework version (incl. level thresholds) | CA (re-auth) | PRD-FR-005 | ADM-004, AI-012 | CompetencyFramework, CompetencyLevel | A |
| GET | `/api/v1/competencies` | List competencies (filters: framework, cluster, status) | any | PRD-FR-005 | ADM-004 | Competency | |
| POST | `/api/v1/competencies` | Create competency in draft framework | CA | PRD-FR-005 | ADM-004 | Competency | A |
| PATCH | `/api/v1/competencies/{id}` | Update competency (restricted-definition guard) | CA | PRD-FR-005 | ADM-004 | Competency | A |
| GET | `/api/v1/users/{id}/competency-profile` | Scoped profile | T, TM (scoped), DA (scoped), CA | PRD-FR-007 | CMP-001, AI-018 | UserCompetency | A (access to others' profiles) |
| GET | `/api/v1/users/{id}/competency-gaps` | Scoped gaps | T, TM (scoped), DA (scoped), CA | PRD-FR-008 | AI-002 | UserCompetency, RoleCompetency | A |
| GET | `/api/v1/users/{id}/competencies/{competency_id}/evidence` | Evidence ledger | self (via `me` id), T (scoped), CA, AU | PRD-FR-007 | AI-016, CMP-016 | CompetencyEvidence | A (non-self) |
| POST | `/api/v1/user-competencies/{id}/adjustments` | Human-reviewed level adjustment with reason | T (scoped), CA (re-auth) | PRD-FR-008 | CMP-019, RAI-017 | CompetencyEvidence, UserCompetencySnapshot | A |
| GET | `/api/v1/topics` | Taxonomy terms | any | PRD-FR-011 | UX-019, MAT-011 | Topic | |

### 2.6 Assessments, attempts and questions

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/assessments` | List assessments (learners: published and eligible only) | any | PRD-FR-006 | ADM-006 | Assessment | |
| POST | `/api/v1/assessments` | Create blueprint (topic, competency or role-based) | T, CA | PRD-FR-006 | ADM-006, ASM-007 to ASM-010 | Assessment, AssessmentQuestion | A |
| GET | `/api/v1/assessments/{id}` | Assessment detail (no keys) | any eligible | PRD-FR-006 | ADM-006 | Assessment | |
| PATCH | `/api/v1/assessments/{id}` | Edit draft / retire | T, CA | PRD-FR-006 | ADM-006 | Assessment | A |
| POST | `/api/v1/assessments/{id}/publish` | Publish (guards: approved versions, minimum items) | T, CA | PRD-FR-006 | ADM-006, ASM-009 | Assessment | A |
| POST | `/api/v1/assessments/{id}/attempts` | Start or resume attempt | L | PRD-FR-006 | AI-001, ASM-011, ASM-014 | AssessmentAttempt, AttemptQuestion | |
| GET | `/api/v1/attempts/{id}` | Attempt state and delivered questions (no keys) | self | PRD-FR-006 | ASM-001 | AssessmentAttempt, AttemptQuestion, QuestionVersion, QuestionOption | |
| PUT | `/api/v1/attempts/{id}/answers/{question_id}` | Save answer | self | PRD-FR-006 | ASM-001 | Answer | |
| POST | `/api/v1/attempts/{id}/submit` | Submit and score | self | PRD-FR-006 | ASM-017, AI-009, AUT-002 | AssessmentAttempt, Answer, CompetencyEvidence | A, I |
| GET | `/api/v1/attempts/{id}/result` | Result with feedback per policy, explanations, citations | self; T (scoped) | PRD-FR-006 | ASM-019, ASM-020, ASM-021 | AssessmentAttempt, Answer, Citation | |
| GET | `/api/v1/users/{id}/attempts` | Scoped attempt history | T, TM (scoped), CA | PRD-FR-006 | ASM-032 | AssessmentAttempt | A |
| GET | `/api/v1/questions` | Question bank (filters: status, competency, topic, origin) | T, CA | PRD-FR-006, PRD-FR-016 | ASM-001 | Question, QuestionVersion | |
| POST | `/api/v1/questions` | Manual question (requires citation) | T, CA | PRD-FR-006 | TRN-008 | Question, QuestionVersion, QuestionOption, Citation | A |
| GET | `/api/v1/questions/{id}` | Question with current version, options, citations | T, CA | PRD-FR-016 | ASM-001, ASM-021 | Question, QuestionVersion, QuestionOption, Citation | |
| PATCH | `/api/v1/questions/{id}` | Edit → new version → re-validation | T, CA | PRD-FR-016 | ASM-030, ASM-031 | QuestionVersion | A |
| GET | `/api/v1/questions/{id}/versions` | Version history | T, CA, AU | PRD-FR-016 | ASM-031 | QuestionVersion | |
| GET | `/api/v1/questions/{id}/validations` | Validator results | T, CA, AU | PRD-FR-015 | RAI-005, ASM-022 to ASM-024 | QuestionValidation | |
| POST | `/api/v1/question-generation-jobs` | Start MCQ generation | T, CA | PRD-FR-014 | AI-007, AUT-003 | BackgroundJob, AIInteractionLog | A, I, J |
| GET | `/api/v1/question-generation-jobs/{id}` | Job status, counts, created question IDs | T, CA (requester or scoped) | PRD-FR-014 | AI-007 | BackgroundJob | |

### 2.7 Review, corrections and governance

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/review-tasks` | Review queue (filters: type, status, assigned) | T, CA, TM; OA (read) | PRD-FR-016 | ASM-027, ADM-009 | ReviewTask | |
| GET | `/api/v1/review-tasks/{id}` | Task detail with target, source passage, validator flags | eligible reviewers | PRD-FR-016 | ASM-027 | ReviewTask, QuestionVersion, QuestionValidation, Citation | |
| POST | `/api/v1/review-tasks/{id}/decision` | Approve / reject / request changes / override | eligible reviewers | PRD-FR-016 | ASM-028, ASM-029, RAI-017 | Approval, Question | A |
| POST | `/api/v1/review-tasks/{id}/reassign` | Reassign task | T (own), CA, TM | PRD-FR-016 | ASM-027 | ReviewTask | A |
| POST | `/api/v1/correction-requests` | Submit correction request | L (self targets) | PRD-FR-023 | RAI-018 | CorrectionRequest, ReviewTask | A, I |
| GET | `/api/v1/correction-requests` | List (self, or scoped for reviewers) | L (self), T (scoped), CA, TM, AU | PRD-FR-023 | RAI-018 | CorrectionRequest | |
| PATCH | `/api/v1/correction-requests/{id}` | Decide (upheld/not upheld with reason) or withdraw (requester) | T (scoped), CA, TM; L (withdraw own) | PRD-FR-023 | RAI-018 | CorrectionRequest | A |
| GET | `/api/v1/audit-logs` | Search audit logs | AU, PA; OA (organisation, limited) | PRD-FR-022 | SEC-009, ADM-017 | AuditLog | A (access) |
| GET | `/api/v1/ai-interactions` | Search AI interaction logs (metadata) | AU, PA | PRD-FR-022 | SEC-011, ADM-017 | AIInteractionLog | A |
| GET | `/api/v1/ai-interactions/{id}` | Interaction detail incl. redacted text (per retention) | AU, PA | PRD-FR-022 | SEC-011 | AIInteractionLog, Citation | A |
| GET | `/api/v1/admin/prompt-templates` | Prompt registry with versions and evaluation status | PA, AU (read) | PRD-FR-023 | RAI-019, RAI-012 | PromptTemplate, PromptTemplateVersion, EvaluationRun | |
| POST | `/api/v1/admin/prompt-templates/{key}/versions` | Register draft version | PA (re-auth) | PRD-FR-023 | RAI-019, RAI-014 | PromptTemplateVersion | A |
| POST | `/api/v1/admin/prompt-templates/{key}/versions/{version}/activate` | Activate version (requires passing evaluation) | PA (re-auth) | PRD-FR-023 | RAI-019, RAI-012 | PromptTemplateVersion, EvaluationRun | A |

### 2.8 Learning materials, documents, search and Q&A

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/learning-materials` | Library listing (ACL-filtered; filters: organisation, type, topic, status) | any | PRD-FR-009, PRD-FR-011 | ADM-008, UX-019 | LearningMaterial, SourceRecord | |
| POST | `/api/v1/learning-materials` | Create material metadata | T, TM, CA, OA | PRD-FR-009 | MAT-001, ADM-008 | LearningMaterial | A |
| GET | `/api/v1/learning-materials/{id}` | Material detail, provenance, licence, topics, documents | any with access | PRD-FR-009 | ADM-008, MAT-011 | LearningMaterial, LearningMaterialTopic, Document, SourceRecord | |
| PATCH | `/api/v1/learning-materials/{id}` | Update metadata, licence flags, topics, access scope | T (own), TM, CA, OA | PRD-FR-009, PRD-FR-010 | ADM-008, MAT-011, MAT-028 | LearningMaterial, LearningMaterialTopic | A |
| DELETE | `/api/v1/learning-materials/{id}` | Soft deactivate | TM, OA | PRD-FR-009 | ADM-008 | LearningMaterial | A |
| POST | `/api/v1/learning-materials/{id}/documents` | Upload file (multipart) | T, TM, CA, OA | PRD-FR-009 | MAT-001, MAT-002, MAT-004, MAT-031 | Document, BackgroundJob | A, I, J |
| GET | `/api/v1/documents/{id}` | Document status and metadata | any with access | PRD-FR-010 | MAT-029 | Document | |
| GET | `/api/v1/documents/{id}/content` | Download or view file | any with access | PRD-FR-009 | MAT-028 | Document | A (restricted scope) |
| GET | `/api/v1/documents/{id}/pages/{page}` | Page text for viewer and citation navigation | any with access | PRD-FR-013 | MAT-020 | DocumentPage | |
| POST | `/api/v1/documents/{id}/reprocess` | Retry processing | T (own), TM, PA | PRD-FR-010 | MAT-030 | BackgroundJob | A, J |
| POST | `/api/v1/search` | Semantic or keyword search | any | PRD-FR-011 | MAT-014, MAT-015 | DocumentChunk, Embedding | |
| POST | `/api/v1/document-qa` | Grounded answer with citations or abstention | any (feature-flagged) | PRD-FR-012, PRD-FR-013 | MAT-017, MAT-018, MAT-019, RAI-001, RAI-003, RAI-015 | AIInteractionLog, Citation | |

**`POST /api/v1/document-qa` response (200):**

```json
{
  "interaction_id": "…",
  "abstained": false,
  "abstention_reason": null,
  "answer": [{"text": "…", "citation_ids": ["c1"]}],
  "citations": [{"id": "c1", "document_id": "…", "document_title": "…", "page_start": 12, "page_end": 12,
                  "quoted_span": "…", "source_organisation": "MoSPI", "source_url": "https://…",
                  "licence_status": "UNVERIFIED_SECONDHAND", "verified": true}],
  "confidence_band": "medium",
  "generated_by": {"model_id": "…", "prompt_version": "document_qa.v1"},
  "notice": "AI-generated from the cited documents. Check the sources."
}
```

### 2.9 Courses, recommendations, learning paths and progress

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/courses` | Catalogue (filters: `course_type`, `review_status`, `topic_id`, `competency_id`) | any (learners: approved and displayable only) | PRD-FR-017 | ADM-005 | Course, SourceRecord | |
| POST | `/api/v1/courses` | Create internal course | TM, OA | PRD-FR-017 | ADM-005 | Course | A |
| GET | `/api/v1/courses/{id}` | Course detail with provenance and mappings | any with access | PRD-FR-017 | ADM-005 | Course, CourseCompetency, CourseTopic | |
| PATCH | `/api/v1/courses/{id}` | Update, review status, deactivate | TM, OA | PRD-FR-017 | ADM-005 | Course | A |
| PUT | `/api/v1/courses/{id}/competencies` | Set and approve competency mappings | CA, TM | PRD-FR-017 | ADM-005, PER-010 | CourseCompetency | A |
| PUT | `/api/v1/courses/{id}/topics` | Review topic tags | TM, CA | PRD-FR-017 | ADM-005 | CourseTopic | A |
| POST | `/api/v1/recommendations/{id}/feedback` | Accept, start or dismiss with reason | L (self) | PRD-FR-017 | AI-005 | Recommendation | |
| PATCH | `/api/v1/learning-path-items/{id}` | Update item status (self-reported) | L (self); T/TM (administrator source, scoped) | PRD-FR-018, PRD-FR-024 | AI-004, PRO-001 | LearningPathItem, ProgressRecord | A (non-self) |
| POST | `/api/v1/learning-activities` | Record activity event | L (self) | PRD-FR-024 | PRO-001, PRO-005 | LearningActivity | |
| GET | `/api/v1/users/{id}/progress` | Scoped learner progress | T, TM, DA (scoped) | PRD-FR-020, PRD-FR-024 | ADM-012 | ProgressRecord, AssessmentAttempt | A |
| GET | `/api/v1/progress` | Scoped learner status list (`department_id`) - unranked | T, TM, DA (scoped) | PRD-FR-020 | ADM-012 | ProgressRecord, User | |
| GET | `/api/v1/trainer/dashboard` | Trainer queue and scoped summaries | T, TM | PRD-FR-020 | TRN-001 | read models | |

### 2.10 Reports

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| POST | `/api/v1/reports` | Generate report (`learner_development`, `competency_gaps`, `assessment`, `progress`) | L (self subject); T, TM, DA (scoped) | PRD-FR-025 | REP-001, REP-003, REP-004, REP-007, REP-014 | Report, BackgroundJob | A, I, J |
| GET | `/api/v1/reports/{id}` | Report status and HTML view | requester; scoped roles | PRD-FR-025 | REP-014 | Report | |
| GET | `/api/v1/reports/{id}/download` | Download (`format=csv`) | requester; scoped roles | PRD-FR-025 | REP-012, REP-015 | Report | A |

### 2.11 Integrations, jobs and settings

| Method | Path | Purpose | Roles | PRD | Features | Entities | Flags |
|---|---|---|---|---|---|---|---|
| GET | `/api/v1/integrations` | Integration list with mode and health | PA, OA, AU | PRD-FR-021 | IGOT-013 | IntegrationConnection | |
| GET | `/api/v1/integrations/igot/health` | iGOT adapter health (`mock` / `not_connected` / `degraded`) | PA, OA, AU | PRD-FR-021 | IGOT-013, IGOT-017 | IntegrationConnection | |
| GET | `/api/v1/integrations/igot/courses` | Mock catalogue passthrough (flagged; every item `provenance.data_status=MOCK`) | PA, TM (demo); L only via recommendations | PRD-FR-021 | IGOT-010, IGOT-011, IGOT-018 | — (not persisted) | |
| GET | `/api/v1/jobs/{id}` | Job status | requester; scoped roles | PRD-FR-027 | AUT-012 | BackgroundJob | |
| GET | `/api/v1/admin/jobs` | Job monitoring (filters: status, type) | PA | PRD-FR-027 | AUT-014, AUT-013 | BackgroundJob | |
| POST | `/api/v1/admin/jobs/{id}/retry` | Retry dead-letter job | PA | PRD-FR-027 | AUT-013 | BackgroundJob | A |
| GET | `/api/v1/admin/settings` | Organisation settings and feature flags | OA, PA | PRD-FR-020 | ADM-014, ADM-010 | Setting, FeatureFlag | |
| PATCH | `/api/v1/admin/settings` | Update settings/flags (evaluation-gated flags enforced) | OA (organisation keys), PA (platform keys); re-auth for security keys | PRD-FR-020 | ADM-014, ADM-010 | Setting, FeatureFlag | A |

### 2.12 Implemented in vertical slice 1

All require a session except login. State-changing routes require `X-CSRF-Token`. "Learning roles" = every access role except `auditor` and `platform_admin` (permission matrix). Simplifications: DEC-047.

| Method | Path | Roles | Status codes | Notes |
|---|---|---|---|---|
| POST | `/api/v1/auth/login` | public | 200, 401, 422, 423 | Body `{email, password, organization_code?}`; sets HttpOnly SameSite=Lax cookie; returns `csrf_token` and user |
| POST | `/api/v1/auth/logout` | any | 204, 401, 403 | Revokes server-side session |
| GET | `/api/v1/auth/session` | any | 200, 401 | CSRF token, expiries, user |
| GET | `/api/v1/me` | any | 200, 401 | Roles, `can_take_assessments`, job role, notice state (draft notice text), `is_synthetic` |
| POST | `/api/v1/me/notice-acknowledgements` | any | 200, 401, 403, 409, 422 | Body `{notice_version}` |
| PUT | `/api/v1/me/job-role` | any | 200, 401, 403, 404, 409, 422 | Body `{job_role_id}`; audited `user.job_role.change` |
| GET | `/api/v1/job-roles` | any | 200, 401 | Active roles in the caller's organisation; `is_demo` |
| GET | `/api/v1/job-roles/{id}/competencies` | any | 200, 401, 404, 422 | Approved mappings only, with framework level scale |
| GET | `/api/v1/assessments` | learning roles | 200, 401, 403 | Published `pre` assessments for the caller's job role |
| POST | `/api/v1/assessments/{id}/attempts` | learning roles | 201 (new), 200 (resumed), 401, 403, 404, 409 | Returns delivered questions without keys |
| GET | `/api/v1/attempts/{id}` | owner | 200, 401, 403, 404 | Other users' attempts return 404 |
| PUT | `/api/v1/attempts/{id}/answers/{question_version_id}` | owner | 200, 401, 403, 404, 409, 422 | Body `{selected_option_id | null}` |
| POST | `/api/v1/attempts/{id}/submit` | owner | 200, 401, 403, 404, 409 | Scores with `score-v1`, writes evidence and estimates, audited `attempt.submit` |
| GET | `/api/v1/attempts/{id}/result` | owner | 200, 401, 403, 404, 409 | Per-competency estimates; per-question feedback per policy |
| GET | `/api/v1/me/competency-profile` | learning roles | 200, 401, 403 | Estimates with explanation blocks |
| GET | `/api/v1/me/competency-gaps` | learning roles | 200, 401, 403, 409 | Status per approved requirement: `gap`, `meets_requirement`, `insufficient_evidence`, `level_unavailable`, `not_assessed` |
| GET | `/api/v1/me/recommendations` | learning roles | 200, 401, 403, 409 | `rec-v1` ranking with reasons and provenance; `igot.included=false` |

---

### 2.13 Implemented in product upgrade phase C (2026-09-15)

| Method | Path | Notes |
|---|---|---|
| GET | `/api/v1/me/attempts` | Own attempts newest first; voided demo attempts excluded. Learning roles |
| GET | `/api/v1/courses` | Learner-visible catalogue (`review_status='approved'`, `status='active'`). Query: `q` (title, description, objectives), `competency_id`, `difficulty`, `max_days` (1-365), `sort` (`recommended`, `title`, `duration_asc`, `duration_desc`). Returns `items`, `total`, `filters` (competency facets with course counts, difficulties, sorts) and `has_learning_context`. Each item carries `competencies`, `recommendation` (rank and reasons from `rec-v1`, learning roles only) and `addresses_your_gaps`. No pagination yet (catalogue below 50 items) |
| GET | `/api/v1/courses/{id}` | Detail with the same fields plus `your_status` per competency, `related_courses` and `learning_content` (`available: false` until the C7 proposal is approved). 404 for unapproved, inactive or other-organisation courses |

**Additive response fields (non-breaking):** competency references gain `description` (null for restricted frameworks); level items gain `description`; recommendation course references gain `difficulty` and `learning_objectives` (DEC-051).

### 2.14 Implemented in Phase 4A - accounts and administration (2026-09-15)

| Method | Path | Auth | Notes |
|---|---|---|---|
| GET | `/api/v1/environment` | Public | `{synthetic_data, self_registration_enabled}`; no configuration values |
| GET | `/api/v1/auth/registration-options` | Public | Query `organization_code` (optional when one organisation exists). `{enabled, organization_name, departments, job_roles}` |
| POST | `/api/v1/auth/register` | Public | 201 + session cookie + `SessionResponse`. 403 `REGISTRATION_DISABLED`, 409 `EMAIL_IN_USE` / `REGISTRATION_ID_IN_USE`, 422 validation. Learner role only (DEC-057) |
| POST | `/api/v1/auth/password/change` | Session + CSRF | `{current_password, new_password}`; 204; 422 `CURRENT_PASSWORD_INCORRECT`; other sessions revoked |
| POST | `/api/v1/auth/password/set` | Public (token) | `{token, new_password}`; 204; 400 `TOKEN_INVALID` for unknown, used or expired tokens; all sessions revoked; invited accounts become active |
| PATCH | `/api/v1/me` | Session + CSRF | `display_name`, `designation`, `department_id` only |
| GET | `/api/v1/departments` | Session | Active departments of the caller's organisation |
| GET | `/api/v1/admin/users` | `users.view` | Query `q`, `status`, `role`, `department_id`, `page`, `page_size` (max 100). `{items, total, page, page_size}`; department administrators see their department only |
| POST | `/api/v1/admin/users` | `users.manage` + CSRF | Creates an `invited` account with roles; returns `{user, setup: {purpose, token, expires_at}}` once |
| GET | `/api/v1/admin/users/{id}` | `users.view` | 404 outside organisation or department scope |
| PATCH | `/api/v1/admin/users/{id}` | `users.manage` + CSRF | Requires `row_version` (409 `STALE_VERSION`). `status` (`active`/`inactive`), details, `roles` (needs `roles.assign`); rules in DEC-057 |
| POST | `/api/v1/admin/users/{id}/password-link` | `users.manage` + CSRF | 201 `{purpose, token, expires_at}`; not for your own account or inactive accounts |
| GET | `/api/v1/admin/roles` | `users.view` | Every access role with label, description, capabilities, user count |
| GET | `/api/v1/admin/departments` | `users.view` | With user counts |
| POST / PATCH | `/api/v1/admin/departments`, `/{id}` | `departments.manage` + CSRF | Name unique per organisation (409 `DEPARTMENT_EXISTS`) |

**Additive `MeResponse` fields:** `registration_id`, `department`, `must_change_password`, `admin_capabilities`, `last_login_at`. Responses never include password or token hashes.

### 2.15 Implemented in Phase 4B - learning experience (2026-09-15)

All routes need a learning role (`SELF_LEARNING_ROLES`); writes need CSRF. Courses and lessons outside the caller's organisation, unapproved or inactive return 404.

| Method | Path | Notes |
|---|---|---|
| GET | `/api/v1/courses/{id}/outline` | `{course, modules[{lessons[{status}]}], progress, prerequisites}` |
| POST | `/api/v1/courses/{id}/start` | Idempotent; creates course progress `in_progress` with a resume lesson; 409 `NO_LESSONS` |
| GET | `/api/v1/lessons/{id}` | Body (Markdown subset), module, position of total, previous/next, caller status, `content_notice` for synthetic content |
| PUT | `/api/v1/me/lessons/{id}/progress` | `{status: in_progress | completed}`; returns lesson status, course progress and next lesson. Never downgrades a completed lesson; completing the last lesson completes the course |
| GET | `/api/v1/me/progress` | Courses in progress and completed, totals, note that completion does not change estimates |
| GET | `/api/v1/me/learning-path` | Active `path-v1` path, generated on first view or when inputs change. `state`: `ready`, `assessment_needed`, `no_gaps`; 409 `JOB_ROLE_REQUIRED` |
| POST | `/api/v1/me/learning-path/regenerate` | New active path; the previous one is `superseded`; completion carried over |

**Additive catalogue fields:** `GET /courses` items gain `content_origin`, `lessons {lesson_count, module_count, total_minutes}` and `your_progress` (learning roles), and accept `progress=not_started|in_progress|completed`. `GET /courses/{id}` gains `prerequisites`, `completion_criteria`, and `learning_content.available` now reflects real lessons.

### 2.16 Implemented in Phase 4C - content administration (2026-09-15)

All routes are under `/api/v1/admin`, organisation-scoped, capability-checked on the server, CSRF on writes. 404 for other organisations' items.

| Method | Path | Capability | Notes |
|---|---|---|---|
| GET | `/questions` | `questions.author` | Query `status`, `competency_id`, `origin`, `q`, `page`, `page_size`; `status_counts` |
| GET | `/questions/options` | `questions.author` | Competencies (with `restricted`), source records, difficulties |
| POST | `/questions` | `questions.author` | Creates a `draft` with version 1: `competency_id`, `difficulty`, `stem`, `explanation`, `options[{text,is_correct}]` (3-5, exactly one correct), `sources[]` |
| GET | `/questions/{id}` | `questions.author` or `questions.review` | Current version with options and correct answer, sources with status labels, versions, review history, `actions` |
| PUT | `/questions/{id}` | `questions.author` | New version; `row_version` required; only `draft`/`rejected` (409 `NOT_EDITABLE`) |
| POST | `/questions/{id}/submit` \| `/withdraw` \| `/retire` | `questions.author` | 422 `SOURCE_REQUIRED`; 409 `USED_IN_PUBLISHED_ASSESSMENT` |
| GET | `/reviews?status=open\|decided\|cancelled\|all` | `questions.review` or `courses.review` | Tasks the caller may review, with `can_decide`, `blocked_reason`, `row_version` |
| POST | `/reviews/{id}/decision` | task capability | `{decision, reason, row_version}`; 403 `SELF_REVIEW_BLOCKED`; 409 `TASK_CLOSED`/`STALE_VERSION`; 422 reason required |
| GET | `/courses?state=&origin=&q=` | `courses.manage` | All courses including drafts and imported listings; `state_counts` |
| GET | `/courses/options` | `courses.manage` | Competencies for linking |
| POST | `/courses` | `courses.manage` | Draft internal course (`content_origin` `synthetic` or `provider`) |
| GET | `/courses/{id}` | `courses.manage` or `courses.review` | Details, modules and lessons (with bodies), competency links, guard checklist, review history, `actions` |
| PATCH | `/courses/{id}` | `courses.manage` | `row_version`; 409 `IN_REVIEW`, `PUBLISHED`, `READ_ONLY_LISTING` |
| POST | `/courses/{id}/modules`, `/courses/{id}/modules/{mid}/lessons` | `courses.manage` | Add module; add lesson (Markdown body) |
| PATCH | `/courses/{id}/lessons/{lid}` | `courses.manage` | Title, type, minutes, body, `status` (hide) |
| PUT | `/courses/{id}/competencies` | `courses.manage` | `{competency_id, relevance}`; `relevance: null` removes; links start `suggested` |
| POST | `/courses/{id}/submit` \| `/withdraw` \| `/publish` \| `/unpublish` | `courses.manage` | 422 `SUBMIT_GUARDS_FAILED`/`PUBLISH_GUARDS_FAILED`; 409 `NOT_APPROVED`; unpublish needs `{reason}` |
| GET | `/competencies` | `frameworks.view` | Frameworks (descriptions withheld when restricted), approved-question counts, job-role requirements |
| GET | `/assessments` | `assessments.manage` | Coverage per competency and quality checks |
| GET | `/audit` | `audit.view` | Query `action` (prefix), `target_type`, `outcome`, `since`, `before_id`, `limit` (max 200); `next_before_id` cursor |

### 2.17 Implemented in Phase 4D - aggregated insight (2026-09-15)

Capability `insight.view` (org_admin, competency_admin, training_manager, department_admin scoped to their departments). A count object is `{value, suppressed}`; `value` is null when suppressed. Minimum group size 5.

| Method | Path | Notes |
|---|---|---|
| GET | `/api/v1/admin/insight/summary` | Learners, baseline completed, with confirmed gaps, started learning, completed a course; `scope` |
| GET | `/api/v1/admin/insight/skill-gaps?job_role_id=` | `competencies[]`, `rows[{department, learners, cells{competency_id: {required_for, assessed, with_gap, share, average_gap, suppressed}}}]`, `totals`, `job_roles` |
| GET | `/api/v1/admin/insight/training-needs` | Competencies with at least 5 learners sharing a gap, ranked: `learners_with_gap`, `average_gap`, `departments_affected`, `published_courses`, started/completed linked course counts, `content_gap`; `withheld_competencies` |

Question detail (`GET /api/v1/admin/questions/{id}`) additionally returns `quality_checks {method, findings[{code, severity, message}]}` from the local structural validator.

## 3. Reserved endpoint groups - P1/P2

**Not implemented in MVP.** No routes may be registered for these groups ([MVP_SCOPE.md](MVP_SCOPE.md) §5). Paths are indicative and are finalised at phase start.

| Group | Indicative paths | Features | Priority |
|---|---|---|---|
| Tutor | `/api/v1/tutor/conversations`, `/api/v1/tutor/conversations/{id}/messages` | TUT-001 to TUT-020 | P1 |
| Analytics | `/api/v1/analytics/competency-heatmap`, `/gaps`, `/departments/{id}`, `/departments/compare`, `/courses`, `/assessments`, `/engagement`, `/improvement`, `/training-effectiveness`, `/recommendations`, `/assessment-quality`, `/ai-quality`, `/fairness` | ANA-*, CMP-003, ADM-013, RAI-010 | P1/P2 |
| Adaptive and extended assessment | `/api/v1/attempts/{id}/next-question`, `/api/v1/answers/{id}/evaluations` | AI-008, AI-010, AI-011, ASM-018 | P1 |
| Personal learning extensions | `/api/v1/me/plans`, `/me/goals`, `/me/weak-topics`, `/me/topic-progress`, `/me/competency-history`, `/me/improvement`, `/me/bookmarks`, `/me/recent`, `/me/badges`, `/me/certificates`, `/me/deletion-requests` | PER-*, AI-014, CMP-010, CMP-012, CMP-013, UX-007, UX-008, GAM-*, SEC-019 | P1 |
| Role suggestions | `/api/v1/job-roles/suggestions` | AI-003 | P1 |
| Assignments | `/api/v1/assignments` | ADM-011, TRN-009 | P1 |
| Notifications | `/api/v1/notifications` | AUT-007, UX-005 | P1 |
| Content intelligence | `/api/v1/documents/{id}/summaries`, `/learning-materials/{id}/topic-suggestions`, `/learning-materials/{id}/versions`, `/courses/{id}/category-suggestions` | MAT-021, MAT-022, MAT-026, MAT-027 | P1 |
| iGOT sync (real access only) | `/api/v1/integrations/igot/sync-jobs` | IGOT-005, IGOT-016 | P1 (blocked) |
| Feedback and help | `/api/v1/feedback`, `/api/v1/help`, `/api/v1/search/global` | TRN-014, UX-016, UX-017, UX-004 | P1 |
| Trainer extensions | `/api/v1/trainer/learners/{id}/performance`, `/api/v1/trainer/support-signals` | TRN-010, TRN-011 | P1 |
| Taxonomy management | `POST/PATCH /api/v1/topics` | ADM-015 | P1 |

---

## 4. Adapter architecture

Every external dependency is accessed through an adapter with the same structure:

```mermaid
flowchart LR
  SVC[Module service] --> IF[Adapter interface]
  IF --> REG[Adapter registry<br/>selects implementation by config + feature flag]
  REG --> MOCK[Mock / fake implementation<br/>data_status MOCK]
  REG --> NC[Not-connected implementation<br/>explicit refusal]
  REG --> REAL[Real implementation<br/>only after verified access]
  IF --> HEALTH[health() -> mode, status]
  REAL --> EXT[(External system)]
  SVC --> PROV[Provenance stamping]
  SVC --> MAP[Error mapping -> problem codes]
  CT[Shared contract test suite] -.runs against.-> MOCK & REAL
```

**Common adapter requirements**

| # | Requirement |
|---|---|
| AD-1 | Interface defined in our code; implementations are swappable without changing callers |
| AD-2 | Explicit modes: `mock`, `not_connected`, `live` |
| AD-3 | `health()` returns mode, status and last error code; a mock never reports `ok`/`connected` |
| AD-4 | Error classes mapped to documented problem codes ([ERROR_HANDLING_SPEC.md](ERROR_HANDLING_SPEC.md)) |
| AD-5 | Timeouts, bounded retries with backoff and jitter, and rate-limit handling (real implementations) |
| AD-6 | Every returned record carries provenance: `source`, `adapter_mode`, `retrieved_at`, `data_status` |
| AD-7 | Credentials only from environment/secret store; never logged |
| AD-8 | Feature flag controlling visibility of the source |
| AD-9 | Shared contract test suite runs against every implementation |
| AD-10 | No outbound calls to hosts outside the adapter's configured allow-list |
| AD-11 | External data is written only in transactional batches with a sync log (P1) |

## 5. iGOT integration

### 5.1 Current state (repository facts)

| Item | Status | Evidence |
|---|---|---|
| Documented public or partner iGOT API | **Unknown - none found** | [../IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md) §1 |
| Real endpoints, base URL, credentials | **None known; none recorded** | `.env.example` has commented placeholders `IGOT_API_BASE_URL`, `IGOT_API_KEY` |
| Interface `IGotClient` | Implemented | `clients/igot_client.py`: `list_courses(limit, offset, provider, competency)`, `get_course(course_id)`, `get_user_enrollments(user_id)`, `get_user_completions(user_id)`, `get_learning_history(user_id)`; errors `NotFoundError`, `AuthorizationRequiredError`, `AccessNotVerifiedError`; factory `create_igot_client()` honours `IGOT_CLIENT_MODE` (`mock` default, `live` refused) |
| Mock implementation | Mocked | `clients/mock_igot_client.py` over `data/samples/mock/MOCK_igot_fixtures.json`; refuses non-MOCK fixtures; 14 tests pass |
| Real implementation | Blocked by external access | Preconditions in [../API_REQUIREMENTS.md](../API_REQUIREMENTS.md) §6.4 unmet |

### 5.2 Required iGOT integration elements

| # | Element | Specification | Status |
|---|---|---|---|
| 1 | **Interface** | `IGotClient` as above; Phase 10 moves it to `backend/app/modules/integrations/igot/` and adds `mode` and `health()` (DEC-021). The interface stays synchronous, called from a thread pool, unless an async version is justified | Implemented (move and extension planned) |
| 2 | **Mock implementation** | `MockIGotClient` unchanged in behaviour; every record `data_status=MOCK`; fixtures never imported into application tables | Mocked |
| 3 | **Contract tests** | Shared suite: pagination semantics, `NotFoundError` on unknown IDs, authorisation behaviour for user-scoped methods, record-type fields present, provenance present. Runs against the mock now and a real adapter later | Planned (current 14 tests are mock unit tests) |
| 4 | **Health status** | `health()` → `{mode: mock | not_connected | live, status: mock | not_connected | ok | degraded, last_checked_at, last_error_code}`; persisted in `IntegrationConnection`; exposed at `GET /api/v1/integrations/igot/health` | Planned |
| 5 | **Sync status** | `IntegrationSyncJob` records (reserved table); `GET /api/v1/integrations/igot/sync-jobs` reserved for P1. MVP responds with mode `mock` and no sync | Planned (P1, blocked) |
| 6 | **Error handling** | Mapping: `AccessNotVerifiedError` → `INTEGRATION_NOT_CONNECTED` (503 for integration routes; source hidden elsewhere); `AuthorizationRequiredError` → `INTEGRATION_UNAUTHORISED` (403); `NotFoundError` → `INTEGRATION_RESOURCE_NOT_FOUND` (404); unexpected → `INTEGRATION_UNAVAILABLE` (503) and `degraded` health | Partially implemented (error classes exist) |
| 7 | **Retry handling** | Real adapter only: per AD-5; documented limits honoured; no retries in mock | Planned (P1, blocked) |
| 8 | **Provenance tracking** | Every iGOT-derived payload includes `provenance: {source: "igot", adapter_mode, data_status, retrieved_at}`; recommendations persist it; UI shows MOCK badge when `data_status=MOCK` | Partially implemented (records carry `data_status`) |
| 9 | **Feature flag** | `igot_mock_source_visible` (organisation flag, default **off** outside `local`/`staging`); `IGOT_CLIENT_MODE` environment variable selects implementation | Partially implemented (`IGOT_CLIENT_MODE` exists) |
| 10 | **Explicit "not connected" state** | When no adapter is enabled, or mode is `live` without verified access: health `not_connected`, source hidden from learners, administrators see "iGOT: not connected - no authorised access" | Planned (factory already refuses `live`) |

**Prohibitions**
- Do not implement, guess or probe iGOT endpoints.
- Do not replay browser tokens or scrape the portal.
- Do not persist mock learner data as real.
- Do not show a mock adapter as `connected`.
- Do not present mock courses without the "MOCK - not real iGOT data" label.

## 6. Future SSO / OAuth adapter

P1 (SEC-004, IGOT-009). Interface only; no provider is configured.

```text
IdentityProviderAdapter
  mode: not_connected | live
  health() -> IntegrationHealth
  authorization_url(state, nonce, redirect_uri) -> URL
  exchange_code(code, redirect_uri) -> TokenSet            # server-side only
  fetch_identity(token_set) -> ExternalIdentity {subject, email, name, org_hint}
  map_to_user(identity) -> User | ProvisioningRequest      # never auto-grants privileged access roles
```

- **Protocol:** OIDC authorization code flow with PKCE; tokens held server-side only.
- **Provider candidates** (e.g. Parichay or other government SSO) are **not verified** and remain Decision required (Q-011).
- **Provisioning:** Just-in-time provisioning creates `learner` accounts only, subject to organisation policy.

## 7. Future government data refresh adapter

P1 (AUT-010). Wraps the **existing** controlled collector (`scripts/collectors/fetch_documents.py`) as a scheduled job.

```text
SourceCollectorAdapter
  run(manifest_id) -> CollectionRun {items: [{doc_id, status, sha256, changed: bool}]}
  health() -> IntegrationHealth
```

- **Hosts:** Only allow-listed hosts per manifest (currently `mospi.gov.in`, `www.mospi.gov.in`, `dopt.gov.in`). No crawling or link-following.
- **Change handling:** A changed checksum creates a new document version candidate and a `superseded_source_review` review task (P1). Raw files are never overwritten.
- **Provenance:** Sidecars and `SourceRecord` rows are updated with retrieval date and hash.

## 8. Future course provider adapters

P1/P2. Same shape as the catalogue subset of `IGotClient`:

```text
CourseProviderAdapter
  provider_key: str
  mode, health()
  list_courses(limit, offset, filters) -> CoursePage
  get_course(course_id) -> Course
```

Imported courses are stored as `Course` with `course_type` specific to the provider, `SourceRecord` provenance and `review_status='unreviewed'`. Mappings follow the same approval rules as internal courses.

## 9. Future notification provider adapters

P1 (AUT-007).

```text
NotificationChannelAdapter
  channel: in_app | email | sms
  mode, health()
  send(message: NotificationMessage) -> DeliveryResult {status, provider_message_id, error_code}
```

- **Content:** Messages contain no sensitive detail in subjects or previews (e.g. no scores).
- **Delivery:** Failures are retried by jobs; preferences and opt-outs are enforced before sending.
- **Provider selection** is Decision required.

---

## 10. Entity to API coverage

Every MVP entity in [DATA_MODEL.md](DATA_MODEL.md) is reachable through at least one endpoint group, or is internal by design.

| Entity | Exposed via | Notes |
|---|---|---|
| Organization | §2.4 `/organizations/current` | |
| Department | §2.4 `/departments` | |
| User | §2.3 `/me`, §2.4 `/users` | |
| UserAccessRole | §2.4 `/users/{id}/access-roles` | |
| Session | §2.2 auth | |
| NoticeAcknowledgement | §2.3 `/me/notice-acknowledgements` | |
| JobRole | §2.4 `/job-roles` | |
| CompetencyFramework, CompetencyCluster, CompetencyLevel | §2.5 `/competency-frameworks` | Clusters and levels nested |
| Competency | §2.5 `/competencies` | |
| RoleCompetency | §2.4 `/job-roles/{id}/competencies` | |
| UserCompetency, UserCompetencySnapshot | §2.3 `/me/competency-profile`, §2.5 `/users/{id}/competency-profile` | Snapshots in profile history (baseline) |
| CompetencyEvidence | §2.5 evidence and adjustments | |
| Topic | §2.5 `/topics` | |
| Question, QuestionVersion, QuestionOption | §2.6 `/questions` | Keys never in learner responses |
| QuestionValidation | §2.6 `/questions/{id}/validations` | |
| Assessment, AssessmentQuestion | §2.6 `/assessments` | Pool nested |
| AssessmentAttempt, AttemptQuestion, Answer | §2.6 `/attempts` | |
| SourceRecord | `provenance` objects in §2.5, §2.8, §2.9 | Not directly editable |
| LearningMaterial, LearningMaterialTopic | §2.8 `/learning-materials` | |
| Document, DocumentPage | §2.8 `/documents` | |
| DocumentChunk, Embedding | §2.8 `/search` (internal representation) | Not directly exposed |
| Citation | §2.6 results/questions, §2.8 document-qa, §2.7 ai-interactions | |
| Course, CourseCompetency, CourseTopic | §2.9 `/courses` | |
| Recommendation | §2.3 `/me/recommendations`, §2.9 feedback | |
| LearningPath, LearningPathItem | §2.3 `/me/learning-path`, §2.9 `/learning-path-items` | |
| LearningActivity | §2.9 `/learning-activities` | |
| ProgressRecord | §2.3 `/me/progress`, §2.9 `/progress`, `/users/{id}/progress` | |
| PromptTemplate, PromptTemplateVersion, EvaluationRun | §2.7 `/admin/prompt-templates` | Evaluation runs created by harness; listed in registry responses |
| AIInteractionLog | §2.7 `/ai-interactions` | |
| ReviewTask, Approval | §2.7 `/review-tasks` | |
| CorrectionRequest | §2.7 `/correction-requests` | |
| AuditLog | §2.7 `/audit-logs` | |
| BackgroundJob | §2.11 `/jobs`, `/admin/jobs` | |
| IdempotencyKey | `Idempotency-Key` header (§1.9) | Internal |
| Setting, FeatureFlag | §2.11 `/admin/settings` | |
| Report | §2.10 `/reports` | |
| IntegrationConnection | §2.11 `/integrations` | |
| IntegrationSyncJob, Notification, TutorConversation, TutorMessage, Badge, UserBadge, Certificate | §3 reserved groups | P1 |
