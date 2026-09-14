# Feature Catalog

| | |
|---|---|
| **Product** | Competency intelligence and personalized learning platform for India's official statistical system (working name: Decision required, [DECISIONS.md](DECISIONS.md) DEC-001) |
| **Document version** | 1.0.0-draft |
| **Status** | Draft for approval - no implementation authorised |
| **Owner** | Product owner: Decision required |
| **Last updated** | 2026-09-14 |
| **Generated from** | `scripts/docs/registry_*.py` via `scripts/docs/generate_feature_catalog.py` (do not hand-edit; edit the registry and regenerate) |
| **Machine-readable copy** | [feature_registry.json](feature_registry.json) |
| **Related** | [PRD.md](PRD.md) · [MVP_SCOPE.md](MVP_SCOPE.md) · [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) · [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) · [UI_UX_SPEC.md](UI_UX_SPEC.md) |

## How to read this catalog

- **Priority:** P0 = MVP (first usable product); P1 = post-MVP; P2 = future. P1 and P2 features must not be implemented during MVP ([MVP_SCOPE.md](MVP_SCOPE.md) §Forbidden).
- **Implementation status** uses the implementation vocabulary in [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md): Implemented, Partially implemented, Mocked, Planned, Unknown, Blocked by external access, Requires human confirmation. Every status cites repository evidence.
- **API requirements** name *planned internal* endpoints of this platform. They are not implemented and are **not** external or iGOT endpoints.
- **Alias entries** ("Alias of") keep the inventory complete where the brief lists the same capability in more than one category; the canonical entry holds the full specification.
- One feature (`UX-021 User profile and account settings`) was added because the P0 list requires a user profile but the inventory had no matching item ([DOCUMENTATION_VALIDATION_REPORT.md](DOCUMENTATION_VALIDATION_REPORT.md)).

## Summary

**370 features** - P0: 173 · P1: 140 · P2: 57

| Implementation status | Features |
|---|---|
| Implemented | 1 |
| Partially implemented | 15 |
| Mocked | 3 |
| Planned | 338 |
| Unknown | 0 |
| Blocked by external access | 12 |
| Requires human confirmation | 1 |

