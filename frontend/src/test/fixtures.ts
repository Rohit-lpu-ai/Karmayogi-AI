import type { Attempt, Gaps, Me, Profile, Recommendations } from "../api/types";

const demoCompetency = (code: string, name: string) => ({
  id: `id-${code}`,
  code,
  name,
  framework_code: "DEMO-FUNCTIONAL",
  framework_status: "draft",
  is_demo: true,
});

export const me: Me = {
  id: "user-1",
  email: "learner01@example.invalid",
  display_name: "Demo Learner 01",
  designation: null,
  organization_id: "org-1",
  access_roles: ["learner"],
  can_take_assessments: true,
  job_role: { id: "role-1", name: "DEMO - Statistical Assistant (synthetic role)", code: "DEMO-ROLE-STAT-ASSISTANT", is_demo: true },
  notice: { notice_type: "privacy_ai_use", version: "privacy-ai-use-draft-0", status: "draft", text: "DRAFT NOTICE", acknowledged_at: "2026-09-15T00:00:00Z" },
  is_synthetic: true,
};

export const session = { csrf_token: "csrf-abc", idle_expires_at: "", absolute_expires_at: "", user: me };

export const gaps: Gaps = {
  job_role: { ...me.job_role!, description: null },
  method_version: "score-v1",
  gap_rule: "gap = required level - estimated level, shown only when evidence band is medium or high",
  items: [
    { competency: demoCompetency("DEMO-C2", "DEMO - Percentages and proportions (synthetic)"), required_level: 3, estimated_level: 1, score: "0.28571", evidence_band: "medium", evidence_count: 5, status: "gap", gap: 2, max_level_span: 3 },
    { competency: demoCompetency("DEMO-C1", "DEMO - Descriptive statistics (synthetic)"), required_level: 3, estimated_level: 4, score: "1.00000", evidence_band: "medium", evidence_count: 5, status: "meets_requirement", gap: 0, max_level_span: 3 },
  ],
  summary: { gap: 1, meets_requirement: 1, insufficient_evidence: 0, not_assessed: 0, level_unavailable: 0 },
};

export const recommendations: Recommendations = {
  rule_version: "rec-v1",
  rule: "score = ...",
  job_role: gaps.job_role,
  items: [
    {
      rank: 1,
      course: { id: "course-2", title: "DEMO - Percentages refresher (synthetic course)", course_type: "internal", provider_organisation: "DEMO provider (synthetic)", duration_days: 1, description: null, is_demo: true },
      score: "0.66667",
      reasons: [
        { rule: "gap_match", competency_code: "DEMO-C2", competency_name: "DEMO - Percentages and proportions (synthetic)", required: 3, estimated: 1, gap: 2 },
        { rule: "mapping", relevance: "primary" },
      ],
      provenance: { source: "internal_catalogue", data_status: "ASSUMED", review_status: "approved", is_demo: true },
    },
  ],
  gaps_without_approved_content: [],
  igot: { included: false, reason: "No iGOT integration: mock source not enabled in this slice" },
};

export const profile: Profile = { method_version: "score-v1", items: [] };

export const attempt: Attempt = {
  id: "attempt-1",
  status: "in_progress",
  started_at: "2026-09-15T00:00:00Z",
  submitted_at: null,
  assessment: { id: "assessment-1", title: "DEMO - Baseline assessment (synthetic arithmetic items)", purpose: "pre", feedback_policy: "correctness_and_explanations", is_demo: true },
  questions: [
    {
      question_version_id: "qv-1",
      position: 1,
      stem: "What is 25% of 200?",
      difficulty: "foundational",
      competency: demoCompetency("DEMO-C2", "DEMO - Percentages and proportions (synthetic)"),
      is_demo: true,
      options: [
        { id: "opt-a", label: "A", text: "25" },
        { id: "opt-c", label: "C", text: "50" },
      ],
      selected_option_id: null,
    },
  ],
  answered_count: 0,
  question_count: 1,
};
