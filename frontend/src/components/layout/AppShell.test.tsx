import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import { setCsrfToken } from "@/api/client";
import { AuthProvider } from "@/auth/AuthContext";
import { ConfirmationDialog } from "@/components/product/ConfirmationDialog";
import { EvidenceBadge } from "@/components/States";
import { PRODUCT } from "@/config/product";
import { mockFetch } from "@/test/fetchMock";
import { gaps, me, profile, recommendations, session } from "@/test/fixtures";

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

const dashboardRoutes = {
  "GET /api/v1/me/competency-gaps": { body: gaps },
  "GET /api/v1/me/recommendations": { body: recommendations },
  "GET /api/v1/me/competency-profile": { body: profile },
};

describe("app shell", () => {
  it("shows a neutral frame, not the signed-out layout, while the session is checked", async () => {
    let release: (value: Response) => void = () => undefined;
    vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>((resolve) => (release = resolve))));
    renderApp("/");
    expect(screen.getByRole("status").textContent).toContain("Checking your session");
    expect(screen.queryByRole("heading", { name: "Sign in" })).toBeNull();
    expect(screen.queryByRole("note")).toBeNull();
    release(new Response(JSON.stringify(session), { status: 200, headers: { "content-type": "application/json" } }));
    expect(await screen.findByRole("navigation", { name: "Main" })).toBeTruthy();
  });

  it("renders landmarks, skip link, product name, navigation and the job role", async () => {
    mockFetch({ "GET /api/v1/auth/session": { body: session }, ...dashboardRoutes });
    renderApp("/");
    const nav = await screen.findByRole("navigation", { name: "Main" });
    expect(within(nav).getByRole("link", { name: "Home" }).getAttribute("aria-current")).toBe("page");
    expect(within(nav).getByRole("link", { name: "Baseline assessment" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Skip to content" }).getAttribute("href")).toBe("#main");
    expect(screen.getByRole("main")).toBeTruthy();
    expect(screen.getAllByRole("link", { name: `${PRODUCT.name} (working name) - home` }).length).toBeGreaterThan(0);
    expect(screen.getByRole("link", { name: `Job role: ${me.job_role!.name} (demo). Change job role` }).getAttribute("href")).toBe("/get-started");
    expect(document.body.textContent).not.toMatch(/Government of India|Karmayogi Bharat|MoSPI|NSSTA/);
  });

  it("hides learning navigation for roles that cannot take assessments", async () => {
    const auditor = { ...me, access_roles: ["auditor"], can_take_assessments: false, job_role: null };
    mockFetch({ "GET /api/v1/auth/session": { body: { ...session, user: auditor } } });
    renderApp("/");
    const nav = await screen.findByRole("navigation", { name: "Main" });
    expect(within(nav).queryByRole("link", { name: "Baseline assessment" })).toBeNull();
  });

  it("explains the demo environment in one expandable note", async () => {
    mockFetch({ "GET /api/v1/auth/session": { body: session }, ...dashboardRoutes });
    renderApp("/");
    await screen.findByRole("navigation", { name: "Main" });
    const note = screen.getByRole("note", { name: "Demo environment" });
    const toggle = within(note).getByRole("button", { name: "What does this mean?" });
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    await userEvent.setup().click(toggle);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    expect(within(note).getByText(/not connected to iGOT Karmayogi/)).toBeTruthy();
  });

  it("does not show the demo notice for non-synthetic accounts", async () => {
    mockFetch({ "GET /api/v1/auth/session": { body: { ...session, user: { ...me, is_synthetic: false } } }, ...dashboardRoutes });
    renderApp("/");
    await screen.findByRole("navigation", { name: "Main" });
    expect(screen.queryByRole("note", { name: "Demo environment" })).toBeNull();
  });

  it("opens the mobile menu as a dialog and closes it after navigating", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: session },
      ...dashboardRoutes,
      "GET /api/v1/assessments": { body: [] },
    });
    renderApp("/");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Open menu" }));
    const dialog = await screen.findByRole("dialog", { name: "Menu" });
    await user.click(within(dialog).getByRole("link", { name: "Baseline assessment" }));
    await waitFor(() => expect(screen.queryByRole("dialog", { name: "Menu" })).toBeNull());
    expect(await screen.findByRole("heading", { name: "Baseline assessment" })).toBeTruthy();
  });

  it("signs out from the account menu with the CSRF token", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      ...dashboardRoutes,
      "POST /api/v1/auth/logout": { status: 204 },
    });
    renderApp("/");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: `Account menu for ${me.display_name}` }));
    const menu = await screen.findByRole("menu");
    expect(within(menu).getByText("Synthetic demo account")).toBeTruthy();
    await user.click(within(menu).getByRole("menuitem", { name: "Sign out" }));
    expect(await screen.findByRole("heading", { name: "Sign in" })).toBeTruthy();
    const logout = calls.find((c) => c.url === "/api/v1/auth/logout");
    expect(logout?.headers["X-CSRF-Token"]).toBe("csrf-abc");
  });

  it("uses the signed-out layout without navigation on the login page", async () => {
    mockFetch({ "GET /api/v1/auth/session": { status: 401, body: { code: "UNAUTHENTICATED", title: "Authentication required" } } });
    renderApp("/login");
    expect(await screen.findByRole("heading", { name: "Sign in" })).toBeTruthy();
    expect(screen.queryByRole("navigation", { name: "Main" })).toBeNull();
    expect(screen.getByText(/Not an official government service/)).toBeTruthy();
  });
});

describe("design system components", () => {
  it("writes evidence strength as text", () => {
    render(
      <>
        <EvidenceBadge band="medium" count={5} />
        <EvidenceBadge band={null} />
      </>,
    );
    expect(screen.getByText("Medium evidence (5 questions)")).toBeTruthy();
    expect(screen.getByText("Not assessed")).toBeTruthy();
  });

  it("confirmation dialog confirms, cancels with Escape and returns focus to the trigger", async () => {
    const onConfirm = vi.fn();
    function Harness() {
      const [open, setOpen] = useState(false);
      return (
        <>
          <button type="button" onClick={() => setOpen(true)}>
            Submit
          </button>
          <ConfirmationDialog open={open} onOpenChange={setOpen} title="Submit your answers?" confirmLabel="Submit answers" onConfirm={onConfirm}>
            1 question is unanswered.
          </ConfirmationDialog>
        </>
      );
    }
    render(<Harness />);
    const user = userEvent.setup();
    const trigger = screen.getByRole("button", { name: "Submit" });
    await user.click(trigger);
    const dialog = await screen.findByRole("dialog", { name: "Submit your answers?" });
    expect(within(dialog).getByText("1 question is unanswered.")).toBeTruthy();
    await user.keyboard("{Escape}");
    await waitFor(() => expect(screen.queryByRole("dialog")).toBeNull());
    await waitFor(() => expect(document.activeElement).toBe(trigger));
    await user.click(trigger);
    await user.click(within(await screen.findByRole("dialog")).getByRole("button", { name: "Submit answers" }));
    expect(onConfirm).toHaveBeenCalledTimes(1);
  });
});