| Category | Prefix | Features | P0 | P1 | P2 |
|---|---|---|---|---|---|
| [A. Core AI intelligence](#a-core-ai-intelligence) | AI | 18 | 11 | 6 | 1 |
| [B. Learning material intelligence](#b-learning-material-intelligence) | MAT | 31 | 20 | 9 | 2 |
| [C. Quiz and assessment engine](#c-quiz-and-assessment-engine) | ASM | 32 | 21 | 10 | 1 |
| [D. Competency intelligence](#d-competency-intelligence) | CMP | 19 | 9 | 7 | 3 |
| [E. Role intelligence](#e-role-intelligence) | ROLE | 13 | 4 | 6 | 3 |
| [F. Personalization](#f-personalization) | PER | 18 | 5 | 9 | 4 |
| [G. AI learning tutor](#g-ai-learning-tutor) | TUT | 20 | 0 | 16 | 4 |
| [H. iGOT integration](#h-igot-integration) | IGOT | 18 | 6 | 9 | 3 |
| [I. Administration](#i-administration) | ADM | 18 | 13 | 5 | 0 |
| [J. Analytics](#j-analytics) | ANA | 16 | 0 | 11 | 5 |
| [K. Trainer workspace](#k-trainer-workspace) | TRN | 15 | 8 | 6 | 1 |
| [L. Multilingual and accessibility](#l-multilingual-and-accessibility) | ACC | 17 | 7 | 6 | 4 |
| [M. Gamification](#m-gamification) | GAM | 12 | 0 | 8 | 4 |
| [N. Progress tracking](#n-progress-tracking) | PRO | 14 | 9 | 5 | 0 |
| [O. Reporting](#o-reporting) | REP | 15 | 7 | 7 | 1 |
| [P. Security](#p-security) | SEC | 21 | 17 | 4 | 0 |
| [Q. Responsible AI](#q-responsible-ai) | RAI | 19 | 17 | 2 | 0 |
| [R. Automation](#r-automation) | AUT | 15 | 8 | 7 | 0 |
| [S. UX and platform experience](#s-ux-and-platform-experience) | UX | 21 | 11 | 7 | 3 |
| [T. Future intelligence](#t-future-intelligence) | FUT | 18 | 0 | 0 | 18 |

## P0 feature index

| ID | Feature | Implementation status | Alias of |
|---|---|---|---|
| AI-001 | AI-based competency assessment | Planned |  |
| AI-002 | Competency-gap detection | Planned |  |
| AI-004 | Personalized learning-path generation | Planned |  |
| AI-005 | AI course recommendation | Planned |  |
| AI-006 | iGOT course recommendation | Mocked |  |
| AI-007 | Quiz and MCQ generation | Planned |  |
| AI-009 | Answer evaluation | Planned |  |
| AI-012 | Competency score calculation | Planned |  |
| AI-016 | Evidence-based competency estimation | Planned |  |
| AI-017 | Confidence scoring | Planned |  |
| AI-018 | Explainable competency results | Planned |  |
| MAT-001 | PDF upload | Partially implemented |  |
| MAT-002 | DOCX upload | Planned |  |
| MAT-004 | TXT upload | Planned |  |
| MAT-007 | Text extraction | Partially implemented |  |
| MAT-008 | Text cleaning | Planned |  |
| MAT-009 | Document normalization | Planned |  |
| MAT-010 | Chunking | Planned |  |
| MAT-011 | Metadata enrichment | Partially implemented |  |
| MAT-012 | Embedding generation | Planned |  |
| MAT-013 | Vector storage | Planned |  |
| MAT-014 | Semantic search | Planned |  |
| MAT-015 | Keyword search | Planned |  |
| MAT-017 | Document Q&A | Planned |  |
| MAT-018 | RAG responses | Planned |  |
| MAT-019 | Source citations | Planned |  |
| MAT-020 | Page-level citations where possible | Planned |  |
| MAT-028 | Document access control | Planned |  |
| MAT-029 | Processing status | Partially implemented |  |
| MAT-030 | Failed-processing recovery | Planned |  |
| MAT-031 | Duplicate-document detection | Partially implemented |  |
| ASM-001 | MCQs | Planned |  |
| ASM-006 | Difficulty levels | Planned |  |
| ASM-007 | Custom question count | Planned |  |
| ASM-008 | Topic-based quizzes | Planned |  |
| ASM-009 | Competency-based quizzes | Planned |  |
| ASM-010 | Role-based quizzes | Planned |  |
| ASM-011 | Pre-assessment | Planned |  |
| ASM-014 | Randomization | Planned |  |
| ASM-017 | Auto-evaluation | Planned |  |
| ASM-019 | Feedback | Planned |  |
| ASM-020 | Explanations | Planned |  |
| ASM-021 | Source evidence | Planned |  |
| ASM-022 | Duplicate detection | Planned |  |
| ASM-023 | Incorrect-answer detection | Planned |  |
| ASM-024 | Hallucination detection | Planned |  |
| ASM-027 | Question review workflow | Planned |  |
| ASM-028 | Question approval | Planned |  |
| ASM-029 | Question rejection | Planned |  |
| ASM-030 | Question editing | Planned |  |
| ASM-031 | Question versioning | Planned |  |
| ASM-032 | Assessment history | Planned |  |
| CMP-001 | Learner competency profile | Planned |  |
| CMP-002 | Competency scores | Planned |  |
| CMP-004 | Competency-gap analysis | Planned |  |
| CMP-006 | Strengths | Planned |  |
| CMP-007 | Developing skills | Planned |  |
| CMP-008 | Required-versus-current comparison | Planned |  |
| CMP-016 | Evidence ledger | Planned |  |
| CMP-017 | Assessment history (competency view) | Planned | ASM-032 |
| CMP-019 | Human-reviewed competency adjustments | Planned |  |
| ROLE-001 | Job-role selection | Planned |  |
| ROLE-002 | Role-to-competency mapping | Requires human confirmation |  |
| ROLE-004 | Role-to-assessment mapping | Planned |  |
| ROLE-007 | Role-specific quizzes | Planned | ASM-010 |
| PER-001 | Personalized dashboard | Planned |  |
| PER-002 | Personalized course recommendations | Planned | AI-005 |
| PER-003 | Personalized learning paths | Planned | AI-004 |
| PER-009 | Performance-based recommendations | Planned |  |
| PER-010 | Competency-based recommendations | Planned |  |
| IGOT-002 | iGOT course recommendation | Mocked | AI-006 |
| IGOT-010 | API client abstraction | Implemented |  |
| IGOT-011 | Mock iGOT adapter | Mocked |  |
| IGOT-013 | Integration health checks | Planned |  |
| IGOT-017 | Integration failure states | Partially implemented |  |
| IGOT-018 | External-source provenance | Partially implemented |  |
| ADM-001 | User management | Planned |  |
| ADM-002 | Department management | Planned |  |
| ADM-003 | Role management | Planned |  |
| ADM-004 | Competency management | Partially implemented |  |
| ADM-005 | Course management | Partially implemented |  |
| ADM-006 | Assessment management | Planned |  |
| ADM-007 | Quiz management | Planned | ADM-006 |
| ADM-008 | Learning-material management | Planned |  |
| ADM-009 | AI-generated-content review | Planned | ASM-027 |
| ADM-010 | Approval workflows | Planned |  |
| ADM-012 | Learner progress monitoring | Planned |  |
| ADM-014 | Configuration management | Planned |  |
| ADM-017 | Audit-log access | Planned |  |
| TRN-001 | Trainer dashboard | Planned |  |
| TRN-002 | Material upload | Planned | MAT-001 |
| TRN-003 | Quiz generation | Planned | AI-007 |
| TRN-004 | Quiz review | Planned | ASM-027 |
| TRN-005 | Quiz editing | Planned | ASM-030 |
| TRN-006 | Quiz approval | Planned | ASM-028 |
| TRN-007 | Quiz rejection | Planned | ASM-029 |
| TRN-008 | Manual question creation | Planned |  |
| ACC-001 | English | Planned |  |
| ACC-003 | Indian-language support architecture | Planned |  |
| ACC-009 | Screen-reader compatibility | Planned |  |
| ACC-010 | Keyboard navigation | Planned |  |
| ACC-014 | Accessible forms | Planned |  |
| ACC-015 | Accessible charts | Planned |  |
| ACC-016 | Reduced-motion support | Planned |  |
| PRO-001 | Course progress | Planned |  |
| PRO-002 | Quiz progress | Planned |  |
| PRO-003 | Competency progress | Planned |  |
| PRO-005 | Learning history | Planned |  |
| PRO-006 | Scores | Planned |  |
| PRO-010 | Completed items | Planned |  |
| PRO-011 | Pending items | Planned |  |
| PRO-012 | Recommended items | Planned |  |
| PRO-013 | Assessment timeline | Planned |  |
| REP-001 | Employee report | Planned |  |
| REP-003 | Competency-gap report | Planned |  |
| REP-004 | Assessment report | Planned |  |
| REP-007 | Progress report | Planned |  |
| REP-012 | CSV export | Planned |  |
| REP-014 | Report access control | Planned |  |
| REP-015 | Report audit trail | Planned |  |
| SEC-001 | Authentication | Planned |  |
| SEC-002 | Role-based access control | Planned |  |
| SEC-003 | JWT or secure session architecture | Planned |  |
| SEC-005 | Admin authentication | Planned |  |
| SEC-006 | Encryption in transit | Planned |  |
| SEC-007 | Encryption at rest | Planned |  |
| SEC-008 | Secure APIs | Planned |  |
| SEC-009 | Audit logs | Planned |  |
| SEC-010 | Activity logs | Planned |  |
| SEC-011 | AI interaction logs | Planned |  |
| SEC-012 | Document-level access control | Planned | MAT-028 |
| SEC-013 | Session management | Planned |  |
| SEC-014 | Rate limiting | Planned |  |
| SEC-015 | Input validation | Planned |  |
| SEC-016 | Output validation | Planned |  |
| SEC-017 | Secret management | Partially implemented |  |
| SEC-021 | Threat modeling | Planned |  |
| RAI-001 | Retrieval grounding | Planned |  |
| RAI-002 | Citations | Planned | MAT-019 |
| RAI-003 | Confidence indicators | Planned |  |
| RAI-004 | Hallucination mitigation | Planned |  |
| RAI-005 | Question validation | Planned |  |
| RAI-006 | Human approval | Planned | ASM-028 |
| RAI-007 | Prompt-injection protection | Planned |  |
| RAI-008 | Audit trails | Planned | SEC-011 |
| RAI-009 | Safety filters | Planned |  |
| RAI-011 | Explainable recommendations | Planned |  |
| RAI-012 | Model evaluation | Planned |  |
| RAI-014 | AI output versioning | Planned |  |
| RAI-015 | Abstention behavior | Planned |  |
| RAI-016 | Sensitive-data minimization | Partially implemented |  |
| RAI-017 | Human override | Planned |  |
| RAI-018 | Appeal/correction workflow | Planned |  |
| RAI-019 | Model and prompt registry | Planned |  |
| AUT-001 | Automated recommendations | Planned |  |
| AUT-002 | Competency updates | Planned |  |
| AUT-003 | Quiz generation (job) | Planned |  |
| AUT-004 | Answer evaluation (automation) | Planned | AI-009 |
| AUT-012 | Background jobs | Planned |  |
| AUT-013 | Retry queues | Planned |  |
| AUT-014 | Job monitoring | Planned |  |
| AUT-015 | Idempotency | Partially implemented |  |
| UX-001 | Responsive design | Planned |  |
| UX-002 | Mobile-friendly experience | Planned |  |
| UX-003 | Personalized home | Planned |  |
| UX-009 | Continue learning | Planned |  |
| UX-011 | Accessibility | Planned | ACC-009 |
| UX-012 | Empty states | Planned |  |
| UX-013 | Loading states | Planned |  |
| UX-014 | Error states | Planned |  |
| UX-015 | Onboarding | Planned |  |
| UX-019 | Search filters | Planned |  |
| UX-021 | User profile and account settings | Planned |  |

## Table of contents

- [A. Core AI intelligence](#a-core-ai-intelligence)
- [B. Learning material intelligence](#b-learning-material-intelligence)
- [C. Quiz and assessment engine](#c-quiz-and-assessment-engine)
- [D. Competency intelligence](#d-competency-intelligence)
- [E. Role intelligence](#e-role-intelligence)
- [F. Personalization](#f-personalization)
- [G. AI learning tutor](#g-ai-learning-tutor)
- [H. iGOT integration](#h-igot-integration)
- [I. Administration](#i-administration)
- [J. Analytics](#j-analytics)
- [K. Trainer workspace](#k-trainer-workspace)
- [L. Multilingual and accessibility](#l-multilingual-and-accessibility)
- [M. Gamification](#m-gamification)
- [N. Progress tracking](#n-progress-tracking)
- [O. Reporting](#o-reporting)
- [P. Security](#p-security)
- [Q. Responsible AI](#q-responsible-ai)
- [R. Automation](#r-automation)
- [S. UX and platform experience](#s-ux-and-platform-experience)
- [T. Future intelligence](#t-future-intelligence)

---

# A. Core AI intelligence


## [AI-001] AI-based competency assessment

- Description: Runs a role-based initial assessment built only from human-approved questions and converts the results into per-competency estimates. AI assists question creation; the score calculation itself is deterministic in MVP.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Gives each learner an evidence-based starting point instead of a self-declared skill list.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: ROLE-002; ASM-011; ASM-027; AI-012
- Data required: Approved Question records tagged to competency, topic and difficulty; RoleCompetency required levels; AssessmentAttempt and Answer records.
- AI involvement: Indirect: questions are AI-generated then human-approved (AI-007, ASM-027). Scoring is rule-based (AI_SYSTEM_SPEC.md §25).
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/assessments/{id}/attempts; PUT /api/v1/attempts/{id}/answers/{question_id}; POST /api/v1/attempts/{id}/submit; GET /api/v1/attempts/{id}/result
- UI requirements: Assessment screen; Assessment results screen (UI_UX_SPEC.md).
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Too few approved questions for a competency -> that competency is reported as 'insufficient evidence'. Session interrupted -> attempt resumable until expiry.
- Acceptance criteria: An attempt produces estimates only from approved questions; each estimate links to its evidence; competencies below the minimum item count show 'insufficient evidence' instead of a score.
- Future extensions: Adaptive item selection (AI-008); IRT calibration (FUT-006).

## [AI-002] Competency-gap detection

- Description: Compares each estimated competency level with the level required by the learner's selected job role and lists gaps by size.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Turns assessment results into a concrete, prioritised development need.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: AI-012; ROLE-002; AI-017
- Data required: UserCompetency estimates with evidence sufficiency; RoleCompetency required levels.
- AI involvement: None in MVP: deterministic comparison (AI_SYSTEM_SPEC.md §25).
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/competency-gaps; GET /api/v1/users/{id}/competency-gaps (scoped roles)
- UI requirements: Competency-gap analysis screen.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: No job role selected -> prompt to select one. Role has no required levels -> 'role not configured' shown to learner and competency administrator.
- Acceptance criteria: A gap is shown only when a required level exists and evidence sufficiency is at least 'medium'; each gap shows required level, estimated level, evidence link and suggested next step.
- Future extensions: Critical-skill weighting (CMP-005); competency dependencies (CMP-010).

## [AI-003] Role mapping

- Description: Suggests the most likely configured job role from department, designation and a free-text description of responsibilities.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Speeds onboarding where designations do not map cleanly to configured roles.
- Priority: P1
- Product area: Core AI intelligence
- Dependencies: ROLE-001; RAI-016
- Data required: JobRole names and descriptions; user-entered responsibilities text.
- AI involvement: LLM classification against configured roles with stated reasons.
- Human review required: Required: the user or an administrator confirms every suggested role.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/job-roles/suggestions (P1)
- UI requirements: Suggestion panel inside Onboarding with accept / choose another.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Low-confidence classification -> no suggestion; free text containing personal data -> redacted before provider call.
- Acceptance criteria: A suggestion never changes the user's role without explicit confirmation; reasons are shown for every suggestion.
- Future extensions: Role transition pathways (ROLE-010).

## [AI-004] Personalized learning-path generation

- Description: Builds an ordered learning path of courses, NSSTA programme listings and approved materials addressing the learner's largest gaps.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Converts gaps into an actionable sequence rather than an unordered list.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: AI-002; AI-005; ADM-005
- Data required: Gaps (AI-002); Course and LearningMaterial with human-approved competency/topic mappings; completion status.
- AI involvement: Rule-based ranking with template explanations in MVP; no LLM (AI_SYSTEM_SPEC.md §26-27).
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/learning-path; POST /api/v1/me/learning-path/regenerate; PATCH /api/v1/learning-path-items/{id}
- UI requirements: Learning path screen; 'Continue learning' card on Learner dashboard.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: No approved content mapped to a gap -> item 'No approved content yet' plus a signal to the training manager.
- Acceptance criteria: Every item states the gap it addresses and the rule that selected it; regenerating with unchanged inputs yields the same ordering.
- Future extensions: Time-boxed plans (PER-005/006); prerequisite ordering (PER-007).

## [AI-005] AI course recommendation

- Description: Recommends internal courses, NSSTA programme listings and approved learning materials relevant to the learner's gaps and role.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Directs limited training time to the most relevant content.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: AI-002; ADM-005; RAI-011
- Data required: Course, LearningMaterial, CourseCompetency/topic mappings (human-approved), gaps, completion history.
- AI involvement: Deterministic scoring in MVP (gap severity x competency/topic match, completed items excluded). LLM re-ranking is P1 and requires evaluation first.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/recommendations; POST /api/v1/recommendations/{id}/feedback
- UI requirements: Recommendation cards on Learner dashboard and Course discovery, each with a 'Why recommended' explanation.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Empty catalogue -> empty state; mapping unreviewed (e.g. ASSUMED topic tags from data/processed) -> item excluded.
- Acceptance criteria: Each recommendation shows reason, source organisation and provenance badge; iGOT items from the mock adapter carry a MOCK badge; dismissed items are not re-shown for the configured period.
- Future extensions: Collaborative signals and LLM re-ranking (P1, after offline evaluation).

## [AI-006] iGOT course recommendation

- Description: Includes courses returned by the iGOT adapter in recommendations. Only the mock adapter exists, so in MVP these are mock records labelled as such.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Demonstrates the integration path without claiming real iGOT access.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: IGOT-010; IGOT-011; AI-005
- Data required: Records from IGotClient.list_courses(); every mock record has data_status MOCK.
- AI involvement: Same deterministic scoring as AI-005.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP - mock data only, feature-flagged
- Implementation status: Mocked - mock catalogue via clients/mock_igot_client.py (tests pass); recommendation logic not built.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/recommendations?source=igot; GET /api/v1/integrations/igot/courses
- UI requirements: MOCK badge and 'Not real iGOT data' text on every iGOT-sourced card.
- Security considerations: Never present mock data as external data; disable in production unless a verified real adapter exists (API_INTEGRATION_SPEC.md §iGOT).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Adapter mode 'live' -> refused (AccessNotVerifiedError) and source hidden; mock disabled by flag -> source hidden, admins see 'not connected'.
- Acceptance criteria: With IGOT_CLIENT_MODE=mock every iGOT-sourced item is visibly labelled MOCK; no code path presents mock data as real; the feature flag can disable the source entirely.
- Future extensions: Real recommendations after authorised access (IGOT-012).

## [AI-007] Quiz and MCQ generation

- Description: Generates candidate multiple-choice questions from licence-permitted, approved document chunks using structured output; every candidate goes through validation and human review.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Reduces trainer effort to create source-grounded question banks.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: MAT-010; ASM-022; ASM-027; RAI-019
- Data required: DocumentChunk text from materials whose licence permits derivative use; Topic; Competency; generation parameters.
- AI involvement: LLM structured generation behind the provider interface (AI_SYSTEM_SPEC.md §21).
- Human review required: Required: no generated question is used in an assessment before approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/question-generation-jobs; GET /api/v1/question-generation-jobs/{id}
- UI requirements: Quiz builder (select sources, topic, competency, count, difficulty) with job progress.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Provider timeout -> retry with backoff; schema-invalid output -> discarded and logged; zero valid questions -> job completes with reasons.
- Acceptance criteria: Every generated question stores source chunk IDs, evidence span, model, prompt version, timestamp and validation status, and starts as 'pending_validation'; none is learner-visible before approval.
- Future extensions: True/false, fill-in-the-blank, scenario types (ASM-002 to ASM-005); multilingual generation (ACC-005).

## [AI-008] Adaptive assessment

- Description: Chooses the next question based on responses so far, stepping difficulty up or down within a competency.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Shorter assessments with better precision at the learner's level.
- Priority: P1
- Product area: Core AI intelligence
- Dependencies: AI-001; ASM-026
- Data required: Approved questions with calibrated difficulty; response history.
- AI involvement: Rule-based staircase in P1; IRT-based selection is FUT-006.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/attempts/{id}/next-question (P1)
- UI requirements: Assessment screen shows progress without revealing difficulty.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Item pool exhausted -> assessment ends with evidence-sufficiency note.
- Acceptance criteria: Adaptive rules are documented and versioned; an attempt can be replayed to reproduce the item sequence.
- Future extensions: IRT (FUT-006); knowledge tracing (FUT-004).

## [AI-009] Answer evaluation

- Description: Scores objective answers (MCQ in MVP) against the approved answer key.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Immediate, consistent scoring.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: ASM-031; ASM-017
- Data required: Approved question version and answer key; Answer.
- AI involvement: None: deterministic.
- Human review required: Not required for deterministic scoring; answer-key corrections are human actions and audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/attempts/{id}/submit
- UI requirements: Assessment results screen.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Answer key later corrected -> affected attempts re-scored with an audit record and learner notice.
- Acceptance criteria: Scoring uses the question version shown to the learner; re-scoring after a key correction is logged and visible to the learner.
- Future extensions: Short-answer and scenario evaluation (AI-010, AI-011).

## [AI-010] Short-answer evaluation

- Description: Scores short free-text answers against an approved rubric and reference answer, citing the rubric criteria met.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Assesses understanding beyond recognition.
- Priority: P1
- Product area: Core AI intelligence
- Dependencies: ASM-018; RAI-006
- Data required: Rubric, reference answer, source citations, learner answer.
- AI involvement: LLM rubric scoring with structured output and evidence spans.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/attempts/{id}/submit (async evaluation job, P1)
- UI requirements: Result shows criteria met / not met and 'pending review' state.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Low-confidence or out-of-rubric answer -> routed to manual evaluation (ASM-018).
- Acceptance criteria: No LLM score contributes to a competency estimate until confirmed by a human during pilot; rubric version and model metadata stored.
- Future extensions: Calibration against human graders; multilingual answers.

## [AI-011] Scenario evaluation

- Description: Evaluates responses to scenario or case questions against a structured rubric.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Assesses applied judgement in statistical work contexts.
- Priority: P1
- Product area: Core AI intelligence
- Dependencies: ASM-004; AI-010
- Data required: Scenario, rubric, reference points, learner response.
- AI involvement: LLM rubric scoring (same controls as AI-010).
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/attempts/{id}/submit (P1)
- UI requirements: Rubric breakdown view.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Ambiguous response -> manual evaluation.
- Acceptance criteria: Human confirmation before contributing to competency estimates.
- Future extensions: Simulation-based learning (FUT-017).

## [AI-012] Competency score calculation

- Description: Calculates a per-competency score from correct answers to approved questions, weighted by difficulty, and maps it to the framework's level scale.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Consistent, reproducible, explainable scores.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: AI-009; ADM-004
- Data required: Answers; question difficulty and competency tags; configurable level thresholds per framework.
- AI involvement: None: deterministic, versioned method (AI_SYSTEM_SPEC.md §25). Thresholds are provisional until confirmed (ASSUMPTIONS_AND_OPEN_QUESTIONS.md).
- Human review required: Method and thresholds approved by competency framework administrator; individual adjustments via CMP-019.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/competency-profile; GET /api/v1/users/{id}/competency-profile
- UI requirements: Competency profile and Assessment results.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Thresholds not configured for a framework -> score shown without a level plus 'levels not configured'.
- Acceptance criteria: Same inputs always produce the same score; method version is stored with each estimate; the explanation lists contributing questions.
- Future extensions: IRT scoring (FUT-006); BKT (FUT-005).

## [AI-013] Learning-outcome prediction

- Description: Predicts the likelihood that a learner reaches a target level given a learning plan.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Helps plan realistic development timelines.
- Priority: P2
- Product area: Core AI intelligence
- Dependencies: PRO-005; RAI-010
- Data required: Historical attempts and outcomes (none exist today).
- AI involvement: Statistical/ML model requiring validation data.
- Human review required: Required: predictions are advisory and never used for employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Insufficient history -> feature unavailable.
- Acceptance criteria: Not built until validated historical data exists and a fairness review is complete.
- Future extensions: Workforce intelligence (FUT-013).

## [AI-014] Weak-topic detection

- Description: Aggregates incorrect answers by topic to highlight topics needing revision.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Finer-grained guidance than competency-level gaps.
- Priority: P1
- Product area: Core AI intelligence
- Dependencies: AI-009; ADM-015
- Data required: Answers with topic tags.
- AI involvement: Rule-based aggregation.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/weak-topics (P1)
- UI requirements: Weak topics panel on Competency profile.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Too few answers per topic -> topic not flagged.
- Acceptance criteria: A topic is flagged only above a minimum answer count; each flag links to the answers behind it.
- Future extensions: Spaced repetition (PER-015).

## [AI-015] Reassessment recommendations

- Description: Suggests reassessment when path items for a gap are completed or a configured interval has passed.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Closes the loop between learning and measured improvement.
- Priority: P1
- Product area: Core AI intelligence
- Dependencies: ASM-012; AI-004
- Data required: Learning path completion; last attempt dates.
- AI involvement: Rule-based triggers.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/recommendations?type=reassessment (P1)
- UI requirements: Reassessment card on Learner dashboard.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: No eligible post-assessment -> no suggestion.
- Acceptance criteria: Suggestions state the trigger that produced them.
- Future extensions: Reminders via notifications (AUT-006).

## [AI-016] Evidence-based competency estimation

- Description: Backs every competency estimate with explicit evidence records (attempt answers, human adjustments) and refuses to estimate without evidence.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Estimates can be inspected, challenged and corrected.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: AI-012; CMP-016
- Data required: CompetencyEvidence linked to Answer, AssessmentAttempt, adjustment records.
- AI involvement: None: estimates are derived from evidence records.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/users/{id}/competencies/{competency_id}/evidence
- UI requirements: Evidence panel in Competency profile.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Evidence voided (e.g. question withdrawn) -> estimate recomputed and change logged.
- Acceptance criteria: No estimate exists without at least one evidence record; each estimate lists its evidence; voiding evidence recomputes the estimate with an audit entry.
- Future extensions: Evidence ledger and skill passport (CMP-016, CMP-015).

## [AI-017] Confidence scoring

- Description: Assigns each estimate an evidence-sufficiency band (insufficient / low / medium / high) from item count and validation status. It is not a statistical accuracy claim.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Prevents over-interpretation of thin evidence.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: AI-012
- Data required: Item counts per competency; question validation statuses.
- AI involvement: None: rule-based bands with provisional thresholds.
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in competency profile and gap responses.
- UI requirements: Band label with definition tooltip and plain-language limitation text.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Thresholds not configured -> default provisional thresholds displayed as provisional.
- Acceptance criteria: Every displayed estimate shows its band and the definition of that band; 'insufficient' estimates never produce gaps.
- Future extensions: Statistical confidence intervals after calibration (FUT-006).

## [AI-018] Explainable competency results

- Description: Shows how each estimate was produced: method version, evidence, required level, limitations, how to improve and how to request a correction.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Supports trust, contestability and human oversight.
- Priority: P0
- Product area: Core AI intelligence
- Dependencies: AI-016; RAI-018
- Data required: Estimate, evidence, method version, required level, limitation text.
- AI involvement: None in MVP (template-based explanation).
- Human review required: Required: estimates and generated artefacts are reviewable and correctable by authorised humans; never used for automated employment decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/competency-profile (includes explanation block)
- UI requirements: 'How was this calculated?' panel on Competency profile and Assessment results.
- Security considerations: Organisation-scoped data; learner personal data never sent to an AI provider without authorisation (RAI-016); every AI call logged (SEC-011).
- Accessibility considerations: Results readable by screen readers; charts have table equivalents; plain-language explanations.
- Failure cases: Missing evidence metadata -> estimate hidden and flagged to administrators.
- Acceptance criteria: Every estimate has an explanation panel with method, evidence, limitations and a correction-request action.
- Future extensions: Natural-language explanations generated from structured evidence (P1, reviewed).

---

# B. Learning material intelligence


## [MAT-001] PDF upload

- Description: Uploads PDF learning materials into a learning material record for processing.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: PDF is the dominant format of NSSTA and MoSPI material.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: File bytes; uploader; material metadata (title, organisation, licence/usage notes, access scope).
- AI involvement: None at upload.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Partially implemented - offline collector downloads public PDFs with signature/size checks (scripts/collectors/fetch_documents.py); no user upload.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-materials; POST /api/v1/learning-materials/{id}/documents (multipart)
- UI requirements: Upload dialog in Document library with licence attestation.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Wrong type or failed %PDF- signature -> rejected; over size limit -> rejected; duplicate SHA-256 -> linked to existing document.
- Acceptance criteria: Only files passing MIME, signature and size checks are stored; SHA-256 recorded; a processing job is queued and its status visible.
- Future extensions: Bulk upload; version supersession (MAT-027).

## [MAT-002] DOCX upload

- Description: Uploads Word documents for processing.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Trainer-authored material is often in DOCX.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: File bytes and material metadata.
- AI involvement: None at upload.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-materials/{id}/documents
- UI requirements: Same upload dialog as MAT-001.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Macro-enabled or malformed files rejected.
- Acceptance criteria: DOCX accepted after type validation; macro-enabled formats (.docm) rejected.
- Future extensions: Tracked-change handling.

## [MAT-003] PPT/PPTX upload

- Description: Uploads presentation files, extracting slide text and speaker notes.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Training decks are common in NSSTA programmes.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: File bytes; slide structure.
- AI involvement: None at upload.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-materials/{id}/documents (P1 types)
- UI requirements: Upload dialog; slide-level viewer.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Image-only slides -> require OCR (MAT-006).
- Acceptance criteria: Slide numbers preserved for citations.
- Future extensions: Slide-level summaries.

## [MAT-004] TXT upload

- Description: Uploads plain-text materials.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Lowest-risk format for notes and extracted text.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: File bytes (UTF-8 required) and metadata.
- AI involvement: None at upload.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-materials/{id}/documents
- UI requirements: Same upload dialog.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Non-UTF-8 encoding -> rejected with guidance.
- Acceptance criteria: UTF-8 text accepted; encoding errors rejected with a clear message.
- Future extensions: Markdown support.

## [MAT-005] Image upload

- Description: Uploads images (scans, charts) for OCR-based extraction.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Captures scanned material such as NSSTA-DOC-004/006.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: MAT-006
- Data required: Image bytes.
- AI involvement: OCR (MAT-006).
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-materials/{id}/documents (P1 types)
- UI requirements: Upload dialog with OCR notice.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Unreadable image -> 'no text extracted'.
- Acceptance criteria: Images are processed only through OCR and stored with the same ACL as documents.
- Future extensions: Chart description with review.

## [MAT-006] OCR

- Description: Extracts text from scanned PDFs and images, including Hindi where the OCR engine supports it.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Two collected NSSTA documents are scanned and currently unreadable.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Page images.
- AI involvement: OCR engine (candidate: Tesseract - Decision required, TECH_STACK.md).
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - not available; 2 collected NSSTA PDFs have no text layer (docs/DATA_COLLECTION_RESULTS.md).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Processing job step (P1)
- UI requirements: OCR-confidence indicator in Document viewer.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Low OCR confidence -> text flagged 'OCR - verify' and excluded from question generation.
- Acceptance criteria: OCR output is marked as OCR-derived with confidence and is excluded from generation until reviewed.
- Future extensions: Layout-aware OCR; table extraction.

## [MAT-007] Text extraction

- Description: Extracts text with page numbers from uploaded PDF, DOCX and TXT files.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Foundation for search, Q&A and question generation.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Stored document file.
- AI involvement: None: parser-based.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Partially implemented - pypdf extraction for collected PDFs in an offline script (scripts/utils/extract_pdf_metadata.py); no application pipeline.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Processing job step; GET /api/v1/documents/{id}
- UI requirements: Processing status and 'no text layer' warning.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: No text layer -> status 'needs_ocr'; parser error -> status 'failed' with retry.
- Acceptance criteria: Extracted text keeps page boundaries; documents without a text layer are flagged, not silently indexed as empty.
- Future extensions: Layout and table extraction.

## [MAT-008] Text cleaning

- Description: Removes repeated headers/footers, hyphenation artefacts and control characters while preserving page mapping.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Improves retrieval and question quality.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Extracted page text.
- AI involvement: None: rule-based.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Processing job step
- UI requirements: None beyond processing status.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Over-aggressive cleaning -> original text retained alongside cleaned text for audit.
- Acceptance criteria: Cleaning is reversible (original retained) and rules are versioned.
- Future extensions: Language-specific cleaning for Hindi.

## [MAT-009] Document normalization

- Description: Converts all formats into one internal representation (document -> pages -> text blocks) with character offsets.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: One downstream pipeline for all formats; stable citation offsets.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Cleaned text per page.
- AI involvement: None.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Processing job step
- UI requirements: None.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Offsets inconsistent -> job fails validation.
- Acceptance criteria: Every block has page number and character offsets usable by citations.
- Future extensions: Structural elements (headings, tables).

## [MAT-010] Chunking

- Description: Splits normalised text into retrieval chunks that never lose their page span, with configurable size and overlap.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Retrieval quality and page-level citations.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Normalised blocks.
- AI involvement: None: deterministic chunker (AI_SYSTEM_SPEC.md §12).
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Processing job step
- UI requirements: Chunk count shown in document details (admin).
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Oversized block -> split at sentence boundaries.
- Acceptance criteria: Each chunk stores page_start, page_end, char offsets and chunker version; re-chunking the same input is deterministic.
- Future extensions: Structure-aware chunking.

## [MAT-011] Metadata enrichment

- Description: Attaches organisation, licence, topics, competencies, language and provenance metadata to documents and chunks.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Enables filtered retrieval and licence-aware generation.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Material metadata; topic taxonomy; source provenance.
- AI involvement: Rule-based topic tagging in MVP (marked ASSUMED until reviewed).
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Partially implemented - rule-based topic tags and PDF metadata exist in offline scripts (scripts/processing/topic_taxonomy.json, ASSUMED).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PATCH /api/v1/learning-materials/{id}
- UI requirements: Metadata panel in Document viewer with review state of each tag.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Unreviewed tags -> not used for recommendations.
- Acceptance criteria: Every tag records its method and review status; licence metadata is required before AI generation is enabled.
- Future extensions: LLM-assisted tagging with review (MAT-022).

## [MAT-012] Embedding generation

- Description: Creates vector embeddings for chunks through the embedding provider interface, recording model and dimension.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Enables semantic search and RAG.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Chunk text.
- AI involvement: Embedding model behind an interface (embedding provider: Decision required, DECISIONS.md DEC-006).
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - no application code; embedding provider not selected.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Processing job step
- UI requirements: None beyond status.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Provider unavailable -> retry with backoff; model change -> re-embedding job.
- Acceptance criteria: Every embedding stores model ID, dimension and created_at; switching models never mixes vectors from different models in one index.
- Future extensions: Multilingual embeddings for Hindi.

## [MAT-013] Vector storage

- Description: Stores embeddings in PostgreSQL with pgvector, scoped by organisation and document ACL.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: One database for relational and vector data.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Embedding vectors.
- AI involvement: None.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal service
- UI requirements: None.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Index build failure -> search degrades to keyword mode with notice.
- Acceptance criteria: Vector queries always filter by organisation and access scope; index type documented (DATA_MODEL.md).
- Future extensions: Dedicated vector store only if scale requires it (SYSTEM_ARCHITECTURE.md).

## [MAT-014] Semantic search

- Description: Finds passages by meaning across documents the user may access.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Discovers relevant content without exact keywords.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Embeddings; ACLs.
- AI involvement: Embedding similarity.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/search (mode=semantic)
- UI requirements: Search in Document library with page-linked results.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Embedding service down -> fall back to keyword search with visible notice.
- Acceptance criteria: Results never include documents the user cannot access; each result links to document and page.
- Future extensions: Hybrid ranking (MAT-016).

## [MAT-015] Keyword search

- Description: Full-text search using PostgreSQL text search, important for acronyms such as PLFS, CPI and NSS.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Exact-term lookup for statistical terminology.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Chunk text with full-text index.
- AI involvement: None.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/search (mode=keyword)
- UI requirements: Search mode toggle in Document library.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Query syntax error -> treated as plain text.
- Acceptance criteria: Exact acronyms are found; ACL filtering identical to semantic search.
- Future extensions: Hindi text-search configuration.

## [MAT-016] Hybrid search

- Description: Combines semantic and keyword results with a fusion ranking.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Better recall and precision than either mode alone.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Both indexes.
- AI involvement: Rank fusion (e.g. reciprocal rank fusion) - to be evaluated.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/search (mode=hybrid, P1)
- UI requirements: Default search mode after evaluation.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: One mode fails -> results from the other mode with notice.
- Acceptance criteria: Adopted only if offline evaluation shows improvement over P0 modes.
- Future extensions: Reranking model (AI_SYSTEM_SPEC.md §15).

## [MAT-017] Document Q&A

- Description: Answers a user's question using only retrieved passages from accessible documents, with citations, or abstains.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Fast, source-grounded answers from official material.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: MAT-014; MAT-019; RAI-001; RAI-015
- Data required: Retrieved chunks; question.
- AI involvement: RAG with LLM behind provider interface (AI_SYSTEM_SPEC.md §11).
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/document-qa
- UI requirements: Document Q&A screen with citation list and confidence/abstention display.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: No sufficiently relevant passage -> abstain; citation verification fails -> answer withheld and abstention shown.
- Acceptance criteria: Every displayed answer has at least one verified citation to an accessible document page; otherwise the system abstains; every interaction is logged.
- Future extensions: Conversational tutor (TUT-001).

## [MAT-018] RAG responses

- Description: Orchestrates retrieval, prompt assembly, generation, citation verification and abstention for grounded answers.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Single controlled pipeline for all grounded generation.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: MAT-013; RAI-007; RAI-019
- Data required: Chunks, prompt template versions.
- AI involvement: LLM generation with retrieved context treated as untrusted data.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal service used by POST /api/v1/document-qa
- UI requirements: None directly.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Provider error -> safe error state; prompt-injection indicators -> response restricted and flagged.
- Acceptance criteria: Pipeline logs retrieved chunk IDs, prompt version, model, citations and verification result for every response.
- Future extensions: Tool-augmented retrieval (P2).

## [MAT-019] Source citations

- Description: Attaches citations (document, page, quoted span) to generated answers and questions.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Users can verify every claim against official material.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: MAT-010; RAI-002
- Data required: Chunk provenance; source URL and organisation.
- AI involvement: Citation generation plus automated verification (AI_SYSTEM_SPEC.md §16-17).
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Citation objects in document-qa and question responses
- UI requirements: Citation chips opening Document viewer at the cited page.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Cited span not found in chunk -> citation rejected.
- Acceptance criteria: Every citation resolves to an existing, accessible chunk and its quoted span matches the source text.
- Future extensions: Paragraph-level anchors.

## [MAT-020] Page-level citations where possible

- Description: Shows page numbers for citations whenever page boundaries are known (PDF); formats without pages cite section or offset.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Precise verification in long manuals (e.g. 353-page NAS Sources and Methods).
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: MAT-019
- Data required: Chunk page spans.
- AI involvement: None beyond MAT-019.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Citation.page_start / page_end
- UI requirements: 'p. 12' labels; viewer opens at page.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Page unknown -> citation shows section/offset and no page claim.
- Acceptance criteria: A page number is never shown unless derived from the source page mapping.
- Future extensions: Line-level highlighting.

## [MAT-021] Document summaries

- Description: Generates reviewed summaries of documents or sections with citations.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Faster orientation in long documents.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: MAT-019; RAI-006
- Data required: Chunks.
- AI involvement: LLM summarisation with citations.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/documents/{id}/summaries (P1)
- UI requirements: Summary tab in Document viewer with review badge.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Citation verification failure -> summary not displayed.
- Acceptance criteria: Summaries show citations and review status; unreviewed summaries are labelled.
- Future extensions: Section-level summaries.

## [MAT-022] Topic extraction

- Description: Suggests topics from the taxonomy for documents and chunks.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Better filtering and linkage to competencies.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Chunks; topic taxonomy.
- AI involvement: LLM or classifier suggestions; keyword rules exist today.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Partially implemented - keyword rules only (scripts/processing/topic_taxonomy.json), ASSUMED status, offline.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-materials/{id}/topic-suggestions (P1)
- UI requirements: Tag suggestions with accept/reject.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Low-confidence suggestion -> not proposed.
- Acceptance criteria: Suggested topics are ASSUMED until accepted by a reviewer.
- Future extensions: Taxonomy expansion proposals.

## [MAT-023] Keyword extraction

- Description: Extracts key terms per document for search facets.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Improves discoverability.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Chunks.
- AI involvement: Statistical term extraction; optional LLM.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Processing job step (P1)
- UI requirements: Keyword facets in Document library.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Noisy terms -> filtered by stop-list.
- Acceptance criteria: Keywords shown with method label.
- Future extensions: Glossary building.

## [MAT-024] Concept extraction

- Description: Identifies statistical concepts and relations for a knowledge graph.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Foundation for competency graph and knowledge tracing.
- Priority: P2
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Chunks; concept vocabulary.
- AI involvement: LLM extraction with review.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Hallucinated concepts -> rejected by source-span check.
- Acceptance criteria: Every concept links to a source span.
- Future extensions: Competency graph (CMP-014).

## [MAT-025] Difficulty estimation

- Description: Estimates reading difficulty of materials.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Matches material to learner level.
- Priority: P2
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Text statistics; learner outcomes.
- AI involvement: Readability metrics plus calibration.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Difficulty badge.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Uncalibrated -> not shown.
- Acceptance criteria: Shown only after calibration against learner data.
- Future extensions: Difficulty-based recommendations (PER-008).

## [MAT-026] Course categorization

- Description: Suggests categories and competencies for courses and materials.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Faster catalogue curation.
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Course metadata; taxonomy.
- AI involvement: Classifier/LLM suggestions with review.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/courses/{id}/category-suggestions (P1)
- UI requirements: Suggestion review in course management.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Conflicting categories -> reviewer decides.
- Acceptance criteria: No category is applied without reviewer acceptance.
- Future extensions: Automatic mapping of iGOT courses (IGOT-003).

## [MAT-027] Document versioning

- Description: Links new uploads as versions of an existing material and marks superseded versions.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Keeps citations stable while content evolves (e.g. revised CPI series).
- Priority: P1
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: Document SHA-256; version chain.
- AI involvement: None.
- Human review required: Required when superseding a version cited by approved questions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-materials/{id}/documents (version), GET /api/v1/learning-materials/{id}/versions (P1)
- UI requirements: Version history in Document viewer.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Questions citing a superseded version -> flagged for review.
- Acceptance criteria: Citations always reference the exact version used; superseded versions stay viewable to authorised users.
- Future extensions: Diff view.

## [MAT-028] Document access control

- Description: Restricts document visibility by organisation, department and access scope; enforced in search, Q&A, generation and download.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Prevents exposure of restricted training material.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-002; SEC-012
- Data required: Material access scope; user access roles.
- AI involvement: Retrieval filters exclude inaccessible chunks before any AI call.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Enforced on all document, search, qa and generation endpoints
- UI requirements: Access scope selector on upload; 'restricted' indicators.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: ACL misconfiguration -> default deny.
- Acceptance criteria: A user can never retrieve, cite or download a chunk from a document outside their scope; covered by automated authorisation tests.
- Future extensions: Attribute-based policies (P2).

## [MAT-029] Processing status

- Description: Tracks each document through uploaded -> extracting -> chunking -> embedding -> ready / needs_ocr / failed.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Users know when material is usable.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: BackgroundJob records.
- AI involvement: None.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Partially implemented - offline collection logs record statuses (data/interim/*/collection_log.json); no application pipeline.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/documents/{id}; GET /api/v1/jobs/{id}
- UI requirements: Status chips and progress in Document library.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Stuck job -> timeout marks failed with reason.
- Acceptance criteria: Status reflects the latest job state within one polling interval; failures show a reason and retry action.
- Future extensions: Push updates (P1).

## [MAT-030] Failed-processing recovery

- Description: Retries failed processing steps idempotently and allows manual reprocessing.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Transient failures do not lose uploads.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: AUT-013; AUT-015
- Data required: Job attempts and errors.
- AI involvement: None.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/documents/{id}/reprocess
- UI requirements: Retry button on failed documents.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Repeated failure -> dead-letter state visible to platform administrator.
- Acceptance criteria: Reprocessing never duplicates chunks or embeddings; retry count and errors recorded.
- Future extensions: Automatic remediation hints.

## [MAT-031] Duplicate-document detection

- Description: Detects exact duplicates by SHA-256 at upload; near-duplicate detection is future work.
- Primary user: Trainer
- Secondary users: Learner; Organization administrator
- Business value: Avoids duplicate indexing and conflicting citations.
- Priority: P0
- Product area: Learning material intelligence
- Dependencies: SEC-012 (document ACL); AUT-012 (background jobs)
- Data required: File hashes.
- AI involvement: None.
- Human review required: Uploader attests right-to-use and absence of personal data; materials with restricted licences are excluded from AI generation (DATA_PROVENANCE.md).
- MVP status: In MVP
- Implementation status: Partially implemented - SHA-256 checksums in collector sidecars (data/raw/*/*.meta.json); no upload flow.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Upload response indicates duplicate_of
- UI requirements: Duplicate notice with link to existing material.
- Security considerations: File-type and signature validation, size limits, malware-scanning placeholder, document ACLs, no execution of embedded content (SECURITY_RESPONSIBLE_AI.md §Upload).
- Accessibility considerations: Upload and processing status keyboard-operable with live-region announcements; text alternatives for document previews.
- Failure cases: Hash collision (theoretical) -> byte comparison.
- Acceptance criteria: Uploading identical bytes links to the existing document instead of re-processing.
- Future extensions: Near-duplicate detection via embeddings (P1).

---

# C. Quiz and assessment engine


## [ASM-001] MCQs

- Description: Single-correct multiple-choice questions with four options, explanation and source citation.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Objective, scalable measurement for initial assessment.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007; ASM-027
- Data required: Question, QuestionOption, Citation.
- AI involvement: Generated by AI-007 or authored manually (TRN-008).
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/POST /api/v1/questions; GET /api/v1/questions/{id}
- UI requirements: Assessment screen radio group; Quiz review editor.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Fewer than two options or no correct option -> validation error.
- Acceptance criteria: An MCQ is usable only with exactly one correct option, an explanation, a citation and approved status.
- Future extensions: Multi-select MCQ (P1).

## [ASM-002] True/false questions

- Description: Binary statements with explanation and citation.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Quick checks of factual understanding.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question.
- AI involvement: Generation P1.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Question type 'true_false' (P1)
- UI requirements: Two-option control.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Ambiguous statement -> validation flag.
- Acceptance criteria: Same approval and citation rules as MCQ.
- Future extensions: Confidence-weighted answers.

## [ASM-003] Fill-in-the-blank questions

- Description: Short exact or pattern-matched answers.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Tests recall of definitions and terms.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question with accepted answers.
- AI involvement: Generation P1.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Question type 'fill_blank' (P1)
- UI requirements: Text input with accessible label.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Multiple valid spellings -> accepted-answer list.
- Acceptance criteria: Accepted answers reviewed by a human.
- Future extensions: Numeric-tolerance answers.

## [ASM-004] Scenario-based questions

- Description: Short work scenarios from statistical practice with structured choices or rubric answers.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Measures applied judgement.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Scenario text; rubric.
- AI involvement: Generation P1; evaluation AI-011.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Question type 'scenario' (P1)
- UI requirements: Scenario panel with question.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Scenario not grounded in sources -> rejected.
- Acceptance criteria: Scenarios cite the methodology they draw on.
- Future extensions: Simulations (FUT-017).

## [ASM-005] Case-based questions

- Description: Question sets sharing a longer case.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Deeper assessment of analytical reasoning.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Case, linked questions.
- AI involvement: Generation P1.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Question type 'case' (P1)
- UI requirements: Case pane with question navigation.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Case edited after approval -> linked questions re-reviewed.
- Acceptance criteria: All questions of a case share one approved case version.
- Future extensions: Data-exercise cases.

## [ASM-006] Difficulty levels

- Description: Tags each question as foundational, intermediate or advanced (reviewer-confirmed).
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Weighted scoring and balanced assessments.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question.difficulty.
- AI involvement: Proposed by generator; confirmed by reviewer.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): difficulty field on questions and generation jobs
- UI requirements: Difficulty selector in Quiz builder and review.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Missing difficulty -> cannot approve.
- Acceptance criteria: Every approved question has a reviewer-confirmed difficulty.
- Future extensions: Empirical difficulty (ASM-026).

## [ASM-007] Custom question count

- Description: Lets trainers choose how many questions to generate or include (within configured limits).
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Fits assessments to available time.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Generation parameters.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): count parameter on generation jobs and assessment blueprints
- UI requirements: Numeric input with min/max hints.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Requested count above available approved questions -> warning and actual count shown.
- Acceptance criteria: The assessment never silently contains fewer questions than configured without a visible warning.
- Future extensions: Blueprint templates.

## [ASM-008] Topic-based quizzes

- Description: Builds quizzes restricted to selected topics.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Targeted practice on specific methodology areas.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question topic tags (reviewed).
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/assessments (blueprint with topic filters)
- UI requirements: Topic multi-select in Quiz builder.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: No approved questions for topic -> blocked with message.
- Acceptance criteria: Quizzes contain only approved questions with the selected topics.
- Future extensions: Adaptive topic mixing.

## [ASM-009] Competency-based quizzes

- Description: Builds quizzes covering selected competencies with per-competency minimum item counts.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Produces sufficient evidence for competency estimates.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question competency tags.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/assessments (blueprint with competency filters)
- UI requirements: Competency selector showing available approved item counts.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Insufficient items -> blueprint cannot be published.
- Acceptance criteria: A competency-based quiz can be published only when each competency meets its minimum approved-item count.
- Future extensions: Adaptive assessment (AI-008).

## [ASM-010] Role-based quizzes

- Description: Generates the initial assessment blueprint from the competencies required by a job role.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: One-click initial assessment per role.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: ROLE-002; ROLE-004
- Data required: RoleCompetency; approved questions.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/assessments (blueprint from job_role_id)
- UI requirements: Role selector in Quiz builder.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Role without mapped competencies -> blocked.
- Acceptance criteria: Blueprint covers every competency mapped to the role or lists the competencies lacking items.
- Future extensions: Role readiness (ROLE-008).

## [ASM-011] Pre-assessment

- Description: Initial assessment taken after role selection, establishing baseline estimates.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Baseline for gaps and later before-vs-after comparison.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Assessment with purpose 'pre'.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Assessment.purpose = 'pre'
- UI requirements: Onboarding step and dashboard prompt.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Learner skips -> dashboard shows 'baseline pending'.
- Acceptance criteria: A learner's first completed pre-assessment is stored as the baseline and never overwritten.
- Future extensions: Post-assessment (ASM-012).

## [ASM-012] Post-assessment

- Description: Reassessment after learning to measure change against baseline.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Evidence of improvement.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Assessment purpose 'post'; baseline.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Assessment.purpose = 'post' (P1)
- UI requirements: Before-vs-after view (PRO-008).
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Different item pools -> comparison caveat shown.
- Acceptance criteria: Comparisons show caveats when item pools differ.
- Future extensions: Equated forms via IRT (FUT-006).

## [ASM-013] Certification assessment

- Description: Formal assessments leading to certificates.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Recognised credentials.
- Priority: P2
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Secure item pools; proctoring policy.
- AI involvement: None decided.
- Human review required: Required: certification outcomes need human sign-off.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Integrity breach -> attempt invalidated by human decision.
- Acceptance criteria: Not built until governance for certification is approved.
- Future extensions: AI certification (FUT-007).

## [ASM-014] Randomization

- Description: Randomises question order and option order per attempt, recorded for reproducibility.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Reduces answer sharing and position bias.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Attempt seed.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Attempt stores randomisation seed
- UI requirements: None visible.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Seed missing -> attempt invalid.
- Acceptance criteria: Each attempt stores its seed; the delivered order can be reconstructed exactly.
- Future extensions: Parallel forms.

## [ASM-015] Timers

- Description: Optional time limits with accessibility extensions.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Standardised conditions where required.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Assessment time limit; accommodations.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Assessment.time_limit (P1)
- UI requirements: Accessible countdown with warnings.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Connection loss -> server-side time is authoritative.
- Acceptance criteria: Timer extensions can be granted per user and are audited.
- Future extensions: Pause policies.

## [ASM-016] Attempt limits

- Description: Limits the number of attempts per assessment.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Prevents trial-and-error gaming.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Attempt counts.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Assessment.max_attempts (P1)
- UI requirements: Remaining attempts indicator.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Limit reached -> start disabled with explanation.
- Acceptance criteria: Limits enforced server-side.
- Future extensions: Cool-down periods.

## [ASM-017] Auto-evaluation

- Description: Automatically scores objective questions on submission.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Immediate results.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-009
- Data required: Answers; keys.
- AI involvement: None (see AI-009).
- Human review required: Not required for objective items.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/attempts/{id}/submit
- UI requirements: Results screen.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Scoring error -> attempt marked 'scoring_failed' and retried.
- Acceptance criteria: Submission returns a result or a retryable pending state; never a partial silent score.
- Future extensions: Short-answer evaluation (AI-010).

## [ASM-018] Manual evaluation

- Description: Trainer scoring of subjective answers with rubric.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Human judgement where automation is unsuitable.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Answers; rubrics.
- AI involvement: None (AI may pre-score in P1).
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/answers/{id}/evaluations (P1)
- UI requirements: Grading queue for trainers.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Grader conflict -> second review.
- Acceptance criteria: Manual scores record grader and rationale.
- Future extensions: Moderation workflows.

## [ASM-019] Feedback

- Description: Shows per-question correctness after submission (when the assessment policy allows).
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Learning from assessment.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Answers; keys.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/attempts/{id}/result
- UI requirements: Result list with correct/incorrect indicators (icon + text).
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Policy hides answers -> only scores shown.
- Acceptance criteria: Feedback visibility follows the assessment policy and never exposes other learners' data.
- Future extensions: Personalised feedback (P1).

## [ASM-020] Explanations

- Description: Each approved question includes an explanation of the correct answer.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Turns assessment into learning.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question.explanation.
- AI involvement: Drafted by generator; reviewed.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Explanation included in result when policy allows
- UI requirements: Expandable explanation under each result item.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Missing explanation -> question cannot be approved.
- Acceptance criteria: Every approved question has a reviewed explanation.
- Future extensions: Explanations at multiple levels (TUT-005).

## [ASM-021] Source evidence

- Description: Each approved question cites the document page and passage it is based on.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Verifiability of every assessed fact.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: MAT-019
- Data required: Citation linked to question version.
- AI involvement: Generated citations verified automatically (RAI-002).
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Citations included in question and result payloads
- UI requirements: 'Source' link opening Document viewer.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Cited document access revoked -> question suspended from use.
- Acceptance criteria: An approved question always has a verified citation to an accessible document version.
- Future extensions: Multiple-source evidence.

## [ASM-022] Duplicate detection

- Description: Detects exact and near-duplicate questions within the question bank before review.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Keeps the bank clean and assessments fair.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: MAT-012
- Data required: Normalised question text; embeddings.
- AI involvement: Text normalisation hash + embedding similarity (threshold to be calibrated).
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Validation result on question
- UI requirements: Duplicate warning with link in Quiz review.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Embedding unavailable -> exact-duplicate check only, flagged.
- Acceptance criteria: Exact duplicates are blocked; suspected near-duplicates are flagged for the reviewer.
- Future extensions: Cross-language duplicates.

## [ASM-023] Incorrect-answer detection

- Description: An independent validation call answers the question from the cited source without seeing the key; disagreement flags the question.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Catches wrong answer keys before review.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question, options, cited chunk.
- AI involvement: Independent LLM validation (AI_SYSTEM_SPEC.md §22).
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Validation result on question
- UI requirements: 'Key disputed by validator' flag in Quiz review.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Validator unavailable -> question marked 'validation_incomplete' and cannot be approved without explicit reviewer override.
- Acceptance criteria: Disagreement between validator and key is always shown to the reviewer.
- Future extensions: Multi-validator consensus.

## [ASM-024] Hallucination detection

- Description: Checks that the question's evidence span exists verbatim in the cited chunk and that the correct answer is supported by it.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Blocks questions not grounded in sources.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: RAI-004
- Data required: Evidence span; chunk text.
- AI involvement: Deterministic span match plus LLM support check.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Validation result on question
- UI requirements: 'Unsupported by source' flag.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Span not found -> automatic rejection before review.
- Acceptance criteria: No question with an unmatched evidence span reaches the review queue.
- Future extensions: Claim-level entailment models.

## [ASM-025] Question quality scoring

- Description: Scores clarity, distractor plausibility and alignment.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Prioritises reviewer attention.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question; validator outputs.
- AI involvement: LLM rubric plus heuristics.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Quality fields on question (P1)
- UI requirements: Quality badge in review queue.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Unscored -> neutral.
- Acceptance criteria: Quality score never approves a question on its own.
- Future extensions: Learner-response analytics (ASM-026).

## [ASM-026] Difficulty scoring

- Description: Estimates empirical difficulty from learner responses.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Calibrates weights and adaptive selection.
- Priority: P1
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Answer statistics.
- AI involvement: Classical test statistics (P1); IRT (P2).
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Question statistics (P1)
- UI requirements: Item statistics in question details.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Too few responses -> not computed.
- Acceptance criteria: Statistics computed only above a minimum response count.
- Future extensions: IRT (FUT-006).

## [ASM-027] Question review workflow

- Description: Routes validated questions into a review queue with validator findings, source and history.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Human oversight of all AI-generated assessment content.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: ReviewTask; QuestionValidation.
- AI involvement: None in the workflow itself.
- Human review required: This feature is the human review.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/review-tasks; GET /api/v1/review-tasks/{id}; POST /api/v1/review-tasks/{id}/decision
- UI requirements: Quiz review screen.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Reviewer lacks access to source -> task reassigned.
- Acceptance criteria: Every AI-generated question passes through a review task; queue shows validator flags and source passage side by side.
- Future extensions: Dual review for certification items (P2).

## [ASM-028] Question approval

- Description: Reviewer approves a question version for use.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Only reviewed content reaches learners.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Approval record.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/review-tasks/{id}/decision (approve)
- UI requirements: Approve action with confirmation.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Unresolved validation flags -> approval requires a written override reason.
- Acceptance criteria: Approval records reviewer, timestamp, version and override reasons; self-approval of one's own manual questions is blocked when a second reviewer is configured.
- Future extensions: Approval policies per assessment type.

## [ASM-029] Question rejection

- Description: Reviewer rejects a question with a reason category.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Improves generation through feedback.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Approval record with reason.
- AI involvement: Rejection reasons feed evaluation datasets.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/review-tasks/{id}/decision (reject)
- UI requirements: Reject action with reason picker.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Missing reason -> blocked.
- Acceptance criteria: Every rejection has a reason; rejected questions are never used.
- Future extensions: Automatic prompt improvement proposals (P1).

## [ASM-030] Question editing

- Description: Reviewer edits a question; the edit creates a new version that is re-validated.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Fix small issues without regenerating.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question versions.
- AI involvement: Re-validation of edited version.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PATCH /api/v1/questions/{id} (creates version)
- UI requirements: Inline editor in Quiz review.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Edit breaks evidence match -> re-validation flags it.
- Acceptance criteria: Edits never modify an approved version in place; AI-generated vs human-edited fields are distinguishable.
- Future extensions: Suggested edits.

## [ASM-031] Question versioning

- Description: Immutable versions of questions referenced by attempts and approvals.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Auditability and correct re-scoring.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: Question version chain.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/questions/{id}/versions
- UI requirements: Version history panel.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Attempt references missing version -> integrity error.
- Acceptance criteria: Attempts always reference the exact version delivered.
- Future extensions: Version diffs.

## [ASM-032] Assessment history

- Description: Lists a learner's attempts with dates, scores and assessment versions.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator
- Business value: Transparency and progress tracking.
- Priority: P0
- Product area: Quiz and assessment engine
- Dependencies: AI-007 (generation); ASM-027 (approval); SEC-002 (RBAC)
- Data required: AssessmentAttempt.
- AI involvement: None.
- Human review required: Required for every AI-generated question before use; edits create new versions.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/attempts; GET /api/v1/users/{id}/attempts (scoped roles)
- UI requirements: History list on Competency profile.
- Security considerations: Answer keys never sent to the client before submission; attempts bound to the authenticated user; organisation scoping; audit of edits and approvals.
- Accessibility considerations: All question types operable by keyboard and screen reader; timers configurable with accommodations; no colour-only feedback.
- Failure cases: Deleted assessment -> history retained read-only.
- Acceptance criteria: Learners see all their own attempts; scoped roles see only permitted users.
- Future extensions: Assessment timeline (PRO-013).

---

# D. Competency intelligence


## [CMP-001] Learner competency profile

- Description: Shows the learner's job role, competencies required by that role, current estimates, evidence-sufficiency bands and gaps.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Single place for a learner to understand their development position.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-012; AI-018; ROLE-001
- Data required: UserCompetency; RoleCompetency; framework metadata.
- AI involvement: None (displays deterministic estimates).
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/competency-profile; GET /api/v1/users/{id}/competency-profile
- UI requirements: Competency profile screen.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: No estimates yet -> call to action to take the pre-assessment.
- Acceptance criteria: Profile shows only the learner's own data (or scoped access); each estimate links to explanation and evidence.
- Future extensions: Skill passport (CMP-015).

## [CMP-002] Competency scores

- Description: Numeric score and mapped level per competency with method version.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Comparable measures over time.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-012
- Data required: UserCompetency.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in competency profile
- UI requirements: Score and level with band.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Levels not configured -> score only with notice.
- Acceptance criteria: Scores are reproducible from evidence and method version.
- Future extensions: IRT-based scaling (FUT-006).

## [CMP-003] Competency heatmap

- Description: Grid of competencies by learners or departments coloured by level, with accessible table view.
- Primary user: Department administrator
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Quick visual scan of capability.
- Priority: P1
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Aggregated estimates with minimum group size.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/competency-heatmap (P1)
- UI requirements: Department heatmap screen.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Group smaller than minimum -> cell suppressed.
- Acceptance criteria: Heatmap never reveals individuals below the minimum group size to unauthorised roles.
- Future extensions: Trend overlays.

## [CMP-004] Competency-gap analysis

- Description: Detailed gap view: required vs estimated level, evidence, and recommended actions.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Clear development priorities.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-002
- Data required: Gaps (AI-002); recommendations.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/competency-gaps
- UI requirements: Competency-gap analysis screen.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Insufficient evidence -> 'reassess to confirm' instead of a gap.
- Acceptance criteria: Each gap shows required level, estimate, band, evidence link and at least one action or an 'no approved content' note.
- Future extensions: Critical skills (CMP-005).

## [CMP-005] Critical skills

- Description: Marks competencies as critical for a role so their gaps are prioritised.
- Primary user: Competency framework administrator
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Aligns development with role-critical work.
- Priority: P1
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: RoleCompetency.is_critical.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PUT /api/v1/job-roles/{id}/competencies (is_critical, P1)
- UI requirements: Critical badge in gap analysis.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Unconfigured -> all equal.
- Acceptance criteria: Critical flags set only by competency framework administrators.
- Future extensions: Weighted readiness (ROLE-008).

## [CMP-006] Strengths

- Description: Lists competencies at or above the required level with sufficient evidence.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Balanced, motivating view of capability.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Estimates vs required levels.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in competency profile
- UI requirements: Strengths section on profile.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Insufficient evidence -> not listed as strength.
- Acceptance criteria: A strength requires evidence sufficiency of at least 'medium'.
- Future extensions: Peer mentoring suggestions (P2).

## [CMP-007] Developing skills

- Description: Lists competencies below the required level (gaps) in plain language.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Non-judgemental framing of gaps.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Gaps.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in competency profile
- UI requirements: 'Developing' section on profile.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Same as CMP-004.
- Acceptance criteria: Wording avoids evaluative labels about the person (UI_UX_SPEC.md content guidelines).
- Future extensions: Progress nudges (P1).

## [CMP-008] Required-versus-current comparison

- Description: Side-by-side comparison of required and current levels per competency.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Makes gaps concrete.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: RoleCompetency; UserCompetency.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in competency-gap response
- UI requirements: Accessible comparison chart with table view.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Missing required level -> 'not configured'.
- Acceptance criteria: Chart and table show identical values; both are keyboard and screen-reader accessible.
- Future extensions: Target-role comparison (ROLE-010).

## [CMP-009] Competency dependencies

- Description: Models prerequisite relations between competencies.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Enables prerequisite-aware paths.
- Priority: P2
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Competency relations.
- AI involvement: None / expert-authored.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Dependency editor (P2).
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Cycles -> rejected.
- Acceptance criteria: Relations authored by competency administrators only.
- Future extensions: Competency graph (CMP-014).

## [CMP-010] Competency progression

- Description: Shows how estimates changed across attempts.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Evidence of development over time.
- Priority: P1
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Historical UserCompetency snapshots.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/competency-history (P1)
- UI requirements: Progression chart with table.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Method version changed -> series break annotated.
- Acceptance criteria: Series breaks are annotated when method versions differ.
- Future extensions: Forecasting (P2).

## [CMP-011] Knowledge tracking

- Description: Tracks mastery of individual knowledge components.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Fine-grained personalisation.
- Priority: P2
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Response-level data.
- AI involvement: Knowledge tracing (FUT-004).
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Sparse data -> no estimate.
- Acceptance criteria: Not built before P2 validation.
- Future extensions: BKT (FUT-005).

## [CMP-012] Topic tracking

- Description: Tracks performance by topic across attempts.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Targeted revision.
- Priority: P1
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Answers with topics.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/topic-progress (P1)
- UI requirements: Topic panel.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Unreviewed topic tags -> excluded.
- Acceptance criteria: Only reviewed topic tags are used.
- Future extensions: Weak-topic detection (AI-014).

## [CMP-013] Improvement tracking

- Description: Quantifies change between baseline and later estimates.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Demonstrates learning impact.
- Priority: P1
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Baseline and post estimates.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/improvement (P1)
- UI requirements: Improvement summary with caveats.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Non-comparable assessments -> caveat.
- Acceptance criteria: Improvement shown only between comparable assessments or with an explicit caveat.
- Future extensions: Training effectiveness analytics (ANA-008).

## [CMP-014] Competency graph

- Description: Visual graph linking competencies, topics, courses and evidence.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Explains relationships behind recommendations.
- Priority: P1
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Mappings.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/competency-graph (P1)
- UI requirements: Interactive graph with list alternative.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Large graph -> filtered view.
- Acceptance criteria: Every node reachable via a keyboard-accessible list view.
- Future extensions: Concept graph (MAT-024).

## [CMP-015] Skill passport

- Description: Portable summary of verified competencies and evidence.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Recognition across postings.
- Priority: P2
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Human-verified estimates.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Unverified estimates -> excluded.
- Acceptance criteria: Contains only human-verified entries; sharing controlled by the learner.
- Future extensions: Competency passport (FUT-008).

## [CMP-016] Evidence ledger

- Description: Append-only record of evidence contributing to each competency estimate.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Auditability and contestability.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: CompetencyEvidence (append-only with void markers).
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/users/{id}/competencies/{competency_id}/evidence
- UI requirements: Evidence panel.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Attempt to edit evidence -> blocked; voiding requires reason.
- Acceptance criteria: Evidence records are never deleted or edited in place; voids record who, when and why.
- Future extensions: Verifiable credentials (P2).

## [CMP-017] Assessment history (competency view)

> Alias of **ASM-032** - see that entry for the full specification.

- Description: Competency-filtered view of assessment history.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Shows which attempts shaped each estimate.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: ASM-032
- Data required: Attempts; evidence.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/attempts?competency_id=
- UI requirements: Filter in history list.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: None specific.
- Acceptance criteria: Filtering shows only attempts with evidence for the competency.
- Future extensions: Timeline (PRO-013).

## [CMP-018] Learning evidence

- Description: Records completed learning activities as supporting (non-assessment) evidence, clearly distinguished from assessed evidence.
- Primary user: Learner
- Secondary users: Trainer; Competency framework administrator; Department administrator
- Business value: Recognises learning effort.
- Priority: P1
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: LearningActivity.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/learning-activities (P1 evidence linkage)
- UI requirements: Evidence panel with type labels.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Self-reported activity -> labelled self-reported.
- Acceptance criteria: Learning evidence never changes a score without an assessment or human adjustment.
- Future extensions: Evidence timeline (PRO-014).

## [CMP-019] Human-reviewed competency adjustments

- Description: Authorised reviewers adjust an estimate with a mandatory reason; the learner is notified and can request correction.
- Primary user: Trainer
- Secondary users: Competency framework administrator; Learner
- Business value: Human oversight of automated estimates.
- Priority: P0
- Product area: Competency intelligence
- Dependencies: AI-012 (score calculation); ADM-004 (competency management)
- Data required: Adjustment record as CompetencyEvidence; ReviewTask.
- AI involvement: None.
- Human review required: Adjustments only by authorised reviewers with a reason; learners can request corrections (RAI-018).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/user-competencies/{id}/adjustments
- UI requirements: Adjustment dialog in trainer/admin views; change visible on learner profile.
- Security considerations: Competency data is personal data: visible to the learner, assigned trainers and scoped administrators only; never used for automated employment decisions.
- Accessibility considerations: Heatmaps and graphs have table equivalents; colour is never the only signal.
- Failure cases: Missing reason -> blocked; reviewer adjusting own record -> blocked.
- Acceptance criteria: Every adjustment stores reviewer, reason, previous and new values; users cannot adjust their own estimates.
- Future extensions: Moderation panels (P1).

---

# E. Role intelligence


## [ROLE-001] Job-role selection

- Description: Learner selects department and job role during onboarding (changeable later with audit).
- Primary user: Learner
- Secondary users: Department administrator
- Business value: Anchors requirements, assessments and recommendations.
- Priority: P0
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: JobRole list; Department list.
- AI involvement: None in MVP (AI suggestion is AI-003, P1).
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/job-roles; PUT /api/v1/me/job-role
- UI requirements: Onboarding role step; Settings.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: No roles configured -> onboarding blocked with administrator contact message.
- Acceptance criteria: A learner cannot start the pre-assessment without a selected role; role changes are audited.
- Future extensions: AI role suggestion (AI-003).

## [ROLE-002] Role-to-competency mapping

- Description: Defines which competencies each job role needs and the required level for each.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Required input for gap detection.
- Priority: P0
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: RoleCompetency.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: In MVP
- Implementation status: Requires human confirmation - no official role-to-competency mapping exists in collected data; must be authored and approved (ASSUMPTIONS_AND_OPEN_QUESTIONS.md).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/job-roles/{id}/competencies; PUT /api/v1/job-roles/{id}/competencies
- UI requirements: Role editor in Admin dashboard.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Mapping references inactive competency -> blocked.
- Acceptance criteria: Mappings are versioned, approved by a competency framework administrator, and visible to learners of the role.
- Future extensions: Role versioning (ROLE-012).

## [ROLE-003] Role-to-course mapping

- Description: Associates recommended or mandatory courses with job roles.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Role-specific catalogues.
- Priority: P1
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: RoleCourse link.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PUT /api/v1/job-roles/{id}/courses (P1)
- UI requirements: Role editor tab.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Course retired -> mapping flagged.
- Acceptance criteria: Mandatory flags set only by authorised administrators.
- Future extensions: Role-specific paths (ROLE-006).

## [ROLE-004] Role-to-assessment mapping

- Description: Links each job role to its initial assessment blueprint.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Correct assessment per role without manual lookup.
- Priority: P0
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Assessment.job_role_id.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Assessment blueprint job_role_id; GET /api/v1/job-roles/{id}/assessments
- UI requirements: Role editor shows linked assessments.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: No published assessment for role -> learner sees 'assessment not yet available'.
- Acceptance criteria: Each role with learners has at most one active pre-assessment at a time.
- Future extensions: Multiple assessment tracks (P1).

## [ROLE-005] Role-to-skill mapping

- Description: Maps finer-grained skills (topics) to roles.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Topic-level targeting.
- Priority: P1
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Role-topic links.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Role editor tab.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Unreviewed topics -> excluded.
- Acceptance criteria: Uses reviewed taxonomy terms only.
- Future extensions: Skill graph.

## [ROLE-006] Role-specific learning paths

- Description: Curated default paths per role, personalised by gaps.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Consistent baseline development per role.
- Priority: P1
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Role path templates.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Path template editor.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Template empty -> falls back to gap-based path.
- Acceptance criteria: Personalised path always states which template it derives from.
- Future extensions: Career paths (FUT-003).

## [ROLE-007] Role-specific quizzes

> Alias of **ASM-010** - see that entry for the full specification.

- Description: Quizzes scoped to a role's competencies (same capability as ASM-010 from the role perspective).
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Relevance of practice.
- Priority: P0
- Product area: Role intelligence
- Dependencies: ASM-010
- Data required: RoleCompetency; approved questions.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): As ASM-010
- UI requirements: As ASM-010.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: As ASM-010.
- Acceptance criteria: As ASM-010.
- Future extensions: As ASM-010.

## [ROLE-008] Role-readiness score

- Description: Aggregated readiness for the learner's own current role, with evidence and caveats.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Self-development planning.
- Priority: P1
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Estimates; critical flags.
- AI involvement: Rule-based aggregation.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Readiness card with explanation.
- Security considerations: Must not be used for promotion or selection decisions (SECURITY_RESPONSIBLE_AI.md §HID).
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Insufficient evidence -> not shown.
- Acceptance criteria: Shown only to the learner and their trainer; labelled as development guidance, not an eligibility decision.
- Future extensions: Target-role readiness (ROLE-010).

## [ROLE-009] Career-development suggestions

- Description: Suggests development directions based on interests and competencies.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Long-term engagement.
- Priority: P2
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Profile; role catalogue.
- AI involvement: LLM suggestions with review.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Unsupported suggestion -> suppressed.
- Acceptance criteria: Advisory only; not linked to HR processes.
- Future extensions: Career pathways (FUT-003).

## [ROLE-010] Role transition pathways

- Description: Shows competencies needed to move to another role.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Voluntary career planning.
- Priority: P2
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Two role mappings.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Target role not configured -> unavailable.
- Acceptance criteria: Learner-initiated only.
- Future extensions: Capability planning (FUT-018).

## [ROLE-011] Role prerequisites

- Description: Defines prerequisite roles or competencies.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Structured progressions.
- Priority: P2
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Role relations.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Cycles -> rejected.
- Acceptance criteria: Authored by administrators only.
- Future extensions: Career pathways.

## [ROLE-012] Role versioning

- Description: Versions role definitions and mappings so estimates reference the mapping version used.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Historical comparability.
- Priority: P1
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: JobRole version fields.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Version history in role editor.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Learners on old version -> migration prompt.
- Acceptance criteria: Gap results store the role-mapping version.
- Future extensions: Scheduled role changes.

## [ROLE-013] Organization-specific role configuration

- Description: Each organisation defines its own roles and mappings.
- Primary user: Competency framework administrator
- Secondary users: Organization administrator; Learner
- Business value: Supports multiple statistical organisations.
- Priority: P1
- Product area: Role intelligence
- Dependencies: ADM-003 (role management); ADM-004 (competency management)
- Data required: Organisation-scoped JobRole.
- AI involvement: None.
- Human review required: Role-to-competency mappings are authored and approved by competency framework administrators; no official mapping exists in collected data (Requires human confirmation).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1 multi-organisation administration
- UI requirements: Organisation selector for platform administrators.
- Security considerations: Role configuration changes audited; role data scoped to organisation.
- Accessibility considerations: Role selection usable with keyboard and screen reader; searchable lists.
- Failure cases: Cross-organisation reference -> blocked.
- Acceptance criteria: Roles never leak across organisations.
- Future extensions: Shared role templates.

---

# F. Personalization


## [PER-001] Personalized dashboard

- Description: Learner home showing role, baseline status, top gaps, continue-learning items, recommendations and recent activity.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Immediate orientation and next action.
- Priority: P0
- Product area: Personalization
- Dependencies: CMP-001; AI-004; PRO-001
- Data required: Profile, gaps, path, progress.
- AI involvement: None (displays deterministic outputs).
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/dashboard (aggregate)
- UI requirements: Learner dashboard screen.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Partial data failure -> affected card shows its own error with retry.
- Acceptance criteria: Dashboard loads with independent card states; no card shows another user's data.
- Future extensions: Customisable layout (P2).

## [PER-002] Personalized course recommendations

> Alias of **AI-005** - see that entry for the full specification.

- Description: Learner-facing view of AI-005 recommendations.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: See AI-005.
- Priority: P0
- Product area: Personalization
- Dependencies: AI-005
- Data required: See AI-005.
- AI involvement: See AI-005.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: See AI-005.
- UI requirements: Recommendation cards.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: See AI-005.
- Acceptance criteria: See AI-005.
- Future extensions: See AI-005.

## [PER-003] Personalized learning paths

> Alias of **AI-004** - see that entry for the full specification.

- Description: Learner-facing view of AI-004 learning paths with item status controls.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: See AI-004.
- Priority: P0
- Product area: Personalization
- Dependencies: AI-004
- Data required: See AI-004.
- AI involvement: See AI-004.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: See AI-004.
- UI requirements: Learning path screen.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: See AI-004.
- Acceptance criteria: See AI-004.
- Future extensions: See AI-004.

## [PER-004] Daily learning plan

- Description: Short daily plan derived from the path and availability.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Habit formation.
- Priority: P2
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Path; availability.
- AI involvement: Scheduling heuristics.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: No availability -> not generated.
- Acceptance criteria: Opt-in only.
- Future extensions: Workload-aware planning (PER-018).

## [PER-005] Weekly learning plan

- Description: Weekly grouping of path items with estimated effort.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Realistic planning.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Path items with durations.
- AI involvement: Rule-based scheduling.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/plans?period=week (P1)
- UI requirements: Weekly plan view.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Unknown durations -> items unscheduled.
- Acceptance criteria: Plans never mark items overdue without a learner-set goal.
- Future extensions: Calendar sync (UX-006).

## [PER-006] 30-day learning plan

- Description: Month-long plan toward selected gaps.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Medium-term focus.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Path; goals.
- AI involvement: Rule-based scheduling.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/plans?period=30d (P1)
- UI requirements: 30-day plan view.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: As PER-005.
- Acceptance criteria: As PER-005.
- Future extensions: Goal setting (PER-016).

## [PER-007] Prerequisite-based recommendations

- Description: Orders recommendations by prerequisite relations.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Avoids content the learner is not ready for.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Course prerequisites.
- AI involvement: Rule-based.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Prerequisite notes on cards.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Missing prerequisites data -> ignored.
- Acceptance criteria: Prerequisite rules visible in explanation.
- Future extensions: Competency dependencies (CMP-009).

## [PER-008] Difficulty-based recommendations

- Description: Matches content difficulty to estimated level.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Appropriate challenge.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Content difficulty (reviewed).
- AI involvement: Rule-based.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Difficulty labels.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Uncalibrated difficulty -> not used.
- Acceptance criteria: Uses reviewed difficulty only.
- Future extensions: Difficulty estimation (MAT-025).

## [PER-009] Performance-based recommendations

- Description: Uses assessment performance (gaps and weak evidence) as the primary ranking signal.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Focus on measured needs.
- Priority: P0
- Product area: Personalization
- Dependencies: AI-005
- Data required: Gaps; evidence bands.
- AI involvement: Rule-based (part of AI-005).
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in GET /api/v1/me/recommendations
- UI requirements: 'Because of your result in …' reason text.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: No attempts -> role-based defaults.
- Acceptance criteria: Reason text names the assessment result that triggered it.
- Future extensions: Weak-topic signals (AI-014).

## [PER-010] Competency-based recommendations

- Description: Matches content via human-approved competency mappings.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Relevance to role requirements.
- Priority: P0
- Product area: Personalization
- Dependencies: AI-005
- Data required: CourseCompetency links (approved).
- AI involvement: Rule-based (part of AI-005).
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in GET /api/v1/me/recommendations
- UI requirements: Competency chips on cards.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Unapproved mappings -> ignored.
- Acceptance criteria: Only approved mappings influence ranking.
- Future extensions: Competency graph explanations.

## [PER-011] Training-history-based recommendations

- Description: Accounts for completed NSSTA programmes and courses.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Avoids repeats.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Learning history (internal; iGOT sync blocked).
- AI involvement: Rule-based.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: 'Already completed' filters.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: History unavailable -> excluded silently only with notice.
- Acceptance criteria: Excluded items are listed on request.
- Future extensions: iGOT history sync (IGOT-007).

## [PER-012] Study-plan generation

- Description: Generates a study plan document with objectives and resources.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Structured self-study.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Path; materials.
- AI involvement: LLM drafting with citations and review.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Study plan view/export.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Unsupported claims -> removed.
- Acceptance criteria: Plans cite resources; unreviewed plans labelled.
- Future extensions: Tutor integration.

## [PER-013] Revision recommendations

- Description: Suggests revisiting materials linked to missed questions.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Reinforces learning.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Incorrect answers; citations.
- AI involvement: Rule-based.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Revision list on results.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Source unavailable -> skipped.
- Acceptance criteria: Each suggestion cites the missed question's source.
- Future extensions: Spaced repetition (PER-015).

## [PER-014] Practice recommendations

- Description: Suggests practice quizzes on weak topics.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Low-stakes practice.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Weak topics; approved questions.
- AI involvement: Rule-based.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Practice card.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: No questions -> none.
- Acceptance criteria: Practice results do not change estimates unless configured as evidence.
- Future extensions: Adaptive practice.

## [PER-015] Spaced repetition

- Description: Schedules review based on forgetting curves.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Retention.
- Priority: P2
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Response history.
- AI involvement: Scheduling algorithm.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Sparse history -> default intervals.
- Acceptance criteria: Opt-in.
- Future extensions: Knowledge tracing.

## [PER-016] Goal setting

- Description: Learners set target levels and dates for competencies.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Ownership of development.
- Priority: P1
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Goal records.
- AI involvement: None.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/me/goals (P1)
- UI requirements: Goal editor.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Unrealistic date -> warning only.
- Acceptance criteria: Goals are private to the learner unless shared.
- Future extensions: Deadline-aware planning.

## [PER-017] Deadline-aware planning

- Description: Plans around assignment deadlines.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Meets organisational timelines.
- Priority: P2
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Assignments; deadlines.
- AI involvement: Scheduling.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: Conflicting deadlines -> surfaced to trainer.
- Acceptance criteria: No automatic escalation to supervisors.
- Future extensions: Workload-aware planning.

## [PER-018] Workload-aware planning

- Description: Adjusts plans to declared workload.
- Primary user: Learner
- Secondary users: Training manager; Trainer
- Business value: Sustainable learning.
- Priority: P2
- Product area: Personalization
- Dependencies: AI-004 (learning path); AI-005 (recommendations)
- Data required: Learner-declared availability.
- AI involvement: Scheduling.
- Human review required: Recommendations are explainable and dismissible; nothing becomes mandatory without a human assignment.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Personalisation uses only the learner's own data and the organisation's approved catalogue.
- Accessibility considerations: Plans and cards readable by screen readers; no motion-dependent interactions.
- Failure cases: No declaration -> defaults.
- Acceptance criteria: Workload data is learner-declared, never inferred from work systems.
- Future extensions: Resource optimisation (FUT-015).

---

# G. AI learning tutor


## [TUT-001] Conversational tutor

- Description: Multi-turn tutor grounded in approved materials.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Interactive learning support beyond single questions.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Conversation history; retrieved chunks.
- AI involvement: RAG over conversation with abstention.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/tutor/conversations; POST /api/v1/tutor/conversations/{id}/messages (P1)
- UI requirements: Tutor screen.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Provider down -> tutor unavailable banner; off-topic -> redirect.
- Acceptance criteria: Every factual answer is grounded with citations or the tutor abstains.
- Future extensions: Voice tutor (FUT-012).

## [TUT-002] Document-aware tutor

- Description: Tutor scoped to a selected document or material set.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Focused study of a manual.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Selected material IDs.
- AI involvement: Scoped retrieval.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Scope parameter on conversation (P1)
- UI requirements: Scope selector.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Scope inaccessible -> blocked.
- Acceptance criteria: Retrieval never exceeds the selected, accessible scope.
- Future extensions: Multi-document comparison.

## [TUT-003] Explain concepts

- Description: Explains a statistical concept from sources.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Understanding of methodology.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Chunks.
- AI involvement: Grounded explanation.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Tutor message intent 'explain' (P1)
- UI requirements: Explain action on selected text.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Concept absent from sources -> abstain.
- Acceptance criteria: Explanations cite sources.
- Future extensions: Concept graph links.

## [TUT-004] Simplify concepts

- Description: Rephrases a passage in simpler language without changing meaning.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Accessibility for newcomers.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Selected passage.
- AI involvement: LLM rewrite constrained to source.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Intent 'simplify' (P1)
- UI requirements: Simplify action.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Meaning drift detected -> original shown.
- Acceptance criteria: Simplified text shows the original passage alongside.
- Future extensions: Reading-level control.

## [TUT-005] Beginner mode

- Description: Default simpler explanations for new learners.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Onboarding support.
- Priority: P2
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: User preference.
- AI involvement: Prompt variant.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): User setting (P2)
- UI requirements: Settings toggle.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: None specific.
- Acceptance criteria: Grounding rules unchanged.
- Future extensions: Adaptive level.

## [TUT-006] Examples

- Description: Provides examples drawn from or consistent with sources.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Concrete understanding.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Chunks.
- AI involvement: Grounded generation.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Intent 'example' (P1)
- UI requirements: Example action.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Invented statistics -> blocked (examples must not present fabricated official figures).
- Acceptance criteria: Illustrative examples are labelled as illustrative and contain no invented official figures.
- Future extensions: Worked data exercises.

## [TUT-007] Analogies

- Description: Offers analogies for difficult concepts.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Intuition building.
- Priority: P2
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Concept.
- AI involvement: LLM generation labelled as analogy.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Misleading analogy -> learner flag.
- Acceptance criteria: Labelled 'analogy - not from source'.
- Future extensions: None.

## [TUT-008] Practice questions

- Description: Generates practice questions in conversation (not used as evidence).
- Primary user: Learner
- Secondary users: Trainer
- Business value: Self-testing.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Chunks.
- AI involvement: Generation with lightweight validation.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Intent 'practice' (P1)
- UI requirements: Inline practice card.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Validation fails -> not shown.
- Acceptance criteria: Tutor practice questions never count as assessment evidence and are labelled unreviewed.
- Future extensions: Promotion to question bank via review.

## [TUT-009] Summaries

- Description: Summarises a section on request.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Revision aid.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Chunks.
- AI involvement: Grounded summarisation.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Intent 'summarize' (P1)
- UI requirements: Summary card with citations.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Citation verification fails -> withheld.
- Acceptance criteria: Summaries carry citations.
- Future extensions: Reviewed summaries (MAT-021).

## [TUT-010] Notes

- Description: Learner-saved notes from tutor sessions.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Personal study record.
- Priority: P2
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Notes.
- AI involvement: None.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Notes panel.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: None specific.
- Acceptance criteria: Notes private to the learner.
- Future extensions: Export.

## [TUT-011] Follow-up questions

- Description: Suggests follow-up questions to deepen understanding.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Guided exploration.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Conversation.
- AI involvement: LLM suggestions.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in tutor response (P1)
- UI requirements: Suggested question chips.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Suggestion answer unavailable -> chip hidden.
- Acceptance criteria: Suggestions answerable from accessible sources.
- Future extensions: Curriculum-aligned prompts.

## [TUT-012] Conversation context

- Description: Keeps bounded conversation history for coherent replies.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Natural dialogue.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Recent messages.
- AI involvement: Context window management.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Conversation state (P1)
- UI requirements: Visible 'context used' indicator.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Context overflow -> summarised with notice.
- Acceptance criteria: Context never includes other users' conversations.
- Future extensions: Long-term memory (P2, opt-in).

## [TUT-013] Topic-aware responses

- Description: Uses taxonomy topics to focus retrieval.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Relevance.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Topics.
- AI involvement: Filtered retrieval.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Topic filter (P1)
- UI requirements: Topic chip.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Unreviewed topics -> not used.
- Acceptance criteria: Topic filter documented in response metadata.
- Future extensions: Competency awareness.

## [TUT-014] Competency-aware tutoring

- Description: Adapts to learner gaps.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Personalised tutoring.
- Priority: P2
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Gaps.
- AI involvement: Prompt conditioning on structured gap data (no raw personal data).
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Missing gaps -> generic mode.
- Acceptance criteria: Only structured competency identifiers sent to provider, never names.
- Future extensions: Knowledge tracing.

## [TUT-015] Grounded responses

- Description: Tutor inherits P0 grounding controls (RAI-001).
- Primary user: Learner
- Secondary users: Trainer
- Business value: Trustworthy tutoring.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Chunks.
- AI involvement: RAG.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): As MAT-018
- UI requirements: Citations inline.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: As MAT-017.
- Acceptance criteria: No ungrounded factual claims displayed without a 'not from sources' label.
- Future extensions: Claim-level verification.

## [TUT-016] Citation display

- Description: Inline citations in tutor messages.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Verifiability.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Citations.
- AI involvement: As MAT-019.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Citation objects in messages (P1)
- UI requirements: Citation chips.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Invalid citation -> removed and flagged.
- Acceptance criteria: All citations resolve to accessible pages.
- Future extensions: Hover previews.

## [TUT-017] Confidence display

- Description: Shows grounding confidence band per answer.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Calibrated trust.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Retrieval scores; verification results.
- AI involvement: Rule-based bands.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Confidence field (P1)
- UI requirements: Band label with explanation.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Unknown -> 'low'.
- Acceptance criteria: Bands defined in UI copy.
- Future extensions: Calibrated probabilities.

## [TUT-018] I don't know behavior

- Description: Tutor explicitly states when sources do not answer the question.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Prevents fabricated answers.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Retrieval results.
- AI involvement: Abstention (RAI-015).
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Abstention flag (P1)
- UI requirements: Abstention message with suggestion to ask a trainer.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: None.
- Acceptance criteria: Unanswerable questions in evaluation set produce abstentions.
- Future extensions: Escalation to trainer queue.

## [TUT-019] Prompt-injection resistance

- Description: Tutor treats document content and user text as data and resists instruction override.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Safety and integrity.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: Inputs.
- AI involvement: Defences per AI_SYSTEM_SPEC.md §36.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal
- UI requirements: Warning when content was restricted.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Injection detected -> restricted response and security log.
- Acceptance criteria: Injection test suite passes before release.
- Future extensions: Classifier-based detection.

## [TUT-020] Tutor conversation history

- Description: Learners view and delete their conversations.
- Primary user: Learner
- Secondary users: Trainer
- Business value: Continuity and control.
- Priority: P1
- Product area: AI learning tutor
- Dependencies: MAT-017 (document Q&A); RAI-001 (grounding); RAI-007 (prompt-injection protection)
- Data required: TutorConversation, TutorMessage.
- AI involvement: None.
- Human review required: Tutor output is advisory; learners can flag responses; flagged responses are reviewable by trainers.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/DELETE /api/v1/tutor/conversations (P1)
- UI requirements: History sidebar.
- Security considerations: Conversations are personal data with a retention policy; personal data redacted before provider calls; prompt-injection defences; no side-effecting tools.
- Accessibility considerations: Chat is screen-reader friendly (live regions, message landmarks), keyboard operable, supports text resizing.
- Failure cases: Deletion -> soft delete then purge per retention.
- Acceptance criteria: Learners can delete their conversations; retention enforced.
- Future extensions: Export.

---

# H. iGOT integration


## [IGOT-001] iGOT course search

- Description: Search iGOT course catalogue through the adapter.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Access to a large official catalogue.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: iGOT course metadata (real access UNKNOWN).
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - no documented public/partner API (IGOT_ACCESS_STATUS.md); mock list_courses() exists without search.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/integrations/igot/courses?q= (P1; mock only until access)
- UI requirements: Course discovery source filter.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Adapter not connected -> source hidden with admin notice.
- Acceptance criteria: Real search only via a verified adapter; mock results labelled MOCK.
- Future extensions: Federated search across providers.

## [IGOT-002] iGOT course recommendation

> Alias of **AI-006** - see that entry for the full specification.

- Description: Integration-side view of AI-006.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: See AI-006.
- Priority: P0
- Product area: iGOT integration
- Dependencies: AI-006
- Data required: See AI-006.
- AI involvement: See AI-006.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: In MVP - mock data only, feature-flagged
- Implementation status: Mocked - mock catalogue only.
- API requirements: See AI-006.
- UI requirements: MOCK badge on cards.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: See AI-006.
- Acceptance criteria: See AI-006.
- Future extensions: See AI-006.

## [IGOT-003] Competency-to-iGOT mapping

- Description: Maps platform competencies to iGOT course competencies.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Links gaps to iGOT content.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: iGOT competency metadata (format UNKNOWN); CSCD/FRAC references.
- AI involvement: Suggestions with review (MAT-026).
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - iGOT competency data format unknown; FRAC page unreachable (docs/DATA_COLLECTION_RESULTS.md).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Mapping review table.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Unknown iGOT competency schema -> blocked.
- Acceptance criteria: Mappings human-approved.
- Future extensions: FRAC alignment (Decision required).

## [IGOT-004] Course deep links

- Description: Links to iGOT course pages.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: One-click access.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Verified iGOT URL pattern (not verified).
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - URL pattern not verified.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Course.external_url (P1)
- UI requirements: 'Open in iGOT' link.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Link pattern unverified -> not shown.
- Acceptance criteria: Only verified URLs displayed; no links fabricated from IDs.
- Future extensions: Return-to-platform flow.

## [IGOT-005] Course metadata synchronization

- Description: Periodically imports course metadata.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Up-to-date catalogue.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Authorised catalogue feed.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - requires authorised access.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/integrations/igot/sync-jobs (P1)
- UI requirements: Sync status on Integration health.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Partial sync -> previous snapshot retained; never partial overwrite.
- Acceptance criteria: Sync is transactional per batch with provenance.
- Future extensions: Delta sync.

## [IGOT-006] Completion synchronization

- Description: Imports learner course completions with consent.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Unified learning record.
- Priority: P2
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Personal learner data.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Blocked by external access - personal data; requires authorisation, consent model and lawful basis.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until access and consent model exist.
- UI requirements: Consent screen; sync status.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Consent missing -> no sync.
- Acceptance criteria: Only with authorisation, consent and lawful basis.
- Future extensions: Bidirectional sync.

## [IGOT-007] Learning-history synchronization

- Description: Imports learning history with consent.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Better recommendations.
- Priority: P2
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Personal learner data.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Blocked by external access - as IGOT-006.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until access and consent model exist.
- UI requirements: Consent screen.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: As IGOT-006.
- Acceptance criteria: As IGOT-006.
- Future extensions: None.

## [IGOT-008] Authentication integration

- Description: Delegated authentication with iGOT accounts.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Single identity for learners.
- Priority: P2
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Official auth documentation.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Blocked by external access - no documented third-party auth (IGOT_ACCESS_STATUS.md §4).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until official documentation exists.
- UI requirements: Login option.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Token failure -> local login.
- Acceptance criteria: Implemented only against officially documented flows.
- Future extensions: SSO federation.

## [IGOT-009] OAuth/SSO placeholder

- Description: Design-level placeholder for OIDC/SSO providers behind the auth adapter; no live connection.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Avoids rework when SSO is authorised.
- Priority: P1
- Product area: iGOT integration
- Dependencies: SEC-004
- Data required: Provider metadata (future).
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Auth adapter interface (API_INTEGRATION_SPEC.md §Adapters)
- UI requirements: Hidden until configured.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Misconfiguration -> disabled.
- Acceptance criteria: Placeholder exposes no login option until a provider is configured and verified.
- Future extensions: Parichay or other government SSO (Decision required).

## [IGOT-010] API client abstraction

- Description: IGotClient interface with record types and errors; factory selects implementation by IGOT_CLIENT_MODE and refuses 'live'.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Mock and real implementations are interchangeable.
- Priority: P0
- Product area: iGOT integration
- Dependencies: ADM-014 (configuration/feature flags)
- Data required: Course, CoursePage, Enrollment, Completion, LearningEvent record types.
- AI involvement: None.
- Human review required: Not required for the interface; any real implementation requires written authorisation (API_REQUIREMENTS.md §6.4).
- MVP status: In MVP
- Implementation status: Implemented - clients/igot_client.py (interface, records, errors, factory); tested in tests/test_mock_igot_client.py. Health and sync methods not yet in the interface.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Backend service boundary; no public HTTP routes of its own
- UI requirements: None directly.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Unknown mode -> ValueError; live -> AccessNotVerifiedError.
- Acceptance criteria: All iGOT access goes through IGotClient; the factory defaults to mock and refuses live.
- Future extensions: Async interface and health/sync methods (API_INTEGRATION_SPEC.md §iGOT).

## [IGOT-011] Mock iGOT adapter

- Description: MockIGotClient over data/samples/mock/MOCK_igot_fixtures.json; every record data_status MOCK; refuses non-MOCK fixtures; simulates authorisation.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Enables development and demos without real access.
- Priority: P0
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Synthetic fixtures (4 courses, 3 users).
- AI involvement: None.
- Human review required: Not required for synthetic fixtures; any display of mock data must carry the MOCK label.
- MVP status: In MVP
- Implementation status: Mocked - clients/mock_igot_client.py with 14 passing tests (re-run 2026-09-14).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Used behind GET /api/v1/integrations/igot/courses
- UI requirements: MOCK badge everywhere mock data appears.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Fixture not fully MOCK-marked -> refuses to load.
- Acceptance criteria: All five interface methods supported; every returned record is MOCK; tests pass.
- Future extensions: Contract tests shared with future real adapter (TESTING_STRATEGY.md).

## [IGOT-012] Real iGOT adapter

- Description: Implementation of IGotClient against officially documented endpoints.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Real catalogue and (with consent) learner data.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Official documentation; credentials via environment.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - no authorisation or documentation (IGOT_ACCESS_STATUS.md).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Adapter behind existing interface
- UI requirements: Connection state 'connected' on Integration health.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Any unverified endpoint -> not implemented.
- Acceptance criteria: Built only after API_REQUIREMENTS.md §6.4 preconditions are VERIFIED by a human; passes the shared contract tests.
- Future extensions: Additional providers.

## [IGOT-013] Integration health checks

- Description: Reports adapter mode and health: 'mock', 'not connected', 'connected', 'degraded'.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Administrators know exactly what data source is active.
- Priority: P0
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Adapter mode; last check.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/integrations; GET /api/v1/integrations/igot/health
- UI requirements: Integration health screen.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Health check error -> 'degraded' with reason.
- Acceptance criteria: Mode 'mock' and 'not connected' are shown explicitly; a mock adapter never reports 'connected'.
- Future extensions: Alerting (OBSERVABILITY_SPEC.md).

## [IGOT-014] Retry handling

- Description: Bounded retries with exponential backoff and jitter for real adapter calls.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Resilience to transient failures.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Error classification.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - applies to the real adapter.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Adapter internals (P1)
- UI requirements: Degraded state shown.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Non-retryable errors -> no retry.
- Acceptance criteria: Retries only on retryable errors; limits configurable.
- Future extensions: Circuit breaker.

## [IGOT-015] Rate-limit handling

- Description: Honours documented rate limits and Retry-After.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Good citizenship with government systems.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Documented limits (unknown).
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - limits unknown.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Adapter internals (P1)
- UI requirements: Sync throttling indicator.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: 429 -> backoff.
- Acceptance criteria: Client stays below documented limits.
- Future extensions: Adaptive throttling.

## [IGOT-016] Data synchronization logs

- Description: Records every sync job with counts, errors and provenance.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Auditability of external data.
- Priority: P1
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: IntegrationSyncJob.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - no real sync possible.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/integrations/igot/sync-jobs (P1)
- UI requirements: Sync log table.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Log write failure -> sync aborted.
- Acceptance criteria: No sync commits data without a sync log record.
- Future extensions: Export of logs.

## [IGOT-017] Integration failure states

- Description: Explicit states and user messages for not-connected, refused, unauthorised and degraded adapters.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: No silent failures or silent data corruption.
- Priority: P0
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Adapter errors (AccessNotVerifiedError, AuthorizationRequiredError, NotFoundError).
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: In MVP
- Implementation status: Partially implemented - error classes exist in clients/igot_client.py; no API or UI mapping.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Problem responses (ERROR_HANDLING_SPEC.md) on integration routes
- UI requirements: Integration health; source-unavailable notices in Course discovery.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Unhandled adapter error -> generic 'integration unavailable' and logged.
- Acceptance criteria: Every adapter error maps to a documented error code; failures never write partial external data.
- Future extensions: Automatic recovery.

## [IGOT-018] External-source provenance

- Description: Tags every externally sourced record with source, adapter mode, retrieval time and data_status.
- Primary user: Platform administrator
- Secondary users: Learner; Training manager
- Business value: Users and auditors can always tell real from mock and where data came from.
- Priority: P0
- Product area: iGOT integration
- Dependencies: IGOT-010 (client abstraction); ADM-014 (configuration/feature flags)
- Data required: Provenance fields on Course and sync records.
- AI involvement: None.
- Human review required: Any real integration requires written authorisation and official documentation from Karmayogi Bharat (IGOT_ACCESS_STATUS.md; API_REQUIREMENTS.md §6.4).
- MVP status: In MVP
- Implementation status: Partially implemented - mock records carry data_status MOCK (clients/mock_igot_client.py); no application storage.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): provenance object on course and recommendation payloads
- UI requirements: Source/provenance badge.
- Security considerations: No credentials in source control; no undocumented endpoints; learner iGOT data is personal data requiring authorisation and consent; mock data never presented as real.
- Accessibility considerations: Integration and MOCK states communicated in text, not colour only.
- Failure cases: Missing provenance -> record rejected.
- Acceptance criteria: No iGOT-sourced record is stored or displayed without provenance; mock records carry data_status MOCK end to end.
- Future extensions: Signed provenance.

---

# I. Administration


## [ADM-001] User management

- Description: Create, deactivate and edit users and assign access roles within the organisation.
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Controlled access for a government deployment.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001; SEC-002
- Data required: User; access role assignments; Department.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/POST /api/v1/users; GET/PATCH /api/v1/users/{id}; PUT /api/v1/users/{id}/access-roles
- UI requirements: Users table and user form in Admin dashboard.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Duplicate email -> conflict error; last org admin removal -> blocked.
- Acceptance criteria: Deactivated users cannot sign in; role changes are audited; an organisation always retains at least one organisation administrator.
- Future extensions: Bulk import; SSO provisioning (P1).

## [ADM-002] Department management

- Description: Maintain departments/divisions within an organisation.
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Scoping for administrators, analytics and learners.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Department.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/POST /api/v1/departments; PATCH /api/v1/departments/{id}
- UI requirements: Departments table.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Department with active users deleted -> blocked (deactivate instead).
- Acceptance criteria: Departments are soft-deactivated, never hard-deleted while referenced.
- Future extensions: Hierarchies (P1).

## [ADM-003] Role management

- Description: Maintain job roles (not access roles) with descriptions and status.
- Primary user: Competency framework administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Basis for role selection and requirements.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: JobRole.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/POST /api/v1/job-roles; PATCH /api/v1/job-roles/{id}
- UI requirements: Job roles table and editor.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Role with learners deactivated -> learners prompted to reselect.
- Acceptance criteria: Job roles are clearly distinguished from access roles in UI and API naming (DECISIONS.md DEC-012).
- Future extensions: Role versioning (ROLE-012).

## [ADM-004] Competency management

- Description: Maintain competency frameworks, competencies and level scales, including imported reference frameworks with licence restrictions.
- Primary user: Competency framework administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Authoritative competency definitions for the organisation.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: CompetencyFramework; Competency; CompetencyLevel; SourceRecord.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Partially implemented - structure-only CSCD dataset (data/processed/competency_framework.json: 4 clusters, 25 competencies, no definitions); no functional statistical competencies; no admin application.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/POST /api/v1/competency-frameworks; GET/POST /api/v1/competencies; PATCH /api/v1/competencies/{id}
- UI requirements: Framework and competency editor.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Importing restricted definitions -> blocked; definition fields left empty with source page reference.
- Acceptance criteria: Imported CSCD entries show names and page references only (definitions not reproduced); functional statistical competencies must be authored and approved before use.
- Future extensions: Framework versioning; FRAC alignment.

## [ADM-005] Course management

- Description: Maintain the internal course catalogue, including seeded NSSTA programme listings and their competency/topic mappings.
- Primary user: Training manager
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Recommendable, curated content.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Course; CourseCompetency; provenance.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Partially implemented - 99 NSSTA programme records in data/processed/training_programmes.json (MACHINE_OBSERVED, unreviewed); no admin application.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/POST /api/v1/courses; GET/PATCH /api/v1/courses/{id}
- UI requirements: Course table and editor with provenance and review state.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Seeded mapping unreviewed -> excluded from recommendations.
- Acceptance criteria: Seeded courses keep source URL, organisation and data_status; NSSTA programmes are listings, not enrollable online courses.
- Future extensions: iGOT catalogue merge (IGOT-005).

## [ADM-006] Assessment management

- Description: Create, publish and retire assessments and blueprints.
- Primary user: Trainer
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Controlled assessment lifecycle.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Assessment; blueprint.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/POST /api/v1/assessments; PATCH /api/v1/assessments/{id}; POST /api/v1/assessments/{id}/publish
- UI requirements: Assessments table and blueprint editor.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Publishing with unapproved items -> blocked.
- Acceptance criteria: Only assessments composed of approved question versions can be published.
- Future extensions: Scheduling windows (P1).

## [ADM-007] Quiz management

> Alias of **ADM-006** - see that entry for the full specification.

- Description: Administrative view of quizzes (assessments with purpose 'practice' or 'topic').
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: See ADM-006.
- Priority: P0
- Product area: Administration
- Dependencies: ADM-006
- Data required: See ADM-006.
- AI involvement: See ADM-006.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ADM-006
- UI requirements: See ADM-006.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: See ADM-006.
- Acceptance criteria: See ADM-006.
- Future extensions: See ADM-006.

## [ADM-008] Learning-material management

- Description: Manage learning materials: metadata, licence notes, access scope, deactivation, reprocessing.
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Governed content library.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: LearningMaterial; Document.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/learning-materials; PATCH /api/v1/learning-materials/{id}; DELETE /api/v1/learning-materials/{id} (soft)
- UI requirements: Materials table in Document library (admin mode).
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Material cited by approved questions deactivated -> questions suspended and review tasks created.
- Acceptance criteria: Deactivating a material immediately removes it from search, Q&A and generation.
- Future extensions: Retention policies per material (SEC-018).

## [ADM-009] AI-generated-content review

> Alias of **ASM-027** - see that entry for the full specification.

- Description: Central review queue for all AI-generated artefacts requiring approval (questions in MVP).
- Primary user: Trainer
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Human oversight at one place.
- Priority: P0
- Product area: Administration
- Dependencies: ASM-027
- Data required: ReviewTask.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/review-tasks; POST /api/v1/review-tasks/{id}/decision
- UI requirements: Quiz review screen; review counters on Trainer/Admin dashboards.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Reviewer unavailable -> tasks reassignable.
- Acceptance criteria: No AI-generated artefact requiring approval is learner-visible before a decision.
- Future extensions: Summaries and tutor flags (P1).

## [ADM-010] Approval workflows

- Description: Configurable single-step approval with optional second reviewer for question approval.
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Proportionate control.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Approval policy; Approval.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/PATCH /api/v1/admin/settings (approval policy)
- UI requirements: Settings section.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Policy change mid-review -> applies to new tasks only.
- Acceptance criteria: Policy changes are audited and do not alter past decisions.
- Future extensions: Multi-stage workflows (P1).

## [ADM-011] Assignment workflows

- Description: Assign learning items or assessments to learners or departments.
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Organisational training programmes.
- Priority: P1
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Assignment.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/assignments (P1)
- UI requirements: Assignment dialog.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Assignment to inaccessible users -> blocked.
- Acceptance criteria: Assignments are visible to learners with due dates and assigner.
- Future extensions: Deadline-aware planning (PER-017).

## [ADM-012] Learner progress monitoring

- Description: Scoped view of learners' assessment status, gaps and path progress for trainers and training managers.
- Primary user: Trainer
- Secondary users: Training manager; Department administrator
- Business value: Timely support for learners.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Progress; attempts; gaps (scoped).
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/users/{id}/progress; GET /api/v1/progress?department_id= (scoped)
- UI requirements: Learner list with status in Trainer dashboard.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Out-of-scope user requested -> 403.
- Acceptance criteria: Monitoring shows only users within the viewer's scope; no rankings of individuals.
- Future extensions: Weak-learner support views (TRN-011).

## [ADM-013] Department analytics

- Description: Aggregated department capability and progress analytics.
- Primary user: Department administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Planning training at department level.
- Priority: P1
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Aggregates with minimum group size.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/departments/{id} (P1)
- UI requirements: Department analytics view.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Small groups -> suppressed.
- Acceptance criteria: Aggregates suppress groups below minimum size.
- Future extensions: Heatmaps (ANA-001).

## [ADM-014] Configuration management

- Description: Organisation settings and feature flags (including iGOT adapter visibility and mock-mode display).
- Primary user: Platform administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Safe, auditable configuration.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Setting; FeatureFlag.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/PATCH /api/v1/admin/settings
- UI requirements: Settings screen (admin sections).
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Invalid setting -> validation error; secrets never editable via UI.
- Acceptance criteria: Every change audited; secrets are environment-managed and never returned by the API.
- Future extensions: Environment promotion.

## [ADM-015] Taxonomy management

- Description: Maintain topic taxonomy terms and review auto-tags.
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Quality of linkage.
- Priority: P1
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Topic.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Partially implemented - project-defined taxonomy v0.1.2 in scripts/processing/topic_taxonomy.json and data/processed/topics.json (ASSUMED).
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST/PATCH /api/v1/topics (P1); GET /api/v1/topics (P0 read)
- UI requirements: Taxonomy editor.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Term in use deleted -> blocked.
- Acceptance criteria: Terms are versioned; seeded taxonomy is ASSUMED until reviewed.
- Future extensions: Multilingual labels.

## [ADM-016] Permission management

- Description: Custom permission sets beyond the fixed MVP access roles.
- Primary user: Organization administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Fit organisational structures.
- Priority: P1
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Permissions.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Permission editor.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Privilege escalation attempt -> blocked and audited.
- Acceptance criteria: Users cannot grant permissions they do not hold.
- Future extensions: Attribute-based access (P2).

## [ADM-017] Audit-log access

- Description: Search and view audit logs and AI interaction logs according to role.
- Primary user: System auditor
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Accountability and investigations.
- Priority: P0
- Product area: Administration
- Dependencies: SEC-009; SEC-011
- Data required: AuditLog; AIInteractionLog.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/audit-logs; GET /api/v1/ai-interactions; GET /api/v1/ai-interactions/{id}
- UI requirements: Audit logs screen.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Export of sensitive content -> restricted to auditor role.
- Acceptance criteria: Audit logs are read-only; access to them is itself audited.
- Future extensions: Tamper-evident log chain (P1).

## [ADM-018] Data-retention configuration

- Description: Configure retention periods per data class.
- Primary user: Platform administrator
- Secondary users: Department administrator; Competency framework administrator; Platform administrator
- Business value: Compliance with retention policy once decided.
- Priority: P1
- Product area: Administration
- Dependencies: SEC-001 (authentication); SEC-002 (RBAC); SEC-009 (audit logs)
- Data required: Retention policy.
- AI involvement: None.
- Human review required: Approval workflows for AI-generated content; configuration changes affecting learners require an authorised administrator.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PATCH /api/v1/admin/settings (retention, P1)
- UI requirements: Retention settings.
- Security considerations: Server-side authorisation on every action; every administrative change audited with before/after values.
- Accessibility considerations: Admin tables and forms meet the table and form patterns in UI_UX_SPEC.md (keyboard, labels, error summaries).
- Failure cases: Retention below legal minimum -> blocked (minimums: Decision required).
- Acceptance criteria: Retention jobs log what was purged.
- Future extensions: Legal holds.

---

# J. Analytics


## [ANA-001] Competency heatmaps

> Alias of **CMP-003** - see that entry for the full specification.

- Description: Organisation/department heatmaps (see CMP-003).
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: See CMP-003.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: See CMP-003.
- AI involvement: See CMP-003.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/competency-heatmap (P1)
- UI requirements: Department heatmap screen.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: See CMP-003.
- Acceptance criteria: See CMP-003.
- Future extensions: See CMP-003.

## [ANA-002] Organization skill gaps

- Description: Most common gaps across the organisation.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Prioritises central training investment.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Aggregated gaps.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/gaps (P1)
- UI requirements: Gap summary chart.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Insufficient data -> not shown.
- Acceptance criteria: Counts only estimates with sufficient evidence.
- Future extensions: Demand forecasting (ANA-012).

## [ANA-003] Department comparisons

- Description: Compares aggregated indicators between departments.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Targeted support.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Aggregates.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/departments/compare (P1)
- UI requirements: Comparison view with caveats.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Different role mixes -> caveat.
- Acceptance criteria: Comparisons include context caveats and suppression.
- Future extensions: Normalised comparisons.

## [ANA-004] Course completion analytics

- Description: Completion rates of courses and path items.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Catalogue effectiveness.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Progress records.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/courses (P1)
- UI requirements: Completion chart.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: External completions unknown -> internal only.
- Acceptance criteria: Source of completion data stated.
- Future extensions: iGOT completions (IGOT-006).

## [ANA-005] Assessment performance

- Description: Aggregated assessment outcomes.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Assessment and training design.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Attempts.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/assessments (P1)
- UI requirements: Performance distribution.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Small samples -> suppressed.
- Acceptance criteria: No individual identification in aggregate views.
- Future extensions: Item analysis (ASM-026).

## [ANA-006] Engagement analytics

- Description: Active use and learning activity trends.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Adoption monitoring.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: LearningActivity.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/engagement (P1)
- UI requirements: Engagement trends.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Tracking disabled -> partial.
- Acceptance criteria: Uses product analytics events only (PRD.md §19).
- Future extensions: Cohort analysis.

## [ANA-007] Improvement analytics

- Description: Aggregated baseline-to-post change.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Evidence of programme impact.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Comparable estimates.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/improvement (P1)
- UI requirements: Before/after aggregate.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Non-comparable -> excluded.
- Acceptance criteria: Only comparable assessments aggregated.
- Future extensions: Training effectiveness (ANA-008).

## [ANA-008] Training effectiveness

- Description: Links training completion to later improvement (associational, not causal).
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Informs training design.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Completions; improvement.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/training-effectiveness (P1)
- UI requirements: Effectiveness view with causal caveat.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Confounding -> caveat.
- Acceptance criteria: Displays 'association, not causation' caveat.
- Future extensions: Controlled evaluations.

## [ANA-009] Training ROI placeholders

- Description: Placeholder metrics pending an agreed ROI method.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Future budgeting insight.
- Priority: P2
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Cost data (not available).
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Placeholder panel.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: No cost data -> placeholder only.
- Acceptance criteria: No ROI figures shown until method approved.
- Future extensions: Cost models.

## [ANA-010] Trend analysis

- Description: Longitudinal trends of capability indicators.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Strategic planning.
- Priority: P2
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Historical aggregates.
- AI involvement: Time-series methods.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Trend charts.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Method changes -> series breaks.
- Acceptance criteria: Series breaks annotated.
- Future extensions: Forecasting.

## [ANA-011] Demand prediction

- Description: Predicts future training demand.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Capacity planning.
- Priority: P2
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Historical demand.
- AI involvement: Forecasting models.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Insufficient history -> unavailable.
- Acceptance criteria: Validated before display.
- Future extensions: Skill-demand forecasting.

## [ANA-012] Skill-demand forecasting

> Alias of **FUT-002** - see that entry for the full specification.

- Description: Forecasts future competency needs.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Workforce planning.
- Priority: P2
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Role changes; external signals.
- AI involvement: Forecasting.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: As ANA-011.
- Acceptance criteria: As ANA-011.
- Future extensions: FUT-002.

## [ANA-013] Recommendation effectiveness

- Description: Acceptance, dismissal and completion rates of recommendations.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Improves recommendation rules.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Recommendation feedback.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/recommendations (P1)
- UI requirements: Effectiveness dashboard.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Low volume -> not computed.
- Acceptance criteria: Metrics defined in PRD.md §18.
- Future extensions: A/B evaluation (P2).

## [ANA-014] Learning-path effectiveness

- Description: Outcome of learners following paths vs not.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Path design.
- Priority: P2
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Paths; improvement.
- AI involvement: Causal methods.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Confounding -> caveat.
- Acceptance criteria: Methodology reviewed.
- Future extensions: Experiments.

## [ANA-015] Assessment quality analytics

- Description: Item statistics and reviewer rejection reasons.
- Primary user: Training manager
- Secondary users: Department administrator; Organization administrator
- Business value: Question bank quality.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: Answers; rejections.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/assessment-quality (P1)
- UI requirements: Item quality table.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Small samples -> suppressed.
- Acceptance criteria: Statistics shown with sample sizes.
- Future extensions: IRT diagnostics.

## [ANA-016] AI quality analytics

- Description: Validation pass rates, reviewer rejection rates, abstention and citation-verification rates.
- Primary user: Platform administrator
- Secondary users: System auditor
- Business value: Monitors AI behaviour over time.
- Priority: P1
- Product area: Analytics
- Dependencies: PRO-005 (learning history); SEC-002 (RBAC)
- Data required: AIInteractionLog; validations; review decisions.
- AI involvement: None.
- Human review required: Analytics are decision support with interpretation notes; they never trigger employment actions.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/ai-quality (P1)
- UI requirements: AI quality dashboard.
- Security considerations: Aggregates suppress groups below a minimum size; no individual rankings; access scoped by role.
- Accessibility considerations: Every chart has a data table alternative and text summary.
- Failure cases: Logging gaps -> flagged.
- Acceptance criteria: Metrics computed from logged data only; no untested accuracy claims.
- Future extensions: Drift detection.

---

# K. Trainer workspace


## [TRN-001] Trainer dashboard

- Description: Trainer home: pending review tasks, generation jobs, recent uploads, learners needing attention (scoped).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: Trainers see their work queue at a glance.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: ADM-009; ADM-012
- Data required: ReviewTask; jobs; scoped progress.
- AI involvement: None.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/trainer/dashboard (aggregate)
- UI requirements: Trainer dashboard screen.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: Partial data failure -> per-card error.
- Acceptance criteria: Shows only scoped data; review counts match the review queue.
- Future extensions: Workload balancing (P1).

## [TRN-002] Material upload

> Alias of **MAT-001** - see that entry for the full specification.

- Description: Trainer-facing upload (see MAT-001/002/004).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See MAT-001.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See MAT-001.
- AI involvement: See MAT-001.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See MAT-001
- UI requirements: Upload from Trainer dashboard.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See MAT-001.
- Acceptance criteria: See MAT-001.
- Future extensions: See MAT-001.

## [TRN-003] Quiz generation

> Alias of **AI-007** - see that entry for the full specification.

- Description: Trainer-facing generation (see AI-007).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See AI-007.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See AI-007.
- AI involvement: See AI-007.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See AI-007
- UI requirements: Quiz builder.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See AI-007.
- Acceptance criteria: See AI-007.
- Future extensions: See AI-007.

## [TRN-004] Quiz review

> Alias of **ASM-027** - see that entry for the full specification.

- Description: Trainer-facing review (see ASM-027).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See ASM-027.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See ASM-027.
- AI involvement: See ASM-027.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ASM-027
- UI requirements: Quiz review screen.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See ASM-027.
- Acceptance criteria: See ASM-027.
- Future extensions: See ASM-027.

## [TRN-005] Quiz editing

> Alias of **ASM-030** - see that entry for the full specification.

- Description: Trainer-facing editing (see ASM-030).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See ASM-030.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See ASM-030.
- AI involvement: See ASM-030.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ASM-030
- UI requirements: Inline editor.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See ASM-030.
- Acceptance criteria: See ASM-030.
- Future extensions: See ASM-030.

## [TRN-006] Quiz approval

> Alias of **ASM-028** - see that entry for the full specification.

- Description: Trainer-facing approval (see ASM-028).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See ASM-028.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See ASM-028.
- AI involvement: See ASM-028.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ASM-028
- UI requirements: Approve action.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See ASM-028.
- Acceptance criteria: See ASM-028.
- Future extensions: See ASM-028.

## [TRN-007] Quiz rejection

> Alias of **ASM-029** - see that entry for the full specification.

- Description: Trainer-facing rejection (see ASM-029).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See ASM-029.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See ASM-029.
- AI involvement: See ASM-029.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ASM-029
- UI requirements: Reject action.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See ASM-029.
- Acceptance criteria: See ASM-029.
- Future extensions: See ASM-029.

## [TRN-008] Manual question creation

- Description: Trainers author questions manually with mandatory citation, entering the same review workflow.
- Primary user: Trainer
- Secondary users: Training manager
- Business value: Assessment continues even where AI generation is unsuitable or unavailable.
- Priority: P0
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: Question; Citation.
- AI involvement: Optional validation checks (ASM-022 to ASM-024).
- Human review required: Required per approval policy (second reviewer when configured).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/questions
- UI requirements: Question editor in Quiz builder.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: Missing citation -> cannot submit for review.
- Acceptance criteria: Manually created questions are marked human-authored, require a citation, and follow the review policy.
- Future extensions: Question import (P1).

## [TRN-009] Assignment creation

> Alias of **ADM-011** - see that entry for the full specification.

- Description: Trainer assigns assessments or materials (see ADM-011).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See ADM-011.
- Priority: P1
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See ADM-011.
- AI involvement: See ADM-011.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ADM-011
- UI requirements: Assignment dialog.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See ADM-011.
- Acceptance criteria: See ADM-011.
- Future extensions: See ADM-011.

## [TRN-010] Learner performance

- Description: Detailed scoped learner performance views beyond MVP monitoring.
- Primary user: Trainer
- Secondary users: Training manager
- Business value: Targeted coaching.
- Priority: P1
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: Attempts; estimates (scoped).
- AI involvement: None.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/trainer/learners/{id}/performance (P1)
- UI requirements: Learner detail page.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: Out of scope -> 403.
- Acceptance criteria: No ranking tables of individuals.
- Future extensions: Coaching notes.

## [TRN-011] Weak-learner identification

- Description: Highlights learners who may need support based on gaps and inactivity, framed as support signals.
- Primary user: Trainer
- Secondary users: Training manager
- Business value: Early help.
- Priority: P1
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: Gaps; activity (scoped).
- AI involvement: Rule-based signals.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/trainer/support-signals (P1)
- UI requirements: Support signal list with reasons.
- Security considerations: Must not feed appraisal or disciplinary processes (SECURITY_RESPONSIBLE_AI.md §HID).
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: Insufficient evidence -> no signal.
- Acceptance criteria: Signals are visible only to assigned trainers, state their reasons, and are labelled as support prompts, not performance judgements.
- Future extensions: Intervention tracking.

## [TRN-012] Progress reports

> Alias of **REP-007** - see that entry for the full specification.

- Description: Trainer-level progress reports (see REP-007).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See REP-007.
- Priority: P1
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See REP-007.
- AI involvement: See REP-007.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See REP-007
- UI requirements: Reports screen.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See REP-007.
- Acceptance criteria: See REP-007.
- Future extensions: See REP-007.

## [TRN-013] Course effectiveness

> Alias of **ANA-008** - see that entry for the full specification.

- Description: Trainer view of course effectiveness (see REP-006 / ANA-008).
- Primary user: Trainer
- Secondary users: Training manager
- Business value: See ANA-008.
- Priority: P1
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: See ANA-008.
- AI involvement: See ANA-008.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ANA-008
- UI requirements: Effectiveness view.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: See ANA-008.
- Acceptance criteria: See ANA-008.
- Future extensions: See ANA-008.

## [TRN-014] Feedback collection

- Description: Collects learner feedback on courses, materials and questions.
- Primary user: Trainer
- Secondary users: Training manager
- Business value: Continuous improvement.
- Priority: P1
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: Feedback records.
- AI involvement: Optional LLM theme summarisation with review (P1).
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/feedback (P1)
- UI requirements: Feedback forms.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: Abusive content -> moderation.
- Acceptance criteria: Feedback can be anonymous where configured.
- Future extensions: Sentiment trends.

## [TRN-015] Training recommendations

- Description: Recommends training programmes to organise based on aggregate gaps.
- Primary user: Trainer
- Secondary users: Training manager
- Business value: Programme planning.
- Priority: P2
- Product area: Trainer workspace
- Dependencies: SEC-002 (RBAC); ASM-027 (review workflow)
- Data required: Aggregated gaps.
- AI involvement: Rule-based / forecasting.
- Human review required: Trainers review and approve AI-generated content; trainer decisions are audited.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Trainers see only assigned learners/departments and materials within scope.
- Accessibility considerations: Dense review screens remain keyboard-first with visible focus and shortcuts documented.
- Failure cases: Low data -> none.
- Acceptance criteria: Advisory only.
- Future extensions: Capability planning (FUT-018).

---

# L. Multilingual and accessibility


## [ACC-001] English

- Description: Complete English user interface.
- Primary user: Learner
- Secondary users: All users
- Business value: Primary working language of source materials.
- Priority: P0
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: UI strings.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Accept-Language / user locale
- UI requirements: All screens.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Missing string -> key fallback logged.
- Acceptance criteria: No hard-coded user-facing strings outside the i18n catalogue.
- Future extensions: Additional languages.

## [ACC-002] Hindi

- Description: Hindi user interface and support for Hindi content.
- Primary user: Learner
- Secondary users: All users
- Business value: Reach across Central and State officials.
- Priority: P1
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Translated strings; Hindi content.
- AI involvement: Machine translation with review (P1).
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Locale 'hi' (P1)
- UI requirements: Language switcher.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Untranslated string -> English fallback labelled.
- Acceptance criteria: Hindi UI reviewed by a human before release; Hindi rendering tested.
- Future extensions: Other Indian languages.

## [ACC-003] Indian-language support architecture

- Description: Internationalisation architecture: externalised strings, Unicode-safe storage, locale-aware formatting, font fallback for Indic scripts.
- Primary user: Learner
- Secondary users: All users
- Business value: Avoids costly retrofitting for Hindi and other languages.
- Priority: P0
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: i18n catalogue.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: In MVP - architecture only; no translations
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Locale negotiation
- UI requirements: Locale-ready components.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Script rendering issues -> caught by visual tests.
- Acceptance criteria: All UI text externalised; UTF-8 end to end; no language other than English claimed as supported in MVP.
- Future extensions: Language packs.

## [ACC-004] Translation workflow

- Description: Draft translation, review and publish workflow for UI and content.
- Primary user: Learner
- Secondary users: All users
- Business value: Quality of translated material.
- Priority: P1
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Translation records.
- AI involvement: Machine translation drafts.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Translation review screen.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Terminology errors -> glossary.
- Acceptance criteria: No machine translation published without review.
- Future extensions: Statistical glossary.

## [ACC-005] Multilingual quizzes

- Description: Questions available in Hindi with linked source language versions.
- Primary user: Learner
- Secondary users: All users
- Business value: Assessment in preferred language.
- Priority: P1
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Question translations.
- AI involvement: Translation drafts with review.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Language toggle in assessments.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Translation not reviewed -> English only.
- Acceptance criteria: Translated items reviewed and linked to the source-language version.
- Future extensions: Other languages.

## [ACC-006] Multilingual tutor

- Description: Tutor in Hindi and other languages.
- Primary user: Learner
- Secondary users: All users
- Business value: Accessible tutoring.
- Priority: P2
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Multilingual retrieval.
- AI involvement: Multilingual models.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Low-quality language -> fallback.
- Acceptance criteria: Evaluated per language before enabling.
- Future extensions: Voice (FUT-012).

## [ACC-007] Text-to-speech

- Description: Reads content aloud.
- Primary user: Learner
- Secondary users: All users
- Business value: Accessibility and low-literacy support.
- Priority: P2
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Text.
- AI involvement: TTS service.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Play controls.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Service down -> hidden.
- Acceptance criteria: Consent and provider data terms verified.
- Future extensions: Voice interface.

## [ACC-008] Speech-to-text

- Description: Voice input.
- Primary user: Learner
- Secondary users: All users
- Business value: Accessibility.
- Priority: P2
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Audio.
- AI involvement: STT service.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Mic control.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Recognition errors -> editable text.
- Acceptance criteria: Audio not retained without consent.
- Future extensions: Voice tutor.

## [ACC-009] Screen-reader compatibility

- Description: Semantic HTML, ARIA only where needed, live regions for async status.
- Primary user: Learner
- Secondary users: All users
- Business value: Usable by visually impaired officials.
- Priority: P0
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: None.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: All screens.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Custom widget inaccessible -> replaced by accessible primitive.
- Acceptance criteria: Automated axe checks pass and manual screen-reader test of core journeys completed before MVP release.
- Future extensions: Periodic audits.

## [ACC-010] Keyboard navigation

- Description: All functionality operable by keyboard with visible focus.
- Primary user: Learner
- Secondary users: All users
- Business value: Accessibility and power-user efficiency.
- Priority: P0
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: None.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: All screens.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Focus trap -> test failure.
- Acceptance criteria: Core journeys completable keyboard-only; focus order logical.
- Future extensions: Shortcut customisation.

## [ACC-011] Font-size controls

- Description: User-adjustable text size beyond browser zoom.
- Primary user: Learner
- Secondary users: All users
- Business value: Readability.
- Priority: P1
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: User preference.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PATCH /api/v1/me (preferences, P1)
- UI requirements: Settings control.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Layout breaks -> responsive fixes.
- Acceptance criteria: UI usable at 200% text size.
- Future extensions: Reading mode.

## [ACC-012] High-contrast mode

- Description: High-contrast theme.
- Primary user: Learner
- Secondary users: All users
- Business value: Low-vision support.
- Priority: P1
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Theme tokens.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): User preference (P1)
- UI requirements: Theme toggle.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Contrast failures -> token fix.
- Acceptance criteria: Meets enhanced contrast for text.
- Future extensions: System preference sync.

## [ACC-013] Captions

- Description: Captions for video/audio content.
- Primary user: Learner
- Secondary users: All users
- Business value: Hearing accessibility.
- Priority: P2
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Media transcripts.
- AI involvement: Optional STT drafts with review.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Caption track.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Missing captions -> media flagged.
- Acceptance criteria: Media not published without captions.
- Future extensions: Transcript search.

## [ACC-014] Accessible forms

- Description: Labels, instructions, error summaries and inline errors linked to fields.
- Primary user: Learner
- Secondary users: All users
- Business value: Error-free data entry for all users.
- Priority: P0
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: None.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Validation errors mapped to fields (ERROR_HANDLING_SPEC.md)
- UI requirements: All forms.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Unlabelled field -> lint failure.
- Acceptance criteria: Every input has a programmatic label; errors announced and linked.
- Future extensions: Autosave.

## [ACC-015] Accessible charts

- Description: Charts with text summaries, data tables and non-colour encodings.
- Primary user: Learner
- Secondary users: All users
- Business value: Analytics usable by everyone.
- Priority: P0
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: Chart data.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: All charts.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Chart library limitation -> table fallback.
- Acceptance criteria: Every chart has a table alternative and meets contrast rules.
- Future extensions: Sonification (P2).

## [ACC-016] Reduced-motion support

- Description: Respects prefers-reduced-motion; no essential motion.
- Primary user: Learner
- Secondary users: All users
- Business value: Vestibular accessibility.
- Priority: P0
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: None.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: Animations.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Motion without fallback -> test failure.
- Acceptance criteria: No animation is required to understand content.
- Future extensions: None.

## [ACC-017] Low-bandwidth considerations

- Description: Lightweight pages, lazy loading, text-first fallbacks, resumable uploads.
- Primary user: Learner
- Secondary users: All users
- Business value: Usable from field offices with poor connectivity.
- Priority: P1
- Product area: Multilingual and accessibility
- Dependencies: UX-001 (responsive design)
- Data required: None.
- AI involvement: None.
- Human review required: Machine translations reviewed before publication; translated content keeps source provenance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Pagination and compression
- UI requirements: Lite states.
- Security considerations: No additional data exposure; speech features (P2) require consent for audio processing.
- Accessibility considerations: Target WCAG 2.1 AA; GIGW applicability to be confirmed (DECISIONS.md DEC-026).
- Failure cases: Slow network -> skeletons and retries.
- Acceptance criteria: Core pages usable on a throttled connection profile defined in TESTING_STRATEGY.md.
- Future extensions: Offline mode (FUT-009).

---

# M. Gamification


## [GAM-001] Points

- Description: Points for completing learning activities (not for assessment scores).
- Primary user: Learner
- Secondary users: Training manager
- Business value: Motivation.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: LearningActivity.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Points indicator.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Gaming behaviour -> anti-gaming rules.
- Acceptance criteria: Points never derived from competency scores.
- Future extensions: Levels.

## [GAM-002] Badges

- Description: Badges for milestones.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Recognition.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Badge definitions.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/badges (P1)
- UI requirements: Badge shelf.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Duplicate award -> idempotent.
- Acceptance criteria: Badge criteria visible.
- Future extensions: Verifiable badges.

## [GAM-003] Streaks

- Description: Consecutive learning-day streaks (see PRO-009).
- Primary user: Learner
- Secondary users: Training manager
- Business value: Habit building.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Activity dates.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Streak counter.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Timezone issues -> user timezone.
- Acceptance criteria: Streaks can be hidden by the learner.
- Future extensions: Streak freezes.

## [GAM-004] Milestones

- Description: Milestones such as baseline completed or path completed.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Progress recognition.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Progress events.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Milestone timeline.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: None specific.
- Acceptance criteria: Milestones based on objective events.
- Future extensions: Certificates.

## [GAM-005] Levels

- Description: Engagement levels.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Long-term motivation.
- Priority: P2
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Points.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Level indicator.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Confusion with competency levels -> distinct naming.
- Acceptance criteria: Never named like competency levels.
- Future extensions: None.

## [GAM-006] Certificates

- Description: Completion certificates for internal programmes.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Formal recognition.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Certificate records.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/certificates (P1)
- UI requirements: Certificate view/download.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Revocation -> certificate marked revoked.
- Acceptance criteria: Issued only on objective completion criteria; verifiable ID.
- Future extensions: AI certification (FUT-007).

## [GAM-007] Goals

> Alias of **PER-016** - see that entry for the full specification.

- Description: Engagement goals (see PER-016).
- Primary user: Learner
- Secondary users: Training manager
- Business value: See PER-016.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: See PER-016.
- AI involvement: See PER-016.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See PER-016
- UI requirements: Goal widgets.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: See PER-016.
- Acceptance criteria: See PER-016.
- Future extensions: See PER-016.

## [GAM-008] Professional leaderboards

- Description: Opt-in leaderboards of learning activity (not competency).
- Primary user: Learner
- Secondary users: Training manager
- Business value: Friendly motivation where culturally appropriate.
- Priority: P2
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Opt-in activity data.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Leaderboard.
- Security considerations: High sensitivity: requires consent model and ethics review; excluded from MVP.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Non-consenting user shown -> blocked.
- Acceptance criteria: Opt-in only, activity-based, aggregated by team where possible; never shows competency scores.
- Future extensions: Team challenges.

## [GAM-009] Team challenges

- Description: Department-level learning challenges.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Collective engagement.
- Priority: P2
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Aggregates.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Challenge page.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Small teams -> suppressed.
- Acceptance criteria: Aggregate-only.
- Future extensions: None.

## [GAM-010] Recognition

- Description: Trainer-issued recognition notes.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Human recognition.
- Priority: P2
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Recognition records.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Recognition feed.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: Misuse -> moderation.
- Acceptance criteria: Human-issued only.
- Future extensions: None.

## [GAM-011] Anti-gaming safeguards

- Description: Detects implausible activity patterns and prevents rewards for trivial actions.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Keeps gamification meaningful.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Activity logs.
- AI involvement: Rule-based.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal (P1)
- UI requirements: None.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: False positive -> no penalty, only no reward.
- Acceptance criteria: Safeguards never penalise learners, only withhold rewards.
- Future extensions: Anomaly detection.

## [GAM-012] Optional gamification settings

- Description: Organisation and user-level toggles.
- Primary user: Learner
- Secondary users: Training manager
- Business value: Respects organisational culture and preferences.
- Priority: P1
- Product area: Gamification
- Dependencies: PRO-001 (progress); ADM-014 (configuration)
- Data required: Settings.
- AI involvement: None.
- Human review required: Rules configured by administrators; recognition awarded manually where it has any organisational significance.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PATCH /api/v1/admin/settings; PATCH /api/v1/me (P1)
- UI requirements: Toggles.
- Security considerations: Opt-in; no public exposure of individual performance without consent; never used in appraisal.
- Accessibility considerations: Badges and progress have text equivalents; no flashing effects.
- Failure cases: None specific.
- Acceptance criteria: Gamification off by default until enabled by organisation.
- Future extensions: Per-department settings.

---

# N. Progress tracking


## [PRO-001] Course progress

- Description: Status of each course/path item: not started, in progress, completed (learner-marked or system-recorded).
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Learners and trainers see advancement.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: ProgressRecord; LearningPathItem.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): PATCH /api/v1/learning-path-items/{id}; GET /api/v1/me/progress
- UI requirements: Status controls in Learning path; progress bars.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Offline completion (e.g. NSSTA programme) -> learner self-report labelled self-reported.
- Acceptance criteria: Every status change records source (system / self-reported / administrator).
- Future extensions: iGOT completion sync (IGOT-006).

## [PRO-002] Quiz progress

- Description: In-progress and completed attempts per assessment.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Resume and completion visibility.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: AssessmentAttempt.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/attempts
- UI requirements: Attempt status on dashboard.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Expired attempt -> marked expired.
- Acceptance criteria: Resumable attempts clearly indicated.
- Future extensions: Attempt analytics.

## [PRO-003] Competency progress

- Description: Current estimate vs baseline per competency.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Shows development direction.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: UserCompetency history (baseline + current).
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in GET /api/v1/me/competency-profile
- UI requirements: Baseline marker on profile.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: No baseline -> baseline pending.
- Acceptance criteria: Baseline is immutable; changes shown with method-version caveats.
- Future extensions: Growth graphs (PRO-007).

## [PRO-004] Learning hours

- Description: Estimated learning time from item durations and activity.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Workload visibility.
- Priority: P1
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Durations; activity.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Hours summary.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Unknown durations -> excluded with note.
- Acceptance criteria: Hours labelled as estimates.
- Future extensions: Calendar integration.

## [PRO-005] Learning history

- Description: Chronological record of the learner's completed items and attempts.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Personal record of development.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: ProgressRecord; attempts.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/progress/history
- UI requirements: History list.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Deleted content -> history entry retained with title snapshot.
- Acceptance criteria: History entries keep title snapshots so deleted content does not break the record.
- Future extensions: Evidence timeline (PRO-014).

## [PRO-006] Scores

- Description: Assessment scores within progress views.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Quick performance recall.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Attempts.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/attempts
- UI requirements: Scores column.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Rescored -> updated with note.
- Acceptance criteria: Rescoring noted.
- Future extensions: Trends.

## [PRO-007] Growth graphs

- Description: Charts of competency change over time.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Visible improvement.
- Priority: P1
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Estimate history.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/competency-history (P1)
- UI requirements: Line charts with tables.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Series breaks annotated.
- Acceptance criteria: Accessible chart pattern used.
- Future extensions: Forecast overlays (P2).

## [PRO-008] Before-vs-after comparisons

- Description: Baseline vs post-assessment comparison.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Demonstrates learning impact.
- Priority: P1
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Pre/post estimates.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/improvement (P1)
- UI requirements: Before/after view.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Non-comparable -> caveat.
- Acceptance criteria: Caveats shown when item pools differ.
- Future extensions: Equated forms.

## [PRO-009] Streaks

> Alias of **GAM-003** - see that entry for the full specification.

- Description: Progress-side view of streaks (see GAM-003).
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: See GAM-003.
- Priority: P1
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: See GAM-003.
- AI involvement: See GAM-003.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See GAM-003
- UI requirements: Streak counter.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: See GAM-003.
- Acceptance criteria: See GAM-003.
- Future extensions: See GAM-003.

## [PRO-010] Completed items

- Description: List of completed path items and assessments.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Sense of accomplishment; avoids repeats.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: ProgressRecord.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/progress?status=completed
- UI requirements: Completed tab.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: None specific.
- Acceptance criteria: Completed items excluded from recommendations.
- Future extensions: Certificates.

## [PRO-011] Pending items

- Description: List of not-started and in-progress items.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Clear to-do list.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: LearningPathItem.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/progress?status=pending
- UI requirements: Pending tab; Continue learning.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: None specific.
- Acceptance criteria: Pending list matches the current learning path.
- Future extensions: Due dates (P1).

## [PRO-012] Recommended items

- Description: Recommended items not yet in the path.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Discovery.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Recommendation.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/recommendations
- UI requirements: Recommended tab.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: None specific.
- Acceptance criteria: Each item links to its reason.
- Future extensions: Saved items.

## [PRO-013] Assessment timeline

- Description: Chronological view of assessments and resulting estimate changes.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Understand how estimates evolved.
- Priority: P0
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Attempts; evidence.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/attempts (timeline view)
- UI requirements: Timeline component on Competency profile.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: None specific.
- Acceptance criteria: Timeline entries link to results and evidence.
- Future extensions: Learning evidence timeline.

## [PRO-014] Learning evidence timeline

- Description: Combined timeline of assessment and learning evidence.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Holistic development record.
- Priority: P1
- Product area: Progress tracking
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Evidence; activities.
- AI involvement: None.
- Human review required: Not required for objective progress records; corrections by administrators are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Timeline with type filters.
- Security considerations: Progress data is personal data: self, assigned trainer and scoped managers only.
- Accessibility considerations: Progress indicators have text values; charts have tables.
- Failure cases: Self-reported items labelled.
- Acceptance criteria: Evidence types visually and textually distinguished.
- Future extensions: Skill passport.

---

# O. Reporting


## [REP-001] Employee report

- Description: Individual development report: role, estimates with bands, gaps, path progress, assessment history.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Structured view for learner and trainer conversations.
- Priority: P0
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Profile; gaps; progress; attempts.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=learner_development); GET /api/v1/reports/{id}
- UI requirements: Reports screen; 'Download my report' on profile.
- Security considerations: Titled 'Learner development report'; carries a notice that it is not an appraisal instrument (SECURITY_RESPONSIBLE_AI.md §HID).
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Generation failure -> job retry and error state.
- Acceptance criteria: Report shows evidence bands and limitations; learners can always generate their own report; access by others is scoped and audited.
- Future extensions: PDF export (REP-010).

## [REP-002] Department report

- Description: Aggregated department capability and progress report.
- Primary user: Department administrator
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Department-level planning.
- Priority: P1
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Aggregates.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=department, P1)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Small groups -> suppressed.
- Acceptance criteria: Minimum group-size suppression applied.
- Future extensions: Scheduled reports (REP-013).

## [REP-003] Competency-gap report

- Description: Gap list for a learner (own) or scoped learners, with evidence bands.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Actionable gap export.
- Priority: P0
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Gaps.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=competency_gaps)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: No gaps data -> empty report with explanation.
- Acceptance criteria: Only gaps with sufficient evidence included; insufficient-evidence competencies listed separately.
- Future extensions: Department gap report (P1).

## [REP-004] Assessment report

- Description: Results of an assessment for a learner, or aggregate for an assessment (scoped).
- Primary user: Trainer
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Assessment follow-up.
- Priority: P0
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Attempts.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=assessment)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Aggregate below minimum size -> suppressed.
- Acceptance criteria: Individual results visible only within scope; aggregates suppressed below minimum size.
- Future extensions: Item analysis (ANA-015).

## [REP-005] Quiz report

- Description: Practice quiz outcomes.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Practice insight.
- Priority: P1
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Attempts.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=quiz, P1)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: As REP-004.
- Acceptance criteria: As REP-004.
- Future extensions: None.

## [REP-006] Course-effectiveness report

> Alias of **ANA-008** - see that entry for the full specification.

- Description: See ANA-008.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: See ANA-008.
- Priority: P1
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: See ANA-008.
- AI involvement: See ANA-008.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=course_effectiveness, P1)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: See ANA-008.
- Acceptance criteria: See ANA-008.
- Future extensions: See ANA-008.

## [REP-007] Progress report

- Description: Learning path and item progress for a learner or scoped group.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Tracks development activity.
- Priority: P0
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Progress records.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=progress)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: As REP-001.
- Acceptance criteria: Self-reported completions labelled.
- Future extensions: Scheduled delivery.

## [REP-008] Improvement report

- Description: Before-vs-after report (see PRO-008).
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: See PRO-008.
- Priority: P1
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: See PRO-008.
- AI involvement: See PRO-008.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=improvement, P1)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: See PRO-008.
- Acceptance criteria: See PRO-008.
- Future extensions: See PRO-008.

## [REP-009] Training recommendation report

- Description: Aggregated recommended training needs.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Programme planning.
- Priority: P1
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Aggregated gaps; recommendations.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (type=training_needs, P1)
- UI requirements: Reports screen.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Low data -> caveat.
- Acceptance criteria: Aggregate-only with caveats.
- Future extensions: TRN-015.

## [REP-010] PDF export

- Description: PDF rendering of reports.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Shareable formal documents.
- Priority: P1
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Report data.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/reports/{id}/download?format=pdf (P1)
- UI requirements: Download menu.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Rendering failure -> CSV offered.
- Acceptance criteria: PDFs are tagged for accessibility.
- Future extensions: Watermarking.

## [REP-011] Excel export

- Description: XLSX exports.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Analysis in spreadsheets.
- Priority: P1
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Report data.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/reports/{id}/download?format=xlsx (P1)
- UI requirements: Download menu.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Formula injection -> values escaped.
- Acceptance criteria: Cell values escaped against formula injection.
- Future extensions: Templates.

## [REP-012] CSV export

- Description: CSV download of report tables.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Interoperability with minimal dependencies.
- Priority: P0
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Report data.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/reports/{id}/download?format=csv
- UI requirements: Download button.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Formula injection risk -> leading =,+,-,@ escaped.
- Acceptance criteria: CSV is UTF-8 with header row; cells escaped against formula injection; download audited.
- Future extensions: Excel (REP-011).

## [REP-013] Scheduled reports

- Description: Recurring report generation and delivery.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Routine oversight.
- Priority: P2
- Product area: Reporting
- Dependencies: SEC-002 (RBAC); AUT-012 (background jobs)
- Data required: Schedules.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Schedule editor.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Delivery failure -> retry.
- Acceptance criteria: Recipients limited to authorised roles.
- Future extensions: Subscriptions.

## [REP-014] Report access control

- Description: Enforces who may generate and download each report type and scope.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Protects personal data in reports.
- Priority: P0
- Product area: Reporting
- Dependencies: SEC-002
- Data required: Permissions; report scope.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Enforced on all /api/v1/reports routes
- UI requirements: Unavailable report types hidden and disabled server-side.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Unauthorised download -> 403 and audit.
- Acceptance criteria: Authorisation tests cover every report type and role.
- Future extensions: Signed download URLs (P1).

## [REP-015] Report audit trail

- Description: Audits report generation and downloads.
- Primary user: Training manager
- Secondary users: Department administrator; Learner (own reports); System auditor
- Business value: Accountability for personal data exports.
- Priority: P0
- Product area: Reporting
- Dependencies: SEC-009
- Data required: AuditLog.
- AI involvement: None.
- Human review required: Reports are decision support; any report about an individual is visible to that individual on request.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Audit entries for report events
- UI requirements: Visible in Audit logs.
- Security considerations: Report access control; generation and downloads audited; exports contain only fields permitted for the requester's scope.
- Accessibility considerations: Reports available as accessible HTML views before export; exports include headers and units.
- Failure cases: Audit write failure -> download refused.
- Acceptance criteria: No report download occurs without an audit record.
- Future extensions: Access reviews.

---

# P. Security


## [SEC-001] Authentication

- Description: Email/username and password authentication with secure hashing for MVP; SSO-ready adapter.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Only known users access the platform.
- Priority: P0
- Product area: Security
- Dependencies: SEC-013; SEC-014
- Data required: User credentials (hashed).
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/auth/login; POST /api/v1/auth/logout; GET /api/v1/auth/session; POST /api/v1/auth/password/change
- UI requirements: Login screen.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Brute force -> rate limiting and lockout policy; unknown user -> generic error.
- Acceptance criteria: Passwords hashed with a modern adaptive algorithm; generic login errors; lockout/rate limits enforced; all events audited.
- Future extensions: SSO/OIDC (SEC-004).

## [SEC-002] Role-based access control

- Description: Server-side permission checks for eight access roles scoped by organisation and department.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Least-privilege access to personal and restricted data.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Access role assignments; permission matrix.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Enforced in every endpoint via dependency-injected policy checks
- UI requirements: UI hides unavailable actions (never relied on for security).
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Missing permission -> 403; ambiguous scope -> deny.
- Acceptance criteria: Every endpoint has an authorisation test per role in the permission matrix (SECURITY_RESPONSIBLE_AI.md §RBAC).
- Future extensions: Permission management (ADM-016).

## [SEC-003] JWT or secure session architecture

- Description: Server-side sessions with HttpOnly, Secure, SameSite cookies and CSRF protection (recommended; DEC-007).
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Revocable sessions for a browser application.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Session store.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Session cookie; CSRF token header
- UI requirements: Session expiry prompts.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Stolen session -> revocation on logout/password change.
- Acceptance criteria: Sessions revocable server-side; cookies HttpOnly/Secure/SameSite; CSRF protection on state-changing requests.
- Future extensions: Token-based API clients (P1).

## [SEC-004] OAuth/SSO readiness

- Description: Authentication adapter supporting OIDC providers when authorised.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Integration with government identity providers.
- Priority: P1
- Product area: Security
- Dependencies: None (foundational)
- Data required: Provider metadata.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Auth adapter (API_INTEGRATION_SPEC.md)
- UI requirements: SSO button when configured.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Provider unavailable -> local login policy.
- Acceptance criteria: No provider enabled without verified configuration.
- Future extensions: Parichay or other SSO (Decision required).

## [SEC-005] Admin authentication

- Description: Stronger requirements for administrative roles (shorter sessions; re-authentication for sensitive actions; MFA when available).
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Protects high-privilege accounts.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Session metadata.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Re-auth endpoint POST /api/v1/auth/reauthenticate
- UI requirements: Re-authentication dialog.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Re-auth failure -> action blocked.
- Acceptance criteria: Sensitive admin actions require recent authentication; MFA requirement recorded as Decision required.
- Future extensions: MFA (P1).

## [SEC-006] Encryption in transit

- Description: TLS for all external traffic; internal traffic encrypted where crossing hosts.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Confidentiality of personal data.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Certificates.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): HTTPS only; HSTS
- UI requirements: None.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Plain HTTP -> redirect/deny.
- Acceptance criteria: No production endpoint accepts plain HTTP.
- Future extensions: mTLS internal (P2).

## [SEC-007] Encryption at rest

- Description: Database, backups and object storage encrypted at rest by the hosting platform or disk encryption.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Protection against media theft.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Storage configuration.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: None.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Unencrypted volume -> deployment check fails.
- Acceptance criteria: Deployment checklist verifies encryption at rest (hosting decision pending).
- Future extensions: Field-level encryption for sensitive fields (P1).

## [SEC-008] Secure APIs

- Description: Validated, authenticated, authorised, rate-limited APIs following OWASP API Security guidance.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Reduces API abuse risk.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: OpenAPI schema.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): All /api/v1 routes
- UI requirements: None.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Mass assignment -> explicit schemas prevent it.
- Acceptance criteria: Request/response schemas explicit; no unauthenticated routes except login, health and readiness.
- Future extensions: API gateway (P2).

## [SEC-009] Audit logs

- Description: Append-only audit records for security, administrative, review and data-access events.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Accountability and investigation.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: AuditLog.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/audit-logs
- UI requirements: Audit logs screen.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Audit write failure for critical events -> operation fails closed.
- Acceptance criteria: Critical events (login, role change, approval, adjustment, export) always produce audit records with actor, action, target, time and correlation ID.
- Future extensions: Tamper-evident hashing (P1).

## [SEC-010] Activity logs

- Description: Operational application logs (structured, redacted).
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Troubleshooting.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Log stream.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: None.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Secrets in logs -> redaction filter.
- Acceptance criteria: Logs are structured JSON with correlation IDs and redaction of secrets and personal fields.
- Future extensions: Central log platform (OBSERVABILITY_SPEC.md).

## [SEC-011] AI interaction logs

- Description: Records every AI provider call: purpose, model, prompt version, input references, output, validation, tokens, latency, user and correlation ID.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Traceability of AI behaviour.
- Priority: P0
- Product area: Security
- Dependencies: RAI-019
- Data required: AIInteractionLog.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/ai-interactions; GET /api/v1/ai-interactions/{id}
- UI requirements: Audit logs screen (AI tab).
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Log write failure -> AI response not shown.
- Acceptance criteria: No AI output is shown to a user without an AIInteractionLog record; stored content follows retention and redaction rules.
- Future extensions: Evaluation sampling.

## [SEC-012] Document-level access control

> Alias of **MAT-028** - see that entry for the full specification.

- Description: Access scopes on materials enforced across storage, retrieval, AI context and downloads (see MAT-028).
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: See MAT-028.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: See MAT-028.
- AI involvement: See MAT-028.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See MAT-028
- UI requirements: See MAT-028.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: See MAT-028.
- Acceptance criteria: See MAT-028.
- Future extensions: See MAT-028.

## [SEC-013] Session management

- Description: Idle and absolute timeouts, logout everywhere, session rotation on privilege change.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Limits session hijacking impact.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Sessions.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/auth/logout; POST /api/v1/auth/sessions/revoke-all
- UI requirements: Timeout warning dialog.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Timeout during form -> draft preserved where safe.
- Acceptance criteria: Session ID rotates on login and privilege change; timeouts configurable.
- Future extensions: Device list (P1).

## [SEC-014] Rate limiting

- Description: Per-user and per-IP limits, stricter on login and AI endpoints.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Abuse and cost control.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Rate-limit counters (Redis or DB).
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): 429 responses with Retry-After
- UI requirements: Friendly rate-limit message.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Limiter unavailable -> fail closed for AI endpoints, open with logging for reads (decision recorded).
- Acceptance criteria: AI and login endpoints have documented limits; 429 includes Retry-After.
- Future extensions: Adaptive limits.

## [SEC-015] Input validation

- Description: Schema validation of all inputs; file validation; length limits.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Prevents injection and malformed data.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Pydantic schemas.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): 422 validation errors
- UI requirements: Inline form errors.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Invalid input -> 422 with field details.
- Acceptance criteria: No endpoint accepts unvalidated input.
- Future extensions: Content security scanning.

## [SEC-016] Output validation

- Description: Validates API responses and AI outputs against schemas; encodes rendered content.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Prevents data leakage and XSS.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Response schemas.
- AI involvement: Structured output validation for AI.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Response models
- UI requirements: Sanitised rendering of AI text (no raw HTML).
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Schema mismatch -> error, not partial data.
- Acceptance criteria: AI text rendered as plain text/markdown sanitised; responses filtered to declared fields.
- Future extensions: Output DLP (P2).

## [SEC-017] Secret management

- Description: Secrets only in environment/secret store; never in code, logs, API responses or client bundles.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Prevents credential leakage.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Environment variables; secret store.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Partially implemented - .env git-ignored and .env.example placeholders only; no CI secret scanning.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: Settings never display secrets.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Secret committed -> pre-commit/CI scan fails.
- Acceptance criteria: Secret scanning in CI; .env git-ignored; .env.example has placeholders only.
- Future extensions: Managed secret store (hosting decision).

## [SEC-018] Data retention

- Description: Retention periods per data class with automated purge jobs.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Data minimisation and compliance.
- Priority: P1
- Product area: Security
- Dependencies: None (foundational)
- Data required: Retention policy.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Retention jobs (P1)
- UI requirements: Retention settings (ADM-018).
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Purge failure -> retried and alerted.
- Acceptance criteria: Retention periods defined and approved before production (Decision required).
- Future extensions: Legal hold.

## [SEC-019] Data deletion

- Description: User and administrator-initiated deletion with propagation to derived data.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Honours deletion requests.
- Priority: P1
- Product area: Security
- Dependencies: None (foundational)
- Data required: Deletion requests.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/me/deletion-requests (P1)
- UI requirements: Deletion request flow.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Audit-required records -> pseudonymised instead of deleted (policy decision).
- Acceptance criteria: Deletion propagates to chunks, embeddings and logs per policy.
- Future extensions: Automated DSAR handling.

## [SEC-020] Backup and recovery

- Description: Encrypted backups with tested restore procedure and defined RPO/RTO.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Resilience.
- Priority: P1
- Product area: Security
- Dependencies: None (foundational)
- Data required: Backups.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: None.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: Restore failure -> incident.
- Acceptance criteria: Restore tested before production; RPO/RTO decided.
- Future extensions: Cross-region replicas.

## [SEC-021] Threat modeling

- Description: Documented threat model maintained per release.
- Primary user: Platform administrator
- Secondary users: System auditor; all users
- Business value: Systematic risk reduction.
- Priority: P0
- Product area: Security
- Dependencies: None (foundational)
- Data required: Threat model.
- AI involvement: None.
- Human review required: Security-relevant configuration changes require an authorised administrator and are audited.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: None.
- Security considerations: See SECURITY_RESPONSIBLE_AI.md for controls and threat model.
- Accessibility considerations: Authentication and security prompts accessible (no CAPTCHA without accessible alternative).
- Failure cases: New feature without threat review -> blocked from release.
- Acceptance criteria: Threat model in SECURITY_RESPONSIBLE_AI.md reviewed at each phase exit.
- Future extensions: External penetration test before production.

---

# Q. Responsible AI


## [RAI-001] Retrieval grounding

- Description: Generative answers and questions are produced only from retrieved, accessible, licence-permitted sources.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Reduces fabrication; keeps content official.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Retrieved chunks.
- AI involvement: RAG constraints (AI_SYSTEM_SPEC.md §11).
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Enforced in document-qa and generation
- UI requirements: Source panel.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: No sources -> abstain.
- Acceptance criteria: Prompts contain only retrieved chunks as knowledge; evaluation set checks unanswerable questions abstain.
- Future extensions: Claim-level verification.

## [RAI-002] Citations

> Alias of **MAT-019** - see that entry for the full specification.

- Description: Every grounded output carries verified citations (see MAT-019).
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: See MAT-019.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: See MAT-019.
- AI involvement: See MAT-019.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See MAT-019
- UI requirements: Citation chips.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: See MAT-019.
- Acceptance criteria: See MAT-019.
- Future extensions: See MAT-019.

## [RAI-003] Confidence indicators

- Description: Rule-based confidence/evidence bands on AI outputs and estimates with defined meanings.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Calibrated user trust.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Retrieval scores; verification; evidence counts.
- AI involvement: Rule-based.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): confidence field on AI responses
- UI requirements: Band label and definition.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Unknown -> 'low'.
- Acceptance criteria: Band definitions published in UI copy; no numeric accuracy claims without evaluation.
- Future extensions: Calibrated probabilities.

## [RAI-004] Hallucination mitigation

- Description: Combination of grounding, span verification, independent validation and abstention.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Protects learners from false statements.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Chunks; outputs.
- AI involvement: Validators (AI_SYSTEM_SPEC.md §18).
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal
- UI requirements: Unsupported-content flags.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Verification fails -> output withheld.
- Acceptance criteria: Unverified generated statements are never displayed as fact.
- Future extensions: Entailment models.

## [RAI-005] Question validation

- Description: Automated schema, grounding, duplicate and answer-key validation before review (ASM-022 to ASM-024).
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Reviewer time focused on plausible questions.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Questions; chunks.
- AI involvement: Validators.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/questions/{id}/validations
- UI requirements: Validation panel.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Validator error -> 'validation_incomplete'.
- Acceptance criteria: Every AI-generated question has a validation record before entering review.
- Future extensions: Quality scoring (ASM-025).

## [RAI-006] Human approval

> Alias of **ASM-028** - see that entry for the full specification.

- Description: Approval gate for AI-generated learner-facing content (see ASM-028).
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: See ASM-028.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: See ASM-028.
- AI involvement: See ASM-028.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See ASM-028
- UI requirements: See ASM-028.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: See ASM-028.
- Acceptance criteria: See ASM-028.
- Future extensions: See ASM-028.

## [RAI-007] Prompt-injection protection

- Description: Treat documents and user input as untrusted data; isolate instructions; no side-effecting tools; detect and flag injection patterns; test suite.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Integrity of AI behaviour.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Inputs; detection rules.
- AI involvement: Defences (AI_SYSTEM_SPEC.md §36).
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal
- UI requirements: Restricted-response notice.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Detection -> restricted output and security event.
- Acceptance criteria: Injection test corpus passes for Q&A and generation before MVP release.
- Future extensions: Classifier detection (P1).

## [RAI-008] Audit trails

> Alias of **SEC-011** - see that entry for the full specification.

- Description: AI-related audit trail combining SEC-009 and SEC-011.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: See SEC-011.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: See SEC-011.
- AI involvement: See SEC-011.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See SEC-011
- UI requirements: Audit logs screen.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: See SEC-011.
- Acceptance criteria: See SEC-011.
- Future extensions: See SEC-011.

## [RAI-009] Safety filters

- Description: Blocks abusive, discriminatory or out-of-scope content in inputs and outputs; relies on provider safety plus application checks.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Professional, safe environment.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Filter rules.
- AI involvement: Provider safety behaviour plus rules.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal; refusal handling
- UI requirements: Polite refusal message.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Provider refusal -> handled as abstention with reason category.
- Acceptance criteria: Refusals and filtered outputs logged and displayed with neutral messaging.
- Future extensions: Custom moderation model.

## [RAI-010] Bias monitoring

- Description: Monitors assessment and recommendation outcomes for disparities across permitted, consented groupings.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Fairness.
- Priority: P1
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Aggregates; permitted attributes (none collected in MVP).
- AI involvement: Statistical checks.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/analytics/fairness (P1)
- UI requirements: Fairness report for auditors.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: No attributes -> item-level checks only.
- Acceptance criteria: No sensitive attributes collected without legal basis; methodology reviewed.
- Future extensions: External fairness audit.

## [RAI-011] Explainable recommendations

- Description: Every recommendation and path item states the rule and data that produced it.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Trust and contestability.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Recommendation reasons.
- AI involvement: Template explanations.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): reason object on recommendation payloads
- UI requirements: 'Why recommended' text.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Missing reason -> recommendation suppressed.
- Acceptance criteria: No recommendation is displayed without a reason.
- Future extensions: Natural-language explanations (P1).

## [RAI-012] Model evaluation

- Description: Offline evaluation harness for Q&A grounding, abstention and question validation using golden datasets built from collected public documents.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Evidence before claims.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Golden datasets (to be created and approved).
- AI involvement: Evaluation runs.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal tooling; results stored as reports
- UI requirements: Evaluation summary for administrators.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: No golden dataset -> release gate cannot pass.
- Acceptance criteria: MVP release requires evaluation results recorded for each prompt version; no accuracy figures published without these results.
- Future extensions: Online evaluation (AI_SYSTEM_SPEC.md §34).

## [RAI-013] Dataset evaluation

- Description: Evaluates coverage and quality of source corpora and question banks.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Detects blind spots.
- Priority: P1
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Corpus metadata.
- AI involvement: Analysis.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): P1
- UI requirements: Corpus report.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Stale sources -> flagged.
- Acceptance criteria: Coverage by topic reported.
- Future extensions: Automated freshness checks.

## [RAI-014] AI output versioning

- Description: AI artefacts store model, prompt version, parameters and timestamps; edits create versions.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Reproducibility and audit.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Version fields.
- AI involvement: None.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Version metadata on artefacts
- UI requirements: Version info panels.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Missing metadata -> artefact rejected.
- Acceptance criteria: Every AI artefact has model ID, prompt version, created_at and validation/review status.
- Future extensions: Replay tooling.

## [RAI-015] Abstention behavior

- Description: The system declines to answer when evidence is insufficient or verification fails.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Prevents confident wrong answers.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Retrieval scores; verification.
- AI involvement: Abstention rules.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): abstained flag with reason
- UI requirements: Abstention message with next steps.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Over-abstention -> tuned via evaluation.
- Acceptance criteria: Unanswerable golden questions yield abstentions; abstentions logged with reason.
- Future extensions: Escalation to trainers.

## [RAI-016] Sensitive-data minimization

- Description: Only necessary data sent to AI providers; personal identifiers excluded or redacted; uploads screened for personal data.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Privacy protection.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Redaction rules.
- AI involvement: Pre-call redaction.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Partially implemented - collected datasets validated free of personal data (validator LP-09); no AI calls exist yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal
- UI requirements: Warning when redaction occurred.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: PII detected in upload -> quarantined for review.
- Acceptance criteria: Provider payloads never include user names, emails or IDs; redaction tests pass.
- Future extensions: Self-hosted models for sensitive workloads (Decision required).

## [RAI-017] Human override

- Description: Authorised humans can override AI validation results, estimates (CMP-019) and withdraw AI artefacts.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Humans remain in control.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: Override records.
- AI involvement: None.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Decision and adjustment endpoints
- UI requirements: Override actions with reason.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Override without reason -> blocked.
- Acceptance criteria: All overrides require reason and are audited.
- Future extensions: Override analytics.

## [RAI-018] Appeal/correction workflow

- Description: Learners request correction of estimates or question results; reviewers respond with outcome and reason.
- Primary user: Learner
- Secondary users: Trainer; Training manager
- Business value: Contestability of automated outputs.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: CorrectionRequest.
- AI involvement: None.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/correction-requests; GET /api/v1/correction-requests; PATCH /api/v1/correction-requests/{id}
- UI requirements: Request action on profile/results; review queue.
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Unanswered request beyond SLA -> escalated to training manager (SLA: Decision required).
- Acceptance criteria: Every request receives a recorded decision and reason; outcome visible to the learner.
- Future extensions: Formal grievance integration (P2).

## [RAI-019] Model and prompt registry

- Description: Versioned registry of prompt templates and model configurations used by AI services.
- Primary user: Platform administrator
- Secondary users: System auditor; Trainer; Learner
- Business value: Controlled change and traceability.
- Priority: P0
- Product area: Responsible AI
- Dependencies: SEC-011 (AI interaction logs)
- Data required: PromptTemplate; model config.
- AI involvement: None.
- Human review required: Human review and override apply to all AI-generated artefacts (SECURITY_RESPONSIBLE_AI.md).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/admin/prompt-templates; POST /api/v1/admin/prompt-templates/{key}/versions
- UI requirements: Registry view (platform administrator).
- Security considerations: AI provider receives only authorised data; outputs validated; interactions logged.
- Accessibility considerations: AI states (confidence, abstention, MOCK, unreviewed) conveyed in text, not only colour or icons.
- Failure cases: Unregistered prompt in use -> startup check fails.
- Acceptance criteria: AI services can only use registered prompt versions; changes audited and linked to evaluation results.
- Future extensions: Automated evaluation gating.

---

# R. Automation


## [AUT-001] Automated recommendations

- Description: Recomputes recommendations after assessment submission or catalogue changes.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Fresh guidance without manual steps.
- Priority: P0
- Product area: Automation
- Dependencies: AI-005; AUT-012
- Data required: Gaps; catalogue.
- AI involvement: Rule-based.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Background job triggered by attempt submission
- UI requirements: Updated recommendation cards.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Job failure -> previous recommendations retained with 'may be outdated' notice.
- Acceptance criteria: Recomputation is idempotent per input snapshot.
- Future extensions: Scheduled refresh (AUT-010).

## [AUT-002] Competency updates

- Description: Recomputes estimates when evidence changes (new attempt, voided evidence, adjustment).
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Estimates stay consistent with evidence.
- Priority: P0
- Product area: Automation
- Dependencies: AI-012; AI-016
- Data required: Evidence.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Background job
- UI requirements: Profile refresh.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Failure -> estimate marked stale.
- Acceptance criteria: Recomputation audited; stale estimates flagged.
- Future extensions: Event sourcing (P2).

## [AUT-003] Quiz generation (job)

- Description: Runs AI-007 generation as background jobs with progress.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Long generation without blocking UI.
- Priority: P0
- Product area: Automation
- Dependencies: AI-007; AUT-012
- Data required: Job parameters.
- AI involvement: LLM.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/question-generation-jobs
- UI requirements: Job progress.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Timeout -> retry; exhausted -> failed with reason.
- Acceptance criteria: Jobs idempotent by client key; partial results saved with status.
- Future extensions: Batch generation.

## [AUT-004] Answer evaluation (automation)

> Alias of **AI-009** - see that entry for the full specification.

- Description: Automatic scoring on submission (see AI-009).
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: See AI-009.
- Priority: P0
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: See AI-009.
- AI involvement: See AI-009.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See AI-009
- UI requirements: See AI-009.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: See AI-009.
- Acceptance criteria: See AI-009.
- Future extensions: See AI-009.

## [AUT-005] Weak-topic detection (automation)

> Alias of **AI-014** - see that entry for the full specification.

- Description: Scheduled computation of weak topics (see AI-014).
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: See AI-014.
- Priority: P1
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: See AI-014.
- AI involvement: See AI-014.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See AI-014
- UI requirements: See AI-014.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: See AI-014.
- Acceptance criteria: See AI-014.
- Future extensions: See AI-014.

## [AUT-006] Reassessment reminders

- Description: Reminds learners when reassessment is suggested.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Closes learning loop.
- Priority: P1
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Reassessment triggers.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Notification job (P1)
- UI requirements: Reminder notifications.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Delivery failure -> retry.
- Acceptance criteria: Learners can opt out.
- Future extensions: Channels (email/SMS) via notification adapter.

## [AUT-007] Notifications

- Description: In-app and email notifications through a notification adapter.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Timely awareness.
- Priority: P1
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Notification.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/notifications; PATCH /api/v1/notifications/{id} (P1)
- UI requirements: Notification centre.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Provider down -> queued.
- Acceptance criteria: Notification preferences respected; no personal data in email subject lines.
- Future extensions: SMS/WhatsApp adapters (P2).

## [AUT-008] Report generation (automation)

- Description: Asynchronous generation for large reports.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Scalability.
- Priority: P1
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Report jobs.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/reports (async)
- UI requirements: Report status.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Failure -> retry.
- Acceptance criteria: Idempotent by request key.
- Future extensions: Scheduled reports.

## [AUT-009] Learning-path updates

- Description: Automatic path refresh when gaps change.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Paths stay current.
- Priority: P1
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Gaps.
- AI involvement: Rule-based.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Background job (P1)
- UI requirements: 'Path updated' notice with diff.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Failure -> previous path kept.
- Acceptance criteria: Learner sees what changed and why.
- Future extensions: Notifications.

## [AUT-010] Scheduled data refresh

- Description: Scheduled URL checks and re-collection of source documents via existing manifest-based scripts.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Detects moved or updated official documents.
- Priority: P1
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Collection manifests; sidecars.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Partially implemented - manual, re-runnable collection and URL-check scripts exist (scripts/collectors/fetch_documents.py, scripts/validators/check_document_urls.py); no scheduler.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Scheduled job (P1)
- UI requirements: Source freshness report.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Source changed -> new version flagged for review, never overwritten.
- Acceptance criteria: Refresh never overwrites raw files; changed checksums create review tasks.
- Future extensions: Change notifications.

## [AUT-011] Integration synchronization

> Alias of **IGOT-005** - see that entry for the full specification.

- Description: Scheduled iGOT sync jobs (see IGOT-005).
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: See IGOT-005.
- Priority: P1
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: See IGOT-005.
- AI involvement: See IGOT-005.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Blocked by external access - requires authorised iGOT access.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See IGOT-005
- UI requirements: See IGOT-005.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: See IGOT-005.
- Acceptance criteria: See IGOT-005.
- Future extensions: See IGOT-005.

## [AUT-012] Background jobs

- Description: Job system for document processing, generation, recommendations and reports.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Responsive UI and reliable long tasks.
- Priority: P0
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: BackgroundJob.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/jobs/{id}
- UI requirements: Job status components.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Worker crash -> job re-queued by visibility timeout.
- Acceptance criteria: Every job records type, status, attempts, timestamps, error and correlation ID.
- Future extensions: Autoscaling workers.

## [AUT-013] Retry queues

- Description: Bounded retries with backoff and dead-letter state.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Recovers from transient failures without infinite loops.
- Priority: P0
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Job attempts.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Internal
- UI requirements: Failed state with retry action.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Max attempts reached -> dead-letter and alert.
- Acceptance criteria: Retry limits configured per job type; dead-lettered jobs visible to platform administrators.
- Future extensions: Automatic remediation.

## [AUT-014] Job monitoring

- Description: Job metrics and dashboard (queue depth, failures, durations).
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: Operational visibility.
- Priority: P0
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Job metrics.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/admin/jobs (platform administrator)
- UI requirements: Jobs panel in Integration health/Admin.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Metrics unavailable -> logs only.
- Acceptance criteria: Failed and stuck jobs visible within one refresh interval.
- Future extensions: Alerting (OBSERVABILITY_SPEC.md).

## [AUT-015] Idempotency

- Description: Idempotency keys for job-creating and state-changing POSTs; idempotent job handlers.
- Primary user: Platform administrator
- Secondary users: Trainer; Learner
- Business value: No duplicates on retries.
- Priority: P0
- Product area: Automation
- Dependencies: AUT-012 (background jobs)
- Data required: Idempotency records.
- AI involvement: None.
- Human review required: Automations never publish AI-generated content or change employment-relevant data without human approval.
- MVP status: In MVP
- Implementation status: Partially implemented - collection scripts skip already-collected files by checksum; no API idempotency.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Idempotency-Key header
- UI requirements: Double-submit protection.
- Security considerations: Jobs run with least privilege, organisation scoping and audit of side effects.
- Accessibility considerations: Job status and failures communicated accessibly in UI.
- Failure cases: Key reuse with different payload -> 409.
- Acceptance criteria: Repeating a request with the same key returns the original result.
- Future extensions: Global idempotency store.

---

# S. UX and platform experience


## [UX-001] Responsive design

- Description: Layouts adapt to desktop, tablet and mobile widths.
- Primary user: Learner
- Secondary users: All users
- Business value: Usable on office desktops and phones.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: None.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: All screens (UI_UX_SPEC.md breakpoints).
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Horizontal scrolling -> layout bug.
- Acceptance criteria: Core journeys usable at 360px width without horizontal page scrolling.
- Future extensions: Native app (FUT-011).

## [UX-002] Mobile-friendly experience

- Description: Touch targets, readable text and simplified navigation on small screens.
- Primary user: Learner
- Secondary users: All users
- Business value: Access away from desks.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: None.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: Mobile navigation pattern.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Small targets -> test failure.
- Acceptance criteria: Touch targets meet minimum size; assessments completable on mobile.
- Future extensions: PWA (P2).

## [UX-003] Personalized home

- Description: Role-specific home: learner dashboard, trainer dashboard or admin dashboard (see PER-001, TRN-001).
- Primary user: Learner
- Secondary users: All users
- Business value: Relevant starting point per user.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Role.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me
- UI requirements: Home routing.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Multiple roles -> role switcher.
- Acceptance criteria: Users with multiple access roles can switch views; default matches primary role.
- Future extensions: Custom widgets.

## [UX-004] Global search

- Description: Search across courses, materials and help.
- Primary user: Learner
- Secondary users: All users
- Business value: Faster navigation.
- Priority: P1
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Search indexes.
- AI involvement: Optional semantic.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/search/global (P1)
- UI requirements: Header search.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Partial index failure -> partial results notice.
- Acceptance criteria: Results respect permissions.
- Future extensions: Command palette.

## [UX-005] Notifications

> Alias of **AUT-007** - see that entry for the full specification.

- Description: UI for notifications (see AUT-007).
- Primary user: Learner
- Secondary users: All users
- Business value: See AUT-007.
- Priority: P1
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: See AUT-007.
- AI involvement: See AUT-007.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): See AUT-007
- UI requirements: Bell menu.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: See AUT-007.
- Acceptance criteria: See AUT-007.
- Future extensions: See AUT-007.

## [UX-006] Calendar

- Description: Calendar of learning plans and programmes.
- Primary user: Learner
- Secondary users: All users
- Business value: Planning.
- Priority: P2
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Plans; programme dates (dates currently unknown).
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Calendar view.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Dates unknown -> not shown.
- Acceptance criteria: No invented dates.
- Future extensions: Calendar sync.

## [UX-007] Bookmarks

- Description: Save courses, materials and passages.
- Primary user: Learner
- Secondary users: All users
- Business value: Quick return.
- Priority: P1
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Bookmark.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST/DELETE /api/v1/me/bookmarks (P1)
- UI requirements: Bookmark toggle.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Deleted target -> bookmark marked unavailable.
- Acceptance criteria: Bookmarks private.
- Future extensions: Collections.

## [UX-008] Recently viewed

- Description: Recently opened items.
- Primary user: Learner
- Secondary users: All users
- Business value: Continuity.
- Priority: P1
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Activity.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/me/recent (P1)
- UI requirements: Recent list.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: None specific.
- Acceptance criteria: Only own history.
- Future extensions: Cross-device.

## [UX-009] Continue learning

- Description: Card resuming the next in-progress path item or attempt.
- Primary user: Learner
- Secondary users: All users
- Business value: Reduces friction.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Path; attempts.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Included in GET /api/v1/me/dashboard
- UI requirements: Continue card on dashboard.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Nothing in progress -> next recommended item.
- Acceptance criteria: Card always points to an accessible, existing item.
- Future extensions: Deep resume positions.

## [UX-010] Dark mode

- Description: Dark colour theme.
- Primary user: Learner
- Secondary users: All users
- Business value: Comfort.
- Priority: P2
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Theme tokens.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): User preference (P2)
- UI requirements: Theme toggle.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Contrast failures -> token fix.
- Acceptance criteria: Meets contrast requirements.
- Future extensions: System sync.

## [UX-011] Accessibility

> Alias of **ACC-009** - see that entry for the full specification.

- Description: Umbrella for L-category accessibility features (see ACC-009/010/014/015/016).
- Primary user: Learner
- Secondary users: All users
- Business value: See category L.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: See category L.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: All screens.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: See category L.
- Acceptance criteria: See ACC-009, ACC-010, ACC-014, ACC-015, ACC-016.
- Future extensions: See category L.

## [UX-012] Empty states

- Description: Designed empty states explaining why content is empty and what to do.
- Primary user: Learner
- Secondary users: All users
- Business value: Guidance instead of dead ends.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: None.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: Per-screen empty states (UI_UX_SPEC.md).
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: None specific.
- Acceptance criteria: Every list and dashboard card has a defined empty state.
- Future extensions: Contextual help.

## [UX-013] Loading states

- Description: Skeletons and progress for loading and background jobs.
- Primary user: Learner
- Secondary users: All users
- Business value: Perceived performance and clarity.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: None.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: Skeleton and progress components.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Long load -> timeout message.
- Acceptance criteria: Every async view has loading and timeout states.
- Future extensions: Optimistic updates.

## [UX-014] Error states

- Description: Consistent recoverable error states mapped from API problem codes.
- Primary user: Learner
- Secondary users: All users
- Business value: Users can recover without support.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Error codes.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Problem responses (ERROR_HANDLING_SPEC.md)
- UI requirements: Error components.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Unknown error -> generic message with correlation ID.
- Acceptance criteria: Every error shows a human message, next step and correlation ID; no stack traces.
- Future extensions: Inline help links.

## [UX-015] Onboarding

- Description: First-login flow: profile confirmation, department and job role selection, privacy notice, optional pre-assessment start.
- Primary user: Learner
- Secondary users: All users
- Business value: Fast, informed start.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: User; roles.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/PATCH /api/v1/me; PUT /api/v1/me/job-role
- UI requirements: Onboarding screen.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: No roles configured -> blocked with admin contact.
- Acceptance criteria: Users see the privacy/AI-use notice before any assessment; onboarding resumable.
- Future extensions: Guided tours (UX-018).

## [UX-016] Help center

- Description: Help articles, FAQs and AI-use explanations.
- Primary user: Learner
- Secondary users: All users
- Business value: Self-service support.
- Priority: P1
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Help content.
- AI involvement: Optional grounded help Q&A (P2).
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET /api/v1/help (P1)
- UI requirements: Help panel.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: None specific.
- Acceptance criteria: Includes plain-language explanation of AI use and limitations.
- Future extensions: Contextual help.

## [UX-017] Feedback collection

- Description: Product feedback widget (see TRN-014 for content feedback).
- Primary user: Learner
- Secondary users: All users
- Business value: Continuous improvement.
- Priority: P1
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Feedback.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): POST /api/v1/feedback (P1)
- UI requirements: Feedback widget.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: None specific.
- Acceptance criteria: Feedback optional and anonymous where configured.
- Future extensions: In-app surveys.

## [UX-018] Guided workflows

- Description: Step-by-step guidance for complex tasks (e.g. building a quiz).
- Primary user: Learner
- Secondary users: All users
- Business value: Reduces errors.
- Priority: P1
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: None.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P1 - post-MVP)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): N/A
- UI requirements: Stepper components.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Abandoned flow -> draft saved.
- Acceptance criteria: Steps resumable.
- Future extensions: Interactive tours.

## [UX-019] Search filters

- Description: Filters for document library, courses and review queues (organisation, topic, type, status).
- Primary user: Learner
- Secondary users: All users
- Business value: Efficient browsing.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Indexed metadata.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Filter parameters per API_INTEGRATION_SPEC.md conventions
- UI requirements: Filter bars with chips.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Invalid filter -> ignored with notice.
- Acceptance criteria: Filters reflected in URL; accessible filter controls.
- Future extensions: Saved views (UX-020).

## [UX-020] Saved views

- Description: Save filter combinations.
- Primary user: Learner
- Secondary users: All users
- Business value: Repeat analysis.
- Priority: P2
- Product area: UX and platform experience
- Dependencies: ACC-009 (screen reader); ACC-010 (keyboard)
- Data required: Saved view.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Saved view menu.
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: None specific.
- Acceptance criteria: Private by default.
- Future extensions: Shared views.

## [UX-021] User profile and account settings

- Description: Self-service profile (name, designation, department, job role, language preference) and privacy information. Added to satisfy the P0 'User profile' requirement, which had no item in the inventory.
- Primary user: Learner
- Secondary users: All users
- Business value: Accurate profile data and user control.
- Priority: P0
- Product area: UX and platform experience
- Dependencies: SEC-001; ROLE-001
- Data required: User.
- AI involvement: None.
- Human review required: Not applicable unless the UX element displays AI-generated content (then RAI rules apply).
- MVP status: In MVP
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): GET/PATCH /api/v1/me
- UI requirements: Settings screen (profile section).
- Security considerations: UI never trusted for authorisation; no sensitive data cached in browser storage.
- Accessibility considerations: Follows UI_UX_SPEC.md accessibility rules.
- Failure cases: Invalid change -> validation errors; role change -> audited.
- Acceptance criteria: Users can view and edit permitted profile fields; changes affecting assessments (job role) are audited.
- Future extensions: Data download (P1).

---

# T. Future intelligence


## [FUT-001] Predictive analysis

- Description: Predictive models over learning and capability data.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-002] Skill-demand forecasting

- Description: Forecasts future competency demand from role and programme trends.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-003] Career pathways

- Description: Voluntary, learner-initiated pathway exploration between roles.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-004] Knowledge tracing

- Description: Models mastery of knowledge components over time.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-005] Bayesian Knowledge Tracing

- Description: BKT models for mastery estimation.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-006] Item Response Theory

- Description: IRT calibration of items and ability estimation.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-007] AI certification

- Description: Assessment programmes leading to certification with human sign-off.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-008] Competency passport

- Description: Portable, verifiable record of human-verified competencies.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-009] Offline mode

- Description: Offline access to materials and practice.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-010] Low-bandwidth mode

- Description: Dedicated lite experience beyond ACC-017.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-011] Mobile application

