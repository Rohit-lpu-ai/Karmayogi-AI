import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import { setCsrfToken } from "@/api/client";
import type { AttemptResult } from "@/api/types";
import { AuthProvider } from "@/auth/AuthContext";
import { mockFetch } from "@/test/fetchMock";
import { gaps, recommendations, session } from "@/test/fixtures";

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

const [c2, c1] = gaps.items.map((g) => g.competency);
const result: AttemptResult = {
  attempt_id: "attempt-1",
  status: "scored",
  scored_at: "2026-09-15T10:00:00Z",
  score_total: "0.64286",
  is_baseline: true,
  feedback_policy: "correctness_and_explanations",
  assessment: { id: "assessment-1", title: "DEMO - Baseline assessment (synthetic arithmetic items)", is_demo: true },
  competencies: [
    { competency: c1, score: "1.00000", level_number: 4, evidence_band: "medium", evidence_count: 5, thresholds_status: "provisional", method_version: "score-v1" },
    { competency: c2, score: "0.28571", level_number: 1, evidence_band: "medium", evidence_count: 5, thresholds_status: "provisional", method_version: "score-v1" },
  ],
  questions: [
    { question_version_id: "qv-1", position: 1, stem: "What is 25% of 200?", competency_id: c2.id, selected_option_id: "opt-a", is_correct: false, correct_option_id: "opt-c", explanation: "0.25 x 200 = 50." },
    { question_version_id: "qv-2", position: 2, stem: "What is the mean of 4, 8 and 12?", competency_id: c1.id, selected_option_id: "opt-b", is_correct: true, correct_option_id: "opt-b", explanation: "24 / 3 = 8." },
    { question_version_id: "qv-3", position: 3, stem: "What is the range of 12, 5, 20 and 9?", competency_id: c1.id, selected_option_id: null, is_correct: false, correct_option_id: "opt-r", explanation: "20 - 5 = 15." },
  ],
  notice: "Development guidance only - not an appraisal or eligibility decision.",
};
const attemptView = {
  id: "attempt-1", status: "scored", started_at: "", submitted_at: "", answered_count: 2, question_count: 3,
  assessment: { id: "assessment-1", title: result.assessment.title, purpose: "pre", feedback_policy: result.feedback_policy, is_demo: true },
  questions: [
    { question_version_id: "qv-1", position: 1, stem: "", difficulty: "foundational", competency: c2, is_demo: true, selected_option_id: "opt-a", options: [{ id: "opt-a", label: "A", text: "25" }, { id: "opt-c", label: "C", text: "50" }] },
    { question_version_id: "qv-2", position: 2, stem: "", difficulty: "foundational", competency: c1, is_demo: true, selected_option_id: "opt-b", options: [{ id: "opt-b", label: "B", text: "8" }] },
    { question_version_id: "qv-3", position: 3, stem: "", difficulty: "intermediate", competency: c1, is_demo: true, selected_option_id: null, options: [{ id: "opt-r", label: "C", text: "15" }] },
  ],
};
const requirements = {
  job_role: gaps.job_role,
  requirements: [c1, c2].map((competency) => ({
    competency, required_level: 3, mapping_version: 1,
    levels: [0, 0.4, 0.6, 0.8].map((min, i) => ({ level_number: i + 1, label: `Level ${i + 1}`, min_score: String(min), threshold_status: "provisional" })),
  })),
};
const routes = {
  "GET /api/v1/auth/session": { body: session },
  "GET /api/v1/attempts/attempt-1/result": { body: result },
  "GET /api/v1/attempts/attempt-1": { body: attemptView },
  "GET /api/v1/me/competency-gaps": { body: gaps },
  "GET /api/v1/me/recommendations": { body: recommendations },
  "GET /api/v1/job-roles/role-1/competencies": { body: requirements },
};

