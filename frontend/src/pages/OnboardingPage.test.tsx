import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import { setCsrfToken } from "@/api/client";
import type { Me } from "@/api/types";
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

const newLearner: Me = { ...me, job_role: null, notice: { ...me.notice, acknowledged_at: null } };
const role = { id: "role-1", name: "DEMO - Statistical Assistant (synthetic role)", code: "DEMO-ROLE-STAT-ASSISTANT", description: "Synthetic job role.", is_demo: true };
const requirements = {
  job_role: role,
  requirements: [
    {
      competency: { id: "c1", code: "DEMO-C1", name: "DEMO - Descriptive statistics (synthetic)", framework_code: "DEMO-FUNCTIONAL", framework_status: "draft", is_demo: true },
      required_level: 3,
      mapping_version: 1,
      levels: [1, 2, 3, 4].map((n) => ({ level_number: n, label: `Level ${n}`, min_score: null, threshold_status: "provisional" })),
    },
  ],
};
const assessmentSummary = { id: "assessment-1", title: "DEMO - Baseline assessment (synthetic arithmetic items)", purpose: "pre", feedback_policy: "correctness_and_explanations", question_count: 10, is_demo: true, latest_attempt: null };

describe("onboarding", () => {
  it("walks a new learner through welcome, notice, job role and assessment with focus on each step", async () => {
    const acknowledged = { ...newLearner, notice: { ...newLearner.notice, acknowledged_at: "2026-09-15T10:00:00Z" } };
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: newLearner } },
      "POST /api/v1/me/notice-acknowledgements": { body: acknowledged },
      "GET /api/v1/job-roles": { body: [role] },
      "GET /api/v1/job-roles/role-1/competencies": { body: requirements },
      "PUT /api/v1/me/job-role": { body: { ...acknowledged, job_role: role } },
      "GET /api/v1/assessments": { body: [assessmentSummary] },
    });
    renderAt("/");
    const user = userEvent.setup();

    // Step 1: welcome explains the platform
    expect(await screen.findByRole("heading", { level: 1, name: `Welcome, ${me.display_name}` })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "How the platform helps you" })).toBeTruthy();
    expect(within(screen.getByRole("navigation", { name: "Progress" })).getAllByText("Welcome").length).toBeGreaterThan(0);
    await user.click(screen.getByRole("button", { name: "Get started" }));

    // Step 2: demo data and notice; cannot continue before ticking the box
    const noticeHeading = await screen.findByRole("heading", { level: 1, name: "Your data and this demo" });
    await waitFor(() => expect(document.activeElement).toBe(noticeHeading));
    expect(screen.getByRole("heading", { name: "You are using a demo environment" })).toBeTruthy();
    expect(screen.getByText(/not connected to iGOT Karmayogi/)).toBeTruthy();
    const acknowledge = screen.getByRole("button", { name: "Acknowledge and continue" });
    expect((acknowledge as HTMLButtonElement).disabled).toBe(true);
    await user.click(screen.getByRole("checkbox", { name: /used for learning and development only/ }));
    await user.click(acknowledge);
    expect(calls.find((c) => c.method === "POST")?.body).toEqual({ notice_version: "privacy-ai-use-draft-0" });

    // Step 3: job role with requirement preview
    expect(await screen.findByRole("heading", { level: 1, name: "Select your job role" })).toBeTruthy();
    await user.click(await screen.findByRole("radio", { name: /DEMO - Statistical Assistant/ }));
    expect(await screen.findByText("Level 3 of 4 required")).toBeTruthy();
    expect(screen.getByRole("img", { name: /required level 3/ })).toBeTruthy();
    await user.click(screen.getByRole("button", { name: "Confirm job role" }));
    const put = calls.find((c) => c.method === "PUT");
    expect(put?.body).toEqual({ job_role_id: "role-1" });
    expect(put?.headers["X-CSRF-Token"]).toBe("csrf-abc");

    // Step 4: the assessment is explained before starting
    expect(await screen.findByRole("heading", { level: 1, name: "Your baseline assessment" })).toBeTruthy();
    expect(await screen.findByText("10 multiple choice")).toBeTruthy();
    expect(screen.getByText(/No time limit/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Continue to the assessment" })).toBeTruthy();
  });

  it("resumes at the job role step when the notice was already acknowledged", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: { ...me, job_role: null } } },
      "GET /api/v1/job-roles": { body: [] },
    });
    renderAt("/");
    expect(await screen.findByRole("heading", { level: 1, name: "Select your job role" })).toBeTruthy();
    expect(await screen.findByText("Your organisation hasn't set up job roles yet.")).toBeTruthy();
    expect((screen.getByRole("button", { name: "Confirm job role" }) as HTMLButtonElement).disabled).toBe(true);
  });

  it("shows a retryable error when the notice cannot be saved", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: newLearner } },
      "POST /api/v1/me/notice-acknowledgements": { status: 503, body: { code: "BACKEND_UNAVAILABLE", title: "Service unavailable", detail: "The platform service is not running.", correlation_id: "corr-x" } },
    });
    renderAt("/get-started");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Get started" }));
    await user.click(await screen.findByRole("checkbox"));
    await user.click(screen.getByRole("button", { name: "Acknowledge and continue" }));
    expect(within(await screen.findByRole("alert")).getByText("The platform service is not running.")).toBeTruthy();
    expect(screen.getByRole("heading", { level: 1, name: "Your data and this demo" })).toBeTruthy();
  });

  it("lets an onboarded learner change job role without repeating onboarding", async () => {
    const other = { ...role, id: "role-2", name: "DEMO - Survey Officer (synthetic role)" };
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/job-roles": { body: [role, other] },
      "GET /api/v1/job-roles/role-1/competencies": { body: requirements },
      "GET /api/v1/job-roles/role-2/competencies": { body: { job_role: other, requirements: [] } },
      "PUT /api/v1/me/job-role": { body: { ...me, job_role: other } },
      "GET /api/v1/me/competency-gaps": { status: 500, body: { code: "X", title: "x" } },
      "GET /api/v1/me/recommendations": { status: 500, body: { code: "X", title: "x" } },
      "GET /api/v1/me/competency-profile": { status: 500, body: { code: "X", title: "x" } },
    });
    renderAt("/get-started");
    const user = userEvent.setup();
    expect(await screen.findByRole("heading", { level: 1, name: "Your job role" })).toBeTruthy();
    expect(screen.queryByRole("navigation", { name: "Progress" })).toBeNull();
    const save = screen.getByRole("button", { name: "Save job role" }) as HTMLButtonElement;
    expect(save.disabled).toBe(true); // unchanged
    await user.click(await screen.findByRole("radio", { name: /Survey Officer/ }));
    expect(await screen.findByText("This job role's requirements haven't been approved yet.")).toBeTruthy();
    await user.click(save);
    await waitFor(() => expect(calls.some((c) => c.method === "PUT")).toBe(true));
    expect(await screen.findByRole("heading", { name: /Welcome/ })).toBeTruthy(); // back on the dashboard
  });
});
