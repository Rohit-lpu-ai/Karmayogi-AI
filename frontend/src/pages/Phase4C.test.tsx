import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import type { AdminCourseDetail, QuestionAuthoringOptions, ReviewTaskItem } from "@/api/adminTypes";
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

const as = (roles: string[], caps: string[]): Me => ({ ...me, id: "admin-1", access_roles: roles, admin_capabilities: caps });
const trainer = as(["trainer"], ["assessments.manage", "questions.author", "questions.review", "sources.view"]);
const manager = as(["training_manager"], ["courses.manage", "courses.review", "insight.view", "sources.view"]);

const authoring: QuestionAuthoringOptions = {
  competencies: [
    { id: "c1", code: "DEMO-SP-TABLES", name: "Reading statistical tables", framework_code: "DEMO-STAT-PRACTICE", restricted: false },
    { id: "c2", code: "CSCD-X", name: "Restricted competency", framework_code: "CSCD", restricted: true },
  ],
  source_records: [{ id: "s1", label: "Source: DoPT - Civil Services Competency Dictionary", organisation: "DoPT", record_id: "CSCD-DOC-001", verified: false, licence_notes: "" }],
  difficulties: ["foundational", "intermediate", "advanced"],
};

describe("question authoring", () => {
  it("validates the form, hides restricted competencies, and sends sources with the draft", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: trainer } },
      "GET /api/v1/admin/questions/options": { body: authoring },
      "POST /api/v1/admin/questions": { status: 422, body: { code: "VALIDATION_FAILED", title: "x", detail: "Check the answer options." } },
    });
    renderAt("/admin/questions/new");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Save draft" }));
    const summary = await screen.findByRole("alert");
    expect(within(summary).getByText(/Choose the competency/)).toBeTruthy();
    expect(within(summary).getByText(/Fill in every answer option/)).toBeTruthy();
    expect(calls.some((c) => c.method === "POST")).toBe(false);
    expect(screen.queryByRole("option", { name: /Restricted competency/ })).toBeNull();

    await user.selectOptions(screen.getByLabelText("Competency"), "c1");
    await user.type(screen.getByLabelText("Question"), "A table reports enrolment in thousands. What does 12.5 mean?");
    for (const [i, text] of ["12.5 people", "12,500 people", "125 people"].entries()) await user.type(screen.getByLabelText(`Option ${i + 1} text`), text);
    await user.click(screen.getByRole("button", { name: "Remove option 4" }));
    await user.click(screen.getByLabelText("Option 2 is correct"));
    await user.type(screen.getByLabelText("Explanation"), "The unit is thousands, so 12.5 is 12,500.");
    await user.click(screen.getByRole("button", { name: "Add source" }));
    await user.type(screen.getByLabelText("Note"), "Invented scenario for practice.");
    await user.click(screen.getByRole("button", { name: "Save draft" }));
    await waitFor(() => expect(calls.some((c) => c.method === "POST")).toBe(true));
    const body = calls.find((c) => c.method === "POST")!.body as { options: { is_correct: boolean }[]; sources: { source_kind: string }[] };
    expect(body.options.map((o) => o.is_correct)).toEqual([false, true, false]);
    expect(body.sources[0].source_kind).toBe("synthetic");
    expect(await screen.findByText("The question was not saved.")).toBeTruthy();
  }, 20_000); // many keystrokes; slow under a parallel test run
});

describe("review queue", () => {
  const task = (over: Partial<ReviewTaskItem>): ReviewTaskItem => ({
    id: "t1", task_type: "question_version_review", target_type: "question", target_id: "q1", target_version_id: "v1",
    title: "A table reports enrolment in thousands.", status: "open", submitted_by: { id: "u2", display_name: "Asha" },
    submitted_at: "2026-09-15T10:00:00Z", submission_note: null, decided_at: null, decision: null, can_decide: true, blocked_reason: null,
    row_version: 1, ...over,
  });

  it("explains why an author cannot decide their own submission", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: trainer } },
      "GET /api/v1/admin/reviews?status=open": { body: [task({ can_decide: false, blocked_reason: "You submitted this item, so another reviewer must decide it." })] },
    });
    renderAt("/admin/review");
    expect(await screen.findByText(/another reviewer must decide it/)).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Decide" })).toBeNull();
  });

  it("requires a reason to request changes and records the decision with the task version", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: trainer } },
      "GET /api/v1/admin/reviews?status=open": { body: [task({ row_version: 3 })] },
      "POST /api/v1/admin/reviews/t1/decision": { body: { status: "decided" } },
    });
    renderAt("/admin/review");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Decide" }));
    const dialog = await screen.findByRole("dialog", { name: "Decide review" });
    await user.click(within(dialog).getByRole("radio", { name: /Request changes/ }));
    await user.click(within(dialog).getByRole("button", { name: "Record decision" }));
    expect(await within(dialog).findByText("Give a reason so the author knows what to change.")).toBeTruthy();
    expect(calls.some((c) => c.method === "POST")).toBe(false);
    await user.type(within(dialog).getByLabelText("Reason"), "State the unit in the stem.");
    await user.click(within(dialog).getByRole("button", { name: "Record decision" }));
    await waitFor(() => expect(calls.some((c) => c.method === "POST")).toBe(true));
    expect(calls.find((c) => c.method === "POST")!.body).toEqual({ decision: "request_changes", reason: "State the unit in the stem.", row_version: 3 });
  });
});

describe("course administration", () => {
  const detail: AdminCourseDetail = {
    id: "k1", row_version: 2, title: "Units and footnotes clinic", description: null, course_type: "internal", content_origin: "synthetic",
    provider_organisation: "Internal (synthetic)", duration_days: null, difficulty: "foundational", learning_objectives: [], completion_criteria: null,
    state: "draft", review_status: "unreviewed", status: "inactive", published_at: null, is_demo: false, source: null, modules: [], competencies: [],
    guards: { checks: [
      { id: "internal", label: "Course is managed in this platform (not an imported listing)", passed: true },
      { id: "description", label: "Has a description", passed: false },
      { id: "lessons", label: "Has at least one active lesson", passed: false },
      { id: "competency_link", label: "Linked to at least one competency", passed: false },
      { id: "approved", label: "Approved by a reviewer", passed: false },
      { id: "approved_link", label: "At least one approved competency link", passed: false },
    ], can_submit: false, can_publish: false },
    reviews: [], open_task_id: null,
    actions: { can_edit: true, can_submit: false, can_withdraw: false, can_publish: false, can_unpublish: false },
  };

  it("shows publishing checks as text and offers no submit until they pass", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: manager } },
      "GET /api/v1/admin/courses/k1": { body: detail },
      "GET /api/v1/admin/courses/options": { body: { competencies: authoring.competencies } },
    });
    renderAt("/admin/courses/k1");
    expect(await screen.findByRole("heading", { level: 1, name: "Units and footnotes clinic" })).toBeTruthy();
    const description = screen.getByText("Has a description").closest("li")!;
    expect(description.textContent).toBe("Not met: Has a description");
    expect(screen.queryByRole("button", { name: "Send for review" })).toBeNull();
    expect(screen.getByText("Complete the first four checks to send this course for review.")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Publish to learners" })).toBeNull();
  });

  it("keeps content screens away from roles without the capability", async () => {
    const calls = mockFetch({ "GET /api/v1/auth/session": { body: { ...session, user: manager } } });
    renderAt("/admin/questions");
    expect(await screen.findByRole("heading", { level: 1, name: "No access to this page" })).toBeTruthy();
    expect(calls.some((c) => c.url.startsWith("/api/v1/admin/questions"))).toBe(false);
  });
});
