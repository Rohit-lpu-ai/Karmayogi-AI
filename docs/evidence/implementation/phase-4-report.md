# Phase 4 - end-to-end platform: final report (2026-09-15)

Plan: [phase-4-plan.md](phase-4-plan.md). Decisions DEC-057 to DEC-062. Status tables: IMPLEMENTATION_STATUS.md sections 1f-1i. Nothing is committed.

This is a local development build with synthetic data. It is not production-ready, and no content in it is official.

## 1. Success criterion walk-through

| Journey | Result | Evidence |
|---|---|---|
| A new learner registers, signs in, understands their role, assesses, sees gaps, gets learning, opens a course, completes lessons, tracks progress | Works end to end | `accounts-admin.spec.ts` (register, onboarding), `learning.spec.ts` (baseline -> path -> every lesson -> completion -> catalogue filter -> dashboard -> history) |
| An administrator manages users | Invite with one-time link, roles, status, password links, departments | `accounts-admin.spec.ts`, `test_accounts_admin_api.py` |
| ... manages content | Questions with versions and sources; courses with modules, lessons, links; review by another person; publish and unpublish | `content-admin.spec.ts`, `test_content_admin_api.py` |
| ... competency requirements | **View only** (frameworks, competencies, job-role levels, approved-question coverage). Editing requirements is not built | `/admin/competencies` |
| ... reviews | Review queue with self-approval block and reasons | `content-admin.spec.ts` |
| ... aggregated training needs | Skill-gap heatmap and ranked training needs, suppressed below 5 learners | `insight.spec.ts`, `test_insight_api.py` |

## 2. Features

### Implemented (MoSCoW Must and Should, plan section 3)
- **4A Foundation:** sign-in with Learner / Administration modes; learner self-registration (local/ci only); administrator-provisioned accounts with one-time account-setup and password-reset links (fragment tokens, hashed, single-use, expiring); profile with password change; capability policy on every admin API; separate admin navigation and route guards; users, roles and permissions, departments.
- **4B Learning core:** modules and lessons; lesson player with contents drawer; self-reported completion, resume, course completion; learning path `path-v1`; assessment history; progress on catalogue, course detail and dashboard; demo reset clears learning progress.
- **4C Content and administration:** question bank and authoring with immutable versions and source metadata; review workflow (`single-reviewer-v1`, author cannot decide); course administration with publishing guards; competency structure view; assessment coverage and quality checks; audit trail; 22 source documents as reference-only records.
- **4D Intelligence:** admin overview learning summary, department skill-gap heatmap, training needs; synthetic cohort built through the real pipeline; local AI interfaces with a rule-based question validator in the UI.

### Deferred or not built
| Item | Reason |
|---|---|
| Reassessment and before/after comparison | Still P1 and undecided (DEC-056 D-2, plan K-4) |
| Editing job-role requirements and frameworks in the UI | Needs a decision on requirement versioning; view only |
| Assembling and versioning assessments in the UI | Deferred; coverage and guards are shown |
| Retiring the `demo-1` arithmetic role and courses (A-6) | Awaits product owner (DEC-056 D-4) |
| Registration outside local/ci | Awaits D4-1 |
| Two-reviewer approval | Single reviewer under A-5 (D4-5) |
| Email delivery of account links | No email provider; links are shown once to the administrator |
| External AI, RAG, tutor | Out of scope; analysis in [phase-4-ai-boundary.md](phase-4-ai-boundary.md) |
| Manual screen-reader review | Needs a person (DEC-056 D-6) |

## 3. Migrations (all reversible; upgrade/downgrade/upgrade run for each)

| Revision | Content |
|---|---|
| 0006 | `users.registration_id`, `users.must_change_password`, `password_reset_tokens` |
| 0007 | `course_modules`, `lessons`, `course_prerequisites`, `progress_records`, `learning_activities` (append-only), `learning_paths`, `learning_path_items`; `courses.content_origin`, `courses.completion_criteria` |
| 0008 | `questions.status` gains `draft`; `question_source_references` (append-only); `review_tasks`; `approvals` (append-only); `courses.published_at`, `published_by` |

Seed: packs `demo-3` (48 synthetic lessons for the 12 demo-2 courses, prerequisites, completion criteria) and `demo-4` (38-learner synthetic cohort); canonical import adds 22 document source records.

