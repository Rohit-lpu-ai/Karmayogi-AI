# Phase 4 - End-to-End Competency Learning Platform: Plan

| Field | Value |
|---|---|
| **Date** | 2026-09-15 |
| **Baseline** | Phases A, B, C implemented and tested (uncommitted on branch `Diw`); migrations `0001`-`0005`; 196 backend, 46 frontend, 10 Playwright journeys passing |
| **Inputs audited** | PRD, MVP_SCOPE (MVP-01/02/05/06/16/17/18/19/20/22/24/25), SECURITY_RESPONSIBLE_AI §3 (authentication), §4 (permission matrix), §11 (audit catalogue), §12 (privacy), §15 (high-impact restrictions); DATA_MODEL (User, Department, JobRole, ReviewTask, Approval, Citation, Course, LearningPath, LearningPathItem, LearningActivity, ProgressRecord); API_INTEGRATION_SPEC §2; DECISIONS DEC-001 to DEC-056; `phase-c-plan.md`, `phase-c-learning-experience-proposal.md`; `data/processed/*` and `DATASET_VALIDATION_REPORT.md`; all backend routes and models; frontend routes |
| **Related** | [phase-c-plan.md](phase-c-plan.md) · [phase-c-learning-experience-proposal.md](phase-c-learning-experience-proposal.md) |

---

## 1. Current state

### Implemented
| Area | What exists |
|---|---|
| Identity | Email + password login (Argon2id), hashed server-side sessions, HMAC CSRF, lockout, logout, notice acknowledgement, job-role selection, 8 access roles in `user_access_roles`, 8 synthetic accounts |
| Competency | Frameworks, clusters, competencies, levels (with descriptions for `demo-2`), approved role mappings, deterministic `score-v1`, evidence ledger, estimates, band-gated gaps |
| Assessment | Published `pre` assessments, key-free delivery, answer save, submit, results; `demo-2` provides 3 roles × 20 scenario items |
| Catalogue | Courses with difficulty and objectives, approved competency mappings, `rec-v1` recommendations, catalogue and course detail APIs |
| Frontend (learner) | Login, onboarding, dashboard, competency profile, gap analysis, assessment, result, catalogue, course detail |
| Demo operations | Versioned seed packs, demo reset, e2e learner creation, launcher |

### Missing (relevant to Phase 4)
| Area | Gap |
|---|---|
| Accounts | No registration, no registration ID, no password change/reset, no profile page, no admin user management |
| Authorisation | Only a coarse "can learn" role guard; no admin policy layer implementing the SECURITY §4 matrix |
| Learning | No modules, lessons, enrolment, progress, learning path (course detail stops at "Lessons are not available yet") |
| Content workflow | No authoring, review tasks, approvals, source references, course lifecycle, assessment publishing API |
| Analytics | No aggregated department or training-need views |
| AI | No interfaces (correct for now) |

### Source material in the repository (M10 findings)
| Dataset | Records | Licence / review | Usable how |
|---|---|---|---|
| `documents.json` (NSSTA, MoSPI, DoPT) | 22 (19 PDFs, 3 links) | Licence `MACHINE_OBSERVED` / `UNVERIFIED_SECONDHAND`; DoPT policy forbids reproduction without permission; `learner_visible=false` everywhere | **Reference metadata only** (title, publisher, URL, retrieval date, SHA-256) for admin source libraries and question/course source references. Text is not reproduced. Not shown to learners |
| `training_programmes.json` (NSSTA calendar) | 99 imported as `nssta_programme_listing` courses | `unreviewed`, dates unknown, "Tentative" | Visible to admins as "awaiting source review"; **publishing blocked** until licence and review are verified |
| `competency_framework.json` (CSCD) | 25 names/structure | Definitions restricted | Admin read-only framework; no definitions displayed |
| `topics.json` | 23 | `ASSUMED` | Admin filter suggestions only |

Conclusion: nothing collected can be published to learners in this phase. Synthetic `demo-2` content remains the learner-visible content, labelled once at environment level.

---

## 2. Conflicts with existing decisions and how this plan handles them

