import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import { setCsrfToken } from "@/api/client";
import type { Attempt } from "@/api/types";
import { AuthProvider } from "@/auth/AuthContext";
import { mockFetch } from "@/test/fetchMock";
import { session } from "@/test/fixtures";

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

const competency = (code: string, name: string) => ({ id: `id-${code}`, code, name, framework_code: "DEMO-FUNCTIONAL", framework_status: "draft", is_demo: true });
const question = (n: number, stem: string, selected: string | null = null) => ({
  question_version_id: `qv-${n}`,
  position: n,
  stem,
  difficulty: "foundational",
  competency: competency("DEMO-C1", "DEMO - Descriptive statistics (synthetic)"),
  is_demo: true,
  options: ["A", "B", "C", "D"].map((label, i) => ({ id: `q${n}-opt-${label}`, label, text: `Option ${n}${label} (${i})` })),
  selected_option_id: selected,
});
const threeQuestions: Attempt = {
  id: "attempt-1",
  status: "in_progress",
  started_at: "2026-09-15T00:00:00Z",
  submitted_at: null,
  assessment: { id: "assessment-1", title: "DEMO - Baseline assessment (synthetic arithmetic items)", purpose: "pre", feedback_policy: "correctness_and_explanations", is_demo: true },
  questions: [question(1, "What is the mean of 4, 8 and 12?", "q1-opt-B"), question(2, "What is 25% of 200?"), question(3, "What is the median of 3, 9, 5?")],
  answered_count: 1,
  question_count: 3,
};
const summary = { id: "assessment-1", title: threeQuestions.assessment.title, purpose: "pre", feedback_policy: "correctness_and_explanations", question_count: 3, is_demo: true };
const requirements = {
  job_role: { ...session.user.job_role, description: null },
  requirements: [{ competency: competency("DEMO-C1", "DEMO - Descriptive statistics (synthetic)"), required_level: 3, mapping_version: 1, levels: [1, 2, 3, 4].map((n) => ({ level_number: n, label: `Level ${n}`, min_score: null, threshold_status: "provisional" })) }],
};
const base = {
  "GET /api/v1/auth/session": { body: session },
  "GET /api/v1/job-roles/role-1/competencies": { body: requirements },
};

describe("assessment introduction", () => {
  it("explains the assessment and starts an attempt on its own page", async () => {
    const calls = mockFetch({
      ...base,
      "GET /api/v1/assessments": { body: [{ ...summary, latest_attempt: null }] },
      "POST /api/v1/assessments/assessment-1/attempts": { status: 201, body: threeQuestions },
      "GET /api/v1/attempts/attempt-1": { body: threeQuestions },
      "PUT /api/v1/attempts/attempt-1/answers/qv-2": { body: { question_version_id: "qv-2", selected_option_id: "q2-opt-A", saved_at: "" } },
    });
    renderAt("/assessment");
    const user = userEvent.setup();
    expect(await screen.findByRole("heading", { level: 1, name: "Baseline assessment" })).toBeTruthy();
    expect(await screen.findByText("Not started")).toBeTruthy();
    expect(screen.getByText("Questions you leave unanswered are counted as not correct.")).toBeTruthy();
    expect(await screen.findByText("Your role requires level 3 of 4")).toBeTruthy();
    await user.click(screen.getByRole("button", { name: "Start assessment" }));
    expect(await screen.findByRole("heading", { level: 1, name: "Question 2 of 3" })).toBeTruthy(); // resumes at first unanswered
    await user.click(screen.getByRole("radio", { name: /Option 2A/ }));
    expect(screen.getByRole("heading", { level: 1, name: "Question 2 of 3" })).toBeTruthy(); // stays after answering
    expect(calls.find((c) => c.method === "POST")?.headers["X-CSRF-Token"]).toBe("csrf-abc");
  });

  it("offers the result when the assessment is completed", async () => {
    mockFetch({ ...base, "GET /api/v1/assessments": { body: [{ ...summary, latest_attempt: { id: "attempt-9", status: "scored" } }] } });
    renderAt("/assessment");
    expect((await screen.findByRole("link", { name: "View your result" })).getAttribute("href")).toBe("/attempts/attempt-9/result");
    expect(screen.queryByRole("button", { name: /Start assessment/ })).toBeNull();
  });

  it("shows an empty state when no assessment exists for the role", async () => {
    mockFetch({ ...base, "GET /api/v1/assessments": { body: [] } });
    renderAt("/assessment");
    expect(await screen.findByText("No assessment is available for your job role yet.")).toBeTruthy();
  });
});

