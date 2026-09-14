# UI/UX Specification

| Field | Value |
|---|---|
| **Version** | 1.0.0-draft |
| **Status** | Proposed - no UI exists; no visual designs produced yet |
| **Last updated** | 2026-09-14 |
| **Related** | [PRD.md](PRD.md) §12, §15.3 · [MVP_SCOPE.md](MVP_SCOPE.md) · [API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) · [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §4, §15 · [ERROR_HANDLING_SPEC.md](ERROR_HANDLING_SPEC.md) · [AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) · [TECH_STACK.md](TECH_STACK.md) §3 |

## Table of contents

1. [Design principles](#1-design-principles)
2. [Visual hierarchy](#2-visual-hierarchy)
3. [Information architecture and navigation](#3-information-architecture-and-navigation)
4. [Responsive behavior and layouts](#4-responsive-behavior-and-layouts)
5. [Color and typography system](#5-color-and-typography-system)
6. [Accessibility rules](#6-accessibility-rules)
7. [Component system](#7-component-system)
8. [Patterns](#8-patterns)
9. [AI interaction patterns](#9-ai-interaction-patterns)
10. [Content and wording guidelines](#10-content-and-wording-guidelines)
11. [Screen specifications](#11-screen-specifications)
12. [Screen-to-role summary](#12-screen-to-role-summary)

---

## 1. Design principles

| Principle | Application |
|---|---|
| **Serious and calm** | A professional work tool for government statistical staff: restrained colour, clear typography, no playful chatbot aesthetics, no gratuitous animation |
| **Evidence first** | Every AI output and estimate shows its source, evidence or reason next to the result, not hidden in a modal |
| **Honest states** | Unknown, unreviewed, mock, provisional and abstained states are shown explicitly in words |
| **Human control visible** | Review, override, correction and dismissal actions are always discoverable where AI output appears |
| **Development, not judgement** | Competency language supports growth (§10) |
| **Accessible by default** | WCAG 2.1 AA target; keyboard-first; screen-reader tested journeys |
| **Low-bandwidth friendly** | Text-first layouts, skeletons instead of heavy imagery, paginated lists |
| **Not an official government identity** | The platform must not imitate official Government of India, Karmayogi Bharat, MoSPI or NSSTA branding (no national emblem or official logos without authorisation). Source organisations are named as attribution only. |

## 2. Visual hierarchy

1. **Page title and purpose line** state what the page is for.
2. **Primary status or next action**, e.g. "Baseline assessment pending - Start assessment".
3. **Key content** in cards or tables.
4. **Supporting detail**: explanations, evidence and provenance, expandable inline.
5. **Secondary actions** in overflow menus.

- Each view has exactly one primary button.
- Destructive actions use a secondary style plus confirmation.

## 3. Information architecture and navigation

### 3.1 Primary navigation (role-aware)

| Section | Route | Visible to | MVP |
|---|---|---|---|
| Home | `/` (routes to role home) | all | Yes |
| My competencies | `/competencies`, `/competencies/gaps` | learner | Yes |
| Assessments | `/assessments`, `/assessments/:id/attempt`, `/attempts/:id/result` | learner | Yes |
| Learning path | `/learning-path` | learner | Yes |
| Courses | `/courses` | all | Yes |
| Library | `/library`, `/library/:materialId` | all | Yes |
| Ask the documents | `/ask` | all except auditor (feature-flagged) | Yes |
| Progress | `/progress` | learner; trainer/managers (scoped) | Yes (basic) |
| Trainer workspace | `/trainer`, `/trainer/quizzes/new`, `/review` | trainer, competency_admin | Yes |
| Reports | `/reports` | learner (self), staff (scoped) | Yes |
| Administration | `/admin`, `/admin/audit`, `/admin/integrations`, `/admin/departments/heatmap` (P1) | admin roles, auditor | Yes (heatmap P1) |
| Tutor | `/tutor` | learner | **P1** |
| Settings | `/settings` | all | Yes |

- **Role-gated navigation:** Items are hidden when the user lacks permission. Direct URL access still returns the server's 403 state (never trusted client-side).
- **Multiple roles:** Users with more than one role get a role switcher in the header that changes the home view and navigation emphasis. It does not change permissions.

### 3.2 Header and global elements

- Product name (working name, DEC-001), environment badge in non-production (e.g. `STAGING`), role switcher, help link, user menu (profile, settings, sign out).
- Global search is P1. MVP search lives inside Library and Courses.
- Skip-to-content link as the first focusable element.

## 4. Responsive behavior and layouts

| Breakpoint | Width | Layout |
|---|---|---|
| Mobile | < 640 px | Single column; bottom-sheet filters; navigation drawer; tables become stacked cards; sticky primary action on assessment screen |
| Tablet | 640–1023 px | Collapsible side navigation; two-column cards; tables with horizontal scroll inside a container (never the page) |
| Desktop | ≥ 1024 px | Persistent left navigation; content max width 1280 px; split views for review (source passage beside question) and document viewer |

- **Minimum supported width:** 360 px (UX-001).
- **Touch targets:** At least 44×44 px on touch devices.
- **Split views** on mobile become tabbed views ("Question" | "Source").

## 5. Color and typography system

Implemented as design tokens (CSS variables consumed by Tailwind/shadcn).

**Colour roles:** exact hex values are chosen in design (Decision required). Every text/background pair must meet contrast rules.

| Token | Role |
|---|---|
| `--background`, `--foreground` | Page |
| `--card`, `--card-foreground` | Surfaces |
| `--primary`, `--primary-foreground` | Primary actions (single brand hue, deep blue/indigo family proposed) |
| `--muted`, `--muted-foreground` | Secondary text and backgrounds |
| `--border`, `--ring` | Borders and focus ring (focus ring ≥ 3:1 against adjacent colours) |
| `--success` | Completed, approved |
| `--warning` | Provisional, unreviewed, validator warnings |
| `--danger` | Errors, rejected, destructive |
| `--info` | Informational notices |
| `--mock` | MOCK data badge (distinct hue plus text "MOCK") |
| `--ai` | AI-generated content marker (subtle; always with text label) |
| `--level-1` … `--level-5` | Competency level scale (sequential palette, colour-blind safe; never the only encoding) |

**Contrast:** Body text ≥ 4.5:1; large text and UI components ≥ 3:1. Colour never conveys meaning alone: always pair with text, icon or pattern.

**Typography**
- **Font:** A system font stack, or an open-licence sans-serif with good Devanagari support (e.g. Noto Sans and Noto Sans Devanagari) for Hindi readiness (Decision required).
- **Scale:** 12 / 14 / 16 (body) / 18 / 20 / 24 / 30 px. Line height 1.5 for body text.
- **Numbers:** Tabular numerals in tables and scores.
- **Text resizing:** Layout must tolerate 200% text resize (ACC-011 control is P1; browser zoom supported in MVP).

## 6. Accessibility rules

| Rule | Detail |
|---|---|
| Semantics | Landmarks (`header`, `nav`, `main`), one `h1` per page, logical heading order, native elements before ARIA |
| Keyboard | All interactive elements reachable and operable; visible focus; no keyboard traps; logical order; `Esc` closes dialogs; focus returns to trigger |
| Screen readers | Accessible names for all controls; `aria-live="polite"` for async status (processing, job progress, save confirmations); `aria-live="assertive"` only for blocking errors |
| Forms | Labels bound to inputs; instructions before fields; inline errors linked via `aria-describedby`; error summary at top on submit with links to fields |
| Tables | `th` with `scope`; captions; sortable headers announce sort state |
| Charts | Text summary plus data table toggle; patterns or markers in addition to colour; keyboard-focusable data points not required when table is provided |
| Motion | Respect `prefers-reduced-motion`; no auto-playing motion; no flashing |
| Timeouts | Session timeout warning with option to extend; assessments have no time limits in MVP |
| Language | `lang="en"` on root; per-element `lang` when Hindi content appears (P1) |
| Testing | axe checks in CI on every P0 screen; manual NVDA/JAWS/VoiceOver and keyboard testing of journeys J-01 to J-07 before MVP release |

## 7. Component system

Based on shadcn/ui (Radix primitives) and extended with product components:

| Component | Purpose |
|---|---|
| `AppShell` | Header, navigation, skip link, content area |
| `PageHeader` | Title, purpose line, primary action |
| `StatusBadge` | Workflow statuses (approved, in review, provisional, needs OCR, …) with text |
| `ProvenanceBadge` | Source organisation and `data_status`; opens provenance popover (URL, retrieval date, licence status) |
| `MockBadge` | "MOCK - not real iGOT data" (never dismissible) |
| `AIGeneratedLabel` | "AI-generated" with model and prompt version in a popover for staff roles |
| `CitationChip` / `CitationList` | Source title, page, quoted span preview; opens viewer at page |
| `ConfidenceIndicator` | Q&A confidence band with definition |
| `EvidenceBand` | Competency evidence sufficiency with definition |
| `ExplanationPanel` | "How was this calculated?" content for estimates |
| `ReasonList` | "Why recommended" reasons |
| `ValidationFlags` | Validator results for reviewers (fail/warn/incomplete) |
| `ReviewActionBar` | Approve / Edit / Reject / Override controls with reason capture |
| `JobProgress` | Background job state with live-region announcements |
| `DataTable` | Accessible table with cursor pagination, sort, filters, empty/loading/error states, mobile card mode |
| `ChartWithTable` | Chart plus table toggle and text summary |
| `EmptyState`, `LoadingState`, `ErrorState` | Standard states (§8.5–8.7) |
| `ConfirmDialog` | Confirmations for destructive or consequential actions |
| `ReauthDialog` | Re-authentication for sensitive actions |
| `NoticeBanner` | Persistent notices (e.g. "Thresholds are provisional", "Environment: STAGING") |

## 8. Patterns

### 8.1 Forms

- Single column. Required fields marked with text ("required").
- Validate on blur and on submit. Server errors are mapped to fields from `errors[]` in problem responses.
- Submit buttons show progress and prevent double submission (idempotency keys for flagged endpoints).
- Unsaved-change warning on navigation for long forms (question editor, framework editor).

### 8.2 Tables

- Cursor pagination with "Load more" or page controls. Sortable columns limited to API allow-lists. Filter chips shown above the table.
- Row actions in an overflow menu, plus a keyboard shortcut to open the row.
- On mobile, rows become cards with the primary field as the title.

### 8.3 Charts

- **Library:** Recharts with a `ChartWithTable` wrapper.
- **Chart types:** Bar charts for required vs current, and a timeline (list) for assessment history. No pie charts for competency data.
- **Axes and summary:** Always labelled, with a text summary sentence (e.g. "3 of 8 competencies are below the level required for your role").

### 8.4 Dashboards

- **Layout:** Card grid with independent data fetching; each card has its own loading, empty and error states.
- **Card content:** Maximum 6–8 cards per dashboard. Each card has one clear action.

### 8.5 Loading states

- **Content:** Skeletons shaped like the content, shown after 300 ms (avoids flicker).
- **Long operations:** Show `JobProgress`, not spinners.
- **Timeout:** After 30 s of loading a non-job request, show "This is taking longer than expected" with retry.

### 8.6 Empty states

- **Structure:** Explain why it is empty and the next step. For example, Library empty for a learner: "No materials have been shared with you yet."
- **Role-specific actions:** e.g. trainers see "Upload material".

### 8.7 Error states

- **Content:** Human message, what the user can do, and the correlation ID ("Reference: 01J9…") with a copy button.
- **Mapping:** From problem `code` per [ERROR_HANDLING_SPEC.md](ERROR_HANDLING_SPEC.md).
- **Permission errors:** 403 shows "You don't have access to this" without revealing whether the resource exists.

### 8.8 Confirmation states

- **Consequential actions:** Approve, reject, publish, adjust, deactivate, activate a prompt and change access roles all use `ConfirmDialog`. The dialog summarises the effect, and a reason field appears where required.
- **Success feedback:** Toast plus inline status update. Toasts are announced politely and never carry the only copy of important information.

### 8.9 Notification patterns

- **MVP:** Inline banners and toasts only.
- **Counts:** Review queue counts appear on the Trainer dashboard and navigation badges (numbers with text for screen readers).
- **P1:** Notification centre and email (AUT-007).

### 8.10 Review workflows

- **Split view:** Question (stem, options, key, explanation, difficulty, competency) beside the cited source passage, scrolled to the quote.
- **Validator flags at the top:** failures first, then warnings, then incomplete.
- **Keyboard shortcuts** (documented, and can be switched off): `A` approve, `E` edit, `R` reject, `N` next task. They are active only when focus is outside text inputs.
- **Reason capture:** Reject requires a reason category. Override requires reason text. Approving with warnings asks the reviewer to acknowledge each warning.
- **Concurrency:** On 409, the reviewer sees "Someone else decided this task" with a refresh action.

### 8.11 Search experience

- **Library search:**
  - query input, mode toggle ("Meaning" / "Exact words");
  - filters (organisation, topic, document type, status);
  - results show document title, page, snippet with matched terms highlighted (keyword mode) and provenance badge.
- **Empty results:** Suggest switching mode and checking filters.
- **Embedding outage:** Banner "Meaning-based search is unavailable; showing exact-word results."

## 9. AI interaction patterns

| Pattern | Rule |
|---|---|
| **Placement** | AI features sit inside task screens (Ask the documents, Quiz builder, Review). There is no floating chatbot. |
| **Labelling** | Every AI-generated artefact shows `AIGeneratedLabel`; staff roles can see model and prompt version. |
| **Citation display** | Answers are segmented; each segment ends with citation chips (`[1] Sources and Methods, p.12`). The citation list below shows document title, organisation, page(s), quoted span and licence status badge. Selecting a chip opens the Document viewer at the page with the span highlighted. Inaccessible sources show "Source no longer accessible". |
| **Confidence display** | `ConfidenceIndicator` with band label ("High confidence" / "Medium confidence") and a "What does this mean?" popover: "Based on how closely the sources match your question and how many passages support the answer. It is not a guarantee of correctness - check the sources." Never shown as a percentage. |
| **Abstention** | A neutral informational panel (not an error style) with the reason text ([AI_SYSTEM_SPEC.md](AI_SYSTEM_SPEC.md) §19) and next steps (rephrase, change scope, ask a trainer). |
| **Streaming** | If streaming is used, citations and confidence appear only after verification completes. Unverified streamed text is not shown; a progress state ("Checking sources…") is shown instead. |
| **Human-review controls** | Wherever AI-generated questions appear (builder results, review queue), review status is visible and review actions are one click away for eligible roles. |
| **Mock data** | `MockBadge` on every iGOT-sourced card, row and detail view; the Integration health screen shows "Mode: MOCK". |
| **Provisional values** | Provisional thresholds and unreviewed tags carry `StatusBadge` "Provisional" or "Unreviewed". |
| **Errors from AI providers** | Shown as "The AI service is temporarily unavailable" with retry; never raw provider messages. |

## 10. Content and wording guidelines

| Use | Avoid |
|---|---|
| "Developing", "Below the level required for your role" | "Weak", "Poor", "Failed", "Deficient" |
| "Strength", "At or above the required level" | "Top performer", "Best" |
| "Reassess to confirm" (insufficient evidence) | "Unknown skill", "No ability" |
| "Learner development report" | "Performance report", "Appraisal", "Evaluation of employee" |
| "Recommended because…" | "You must…" (unless an assignment, P1) |
| "AI-generated from the cited documents - check the sources" | "The answer is…" without sources |
| "MOCK - not real iGOT data" | "iGOT courses" for mock items |
| "Provisional thresholds" | Presenting thresholds as validated |

A copy lint list of prohibited terms is maintained with the i18n catalogue and checked in CI (MVP-08 test requirement).

---

## 11. Screen specifications

Permission rules reference [SECURITY_RESPONSIBLE_AI.md](SECURITY_RESPONSIBLE_AI.md) §4. Every screen enforces permissions server-side. The UI only hides or disables controls.

### S-01 Login

- **Purpose:** Authenticate provisioned users.
- **Primary user:** All.
- **MVP:** Yes (MVP-01).
- **Entry points:** Direct URL; redirect on 401; session expiry.
- **Main components:** Email field, password field, show-password toggle, submit, "Forgot password? Contact your administrator" text (no self-reset in MVP), environment badge.
- **Main actions:** Sign in.
- **Data displayed:** None beyond form; lockout message when applicable.
- **Empty state:** Not applicable.
- **Loading state:** Submit button busy; inputs disabled during request.
- **Error state:** Generic "Email or password is incorrect"; lockout with time; rate limited with retry time; service unavailable.
- **Permission rules:** Public; authenticated users are redirected to Home.
- **Accessibility requirements:** Labels, autocomplete attributes, error summary with focus, no CAPTCHA without accessible alternative.
- **Acceptance criteria:** Keyboard-only login works; errors announced; no information about account existence; session cookie set as specified in MVP-01.

### S-02 Onboarding

- **Purpose:** Privacy and AI-use notice, profile confirmation, department and job role selection, optional baseline start.
- **Primary user:** Learner (all new users see the notice).
- **MVP:** Yes (MVP-03, MVP-04).
- **Entry points:** First login; forced when notice version changes; profile incomplete.
- **Main components:** Stepper (Notice → Profile → Role → Start); notice text with acknowledgement checkbox; profile form; department and job role searchable selects; role's required competencies preview; "Start baseline assessment" / "Later".
- **Main actions:** Acknowledge; save profile; select role; start assessment.
- **Data displayed:** Notice (versioned); departments; active job roles; approved competency requirements of selected role.
- **Empty state:** No job roles configured → "Your organisation hasn't set up job roles yet. Contact your administrator." (blocks the Role step).
- **Loading state:** Skeleton for role list; busy buttons.
- **Error state:** Validation errors per field; save failures with retry.
- **Permission rules:** Own profile only; role list is organisation-scoped.
- **Accessibility requirements:** Stepper announces current step; focus moves to step heading; checkbox label contains the full acknowledgement statement.
- **Acceptance criteria:** Cannot reach any assessment without acknowledgement; progress is resumable; role change is audited (server).

### S-03 Learner dashboard

- **Purpose:** Orientation and next action.
- **Primary user:** Learner.
- **MVP:** Yes (MVP-19).
- **Entry points:** Home (`/`) for learners; logo link.
- **Main components:** `PageHeader` with role and department; cards: Baseline status, Top gaps (max 3), Continue learning, Recommendations (max 3, `ReasonList`, `ProvenanceBadge`, `MockBadge` when applicable), Recent assessments, Correction requests status.
- **Main actions:** Start or resume assessment; open gap analysis; continue item; open recommendation; dismiss recommendation.
- **Data displayed:** `GET /api/v1/me/dashboard`.
- **Empty state:** New learner: "Start with a baseline assessment to see your competency profile." No recommendations: "No approved learning content matches your gaps yet."
- **Loading state:** Per-card skeletons.
- **Error state:** Per-card `ErrorState` with retry; the rest of the dashboard remains usable.
- **Permission rules:** Self data only.
- **Accessibility requirements:** Cards as sections with headings; counts announced with text.
- **Acceptance criteria:** Each card handles all three states independently; MOCK items labelled; no other user's data.

### S-04 Competency profile

- **Purpose:** Current estimates with evidence, bands, explanations and history.
- **Primary user:** Learner (self); trainer, competency admin, scoped managers (others).
- **MVP:** Yes (MVP-07, MVP-08).
- **Entry points:** Navigation "My competencies"; dashboard; results screen; staff views of a learner.
- **Main components:**
  - role summary;
  - competency list grouped by framework/cluster, with score, level, `EvidenceBand`, required level;
  - `ExplanationPanel`;
  - evidence list;
  - assessment timeline;
  - "Request a review of this result" action;
  - adjustment indicator;
  - staff-only "Adjust" action (eligible roles).
- **Main actions:** Open explanation; view evidence; request correction; (staff) adjust with reason.
- **Data displayed:** `GET /api/v1/me/competency-profile` or `/users/{id}/competency-profile`; evidence endpoint.
- **Empty state:** No estimates: call to action for the baseline assessment. Insufficient evidence: "Reassess to confirm".
- **Loading state:** List skeleton.
- **Error state:** Profile unavailable with retry; stale estimate banner "Being recalculated".
- **Permission rules:** Learner self; trainer assigned scope; competency_admin org; department_admin and training_manager scoped per matrix. Viewing another user's profile is audited (server).
- **Accessibility requirements:** Level shown as text plus visual; explanation panel as disclosure with heading; timeline as ordered list.
- **Acceptance criteria:** Every estimate shows band, method version and limitations; provisional thresholds labelled; correction request action present for the learner; adjustments show reviewer and date.

### S-05 Competency-gap analysis

- **Purpose:** Prioritised gaps with required-vs-current comparison and actions.
- **Primary user:** Learner.
- **MVP:** Yes (MVP-08).
- **Entry points:** Dashboard "Top gaps"; profile.
- **Main components:** `ChartWithTable` (required vs current); gap list sorted by size with evidence band; "Recommended learning" per gap; "Insufficient evidence" section; "Strengths" section.
- **Main actions:** Open recommended item; add to path (regenerate); request review; reassess (P1 post-assessment; MVP shows guidance only).
- **Data displayed:** `GET /api/v1/me/competency-gaps`, recommendations.
- **Empty state:** No gaps with sufficient evidence: "No gaps confirmed. Competencies needing more evidence are listed below."
- **Loading state:** Chart and list skeletons.
- **Error state:** Role not configured: "Your job role's requirements haven't been approved yet." No role: link to settings.
- **Permission rules:** Self; scoped staff via user context.
- **Accessibility requirements:** Chart summary sentence; table default on small screens.
- **Acceptance criteria:** Gaps only where evidence ≥ medium; wording follows §10; table and chart values identical.

### S-06 Assessment screen

- **Purpose:** Take an assessment attempt.
- **Primary user:** Learner.
- **MVP:** Yes (MVP-06).
- **Entry points:** Dashboard; onboarding; assessments list.
- **Main components:** Header with assessment title and progress ("Question 4 of 20"); question stem; radio option group; "Previous" / "Next"; question navigator; save status; submit dialog summarising unanswered questions.
- **Main actions:** Answer; navigate; submit.
- **Data displayed:** `GET /api/v1/attempts/{id}` (no keys).
- **Empty state:** Not applicable (attempt cannot be created without questions).
- **Loading state:** Question skeleton; answer save "Saving…" then "Saved" (polite live region).
- **Error state:** Save failure → retry with answer preserved locally in memory (not persistent storage); attempt expired; already submitted (redirect to result).
- **Permission rules:** Attempt owner only.
- **Accessibility requirements:** Fieldset/legend per question; options as native radio inputs; navigator buttons labelled with answered state; no time pressure in MVP.
- **Acceptance criteria:** No answer keys in network responses; answers persist on reload; submit requires confirmation; fully keyboard operable.

### S-07 Assessment results

- **Purpose:** Show scoring outcome, feedback and competency impact.
- **Primary user:** Learner; trainer (scoped).
- **MVP:** Yes (MVP-06, MVP-07).
- **Entry points:** After submit; history.
- **Main components:** Overall summary; per-competency results with bands; per-question feedback (per policy) with correct/incorrect icons plus text, explanations and `CitationChip`s; "Go to gap analysis"; "Request a review" per question.
- **Main actions:** View explanations and sources; request correction; open gap analysis.
- **Data displayed:** `GET /api/v1/attempts/{id}/result`.
- **Empty state:** Not applicable.
- **Loading state:** "Scoring your assessment…" with job-like progress if scoring is pending.
- **Error state:** `scoring_failed` → "We couldn't score this yet. We'll retry automatically." with status polling.
- **Permission rules:** Owner; scoped trainer.
- **Accessibility requirements:** Result list uses text labels, not colour; explanations as disclosures.
- **Acceptance criteria:** Feedback follows the assessment policy; citations open source pages; rescoring notices shown when applicable.

### S-08 Learning path

- **Purpose:** Ordered learning items addressing gaps.
- **Primary user:** Learner.
- **MVP:** Yes (MVP-18).
- **Entry points:** Navigation; dashboard "Continue learning"; gap analysis.
- **Main components:** Path header (generated date, rule version for staff); ordered item list grouped by gap; each item: title, type, provider, `ProvenanceBadge`, `MockBadge` if applicable, `ReasonList`, status control (not started / in progress / completed - self-reported label); "Regenerate path" (with confirmation).
- **Main actions:** Open item; change status; regenerate.
- **Data displayed:** `GET /api/v1/me/learning-path`.
- **Empty state:** No gaps: "Your path is empty because no gaps are confirmed." No content: placeholder items "No approved content yet for <competency>".
- **Loading state:** List skeleton; regenerate job progress.
- **Error state:** Regeneration failed → previous path retained with notice.
- **Permission rules:** Self; scoped staff read-only (administrator status changes audited).
- **Accessibility requirements:** Ordered list semantics; status control as labelled select or segmented radio.
- **Acceptance criteria:** Every item shows reason and provenance; completed items preserved after regeneration; self-reported completions labelled.

### S-09 Course discovery

- **Purpose:** Browse the catalogue (internal courses, NSSTA programme listings, mock iGOT when flagged).
- **Primary user:** Learner; training manager (curation).
- **MVP:** Yes (MVP-17).
- **Entry points:** Navigation "Courses"; recommendation cards.
- **Main components:** Filters (source type, topic, competency); course cards (title, provider, target group, duration, fiscal year, schedule status "Tentative", provenance, review status for staff, `MockBadge`); detail drawer; staff "Edit / review mappings".
- **Main actions:** View details; (learner) open recommendation reason; (staff) review course, approve mappings.
- **Data displayed:** `GET /api/v1/courses`, `GET /api/v1/integrations/igot/courses` (flagged, mock).
- **Empty state:** "No approved courses available yet." Staff variant: "Seeded NSSTA listings await review."
- **Loading state:** Card skeletons.
- **Error state:** iGOT source unavailable → "iGOT source not connected" (staff) / silently omitted with notice for learners.
- **Permission rules:** Learners see approved, displayable items only; staff see review states per matrix.
- **Accessibility requirements:** Cards as list items with headings; filters as accessible form controls.
- **Acceptance criteria:** NSSTA listings show "dates not available" and "Tentative"; programme codes shown as printed; mock items never without MOCK label.

### S-10 Document library

- **Purpose:** Browse, search, upload and manage learning materials.
- **Primary user:** Trainer; learner (browse/search).
- **MVP:** Yes (MVP-09, MVP-10, MVP-11).
- **Entry points:** Navigation "Library"; trainer dashboard.
- **Main components:**
  - search bar with mode toggle;
  - filters;
  - materials table/cards (title, organisation, type, pages, processing status, licence status, access scope, provenance);
  - "Upload material" dialog (metadata, access scope, licence notes, attestation checkboxes, file input);
  - `JobProgress` per upload;
  - admin actions (deactivate, reprocess, licence flags).
- **Main actions:** Search; open material; upload; reprocess; deactivate.
- **Data displayed:** `GET /api/v1/learning-materials`, `POST /api/v1/search`.
- **Empty state:** Learner: "No materials shared with you yet." Trainer: "Upload your first material."
- **Loading state:** Table skeleton; upload progress bar plus processing status.
- **Error state:** Upload validation errors (file type, size, signature); `needs_ocr` status explained ("This document has no readable text. OCR is not available yet."); processing failed with retry.
- **Permission rules:** ACL filtering server-side; upload for trainer and admin roles; licence flags for OA/CA/TM.
- **Accessibility requirements:** File input with clear label and instructions; upload status announced; table accessible.
- **Acceptance criteria:** Duplicate upload shows link to existing material; statuses match job state; restricted materials never visible to unauthorised users.

### S-11 Document viewer

- **Purpose:** Read a document with page navigation and citation highlighting.
- **Primary user:** All with access.
- **MVP:** Yes (MVP-13).
- **Entry points:** Library; citation chips; results; review split view.
- **Main components:** Metadata panel (title, organisation, source URL, retrieval date, licence, series/base year status, topics with review state); page navigator; page text view with highlighted cited span; PDF render (sandboxed) where available; "Ask about this document" link (scope preset).
- **Main actions:** Navigate pages; open source URL (external link, labelled); ask a question scoped to the document.
- **Data displayed:** `GET /api/v1/learning-materials/{id}`, `GET /api/v1/documents/{id}/pages/{page}`.
- **Empty state:** Link-only material: "This document is recorded as a link only; open the official source."
- **Loading state:** Page skeleton.
- **Error state:** Access revoked (403 message); page out of range.
- **Permission rules:** Document ACL re-checked per page request.
- **Accessibility requirements:** Text view is the accessible primary view; highlighted span announced ("Cited passage"); page navigator labelled.
- **Acceptance criteria:** Citation deep links land on the correct page with the span highlighted; licence and provenance visible; superseded/series warnings visible when set.

### S-12 Document Q&A ("Ask the documents")

- **Purpose:** Grounded answers with citations or abstention.
- **Primary user:** Learner, trainer.
- **MVP:** Yes (MVP-12); feature-flagged and evaluation-gated.
- **Entry points:** Navigation; document viewer.
- **Main components:** Scope selector (all accessible / selected material); question input with character limit; privacy hint ("Don't include personal information"); answer panel with segmented text, `CitationChip`s, `CitationList`, `ConfidenceIndicator`, `AIGeneratedLabel`; abstention panel; "Report a problem" link (logs flag for audit sampling); recent questions in session memory only.
- **Main actions:** Ask; open citations; change scope.
- **Data displayed:** `POST /api/v1/document-qa` response.
- **Empty state:** Before first question: example questions drawn from accessible documents' titles (static copy, not AI-generated).
- **Loading state:** "Searching documents…" then "Checking sources…" (polite live region).
- **Error state:** Rate limited (retry time); AI unavailable; feature disabled ("This feature isn't available yet").
- **Permission rules:** All roles except auditor; retrieval limited to accessible and (for learners) display-permitted documents.
- **Accessibility requirements:** Answer region is a live region announced once complete; citations as a list of links.
- **Acceptance criteria:** No answer without verified citation; abstention styled as information; no percentages; redaction notice shown when redaction applied.

### S-13 Quiz builder

- **Purpose:** Generate MCQs, author questions manually, and build assessment blueprints.
- **Primary user:** Trainer, competency admin.
- **MVP:** Yes (MVP-06, MVP-14).
- **Entry points:** Trainer dashboard; navigation.
- **Main components:**
  - Tabs: Generate | Write manually | Build assessment.
  - Generate: source picker showing only `generation_permitted` materials (others disabled with reason), competency, topic, difficulty, count, `JobProgress`, results list linking to review.
  - Write: question editor with mandatory citation picker (document, page, quote).
  - Build: blueprint editor (purpose, job role, competencies with available approved item counts, minimum items), publish.
- **Main actions:** Start generation; save manual question (submit to review); create or publish assessment.
- **Data displayed:** Materials, competencies, topics, question counts, job status.
- **Empty state:** No generation-permitted materials: "No materials are cleared for question generation. Ask an administrator to review licence status."
- **Loading state:** Job progress with counts (generated, passed validation).
- **Error state:** Quota exceeded; provider unavailable; publish blocked with a list of unmet requirements.
- **Permission rules:** Trainer and competency_admin; source ACLs.
- **Accessibility requirements:** Tabs with arrow-key navigation; editor fields labelled; citation picker keyboard operable.
- **Acceptance criteria:** Generated questions go only to review; publish blocked unless all items approved and minimums met; licence gate visible.

### S-14 Quiz review

- **Purpose:** Human review of AI-generated and manual questions.
- **Primary user:** Trainer, competency admin.
- **MVP:** Yes (MVP-15, MVP-16).
- **Entry points:** Trainer dashboard review count; navigation "Review".
- **Main components:** Queue table (filters: status, competency, origin, flags); split view (question vs source passage); `ValidationFlags`; near-duplicate links; AI metadata; version history; `ReviewActionBar`; inline editor.
- **Main actions:** Approve; edit (new version); reject with reason; override validation with reason; reassign; next task.
- **Data displayed:** `GET /api/v1/review-tasks`, task detail, validations, citations.
- **Empty state:** "No questions waiting for review."
- **Loading state:** Split-view skeleton.
- **Error state:** 409 concurrent decision; source inaccessible → reassign prompt.
- **Permission rules:** Eligible reviewer roles; second-reviewer policy and self-approval block enforced server-side and reflected in UI.
- **Accessibility requirements:** Shortcuts optional and documented; focus management between queue and detail; flags announced.
- **Acceptance criteria:** Reviewers can complete a decision keyboard-only; every rejection has a reason; edits create new versions visible in history.

### S-15 Tutor (P1)

- **Purpose:** Conversational grounded tutoring.
- **Primary user:** Learner.
- **MVP:** **No - P1** (TUT-001 to TUT-020). The screen must not be reachable in the MVP build.
- **Entry points (P1):** Navigation "Tutor"; document viewer "Study with tutor".
- **Main components (P1):** Conversation list; message thread with citations and confidence; scope selector; flag response; delete conversation.
- **Main actions (P1):** Send message; open citations; flag; delete history.
- **Data displayed (P1):** Tutor endpoints (reserved).
- **Empty state (P1):** Introductory guidance and limitations.
- **Loading state (P1):** "Checking sources…".
- **Error state (P1):** Abstentions; AI unavailable.
- **Permission rules (P1):** Self conversations only.
- **Accessibility requirements (P1):** Message list as log region; keyboard send; history deletion confirmation.
- **Acceptance criteria (P1):** Same grounding invariants as S-12; learner-deletable history.

### S-16 Progress analytics (basic)

- **Purpose:** Progress lists and assessment timeline.
- **Primary user:** Learner; trainer and managers (scoped).
- **MVP:** Yes, basic (MVP-24). Growth graphs and before-vs-after are P1.
- **Entry points:** Navigation "Progress"; staff learner views.
- **Main components:** Tabs Completed | Pending | Recommended; learning history list; assessment timeline; baseline indicator per competency.
- **Main actions:** Open item; mark completion (self); filter.
- **Data displayed:** `GET /api/v1/me/progress`, `/me/progress/history`, `/me/attempts`.
- **Empty state:** "No learning activity yet."
- **Loading state:** List skeletons.
- **Error state:** Per-tab error with retry.
- **Permission rules:** Self; scoped staff read.
- **Accessibility requirements:** Tabs accessible; timeline as ordered list with dates.
- **Acceptance criteria:** Self-reported labels visible; history survives deactivated content (title snapshots).

### S-17 Trainer dashboard

- **Purpose:** Trainer work queue and scoped learner status.
- **Primary user:** Trainer; training manager.
- **MVP:** Yes (MVP-20).
- **Entry points:** Home for trainers.
- **Main components:** Cards: Questions awaiting review (count plus link), Generation jobs (status), Recent uploads (processing status), Correction requests awaiting decision, Learners in scope (unranked list with baseline status and path progress).
- **Main actions:** Open review queue; open job; open learner (scoped profile); open correction request.
- **Data displayed:** `GET /api/v1/trainer/dashboard`, `GET /api/v1/progress`.
- **Empty state:** Per card (e.g. "No learners in your scope yet").
- **Loading state:** Card skeletons.
- **Error state:** Per-card errors.
- **Permission rules:** Trainer scope per matrix; no rankings.
- **Accessibility requirements:** As dashboards pattern.
- **Acceptance criteria:** Counts match queues; learner list unranked and scoped; viewing a learner profile audited (server).

### S-18 Admin dashboard

- **Purpose:** Organisation administration.
- **Primary user:** Organisation admin; competency admin; department admin (scoped); platform admin.
- **MVP:** Yes (MVP-02, MVP-04, MVP-05, MVP-17, MVP-20).
- **Entry points:** Navigation "Administration".
- **Main components:** Sections: Users (table, provision, deactivate, access roles with `ReauthDialog`); Departments; Job roles (with competency mapping editor and approval); Competency frameworks (import provenance, clusters, levels with provisional thresholds, approve); Courses (seeded NSSTA listings review, mappings); Materials licence flags; Seed import status (read-only).
- **Main actions:** Create/update/deactivate; approve framework/mappings; review courses.
- **Data displayed:** Admin endpoints ([API_INTEGRATION_SPEC.md](API_INTEGRATION_SPEC.md) §2.4, §2.5, §2.9).
- **Empty state:** Per section with guidance (e.g. "No job roles yet - create one").
- **Loading state:** Table skeletons.
- **Error state:** Validation errors; 409 optimistic lock conflicts ("This was changed by someone else - reload").
- **Permission rules:** Section visibility per matrix; CSCD definitions never editable (restricted guard message).
- **Accessibility requirements:** Tables and forms patterns; confirmation dialogs.
- **Acceptance criteria:** Last org admin cannot be removed; approvals require re-authentication; restricted framework shows page references not definitions.

### S-19 Department heatmap (P1)

- **Purpose:** Aggregated competency levels by department and competency.
- **Primary user:** Department admin; training manager.
- **MVP:** **No - P1** (CMP-003, ANA-001). Not reachable in MVP.
- **Entry points (P1):** Administration → Analytics.
- **Main components (P1):** Heatmap with table toggle; suppression indicators; caveat banner.
- **Main actions (P1):** Filter by department/competency; export (P1).
- **Data displayed (P1):** Analytics endpoints (reserved).
- **Empty state (P1):** "Not enough data to show this safely."
- **Loading state (P1):** Grid skeleton.
- **Error state (P1):** Suppressed cells explained.
- **Permission rules (P1):** Scoped managers; minimum group size.
- **Accessibility requirements (P1):** Table equivalent mandatory; non-colour encodings.
- **Acceptance criteria (P1):** No cell below minimum group size; caveats shown.

### S-20 Reports

- **Purpose:** Generate and download reports.
- **Primary user:** Training manager; learner (own); trainer and department admin (scoped).
- **MVP:** Yes (MVP-25).
- **Entry points:** Navigation "Reports"; profile "Download my report".
- **Main components:** Report type selector (types filtered by role); subject/scope selector; generate button; report list with status and `JobProgress`; HTML report view with "not an appraisal" notice; CSV download.
- **Main actions:** Generate; view; download CSV.
- **Data displayed:** `POST /api/v1/reports`, `GET /api/v1/reports/{id}`.
- **Empty state:** "No reports generated yet."
- **Loading state:** Generation progress.
- **Error state:** Unauthorised scope; generation failed with retry.
- **Permission rules:** Report types and subjects per matrix; downloads audited.
- **Accessibility requirements:** HTML view is primary accessible format; table headers and units.
- **Acceptance criteria:** Learner can always generate own development report; notice present; CSV escaped.

### S-21 Settings

- **Purpose:** Personal settings and (for admins) organisation settings and feature flags.
- **Primary user:** All; org admin and platform admin for organisation sections.
- **MVP:** Yes (MVP-03, MVP-20).
- **Entry points:** User menu; Administration.
- **Main components:** Profile (UX-021); Job role; Privacy notice (view acknowledged version); Sessions ("Sign out everywhere"); Admin sections: approval policy, evidence-band and threshold settings (read-only link to framework approval), feature flags (with evaluation-gate status), iGOT mock source visibility flag.
- **Main actions:** Save profile; change job role; revoke sessions; update settings (re-authentication for security keys).
- **Data displayed:** `GET /api/v1/me`, `GET /api/v1/admin/settings`.
- **Empty state:** Not applicable.
- **Loading state:** Form skeletons.
- **Error state:** Validation; evaluation gate not met ("This AI feature can't be enabled until its evaluation passes").
- **Permission rules:** Admin sections per matrix; secrets never displayed.
- **Accessibility requirements:** Forms pattern; toggles with labels and state text.
- **Acceptance criteria:** Evaluation-gated flags cannot be enabled without passing evaluation; changes audited (server).

### S-22 Audit logs

- **Purpose:** Investigate actions and AI interactions.
- **Primary user:** System auditor; platform admin; org admin (limited).
- **MVP:** Yes (MVP-22).
- **Entry points:** Administration → Audit.
- **Main components:** Tabs Events | AI interactions; filters (actor, action, target, date range, outcome, correlation ID, purpose, status, abstained); results table; detail drawer (redacted before/after, reason; AI: model, prompt version, input refs, citations, validation, tokens, latency); "Follow correlation ID" action; export (P1).
- **Main actions:** Filter; open detail; follow correlation.
- **Data displayed:** `GET /api/v1/audit-logs`, `GET /api/v1/ai-interactions`.
- **Empty state:** "No events match these filters."
- **Loading state:** Table skeleton.
- **Error state:** Access denied; query too broad ("Narrow the date range").
- **Permission rules:** Read-only; AI tab auditor and platform admin only; access audited.
- **Accessibility requirements:** Data table pattern; drawer focus management.
- **Acceptance criteria:** No modification controls exist; redacted fields indicated; correlation trace shows linked events across API, jobs and AI.

### S-23 Integration health

- **Purpose:** Show exact state of external integrations and jobs.
- **Primary user:** Platform admin; org admin; auditor (read).
- **MVP:** Yes (MVP-21, MVP-F2).
- **Entry points:** Administration → Integrations.
- **Main components:** iGOT card: Mode (`MOCK` / `NOT CONNECTED`), health status, last checked, last error, feature flag state, explanatory text ("No authorised iGOT access. Mock data is synthetic and labelled."); link to IGOT_ACCESS_STATUS summary; AI provider status (configured provider name, evaluation gate status, fake/real); job monitoring panel (queue counts, failed/dead-letter jobs with retry for platform admin).
- **Main actions:** Run health check; toggle mock visibility flag (org admin/platform admin); retry dead-letter job (platform admin).
- **Data displayed:** `GET /api/v1/integrations`, `/integrations/igot/health`, `/admin/jobs`.
- **Empty state:** No integrations configured: "No integrations configured."
- **Loading state:** Card skeletons.
- **Error state:** Health check failed → `degraded` with error code.
- **Permission rules:** Per matrix; no credentials displayed or editable.
- **Accessibility requirements:** Status conveyed in text; job table accessible.
- **Acceptance criteria:** A mock adapter never shows "Connected"; not-connected state explicit; retry actions audited (server).

---

## 12. Screen-to-role summary

| Screen | learner | trainer | department_admin | org_admin | competency_admin | training_manager | auditor | platform_admin | MVP |
|---|---|---|---|---|---|---|---|---|---|
| S-01 Login | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Yes |
| S-02 Onboarding | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (notice/profile) | ✓ (notice/profile) | Yes |
| S-03 Learner dashboard | ✓ | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) | - | - | Yes |
| S-04 Competency profile | ✓ self | ○ assigned | ○ dept (limited) | - | ✓ | ○ dept | - | - | Yes |
| S-05 Gap analysis | ✓ self | ○ assigned | - | - | ✓ | ○ dept | - | - | Yes |
| S-06 Assessment screen | ✓ | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) | - | - | Yes |
| S-07 Assessment results | ✓ self | ○ assigned | - | - | ✓ | - | - | - | Yes |
| S-08 Learning path | ✓ self | ○ read | - | - | - | ○ read | - | - | Yes |
| S-09 Course discovery | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ (curate) | - | - | Yes |
| S-10 Document library | ✓ | ✓ (upload) | ✓ | ✓ | ✓ | ✓ | - | ✓ (reprocess) | Yes |
| S-11 Document viewer | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✓ | Yes |
| S-12 Document Q&A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | - | ✓ | Yes |
| S-13 Quiz builder | - | ✓ | - | - | ✓ | - | - | - | Yes |
| S-14 Quiz review | - | ✓ | - | - | ✓ | read | - | - | Yes |
| S-15 Tutor | ✓ | - | - | - | - | - | - | - | P1 |
| S-16 Progress analytics | ✓ self | ○ assigned | ○ dept | - | - | ○ dept | - | - | Yes |
| S-17 Trainer dashboard | - | ✓ | - | - | ✓ | ✓ | - | - | Yes |
| S-18 Admin dashboard | - | - | ○ dept users | ✓ | ✓ (competency sections) | ✓ (courses/materials) | - | ✓ (platform sections) | Yes |
| S-19 Department heatmap | - | - | ○ | ✓ | - | ○ | - | - | P1 |
| S-20 Reports | ✓ self | ○ | ○ dept | ✓ | ✓ | ○ | - | - | Yes |
| S-21 Settings | ✓ | ✓ | ✓ | ✓ (+org) | ✓ | ✓ | ✓ | ✓ (+platform) | Yes |
| S-22 Audit logs | - | - | - | ○ limited | - | - | ✓ | ✓ | Yes |
| S-23 Integration health | - | - | - | ✓ | - | read | read | ✓ | Yes |