- Description: Native or installable mobile application.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-012] Voice interface

- Description: Voice interaction for tutor and navigation.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-013] Workforce intelligence

- Description: Aggregated capability intelligence for planning.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-014] Cross-department intelligence

- Description: Cross-department capability insights with strict aggregation.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-015] Resource optimization

- Description: Optimises allocation of training resources.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-016] AI trainer designer

- Description: AI-assisted design of training programmes with expert review.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-017] Simulation-based learning

- Description: Simulated statistical work scenarios.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.

## [FUT-018] Organization-wide capability planning

- Description: Long-range capability planning across the organisation.
- Primary user: Organization administrator
- Secondary users: Training manager; Platform administrator
- Business value: Strategic capability beyond MVP and P1.
- Priority: P2
- Product area: Future intelligence
- Dependencies: Validated historical data; fairness and ethics review
- Data required: To be determined; requires validated historical data and legal basis.
- AI involvement: To be determined at design time; evaluation before any use.
- Human review required: Required: all outputs advisory; never used for automated employment decisions.
- MVP status: Excluded from MVP (P2 - future)
- Implementation status: Planned - No application code exists yet.
- API requirements: Planned internal API (docs/API_INTEGRATION_SPEC.md): Not defined until P2 design.
- UI requirements: Not defined until P2 design.
- Security considerations: Requires a new data protection impact assessment and ethics review before design.
- Accessibility considerations: To be specified at design time.
- Failure cases: Insufficient validated data -> feature not enabled.
- Acceptance criteria: Not built until a design, data protection impact assessment and evaluation plan are approved.
- Future extensions: To be defined.
