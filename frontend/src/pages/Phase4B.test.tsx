import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import { setCsrfToken } from "@/api/client";
import type { CourseOutline, CourseProgress, LearningPath, LessonDetail } from "@/api/types";
import { AuthProvider } from "@/auth/AuthContext";
import { Markdown } from "@/components/product/Markdown";
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

const course = { id: "c1", title: "DEMO - Reading statistical tables critically (synthetic course)", difficulty: "foundational" as const, duration_days: 1,
  content_origin: "synthetic" as const, completion_criteria: "Open and mark all 2 lessons as complete.", is_demo: true };
const progress = (over: Partial<CourseProgress> = {}): CourseProgress => ({
  lesson_count: 2, total_minutes: 17, module_count: 1, completed_lessons: 0, percent: 0, status: "not_started",
  started_at: null, completed_at: null, resume_lesson: { id: "l1", title: "The anatomy of a statistical table" }, ...over,
});
const outline = (over: Partial<CourseProgress> = {}, statuses: [string, string] = ["not_started", "not_started"]): CourseOutline => ({
  course,
  modules: [{ id: "m1", position: 1, title: "Before you quote a figure", summary: "Units and footnotes.", lessons: [
    { id: "l1", position: 1, title: "The anatomy of a statistical table", lesson_type: "reading", estimated_minutes: 7, status: statuses[0] as never },
    { id: "l2", position: 2, title: "Worked example: reading an enrolment table", lesson_type: "worked_example", estimated_minutes: 10, status: statuses[1] as never },
  ] }],
  progress: progress(over),
  prerequisites: [],
});
const lesson = (id: "l1" | "l2", status: LessonDetail["status"] = "not_started"): LessonDetail => ({
  id, title: id === "l1" ? "The anatomy of a statistical table" : "Worked example: reading an enrolment table",
  lesson_type: id === "l1" ? "reading" : "worked_example", estimated_minutes: id === "l1" ? 7 : 10, content_kind: "inline_markdown",
  body_markdown: "Read the **unit** first.\n\n## Checklist\n\n1. Title\n2. Unit\n\n| Region | Total |\n|---|---|\n| North | 78.1 |\n",
  module: { id: "m1", title: "Before you quote a figure", position: 1 }, position: id === "l1" ? 1 : 2, lesson_count: 2, status,
  previous: id === "l2" ? { id: "l1", title: "The anatomy of a statistical table" } : null,
  next: id === "l1" ? { id: "l2", title: "Worked example: reading an enrolment table" } : null,
  course, content_notice: "Synthetic lesson written for product evaluation. Figures are invented.",
});

describe("Markdown renderer", () => {
  it("renders headings, lists, tables and emphasis, and shows any markup as plain text", () => {
    const { container } = render(<Markdown source={"Intro with **bold** and *italic*.\n\n## Heading\n\n- one\n- two\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n<img src=x onerror=alert(1)> <script>alert(1)</script>"} />);
    expect(screen.getByRole("heading", { level: 2, name: "Heading" })).toBeTruthy();
    expect(container.querySelector("strong")?.textContent).toBe("bold");
    expect(screen.getAllByRole("listitem")).toHaveLength(2);
    expect(within(screen.getByRole("table")).getByRole("columnheader", { name: "A" })).toBeTruthy();
    expect(container.querySelector("img, script")).toBeNull();
    expect(container.textContent).toContain("<script>alert(1)</script>");
  });
});

describe("course learning hub", () => {
  it("starts the course and opens the first lesson", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/courses/c1/outline": { body: outline() },
      "POST /api/v1/courses/c1/start": { body: outline({ status: "in_progress" }) },
      "GET /api/v1/lessons/l1": { body: lesson("l1") },
      "PUT /api/v1/me/lessons/l1/progress": { body: { lesson_id: "l1", lesson_status: "in_progress", course_progress: progress({ status: "in_progress" }), next: null } },
    });
    renderAt("/courses/c1/learn");
    expect(await screen.findByRole("heading", { level: 1, name: "Reading statistical tables critically" })).toBeTruthy();
    expect(screen.getByText("Open and mark all 2 lessons as complete.")).toBeTruthy();
    await userEvent.setup().click(screen.getByRole("button", { name: "Start course" }));
    expect(await screen.findByRole("heading", { level: 1, name: "The anatomy of a statistical table" })).toBeTruthy();
    expect(calls.find((c) => c.method === "POST")!.headers["X-CSRF-Token"]).toBe("csrf-abc");
  });

  it("offers Continue with the resume lesson for a course in progress", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/courses/c1/outline": { body: outline({ status: "in_progress", completed_lessons: 1, percent: 50, resume_lesson: { id: "l2", title: "Worked example: reading an enrolment table" } }, ["completed", "not_started"]) },
    });
    renderAt("/courses/c1/learn");
    const link = await screen.findByRole("link", { name: /Continue: Worked example/ });
    expect(link.getAttribute("href")).toBe("/courses/c1/lessons/l2");
    expect(screen.getByRole("progressbar", { name: /Progress in/ }).getAttribute("aria-valuetext")).toBe("1 of 2 lessons completed");
  });
});

