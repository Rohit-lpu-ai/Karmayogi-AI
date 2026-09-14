# Product Requirements Document

## 1. Document metadata

| Field | Value |
|---|---|
| **Product name** | Working name undecided (Decision required: [DECISIONS.md](DECISIONS.md) DEC-001). The repository history uses "AURA"; the GitHub repository is `Karmayogi-AI`; the local folder is `KaramYogiAI`. This document uses **"the platform"**. |
| **Product category** | AI-assisted competency intelligence and personalized learning platform for India's official statistical system |
| **Version** | 1.0.0-draft |
| **Status** | Draft for approval. No implementation authorised until approved. |
| **Owner** | Product owner: Decision required. Repository contributors per git history: Rohit Sharma, Diw696. |
| **Last updated** | 2026-09-14 |
| **Related documents** | [FEATURE_CATALOG.md](FEATURE_CATALOG.md) · [MVP_SCOPE.md](MVP_SCOPE.md) · [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) · [DATA_MODEL.md](DATA_MODEL.md) · [AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) · [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) · [UI_UX_SPEC.md](UI_UX_SPEC.md) · [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) · [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) · [ASSUMPTIONS_AND_OPEN_QUESTIONS.md](ASSUMPTIONS_AND_OPEN_QUESTIONS.md) · [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) |

## Table of contents

