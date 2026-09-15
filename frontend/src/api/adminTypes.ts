// Response shapes of the Phase 4C content administration endpoints (backend/app/modules/content_admin).

export type QuestionStatus = "draft" | "pending_validation" | "failed_validation" | "validation_incomplete" | "in_review" | "approved" | "rejected" | "suspended" | "retired";
export type SourceKind = "synthetic" | "source_record" | "external_reference";
export type Difficulty = "foundational" | "intermediate" | "advanced";

export interface CompetencyOption {
  id: string;
  code: string;
  name: string;
  framework_code: string;
  restricted?: boolean;
}

export interface QuestionListItem {
  id: string;
  status: QuestionStatus;
  origin: "human_authored" | "demo_seed" | "ai_generated";
  stem: string;
  difficulty: Difficulty;
  version_number: number;
  competency: { id: string; code: string; name: string };
  source_count: number;
  is_demo: boolean;
  updated_at: string;
}

export interface QuestionList {
  items: QuestionListItem[];
  total: number;
  page: number;
  page_size: number;
  status_counts: Record<string, number>;
}

export interface SourceOut {
  id: string;
  source_kind: SourceKind;
  label: string;
  status: string;
  source_record_id: string | null;
  title: string | null;
  publisher: string | null;
  url: string | null;
  locator: string | null;
  note: string | null;
}

export interface ReviewHistoryItem {
  task_id: string;
  status: "open" | "decided" | "cancelled";
  version_id: string | null;
  submitted_at: string;
  submitted_by: string | null;
  note: string | null;
  decision: "approve" | "reject" | "request_changes" | null;
  reason: string | null;
  decided_by: string | null;
  decided_at: string | null;
}

export interface QuestionDetail {
  id: string;
  status: QuestionStatus;
  origin: QuestionListItem["origin"];
  row_version: number;
  is_demo: boolean;
  current_version: {
    id: string;
    version_number: number;
    stem: string;
    explanation: string;
    difficulty: Difficulty;
    competency: { id: string; code: string; name: string; framework_code: string };
    options: { label: string; text: string; is_correct: boolean }[];
    sources: SourceOut[];
    created_at: string;
    created_by: string | null;
  };
  approved_version_id: string | null;
  versions: { id: string; version_number: number; created_at: string; created_by: string | null; is_approved: boolean }[];
  reviews: ReviewHistoryItem[];
  open_task_id: string | null;
  used_in_assessments: { id: string; title: string; status: string }[];
  quality_checks: { method: string; findings: { code: string; severity: "error" | "warning"; message: string }[] };
  actions: { can_edit: boolean; can_submit: boolean; can_withdraw: boolean; can_retire: boolean };
}

export interface QuestionAuthoringOptions {
  competencies: CompetencyOption[];
  source_records: { id: string; label: string; organisation: string; record_id: string; verified: boolean; licence_notes: string }[];
  difficulties: Difficulty[];
}

export interface SourceInput {
  source_kind: SourceKind;
  source_record_id?: string | null;
  title?: string | null;
  publisher?: string | null;
  url?: string | null;
  locator?: string | null;
  note?: string | null;
}

export interface ReviewTaskItem {
  id: string;
  task_type: "question_version_review" | "course_review";
  target_type: "question" | "course";
  target_id: string;
  target_version_id: string | null;
  title: string;
  status: "open" | "decided" | "cancelled";
  submitted_by: { id: string; display_name: string } | null;
  submitted_at: string;
  submission_note: string | null;
  decided_at: string | null;
  decision: { decision: string; reason: string | null; decided_at: string; decided_by: string | null } | null;
  can_decide: boolean;
  blocked_reason: string | null;
  row_version: number;
}

export type CourseState = "draft" | "in_review" | "approved" | "published";

export interface AdminCourseItem {
  id: string;
  title: string;
  course_type: "internal" | "nssta_programme_listing";
  content_origin: "synthetic" | "official_source" | "provider";
  provider_organisation: string;
  difficulty: Difficulty | null;
  state: CourseState;
  review_status: string;
  lesson_count: number;
  is_demo: boolean;
  published_at: string | null;
  updated_at: string;
}

export interface AdminCourseList {
  items: AdminCourseItem[];
  total: number;
  state_counts: Record<CourseState, number>;
}

export interface AdminLesson {
  id: string;
  position: number;
  title: string;
  lesson_type: "reading" | "worked_example" | "practice_check";
  estimated_minutes: number;
  status: "active" | "inactive";
  body_markdown: string | null;
}

export interface AdminCourseDetail {
  id: string;
  row_version: number;
  title: string;
  description: string | null;
  course_type: AdminCourseItem["course_type"];
  content_origin: AdminCourseItem["content_origin"];
  provider_organisation: string;
  duration_days: number | null;
  difficulty: Difficulty | null;
  learning_objectives: string[];
  completion_criteria: string | null;
  state: CourseState;
  review_status: string;
  status: string;
  published_at: string | null;
  is_demo: boolean;
  source: { attribution: string; url: string; verified: boolean; licence_notes: string } | null;
  modules: { id: string; position: number; title: string; summary: string | null; status: string; lessons: AdminLesson[] }[];
  competencies: { id: string; competency: { id: string; code: string; name: string }; relevance: "primary" | "secondary"; status: string }[];
  guards: { checks: { id: string; label: string; passed: boolean }[]; can_submit: boolean; can_publish: boolean };
  reviews: ReviewHistoryItem[];
  open_task_id: string | null;
  actions: { can_edit: boolean; can_submit: boolean; can_withdraw: boolean; can_publish: boolean; can_unpublish: boolean };
}

export interface CompetencyStructure {
  frameworks: {
    id: string;
    code: string;
    name: string;
    status: string;
    version_label: string;
    definitions_restricted: boolean;
    is_demo: boolean;
    level_count: number;
    competencies: { id: string; code: string; name: string; status: string; description: string | null; approved_questions: number }[];
  }[];
  job_roles: {
    id: string;
    code: string | null;
    name: string;
    status: string;
    is_demo: boolean;
    requirements: { competency: { id: string; code: string; name: string }; required_level: number; status: string; mapping_version: number }[];
  }[];
}

export interface AssessmentOverview {
  id: string;
  title: string;
  purpose: string;
  status: string;
  published_at: string | null;
  feedback_policy: string;
  job_role: { id: string; name: string } | null;
  item_count: number;
  demo_seed_items: number;
  coverage: { competency: { id: string; code: string; name: string }; items: number }[];
  checks: { id: string; label: string; passed: boolean; detail: string | null }[];
  publishable: boolean;
  is_demo: boolean;
}

export interface AuditEntry {
  id: number;
  occurred_at: string;
  actor: string;
  actor_roles: string[];
  action: string;
  target_type: string;
  target_id: string | null;
  outcome: "success" | "denied" | "failure";
  before: Record<string, unknown> | null;
  after: Record<string, unknown> | null;
  reason: string | null;
  correlation_id: string;
}

export interface AuditPage {
  items: AuditEntry[];
  next_before_id: number | null;
  action_groups: string[];
}
