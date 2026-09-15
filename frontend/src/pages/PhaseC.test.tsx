import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import { setCsrfToken } from "@/api/client";
import type { Catalogue, CourseDetail, CourseSummary, GapItem, Gaps, Recommendations } from "@/api/types";
import { AuthProvider } from "@/auth/AuthContext";
import { mockFetch } from "@/test/fetchMock";
import { me, session } from "@/test/fixtures";

afterEach(() => {
  cleanup();
  setCsrfToken(null);
  vi.unstubAllGlobals();
});

function renderAt(path: string) {
  return render(
    <MemoryRouter initialEntries={[path]}>
      <AuthProvider>
        <Routes>
          <Route path="*" element={<App />} />
        </Routes>
      </AuthProvider>
    </MemoryRouter>,
  );
}

const comp = (code: string, name: string, description = `${name} matters in statistical work.`) => ({
  id: `id-${code}`, code, name, framework_code: "DEMO-STAT-PRACTICE", framework_status: "draft", description, is_demo: true,
});
const TABLES = comp("DEMO-SP-TABLES", "DEMO - Reading statistical tables (synthetic)");
const RATES = comp("DEMO-SP-RATES", "DEMO - Rates, ratios and percentage change (synthetic)");
const DESC = comp("DEMO-SP-DESC", "DEMO - Descriptive statistics (synthetic)");
const QUAL = comp("DEMO-SP-QUALITY", "DEMO - Data quality and validation (synthetic)");
const gap = (competency: typeof TABLES, required: number, estimated: number | null, status: GapItem["status"], gapSize: number | null, band: string | null = "medium"): GapItem => ({
  competency, required_level: required, estimated_level: estimated, score: estimated === null ? null : "0.2", evidence_band: band,
  evidence_count: band ? 5 : 0, status, gap: gapSize, max_level_span: 3,
});
const role = { id: "role-1", name: "DEMO - Junior Statistical Officer (synthetic role)", code: "DEMO-ROLE-JSO", description: null, is_demo: true };
const gapsScored: Gaps = {
  job_role: role, method_version: "score-v1", gap_rule: "x",
  items: [gap(TABLES, 3, 1, "gap", 2), gap(RATES, 3, 2, "gap", 1), gap(DESC, 3, 4, "meets_requirement", 0), gap(QUAL, 2, 1, "insufficient_evidence", null, "low")],
  summary: { gap: 2, meets_requirement: 1, insufficient_evidence: 1, not_assessed: 0, level_unavailable: 0 },
};
const gapsNotAssessed: Gaps = { ...gapsScored, items: gapsScored.items.map((g) => ({ ...g, estimated_level: null, evidence_band: null, evidence_count: 0, status: "not_assessed", gap: null })), summary: { gap: 0, meets_requirement: 0, insufficient_evidence: 0, not_assessed: 4, level_unavailable: 0 } };
const levels = [1, 2, 3, 4].map((n) => ({ level_number: n, label: `Level ${n} - ${["Foundation", "Working", "Proficient", "Advanced"][n - 1]}`, description: `Level ${n} description.`, min_score: String((n - 1) * 0.2), threshold_status: "provisional" }));
const requirements = { job_role: role, requirements: [TABLES, RATES, DESC, QUAL].map((c) => ({ competency: c, required_level: 3, mapping_version: 1, levels })) };
const tablesCourse = { id: "course-tables", title: "DEMO - Reading statistical tables critically (synthetic course)", course_type: "internal", provider_organisation: "DEMO provider (synthetic)", duration_days: 1, description: "Read tables well.", difficulty: "foundational" as const, learning_objectives: ["Identify units"], is_demo: true };
const recs: Recommendations = {
  rule_version: "rec-v1", rule: "x", job_role: role, gaps_without_approved_content: [], igot: { included: false, reason: "x" },
  items: [{ rank: 1, course: tablesCourse, score: "0.66", reasons: [{ rule: "gap_match", competency_code: "DEMO-SP-TABLES", competency_name: TABLES.name, required: 3, estimated: 1, gap: 2 }, { rule: "mapping", relevance: "primary" }], provenance: { source: "internal_catalogue", data_status: "ASSUMED", review_status: "approved", is_demo: true } }],
};
const jsoSession = { ...session, user: { ...me, job_role: { id: "role-1", name: role.name, code: role.code, is_demo: true } } };
const scoredAssessment = [{ id: "a-1", title: "DEMO - Baseline assessment: Junior Statistical Officer (synthetic)", purpose: "pre", feedback_policy: "correctness_and_explanations", question_count: 20, is_demo: true, latest_attempt: { id: "att-1", status: "scored" } }];
const history = [{ id: "att-1", status: "scored", started_at: "2026-09-15T08:00:00Z", submitted_at: "2026-09-15T08:20:00Z", scored_at: "2026-09-15T08:20:00Z", score_total: "0.45", is_baseline: true, assessment: { id: "a-1", title: scoredAssessment[0].title, purpose: "pre", is_demo: true } }];
const learnerRoutes = {
  "GET /api/v1/auth/session": { body: jsoSession },
  "GET /api/v1/assessments": { body: scoredAssessment },
  "GET /api/v1/me/competency-gaps": { body: gapsScored },
  "GET /api/v1/me/recommendations": { body: recs },
  "GET /api/v1/me/attempts": { body: history },
  "GET /api/v1/job-roles/role-1/competencies": { body: requirements },
  "GET /api/v1/me/competency-profile": { body: { method_version: "score-v1", items: [{ competency: TABLES, score: "0.2", level_number: 1, evidence_band: "medium", evidence_count: 5, method_version: "score-v1", computed_at: "", explanation: { formula: "", limitations: [], thresholds_status: "provisional", band_rule: "", items: [{ correct: true }, { correct: false }, { correct: false }, { correct: false }, { correct: true }] } }] } },
};