1. [Document metadata](#1-document-metadata)
2. [Executive summary](#2-executive-summary)
3. [Product vision](#3-product-vision)
4. [Product positioning](#4-product-positioning)
5. [Problem statement](#5-problem-statement)
6. [Current problems in competency and training management](#6-current-problems-in-competency-and-training-management)
7. [Target users and personas](#7-target-users-and-personas)
8. [User goals and pain points](#8-user-goals-and-pain-points)
9. [Product objectives](#9-product-objectives)
10. [Non-goals](#10-non-goals)
11. [Product principles](#11-product-principles)
12. [Core user journeys](#12-core-user-journeys)
13. [Product modules](#13-product-modules)
14. [Functional requirements](#14-functional-requirements)
15. [Non-functional requirements](#15-non-functional-requirements)
16. [MVP scope](#16-mvp-scope)
17. [P1 and P2 roadmap scope](#17-p1-and-p2-roadmap-scope)
18. [Success metrics](#18-success-metrics)
19. [Product analytics events](#19-product-analytics-events)
20. [Constraints](#20-constraints)
21. [Dependencies](#21-dependencies)
22. [Risks](#22-risks)
23. [Open decisions](#23-open-decisions)
24. [Acceptance criteria](#24-acceptance-criteria)
25. [Definition of done](#25-definition-of-done)
26. [Traceability matrix](#26-traceability-matrix)

---

## 2. Executive summary

The platform helps government statistical organisations do five things:
- understand the competencies each job role requires;
- estimate where individual officials stand, using assessment evidence;
- recommend relevant learning;
- generate and govern source-grounded assessments;
- measure improvement over time.

AI is an **assistive layer**. It drafts questions, answers questions from official documents with citations, and helps order learning. It never makes employment decisions. Every competency estimate is evidence-based, explainable, reviewable and correctable by humans.

**Where the project stands (2026-09-14, verified in the repository):**
- **Discovery and data collection are finished.** 19 official documents have been collected from NSSTA, MoSPI and DoPT.
- **Five validated canonical datasets exist:**
  - 99 NSSTA programmes for FY 2025-26;
  - 22 document records;
  - 25 CSCD competencies, names and structure only;
  - 16 TPAC references;
  - a 23-term topic taxonomy.
- **iGOT is interface plus mock only.** There is an iGOT client interface and a mock adapter. No public iGOT API has been documented, so no real integration exists.
- **There is no application yet:** no backend service, frontend, database, authentication or AI pipeline.

This PRD defines the product and the MVP boundary. Implementation starts only after the documentation package is approved ([IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) Phase 2).

## 3. Product vision

Every official in India's statistical system can see the competencies their role needs and receive trustworthy guidance on what to learn next, backed by official sources. Training institutions and administrators can see, in aggregate, where capability is growing and where support is needed. Neither group has to hand any judgement about a person to an opaque algorithm.

## 4. Product positioning

| Dimension | Position |
|---|---|
| **For** | Officials, trainers and administrators in India's official statistical system (e.g. MoSPI/NSO, NSSTA, State Directorates of Economics and Statistics) |
| **Who need** | Clear competency expectations, evidence of their current level, and relevant learning drawn from official statistical methodology |
| **The platform is** | A competency intelligence and personalised learning platform with an assistive, source-grounded AI layer |
| **Unlike** | Generic chatbots, which answer without sources, and employee-evaluation tools, which score people for administrative decisions |
| **It** | Grounds every AI answer and question in official documents with citations, keeps humans in control of all consequential outputs, and treats competency estimates as development guidance |
| **It is not** | An appraisal, promotion, disciplinary or selection system, and not a replacement for iGOT Karmayogi. It complements iGOT through an adapter once access is authorised ([IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md)). |

## 5. Problem statement

Officials and training institutions in the official statistical system lack a way to connect four things:
- role competency expectations;
- measured current capability;
- official learning material, which is mostly PDFs;
- the training on offer.

As a result, learning is chosen without evidence of need, assessments are hard to create and keep grounded in current methodology, and no one can show whether training improved capability.

## 6. Current problems in competency and training management

Each problem is labelled by evidence status ([STATUS_VOCABULARY.md](../STATUS_VOCABULARY.md)).

| # | Problem | Evidence status | Evidence |
|---|---|---|---|
| P-01 | Programme information is locked in PDFs and JavaScript-only pages. The NSSTA Offerings and Documents pages return an empty JavaScript shell to non-browser clients. | MACHINE_OBSERVED | [DATA_COLLECTION_RESULTS.md](DATA_COLLECTION_RESULTS.md) §3.1 |
| P-02 | Training calendars are tentative, and programme dates cannot be reliably extracted. | MACHINE_OBSERVED | FY 2025-26 calendar marks itself "(Tentative)"; week labels detached ([DATA_COLLECTION_RESULTS.md](DATA_COLLECTION_RESULTS.md) §3.3) |
| P-03 | Competency frameworks exist as documents, not usable structures, and reuse is restricted. The DoPT CSCD cannot be reproduced without permission. | MACHINE_OBSERVED | DoPT Copyright Policy ([DATA_COLLECTION_RESULTS.md](DATA_COLLECTION_RESULTS.md) §5) |
| P-04 | No machine-usable mapping of statistical job roles to required competencies was found. | MACHINE_OBSERVED (absence in collected sources) | ROLE-002 status "Requires human confirmation" |
| P-05 | Methodology changes over time, so learners can be taught superseded methods. Examples: CPI base years, a new GDP series. | MACHINE_OBSERVED | [docs/evidence/MoSPI/mospi_document_audit.md](evidence/MoSPI/mospi_document_audit.md) §5 |
| P-06 | No documented third-party integration route to iGOT course or learner data exists. | MACHINE_OBSERVED | [IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md) §1 |
| P-07 | Creating source-grounded assessment questions by hand is slow for trainers. | ASSUMED (to validate with NSSTA trainers) | — |
| P-08 | Training nominations are not systematically linked to measured competency gaps. | ASSUMED (to validate) | — |
| P-09 | Training effectiveness (before-vs-after capability) is not routinely measured. | ASSUMED (to validate) | — |

## 7. Target users and personas

The personas are **provisional archetypes** (ASSUMED), not research findings. User research with NSSTA and MoSPI stakeholders is required ([ASSUMPTIONS_AND_OPEN_QUESTIONS.md](ASSUMPTIONS_AND_OPEN_QUESTIONS.md) Q-003). Each persona maps to one access role ([SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §RBAC).

| Persona | Access role | Description | MVP? |
|---|---|---|---|
| **Learner / employee** | `learner` | Official in a statistical role (e.g. ISS officer, SSS officer, State DES officer) developing their competencies | Yes |
| **Trainer** | `trainer` | NSSTA or institutional faculty who upload material, generate and review questions, and support learners | Yes |
| **Department administrator** | `department_admin` | Manages users and views progress within a department or division | Yes |
| **Organization administrator** | `org_admin` | Manages the organisation's configuration, departments, job roles and users | Yes |
| **Competency framework administrator** | `competency_admin` | Owns competency frameworks, level scales and role-to-competency mappings | Yes |
| **Training manager** | `training_manager` | Curates the catalogue, monitors programmes and uses reports to plan training | Yes |
| **System auditor** | `auditor` | Reviews audit logs, AI interaction logs and governance records; read-only | Yes |
| **Platform administrator** | `platform_admin` | Operates the platform: configuration, prompt/model registry, integrations, jobs | Yes |

## 8. User goals and pain points

| Persona | Goals | Pain points (ASSUMED unless stated) |
|---|---|---|
| Learner | Know what the role requires; see where they stand and why; find relevant, trustworthy learning; show improvement | Unclear expectations; generic training; distrust of opaque scores; limited time; scattered PDFs (P-01, evidenced) |
| Trainer | Build good question banks quickly; keep content current with methodology; see who needs support | Manual question writing (P-07); keeping up with method changes (P-05, evidenced) |
| Department administrator | Keep users and structure accurate; see department progress | Manual tracking; no aggregated view |
| Organization administrator | Configure the platform safely; control access | Risk of data exposure; inconsistent role definitions |
| Competency framework administrator | Maintain valid frameworks and role mappings | Frameworks not machine-usable and licence-restricted (P-03, evidenced); no role mappings (P-04, evidenced) |
| Training manager | Match programmes to needs; evidence of effectiveness | No link between gaps and nominations (P-08); no effectiveness data (P-09) |
| System auditor | Verify AI and administrative actions are accountable | Lack of traceable AI outputs |
| Platform administrator | Run a reliable, secure platform; know integration state precisely | Unclear external integration status (P-06, evidenced) |

## 9. Product objectives

| ID | Objective | Measured by (§18) |
|---|---|---|
| OBJ-1 | Give each learner an explainable, evidence-based competency baseline for their role | M-01, M-02 |
| OBJ-2 | Turn gaps into relevant, explainable learning recommendations | M-05, M-06 |
| OBJ-3 | Reduce trainer effort to produce source-grounded, human-approved assessment questions | M-07, M-08 |
| OBJ-4 | Provide trustworthy, cited answers from official statistical documents | M-09, M-10 |
| OBJ-5 | Keep all consequential AI outputs under human oversight with complete audit trails | M-11, M-12 |
| OBJ-6 | Be ready to integrate iGOT through an adapter without misrepresenting mock data | M-13 |

## 10. Non-goals

- **NG-1:** Making or recommending employment decisions (appraisal, promotion, transfer, discipline, termination, selection).
- **NG-2:** Ranking individuals against each other for administrative purposes.
- **NG-3:** Replacing iGOT Karmayogi as a learning management system.
- **NG-4:** Claiming or building real iGOT integration before written authorisation and official documentation exist.
- **NG-5:** Reproducing licence-restricted content (for example CSCD definitions) without permission.
- **NG-6:** Collecting government employee data from external systems. The MVP uses only accounts created on the platform.
- **NG-7:** Producing official statistics or statistical estimates. The platform teaches methodology; it does not publish figures.
- **NG-8:** Implementing P1/P2 features during MVP ([MVP_SCOPE.md](MVP_SCOPE.md) §Forbidden).

## 11. Product principles

| Principle | Meaning in this product | Enforced by |
|---|---|---|
| **Evidence-based** | No competency estimate without evidence records; no gap without sufficient evidence | AI-016, AI-017 |
| **Human-in-the-loop** | AI-generated questions need approval; estimates are adjustable and appealable by humans | ASM-027, CMP-019, RAI-018 |
| **Privacy-preserving** | Minimum personal data; nothing sent to AI providers without authorisation; scoped access | RAI-016, SEC-002 |
| **Explainable** | Every estimate and recommendation says how it was produced | AI-018, RAI-011 |
| **Accessible** | WCAG 2.1 AA target; keyboard and screen-reader support for core journeys | ACC-009, ACC-010 |
| **Modular** | Modular monolith with provider and adapter interfaces | [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) |
| **Source-grounded** | Generated answers and questions cite verified passages of official documents, or abstain | RAI-001, MAT-019 |
| **Government-context aware** | Respects licence terms, data sensitivity, bilingual needs and low-bandwidth realities | DATA_PROVENANCE.md, ACC-003, ACC-017 |
| **No unsupported automation** | Automations never publish AI content or change consequential data without human approval | Category R rules |

## 12. Core user journeys

Journeys marked P1/P2 are specified for continuity but are **excluded from MVP**.

| # | Journey | Priority | Steps (summary) | Requirements |
|---|---|---|---|---|
| J-01 | New learner onboarding | P0 | Account provisioned by admin → first login → privacy and AI-use notice → confirm profile | PRD-FR-003 |
| J-02 | Role selection | P0 | Select department → select job role → view role's required competencies | PRD-FR-004, PRD-FR-005 |
| J-03 | Initial competency assessment | P0 | Start pre-assessment → answer approved MCQs → submit → result | PRD-FR-006 |
| J-04 | Competency-gap analysis | P0 | View estimates with evidence bands → view gaps → open explanation → request correction if needed | PRD-FR-007, PRD-FR-008, PRD-AI-005 |
| J-05 | Personalized learning plan | P0 | View ordered learning path → see why each item was selected → mark progress | PRD-FR-018 |
| J-06 | Learning-material upload | P0 | Trainer uploads PDF/DOCX/TXT with licence attestation → processing status → ready / needs OCR / failed | PRD-FR-009, PRD-FR-010 |
| J-07 | RAG document question answering | P0 | Ask question → retrieval within access scope → cited answer or abstention | PRD-FR-011 to 013 |
| J-08 | Quiz generation | P0 | Trainer selects sources, topic, competency, count → generation job → validated candidates | PRD-FR-014, PRD-FR-015 |
| J-09 | Human question review | P0 | Review queue → inspect validator flags and source passage → approve / edit / reject with reason | PRD-FR-016 |
| J-10 | Course recommendation | P0 | Dashboard shows recommendations with reasons and provenance (mock iGOT items labelled) | PRD-FR-017 |
| J-11 | Learning completion | P0 | Learner marks item complete (self-reported label) or system records completion | PRD-FR-024 |
| J-12 | Reassessment | P1 | Reassessment suggested → post-assessment | PRD-FR-101 |
| J-13 | Before-vs-after comparison | P1 | Compare baseline and post estimates with caveats | PRD-FR-102 |
| J-14 | Trainer monitoring | P0 (basic) | Trainer dashboard: review queue, scoped learner status | PRD-FR-020 |
| J-15 | Department-level analysis | P1 | Heatmap and aggregates with suppression | PRD-FR-103 |
| J-16 | Administrator governance | P0 | Manage users, roles, frameworks, approval policy, settings; view integration mode | PRD-FR-002, 005, 020, 021 |
| J-17 | Audit investigation | P0 | Auditor filters audit and AI interaction logs by actor/target/time; follows correlation IDs | PRD-FR-022, PRD-SEC-004 |

Screen-level detail for each journey is in [UI_UX_SPEC.md](UI_UX_SPEC.md).

## 13. Product modules

| Module | Scope | Catalog categories | MVP |
|---|---|---|---|
| Identity & access | Authentication, sessions, RBAC, user profile | P (SEC), S (UX-021) | Yes |
| Organisation administration | Departments, job roles, users, settings | I (ADM) | Yes |
| Competency framework | Frameworks, levels, role-competency mapping | D, E, I | Yes |
| Assessment engine | Question bank, assessments, attempts, scoring | C, A | Yes |
| Competency intelligence | Estimates, evidence, gaps, explanations, adjustments | A, D | Yes |
| Learning content | Materials, documents, processing, search, Q&A, citations | B | Yes |
| AI generation & validation | MCQ generation, validators, review workflow | A, C, Q | Yes |
| Recommendations & paths | Recommendations, learning paths | A, F | Yes |
| Progress & reporting | Progress records, basic reports, CSV | N, O | Yes |
| Integrations | iGOT adapter (mock), health, provenance | H | Yes (mock) |
| Governance & audit | Audit logs, AI logs, prompt registry, correction requests | P, Q | Yes |
| Tutor | Conversational tutor | G | No (P1) |
| Analytics | Heatmaps, aggregates, effectiveness | J | No (P1/P2) |
| Engagement | Gamification, notifications | M, R | No (P1/P2) |
| Future intelligence | Forecasting, IRT/BKT, passport | T | No (P2) |

## 14. Functional requirements

Each P0 requirement maps to one MVP capability in [MVP_SCOPE.md](MVP_SCOPE.md) and to features in [FEATURE_CATALOG.md](FEATURE_CATALOG.md). The complete mapping is in §26.

### 14.1 P0 functional requirements (MVP)

| ID | Requirement | MVP capability | Features |
|---|---|---|---|
| PRD-FR-001 | Users authenticate with secure credentials and server-side sessions; administrators re-authenticate for sensitive actions. | MVP-01 | SEC-001, SEC-003, SEC-005, SEC-013, SEC-014 |
| PRD-FR-002 | All data access is authorised server-side by access role and organisation/department scope; user accounts are managed by administrators. | MVP-02 | SEC-002, SEC-012, ADM-001 |
| PRD-FR-003 | Users complete onboarding and maintain a profile (designation, department, job role, language preference). | MVP-03 | UX-021, UX-015 |
| PRD-FR-004 | Learners select a department and job role; administrators maintain departments and job roles. | MVP-04 | ROLE-001, ADM-002, ADM-003 |
| PRD-FR-005 | Competency framework administrators maintain frameworks, level scales and approved role-to-competency mappings, including structure-only imports of restricted frameworks. | MVP-05 | ADM-004, ROLE-002, ROLE-004 |
| PRD-FR-006 | Learners take a role-based initial assessment composed only of approved MCQ versions, with randomisation, feedback, explanations and source evidence. | MVP-06 | AI-001, ASM-001, ASM-006 to ASM-011, ASM-014, ASM-017, ASM-019 to ASM-021, ASM-031, ASM-032, CMP-017, ROLE-007, ADM-006, ADM-007, AI-009, AUT-004, TRN-008 |
| PRD-FR-007 | The system calculates reproducible competency scores and levels with evidence records, evidence-sufficiency bands and explanations. | MVP-07 | AI-012, AI-016, AI-017, AI-018, CMP-002, CMP-016, AUT-002 |
| PRD-FR-008 | The system detects gaps between required and estimated levels, shows strengths and developing areas, and supports human-reviewed adjustments. | MVP-08 | AI-002, CMP-001, CMP-004, CMP-006, CMP-007, CMP-008, CMP-019 |
| PRD-FR-009 | Trainers upload PDF, DOCX and TXT materials with metadata, licence attestation and access scope; exact duplicates are detected. | MVP-09 | MAT-001, MAT-002, MAT-004, MAT-028, MAT-031, ADM-008, TRN-002 |
| PRD-FR-010 | Uploaded documents are extracted, cleaned, normalised, chunked, enriched, embedded and stored with visible processing status and recovery. | MVP-10 | MAT-007 to MAT-013, MAT-029, MAT-030 |
| PRD-FR-011 | Users search accessible documents in semantic and keyword modes with filters. | MVP-11 | MAT-014, MAT-015, UX-019 |
| PRD-FR-012 | Users ask questions and receive grounded answers with confidence bands, or an explicit abstention. | MVP-12 | MAT-017, MAT-018, RAI-001, RAI-003, RAI-015 |
| PRD-FR-013 | Every grounded output carries verified citations, with page numbers where page boundaries are known. | MVP-13 | MAT-019, MAT-020, RAI-002 |
| PRD-FR-014 | Trainers generate candidate MCQs from licence-permitted sources as background jobs. | MVP-14 | AI-007, AUT-003, TRN-003 |
| PRD-FR-015 | Generated questions are automatically validated for schema, grounding, duplicates and answer-key correctness before review. | MVP-15 | ASM-022, ASM-023, ASM-024, RAI-004, RAI-005 |
| PRD-FR-016 | Reviewers approve, edit (versioned) or reject questions with reasons under a configurable approval policy; humans can override AI results. | MVP-16 | ASM-027 to ASM-030, ADM-009, ADM-010, RAI-006, RAI-017, TRN-004 to TRN-007 |
| PRD-FR-017 | Learners receive explainable recommendations from approved catalogue mappings; mock iGOT items are labelled MOCK and feature-flagged. | MVP-17 | AI-005, AI-006, PER-002, PER-009, PER-010, ADM-005, AUT-001, RAI-011, IGOT-002 |
| PRD-FR-018 | Learners receive an ordered learning path addressing their gaps, with reasons per item. | MVP-18 | AI-004, PER-003 |
| PRD-FR-019 | Learners have a personalised dashboard with continue-learning and role-specific home routing. | MVP-19 | PER-001, UX-003, UX-009 |
| PRD-FR-020 | Trainers and administrators have a review-focused dashboard with scoped learner monitoring and configuration. | MVP-20 | TRN-001, ADM-012, ADM-014 |
| PRD-FR-021 | iGOT access goes through a client interface with a mock adapter, explicit health/mode states, failure states and provenance; no real calls. | MVP-21 | IGOT-010, IGOT-011, IGOT-013, IGOT-017, IGOT-018 |
| PRD-FR-022 | Security, administrative, review, data-access and AI events are audit-logged and searchable by authorised roles. | MVP-22 | SEC-009, SEC-010, SEC-011, ADM-017, RAI-008 |
| PRD-FR-023 | Responsible-AI controls apply to all AI features: injection defence, safety filters, evaluation gate, output versioning, data minimisation, correction workflow, prompt/model registry. | MVP-23 | RAI-007, RAI-009, RAI-012, RAI-014, RAI-016, RAI-018, RAI-019 |
| PRD-FR-024 | Learners and scoped staff see course, quiz and competency progress, history, completed, pending and recommended items and an assessment timeline. | MVP-24 | PRO-001, PRO-002, PRO-003, PRO-005, PRO-006, PRO-010 to PRO-013 |
| PRD-FR-025 | Authorised users generate learner development, gap, assessment and progress reports with CSV export, access control and audit. | MVP-25 | REP-001, REP-003, REP-004, REP-007, REP-012, REP-014, REP-015 |
| PRD-FR-026 | The platform provides a security baseline: TLS, encryption at rest, secure APIs, input/output validation, secret management, threat model. | MVP-F1 | SEC-006, SEC-007, SEC-008, SEC-015, SEC-016, SEC-017, SEC-021 |
| PRD-FR-027 | Long-running work runs as idempotent background jobs with retries, dead-letter state and monitoring. | MVP-F2 | AUT-012, AUT-013, AUT-014, AUT-015 |
| PRD-FR-028 | The UI is responsive and mobile-friendly, with defined empty, loading and error states. | MVP-F3 | UX-001, UX-002, UX-012, UX-013, UX-014 |
| PRD-FR-029 | The UI is English, i18n-ready and accessible (screen reader, keyboard, forms, charts, reduced motion). | MVP-F4 | ACC-001, ACC-003, ACC-009, ACC-010, ACC-014, ACC-015, ACC-016, UX-011 |

### 14.2 P1 functional requirements (post-MVP)

| ID | Requirement | Features |
|---|---|---|
| PRD-FR-101 | Reassessment and post-assessment | ASM-012, AI-015, AUT-006 |
| PRD-FR-102 | Before-vs-after tracking, progression, learning hours and evidence timeline | PRO-004, PRO-007, PRO-008, PRO-014, CMP-010, CMP-013, REP-008 |
| PRD-FR-103 | Department heatmaps and aggregate analytics | CMP-003, ANA-001 to ANA-008, ANA-013, ANA-015, ANA-016, ADM-013, REP-002 |
| PRD-FR-104 | AI tutor | TUT-001 to TUT-004, TUT-006, TUT-008, TUT-009, TUT-011 to TUT-013, TUT-015 to TUT-020 |
| PRD-FR-105 | Adaptive assessment and additional question types with rubric evaluation | AI-008, AI-010, AI-011, ASM-002 to ASM-005, ASM-015, ASM-016, ASM-018, ASM-025, ASM-026 |
| PRD-FR-106 | Competency graph, topic tracking, learning evidence | CMP-005, CMP-012, CMP-014, CMP-018, AI-014 |
| PRD-FR-107 | Hindi and multilingual expansion; further accessibility options | ACC-002, ACC-004, ACC-005, ACC-011, ACC-012, ACC-017 |
| PRD-FR-108 | Advanced personalisation and planning | AI-003, PER-005 to PER-008, PER-011 to PER-014, PER-016, ROLE-003, ROLE-005, ROLE-006, ROLE-008, ROLE-012, ROLE-013 |
| PRD-FR-109 | Gamification (opt-in) | GAM-001 to GAM-004, GAM-006, GAM-007, GAM-011, GAM-012, PRO-009 |
| PRD-FR-110 | Advanced reports and exports | REP-005, REP-006, REP-009, REP-010, REP-011, TRN-012, TRN-013 |
| PRD-FR-111 | Notification and path automation | AUT-005, AUT-007 to AUT-010, UX-005 |
| PRD-FR-112 | iGOT synchronisation when access is authorised | IGOT-001, IGOT-003 to IGOT-005, IGOT-009, IGOT-012, IGOT-014 to IGOT-016, AUT-011 |
| PRD-FR-113 | Additional content intelligence (OCR, PPTX, images, hybrid search, summaries, tagging, versioning) | MAT-003, MAT-005, MAT-006, MAT-016, MAT-021 to MAT-023, MAT-026, MAT-027 |
| PRD-FR-114 | Administration extensions (assignments, taxonomy, permissions, retention) and security extensions | ADM-011, ADM-015, ADM-016, ADM-018, TRN-009 to TRN-011, TRN-014, SEC-004, SEC-018 to SEC-020, RAI-010, RAI-013 |
| PRD-FR-115 | UX extensions | UX-004, UX-007, UX-008, UX-016 to UX-018, TUT-020 |

### 14.3 P2 functional requirements (future)

| ID | Requirement | Features |
|---|---|---|
| PRD-FR-201 | Predictive and workforce intelligence | AI-013, ANA-009 to ANA-012, ANA-014, FUT-001, FUT-002, FUT-013 to FUT-015, FUT-018, TRN-015 |
| PRD-FR-202 | Knowledge tracing, IRT/BKT, competency passport and certification | FUT-004 to FUT-008, CMP-009, CMP-011, CMP-015, ASM-013 |
| PRD-FR-203 | Career intelligence | FUT-003, ROLE-009 to ROLE-011, PER-004, PER-015, PER-017, PER-018 |
| PRD-FR-204 | Offline, low-bandwidth, mobile and voice | FUT-009 to FUT-012, ACC-006 to ACC-008, ACC-013 |
| PRD-FR-205 | Simulation and AI trainer design | FUT-016, FUT-017, MAT-024, MAT-025 |
| PRD-FR-206 | Advanced engagement and experience | GAM-005, GAM-008 to GAM-010, TUT-005, TUT-007, TUT-010, TUT-014, UX-006, UX-010, UX-020, REP-013, IGOT-006 to IGOT-008 |

## 15. Non-functional requirements

These are **design targets**, not measured results. Numeric thresholds marked "Decision required" must be agreed before Phase 12 hardening.

| ID | Category | Requirement |
|---|---|---|
| PRD-NFR-001 | Performance | Interactive, non-AI API reads target p95 < 500 ms under pilot load (pilot load profile: Decision required). |
| PRD-NFR-002 | Performance | AI endpoints stream or return job handles. The UI shows progress within 1 s of a request. End-to-end AI latency targets are set after baseline measurement (Decision required). |
| PRD-NFR-003 | Scalability | The modular monolith scales horizontally behind a load balancer. Workers scale independently ([SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) §Scaling). |
| PRD-NFR-004 | Availability | Pilot availability target: Decision required. Maintenance windows are announced. |
| PRD-NFR-005 | Reliability | Background jobs are idempotent with bounded retries. No uploaded file is lost to a transient failure. |
| PRD-NFR-006 | Data integrity | Evidence, audit logs and approved question versions are append-only or immutable. Schema changes go through migrations only. |
| PRD-NFR-007 | Maintainability | Modular boundaries enforced ([SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md)). Typed code. Tests required for new behaviour ([TESTING_STRATEGY.md](TESTING_STRATEGY.md)). |
| PRD-NFR-008 | Portability | Runs locally via containers. Cloud-agnostic, with no hard dependency on a single cloud vendor's proprietary services in MVP. |
| PRD-NFR-009 | Observability | Structured logs, metrics and traces with correlation IDs ([OBSERVABILITY_SPEC.md](OBSERVABILITY_SPEC.md)). |
| PRD-NFR-010 | Localisation | UTF-8 end to end. All UI strings externalised. English in MVP; Hindi in P1. |
| PRD-NFR-011 | Accessibility | WCAG 2.1 AA target for all P0 screens. GIGW applicability to be confirmed (DEC-026). |
| PRD-NFR-012 | Low bandwidth | Core learner pages remain usable on constrained connections (profile defined in [TESTING_STRATEGY.md](TESTING_STRATEGY.md)). |
| PRD-NFR-013 | Cost control | Per-request token limits, per-user AI rate limits and budget alerts for AI usage ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §6). |
| PRD-NFR-014 | Browser support | Current versions of Chrome, Edge and Firefox, plus the most recent Safari. Exact support matrix: Decision required. |

### 15.1 Security requirements

| ID | Requirement |
|---|---|
| PRD-SEC-001 | Authentication, authorisation and all permission checks are enforced server-side. The frontend is never trusted. |
| PRD-SEC-002 | Organisation isolation is enforced on every tenant-scoped query. |
| PRD-SEC-003 | Uploaded files are validated (type, signature, size) and never executed; a malware-scanning hook exists (placeholder in MVP). |
| PRD-SEC-004 | Critical events are audit-logged with actor, action, target, time and correlation ID. Audit logs are immutable to application users. |
| PRD-SEC-005 | Secrets live only in the environment or a secret store. None appear in code, logs, API responses or client bundles. |
| PRD-SEC-006 | Personal data is minimised, access-scoped, retained per an approved policy (Decision required) and deletable per policy (P1). |
| PRD-SEC-007 | Rate limiting applies to authentication and AI endpoints. |
| PRD-SEC-008 | No outbound requests to user-supplied URLs (SSRF prevention). The document collector uses allow-listed hosts only. |
| PRD-SEC-009 | A threat model is maintained and reviewed at each phase exit ([SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md)). |

### 15.2 AI requirements

| ID | Requirement |
|---|---|
| PRD-AI-001 | All LLM and embedding access goes through provider interfaces. The provider is configurable, and no provider-specific code sits outside adapters. |
| PRD-AI-002 | Grounded outputs use only retrieved, accessible, licence-permitted sources and carry verified citations, or the system abstains. |
| PRD-AI-003 | Every AI artefact stores source references, evidence, model metadata, prompt version, timestamp, confidence, validation status and human-review status. |
| PRD-AI-004 | No AI-generated question is used before human approval. |
| PRD-AI-005 | Competency estimates are deterministic in MVP. An LLM never assigns a competency score. |
| PRD-AI-006 | AI outputs never make or recommend employment decisions. |
| PRD-AI-007 | Personal data is not sent to an AI provider without authorisation. Payloads are redacted. |
| PRD-AI-008 | Prompt-injection defences and an injection test suite are required before any AI feature is released. |
| PRD-AI-009 | No AI quality or accuracy claim is published without recorded evaluation results against approved golden datasets. |
| PRD-AI-010 | A provider failure degrades gracefully to an explicit error or abstention and never corrupts data. |

### 15.3 UX requirements

| ID | Requirement |
|---|---|
| PRD-UX-001 | The interface is a professional SaaS application suited to government training contexts, not a chatbot-first design. |
| PRD-UX-002 | AI-generated content is visually and textually distinguished, with citation, confidence and review-status indicators. |
| PRD-UX-003 | MOCK data is always labelled "MOCK - not real iGOT data" wherever displayed. |
| PRD-UX-004 | Competency results use development-oriented language and always show evidence, limitations and a correction route. |
| PRD-UX-005 | Every screen defines empty, loading and error states. |
| PRD-UX-006 | Every chart has a table alternative. |
| PRD-UX-007 | Permission-restricted actions are hidden or disabled with an explanation, and still enforced server-side. |

## 16. MVP scope

The MVP is the 25 capabilities MVP-01 to MVP-25 plus four foundation capabilities MVP-F1 to MVP-F4. Together they cover all 173 P0 catalogue entries (154 canonical and 19 aliases). The strict boundary, per-capability details and the list of **features that must not be implemented during MVP** are in [MVP_SCOPE.md](MVP_SCOPE.md).

**MVP operating assumptions** (confirm before Phase 4):
- Single organisation, with the multi-organisation schema in place.
- Accounts are provisioned by administrators; there is no self-registration.
- Competency frameworks and role mappings must be authored and approved on the platform. None exist in the collected data except the CSCD structure (names only).
- AI calls in development and pilot use only public source documents, with no real employee data, until the provider data policy is decided (DEC-005).

## 17. P1 and P2 roadmap scope

- **P1** (post-MVP, PRD-FR-101 to 115): adaptive assessments, AI tutor, competency graph, before-vs-after tracking, department heatmaps, trainer analytics, Hindi and multilingual expansion, advanced personalisation, gamification, advanced reports, notification automation, and iGOT synchronisation once access is available.
- **P2** (future, PRD-FR-201 to 206): predictive workforce intelligence, skill-demand forecasting, career-path intelligence, knowledge tracing, IRT/BKT, AI certification, offline mode, voice interface, mobile application, cross-department optimisation, advanced simulation, AI trainer designer.

Sequencing is in [IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md) Phases 13–14.

## 18. Success metrics

No metric has been measured. Targets marked **Baseline first** are set after pilot measurement. Targets marked **Invariant** are design guarantees verified by tests and audits, not performance claims.

| ID | Metric | Definition | Target |
|---|---|---|---|
| M-01 | Baseline completion | Share of onboarded pilot learners who complete a pre-assessment | Baseline first |
| M-02 | Evidence sufficiency | Share of role competencies with evidence band ≥ medium after the pre-assessment | Baseline first |
| M-03 | Correction request rate | Correction requests per 100 estimates, and share upheld | Baseline first; monitored for signs of estimation problems |
| M-04 | Explanation views | Share of learners opening "How was this calculated?" | Baseline first |
| M-05 | Recommendation engagement | Accepted or started ÷ shown; dismissals by reason | Baseline first |
| M-06 | Path progress | Share of path items started or completed within 30 days | Baseline first |
| M-07 | Question approval yield | Approved ÷ generated candidates reaching review | Baseline first |
| M-08 | Reviewer effort | Median review time per question | Baseline first |
| M-09 | Citation integrity | Displayed grounded answers with ≥1 verified citation ÷ displayed grounded answers | **Invariant: 100%** |
| M-10 | Grounded answer quality | Golden-set correctness and abstention precision/recall per prompt version | Baseline first (evaluation gate, RAI-012) |
| M-11 | Review coverage | AI-generated questions used in assessments with an approval record ÷ all used | **Invariant: 100%** |
| M-12 | AI traceability | AI outputs shown with an AIInteractionLog record ÷ all AI outputs shown | **Invariant: 100%** |
| M-13 | Mock labelling | Mock-sourced records displayed with the MOCK label ÷ mock records displayed | **Invariant: 100%** |
| M-14 | Accessibility conformance | Automated accessibility violations on P0 screens (serious/critical) | **Invariant: 0 at release** |

## 19. Product analytics events

Events carry pseudonymous user IDs, organisation ID and role. They carry **no names, emails, free-text questions or answer content**. Event data is subject to the retention policy.

| Event | Trigger | Properties |
|---|---|---|
| `onboarding_completed` | Onboarding finished | job_role_id, department_id |
| `job_role_selected` | Role selected or changed | job_role_id, previous_job_role_id |
| `assessment_started` | Attempt created | assessment_id, purpose |
| `assessment_submitted` | Attempt submitted | assessment_id, question_count, duration_s |
| `competency_explanation_viewed` | Explanation panel opened | competency_id, evidence_band |
| `correction_request_submitted` | Correction requested | target_type |
| `gap_viewed` | Gap analysis opened | gap_count |
| `recommendation_shown` | Recommendation rendered | recommendation_id, source, is_mock |
| `recommendation_actioned` | Accept / start / dismiss | recommendation_id, action, reason |
| `learning_path_item_status_changed` | Status change | item_id, from, to, source |
| `document_uploaded` | Upload accepted | material_id, file_type, size_bucket |
| `document_processing_finished` | Job finished | document_id, status, duration_s |
| `search_performed` | Search executed | mode, result_count |
| `qa_answered` | Q&A response returned | abstained, citation_count, confidence_band |
| `question_generation_job_finished` | Job finished | requested, generated, passed_validation |
| `review_decision_made` | Approve / reject / edit | decision, reason_category, validator_flag_count |
| `report_generated` | Report created | report_type, format |
| `integration_mode_viewed` | Integration health opened | adapter, mode |

## 20. Constraints

| # | Constraint | Source |
|---|---|---|
| C-01 | No documented public/partner iGOT API. Real integration is blocked. | [IGOT_ACCESS_STATUS.md](../IGOT_ACCESS_STATUS.md) |
| C-02 | CSCD definitions and behavioural indicators may not be reproduced without DoPT permission. | DoPT Copyright Policy ([DATA_COLLECTION_RESULTS.md](DATA_COLLECTION_RESULTS.md) §5) |
| C-03 | MoSPI/NSSTA reuse terms are unverified (secondhand "reproduction with acknowledgement"). Content is not learner-visible until confirmed. | [DATA_PROVENANCE.md](DATA_PROVENANCE.md) |
| C-04 | Nothing in collected data is VERIFIED. Human review is required before release. | [DATASET_VALIDATION_REPORT.md](DATASET_VALIDATION_REPORT.md) |
| C-05 | Personal data processing requires a lawful basis (e.g. DPDP Act, 2023). Legal review required. | [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) |
| C-06 | The AI provider must be approved for government data (retention, region, terms). Undecided. | DEC-005 |
| C-07 | PostgreSQL is the application database; AI providers stay behind interfaces. | Product brief; [AGENT_CONTEXT.md](AGENT_CONTEXT.md) |
| C-08 | Two collected documents are scanned. OCR is P1. | [DATA_COLLECTION_RESULTS.md](DATA_COLLECTION_RESULTS.md) |
| C-09 | SIH (Smart India Hackathon) timeline and demo expectations: dates undecided. | Decision required |

## 21. Dependencies

| # | Dependency | Type | Needed for | Status |
|---|---|---|---|---|
| D-01 | Approved functional competency framework for statistical roles | Human/SME | MVP-05 to MVP-08 | Requires human confirmation |
| D-02 | Approved role-to-competency mappings and level thresholds | Human/SME | MVP-05, MVP-07 | Requires human confirmation |
| D-03 | LLM provider decision and data-processing approval | Decision/legal | MVP-12, MVP-14, MVP-15 | Decision required |
| D-04 | Embedding provider decision | Decision | MVP-10, MVP-11 | Decision required |
| D-05 | Confirmation of MoSPI/NSSTA content reuse terms | Human/legal | Learner-visible content | Not yet verified |
| D-06 | DoPT permission for CSCD definitions (optional) | External | Displaying definitions | Not requested |
| D-07 | Golden evaluation datasets approved by SMEs | Human/SME | MVP-23 release gate | Not started |
| D-08 | Hosting and deployment environment | Decision | Phase 12 | Decision required |
| D-09 | Karmayogi Bharat authorisation and documentation | External | IGOT-012 (P1) | Blocked |
| D-10 | Merge of Phase 1 work into `main` (branch `Diw`) | Team | All phases | Decision required (DEC-019) |

## 22. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R-01 | Competency estimates misused for employment decisions | Medium | Critical | Non-goals, UI notices, report titling, no individual rankings, governance review (§HID in SECURITY_RESPONSIBLE_AI.md) |
| R-02 | Hallucinated or wrong answer keys reach learners | Medium | High | Grounding, span verification, independent validation, mandatory human approval |
| R-03 | Mock iGOT data mistaken for real | Medium | High | MOCK labels, feature flag, health mode 'mock', no 'connected' state for mocks |
| R-04 | No SME-approved competency framework in time | High | High | Early Phase 4 dependency; demo mode clearly labelled draft if necessary |
| R-05 | AI provider not approvable for government data | Medium | High | Provider interface; option for self-hosted models; public-document-only AI use until approved |
| R-06 | Licence terms prohibit re-serving collected content | Medium | High | Learner visibility gate on licence; link-out fallback |
| R-07 | Prompt injection via uploaded documents | Medium | Medium | Untrusted-content handling, no side-effecting tools, injection test suite |
| R-08 | Scope creep into P1/P2 during MVP | High | Medium | MVP_SCOPE forbidden list; AGENT_CONTEXT rules; roadmap exit criteria |
| R-09 | Superseded methodology taught as current | Medium | High | series_base_year field and release blocker (LP-20) |
| R-10 | Personal data exposure through reports or analytics | Low | Critical | Scoped access, suppression, audit, export controls |
| R-11 | Accessibility gaps exclude users | Medium | Medium | WCAG 2.1 AA target, automated and manual tests |

## 23. Open decisions

The full register is in [DECISIONS.md](DECISIONS.md) and [ASSUMPTIONS_AND_OPEN_QUESTIONS.md](ASSUMPTIONS_AND_OPEN_QUESTIONS.md). Blocking decisions:

| ID | Decision | Blocks |
|---|---|---|
| DEC-001 | Product name (avoid implying official Karmayogi Bharat endorsement) | Branding, UI copy |
| DEC-005 | LLM provider and data-processing terms | Phases 5–6 |
| DEC-006 | Embedding provider and model | Phase 5 |
| DEC-013 | Source of the functional competency framework and role mappings | Phase 4 |
| DEC-019 | Branch strategy and merge of Phase 1 | Phase 2 |
| DEC-020 | Scoring weights, level thresholds and evidence-band thresholds | Phase 4 |
| DEC-027 | Data retention periods and lawful basis | Phase 11–12 |

## 24. Acceptance criteria

The MVP is accepted when **all** of the following hold:

1. Every P0 capability MVP-01 to MVP-25 and MVP-F1 to MVP-F4 meets its acceptance criteria in [MVP_SCOPE.md](MVP_SCOPE.md).
2. Journeys J-01 to J-11, J-14, J-16 and J-17 can be completed end to end in a pilot environment by users in the corresponding roles, with keyboard-only operation verified for J-01 to J-07.
3. Invariant metrics M-09, M-11, M-12, M-13 and M-14 hold in automated tests and an audit sample.
4. Authorisation tests pass for every endpoint × access role in the permission matrix.
5. The AI evaluation gate (RAI-012) has recorded results for every prompt version in use, and the injection test suite passes.
6. No P1/P2 feature is implemented or reachable in the MVP build.
7. The threat model has been reviewed, and no open critical or high security findings remain.
8. All documentation affected by implementation has been updated ([AGENT_CONTEXT.md](AGENT_CONTEXT.md) documentation rules).

## 25. Definition of done

A requirement or feature is **done** only when:

- its code is merged via review to the agreed main branch;
- automated tests covering its acceptance criteria pass in CI, including authorisation tests for new endpoints;
- schema changes are delivered as migrations;
- API changes are reflected in the OpenAPI specification and [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md);
- AI changes are registered as prompt/model versions with evaluation results;
- audit events, logs and metrics defined for it are emitted;
- empty, loading, error and permission states are implemented and accessibility checks pass;
- its implementation status is updated in the feature registry ([FEATURE_CATALOG.md](FEATURE_CATALOG.md) regenerated) with evidence;
- no secret, personal data or mock data appears where prohibited.

## 26. Traceability matrix

| PRD requirement | MVP capability | Roadmap phase ([IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)) | Primary API group ([API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md)) | Primary screens ([UI_UX_SPEC.md](UI_UX_SPEC.md)) |
|---|---|---|---|---|
| PRD-FR-001 | MVP-01 | Phase 3 | Auth | Login |
| PRD-FR-002 | MVP-02 | Phase 3 | Users, Auth | Admin dashboard |
| PRD-FR-003 | MVP-03 | Phase 3 (API), Phase 8 (UI) | Me | Onboarding, Settings |
| PRD-FR-004 | MVP-04 | Phase 4 | Organisation, Job roles | Onboarding, Admin dashboard |
| PRD-FR-005 | MVP-05 | Phase 4 | Competencies, Job roles | Admin dashboard |
| PRD-FR-006 | MVP-06 | Phase 4 | Assessments, Attempts, Questions | Assessment screen, Assessment results |
| PRD-FR-007 | MVP-07 | Phase 4 | Competency profile | Competency profile |
| PRD-FR-008 | MVP-08 | Phase 4 | Competency profile, Corrections | Competency-gap analysis |
| PRD-FR-009 | MVP-09 | Phase 5 | Learning materials | Document library |
| PRD-FR-010 | MVP-10 | Phase 5 | Documents, Jobs | Document library, Document viewer |
| PRD-FR-011 | MVP-11 | Phase 5 | Search | Document library |
| PRD-FR-012 | MVP-12 | Phase 5 | Document Q&A | Document Q&A |
| PRD-FR-013 | MVP-13 | Phase 5 | Document Q&A, Questions | Document viewer, Document Q&A |
| PRD-FR-014 | MVP-14 | Phase 6 | Question generation | Quiz builder |
| PRD-FR-015 | MVP-15 | Phase 6 | Questions | Quiz review |
| PRD-FR-016 | MVP-16 | Phase 6 (API), Phase 9 (UI) | Review tasks | Quiz review |
| PRD-FR-017 | MVP-17 | Phase 7 | Recommendations, Courses | Learner dashboard, Course discovery |
| PRD-FR-018 | MVP-18 | Phase 7 | Learning paths | Learning path |
| PRD-FR-019 | MVP-19 | Phase 8 | Me (dashboard) | Learner dashboard |
| PRD-FR-020 | MVP-20 | Phase 9 | Trainer, Admin settings | Trainer dashboard, Admin dashboard, Settings |
| PRD-FR-021 | MVP-21 | Phase 10 | Integrations | Integration health, Course discovery |
| PRD-FR-022 | MVP-22 | Phase 2 (logging), Phase 11 (completeness, UI) | Audit | Audit logs |
| PRD-FR-023 | MVP-23 | Phases 5–6 (controls), Phase 11 (governance) | Admin prompt registry, Corrections | Audit logs, Competency profile |
| PRD-FR-024 | MVP-24 | Phase 8 | Progress | Learner dashboard, Progress analytics |
| PRD-FR-025 | MVP-25 | Phase 9 | Reports | Reports |
| PRD-FR-026 | MVP-F1 | Phase 2, Phase 12 | All | All |
| PRD-FR-027 | MVP-F2 | Phase 2 | Jobs | Document library, Quiz builder |
| PRD-FR-028 | MVP-F3 | Phase 8 | — | All |
| PRD-FR-029 | MVP-F4 | Phase 8, Phase 12 | — | All |