| # | Brief asks for | Existing rule | Handling in this plan |
|---|---|---|---|
| K-1 | Learner sign-up (`/register`) | MVP-01: "No self-registration" | **Assumption A-1:** self-registration behind `LEARNER_SELF_REGISTRATION_ENABLED`, default **on only in `local`/`ci`**, refused elsewhere; learner role only; administrators are always provisioned. Needs your approval before any other environment (D4-1) |
| K-2 | "Avoid displaying DEMO repeatedly" | DEC-045: DEMO badges and banner | Superseded in part: one environment banner plus page-level notices (catalogue, assessment); `is_demo` stays in every API payload; admin screens show content origin explicitly (DEC recorded) |
| K-3 | Department skill-gap heatmap, training needs (S2, S3) | Aggregates are P1 and need minimum group-size suppression (SECURITY §12, §15.6) | **Assumption A-3:** implemented as admin-only aggregates with suppression below 5 learners per cell (configurable), no individual data, synthetic cohort only; needs your approval as a P1 pull-forward (D4-3) |
| K-4 | Before-vs-after tracking (S1) | Reassessment is P1 and still undecided (DEC-056 D-2) | **Not implemented.** No reassessment behaviour is added |
| K-5 | Learning path uses difficulty and prerequisites | DEC-051: difficulty never affects `rec-v1` ranking | `rec-v1` unchanged. A separate documented rule `path-v1` orders *within* a gap by prerequisites then difficulty (DEC recorded) |
| K-6 | Question source metadata / citations | Citation entity needs Documents and chunks (Phase 5) | Interim `question_source_references` pointing at `source_records` or a declared synthetic origin; never presented as verified citations (DEC recorded) |
| K-7 | Admin approval workflow | MVP-16: ReviewTask/Approval; self-approval blocked when two reviewers required | Implement `review_tasks` and `approvals` as specified; **assumption A-5:** single reviewer, and authors may not approve their own work (D4-5) |
| K-8 | Password reset | SECURITY §3: administrator-issued one-time set-password token; no email provider | One-time token shown once to the administrator; learner sets a password at `/set-password`; all sessions revoked |
| K-9 | Retire arithmetic content (implied by "no longer feel like a simple arithmetic quiz") | DEC-056 D-4 unanswered | **Assumption A-6:** `demo-2` v2 deactivates the `demo-1` job role and courses for new selection; existing accounts keep their data; reversible (D4-6) |

---

## 3. MoSCoW scope for this phase

| Priority | Item | Phase | Status in plan |
|---|---|---|---|
| **Must** | M1 Role-based entry (Learner / Administration), registration (A-1), profile, password change, admin-issued reset, logout | 4A | Implement |
| **Must** | M2 PostgreSQL user records with registration ID, department, status, timestamps | 4A | Implement |
| **Must** | M3 Role-based competency structure; admin management of job roles and requirements | 4A/4C | Implement |
| **Must** | M4 Assessment engine: question lifecycle, source metadata, publishing guards, versions (assessment `version_label`), sections derived by competency | 4C | Implement |
| **Must** | M5 Transparent gap engine and explanations | 4D | Implemented in C; extend explanations and admin aggregates |
| **Must** | M6 Personalised learning path (`path-v1`) | 4B | Implement |
| **Must** | M7 Catalogue: prerequisites, modules, lessons, completion criteria, content origin, progress filters | 4B | Implement |
| **Must** | M8 Lessons, player, progress, resume, completion (approved proposal, amended below) | 4B | Implement |
| **Must** | M9 Admin content workflow: questions, courses, review, publish, audit | 4C | Implement |
| **Must** | M10 Source/content import strategy; reference-only source library | 4C | Implement (documents import + strategy doc) |
| **Should** | S2 Department skill-gap heatmap (suppressed aggregates) | 4D | Implement if Musts are stable (A-3) |
| **Should** | S3 Training-need analysis | 4D | Implement if Musts are stable (A-3) |
| **Should** | S5 Admin dashboard with actionable metrics | 4A/4D | Implement |
| **Should** | S4 Recommendation feedback (save, dismiss with reason) | 4D | Implement if time allows |
| **Should** | S1 Before-vs-after tracking | - | **Deferred** (reassessment not approved) |
| **Could** | AI quizzes, tutor, RAG, AI explanations, Gemini/OpenAI, adaptive testing, graphs, notifications, gamification, chatbot, voice | - | Not started; only local interfaces (§9) |
| **Won't (yet)** | Government SSO, HR/employee data, real iGOT, appraisal/promotion/certification, real AI keys, sending learner data to AI providers | - | Excluded |

---

## 4. Database changes (each migration is reversible)

### `0006` - accounts (4A)
| Change | Detail |
|---|---|
| `users.registration_id` | `citext` null; partial unique `(organization_id, registration_id) WHERE registration_id IS NOT NULL`; CHECK `^[A-Za-z0-9][A-Za-z0-9-/]{2,39}$`. Existing synthetic users get `DEMO-0001`.. via seed |
| `users.must_change_password` | boolean default false |
| `password_reset_tokens` | `id`, TS, `user_id` → users, `token_hash` (sha256, unique), `issued_by` → users, `expires_at`, `used_at`, `created_at`; index `(user_id)`; tokens single-use, 24 h |
| Departments | Data only: synthetic departments in the demo pack |
| Rollback | Drop table and columns; no existing data depends on them |

