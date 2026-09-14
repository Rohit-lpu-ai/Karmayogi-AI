# MVP Scope

| Field | Value |
|---|---|
| **Version** | 1.0.0-draft |
| **Status** | Draft for approval |
| **Last updated** | 2026-09-14 |
| **Related** | [PRD.md](PRD.md) §14, §16 · [FEATURE_CATALOG.md](FEATURE_CATALOG.md) · [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) · [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) · [DATA_MODEL.md](DATA_MODEL.md) · [UI_UX_SPEC.md](UI_UX_SPEC.md) · [TESTING_STRATEGY.md](TESTING_STRATEGY.md) |

## Table of contents

- [1. Purpose and rules](#1-purpose-and-rules)
- [2. MVP at a glance](#2-mvp-at-a-glance)
- [3. MVP capabilities](#3-mvp-capabilities)
- [4. Foundation capabilities](#4-foundation-capabilities)
- [5. Features that must not be implemented during MVP](#5-features-that-must-not-be-implemented-during-mvp)
- [6. MVP data boundary](#6-mvp-data-boundary)
- [7. MVP exit criteria](#7-mvp-exit-criteria)

## 1. Purpose and rules

This document fixes the MVP boundary.

- **Scope is defined at capability level.** Each capability lists the catalog feature IDs it contains. Together, the capabilities cover every P0 entry in [FEATURE_CATALOG.md](FEATURE_CATALOG.md): 173 entries, of which 154 are canonical and 19 are aliases.
- **Only listed features may be built.** Anything not listed is **out of MVP**. A request to add scope needs an explicit product decision recorded in [DECISIONS.md](DECISIONS.md).
- **"Out-of-scope behaviour"** describes what the MVP deliberately does *not* do inside an in-scope capability.
- **API paths** are *planned internal* endpoints of this platform ([API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md)). Health endpoints and the vertical slice 1 endpoints exist; the rest are planned.
- **Implementation status today:** see [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md), which is the only maintained status record. Vertical slice 1 implements thin, partial versions of MVP-01, MVP-02, MVP-03, MVP-04, MVP-06, MVP-07, MVP-08, MVP-17 and MVP-19 on synthetic DEMO content; no capability is complete.

## 2. MVP at a glance

| ID | Capability | Roadmap phase | Primary users |
|---|---|---|---|
| MVP-01 | Authentication | 3 | All |
| MVP-02 | Role-based access control | 3 | All |
| MVP-03 | User profile | 3, 8 | All |
| MVP-04 | Department and role selection | 4 | Learner, Org admin |
| MVP-05 | Competency framework | 4 | Competency framework admin |
| MVP-06 | Initial competency assessment | 4 | Learner, Trainer |
| MVP-07 | Competency score calculation | 4 | Learner |
| MVP-08 | Competency-gap detection | 4 | Learner, Trainer |
| MVP-09 | Learning-material upload | 5 | Trainer |
| MVP-10 | Document processing pipeline | 5 | Trainer, Platform admin |
| MVP-11 | RAG-based document search | 5 | Learner, Trainer |
| MVP-12 | Document Q&A | 5 | Learner |
| MVP-13 | Source citations | 5 | Learner, Trainer |
| MVP-14 | MCQ generation | 6 | Trainer |
| MVP-15 | Question validation | 6 | Trainer |
| MVP-16 | Human review | 6, 9 | Trainer, Competency framework admin |
| MVP-17 | Course recommendation | 7 | Learner, Training manager |
| MVP-18 | Personalized learning path | 7 | Learner |
| MVP-19 | Learner dashboard | 8 | Learner |
| MVP-20 | Trainer/admin review dashboard | 9 | Trainer, admins |
| MVP-21 | Mock iGOT adapter | 10 | Platform admin |
| MVP-22 | Audit logs | 2, 11 | Auditor |
| MVP-23 | Responsible-AI controls | 5, 6, 11 | Platform admin, Auditor |
| MVP-24 | Basic progress tracking | 8 | Learner, Trainer |
| MVP-25 | Basic reporting | 9 | Training manager, Learner |
| MVP-F1 | Platform security baseline | 2, 12 | Platform admin |
| MVP-F2 | Background job infrastructure | 2 | Platform admin |
| MVP-F3 | UX foundations | 8 | All |
| MVP-F4 | Accessibility and i18n foundation | 8, 12 | All |

---

## 3. MVP capabilities

### MVP-01 Authentication

- **Feature IDs:** SEC-001, SEC-003, SEC-005, SEC-013, SEC-014
- **User value:** Only provisioned users can access personal competency data.
- **Scope:**
  - Username/email and password login.
  - Adaptive password hashing.
  - Server-side sessions in HttpOnly/Secure/SameSite cookies, with CSRF protection.
  - Idle and absolute timeouts; session rotation.
  - Logout and revoke-all.
  - Re-authentication for sensitive admin actions.
  - Login rate limiting and lockout policy.
  - Administrator-initiated password set/reset.
- **Out-of-scope behaviour:** No self-registration. No SSO/OIDC (SEC-004 is P1). No MFA enforcement (Decision required, P1). No email-based password reset unless a notification provider is decided.
- **Dependencies:** MVP-F1; DATA_MODEL `User`, `Session`.
- **Acceptance criteria:**
  - Valid credentials create a session cookie with the HttpOnly, Secure and SameSite flags.
  - Invalid credentials return a generic error.
  - N failed attempts trigger lockout (N configurable).
  - Sessions expire on idle and absolute timeouts.
  - Logout invalidates the session server-side.
  - Every login, logout, failure and lockout creates an AuditLog record.
- **API requirements:** `POST /api/v1/auth/login`, `POST /api/v1/auth/logout`, `GET /api/v1/auth/session`, `POST /api/v1/auth/password/change`, `POST /api/v1/auth/reauthenticate`, `POST /api/v1/auth/sessions/revoke-all`.
- **Data requirements:** `User` (credential hash, status, lockout counters), `Session`, `AuditLog`.
- **UI requirements:** Login screen; session-expiry warning dialog; re-authentication dialog.
- **Test requirements:**
  - Unit tests for password hashing and lockout.
  - Integration tests for session lifecycle and CSRF rejection.
  - Rate-limit tests.
  - Audit event assertions.
- **Security requirements:** OWASP ASVS-aligned authentication controls. No credentials in logs. Generic errors.
- **Failure states:** Locked account; expired session; CSRF failure (403); rate limited (429 with Retry-After).

### MVP-02 Role-based access control

- **Feature IDs:** SEC-002, SEC-012 (alias), ADM-001
- **User value:** Personal and restricted data is visible only to the people who need it.
- **Scope:**
  - Eight fixed access roles: `learner`, `trainer`, `department_admin`, `org_admin`, `competency_admin`, `training_manager`, `auditor`, `platform_admin`.
  - Organisation and department scoping.
  - Server-side policy checks on every endpoint.
  - User management for administrators: create, deactivate, assign access roles.
- **Out-of-scope behaviour:** No custom permission sets (ADM-016, P1). No attribute-based policies. No cross-organisation administration in the UI (ROLE-013, P1).
- **Dependencies:** MVP-01.
- **Acceptance criteria:**
  - The permission matrix ([SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §4) is implemented as code.
  - Every endpoint has automated tests for each access role: allowed and denied.
  - Out-of-scope resources return 403 or 404 without leaking existence details.
  - The last `org_admin` cannot be removed.
  - Every role change is audited.
- **API requirements:** `GET/POST /api/v1/users`, `GET/PATCH /api/v1/users/{id}`, `PUT /api/v1/users/{id}/access-roles`.
- **Data requirements:** `User`, `UserAccessRole`, `Department`, `Organization`.
- **UI requirements:** Users table and form (Admin dashboard). Unavailable actions are hidden or disabled, but the server still enforces them.
- **Test requirements:** Generated authorisation test matrix (endpoint × role); privilege-escalation tests.
- **Security requirements:** Default deny; no authorisation decisions in the frontend; organisation filter applied in the data-access layer.
- **Failure states:** 401 unauthenticated; 403 forbidden; 404 for resources outside scope where existence must not be revealed.

### MVP-03 User profile

- **Feature IDs:** UX-021, UX-015
- **User value:** Accurate profile data, a clear privacy and AI-use notice, and a guided start.
- **Scope:**
  - First-login onboarding: privacy and AI-use notice acknowledgement, profile confirmation, department and job role selection, and an optional start of the pre-assessment.
  - Profile view/edit of permitted fields: name, designation, department, job role, language preference (English only in MVP).
- **Out-of-scope behaviour:** No self-service data download (P1). No account deletion requests (SEC-019, P1). No avatar uploads.
- **Dependencies:** MVP-01, MVP-04.
- **Acceptance criteria:**
  - A user cannot start any assessment before acknowledging the notice; the acknowledgement is stored with version and timestamp.
  - Onboarding can be resumed.
  - Changing job role is audited and triggers recomputation of gaps.
- **API requirements:** `GET /api/v1/me`, `PATCH /api/v1/me`, `PUT /api/v1/me/job-role`, `POST /api/v1/me/notice-acknowledgements`.
- **Data requirements:** `User`, `NoticeAcknowledgement`.
- **UI requirements:** Onboarding screen; Settings (profile section).
- **Test requirements:** Onboarding flow tests; validation tests; audit on role change.
- **Security requirements:** Users may edit only permitted fields; server-side field allow-list (no mass assignment).
- **Failure states:** No job roles configured (onboarding blocked with administrator contact); validation errors.

### MVP-04 Department and role selection

- **Feature IDs:** ROLE-001, ADM-002, ADM-003
- **User value:** Requirements, assessments and recommendations are anchored to the learner's actual job role.
- **Scope:**
  - Administrators maintain departments and job roles; roles can be soft-deactivated.
  - Learners select a department and job role.
  - Job roles are named `JobRole` in code and API to avoid confusion with access roles (DEC-012).
- **Out-of-scope behaviour:** No AI role suggestion (AI-003, P1). No role versioning UI (ROLE-012, P1). No department hierarchies.
- **Dependencies:** MVP-02.
- **Acceptance criteria:**
  - A learner without a job role cannot start a pre-assessment.
  - Deactivated roles are not selectable.
  - Learners on a deactivated role are prompted to reselect.
  - All changes are audited.
- **API requirements:** `GET/POST /api/v1/departments`, `PATCH /api/v1/departments/{id}`, `GET/POST /api/v1/job-roles`, `GET/PATCH /api/v1/job-roles/{id}`, `PUT /api/v1/me/job-role`.
- **Data requirements:** `Department`, `JobRole`, `User.job_role_id`.
- **UI requirements:** Onboarding role step; Admin dashboard departments and job roles tables.
- **Test requirements:** CRUD tests; soft-deactivation tests; authorisation tests.
- **Security requirements:** Organisation-scoped; only `org_admin` / `competency_admin` may change job roles.
- **Failure states:** Duplicate name conflict (409); deactivation blocked while referenced (use soft deactivate).

### MVP-05 Competency framework

- **Feature IDs:** ADM-004, ROLE-002, ROLE-004
- **User value:** One authoritative, approved definition of what each role requires.
- **Scope:**
  - Maintain competency frameworks, competencies, level scales (default five levels) and approved role-to-competency mappings with required levels.
  - Link each job role to its pre-assessment blueprint.
  - **Import the CSCD structure** from `data/processed/competency_framework.json` as a reference framework: 4 clusters, 25 competencies, names and page references **only**.
  - **Author functional statistical competencies** on the platform (no source exists).
  - Draft/approved status on frameworks and mappings.
- **Out-of-scope behaviour:**
  - No CSCD definitions or behavioural indicators (DoPT copyright).
  - No FRAC import (source unreachable).
  - No competency dependencies (CMP-009, P2).
  - No critical-skill flags (CMP-005, P1).
  - No automatic mapping suggestions.
- **Dependencies:** MVP-04. **Human dependency D-01/D-02:** SME-approved functional competencies and role mappings ([PRD.md](PRD.md) §21).
- **Acceptance criteria:**
  - A mapping cannot be used by assessments or gap detection until it is `approved`.
  - Imported CSCD entries have `definition = null` and a `source_page` reference.
  - Imports preserve provenance (source URL, SHA-256, licence notes).
  - Every change is audited and versioned.
- **API requirements:** `GET/POST /api/v1/competency-frameworks`, `GET /api/v1/competency-frameworks/{id}`, `POST /api/v1/competency-frameworks/{id}/approve`, `GET/POST /api/v1/competencies`, `PATCH /api/v1/competencies/{id}`, `GET/PUT /api/v1/job-roles/{id}/competencies`, `GET /api/v1/job-roles/{id}/assessments`.
- **Data requirements:** `CompetencyFramework`, `Competency`, `CompetencyLevel`, `RoleCompetency`, `SourceRecord`.
- **UI requirements:** Framework, competency and role-mapping editors in Admin dashboard, with provenance and approval badges.
- **Test requirements:**
  - Import test against the canonical dataset, asserting no definition text.
  - Approval gating tests.
  - Versioning tests.
- **Security requirements:** Only `competency_admin` (and `org_admin` for read) may modify; restricted-content guard on import.
- **Failure states:** Import validation failure (dataset validator verdict must not be INVALID); unapproved mapping used (blocked); referenced competency deactivated (blocked).

### MVP-06 Initial competency assessment

- **Feature IDs:** AI-001, ASM-001, ASM-006, ASM-007, ASM-008, ASM-009, ASM-010, ROLE-007 (alias), ASM-011, ASM-014, ASM-017, ASM-019, ASM-020, ASM-021, ASM-031, ASM-032, CMP-017 (alias), ADM-006, ADM-007 (alias), AI-009, AUT-004 (alias), TRN-008
- **User value:** An evidence-based baseline instead of self-declared skills.
- **Scope:**
  - Question bank of single-correct MCQs with difficulty, topic, competency, explanation and citation.
  - Manual question authoring with a mandatory citation.
  - Assessment blueprints by topic, competency or job role, with custom counts and per-competency minimum items.
  - Publishing restricted to approved question versions.
  - Attempts with randomised question and option order (seed stored); resumable attempts.
  - Deterministic scoring on submit; feedback and explanations per policy; attempt history.
  - The first completed pre-assessment is stored as the immutable baseline.
- **Out-of-scope behaviour:**
  - No true/false, fill-blank, scenario or case questions (P1).
  - No adaptive selection (AI-008, P1).
  - No timers or attempt limits (P1); no manual grading (P1).
  - No post-assessment / reassessment (P1); no certification (P2).
- **Dependencies:** MVP-05; approved questions (MVP-16, or manual questions reviewed under MVP-16 policy).
- **Acceptance criteria:**
  - Publishing fails if any question version is unapproved or any competency lacks the minimum items.
  - Answer keys are never included in any response before submission.
  - The delivered order can be reconstructed from the stored seed.
  - Scoring uses the exact delivered question versions.
  - A key correction re-scores affected attempts with an audit record and learner notice.
- **API requirements:**
  - `GET/POST /api/v1/assessments`, `PATCH /api/v1/assessments/{id}`, `POST /api/v1/assessments/{id}/publish`.
  - `POST /api/v1/assessments/{id}/attempts`, `GET /api/v1/attempts/{id}`, `PUT /api/v1/attempts/{id}/answers/{question_id}`, `POST /api/v1/attempts/{id}/submit`, `GET /api/v1/attempts/{id}/result`, `GET /api/v1/me/attempts`.
  - `GET/POST /api/v1/questions`, `GET/PATCH /api/v1/questions/{id}`, `GET /api/v1/questions/{id}/versions`.
- **Data requirements:** `Assessment`, `AssessmentQuestion`, `AssessmentAttempt`, `AttemptQuestion`, `Answer`, `Question`, `QuestionVersion`, `QuestionOption`, `Citation`.
- **UI requirements:** Quiz builder (manual authoring and blueprint), Assessment screen, Assessment results, history list.
- **Test requirements:**
  - Key-leak tests on every attempt endpoint.
  - Seed reproducibility tests.
  - Publishing guard tests.
  - Re-scoring tests.
  - Accessibility tests on the assessment screen.
- **Security requirements:** Attempts bound to the session user; server-authoritative state; no client-side scoring.
- **Failure states:** No published assessment for role; attempt expired; submission conflict (409 if already submitted); scoring failure (retryable pending state).

### MVP-07 Competency score calculation

- **Feature IDs:** AI-012, AI-016, AI-017, AI-018, CMP-002, CMP-016, AUT-002
- **User value:** Reproducible, explainable estimates with honest limitations.
- **Scope:**
  - Deterministic, versioned scoring method ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §25): difficulty-weighted proportion correct per competency, mapped to levels using configurable thresholds.
  - Evidence-sufficiency bands; append-only evidence ledger.
  - Explanation block (method version, evidence, limitations, correction route).
  - Recomputation job when evidence changes.
- **Out-of-scope behaviour:** No LLM involvement in scoring; no IRT/BKT (P2); no learning-activity evidence (CMP-018, P1).
- **Dependencies:** MVP-06; DEC-020 (weights and thresholds).
- **Acceptance criteria:**
  - Identical evidence and method version always produce identical scores.
  - No estimate exists without evidence.
  - Estimates in the `insufficient` band never produce gaps.
  - Every estimate response includes an explanation block.
  - Voiding evidence recomputes with an audit record.
- **API requirements:** `GET /api/v1/me/competency-profile`, `GET /api/v1/users/{id}/competency-profile`, `GET /api/v1/users/{id}/competencies/{competency_id}/evidence`.
- **Data requirements:** `UserCompetency`, `UserCompetencySnapshot`, `CompetencyEvidence`, `CompetencyLevel` (thresholds), `BackgroundJob`; scoring `method_version` is code configuration recorded on each estimate ([DATA_MODEL.md](DATA_MODEL.md)).
- **UI requirements:** Competency profile with band labels and a "How was this calculated?" panel.
- **Test requirements:** Property-based determinism tests; golden scoring fixtures; band threshold tests; recomputation idempotency.
- **Security requirements:** Profile access limited to self, assigned trainers and scoped admins.
- **Failure states:** Thresholds not configured (score without level, notice); recomputation failure (estimate marked stale).

### MVP-08 Competency-gap detection

- **Feature IDs:** AI-002, CMP-001, CMP-004, CMP-006, CMP-007, CMP-008, CMP-019
- **User value:** Clear development priorities, framed constructively.
- **Scope:**
  - Gap computation (required minus estimated level) where evidence is at least `medium`.
  - Strengths and developing areas; required-versus-current comparison (chart with table).
  - Human-reviewed adjustments with mandatory reason and learner visibility.
- **Out-of-scope behaviour:** No critical-skill weighting (P1); no heatmaps (P1); no role-readiness score (P1); no comparisons between learners.
- **Dependencies:** MVP-07.
- **Acceptance criteria:**
  - A gap requires an approved required level and evidence ≥ medium.
  - Insufficient-evidence competencies show "reassess to confirm".
  - Adjustments require a reason, cannot be self-applied, and are visible to the learner with reviewer and time.
- **API requirements:** `GET /api/v1/me/competency-gaps`, `GET /api/v1/users/{id}/competency-gaps`, `POST /api/v1/user-competencies/{id}/adjustments`.
- **Data requirements:** `UserCompetency`, `RoleCompetency`, `CompetencyEvidence` (adjustment type).
- **UI requirements:** Competency-gap analysis screen; adjustment dialog (trainer/admin).
- **Test requirements:** Gap computation fixtures; adjustment authorisation tests; wording lint for prohibited evaluative terms (UI copy list).
- **Security requirements:** Adjustments restricted to `trainer` (assigned scope) and `competency_admin`; audited.
- **Failure states:** No role; role not configured; no estimates.

### MVP-09 Learning-material upload

- **Feature IDs:** MAT-001, MAT-002, MAT-004, MAT-028, MAT-031, ADM-008, TRN-002 (alias)
- **User value:** Trainers bring official and institutional material into a governed library.
- **Scope:**
  - Learning materials with metadata: title, organisation, licence/usage notes, licence status, access scope, topics.
  - PDF, DOCX and TXT upload with MIME, signature and size checks.
  - Uploader attestation (right to use; no personal data).
  - SHA-256 duplicate detection; malware-scan hook (no-op placeholder that records "not scanned").
  - Soft deactivation.
  - Seed import of the 19 collected documents from `data/processed/documents.json` **metadata**. Raw PDFs are imported only in environments where they exist locally; their licence status stays as recorded.
- **Out-of-scope behaviour:**
  - No PPT/PPTX or images (P1); no versioning UI (MAT-027, P1).
  - No near-duplicate detection; no bulk upload; no URL-based import from user-supplied URLs (SSRF).
- **Dependencies:** MVP-02, MVP-F2, object storage (DEC-008).
- **Acceptance criteria:**
  - Invalid files are rejected with a specific error code.
  - Identical bytes link to the existing document.
  - A material without licence metadata cannot be used for AI generation.
  - Deactivation removes the material from search, Q&A and generation immediately.
  - Imported seeds retain source URL, retrieval date, SHA-256 and data_status.
- **API requirements:** `GET/POST /api/v1/learning-materials`, `GET/PATCH/DELETE /api/v1/learning-materials/{id}`, `POST /api/v1/learning-materials/{id}/documents` (multipart), `GET /api/v1/documents/{id}`, `GET /api/v1/documents/{id}/content`.
- **Data requirements:** `LearningMaterial`, `Document`, `SourceRecord`, `BackgroundJob`.
- **UI requirements:** Document library with upload dialog, attestation, access scope and status chips.
- **Test requirements:** File-validation tests (spoofed extension, oversized, macro DOCX); ACL tests on download; duplicate tests.
- **Security requirements:** Storage keys not guessable; downloads authorised per request; no inline rendering of uploaded HTML; content-disposition attachment for non-PDF.
- **Failure states:** Validation failure (422); storage failure (retryable 503); duplicate (200 with `duplicate_of`).

### MVP-10 Document processing pipeline

- **Feature IDs:** MAT-007, MAT-008, MAT-009, MAT-010, MAT-011, MAT-012, MAT-013, MAT-029, MAT-030
- **User value:** Uploaded material becomes searchable and usable for grounded AI without manual steps.
- **Scope:**
  - Idempotent background pipeline: extract (pypdf for PDF; DOCX and TXT parsers), clean, normalise to pages and blocks with offsets, chunk (page-span preserving), enrich metadata (rule-based topics marked ASSUMED), embed (embedding provider interface), store vectors (pgvector).
  - Statuses: `uploaded`, `extracting`, `chunking`, `embedding`, `ready`, `needs_ocr`, `failed`; reprocess.
- **Out-of-scope behaviour:** No OCR (documents without text are marked `needs_ocr`); no LLM tagging, summaries or keyword extraction (P1); no table extraction.
- **Dependencies:** MVP-09, MVP-F2, DEC-006 (embedding provider).
- **Acceptance criteria:**
  - Reprocessing never duplicates chunks or embeddings.
  - Every chunk has page_start/page_end, offsets and chunker version.
  - Every embedding records model ID and dimension.
  - Scanned documents (e.g. NSSTA-DOC-004, NSSTA-DOC-006 seeds) end in `needs_ocr`, not `ready`.
- **API requirements:** `GET /api/v1/documents/{id}`, `POST /api/v1/documents/{id}/reprocess`, `GET /api/v1/jobs/{id}`.
- **Data requirements:** `Document`, `DocumentPage`, `DocumentChunk`, `Embedding`, `BackgroundJob`.
- **UI requirements:** Processing status and retry in Document library; chunk and page info in Document viewer (admin).
- **Test requirements:** Pipeline fixtures using collected public PDFs (locally available); idempotency tests; failure-injection tests; embedding provider contract tests with a fake provider.
- **Security requirements:** Parsing in worker processes with resource limits; no execution of embedded content; extracted text treated as untrusted.
- **Failure states:** `needs_ocr`; `failed` with reason (parser error, provider unavailable); dead-letter after max retries.

### MVP-11 RAG-based document search

- **Feature IDs:** MAT-014, MAT-015, UX-019
- **User value:** Fast discovery of relevant official passages, including exact statistical acronyms.
- **Scope:** Semantic search (pgvector similarity) and keyword search (PostgreSQL full-text) as selectable modes; filters for organisation, topic, document type and status; ACL filtering before ranking; page-linked results.
- **Out-of-scope behaviour:** No hybrid fusion (MAT-016, P1); no reranker; no global cross-entity search (UX-004, P1); no Hindi text-search configuration.
- **Dependencies:** MVP-10.
- **Acceptance criteria:**
  - Results never include inaccessible documents (tested with multi-scope fixtures).
  - Acronym queries (e.g. "PLFS", "CPI") return exact matches in keyword mode.
  - If embeddings are unavailable, the response states the fallback to keyword mode.
- **API requirements:** `POST /api/v1/search` (`mode`, `query`, `filters`, pagination).
- **Data requirements:** `DocumentChunk` (tsvector), `Embedding`.
- **UI requirements:** Document library search bar, mode toggle, filter chips, results with page links.
- **Test requirements:** ACL retrieval tests; relevance smoke set; fallback tests.
- **Security requirements:** Query length limits; rate limiting; queries logged without storing full text beyond retention policy.
- **Failure states:** Empty results (empty state with tips); embedding service down (keyword fallback notice).

### MVP-12 Document Q&A

- **Feature IDs:** MAT-017, MAT-018, RAI-001, RAI-003, RAI-015
- **User value:** Trustworthy answers from official documents, or an honest "not found".
- **Scope:**
  - Single-turn question answering: retrieval within scope, then prompt assembly (retrieved content treated as untrusted data), then generation through the LLM provider interface, then citation verification.
  - Confidence band; abstention when evidence is insufficient or verification fails.
  - Scope selector (all accessible documents or a selected material).
- **Out-of-scope behaviour:** No multi-turn conversation or memory (tutor, P1); no summaries (P1); no web search; no answers from model knowledge without sources.
- **Dependencies:** MVP-11, MVP-13, MVP-23, DEC-005 (LLM provider).
- **Acceptance criteria:**
  - 100% of displayed answers have at least one verified citation (invariant M-09).
  - Golden-set unanswerable questions produce abstentions, with results recorded (RAI-012).
  - Every response has an AIInteractionLog record.
  - A provider failure produces an explicit error, never a partial answer.
- **API requirements:** `POST /api/v1/document-qa` (`question`, `scope`) → answer, citations[], confidence, abstained, abstention_reason, interaction_id.
- **Data requirements:** `AIInteractionLog`, `Citation` (response-scoped), `PromptTemplate`.
- **UI requirements:** Document Q&A screen with citation chips, confidence label and abstention message.
- **Test requirements:** Citation verification unit tests; injection test suite; provider fake for deterministic tests; golden evaluation run.
- **Security requirements:** Personal-data redaction of question text before the provider call; per-user AI rate limit; no tools with side effects.
- **Failure states:** Abstained (normal outcome); provider timeout (retry once, then error state); rate limited (429).

### MVP-13 Source citations

- **Feature IDs:** MAT-019, MAT-020, RAI-002 (alias)
- **User value:** Every AI claim can be checked against the source page.
- **Scope:**
  - Citation objects: document, version, chunk, page_start/page_end, quoted span, source URL, organisation, licence status.
  - Verification: the chunk is in the retrieved set and accessible, and the quoted span matches the chunk text after whitespace normalisation.
  - Page numbers only where known.
- **Out-of-scope behaviour:** No line-level highlighting; no multi-document synthesis citations beyond listing each source.
- **Dependencies:** MVP-10.
- **Acceptance criteria:**
  - An unverifiable citation is dropped, and if no verified citation remains the answer is withheld.
  - Page numbers are never fabricated.
  - Citation chips open Document viewer at the cited page.
- **API requirements:** Citation schema shared by `POST /api/v1/document-qa` and question payloads; `GET /api/v1/documents/{id}/pages/{page}` for the viewer.
- **Data requirements:** `Citation`, `DocumentChunk`, `DocumentPage`.
- **UI requirements:** Citation chips and Document viewer page navigation.
- **Test requirements:** Span-match tests with normalisation edge cases; page mapping tests.
- **Security requirements:** Viewer re-checks ACL on each page request.
- **Failure states:** Citation invalid (dropped, logged); document access revoked (citation shows "source no longer accessible").

### MVP-14 MCQ generation

- **Feature IDs:** AI-007, AUT-003, TRN-003 (alias)
- **User value:** Trainers get source-grounded candidate questions in minutes.
- **Scope:**
  - Generation jobs parameterised by source materials (licence-permitted only), topic, competency, difficulty and count.
  - Chunk selection, then structured-output generation (JSON schema), then persistence as `pending_validation` with full AI metadata.
  - Job progress; idempotency key.
- **Out-of-scope behaviour:** No other question types (P1); no multilingual generation (P1); no generation from CSCD or other restricted-licence materials; no automatic publishing.
- **Dependencies:** MVP-10, MVP-23, DEC-005.
- **Acceptance criteria:**
  - Every candidate stores source chunk IDs, evidence span, model, prompt version, parameters, timestamp and statuses.
  - Candidates never appear in assessments before approval.
  - Generation refuses materials without permissive licence metadata.
- **API requirements:** `POST /api/v1/question-generation-jobs` (Idempotency-Key), `GET /api/v1/question-generation-jobs/{id}`.
- **Data requirements:** `QuestionGenerationJob` (BackgroundJob subtype), `Question`, `QuestionVersion`, `QuestionOption`, `Citation`, `AIInteractionLog`.
- **UI requirements:** Quiz builder generation panel with source picker (licence indicators), parameters and job progress.
- **Test requirements:** Schema validation tests with a fake provider; licence gate tests; idempotency tests.
- **Security requirements:** Only `trainer`/`competency_admin`; source ACL enforced; per-organisation generation quota.
- **Failure states:** Provider error (retry, then failed); schema-invalid outputs discarded and counted; zero valid candidates (completed with reasons).

### MVP-15 Question validation

- **Feature IDs:** ASM-022, ASM-023, ASM-024, RAI-004, RAI-005
- **User value:** Reviewers see only plausible, grounded questions, with problems flagged.
- **Scope:** Validators recorded per question version:
  - schema and structural rules (4 unique options, exactly one correct);
  - evidence-span exact match (automatic rejection on failure);
  - exact duplicate (normalised hash) and near-duplicate (embedding similarity threshold, provisional);
  - independent answer-key check (validator model answers from the source without the key).
- **Out-of-scope behaviour:** No quality scoring (ASM-025, P1); no empirical difficulty (P1); no multi-validator consensus.
- **Dependencies:** MVP-14, MVP-10.
- **Acceptance criteria:**
  - No question with an unmatched evidence span reaches review.
  - Validator disagreement is shown to reviewers.
  - A validator outage marks `validation_incomplete`, which needs an explicit reviewer override with reason.
- **API requirements:** `GET /api/v1/questions/{id}/validations`.
- **Data requirements:** `QuestionValidation`, `AIInteractionLog`.
- **UI requirements:** Validation panel with flags in Quiz review.
- **Test requirements:** Validator unit tests with crafted bad questions (wrong key, fabricated span, duplicate); evaluation of validator agreement on a reviewed sample.
- **Security requirements:** Validator prompts treat question and source as untrusted data.
- **Failure states:** `failed_validation` (auto-rejected with reason); `validation_incomplete`.

### MVP-16 Human review

- **Feature IDs:** ASM-027, ASM-028, ASM-029, ASM-030, ADM-009 (alias), ADM-010, RAI-006 (alias), RAI-017, TRN-004, TRN-005, TRN-006, TRN-007 (aliases)
- **User value:** Humans decide what reaches learners.
- **Scope:**
  - Review queue with source passage side by side and validator flags.
  - Approve, reject (reason required) and edit (new version, re-validated).
  - Approval policy: single reviewer, optionally a required second reviewer; self-approval blocked when a second reviewer is required.
  - Override with reason; reassignment.
- **Out-of-scope behaviour:** No review of summaries or tutor outputs (P1); no multi-stage workflows; no SLA escalation automation.
- **Dependencies:** MVP-15.
- **Acceptance criteria:**
  - 100% of questions used in assessments have an approval record (invariant M-11).
  - Rejected questions are unusable.
  - Edits never mutate approved versions.
  - All decisions are audited with reviewer, time and reasons.
- **API requirements:** `GET /api/v1/review-tasks`, `GET /api/v1/review-tasks/{id}`, `POST /api/v1/review-tasks/{id}/decision`, `POST /api/v1/review-tasks/{id}/reassign`, `PATCH /api/v1/questions/{id}`, `GET/PATCH /api/v1/admin/settings` (approval policy).
- **Data requirements:** `ReviewTask`, `Approval`, `QuestionVersion`, `AuditLog`.
- **UI requirements:** Quiz review screen (keyboard-first); review counts on dashboards.
- **Test requirements:** Workflow state-machine tests; policy tests; audit assertions; accessibility tests on the review screen.
- **Security requirements:** Reviewers need access to the cited source; decisions are server-validated against the task state (optimistic concurrency).
- **Failure states:** Concurrent decision (409); source inaccessible to reviewer (task reassignment prompt).

### MVP-17 Course recommendation

- **Feature IDs:** AI-005, AI-006, PER-002 (alias), PER-009, PER-010, ADM-005, AUT-001, RAI-011, IGOT-002 (alias)
- **User value:** Limited learning time goes to the most relevant content, with reasons.
- **Scope:**
  - Internal catalogue management, including seeding of 99 NSSTA programme listings from `data/processed/training_programmes.json` (provenance kept; topic tags ASSUMED, so not used until reviewed).
  - Human-approved course/material-to-competency and topic mappings.
  - Deterministic ranking with reason objects; dismiss and accept feedback; recomputation after assessments.
  - Mock iGOT source behind a feature flag with MOCK labels.
- **Out-of-scope behaviour:**
  - No LLM ranking; no collaborative filtering; no prerequisite, difficulty or training-history logic (P1).
  - No real iGOT data; no deep links to iGOT (unverified URL pattern).
  - NSSTA programmes are listings with unknown dates, not enrollable courses.
- **Dependencies:** MVP-08, MVP-21.
- **Acceptance criteria:**
  - Every recommendation has a reason and provenance.
  - Unreviewed mappings have no influence.
  - With the mock flag on, every iGOT item shows "MOCK - not real iGOT data" (invariant M-13).
  - With the flag off, no iGOT items appear.
  - Results are identical for identical inputs.
- **API requirements:** `GET /api/v1/me/recommendations`, `POST /api/v1/recommendations/{id}/feedback`, `GET/POST /api/v1/courses`, `GET/PATCH /api/v1/courses/{id}`, `PUT /api/v1/courses/{id}/competencies`.
- **Data requirements:** `Course`, `CourseCompetency`, `CourseTopic`, `Recommendation`, `SourceRecord`.
- **UI requirements:** Recommendation cards (Learner dashboard, Course discovery) with "Why recommended", source and MOCK badges; course editor with mapping review.
- **Test requirements:** Ranking fixtures; mapping-approval gate tests; MOCK label snapshot tests; feature-flag tests.
- **Security requirements:** Recommendations computed only from the learner's own data; mock data never persisted as non-mock.
- **Failure states:** Empty catalogue or no matches (empty state); recomputation job failure (previous results with "may be outdated").

### MVP-18 Personalized learning path

- **Feature IDs:** AI-004, PER-003 (alias)
- **User value:** A clear sequence of what to do next.
- **Scope:** Ordered path generated from gaps and recommendations; items with status (not started / in progress / completed) and source (system / self-reported / administrator); regenerate on demand or after assessment; reasons per item.
- **Out-of-scope behaviour:** No weekly or 30-day plans, deadlines or workload awareness (P1/P2); no automatic path updates on gap change beyond the post-assessment trigger (AUT-009, P1); no assignments.
- **Dependencies:** MVP-17.
- **Acceptance criteria:**
  - Every item cites its gap and rule.
  - Regeneration with unchanged inputs gives the same order.
  - Completed items persist across regeneration.
  - Gaps without approved content produce an explicit "no approved content yet" item.
- **API requirements:** `GET /api/v1/me/learning-path`, `POST /api/v1/me/learning-path/regenerate`, `PATCH /api/v1/learning-path-items/{id}`.
- **Data requirements:** `LearningPath`, `LearningPathItem`, `ProgressRecord`.
- **UI requirements:** Learning path screen; Continue learning card.
- **Test requirements:** Determinism and persistence tests; status transition tests.
- **Security requirements:** Paths private to the learner and scoped staff.
- **Failure states:** No gaps (celebration/maintenance message); regeneration failure (previous path retained).

### MVP-19 Learner dashboard

- **Feature IDs:** PER-001, UX-003, UX-009
- **User value:** One place to see status and next action.
- **Scope:** Role-based home routing; learner cards for baseline status, top gaps, continue learning, recommendations, recent activity and pending review of correction requests; independent card loading and error states.
- **Out-of-scope behaviour:** No customisable layout; no notifications centre (P1); no gamification (P1); no calendar (P2).
- **Dependencies:** MVP-08, MVP-17, MVP-18, MVP-24.
- **Acceptance criteria:**
  - Each card loads and fails independently.
  - No card shows another user's data.
  - Users with multiple access roles can switch home views.
- **API requirements:** `GET /api/v1/me/dashboard`.
- **Data requirements:** Aggregated read models only (no new entities).
- **UI requirements:** Learner dashboard screen.
- **Test requirements:** Component tests for card states; end-to-end journey J-01 to J-05.
- **Security requirements:** Dashboard aggregate endpoint enforces the same scopes as source endpoints.
- **Failure states:** Partial failures per card; empty states for new learners.

### MVP-20 Trainer/admin review dashboard

- **Feature IDs:** TRN-001, ADM-012, ADM-014
- **User value:** Trainers and administrators see their work queues and learner status within scope, and configure the platform safely.
- **Scope:**
  - Trainer dashboard: pending reviews, generation jobs, recent uploads, scoped learner status without rankings.
  - Admin dashboard: users, departments, job roles, frameworks, settings and feature flags (including iGOT mock visibility) with audit.
- **Out-of-scope behaviour:** No department analytics or heatmaps (P1); no weak-learner identification (P1); no assignments (P1); no permission editor (P1).
- **Dependencies:** MVP-16, MVP-24.
- **Acceptance criteria:**
  - Counts match the underlying queues.
  - Learner lists are scoped and unranked.
  - Every settings change is audited.
  - Secrets are never displayed.
- **API requirements:** `GET /api/v1/trainer/dashboard`, `GET /api/v1/progress?department_id=`, `GET /api/v1/users/{id}/progress`, `GET/PATCH /api/v1/admin/settings`.
- **Data requirements:** `Setting`, `FeatureFlag`, read models.
- **UI requirements:** Trainer dashboard, Admin dashboard, Settings (admin sections).
- **Test requirements:** Scope tests; settings audit tests.
- **Security requirements:** Settings changes require re-authentication for security-relevant keys.
- **Failure states:** Card-level errors; validation errors on settings.

### MVP-21 Mock iGOT adapter

- **Feature IDs:** IGOT-010, IGOT-011, IGOT-013, IGOT-017, IGOT-018
- **User value:** The integration path is demonstrable without misrepresenting access.
- **Scope:**
  - Use the existing `clients/igot_client.py` interface and `clients/mock_igot_client.py`.
  - Extend the interface with health and mode reporting (documented change, DEC-021).
  - Backend adapter registry; feature flag.
  - Integration health endpoint returning `mock` / `not_connected` / `degraded`.
  - Error mapping to problem codes; provenance on all iGOT-sourced payloads.
- **Out-of-scope behaviour:**
  - No real adapter, sync, deep links or auth integration.
  - No user enrolment or completion features shown to learners from mock data beyond explicit demo views labelled MOCK.
  - No `connected` state.
- **Dependencies:** MVP-F2 (for future sync only), ADM-014.
- **Acceptance criteria:**
  - A mock adapter can never report `connected`.
  - `IGOT_CLIENT_MODE=live` is refused.
  - Contract tests pass for the mock and are ready to run against a future real adapter.
  - Every iGOT payload includes `provenance.data_status`.
- **API requirements:** `GET /api/v1/integrations`, `GET /api/v1/integrations/igot/health`, `GET /api/v1/integrations/igot/courses`.
- **Data requirements:** `IntegrationConnection` (mode, status, last_checked_at); no persistence of mock learner data.
- **UI requirements:** Integration health screen; MOCK badges; "not connected" notices.
- **Test requirements:** Existing 14 mock tests; contract test suite; health mode tests; label tests.
- **Security requirements:** No credentials configured in MVP; environment variables `IGOT_API_BASE_URL` and `IGOT_API_KEY` remain unset placeholders.
- **Failure states:** Adapter refused (live mode); adapter disabled (not connected); mock fixture invalid (startup error).

### MVP-22 Audit logs

- **Feature IDs:** SEC-009, SEC-010, SEC-011, ADM-017, RAI-008 (alias)
- **User value:** Every consequential action is accountable and investigable.
- **Scope:**
  - Append-only AuditLog for authentication, role and permission changes, framework/mapping changes, approvals, adjustments, correction decisions, report exports, settings changes and data access to other users' profiles.
  - AIInteractionLog for every provider call.
  - Structured redacted application logs with correlation IDs.
  - Auditor UI with filters and correlation-ID trace.
- **Out-of-scope behaviour:** No tamper-evident hash chain (P1); no SIEM export (P1); no log-based alerting UI.
- **Dependencies:** Logging infrastructure from Phase 2.
- **Acceptance criteria:**
  - Critical events fail closed if the audit write fails.
  - AI outputs are not shown without a log record (invariant M-12).
  - Auditor access is read-only and itself audited.
  - Logs contain no secrets or passwords.
- **API requirements:** `GET /api/v1/audit-logs`, `GET /api/v1/ai-interactions`, `GET /api/v1/ai-interactions/{id}`.
- **Data requirements:** `AuditLog`, `AIInteractionLog`.
- **UI requirements:** Audit logs screen (events and AI interactions tabs).
- **Test requirements:** Audit emission tests per critical event; redaction tests; fail-closed tests.
- **Security requirements:** No update/delete paths for application users; retention per policy.
- **Failure states:** Audit store unavailable (critical operations refused with 503).

### MVP-23 Responsible-AI controls

- **Feature IDs:** RAI-007, RAI-009, RAI-012, RAI-014, RAI-016, RAI-018, RAI-019
- **User value:** AI features are safe, traceable, contestable and evaluated before use.
- **Scope:**
  - Prompt-injection defences and test corpus.
  - Safety filtering and provider refusal handling.
  - Offline evaluation harness and release gate.
  - AI output versioning metadata.
  - Personal-data redaction before provider calls, and an upload personal-data screen (quarantine on detection).
  - Correction-request workflow.
  - Model and prompt registry (versioned templates; services use registered versions only).
- **Out-of-scope behaviour:** No bias monitoring dashboards (RAI-010, P1); no dataset evaluation reports (P1); no online A/B evaluation.
- **Dependencies:** MVP-12, MVP-14, MVP-15; D-07 (golden datasets).
- **Acceptance criteria:**
  - An AI feature cannot be enabled in pilot without evaluation results for its prompt version.
  - The injection corpus passes.
  - Redaction tests pass.
  - Every correction request gets a recorded decision and reason.
  - Unregistered prompts fail a startup check.
- **API requirements:** `GET /api/v1/admin/prompt-templates`, `POST /api/v1/admin/prompt-templates/{key}/versions`, `POST /api/v1/correction-requests`, `GET /api/v1/correction-requests`, `PATCH /api/v1/correction-requests/{id}`.
- **Data requirements:** `PromptTemplate`, `PromptTemplateVersion`, `EvaluationRun`, `CorrectionRequest`, `AIInteractionLog`.
- **UI requirements:** Correction request action and queue; registry view (platform admin); evaluation summary.
- **Test requirements:** Injection suite; redaction suite; evaluation harness tests; correction workflow tests.
- **Security requirements:** Registry changes restricted to `platform_admin` and audited; evaluation datasets access-controlled.
- **Failure states:** Evaluation gate not met (feature flag cannot be enabled); PII detected in upload (quarantined).

### MVP-24 Basic progress tracking

- **Feature IDs:** PRO-001, PRO-002, PRO-003, PRO-005, PRO-006, PRO-010, PRO-011, PRO-012, PRO-013
- **User value:** Learners and scoped staff can see advancement.
- **Scope:** Progress records with source labels; attempt status; baseline vs current per competency; history with title snapshots; completed, pending and recommended lists; assessment timeline.
- **Out-of-scope behaviour:** No learning hours, growth graphs or before-vs-after comparisons (P1); no streaks (P1); no iGOT completion import (blocked).
- **Dependencies:** MVP-06, MVP-18.
- **Acceptance criteria:**
  - Self-reported completions are labelled.
  - The baseline is immutable.
  - History survives content deactivation.
  - Scoped staff see only permitted users.
- **API requirements:** `POST /api/v1/learning-activities`, `GET /api/v1/me/progress`, `GET /api/v1/me/progress/history`, `GET /api/v1/users/{id}/progress`.
- **Data requirements:** `ProgressRecord`, `LearningActivity`.
- **UI requirements:** Progress sections on Learner dashboard and Progress analytics (basic) screen.
- **Test requirements:** Status transition and source labelling tests; scope tests.
- **Security requirements:** Activity events contain no content text.
- **Failure states:** Invalid transition (409); item removed (history retained).

### MVP-25 Basic reporting

- **Feature IDs:** REP-001, REP-003, REP-004, REP-007, REP-012, REP-014, REP-015
- **User value:** Structured, shareable summaries for development conversations and training planning.
- **Scope:** Asynchronous generation of learner development, competency-gap, assessment and progress reports; HTML view; CSV export with formula-injection escaping; access control per report type and scope; audit of generation and download.
- **Out-of-scope behaviour:** No PDF/Excel (P1); no department reports (P1); no scheduled reports (P2); no aggregate reports below the minimum group size.
- **Dependencies:** MVP-07, MVP-08, MVP-24, MVP-F2.
- **Acceptance criteria:**
  - Learners can generate their own development report.
  - Reports about others require scope and are audited.
  - CSV cells are escaped.
  - Reports carry a notice that they are not an appraisal instrument.
- **API requirements:** `POST /api/v1/reports`, `GET /api/v1/reports/{id}`, `GET /api/v1/reports/{id}/download?format=csv`.
- **Data requirements:** `Report`, `BackgroundJob`, `AuditLog`.
- **UI requirements:** Reports screen.
- **Test requirements:** Authorisation tests per report type × role; CSV escaping tests; audit tests.
- **Security requirements:** Download links authorised per request; no personal data in filenames.
- **Failure states:** Generation failure (retry); unauthorised (403).

---

## 4. Foundation capabilities

These make up the remaining P0 catalogue entries that support all MVP capabilities.

### MVP-F1 Platform security baseline

- **Feature IDs:** SEC-006, SEC-007, SEC-008, SEC-015, SEC-016, SEC-017, SEC-021
- **User value:** Personal and restricted data is protected by default.
- **Scope:** TLS and HSTS; encryption at rest (platform-provided); explicit request and response schemas; input and output validation; secret management and CI secret scanning; threat model per phase.
- **Out-of-scope behaviour:** No field-level encryption; no WAF configuration; no penetration test before pilot (required before production).
- **Dependencies:** DEC-009 (hosting).
- **Acceptance criteria:** No unauthenticated routes except login, health and readiness; secret scanning in CI; threat model reviewed at each phase exit.
- **API requirements:** Applies to all routes; `GET /healthz`, `GET /readyz`.
- **Data requirements:** None specific.
- **UI requirements:** None specific; sanitised rendering.
- **Test requirements:** Schema tests; OWASP API checks; dependency vulnerability scan in CI.
- **Security requirements:** As listed.
- **Failure states:** Validation 422; TLS required.

### MVP-F2 Background job infrastructure

- **Feature IDs:** AUT-012, AUT-013, AUT-014, AUT-015
- **User value:** Reliable long-running processing without blocking users.
- **Scope:** Job queue (DEC-004); job records; bounded retries with backoff; dead-letter state; job monitoring endpoint; Idempotency-Key handling.
- **Out-of-scope behaviour:** No scheduled jobs except the documented retention and health checks (P1 for data refresh); no autoscaling.
- **Dependencies:** Redis (if the selected queue requires it), PostgreSQL.
- **Acceptance criteria:** Worker crashes do not lose jobs; replayed idempotent requests return the original result; dead-lettered jobs are visible.
- **API requirements:** `GET /api/v1/jobs/{id}`, `GET /api/v1/admin/jobs`.
- **Data requirements:** `BackgroundJob`, `IdempotencyKey`.
- **UI requirements:** Job status components.
- **Test requirements:** Failure-injection and idempotency tests.
- **Security requirements:** Jobs carry organisation and actor context; no cross-organisation processing.
- **Failure states:** Retrying; dead-letter; timed out.

### MVP-F3 UX foundations

- **Feature IDs:** UX-001, UX-002, UX-012, UX-013, UX-014
- **User value:** A consistent, understandable interface on any device.
- **Scope:** Responsive layout system; mobile navigation; shared empty, loading and error components mapped to API problem codes with correlation IDs.
- **Out-of-scope behaviour:** No dark mode (P2); no saved views (P2); no guided tours (P1).
- **Dependencies:** Component system ([UI_UX_SPEC.md](UI_UX_SPEC.md)).
- **Acceptance criteria:** Every P0 screen defines and implements empty, loading and error states; usable at 360 px width.
- **API requirements:** Problem responses ([ERROR_HANDLING_SPEC.md](ERROR_HANDLING_SPEC.md)).
- **Data requirements:** None.
- **UI requirements:** Per [UI_UX_SPEC.md](UI_UX_SPEC.md).
- **Test requirements:** Visual and component tests; responsive tests.
- **Security requirements:** No sensitive data in browser storage.
- **Failure states:** Generic error with correlation ID.

### MVP-F4 Accessibility and i18n foundation

- **Feature IDs:** ACC-001, ACC-003, ACC-009, ACC-010, ACC-014, ACC-015, ACC-016, UX-011 (alias)
- **User value:** Usable by all officials, and ready for Hindi.
- **Scope:** English UI; externalised strings; UTF-8 end to end; semantic and screen-reader-friendly components; keyboard operation; accessible forms and charts; reduced motion.
- **Out-of-scope behaviour:** No Hindi translation (P1); no font-size or high-contrast controls (P1); no speech features (P2).
- **Dependencies:** MVP-F3.
- **Acceptance criteria:** Zero serious or critical automated accessibility violations on P0 screens (invariant M-14); manual screen-reader and keyboard test of journeys J-01 to J-07 recorded.
- **API requirements:** Locale negotiation header support.
- **Data requirements:** `User.locale`.
- **UI requirements:** Per [UI_UX_SPEC.md](UI_UX_SPEC.md) §Accessibility.
- **Test requirements:** axe checks in CI; manual audit checklist.
- **Security requirements:** None specific.
- **Failure states:** Missing translation key (English fallback and log).

---

## 5. Features that must not be implemented during MVP

**Rule:** No P1 or P2 feature in [FEATURE_CATALOG.md](FEATURE_CATALOG.md) may be implemented, stubbed into production routes or exposed in the UI during MVP. That covers 140 P1 and 57 P2 entries. This applies to humans and AI coding agents ([AGENT_CONTEXT.md](AGENT_CONTEXT.md) rule 1). Schema columns needed later may be added only when they carry no behaviour and are recorded in [DECISIONS.md](DECISIONS.md).

Explicitly forbidden during MVP (non-exhaustive, highest scope-creep risk):

| Forbidden item | Catalog IDs | Why excluded |
|---|---|---|
| Conversational AI tutor (any multi-turn chat) | TUT-001 to TUT-020 | P1; needs conversation retention policy and injection hardening |
| Adaptive assessment, IRT, BKT, knowledge tracing | AI-008, FUT-004 to FUT-006, CMP-011 | P1/P2; requires calibrated item data |
| LLM-based scoring of free-text, scenario or case answers | AI-010, AI-011, ASM-002 to ASM-005, ASM-018 | P1; human grading governance not defined |
| Any LLM involvement in competency score calculation | AI-012 (constraint) | PRD-AI-005 |
| Real iGOT adapter, sync, deep links, auth or SSO | IGOT-001, IGOT-003 to IGOT-009, IGOT-012, IGOT-014 to IGOT-016, AUT-011 | Blocked: no authorisation or documentation |
| Presenting mock iGOT data without MOCK labels, or a `connected` state for mocks | IGOT-011 (constraint) | Invariant M-13 |
| OCR, image, PPT/PPTX upload | MAT-003, MAT-005, MAT-006 | P1 |
| Hybrid search fusion, rerankers, summaries, AI tagging, keyword/concept extraction | MAT-016, MAT-021 to MAT-026 | P1/P2 |
| Department heatmaps, comparisons and analytics dashboards | CMP-003, ANA-001 to ANA-016, ADM-013, REP-002 | P1/P2; aggregation and suppression rules first |
| Weak-learner identification and learner performance rankings | TRN-010, TRN-011 | P1; high misuse risk |
| Role-readiness score, career suggestions, transition pathways | ROLE-008 to ROLE-011, FUT-003 | P1/P2; misuse risk for selection decisions |
| Gamification, leaderboards, badges, streaks, certificates | GAM-001 to GAM-012, PRO-009 | P1/P2 |
| Notifications and reminders | AUT-006, AUT-007, UX-005 | P1 |
| Hindi translations and multilingual AI | ACC-002, ACC-004 to ACC-008 | P1/P2 (i18n architecture only in MVP) |
| Post-assessment and before-vs-after comparison | ASM-012, PRO-007, PRO-008, CMP-010, CMP-013 | P1 |
| PDF/Excel exports, scheduled reports | REP-010, REP-011, REP-013 | P1/P2 |
| Weekly/30-day/daily plans, goals, spaced repetition | PER-004 to PER-008, PER-011 to PER-018 | P1/P2 |
| Assignments and custom permissions | ADM-011, ADM-016, TRN-009 | P1 |
| Predictive analytics, forecasting, workforce intelligence | AI-013, FUT-001, FUT-002, FUT-013 to FUT-015, FUT-018 | P2 |
| Offline mode, mobile app, voice | FUT-009 to FUT-012 | P2 |
| Reproducing CSCD definitions or behavioural indicators | ADM-004 (constraint) | DoPT copyright policy |
| Importing government employee data from any external system | — | Non-goal NG-6 |

## 6. MVP data boundary

| Data | MVP use | Status and restriction |
|---|---|---|
| `data/processed/training_programmes.json` (99 programmes) | Seed catalogue listings | MACHINE_OBSERVED; topic tags ASSUMED; dates unknown; not learner-visible until reviewed and licence confirmed |
| `data/processed/documents.json` (22 records) | Seed document library metadata | Titles for 21 records UNVERIFIED_SECONDHAND; licence not verified; 3 link-only; 2 scanned |
| `data/processed/competency_framework.json` (25 competencies) | Reference framework import (names only) | DoPT copyright restriction; definitions excluded |
| `data/processed/tpac_references.json` (16) | Not used by MVP features (reference only) | Kept for future governance views |
| `data/processed/topics.json` (23 terms) | Seed taxonomy | ASSUMED; reviewed before driving recommendations |
| `data/samples/mock/MOCK_igot_fixtures.json` | Mock iGOT adapter only | MOCK; never imported into application tables as real data |
| Real employee data | Pilot accounts created on the platform only | Requires lawful basis and approvals (DEC-027) |

## 7. MVP exit criteria

See [PRD.md](PRD.md) §24 and [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) Phase 12 exit criteria. In short, every capability above meets its acceptance criteria, invariants M-09 and M-11 to M-14 hold, authorisation and injection suites pass, and no forbidden item is present.