## 4. API changes
Documented in API_INTEGRATION_SPEC.md sections 2.14 (accounts and administration), 2.15 (learning), 2.16 (content administration), 2.17 (insight). All additive; no existing response field was removed.

## 5. Routes

- **Learner:** `/login`, `/register`, `/set-password`, `/get-started`, `/`, `/profile`, `/competencies`, `/competencies/gaps`, `/assessment`, `/assessment/attempts/:id`, `/attempts/:id/result`, `/me/attempts`, `/learning-path`, `/courses`, `/courses/:id`, `/courses/:id/learn`, `/courses/:id/lessons/:lessonId`.
- **Admin:** `/admin`, `/admin/users`, `/admin/roles`, `/admin/review`, `/admin/questions`, `/admin/questions/new`, `/admin/questions/:id`, `/admin/courses`, `/admin/courses/new`, `/admin/courses/:id`, `/admin/competencies`, `/admin/assessments`, `/admin/skill-gaps`, `/admin/training-needs`, `/admin/audit`.

Every route has working content; none is a placeholder.

## 6. Security and privacy
- Server-side capability checks on every admin endpoint; department administrators limited to their department and learner-only accounts; only a platform administrator manages platform administrators; no self role or status changes.
- Passwords Argon2id; set-password tokens SHA-256 only, single-use, expiring, in URL fragments; sessions revoked on password set, change (others), deactivation and role change.
- No password hashes, token hashes or answer keys in API responses to learners; admin question detail shows answers to authors and reviewers only.
- Aggregates only in insight, minimum group size 5, department scoping, no personal data (tested).
- CSRF on every state change; request bodies reject unknown fields.
- Log scan after the full run: 0 occurrences of the demo password, cookies, set-password tokens or hashes. `registration_id` added to log redaction.
- Content honesty: synthetic content labelled at environment and page level; external references shown as "author-provided, not verified"; licence-restricted framework definitions never shown or used for authoring; nothing published without human approval.

## 7. Tests and checks (final run)

| Check | Result |
|---|---|
| Backend `pytest -q` | 289 passed |
| `alembic check` | no drift at `0008` |
| Frontend typecheck, Vitest | clean; 77 passed |
| Build, audit | main JS 453 kB (130 kB gzip); 0 vulnerabilities |
| Playwright + axe, 1440 px and 360 px | 26 passed; 0 serious/critical violations; no horizontal scroll; no unexpected errors |
| Live API smoke through the proxy | passes |

Bugs found by these checks and fixed: unique-constraint race when opening and completing a lesson together; running app missing the model registry (500 on first question save); sign-out passing the previous user's page to the next person; login mode lost on remount; absolutely positioned screen-reader text widening pages; toasts covering form actions; single-line code in lessons not keyboard-scrollable at 360 px.

## 8. Screenshots
`docs/evidence/implementation/phase-4a/`, `phase-4b/`, `phase-4c/`, `phase-4d/` (the 4d folder holds the final full run of every journey on both viewports).

## 9. Known limitations
- Local database contains test artefacts from browser journeys: `e2e-*` learners (some registered to the demo department), approved test questions, unpublished "Units and footnotes clinic ..." courses.
- Learning completion is self-reported and never changes estimates; there is no reassessment.
- Insight on the local database includes about 150 test learners without a department ("No department recorded").
- The admin overview imports insight helpers, so a small part of insight code is in the admin overview chunk.
- Vite's development server stopped twice in the background during long runs; restarting it fixed the runs.

## 10. Decisions needed from the product owner
D4-1 registration outside local/ci; D4-3 insight pull-forward and group size; D4-5 single reviewer; D4-6 retire demo-1 content; DEC-056 D-2 reassessment; and whether to plan any external AI capability (see the AI boundary analysis).

## 11. Suggested next phase
1. Decide reassessment (unlocks before/after tracking and makes learning completion meaningful for estimates).
2. Assessment assembly and versioning from approved questions, with a second reviewer for publication.
3. Requirement and framework editing with versioned mappings and review.
4. Email or SSO for account provisioning in a pilot environment.
5. Only after a recorded decision: embeddings for lesson search (pgvector, local) as the first AI capability, then a grounded tutor.