describe("lesson player", () => {
  it("records the lesson as started, renders the body, and marks it complete", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/courses/c1/outline": { body: outline({ status: "in_progress" }) },
      "GET /api/v1/lessons/l1": { body: lesson("l1") },
      "PUT /api/v1/me/lessons/l1/progress": (call) => ({
        body: { lesson_id: "l1", lesson_status: (call.body as { status: string }).status, course_progress: progress({ status: "in_progress", completed_lessons: 1, percent: 50 }), next: { id: "l2", title: "Worked example" } },
      }),
    });
    renderAt("/courses/c1/lessons/l1");
    expect(await screen.findByRole("heading", { level: 1, name: "The anatomy of a statistical table" })).toBeTruthy();
    expect(screen.getByText("Lesson 1 of 2 · Module 1: Before you quote a figure")).toBeTruthy();
    expect(screen.getByRole("table")).toBeTruthy();
    await waitFor(() => expect(calls.some((c) => c.method === "PUT" && (c.body as { status: string }).status === "in_progress")).toBe(true));

    await userEvent.setup().click(screen.getByRole("button", { name: "Mark as complete" }));
    await waitFor(() => expect(calls.some((c) => c.method === "PUT" && (c.body as { status: string }).status === "completed")).toBe(true));
    expect(await screen.findAllByText("Completed")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Mark as complete" })).toBeNull();
    expect(screen.getByRole("link", { name: /Next: Worked example/ }).getAttribute("href")).toBe("/courses/c1/lessons/l2");
  });

  it("does not re-open a completed lesson and announces course completion on the last lesson", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/courses/c1/outline": { body: outline({ status: "in_progress" }, ["completed", "in_progress"]) },
      "GET /api/v1/lessons/l2": { body: lesson("l2", "in_progress") },
      "PUT /api/v1/me/lessons/l2/progress": { body: { lesson_id: "l2", lesson_status: "completed", course_progress: progress({ status: "completed", completed_lessons: 2, percent: 100, resume_lesson: null }), next: null } },
    });
    renderAt("/courses/c1/lessons/l2");
    await userEvent.setup().click(await screen.findByRole("button", { name: "Mark as complete" }));
    expect(await screen.findByText("Course complete")).toBeTruthy();
    expect(document.body.textContent).toMatch(/competency estimates only change with new\s+assessment evidence/);
    expect(calls.filter((c) => c.method === "PUT")).toHaveLength(1); // no automatic "in_progress" for a lesson already started
  });

  it("shows a clear message for a lesson that is not available", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/lessons/missing": { status: 404, body: { code: "NOT_FOUND", title: "Not found", detail: "This lesson is not available." } },
      "GET /api/v1/courses/c1/outline": { body: outline() },
    });
    renderAt("/courses/c1/lessons/missing");
    expect(await screen.findByText("This lesson is not available.")).toBeTruthy();
    expect(screen.getByRole("link", { name: /Back to course contents/ }).getAttribute("href")).toBe("/courses/c1/learn");
  });
});

describe("learning path", () => {
  const basePath: LearningPath = {
    id: "p1", rule_version: "path-v1", rule: "Gaps largest first.", generated_at: "2026-09-15T10:00:00Z",
    job_role: { id: "role-1", name: "DEMO - Junior Statistical Officer (synthetic role)", code: "DEMO-ROLE-JSO", description: null, is_demo: true },
    state: "ready",
    summary: { courses: 2, completed: 1, in_progress: 0, total_minutes: 34, gaps_without_content: 1 },
    groups: [
      { competency: { id: "g1", code: "DEMO-SP-TABLES", name: "DEMO - Reading statistical tables (synthetic)" }, required_level: 3, estimated_level: 1, gap: 2, items: [
        { id: "i1", position: 1, item_type: "course", course, progress: progress({ status: "completed", completed_lessons: 2, percent: 100, resume_lesson: null }), status: "completed", reasons: [{ rule: "gap_match", competency_name: "DEMO - Reading statistical tables (synthetic)" }] },
        { id: "i2", position: 2, item_type: "course", course: { ...course, id: "c2", title: "DEMO - Communicating statistics clearly (synthetic course)" }, progress: progress(), status: "not_started", reasons: [{ rule: "prerequisite", for_course_title: "Advanced tables" }] },
      ] },
      { competency: { id: "g2", code: "DEMO-SP-QUALITY", name: "DEMO - Data quality and validation (synthetic)" }, required_level: 2, estimated_level: 1, gap: 1, items: [
        { id: "i3", position: 3, item_type: "no_content_placeholder", course: null, progress: null, status: "not_started", reasons: [{ rule: "no_approved_content" }] },
      ] },
    ],
    completed_earlier: [],
    note: "Completing courses does not change your competency estimates.",
  };

  it("groups courses by gap, leads with the next course and explains placeholders and ordering", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/me/learning-path": { body: basePath },
      "POST /api/v1/me/learning-path/regenerate": { body: { ...basePath, id: "p2" } },
    });
    renderAt("/learning-path");
    expect(await screen.findByRole("heading", { level: 1, name: "Your learning path" })).toBeTruthy();
    expect(screen.getByRole("heading", { level: 2, name: "Communicating statistics clearly" })).toBeTruthy(); // up next skips completed
    expect(screen.getAllByText("Recommended before Advanced tables.")).toHaveLength(2); // up next card and the path row
    expect(screen.getByText(/No approved course covers this gap yet/)).toBeTruthy();
    expect(screen.getByText("Level 1 now · level 3 needed (2 to go)")).toBeTruthy();
    expect(screen.getByRole("link", { name: /Review Reading statistical tables critically/ })).toBeTruthy();
    await userEvent.setup().click(screen.getByRole("button", { name: "Refresh path" }));
    await waitFor(() => expect(calls.some((c) => c.method === "POST")).toBe(true));
  });

  it("asks for the baseline when no gaps are assessed yet", async () => {
    mockFetch({ "GET /api/v1/auth/session": { body: session }, "GET /api/v1/me/learning-path": { body: { ...basePath, state: "assessment_needed", groups: [] } } });
    renderAt("/learning-path");
    expect(await screen.findByText("Take your baseline assessment to build your path")).toBeTruthy();
    expect(screen.getByRole("link", { name: "Go to the baseline assessment" }).getAttribute("href")).toBe("/assessment");
  });
});
