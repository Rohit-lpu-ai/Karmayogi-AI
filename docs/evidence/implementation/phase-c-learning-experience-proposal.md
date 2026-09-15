# Proposal - Learning Experience Schema (C7)

| Field | Value |
|---|---|
| **Status** | **Proposed - awaiting product owner approval.** No migration has been written |
| **Date** | 2026-09-15 |
| **Required by** | DEC-049 ("the schema migration is proposed in writing before implementation") |
| **Related** | DATA_MODEL.md §8 (LearningPath, LearningPathItem, LearningActivity, ProgressRecord, LearningMaterial) · MVP-18, MVP-24 · UI_UX_SPEC S-08, S-16 · DEC-049, DEC-051, DEC-052 |

## 1. Goal

Let a learner open a recommended course, work through its modules and lessons, mark lessons complete, resume where they stopped, and see progress on the course, the learning path and the dashboard - using synthetic DEMO lessons now, replaceable by reviewed content later.

## 2. Principles

1. **Reuse the specified entities** for paths and progress (`LearningPath`, `LearningPathItem`, `ProgressRecord`, `LearningActivity`) exactly as DATA_MODEL.md defines them.
2. **Separate structure from content.** A lesson points to its body through a content reference, so a synthetic Markdown body can later become a reviewed `LearningMaterial`, an approved external resource or a cited retrieval result without touching progress history.
3. **Progress never changes competency estimates** (CMP-018 is P1). Only assessments create evidence.
4. **Self-reported completion is labelled** (`status_source='self_reported'`, MVP-24).
5. **No P1 metrics:** no time-on-task, streaks, hours, certificates or growth graphs.

## 3. Proposed tables (migration `0006`)

### 3.1 New (DEC-049)

**`course_modules`** - SC, TS

| Column | Type | Notes |
|---|---|---|
| `course_id` | uuid → courses | |
| `position` | smallint | unique `(course_id, position)` |
| `title` | text | |
| `summary` | text null | |
| `status` | text | `active`, `inactive` |

**`lessons`** - SC, TS, OL

| Column | Type | Notes |
|---|---|---|
| `module_id` | uuid → course_modules | |
| `position` | smallint | unique `(module_id, position)` |
| `title` | text | |
| `lesson_type` | text | `reading`, `worked_example`, `practice_check` (MVP) |
| `estimated_minutes` | smallint null | author's estimate, shown as guidance only |
| `content_kind` | text | `inline_markdown` (DEMO), `learning_material` (later) |
| `body_markdown` | text null | required when `inline_markdown`; rendered as sanitised Markdown, no HTML |
| `learning_material_id` | uuid null | reserved for `learning_material`; FK added with the Phase 5 content tables |
| `data_status` | text | `ASSUMED` for DEMO |
| `review_status` | text | `unreviewed`, `approved`; learners see `approved` only |
| `status` | text | `active`, `inactive` |

Constraint: exactly one content source per `content_kind`.

### 3.2 From DATA_MODEL.md (P0, not yet migrated)

- `learning_paths`, `learning_path_items` - as specified (§8), item types `course` and `no_content_placeholder` in this phase.
- `progress_records` - as specified; `target_type` gains `lesson` alongside `course`, `learning_material`, `learning_path_item`.
- `learning_activities` - as specified, append-only; `activity_type` gains `lesson_opened`, `lesson_completed`.

## 4. API (all under `/api/v1`, learner self-service)

| Method | Path | Purpose |
|---|---|---|
| GET | `/courses/{id}/outline` | Modules and lessons with the caller's lesson status |
| GET | `/lessons/{id}` | Lesson body, previous/next lesson, caller's status |
| PUT | `/me/lessons/{id}/progress` | `{status: "in_progress" \| "completed"}`; self-reported; updates course `ProgressRecord` (completed when all active lessons completed) |
| GET | `/me/learning-path` | Active path (generated from gaps with `path-v1`: one item per recommended course, ordered like `rec-v1`, plus placeholders for gaps without content) |
| POST | `/me/learning-path/regenerate` | Deterministic; completed items carried over |
| GET | `/me/progress` | Courses in progress, completed, and next lesson to resume |

## 5. Screens

- **Course detail:** outline with module and lesson status, progress bar, "Start course" / "Continue: <lesson>".
- **Lesson player** (`/courses/:courseId/lessons/:lessonId`): lesson navigation sidebar (drawer on mobile), readable body, "Mark as complete", previous/next, completion state for the course, DEMO label on every lesson.
- **Learning path** (`/learning-path`): ordered items grouped by gap with reason and status.
- **Dashboard:** "Continue learning" card and learning progress (courses started and completed only).

## 6. DEMO content in pack `demo-2` (version 2)

2-3 modules and 5-8 short lessons per course (reading, worked example, practice check), all synthetic, labelled DEMO, `review_status='approved'` by the seed only (as DEC-045).

## 7. Risks

| Risk | Mitigation |
|---|---|
| Synthetic lessons read as official training | DEMO label on course, module and lesson; footer on every lesson |
| Stored Markdown becomes an XSS vector | Render with a Markdown renderer that disallows raw HTML; test with script payloads |
| Scope creep into P1 progress analytics | Only statuses and counts; no time, streaks or graphs |
| Two sources of truth for progress | `ProgressRecord` is the only current-state table; `LearningActivity` is history |

## 8. Decision needed

Approve sections 3-6 as written (or amend), so migration `0006` and the C7 screens can be implemented.
