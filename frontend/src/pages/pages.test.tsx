import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "../App";
import { setCsrfToken } from "../api/client";
import { AuthProvider } from "../auth/AuthContext";
import { mockFetch } from "../test/fetchMock";
import { me, session } from "../test/fixtures";

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
    expect(await screen.findByRole("heading", { level: 1, name: "Select your job role" })).toBeTruthy();
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