### `0007` - learning experience (4B), from the approved proposal with amendments
| Table | Key columns and constraints |
|---|---|
| `courses` (alter) | `content_origin` (`synthetic`, `official_source`, `provider`; default `synthetic` for internal, `official_source` for listings), `completion_criteria` text, `published_at`, `published_by`, `lifecycle_status` (`draft`, `in_review`, `approved`, `rejected`, `published`, `archived`). Backfill: existing approved+active → `published`; NSSTA listings → `draft`. Learner visibility becomes `lifecycle_status='published'` |
| `course_prerequisites` | `course_id`, `prerequisite_course_id`, unique pair, CHECK not self |
| `course_modules` | `course_id`, `position` (unique per course), `title`, `summary`, `status` |
| `lessons` | `module_id`, `position` (unique per module), `title`, `lesson_type` (`reading`, `worked_example`, `practice_check`), `estimated_minutes`, `content_kind` (`inline_markdown`, `learning_material`), `body_markdown`, `learning_material_id` (no FK until Phase 5), `status`; CHECK body present for `inline_markdown` |
| `progress_records` | As DATA_MODEL: `user_id`, `target_type` (`course`, `lesson`, `learning_path_item`), `target_id`, `title_snapshot`, `status`, `status_source`, `started_at`, `completed_at`, **`resume_lesson_id`** (amendment, courses only); unique `(user_id, target_type, target_id)`; index `(user_id, status)` |
| `learning_activities` | Append-only (trigger): `user_id`, `activity_type` (`course_started`, `lesson_opened`, `lesson_completed`, `course_completed`, `path_generated`), `target_type`, `target_id`, `metadata` jsonb (ids and counts only), `occurred_at` |
| `learning_paths` | As DATA_MODEL; partial unique active path per user |
| `learning_path_items` | As DATA_MODEL; item types `course`, `no_content_placeholder` |
| Rollback | Drop new tables; drop course columns (lifecycle backfill is derivable from review/status) |

### `0008` - content workflow (4C)
| Change | Detail |
|---|---|
| `questions.status` | CHECK gains `draft` and `archived` |
| `question_source_references` | `question_version_id`, `source_kind` (`source_record`, `synthetic`, `external_reference`), `source_record_id` → source_records (null unless `source_record`), `title`, `publisher`, `url`, `retrieved_on`, `locator` (page/section), `note`; append-only with the version |
| `review_tasks`, `approvals` | As DATA_MODEL; task types `question_version_review`, `course_review` |
| `assessments.version_label` | text default `v1` |
| Source records | Data: import `documents.json` (22) as reference-only `source_records` |
| Rollback | Drop tables/columns; revert CHECK (questions in `draft`/`archived` become `retired`) |

Every table is tenant-scoped with `organization_id`, uses UUID keys, standard audit columns, and is documented in DATA_MODEL.md in the same change.

---

## 5. API changes (all `/api/v1`, problem+json, CSRF on state changes)

| Group | Endpoints |
|---|---|
| Auth | `POST /auth/register` (flagged), `POST /auth/password/change`, `POST /auth/password/set` (token), `GET /auth/registration-options` (departments, flag) |
| Me | `GET /me` gains `registration_id`, `department`, `must_change_password`, `is_admin`, `admin_capabilities`; `PATCH /me` (display name, designation, department); `GET /me/progress`; `GET /me/learning-path`; `POST /me/learning-path/regenerate`; `PUT /me/lessons/{id}/progress` |
| Learning | `GET /courses/{id}/outline`; `POST /courses/{id}/start`; `GET /lessons/{id}` |
| Admin users | `GET/POST /admin/users`, `GET/PATCH /admin/users/{id}`, `POST /admin/users/{id}/password-reset`, `GET /admin/departments` |
| Admin competency | `GET /admin/frameworks`, `GET/POST/PATCH /admin/job-roles`, `PUT /admin/job-roles/{id}/requirements` |
| Admin content | `GET/POST /admin/questions`, `GET/PATCH /admin/questions/{id}`, `POST /admin/questions/{id}/submit`, `GET /admin/review-tasks`, `POST /admin/review-tasks/{id}/decision`, `GET/POST /admin/courses`, `GET/PATCH /admin/courses/{id}`, `POST /admin/courses/{id}/submit`, `POST /admin/courses/{id}/publish`, `POST /admin/courses/{id}/archive`, `GET /admin/assessments`, `POST /admin/assessments/{id}/publish`, `GET /admin/sources` |
| Admin insight | `GET /admin/overview`, `GET /admin/skill-gaps`, `GET /admin/training-needs`, `GET /admin/audit` |

Existing learner endpoints keep their shapes; additions are optional fields.

## 6. Frontend routes