describe("taking an assessment", () => {
  it("shows one question at a time with previous/next, the grid and saved answers", async () => {
    const calls = mockFetch({
      ...base,
      "GET /api/v1/attempts/attempt-1": { body: threeQuestions },
      "PUT /api/v1/attempts/attempt-1/answers/qv-2": { body: { question_version_id: "qv-2", selected_option_id: "q2-opt-C", saved_at: "" } },
    });
    renderAt("/assessment/attempts/attempt-1?q=1");
    const user = userEvent.setup();

    expect(await screen.findByRole("heading", { level: 1, name: "Question 1 of 3" })).toBeTruthy();
    expect(screen.getByRole("group", { name: "What is the mean of 4, 8 and 12?" })).toBeTruthy();
    expect(screen.queryByText("What is 25% of 200?")).toBeNull(); // one question at a time
    expect((screen.getByRole("radio", { name: /Option 1B/ }) as HTMLInputElement).checked).toBe(true);
    expect((screen.getByRole("button", { name: "Previous" }) as HTMLButtonElement).disabled).toBe(true);

    const grid = screen.getByRole("complementary", { name: "Question overview" });
    expect(within(grid).getByRole("button", { name: "Question 1, answered, current" })).toBeTruthy();
    expect(within(grid).getByRole("button", { name: "Question 2, not answered" })).toBeTruthy();

    await user.click(screen.getByRole("button", { name: "Next" }));
    const heading = await screen.findByRole("heading", { level: 1, name: "Question 2 of 3" });
    await waitFor(() => expect(document.activeElement).toBe(heading));

    await user.click(screen.getByRole("radio", { name: /Option 2C/ }));
    await waitFor(() => expect(screen.getByRole("status").textContent).toContain("All answers saved"));
    expect(screen.getByRole("heading", { level: 1, name: "Question 2 of 3" })).toBeTruthy(); // answering never moves on
    const put = calls.find((c) => c.method === "PUT");
    expect(put?.headers["X-CSRF-Token"]).toBe("csrf-abc");
    expect(put?.body).toEqual({ selected_option_id: "q2-opt-C" });
    expect(screen.getByText("2 of 3 answered")).toBeTruthy();
    expect(within(grid).getByRole("button", { name: "Question 2, answered, current" })).toBeTruthy();

    await user.click(within(grid).getByRole("button", { name: "Question 3, not answered" }));
    expect(await screen.findByRole("heading", { level: 1, name: "Question 3 of 3" })).toBeTruthy();
    expect(screen.getAllByRole("button", { name: /Review and submit/ }).length).toBeGreaterThan(0);
    expect(document.body.textContent).not.toMatch(/is_correct|correct answer/i);
  });

  it("keeps the choice and offers a retry when saving fails", async () => {
    let attempts = 0;
    mockFetch({
      ...base,
      "GET /api/v1/attempts/attempt-1": { body: threeQuestions },
      "PUT /api/v1/attempts/attempt-1/answers/qv-2": () => {
        attempts += 1;
        return attempts === 1
          ? { status: 503, body: { code: "BACKEND_UNAVAILABLE", title: "Service unavailable", detail: "The platform service is not running.", correlation_id: "corr-s" } }
          : { body: { question_version_id: "qv-2", selected_option_id: "q2-opt-A", saved_at: "" } };
      },
    });
    renderAt("/assessment/attempts/attempt-1?q=2");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("radio", { name: /Option 2A/ }));
    const alert = await screen.findByRole("alert");
    expect(within(alert).getByText(/An answer was not saved/)).toBeTruthy();
    expect((screen.getByRole("radio", { name: /Option 2A/ }) as HTMLInputElement).checked).toBe(true);
    expect((screen.getByRole("button", { name: "Save and exit" }) as HTMLButtonElement).disabled).toBe(true);
    await user.click(within(alert).getByRole("button", { name: "Retry saving" }));
    await waitFor(() => expect(screen.queryByRole("alert")).toBeNull());
    expect(attempts).toBe(2);
  });

  it("confirms before submitting, lists unanswered questions and opens the result", async () => {
    const calls = mockFetch({
      ...base,
      "GET /api/v1/attempts/attempt-1": { body: threeQuestions },
      "POST /api/v1/attempts/attempt-1/submit": { body: { attempt_id: "attempt-1", status: "scored", score_total: "0.5", is_baseline: true, result_url: "" } },
      "GET /api/v1/attempts/attempt-1/result": { status: 500, body: { code: "X", title: "x", detail: "Result page reached." } },
    });
    renderAt("/assessment/attempts/attempt-1?q=3");
    const user = userEvent.setup();
    await user.click((await screen.findAllByRole("button", { name: "Review and submit" }))[0]);
    const dialog = await screen.findByRole("dialog", { name: "Submit your answers?" });
    expect(within(dialog).getByText("1 of 3 questions answered")).toBeTruthy();
    expect(within(dialog).getByText(/2 unanswered questions will be counted as not correct/)).toBeTruthy();

    await user.click(within(dialog).getByRole("button", { name: "Go to question 2" }));
    expect(await screen.findByRole("heading", { level: 1, name: "Question 2 of 3" })).toBeTruthy();
    expect(calls.some((c) => c.method === "POST")).toBe(false);

    await user.click(screen.getAllByRole("button", { name: "Review and submit" })[0]);
    await user.click(within(await screen.findByRole("dialog")).getByRole("button", { name: "Submit answers" }));
    expect(await screen.findByText("Result page reached.")).toBeTruthy();
    expect(calls.find((c) => c.method === "POST")?.headers["X-CSRF-Token"]).toBe("csrf-abc");
  });

  it("sends an already submitted attempt to its result", async () => {
    mockFetch({
      ...base,
      "GET /api/v1/attempts/attempt-1": { body: { ...threeQuestions, status: "scored" } },
      "GET /api/v1/attempts/attempt-1/result": { status: 500, body: { code: "X", title: "x", detail: "Result page reached." } },
    });
    renderAt("/assessment/attempts/attempt-1");
    expect(await screen.findByText("Result page reached.")).toBeTruthy();
  });
});
