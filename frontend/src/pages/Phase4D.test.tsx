import { cleanup, render, screen, within } from "@testing-library/react";
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

const manager: Me = { ...me, id: "m1", access_roles: ["training_manager"], admin_capabilities: ["courses.manage", "courses.review", "insight.view", "sources.view"] };
const note = "Aggregated development insight. Figures for fewer than 5 learners are withheld.";
const withheld = { required_for: null, assessed: null, with_gap: null, share: null, average_gap: null, suppressed: true };
const notRequired = { required_for: null, assessed: null, with_gap: null, share: null, average_gap: null, suppressed: false };
const shown = { required_for: 18, assessed: 18, with_gap: 12, share: 0.667, average_gap: 1.4, suppressed: false };

describe("skill gaps heatmap", () => {
  it("shows values as text, marks withheld cells and never lists people", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: manager } },
      "GET /api/v1/admin/insight/skill-gaps": { body: {
        competencies: [{ id: "c1", code: "DEMO-SP-SAMPLING", name: "DEMO - Sampling and survey design (synthetic)" }, { id: "c2", code: "DEMO-SP-INDEX", name: "DEMO - Index numbers (synthetic)" }],
        rows: [
          { department: { id: "d1", name: "DEMO Survey Operations Division (synthetic)" }, learners: { value: 18, suppressed: false }, cells: { c1: shown, c2: notRequired } },
          { department: { id: "d2", name: "DEMO Data Services Unit (synthetic)" }, learners: { value: null, suppressed: true }, cells: { c1: withheld, c2: withheld } },
        ],
        totals: { c1: shown, c2: withheld }, job_roles: [], job_role_id: null, min_group_size: 5, note,
      } },
    });
    renderAt("/admin/skill-gaps");
    const table = await screen.findByRole("table");
    const survey = within(table).getByRole("row", { name: /Survey Operations/ });
    expect(within(survey).getByText("67%")).toBeTruthy();
    expect(within(survey).getByText("12 of 18")).toBeTruthy();
    expect(within(survey).getByText("Not required")).toBeTruthy();
    const small = within(table).getByRole("row", { name: /Data Services/ });
    expect(within(small).getByText("Under 5 learners")).toBeTruthy();
    expect(within(small).getAllByText(/learners assessed; withheld/)).toHaveLength(2);
    expect(screen.getByText(note)).toBeTruthy();
    expect(document.body.textContent).not.toMatch(/@example\.invalid|Cohort Learner/);
  });
});

describe("training needs", () => {
  it("ranks needs, flags missing content and withholds small counts", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: manager } },
      "GET /api/v1/admin/insight/training-needs": { body: {
        items: [
          { competency: { id: "c1", code: "A", name: "DEMO - Rates, ratios and percentage change (synthetic)" }, learners_with_gap: 20, average_gap: 1.5, departments_affected: 2, published_courses: 3,
            learners_started_linked_course: { value: 6, suppressed: false }, learners_completed_linked_course: { value: null, suppressed: true }, content_gap: false },
          { competency: { id: "c2", code: "B", name: "DEMO - Index numbers (synthetic)" }, learners_with_gap: 7, average_gap: 1, departments_affected: 1, published_courses: 0,
            learners_started_linked_course: { value: null, suppressed: true }, learners_completed_linked_course: { value: null, suppressed: true }, content_gap: true },
        ],
        withheld_competencies: 2, min_group_size: 5, note,
      } },
    });
    renderAt("/admin/training-needs");
    const first = (await screen.findByRole("heading", { level: 2, name: "Rates, ratios and percentage change" })).closest("li")!;
    const second = screen.getByRole("heading", { level: 2, name: "Index numbers" }).closest("li")!;
    expect(first.compareDocumentPosition(second) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(within(first).getByText("20 learners with a gap")).toBeTruthy();
    expect(within(first).getAllByText("Under 5")).toHaveLength(1);
    expect(within(second).getByText("No published course")).toBeTruthy();
    expect(screen.getByText(/2 competencies are not listed because fewer than 5 learners have that gap/)).toBeTruthy();
  });
});