| Learner | Admin |
|---|---|
| `/login` (Learner / Administration), `/register`, `/set-password`, `/get-started`, `/`, `/profile`, `/competencies`, `/competencies/gaps`, `/assessment`, `/assessment/attempts/:id`, `/attempts/:id/result`, `/me/attempts`, `/learning-path`, `/courses`, `/courses/:id`, `/courses/:id/learn`, `/courses/:id/lessons/:lessonId` | `/admin`, `/admin/users`, `/admin/roles`, `/admin/competencies`, `/admin/assessments`, `/admin/questions`, `/admin/questions/new`, `/admin/questions/:id`, `/admin/review`, `/admin/courses`, `/admin/courses/new`, `/admin/courses/:id`, `/admin/skill-gaps`, `/admin/training-needs`, `/admin/audit` |

Admin routes appear only for users holding an admin capability; each route checks the capability again on the server. A route is added only when its backing API exists.

## 7. Security implications

| Topic | Control |
|---|---|
| Admin access | New `identity/policy.py` maps capabilities to roles exactly as SECURITY §4; every admin endpoint depends on a capability; learners get 403 |
| Registration | Flag-gated, learner role only, generic duplicate messages that do not confirm account existence beyond "email or registration ID already in use" (**trade-off noted**: registration inherently reveals use; acceptable for local demo, re-evaluated before any pilot) |
| Passwords | Argon2id, min length 12, change requires current password, reset tokens hashed and single-use, all sessions revoked on change/reset |
| Separation of duties | Authors cannot approve their own questions or courses; auditors read-only; `platform_admin` does not see learner competency data |
| Privacy | Aggregates suppress groups below 5; no individual rows in admin insight views; audit of data-access views |
| Content safety | Lesson Markdown rendered without raw HTML; links restricted to http(s) |
| Logging | No passwords, tokens, registration IDs in logs (redaction list extended) |

## 8. Migration risks

| Risk | Mitigation |
|---|---|
| Changing learner visibility from `review_status` to `lifecycle_status` could hide or expose courses | Backfill in the migration, tests asserting the same 15 visible courses before and after, NSSTA listings stay hidden |
| Question status CHECK change on existing rows | Only adds values; downgrade maps new values to `retired` |
| Large synthetic lesson content in a pack | Pack `demo-2` version 2 is additive; idempotency tests |
| Existing learners' results after deactivating `demo-1` | Gaps use `job_role_in_org` without active filter, so existing data keeps working; tested |

## 9. AI boundary

Local interfaces only (`backend/app/modules/ai/interfaces.py`): `CompetencyInterpreter`, `RecommendationExplainer`, `LearningContentRetriever`, `QuestionGenerator`, `QuestionValidator`, `LearningTutor`, with deterministic implementations (template explanations, keyword retrieval over published lessons, validators for structure). No network calls, no keys. External-provider analysis in the final report.

## 10. Testing strategy

| Layer | Additions |
|---|---|
| Backend | Registration and password flows; policy matrix tests per capability × role; learner cannot reach any `/admin` endpoint; learner isolation for progress and paths; lesson progress state machine; path determinism and completed-item carry-over; review workflow state machine including self-approval block; publishing guards (missing source, unapproved items, minimum items per competency); suppression below group size; audit assertions |
| Frontend | Component tests for login modes, registration validation, profile, learning path, player, admin tables and forms |
| Browser | Playwright desktop + 360 px: register → onboard → assess → path → complete lessons → progress; admin: user provisioning, question author → review by second admin → publish; axe on every new route; keyboard checks on player and forms; horizontal-scroll and console-error checks |
| Checks | Log grep for passwords/cookies; migration upgrade/downgrade/drift |

## 11. Decisions required from you

| ID | Decision | What I will do until you answer |
|---|---|---|
| D4-1 | Allow learner self-registration outside local/ci? | Enabled only in `local`/`ci` (A-1) |
| D4-2 | Registration ID format and uniqueness scope | 3-40 characters, letters/digits/`-`/`/`, unique per organisation |
| D4-3 | Pull forward department heatmap and training needs (P1) with suppression below 5 | Implement admin-only with suppression (A-3) |
| D4-4 | Reassessment and before-vs-after (still DEC-056 D-2) | Not implemented |
| D4-5 | Review policy: one reviewer, author cannot approve own content | Implement (A-5) |
| D4-6 | Deactivate `demo-1` arithmetic role and courses | Implement reversibly (A-6) |
| D4-7 | Add `react-markdown` + `remark-gfm` (MIT) to render lesson Markdown safely | Add, recorded in TECH_STACK |
| D4-8 | Mention "Smart India Hackathon" in the UI | No mention |
| D4-9 | External AI provider (DEC-005) | No integration; interfaces and local implementations only |
