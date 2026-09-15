# Product Upgrade - Baseline Audit (Phase 0)

| Field | Value |
|---|---|
| **Date** | 2026-09-15 |
| **Branch / HEAD** | `Diw` / `0b2f86d` (working tree clean except the untracked `start-dev.bat`) |
| **Purpose** | Record the verified state of vertical slice 1 before the product/UX upgrade, so every later phase can be compared against it |
| **Raw command output** | [product-upgrade-baseline/](product-upgrade-baseline/) |
| **Related** | [../../IMPLEMENTATION_STATUS.md](../../IMPLEMENTATION_STATUS.md) · [../../VERTICAL_SLICE_1_PLAN.md](../../VERTICAL_SLICE_1_PLAN.md) · [../../UI_UX_SPEC.md](../../UI_UX_SPEC.md) · [../../MVP_SCOPE.md](../../MVP_SCOPE.md) · [../../DECISIONS.md](../../DECISIONS.md) |

No application code, schema or data model was changed during this audit.

---

## 1. Verification performed

| # | Check | Command | Result | Evidence |
|---|---|---|---|---|
| 1 | Database container | `docker inspect -f "{{.State.Health.Status}}" platform-local-db-1` | `healthy` (pgvector/pgvector:pg17, 127.0.0.1:5433) | — |
| 2 | Backend tests (unit + PostgreSQL) | `cd backend && .venv/Scripts/python -m pytest -q --color=no` | **167 passed**, 0 failed, 2 deprecation warnings (Starlette `httpx` test client, anyio alias) | `01-backend-pytest.txt` |
| 3 | Migrations | `cd backend && .venv/Scripts/alembic current && .venv/Scripts/alembic check` | `0003 (head)`; "No new upgrade operations detected" (models = migrations) | `02-alembic.txt` |
| 4 | Phase 1 dataset/mock tests | `python -m unittest discover -s tests -t .` | **35 passed** | `03-phase1-unittest.txt` |
| 5 | Frontend type-check | `cd frontend && npm run typecheck` | 0 errors | `04-frontend.txt` |
| 6 | Frontend tests | `npm test` | **12 passed** (2 files) | `04-frontend.txt` |
| 7 | Frontend build | `npm run build` | OK - JS 202.89 kB (65.56 kB gzip), CSS 4.20 kB | `04-frontend.txt` |
| 8 | Dependency audit | `npm audit` | 0 vulnerabilities | `04-frontend.txt` |
| 9 | Live API journey | `uvicorn --factory app.main:app_factory --port 8001` + `SMOKE_BASE_URL=http://127.0.0.1:8001 .venv/Scripts/python scripts/smoke_vertical_slice.py department-admin01@example.invalid` | Exit 0. health 200, ready 200, 401 unauthenticated, login 200, CSRF-missing 403, notice 200, role 200, attempt 201, submit 200 (0.35714, baseline), gaps 2×`gap`, 3 recommendations (all `is_demo`), resubmit 409, logout 204, 401 after logout | `05-live-smoke.txt` |
| 10 | Seeded row counts | SQL counts through the app engine | users 8, job_roles 1, competencies 27 (25 CSCD + 2 DEMO), courses 102 (99 NSSTA listings + 3 DEMO), course_competencies 4, questions 10, assessments 1, attempts 4 (after #9), audit_logs 22+ | this document §4 |
| 11 | Browser walkthrough / screenshots | Claude-in-Chrome | **Not performed**: the browser extension was not connected. Also, entering the demo password into the login form is outside what the agent may do, so signed-in screens could not be captured by the agent in any case. UI review below is from source code, component tests and live API payloads | — |
| 12 | Accessibility automation (axe) | — | **Not performed**: no axe/Playwright tooling exists | — |

**Side effect of check 9:** the synthetic account `department-admin01@example.invalid` now has a scored baseline attempt in the local database. Unused synthetic accounts that can still take the baseline: `org-admin01`, `competency-admin01` (see risk R-06).

## 2. What currently works

| Capability | Evidence |
|---|---|
| Server-side sessions (Argon2id, hashed tokens, idle/absolute expiry), HMAC CSRF, account lockout, logout | `identity/{security,service,dependencies,api}.py`; `tests/db/test_vertical_slice_api.py`; smoke #9 |
| Problem+json errors with correlation IDs; security headers; redacting JSON logs | `core/{errors,middleware,logging}.py`; `tests/unit/test_http_foundation.py`, `test_logging.py` |
| Privacy/AI-use notice acknowledgement (draft notice), job-role selection with audit | `POST /me/notice-acknowledgements`, `PUT /me/job-role` |
| Role requirements for a job role | `GET /job-roles/{id}/competencies` |
| Baseline assessment: key-free delivery, seed-reproducible order, answer save, transactional submit, duplicate-submit 409, result with explanations | `assessment/{service,api}.py`; `tests/unit/test_security_and_delivery.py`; journey tests |
| Deterministic `score-v1` estimates with evidence bands, explanation blocks and limitations | `competency/scoring.py`; `tests/unit/test_scoring.py` |
| Band-gated gap classification | `scoring.classify_gap`; `GET /me/competency-gaps` |
| Deterministic `rec-v1` recommendations with reason objects, approved mappings only | `recommendation/rules.py`; `tests/unit/test_recommendation_rules.py` |
| DEMO labelling end to end (`is_demo`, DEMO banner/badges, seed refused outside local/ci) | `core/demo.py`, `seed/demo_content.py`, frontend `States.tsx`, `AppShell.tsx` |
| Frontend journey: login → get started → dashboard → assessment → result, with per-card loading/empty/error states | `frontend/src/pages/*`; `pages.test.tsx` |
| One-click local launcher | `start-dev.bat` (untracked; verified 2026-09-15: DB healthy, `/healthz` 200, proxy 401 on `/auth/session` when signed out) |

## 3. What currently fails or is fragile

No automated check fails. The following are defects or operational problems found during the audit:

| # | Finding | Impact |
|---|---|---|
| F-01 | A stray `uvicorn app.main:app --reload` process (global Python, not `.venv`, and not the `--factory` entry point) held port 8000 in `Bound` state without serving. The Vite proxy then returns `ECONNREFUSED` - the exact error seen before the launcher existed | Confusing "backend not running" failures. `start-dev.bat` only detects `LISTENING` sockets, so it would try to start and fail to bind in this state |
| F-02 | Each synthetic account can take the baseline only once (`ASSESSMENT_ALREADY_COMPLETED`, DEC-047 #9) and there is no local reset command | The demo is one-shot per account; 5 of 6 learning-capable accounts are already used |
| F-03 | The demo content seed is idempotent **as a unit** (it returns immediately if `DEMO-FUNCTIONAL` exists) | Richer synthetic content cannot be added by editing the existing seed; existing databases would silently not receive it |
| F-04 | Recommendation cards link nowhere: there is no course list, course detail or `GET /courses` endpoint | Journey stops at "Recommended learning" |
| F-05 | Dashboard exposes internal rule strings (`Rule: required - estimated level…`, method versions, `iGOT: not connected. No iGOT integration: mock source not enabled in this slice`) to learners | Reads as a developer tool, not a product |
| F-06 | Assessment renders all 10 questions on one page; no navigator, no per-question progress, no intro screen; the attempt state lives only in component state (reload returns to the start screen, although the server resumes the attempt) | Weak assessment experience; resume works only via "Resume assessment" |
| F-07 | Result page shows `/100` scores and a raw table; no required-vs-estimated comparison, no next steps, no "How was this calculated?" disclosure | Result lacks meaning for a learner |
| F-08 | Header brand is "Competency Learning Platform (working name)"; no navigation beyond Dashboard/Assessment; no competency profile, gaps, progress or courses pages | Information architecture is two screens deep |
| F-09 | `useApi` has no request de-duplication or caching; the dashboard makes 3 independent requests and recomputes gaps twice on the server (gaps + recommendations) | Acceptable at demo scale; noted for the `/me/dashboard` aggregate |
| F-10 | `IMPLEMENTATION_STATUS.md` header still says everything after `35d10a9` is uncommitted; vertical slice 1 was committed as `0b2f86d` | Stale documentation |
| F-11 | Starlette deprecation warnings in the test run | No impact today; will break on a future Starlette/FastAPI upgrade |

## 4. Inventory

### 4.1 API routes (all implemented, all under test)

| Method | Path | Auth | Module |
|---|---|---|---|
| GET | `/healthz` | public | platform |
| GET | `/readyz` | public (DB check) | platform |
| POST | `/api/v1/auth/login` | public | identity |
| POST | `/api/v1/auth/logout` | session + CSRF | identity |
| GET | `/api/v1/auth/session` | session | identity |
| GET | `/api/v1/me` | session | identity |
| POST | `/api/v1/me/notice-acknowledgements` | session + CSRF | identity |
| PUT | `/api/v1/me/job-role` | session + CSRF | identity |
| GET | `/api/v1/job-roles` | session | competency |
| GET | `/api/v1/job-roles/{id}/competencies` | session | competency |
| GET | `/api/v1/me/competency-profile` | learning role | competency |
| GET | `/api/v1/me/competency-gaps` | learning role | competency |
| GET | `/api/v1/assessments` | learning role | assessment |
| POST | `/api/v1/assessments/{id}/attempts` | learning role + CSRF | assessment |
| GET | `/api/v1/attempts/{id}` | owner | assessment |
| PUT | `/api/v1/attempts/{id}/answers/{question_version_id}` | owner + CSRF | assessment |
| POST | `/api/v1/attempts/{id}/submit` | owner + CSRF | assessment |
| GET | `/api/v1/attempts/{id}/result` | owner | assessment |
| GET | `/api/v1/me/recommendations` | learning role | recommendation |

Learning roles (`SELF_LEARNING_ROLES`): learner, trainer, department_admin, org_admin, competency_admin, training_manager. Auditor and platform_admin cannot take assessments.

Specified in API_INTEGRATION_SPEC/MVP_SCOPE but **missing**: `/me/dashboard`, `/me/attempts`, `/courses` (list/detail), `/recommendations/{id}/feedback`, `/me/learning-path` (+ regenerate, item PATCH), `/learning-activities`, `/me/progress` (+ history).

### 4.2 Database entities (migrations `0001`-`0003`, 28 tables)

| Module | Tables |
|---|---|
| platform | `topics` |
| organization | `organizations`, `departments`, `job_roles` |
| identity | `users`, `user_access_roles`, `sessions`, `notice_acknowledgements` |
| competency | `competency_frameworks`, `competency_clusters`, `competencies`, `competency_levels`, `role_competencies`, `competency_evidence` (append-only), `user_competencies` |
| assessment | `questions`, `question_versions`, `question_options`, `assessments`, `assessment_questions`, `assessment_attempts`, `attempt_questions`, `answers` |
| recommendation | `courses`, `course_topics`, `course_competencies` |
| content | `source_records` |
| governance | `audit_logs` (append-only) |

`courses` columns: course_type, title, description, provider_organisation, programme_family, cohort, target_group, duration_days, batch sizes, venue, fiscal_year, schedule_status, external_ref, external_url, source_record_id, data_status, review_status, status. **No** difficulty, learning objectives, modules, lessons, enrolment or progress entities exist. No vector columns (DEC-038). All three migrations define `downgrade()`.

### 4.3 Frontend

| Route | Page | Data |
|---|---|---|
| `/login` | `LoginPage` | `POST /auth/login` |
| `/get-started` | `OnboardingPage` (notice → job role, 2 stacked cards) | `/me`, `/job-roles`, `/job-roles/{id}/competencies` |
| `/` | `DashboardPage` (gaps table, recommendations list, explanation disclosures) | `/me/competency-gaps`, `/me/recommendations`, `/me/competency-profile` |
| `/assessment` | `AssessmentPage` (list → all questions on one page → inline confirm) | `/assessments`, attempts endpoints |
| `/attempts/:id/result` | `ResultPage` (score table + per-question feedback) | `/attempts/{id}/result` |

Components: `AppShell` (skip link, DEMO banner, header nav), `States.tsx` (`DemoBadge`, `StatusBadge`, `LoadingState`, `EmptyState`, `ErrorState`). Styling: one 99-line `styles.css` with basic tokens (DEC-048). Stack: React 18.3, TypeScript 5.9, Vite 8.3, React Router 7, Vitest 5, Testing Library. No Tailwind, shadcn/ui, icon set, chart library, i18n catalogue, TanStack Query, Playwright or axe.

### 4.4 Tests

| Suite | Files | Count |
|---|---|---|
| Backend unit | `test_config`, `test_http_foundation`, `test_logging`, `test_scoring`, `test_recommendation_rules`, `test_security_and_delivery` | part of 167 |
| Backend DB | `test_migrations` (upgrade/downgrade/drift), `test_reference_schema` (constraints, triggers), `test_seed`, `test_vertical_slice_api` (journey, validation, authorisation, CSRF, lockout, key leakage) | part of 167 |
| Phase 1 | `tests/test_canonical_datasets.py`, `tests/test_mock_igot_client.py` | 35 |
| Frontend | `api/client.test.ts` (5), `pages/pages.test.tsx` (7: routing, login error, dashboard labels and wording, per-card failure, key-free assessment, submit confirmation) | 12 |
| Live smoke | `backend/scripts/smoke_vertical_slice.py` | manual |
| Browser/E2E, accessibility, visual | — | **none** |

## 5. Current limitations

- **Content:** one DEMO job role, two DEMO competencies (both arithmetic), 10 arithmetic items, 3 DEMO courses without any learning content. 99 NSSTA listings and 25 CSCD competencies exist in the database but are unreviewed/restricted and correctly never shown.
- **Journey stops at recommendations:** no catalogue, course detail, learning experience, progress, learning path or assessment history.
- **One attempt per account**, no reassessment (P1) and no local reset.
- **No AI code at all:** no `LLMProvider`/`EmbeddingProvider` interfaces, no fake providers, no ingestion, retrieval or citations.
- **Recommendations are computed on read**, not persisted; no accept/dismiss feedback.
- **UI:** functional but minimal; tables for learner-facing data, developer strings visible, no design system beyond ~20 tokens, no icons, no charts, no mobile navigation pattern, not verified in a real browser.
- **Governance gaps unchanged:** DEC-001 (product name), DEC-005/006 (AI providers), DEC-013 (official framework), DEC-020 (thresholds), DEC-027 (legal notice) still open.

## 6. Scope and documentation conflicts with the upgrade brief

The repository's own rules ([AGENT_CONTEXT.md](../../AGENT_CONTEXT.md) rules 1-3, [MVP_SCOPE.md](../../MVP_SCOPE.md) §5) forbid implementing P1/P2 features or adding dependencies without a record. Checked against the upgrade brief:

| # | Brief asks for | Documentation says | Conflict? | Proposed handling |
|---|---|---|---|---|
| C-1 | Design system, AppShell, dashboard redesign, competency profile, gap analysis, assessment redesign, results | P0: MVP-F3, MVP-F4, MVP-19, S-03 to S-07 | No | Proceed |
| C-2 | Course catalogue with search/filters, course detail | P0: MVP-17, S-09 (filters by source, topic, competency) | Partly: **difficulty** is not a course attribute; "difficulty logic" in recommendation is P1 | Show and filter difficulty as a descriptive attribute only; never used in ranking. Needs a new column (migration) - **decision D-3** |
| C-3 | Course modules, lessons, learning player, mark lesson complete, resume | **Not specified anywhere.** Courses are catalogue entries; learning material is uploaded documents (MVP-09/11); progress is self-reported items (MVP-24) | **Yes** - new scope | Record DEC-049 "Synthetic in-app course content (local/ci only)", modelled so lessons become `LearningMaterial` references later. **Decision D-1** |
| C-4 | Learning progress, started/completed courses | P0: MVP-24 (`ProgressRecord`, `LearningActivity`), MVP-18 learning path | No | Implement against the specified entities, not ad-hoc tables |
| C-5 | Streaks, activity metrics | P1 (MVP-24 out-of-scope, GAM-*) | Yes - the brief itself says "only if real data exists" | Do not build |
| C-6 | Reassess later | P1 (J-12, ASM-012) | Yes - brief says "when supported" | Guidance text only; plus a **local-only demo reset** command (not a product feature) for F-02 |
| C-7 | Multiple job roles, competencies, courses, questions | DEC-045 allows one labelled DEMO set, local/ci only | Extension | New versioned demo pack (`demo-2`) added alongside `demo-1` (F-03); still arithmetic/generic methodology, never official |
| C-8 | Provider interfaces for LLM, embeddings, ingestion, retrieval, reranking, citations, generation, summarisation - local/mock only | P0 interfaces + fake providers (AI_SYSTEM_SPEC §1-2, rule 6, rule 30). Summaries and rerankers are P1 **features** | Partly | Build interfaces and fakes; do not expose summarisation or reranking in any route or screen |
| C-9 | Tailwind / shadcn/ui | TECH_STACK proposes them; DEC-048 deferred to Phase 8 | Decision | **Decision D-2** |
| C-10 | Playwright browser tests, axe | TECH_STACK §16 "proposed" | Needs admission record | Add at Phase 10 of the brief with a TECH_STACK/DECISIONS entry |
| C-11 | "Premium" branding | DEC-001 product name undecided; no official branding allowed | Decision | Neutral working name until DEC-001 is decided |

## 7. Risks

| # | Risk | Mitigation |
|---|---|---|
| R-01 | Polished UI makes synthetic content look official | Keep `is_demo` in every payload; persistent DEMO notice; "Synthetic - not an approved course" on every course surface; copy lint for prohibited terms (UI_UX_SPEC §10) |
| R-02 | Richer UI tempts invented metrics (hours, streaks, percentiles) | Only render fields that come from the API; no client-side derived "performance" numbers |
| R-03 | Scope creep into P1 (tutor, reassessment, gamification) | Scope table §6 is the gate; new scope needs a DEC record |
| R-04 | Adding Tailwind/shadcn rewrites every component at once | Migrate screen by screen behind the existing tests; keep page tests green at each step |
| R-05 | Schema growth for course content conflicts with DATA_MODEL (`LearningMaterial`, `ProgressRecord`) | Propose migration `0004` in writing first; align names with DATA_MODEL; reversible downgrade; drift test |
| R-06 | Demo accounts exhausted (F-02) | Local/ci-only `python -m app.seed demo-reset` that voids demo attempts with an audit record (evidence ledger stays append-only - void, never delete) |
| R-07 | Stale processes on port 8000 (F-01) | Launcher: detect any socket on 8000/5173, report the owning process, and refuse to start rather than fail silently |
| R-08 | No browser verification | Add Playwright smoke for J-01..J-05 before calling any screen done |
| R-09 | Starlette test-client deprecation | Pin or migrate before upgrading FastAPI |
| R-10 | Documentation drift (F-10) | Update IMPLEMENTATION_STATUS at the end of each phase |

## 8. Recommended implementation order

| Step | Content | Why this order |
|---|---|---|
| 0.5 Critical fixes | Launcher port-conflict detection (F-01); local demo reset (F-02); hide developer strings behind disclosures (F-05); fix stale status doc (F-10) | Unblocks repeatable demos; small and safe |
| 1 Design foundation | Tokens, typography, spacing, component library (decision D-2), AppShell with sidebar + mobile drawer, PageHeader, badges, states, dialog, toast | Every later screen depends on it |
| 2 Information architecture | Routes `/`, `/competencies`, `/competencies/gaps`, `/assessments`, `/courses`, `/courses/:id`, `/progress`; onboarding as a stepper | Gives the journey a spine before content grows |
| 3 Assessment + results redesign | Intro page, one-question-at-a-time with navigator, URL-addressable attempt (resume on reload), confirm dialog, result page with required-vs-estimated and "How was this calculated?" | Uses existing endpoints only; highest demo impact, lowest risk |
| 4 Dashboard + competency profile + gaps | `GET /me/dashboard` aggregate (MVP-19), `GET /me/attempts`; cards, level indicators, chart-with-table | Uses existing scoring; needs step 1-2 |
| 5 Richer synthetic data | `demo-2` pack: ~3 roles, ~8 competencies, ~40 items with explanations, ~12 courses | Makes steps 3-4 look real; needed before catalogue |
| 6 Course catalogue + detail | `GET /courses`, `GET /courses/{id}` (approved + displayable only), filters, reasons linked to gaps | MVP-17 P0 |
| 7 Learning experience + progress | Migration `0004` (after D-1/D-3): course modules/lessons as synthetic material, `ProgressRecord`/`LearningActivity`, learning player, `GET /me/progress`, learning path | Largest schema change; last among product features |
| 8 AI/RAG preparation | `ai/providers` interfaces + fake providers, contract tests, ingestion/retrieval/citation interfaces; no routes | Independent of UI; no external calls |
| 9 Official data integration plan | Source-by-source plan (authorisation, API, licence, privacy, update cadence, citation, failure, human review) | Documentation only |
| 10 Quality | Playwright + axe journeys, responsive checks at 360 px, keyboard/screen-reader notes, test additions per brief | Continuous, with a final pass |

## 9. Prioritised roadmap

### Critical fixes
1. Launcher detects occupied ports (any state) and names the process (F-01).
2. Local/ci-only demo reset for synthetic accounts, audited, void-not-delete (F-02).
3. Versioned demo pack mechanism so new synthetic content reaches existing databases (F-03).
4. Update stale `IMPLEMENTATION_STATUS.md` header (F-10).

### High-value UX improvements
1. Design system and component library (D-2) with focus, contrast and reduced-motion rules.
2. AppShell: sidebar navigation, mobile drawer, breadcrumbs, user menu, persistent but compact DEMO notice.
3. Onboarding stepper with purpose explanation and role requirement preview.
4. Assessment intro, one-question view, navigator, save status, resume by URL, confirmation dialog.
5. Result page: overall summary, per-competency required vs estimated, evidence strength, next steps, "How was this calculated?".
6. Dashboard: hero with next action, competency overview, top gaps, recommendations, recent assessment, progress (real data only).

### Course experience
1. Catalogue API and page (search, competency/difficulty/duration filters, sort, all states).
2. Course detail with objectives, structure, reason and related gap.
3. Synthetic lessons, learning player, mark complete, resume, completion (requires D-1, migration `0004`).
4. Progress page and learning path (MVP-18, MVP-24).

### Competency intelligence
1. Competency profile page (level indicators, evidence band, explanation, history via `/me/attempts`).
2. Gap analysis page with chart + table, strengths, insufficient-evidence section, linked learning.
3. `/me/dashboard` aggregate endpoint.
4. Interfaces for future explanation/path providers that default to the deterministic engine (rule 27: scores stay deterministic).

### Future AI/RAG preparation
1. `LLMProvider`, `EmbeddingProvider` interfaces with `Fake*` implementations and contract tests.
2. `DocumentIngestor`, `Retriever`, `Reranker` (interface only), `CitationVerifier`, `QuestionGenerator`, `ExplanationProvider` interfaces with local implementations.
3. Configuration defaults to fake providers; external providers refused without explicit settings (mirrors `IGOT_CLIENT_MODE`).

### Official data integration (later, controlled)
1. Integration plan document per source (NSSTA, MoSPI, CSCD/DoPT, iGOT, data.gov.in).
2. No scraping, no invented endpoints, no official branding, no approval claims until authorised.

## 10. Decisions needed before the affected steps

| # | Decision | Needed before | Recommendation |
|---|---|---|---|
| D-1 | Approve synthetic in-app course content (modules, lessons, learning player) as new, local/ci-only scope (DEC-049) | Step 7 | Approve, labelled DEMO, modelled on `LearningMaterial` so real content can replace it |
| D-2 | UI foundation: adopt Tailwind CSS + shadcn/ui (TECH_STACK proposal) or extend the current plain-CSS tokens | Step 1 | Adopt Tailwind + shadcn/ui now (already the documented target; Radix gives accessible dialogs/tabs/menus); migrate screen by screen |
| D-3 | Add descriptive `difficulty` (and learning objectives) to courses, not used in ranking | Step 6 | Approve |
| D-4 | Product name shown in the UI (DEC-001) | Step 1 | Keep a neutral working name until decided |
