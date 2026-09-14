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
  is_demo: boolean;
}

export interface Level {
  level_number: number;
  label: string;
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
    course: { id: string; title: string; course_type: string; provider_organisation: string; duration_days: number | null; description: string | null; is_demo: boolean };
    score: string;
    reasons: RecommendationReason[];
    provenance: { source: string; data_status: string; review_status: string; is_demo: boolean };
  }[];
  gaps_without_approved_content: string[];
  igot: { included: boolean; reason: string };
}
