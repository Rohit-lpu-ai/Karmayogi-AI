import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "../App";
import { setCsrfToken } from "../api/client";
import { AuthProvider } from "../auth/AuthContext";
import { mockFetch } from "../test/fetchMock";
import { attempt, gaps, me, profile, recommendations, session } from "../test/fixtures";

afterEach(() => {
  cleanup();
  setCsrfToken(null);
  vi.unstubAllGlobals();
});

function renderApp(path: string) {
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

describe("routing", () => {
  it("sends signed-out users to the login page", async () => {
    mockFetch({ "GET /api/v1/auth/session": { status: 401, body: { code: "UNAUTHENTICATED", title: "Authentication required" } } });
    renderApp("/");
    expect(await screen.findByRole("heading", { name: "Sign in" })).toBeTruthy();
  });

  it("sends learners without a job role to onboarding", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: { ...me, job_role: null } } },
      "GET /api/v1/job-roles": { body: [] },
    });
    renderApp("/");
    expect(await screen.findByRole("heading", { name: "Get started" })).toBeTruthy();
    expect(await screen.findByText("Your organisation hasn't set up job roles yet.")).toBeTruthy();
  });

  it("shows login errors from the API without revealing account details", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { status: 401, body: { code: "UNAUTHENTICATED", title: "Authentication required" } },
      "POST /api/v1/auth/login": { status: 401, body: { code: "INVALID_CREDENTIALS", title: "Sign-in failed", detail: "Email or password is incorrect.", correlation_id: "corr-9" } },
    });
    renderApp("/login");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("Email"), "learner01@example.invalid");
    await user.type(screen.getByLabelText("Password"), "wrong-password");
    await user.click(screen.getByRole("button", { name: "Sign in" }));
    const alert = await screen.findByRole("alert");
    expect(within(alert).getByText("Email or password is incorrect.")).toBeTruthy();
    expect(within(alert).getByText("corr-9")).toBeTruthy();
  });
});

describe("dashboard", () => {
  it("shows gaps with development wording and DEMO-labelled recommendations with reasons", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/me/competency-gaps": { body: gaps },
      "GET /api/v1/me/recommendations": { body: recommendations },
      "GET /api/v1/me/competency-profile": { body: profile },
    });
    renderApp("/");
    expect(await screen.findByText("Developing - 2 levels below the level required for your role")).toBeTruthy();
    expect(screen.getByText("Strength - at or above the required level")).toBeTruthy();
    const recs = await screen.findByRole("region", { name: "Recommended learning" });
    expect(within(recs).getByText("DEMO - Percentages refresher (synthetic course)")).toBeTruthy();
    expect(within(recs).getAllByText("DEMO - synthetic").length).toBeGreaterThan(0);
    expect(within(recs).getByText(/estimated level 1, required level 3/)).toBeTruthy();
    expect(within(recs).getByText(/iGOT Karmayogi\) are not connected/)).toBeTruthy();
    expect(document.body.textContent).not.toMatch(/Rule:|rec-v1|gap_rule/);
    expect(within(recs).queryByText("Reviewed")).toBeNull();
    expect(screen.getByRole("note").textContent).toContain("DEMO environment");
    expect(document.body.textContent).not.toMatch(/weak|failed|poor/i);
  });

  it("keeps other cards usable when one card fails", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/me/competency-gaps": { body: gaps },
      "GET /api/v1/me/recommendations": { status: 500, body: { code: "INTERNAL_ERROR", title: "Internal server error", detail: "Something went wrong.", correlation_id: "corr-500" } },
      "GET /api/v1/me/competency-profile": { body: profile },
    });
    renderApp("/");
    const recs = await screen.findByRole("region", { name: "Recommended learning" });
    expect(await within(recs).findByText("Something went wrong.")).toBeTruthy();
    expect(within(recs).getByRole("button", { name: "Try again" })).toBeTruthy();
    expect(await screen.findByText("Developing - 2 levels below the level required for your role")).toBeTruthy();
  });
});

describe("assessment", () => {
  it("renders delivered questions without keys and saves answers with the CSRF token", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/assessments": { body: [{ id: "assessment-1", title: attempt.assessment.title, purpose: "pre", feedback_policy: "correctness_and_explanations", question_count: 1, is_demo: true, latest_attempt: null }] },
      "POST /api/v1/assessments/assessment-1/attempts": { status: 201, body: attempt },
      "PUT /api/v1/attempts/attempt-1/answers/qv-1": { body: { question_version_id: "qv-1", selected_option_id: "opt-c", saved_at: "" } },
    });
    renderApp("/assessment");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Start assessment" }));
    const question = await screen.findByRole("group", { name: /What is 25% of 200\?/ });
    expect(within(question).getByText("DEMO item")).toBeTruthy();
    await user.click(within(question).getByLabelText("50"));
    await waitFor(() => expect(screen.getByRole("status").textContent).toBe("Saved"));
    const put = calls.find((c) => c.method === "PUT");
    expect(put?.headers["X-CSRF-Token"]).toBe("csrf-abc");
    expect(put?.body).toEqual({ selected_option_id: "opt-c" });
    expect(document.body.textContent).not.toMatch(/correct answer|is_correct/i);
  });

  it("asks for confirmation and warns about unanswered questions before submitting", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/assessments": { body: [{ id: "assessment-1", title: attempt.assessment.title, purpose: "pre", feedback_policy: "correctness_and_explanations", question_count: 1, is_demo: true, latest_attempt: { id: "attempt-1", status: "in_progress" } }] },
      "POST /api/v1/assessments/assessment-1/attempts": { body: attempt },
    });
    renderApp("/assessment");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Resume assessment" }));
    await user.click(await screen.findByRole("button", { name: "Review and submit" }));
    expect(screen.getByText(/1 question\(s\) are unanswered and will be scored as incorrect/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Submit answers" })).toBeTruthy();
  });
});
