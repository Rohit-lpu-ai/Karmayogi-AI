# Phase C - Learner Experience Plan

| Field | Value |
|---|---|
| **Date** | 2026-09-15 |
| **Scope** | Login, dashboard, competency profile, gap analysis, course catalogue and detail, learning experience, richer demo content |
| **Inputs audited** | PRD §7-12, §18; MVP_SCOPE (MVP-06/07/08/17/18/19/24, F3/F4, §5 forbidden list); UI_UX_SPEC S-01, S-03 to S-09, S-16; DATA_MODEL (Competency, CompetencyLevel, RoleCompetency, Course, CourseCompetency, Recommendation, LearningPath, LearningPathItem, LearningActivity, ProgressRecord, LearningMaterial); API_INTEGRATION_SPEC §2.3, §2.5, §2.9; DECISIONS DEC-001 to DEC-053; Phase A/B evidence and screenshots; migrations 0001-0004; seed packs; frontend routes |
| **Related** | [product-upgrade-baseline.md](product-upgrade-baseline.md) · [phase-c-learning-experience-proposal.md](phase-c-learning-experience-proposal.md) |

## 1. What the documents already allow

| Area | Documented basis | Status for Phase C |
|---|---|---|
| C1 Login | S-01 (email, password, show-password toggle, "contact your administrator", lockout message). No self-registration (MVP-01 out of scope) | **Approved** - no signup |
| C2 Dashboard | S-03, MVP-19 (baseline status, top gaps max 3, continue learning, recommendations max 3, recent assessments); `GET /me/dashboard`, `GET /me/attempts` specified | **Approved**, with the readiness conflict below |
| C3 Competency profile | S-04, MVP-07; `CompetencyLevel.description` exists for plain-language level meaning | **Approved** (correction request action is Phase 4 governance; shown as not yet available) |
| C4 Gap analysis | S-05, MVP-08 (gaps only with evidence ≥ medium; strengths; insufficient-evidence section; chart + table) | **Approved** |
| C5 Catalogue | S-09, MVP-17; `GET /courses` (filters competency, type); MVP search inside Courses allowed (UX §3.2); learners see approved and displayable items only | **Approved** (99 NSSTA listings stay hidden: unreviewed) |
| C6 Course detail | `GET /courses/{id}`; DEC-051 difficulty and objectives | **Approved** except structure/progress (C7) |
| C7 Lessons, learning player, progress | DEC-049 accepted, **but** it requires a written schema proposal before implementation; LearningPath/ProgressRecord are P0 entities not yet migrated | **Blocked on approval** of the written proposal |
| C8 Demo content | DEC-045 (synthetic, local/ci only), DEC-052 (versioned packs); question model supports single-answer MCQ with scenario stems | **Approved** as pack `demo-2` |
| AI/RAG | AGENT_CONTEXT rules 6, 24-30; DEC-005/006 undecided | **Not in Phase C** |

## 2. Conflicts between the Phase C brief and existing decisions

| # | Brief asks for | Document says | Proposed handling |
|---|---|---|---|
| X-1 | "Overall competency readiness" on the dashboard | Role-readiness score is **P1** with misuse risk (ROLE-008; MVP-08 out of scope; MVP_SCOPE §5) | Show "N of M competencies at the required level" and per-competency status. No single readiness percentage. **Decision D-1** |
| X-2 | Loop ends with "new evidence → updated competency profile" | Learning-activity evidence is **P1** (CMP-018); reassessment is **P1** (ASM-012, J-12) | Show the full loop on the dashboard, with the last two steps marked "later release". Estimates change only through assessments. **Decision D-2** |
| X-3 | Course structure, progress, start/continue (C6, C7) | DEC-049: proposal before schema | Written proposal delivered; course detail ships with objectives, reason and gap, and an honest "lessons not available yet" state until approval. **Decision D-3** |
| X-4 | Arithmetic items "only for infrastructure testing" | DEC-045 created them; DEC-052 packs are additive | `demo-2` adds new roles. Retiring the `demo-1` job role from the role picker is a data change to existing demo accounts. **Decision D-4** |
| X-5 | "Communicate the SIH vision" | DEC-053 neutral working name; UI_UX_SPEC §1 no official branding | Value proposition in plain words on login and dashboard; no SIH or government logos. Mentioning "Smart India Hackathon" in the UI is **Decision D-5** |

## 3. Implementation order

| Step | Content | Schema | API |
|---|---|---|---|
| C8 | Pack `demo-2`: synthetic "statistical practice" framework, 4 levels with plain-language descriptions, 8 competencies with descriptions, 3 job roles, 40 scenario questions (5 per competency, so evidence reaches "medium"), 3 baseline assessments (20 items each), 12 courses with difficulty and objectives | Migration `0005`: `courses.difficulty`, `courses.learning_objectives` (DEC-051) | Additive fields: competency `description`, level `description`, course `difficulty`/`learning_objectives` |
| C4/C3 | Gap analysis and competency profile pages | none | `GET /me/attempts` (specified); evidence summary from the existing profile explanation |
| C2 | Dashboard | none | uses profile, gaps, recommendations, assessments, attempts |
| C5/C6 | Catalogue with search and filters; course detail with reason and gap | none beyond 0005 | `GET /courses`, `GET /courses/{id}` (specified) |
| C1 | Login | none | none |
| C7 | Lessons, learning path, progress | **after approval** (see proposal) | `/me/learning-path`, `/learning-path-items/{id}`, `/me/progress`, lesson endpoints |
| C10 | Playwright + axe for every new route, desktop and 360 px; screenshots | - | - |

Not in Phase C: AI provider interfaces (after the loop is complete), correction requests, recommendation dismiss/accept persistence, `/me/dashboard` aggregate endpoint (the dashboard composes existing endpoints; each card loads and fails independently as MVP-19 requires).

## 4. Decisions required

| ID | Question | Recommendation |
|---|---|---|
| D-1 | Show a single role-readiness score? | No. Keep "N of M at required level" (ROLE-008 is P1) |
| D-2 | Let learning completion or reassessment update competency estimates in MVP? | No for learning evidence (CMP-018). Consider approving reassessment (ASM-012) as the only P1 pull-forward if the demo must show "updated profile" |
| D-3 | Approve the learning-experience schema proposal | Approve as written, or amend |
| D-4 | Retire the `demo-1` arithmetic job role from the role picker (set inactive; existing accounts keep working) | Yes, after `demo-2` is verified |
| D-5 | May the UI mention "Smart India Hackathon prototype" (text only, no logos)? | Your call; default is no mention |
| D-6 | Manual screen-reader review | Needs a person with NVDA or Narrator; not possible from this environment |
