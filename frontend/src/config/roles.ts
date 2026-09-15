/** Display names for access roles and capabilities. Authorisation itself lives in backend/app/modules/identity/policy.py. */

export const ROLE_LABELS: Record<string, string> = {
  learner: "Learner",
  trainer: "Trainer",
  department_admin: "Department administrator",
  org_admin: "Organisation administrator",
  competency_admin: "Competency administrator",
  training_manager: "Training manager",
  auditor: "Auditor",
  platform_admin: "Platform administrator",
};

export const ROLE_ORDER = Object.keys(ROLE_LABELS);

export function roleLabel(role: string): string {
  return ROLE_LABELS[role] ?? role.replace(/_/g, " ");
}

export const CAPABILITY_GROUPS: { label: string; items: { id: string; label: string }[] }[] = [
  {
    label: "People",
    items: [
      { id: "users.view", label: "View users" },
      { id: "users.manage", label: "Manage users" },
      { id: "roles.assign", label: "Assign access roles" },
      { id: "departments.manage", label: "Manage departments" },
    ],
  },
  {
    label: "Competency structure",
    items: [
      { id: "job_roles.manage", label: "Manage job roles" },
      { id: "frameworks.view", label: "View frameworks" },
      { id: "frameworks.manage", label: "Manage frameworks" },
    ],
  },
  {
    label: "Content",
    items: [
      { id: "questions.author", label: "Author questions" },
      { id: "questions.review", label: "Review questions" },
      { id: "assessments.manage", label: "Manage assessments" },
      { id: "courses.manage", label: "Manage courses" },
      { id: "courses.review", label: "Review courses" },
      { id: "sources.view", label: "View sources" },
    ],
  },
  {
    label: "Insight and governance",
    items: [
      { id: "insight.view", label: "Aggregated insight" },
      { id: "audit.view", label: "Audit trail" },
    ],
  },
];

export const USER_STATUS: Record<string, { label: string; tone: "success" | "warning" | "neutral" | "danger" }> = {
  active: { label: "Active", tone: "success" },
  invited: { label: "Invited", tone: "warning" },
  locked: { label: "Locked", tone: "danger" },
  inactive: { label: "Inactive", tone: "neutral" },
};
