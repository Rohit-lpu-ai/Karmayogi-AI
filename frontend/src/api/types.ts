// Response shapes of the vertical slice endpoints (backend/app/modules/*/api.py).
// Decimal values arrive as strings.

export interface JobRoleRef {
  id: string;
  name: string;
  code: string | null;
  is_demo: boolean;
}

export interface JobRole extends JobRoleRef {
  description: string | null;
}

export interface Me {
  id: string;
  email: string;
  display_name: string;
  designation: string | null;
  organization_id: string;
  access_roles: string[];
  can_take_assessments: boolean;
  job_role: JobRoleRef | null;
  notice: { notice_type: string; version: string; status: string; text: string; acknowledged_at: string | null };
  is_synthetic: boolean;
  registration_id?: string | null;
  department?: DepartmentRef | null;
  must_change_password?: boolean;
  /** Administrative capabilities from the server policy. Used only to choose navigation; the API enforces access. */
  admin_capabilities?: string[];
  last_login_at?: string | null;
}

export interface DepartmentRef {
  id: string;
  name: string;
  code: string | null;
}

export interface EnvironmentInfo {
  synthetic_data: boolean;
  self_registration_enabled: boolean;
}

export interface RegistrationOptions {
  enabled: boolean;
  organization_name: string | null;
  departments: { id: string; name: string }[];
  job_roles: { id: string; name: string }[];
}

export interface RoleAssignment {
  role: string;
  department_scope_id: string | null;
}

export interface AdminUser {
  id: string;
  display_name: string;
  email: string;
  registration_id: string | null;
  designation: string | null;
  status: "invited" | "active" | "locked" | "inactive";
  department: DepartmentRef | null;
  job_role: { id: string; name: string } | null;
  roles: RoleAssignment[];
  is_synthetic: boolean;
  has_password: boolean;
  last_login_at: string | null;
  created_at: string;
  row_version: number;
}

export interface AdminUserPage {
  items: AdminUser[];
  total: number;
  page: number;
  page_size: number;
}

export interface PasswordLink {
  purpose: "account_setup" | "password_reset";
  token: string;
  expires_at: string;
}

export interface AdminDepartment {
  id: string;
  name: string;
  code: string | null;
  status: string;
  user_count: number;
}

export interface AdminRole {
  role: string;
  label: string;
  description: string;
  capabilities: string[];
  user_count: number;
  department_scoped: boolean;
}

export interface SessionInfo {
  csrf_token: string;
  idle_expires_at: string;
  absolute_expires_at: string;
  user: Me;
}

export interface CompetencyRef {
  id: string;
  code: string;
  name: string;
  framework_code: string;
  framework_status: string;
  /** Plain-language description; always null for licence-restricted frameworks. */
  description?: string | null;
  is_demo: boolean;
}

export interface Level {
  level_number: number;
  label: string;
  description?: string | null;
  min_score: string | null;
  threshold_status: string;
}

export interface JobRoleCompetencies {
  job_role: JobRole;
  requirements: { competency: CompetencyRef; required_level: number; mapping_version: number; levels: Level[] }[];
}

export interface AssessmentSummary {
  id: string;
  title: string;
  purpose: string;
  feedback_policy: string;
  question_count: number;
  is_demo: boolean;
  latest_attempt: { id: string; status: string } | null;
}

export interface DeliveredQuestion {
  question_version_id: string;
  position: number;
  stem: string;
  difficulty: string;
  competency: CompetencyRef;
  is_demo: boolean;
  options: { id: string; label: string; text: string }[];
  selected_option_id: string | null;
}

export interface Attempt {
  id: string;
  status: string;
  started_at: string;
  submitted_at: string | null;
  assessment: { id: string; title: string; purpose: string; feedback_policy: string; is_demo: boolean };
  questions: DeliveredQuestion[];
  answered_count: number;
  question_count: number;
}

export interface SubmitResponse {
  attempt_id: string;
  status: string;
  score_total: string;
  is_baseline: boolean;
  result_url: string;
}

export interface AttemptResult {
  attempt_id: string;
  status: string;
  scored_at: string;
  score_total: string;
  is_baseline: boolean;
  feedback_policy: string;
  assessment: { id: string; title: string; is_demo: boolean };
  competencies: {
    competency: CompetencyRef;
    score: string | null;
    level_number: number | null;
    evidence_band: string;
    evidence_count: number;
    thresholds_status: string;
    method_version: string;
  }[];
  questions: {
    question_version_id: string;
    position: number;
    stem: string;
    competency_id: string;
    selected_option_id: string | null;
    is_correct: boolean | null;
    correct_option_id: string | null;
    explanation: string | null;
  }[];
  notice: string;
}

export type GapStatus = "gap" | "meets_requirement" | "insufficient_evidence" | "not_assessed" | "level_unavailable";

export interface GapItem {
  competency: CompetencyRef;
  required_level: number;
  estimated_level: number | null;
  score: string | null;
  evidence_band: string | null;
  evidence_count: number;
  status: GapStatus;
  gap: number | null;
  max_level_span: number;
}

export interface Gaps {
  job_role: JobRole;
  method_version: string;
  gap_rule: string;
  items: GapItem[];
  summary: Record<GapStatus, number>;
}

export interface ProfileItem {
  competency: CompetencyRef;
  score: string | null;
  level_number: number | null;
  evidence_band: string;
  evidence_count: number;
  method_version: string;
  computed_at: string;
  explanation: { formula: string; limitations: string[]; thresholds_status: string; band_rule: string; items: unknown[] };
}

export interface Profile {
  method_version: string;
  items: ProfileItem[];
}