describe("result page", () => {
  it("leads with the outcome in plain language and labels it as development guidance", async () => {
    mockFetch(routes);
    renderAt("/attempts/attempt-1/result");
    expect(await screen.findByRole("heading", { level: 1, name: "Your baseline result" })).toBeTruthy();
    expect(screen.getByRole("img", { name: "Overall score 64 out of 100" })).toBeTruthy();
    expect(screen.getByText("1 of 3 questions correct")).toBeTruthy();
    expect(screen.getByText("Development guidance, not an appraisal")).toBeTruthy();
    expect(screen.getAllByText("DEMO - synthetic").length).toBeGreaterThan(0);
    const meaning = screen.getByRole("region", { name: "What this means" });
    expect(await within(meaning).findByText("1 of 2 competencies is below the level your role requires. Start your learning there.")).toBeTruthy();
  });

  it("shows each competency with estimated and required level, evidence and status", async () => {
    mockFetch(routes);
    renderAt("/attempts/attempt-1/result");
    const section = await screen.findByRole("region", { name: "Result by competency" });
    const cards = await within(section).findAllByRole("listitem");
    const developing = cards.find((card) => card.textContent?.includes("Percentages"))!;
    expect(await within(developing).findByText("Developing")).toBeTruthy();
    expect(within(developing).getByText("2 levels below what your role requires. Learning suggestions focus here.")).toBeTruthy();
    expect(within(developing).getByRole("img", { name: /estimated level 1 of 4, required level 3/ })).toBeTruthy();
    expect(within(developing).getByText("Medium evidence (5 questions)")).toBeTruthy();
    const strength = cards.find((card) => card.textContent?.includes("Descriptive"))!;
    expect(within(strength).getByText("Meets requirement")).toBeTruthy();
  });

  it("gives next steps linking to gaps, recommended learning and answer review", async () => {
    mockFetch(routes);
    renderAt("/attempts/attempt-1/result");
    const steps = await screen.findByRole("region", { name: "What to do next" });
    expect(within(steps).getByRole("link", { name: "View competency gaps" }).getAttribute("href")).toBe("/competencies/gaps");
    expect(within(steps).getByRole("link", { name: "See recommended learning" }).getAttribute("href")).toBe("/courses");
    expect(within(steps).getByRole("link", { name: "Review your answers" }).getAttribute("href")).toBe("#question-review");
    expect(await within(steps).findByText("DEMO - Percentages refresher (synthetic course)")).toBeTruthy();
    expect(within(steps).getByText(/Helps with DEMO - Percentages and proportions/)).toBeTruthy();
  });

  it("reviews answers with the answer text and keeps the method in a closed disclosure", async () => {
    mockFetch(routes);
    renderAt("/attempts/attempt-1/result");
    const review = await screen.findByRole("region", { name: "Your answers" });
    expect(within(review).getByText("Not correct")).toBeTruthy();
    expect(within(review).getByText("Correct")).toBeTruthy();
    expect(within(review).getAllByText("Not answered").length).toBeGreaterThan(0);
    expect(await within(review).findByText("25")).toBeTruthy(); // your answer text from the attempt view
    expect(within(review).getByText("50")).toBeTruthy(); // correct answer text

    // Developer details are not on the page until the learner asks for them
    expect(document.body.textContent).not.toMatch(/score-v1|rec-v1|gap_rule|foundational 1, intermediate/);
    const trigger = screen.getByRole("button", { name: "How was this calculated?" });
    expect(trigger.getAttribute("aria-expanded")).toBe("false");
    await userEvent.setup().click(trigger);
    expect(screen.getByText(/foundational 1, intermediate 1.5, advanced 2/)).toBeTruthy();
    expect(screen.getByText(/Level 2 from 40/)).toBeTruthy();
    expect(screen.getByText(/Method version: score-v1/)).toBeTruthy();
    expect(document.body.textContent).not.toMatch(/weak|failed|poor/i);
  });

  it("keeps the result usable when recommendations fail", async () => {
    mockFetch({
      ...routes,
      "GET /api/v1/me/recommendations": { status: 500, body: { code: "INTERNAL_ERROR", title: "x", detail: "Something went wrong.", correlation_id: "corr-r" } },
    });
    renderAt("/attempts/attempt-1/result");
    const steps = await screen.findByRole("region", { name: "What to do next" });
    expect(await within(steps).findByText("Something went wrong.")).toBeTruthy();
    expect(screen.getByRole("img", { name: "Overall score 64 out of 100" })).toBeTruthy();
  });

  it("explains when a result is not available", async () => {
    mockFetch({
      ...routes,
      "GET /api/v1/attempts/attempt-1/result": { status: 409, body: { code: "ATTEMPT_NOT_SCORED", title: "Result not available", detail: "Submit the attempt to see its result." } },
    });
    renderAt("/attempts/attempt-1/result");
    expect(await screen.findByText("Submit the attempt to see its result.")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Back to the assessment" })).toBeTruthy();
  });
});