// --- Login -----------------------------------------------------------------------------------------

describe("login", () => {
  const signedOut = { "GET /api/v1/auth/session": { status: 401, body: { code: "UNAUTHENTICATED", title: "x" } } };

  it("explains the product and shows no sign-up when registration is closed", async () => {
    mockFetch({ ...signedOut, "GET /api/v1/environment": { body: { synthetic_data: true, self_registration_enabled: false } } });
    renderAt("/login");
    expect(await screen.findByRole("heading", { level: 1, name: "Sign in" })).toBeTruthy();
    expect(screen.getByRole("heading", { level: 2, name: /Know what your role needs/ })).toBeTruthy();
    expect(await screen.findByText(/Forgot your password\? Ask your administrator/)).toBeTruthy();
    expect(screen.queryByRole("link", { name: /sign up|register|create .*account/i })).toBeNull();
    expect(screen.getByRole("note", { name: "Demo environment" })).toBeTruthy();
  });

  it("offers learner registration only in learner mode, and states there is no administrator sign-up", async () => {
    mockFetch({ ...signedOut, "GET /api/v1/environment": { body: { synthetic_data: true, self_registration_enabled: true } } });
    renderAt("/login");
    const user = userEvent.setup();
    expect(await screen.findByRole("link", { name: "Create a learner account" })).toBeTruthy();
    await user.click(screen.getByRole("button", { name: "Administration" }));
    expect(screen.getByRole("button", { name: "Administration" }).getAttribute("aria-pressed")).toBe("true");
    expect(screen.queryByRole("link", { name: "Create a learner account" })).toBeNull();
    expect(screen.getByText(/There is no public sign-up for administration/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Sign in to administration" })).toBeTruthy();
  });

  it("validates before sending, focuses the error summary and toggles password visibility", async () => {
    const calls = mockFetch(signedOut);
    renderAt("/login");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Sign in" }));
    const summary = await screen.findByRole("alert");
    await waitFor(() => expect(document.activeElement).toBe(summary));
    expect(within(summary).getByText("Enter your email address.")).toBeTruthy();
    expect(screen.getByLabelText("Email").getAttribute("aria-invalid")).toBe("true");
    expect(calls.some((c) => c.method === "POST")).toBe(false);

    const password = screen.getByLabelText("Password") as HTMLInputElement;
    const toggle = screen.getByRole("button", { name: "Show password" });
    expect(password.type).toBe("password");
    await user.click(toggle);
    expect(password.type).toBe("text");
    expect(toggle.getAttribute("aria-pressed")).toBe("true");
  });

  it("shows a lockout message from the API", async () => {
    mockFetch({ ...signedOut, "POST /api/v1/auth/login": { status: 423, body: { code: "ACCOUNT_LOCKED", title: "Locked", detail: "Try again in 15 minutes.", correlation_id: "corr-l" } } });
    renderAt("/login");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("Email"), "learner01@example.invalid");
    await user.type(screen.getByLabelText("Password"), "secret-pass");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    const alert = await screen.findByRole("alert");
    expect(within(alert).getByText("This account is temporarily locked.")).toBeTruthy();
    expect(within(alert).getByText("Try again in 15 minutes.")).toBeTruthy();
  });
});

// --- Dashboard ------------------------------------------------------------------------------------------

describe("dashboard", () => {
  it("leads with the priority next action, the learning journey and plain counts (no readiness score)", async () => {
    mockFetch(learnerRoutes);
    renderAt("/");
    expect(await screen.findByRole("heading", { level: 1, name: `Welcome back, ${me.display_name}` })).toBeTruthy();
    expect(await screen.findByRole("heading", { name: "Develop Reading statistical tables" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Open your learning path" }).getAttribute("href")).toBe("/learning-path");

    const journey = screen.getByRole("navigation", { name: "Your learning journey" });
    expect(within(journey).getAllByText(/Later release/, { selector: ".sr-only" })).toHaveLength(1); // reassessment only
    expect(within(journey).getAllByText("Reassessment").length).toBe(1);

    expect(await screen.findByText("1 of 4")).toBeTruthy(); // at required level
    expect(document.body.textContent).not.toMatch(/readiness|% ready/i);
    const priority = screen.getByRole("region", { name: "Priority gaps" });
    expect(within(priority).getAllByRole("listitem")[0].textContent).toContain("Reading statistical tables");
    expect(within(priority).getByText("2 levels to go")).toBeTruthy();
    const recommended = screen.getByRole("region", { name: "Recommended learning" });
    expect(within(recommended).getByText(/your level in/)).toBeTruthy();
    expect(within(screen.getByRole("region", { name: "Recent assessment activity" })).getByText("Completed baseline assessment")).toBeTruthy();
  });

  it("asks a learner without a baseline to take it, and each card fails independently", async () => {
    mockFetch({
      ...learnerRoutes,
      "GET /api/v1/assessments": { body: [{ ...scoredAssessment[0], latest_attempt: null }] },
      "GET /api/v1/me/competency-gaps": { body: gapsNotAssessed },
      "GET /api/v1/me/recommendations": { status: 500, body: { code: "INTERNAL_ERROR", title: "x", detail: "Recommendations failed.", correlation_id: "c" } },
      "GET /api/v1/me/attempts": { body: [] },
    });
    renderAt("/");
    expect(await screen.findByRole("heading", { name: "Take your baseline assessment" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Start baseline assessment" }).getAttribute("href")).toBe("/assessment");
    expect(await within(screen.getByRole("region", { name: "Recommended learning" })).findByText("Recommendations failed.")).toBeTruthy();
    expect(within(screen.getByRole("region", { name: "Priority gaps" })).getByText("Start with a baseline assessment to see your gaps.")).toBeTruthy();
  });
});

// --- Competency profile and gaps ------------------------------------------------------------------------------

describe("competency profile", () => {
  it("shows each role competency with levels, evidence, meaning and an action", async () => {
    mockFetch(learnerRoutes);
    renderAt("/competencies");
    expect(await screen.findByRole("heading", { level: 1, name: "My competencies" })).toBeTruthy();
    expect(await screen.findByText("1 of 4 competencies are at the level your role requires.")).toBeTruthy();
    const list = screen.getByRole("region", { name: "Competencies for your role" });
    const tables = within(list).getAllByRole("listitem").find((li) => li.textContent?.includes("Reading statistical tables"))!;
    expect(within(tables).getByText("Developing")).toBeTruthy();
    expect(within(tables).getByText("2 levels below what your role requires.")).toBeTruthy();
    expect(await within(tables).findByText("2 of 5 questions answered correctly")).toBeTruthy();
    expect(within(tables).getByRole("link", { name: "See learning for this gap" }).getAttribute("href")).toBe("/competencies/gaps");
    expect(within(screen.getByRole("region", { name: "Assessment history" })).getByRole("link", { name: "View result" }).getAttribute("href")).toBe("/attempts/att-1/result");
    expect(document.body.textContent).not.toMatch(/score-v1/);
  });
});

describe("gap analysis", () => {
  it("prioritises gaps and explains level, why it matters and the recommended learning", async () => {
    mockFetch(learnerRoutes);
    renderAt("/competencies/gaps");
    expect(await screen.findByRole("heading", { level: 1, name: "Gap analysis" })).toBeTruthy();
    expect(await screen.findByText("2 of 4 competencies need development for your role.")).toBeTruthy();
    const priority = screen.getByRole("region", { name: "Priority gaps" });
    const cards = within(priority).getAllByRole("listitem").filter((li) => li.parentElement?.parentElement === priority);
    expect(cards[0].textContent).toContain("Reading statistical tables");
    expect(cards[1].textContent).toContain("Rates, ratios");
    expect(within(cards[0]).getByText("Where you are now")).toBeTruthy();
    expect(await within(cards[0]).findByText("Level 3 description.")).toBeTruthy();
    expect(within(cards[0]).getByText(TABLES.description)).toBeTruthy();
    expect(within(cards[0]).getByRole("link", { name: "Reading statistical tables critically" }).getAttribute("href")).toBe("/courses/course-tables");
    expect(within(cards[1]).getByText("No approved learning content matches this gap yet.")).toBeTruthy();
    expect(screen.getByRole("region", { name: "Strengths" })).toBeTruthy();
    expect(screen.getByRole("region", { name: "Needs more evidence" })).toBeTruthy();

    const user = userEvent.setup();
    await user.click(screen.getByRole("tab", { name: "Table" }));
    expect(screen.getByRole("table", { name: "Required and estimated level by competency" })).toBeTruthy();
    expect(screen.queryByText(/gap = required level/)).toBeNull(); // rule only inside the disclosure
  });

  it("invites a learner without evidence to take the baseline", async () => {
    mockFetch({ ...learnerRoutes, "GET /api/v1/me/competency-gaps": { body: gapsNotAssessed } });
    renderAt("/competencies/gaps");
    expect(await screen.findByText("Take the baseline assessment to see your gaps.")).toBeTruthy();
  });
});

// --- Courses -----------------------------------------------------------------------------------------------------

const summary = (overrides: Partial<CourseSummary>): CourseSummary => ({
  ...tablesCourse, course_type: "internal", learning_objectives: ["Identify units"], competencies: [{ competency: TABLES, relevance: "primary" }],
  recommendation: null, addresses_your_gaps: [], provenance: { data_status: "ASSUMED", review_status: "approved", is_demo: true }, ...overrides,
});
const catalogue: Catalogue = {
  items: [
    summary({ recommendation: { rank: 1, reasons: recs.items[0].reasons }, addresses_your_gaps: [{ competency_id: TABLES.id, competency_name: TABLES.name, required_level: 3, estimated_level: 1, gap: 2 }] }),
    summary({ id: "course-sampling", title: "DEMO - Survey sampling essentials (synthetic course)", difficulty: "intermediate", duration_days: 3, competencies: [{ competency: comp("DEMO-SP-SAMPLING", "DEMO - Sampling and survey design (synthetic)"), relevance: "primary" }] }),
  ],
  total: 2,
  filters: { competencies: [{ ...TABLES, course_count: 1 }], difficulties: ["foundational", "intermediate", "advanced"], sorts: ["recommended"] },
  has_learning_context: true,
};

describe("course catalogue", () => {
  it("lists courses with recommendation context, one catalogue notice and filters that query the API", async () => {
    const calls = mockFetch({
      ...learnerRoutes,
      "GET /api/v1/courses": { body: catalogue },
      "GET /api/v1/courses?difficulty=advanced": { body: { ...catalogue, items: [], total: 0 } },
    });
    renderAt("/courses");
    expect(await screen.findByRole("heading", { level: 1, name: "Course catalogue" })).toBeTruthy();
    expect(await screen.findByText("2 courses, 1 linked to your gaps")).toBeTruthy();
    const first = screen.getAllByRole("article")[0];
    expect(within(first).getByText("Top pick for you")).toBeTruthy();
    expect(within(first).getByText(/Helps close your gap in/)).toBeTruthy();
    expect(within(first).queryByText("DEMO")).toBeNull(); // one environment banner and one page notice instead (DEC-058)
    expect(screen.getByText(/This catalogue currently contains synthetic learning examples for product evaluation/)).toBeTruthy();

    const user = userEvent.setup();
    await user.selectOptions(screen.getByLabelText("Difficulty"), "advanced");
    expect(await screen.findByText("No courses match these filters.")).toBeTruthy();
    expect(calls.some((c) => c.url === "/api/v1/courses?difficulty=advanced")).toBe(true);
    await user.click(screen.getAllByRole("button", { name: "Clear filters" })[0]);
    expect(await screen.findByText("2 courses, 1 linked to your gaps")).toBeTruthy();
  });
});

describe("course detail", () => {
  const detail: CourseDetail = {
    ...catalogue.items[0],
    competencies: [{ competency: TABLES, relevance: "primary", your_status: { status: "gap", required_level: 3, estimated_level: 1, gap: 2, evidence_band: "medium" } }],
    related_courses: [{ id: "course-comm", title: "DEMO - Communicating statistics clearly (synthetic course)", difficulty: "foundational", duration_days: 2, is_demo: true, is_recommended: false }],
    learning_content: { available: false, reason: "This course has no lessons in the platform yet." },
  };

  it("explains why it is recommended, the gap it addresses, objectives and the honest lesson state", async () => {
    mockFetch({ ...learnerRoutes, "GET /api/v1/courses/course-tables": { body: detail } });
    renderAt("/courses/course-tables");
    expect(await screen.findByRole("heading", { level: 1, name: "Reading statistical tables critically" })).toBeTruthy();
    const why = screen.getByRole("region", { name: "Why this course is recommended for you" });
    expect(within(why).getByText(/Your estimated level is 1; your role requires level 3 \(2 levels to go\)/)).toBeTruthy();
    expect(within(screen.getByRole("region", { name: "What you will learn" })).getByText("Identify units")).toBeTruthy();
    expect(screen.getByText("No lessons yet")).toBeTruthy();
    expect(screen.queryByRole("link", { name: /Start course/ })).toBeNull(); // no dead-end call to action
    expect(screen.getByText("You: level 1 · role needs 3")).toBeTruthy();
    expect(screen.getByRole("link", { name: /Communicating statistics clearly/ }).getAttribute("href")).toBe("/courses/course-comm");
  });

  it("shows a clear message for an unavailable course", async () => {
    mockFetch({ ...learnerRoutes, "GET /api/v1/courses/missing": { status: 404, body: { code: "NOT_FOUND", title: "Not found", detail: "This course is not available." } } });
    renderAt("/courses/missing");
    expect(await screen.findByText("This course is not available.")).toBeTruthy();
    expect(screen.getByRole("link", { name: /Back to the catalogue/ })).toBeTruthy();
  });
});