export interface RecommendationReason {
  rule: string;
  competency_code?: string;
  competency_name?: string;
  required?: number;
  estimated?: number;
  gap?: number;
  relevance?: string;
}

export interface Recommendations {
  rule_version: string;
  rule: string;
  job_role: JobRole;
  items: {
    rank: number;
    course: {
      id: string;
      title: string;
      course_type: string;
      provider_organisation: string;
      duration_days: number | null;
      description: string | null;
      difficulty?: CourseDifficulty | null;
      learning_objectives?: string[];
      is_demo: boolean;
    };
    score: string;
    reasons: RecommendationReason[];
    provenance: { source: string; data_status: string; review_status: string; is_demo: boolean };
  }[];
  gaps_without_approved_content: string[];
  igot: { included: boolean; reason: string };
}

export type CourseDifficulty = "foundational" | "intermediate" | "advanced";

export interface AttemptHistoryItem {
  id: string;
  status: string;
  started_at: string;
  submitted_at: string | null;
  scored_at: string | null;
  score_total: string | null;
  is_baseline: boolean;
  assessment: { id: string; title: string; purpose: string; is_demo: boolean };
}

export interface CourseCompetencyItem {
  competency: CompetencyRef;
  relevance: "primary" | "secondary";
  your_status?: { status: GapStatus; required_level: number; estimated_level: number | null; gap: number | null; evidence_band: string | null } | null;
}

export interface CourseSummary {
  id: string;
  title: string;
  description: string | null;
  provider_organisation: string;
  course_type: string;
  duration_days: number | null;
  difficulty: CourseDifficulty | null;
  learning_objectives: string[];
  competencies: CourseCompetencyItem[];
  recommendation: { rank: number; reasons: RecommendationReason[] } | null;
  addresses_your_gaps: { competency_id: string; competency_name: string; required_level: number; estimated_level: number | null; gap: number | null }[];
  is_demo: boolean;
  provenance: { data_status: string; review_status: string; is_demo: boolean };
  content_origin?: ContentOrigin;
  lessons?: { lesson_count: number; module_count: number; total_minutes: number };
  /** The caller's own progress; null for roles without learning features. */
  your_progress?: { status: ProgressStatus; completed_lessons: number; percent: number; resume_lesson: LessonRef | null } | null;
}

export type ContentOrigin = "synthetic" | "official_source" | "provider";
export type ProgressStatus = "not_started" | "in_progress" | "completed";

export interface LessonRef {
  id: string;
  title: string;
}

export interface CourseProgress {
  lesson_count: number;
  total_minutes: number;
  module_count: number;
  completed_lessons: number;
  percent: number;
  status: ProgressStatus;
  started_at: string | null;
  completed_at: string | null;
  resume_lesson: LessonRef | null;
}

export interface LearningCourseRef {
  id: string;
  title: string;
  difficulty: CourseDifficulty | null;
  duration_days: number | null;
  content_origin: ContentOrigin;
  completion_criteria: string | null;
  is_demo: boolean;
  description?: string | null;
}

export type LessonType = "reading" | "worked_example" | "practice_check";

export interface CourseOutline {
  course: LearningCourseRef;
  modules: { id: string; position: number; title: string; summary: string | null; lessons: { id: string; position: number; title: string; lesson_type: LessonType; estimated_minutes: number; status: ProgressStatus }[] }[];
  progress: CourseProgress;
  prerequisites: { id: string; title: string; status: ProgressStatus }[];
}

export interface LessonDetail {
  id: string;
  title: string;
  lesson_type: LessonType;
  estimated_minutes: number;
  content_kind: string;
  body_markdown: string | null;
  module: { id: string; title: string; position: number };
  position: number;
  lesson_count: number;
  status: ProgressStatus;
  previous: LessonRef | null;
  next: LessonRef | null;
  course: LearningCourseRef;
  content_notice: string | null;
}

export interface LessonProgressResult {
  lesson_id: string;
  lesson_status: ProgressStatus;
  course_progress: CourseProgress;
  next: LessonRef | null;
}

export interface ProgressItem {
  course: LearningCourseRef;
  progress: CourseProgress;
  last_activity_at: string;
}

export interface MyProgress {
  in_progress: ProgressItem[];
  completed: ProgressItem[];
  totals: { courses_started: number; courses_completed: number; lessons_completed: number };
  note: string;
}

export interface PathItem {
  id: string;
  position: number;
  item_type: "course" | "no_content_placeholder";
  course: LearningCourseRef | null;
  progress: CourseProgress | null;
  status: ProgressStatus;
  reasons: Record<string, unknown>[];
}

export interface LearningPath {
  id: string;
  rule_version: string;
  rule: string;
  generated_at: string;
  job_role: JobRole;
  state: "ready" | "assessment_needed" | "no_gaps";
  summary: { courses: number; completed: number; in_progress: number; total_minutes: number; gaps_without_content: number };
  groups: { competency: { id: string; code: string | null; name: string | null }; required_level: number | null; estimated_level: number | null; gap: number | null; items: PathItem[] }[];
  completed_earlier: PathItem[];
  note: string;
}

export interface Catalogue {
  items: CourseSummary[];
  total: number;
  filters: { competencies: (CompetencyRef & { course_count: number })[]; difficulties: CourseDifficulty[]; sorts: string[] };
  has_learning_context: boolean;
}

export interface CourseDetail extends CourseSummary {
  related_courses: { id: string; title: string; difficulty: CourseDifficulty | null; duration_days: number | null; is_demo: boolean; is_recommended: boolean }[];
  learning_content: { available: boolean; reason: string | null };
  prerequisites?: { id: string; title: string }[];
  completion_criteria?: string | null;
}
