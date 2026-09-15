import { cleanup, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";
import { App } from "@/App";
import { setCsrfToken } from "@/api/client";
import type { AdminUser, AdminUserPage, Me } from "@/api/types";
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

const signedOut = { "GET /api/v1/auth/session": { status: 401, body: { code: "UNAUTHENTICATED", title: "x" } } };
const environment = { "GET /api/v1/environment": { body: { synthetic_data: true, self_registration_enabled: true } } };
const orgAdmin: Me = {
  ...me,
  id: "admin-1",
  email: "org-admin01@example.invalid",
  display_name: "Demo Org Admin 01",
  access_roles: ["org_admin"],
  admin_capabilities: ["audit.view", "courses.manage", "departments.manage", "roles.assign", "users.manage", "users.view"],
};
const learnerUser: AdminUser = {
  id: "user-9", display_name: "Asha Verma", email: "asha@example.invalid", registration_id: "STA-0142", designation: null, status: "active",
  department: { id: "dept-1", name: "North Division", code: "north" }, job_role: null, roles: [{ role: "learner", department_scope_id: null }],
  is_synthetic: false, has_password: true, last_login_at: null, created_at: "2026-09-15T00:00:00Z", row_version: 3,
};
const page = (items: AdminUser[]): AdminUserPage => ({ items, total: items.length, page: 1, page_size: 20 });

describe("registration", () => {
  const options = { "GET /api/v1/auth/registration-options": { body: { enabled: true, organization_name: "Local development organisation", departments: [{ id: "dept-1", name: "North Division" }], job_roles: [] } } };

  it("validates every field before sending and links the summary to fields", async () => {
    const calls = mockFetch({ ...signedOut, ...environment, ...options });
    renderAt("/register");
    const user = userEvent.setup();
    await user.click(await screen.findByRole("button", { name: "Create account" }));
    const summary = await screen.findByRole("alert");
    await waitFor(() => expect(document.activeElement).toBe(summary));
    expect(within(summary).getByRole("link", { name: /Registration ID/ }).getAttribute("href")).toBe("#registration_id");
    expect(within(summary).getByRole("link", { name: /Password: Use at least 12 characters/ })).toBeTruthy();
    expect(calls.some((c) => c.method === "POST")).toBe(false);
  });

  it("creates a learner account and continues to onboarding; the password is sent only in the body", async () => {
    const calls = mockFetch({
      ...signedOut,
      ...environment,
      ...options,
      "POST /api/v1/auth/register": { status: 201, body: { ...session, user: { ...me, job_role: null } } },
      "GET /api/v1/job-roles": { body: [] },
    });
    renderAt("/register");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("Full name"), "Asha Verma");
    await user.type(screen.getByLabelText("Email"), "asha@example.invalid");
    await user.type(screen.getByLabelText("Registration ID"), "STA-2026-0142");
    await user.selectOptions(screen.getByLabelText("Department (optional)"), "dept-1");
    await user.type(screen.getByLabelText("Password"), "a long enough phrase");
    await user.type(screen.getByLabelText("Confirm password"), "a long enough phrase");
    await user.click(screen.getByRole("button", { name: "Create account" }));
    expect(await screen.findByRole("heading", { level: 1, name: "Select your job role" })).toBeTruthy();
    const post = calls.find((c) => c.method === "POST" && c.url === "/api/v1/auth/register")!;
    expect(post.body).toEqual({ display_name: "Asha Verma", email: "asha@example.invalid", registration_id: "STA-2026-0142", password: "a long enough phrase", department_id: "dept-1" });
    expect(calls.every((c) => !c.url.includes("long"))).toBe(true);
  });

  it("shows duplicate email next to the field", async () => {
    mockFetch({
      ...signedOut, ...environment, ...options,
      "POST /api/v1/auth/register": { status: 409, body: { code: "EMAIL_IN_USE", title: "Email already registered", errors: [{ field: "email", code: "EMAIL_IN_USE", message: "Email already registered." }] } },
    });
    renderAt("/register");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("Full name"), "Asha Verma");
    await user.type(screen.getByLabelText("Email"), "asha@example.invalid");
    await user.type(screen.getByLabelText("Registration ID"), "STA-2026-0142");
    await user.type(screen.getByLabelText("Password"), "a long enough phrase");
    await user.type(screen.getByLabelText("Confirm password"), "a long enough phrase");
    await user.click(screen.getByRole("button", { name: "Create account" }));
    expect((await screen.findAllByText(/An account with this email already exists/)).length).toBeGreaterThan(0);
    expect(screen.getByLabelText("Email").getAttribute("aria-invalid")).toBe("true");
  });

  it("explains when registration is closed", async () => {
    mockFetch({ ...signedOut, "GET /api/v1/auth/registration-options": { body: { enabled: false, organization_name: null, departments: [], job_roles: [] } } });
    renderAt("/register");
    expect(await screen.findByText("Registration is not available here")).toBeTruthy();
    expect(screen.queryByRole("button", { name: "Create account" })).toBeNull();
  });
});

describe("set password", () => {
  it("reads the token from the fragment, sends it in the body and returns to sign in", async () => {
    const calls = mockFetch({ ...signedOut, "POST /api/v1/auth/password/set": { status: 204 } });
    renderAt("/set-password#token=one-time-token-value-123");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("New password"), "brand new password");
    await user.type(screen.getByLabelText("Confirm password"), "brand new password");
    await user.click(screen.getByRole("button", { name: "Set password" }));
    expect(await screen.findByText("Your password is set. Sign in with your new password.")).toBeTruthy();
    expect(calls.find((c) => c.method === "POST")!.body).toEqual({ token: "one-time-token-value-123", new_password: "brand new password" });
  });

  it("explains an invalid or used link", async () => {
    mockFetch({ ...signedOut, "POST /api/v1/auth/password/set": { status: 400, body: { code: "TOKEN_INVALID", title: "Link not valid" } } });
    renderAt("/set-password#token=used-token-value-12345");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("New password"), "brand new password");
    await user.type(screen.getByLabelText("Confirm password"), "brand new password");
    await user.click(screen.getByRole("button", { name: "Set password" }));
    expect(await screen.findByText("This link cannot be used.")).toBeTruthy();
  });

  it("handles a link without a token", async () => {
    mockFetch(signedOut);
    renderAt("/set-password");
    expect(await screen.findByText("This link is incomplete")).toBeTruthy();
  });
});

describe("profile", () => {
  it("changes the password with the current password and CSRF header", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/departments": { body: [] },
      "POST /api/v1/auth/password/change": { status: 204 },
    });
    renderAt("/profile");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("Current password"), "old password value");
    await user.type(screen.getByLabelText("New password"), "new password value");
    await user.type(screen.getByLabelText("Confirm new password"), "new password value");
    await user.click(screen.getByRole("button", { name: "Change password" }));
    await waitFor(() => expect(calls.some((c) => c.url === "/api/v1/auth/password/change")).toBe(true));
    const post = calls.find((c) => c.url === "/api/v1/auth/password/change")!;
    expect(post.headers["X-CSRF-Token"]).toBe("csrf-abc");
    expect(post.body).toEqual({ current_password: "old password value", new_password: "new password value" });
  });

  it("shows an incorrect current password on the field", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: session },
      "GET /api/v1/departments": { body: [] },
      "POST /api/v1/auth/password/change": { status: 422, body: { code: "CURRENT_PASSWORD_INCORRECT", title: "x", errors: [{ field: "current_password", code: "CURRENT_PASSWORD_INCORRECT", message: "Incorrect password." }] } },
    });
    renderAt("/profile");
    const user = userEvent.setup();
    await user.type(await screen.findByLabelText("Current password"), "wrong password value");
    await user.type(screen.getByLabelText("New password"), "new password value");
    await user.type(screen.getByLabelText("Confirm new password"), "new password value");
    await user.click(screen.getByRole("button", { name: "Change password" }));
    expect((await screen.findAllByText(/Incorrect password/)).length).toBeGreaterThan(0);
  });
});

describe("administration access", () => {
  it("never shows administration navigation or pages to a learner", async () => {
    const calls = mockFetch({ "GET /api/v1/auth/session": { body: session } });
    renderAt("/admin/users");
    expect(await screen.findByRole("heading", { level: 1, name: "No access to this page" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Go to your learning" }).getAttribute("href")).toBe("/");
    expect(calls.some((c) => c.url.startsWith("/api/v1/admin"))).toBe(false);
    expect(screen.queryByRole("link", { name: "Administration" })).toBeNull();
  });

  it("sends signed-out visitors of admin pages to the administration sign-in", async () => {
    mockFetch({ ...signedOut, ...environment });
    renderAt("/admin");
    expect(await screen.findByRole("button", { name: "Sign in to administration" })).toBeTruthy();
  });

  it("separates administration navigation from learning navigation", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: orgAdmin } },
      "GET /api/v1/admin/users?page_size=1": { body: page([learnerUser]) },
      "GET /api/v1/admin/users?status=active&page_size=1": { body: page([learnerUser]) },
      "GET /api/v1/admin/users?status=invited&page_size=1": { body: page([]) },
      "GET /api/v1/admin/users?status=inactive&page_size=1": { body: page([]) },
      "GET /api/v1/admin/departments": { body: [{ id: "dept-1", name: "North Division", code: "north", status: "active", user_count: 1 }] },
    });
    renderAt("/admin");
    const nav = await screen.findByRole("navigation", { name: "Administration" });
    expect(within(nav).getByRole("link", { name: "Users" })).toBeTruthy();
    expect(within(nav).getByRole("link", { name: "My learning" }).getAttribute("href")).toBe("/");
    expect(within(nav).queryByRole("link", { name: "Baseline assessment" })).toBeNull();
    expect(await screen.findByRole("link", { name: /Invited, not set up/ })).toBeTruthy();
  });

  it("adds a user and shows the one-time setup link with a fragment token", async () => {
    const calls = mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: orgAdmin } },
      "GET /api/v1/admin/users?page=1&page_size=20": { body: page([learnerUser]) },
      "GET /api/v1/admin/departments": { body: [{ id: "dept-1", name: "North Division", code: "north", status: "active", user_count: 1 }] },
      "POST /api/v1/admin/users": {
        status: 201,
        body: { user: { ...learnerUser, id: "user-10", display_name: "Ravi Kumar", status: "invited", has_password: false }, setup: { purpose: "account_setup", token: "setup-token-abc", expires_at: "2026-09-16T00:00:00Z" } },
      },
    });
    renderAt("/admin/users");
    const user = userEvent.setup();
    expect(await screen.findAllByText("Asha Verma")).toBeTruthy();
    await user.click(screen.getByRole("button", { name: "Add a user" }));
    const dialog = await screen.findByRole("dialog", { name: "Add a user" });
    await user.type(within(dialog).getByLabelText("Full name"), "Ravi Kumar");
    await user.type(within(dialog).getByLabelText("Email"), "ravi@example.invalid");
    await user.click(within(dialog).getByRole("checkbox", { name: "Trainer" }));
    await user.click(within(dialog).getByRole("button", { name: "Add user" }));
    const link = (await screen.findByLabelText("Set-password link")) as HTMLInputElement;
    expect(link.value).toMatch(/\/set-password#token=setup-token-abc$/);
    const post = calls.find((c) => c.method === "POST")!;
    expect(post.body).toMatchObject({ display_name: "Ravi Kumar", email: "ravi@example.invalid", roles: [{ role: "learner" }, { role: "trainer" }] });
  });

  it("blocks editing your own roles and platform administrator grants for an organisation administrator", async () => {
    const self: AdminUser = { ...learnerUser, id: "admin-1", display_name: "Demo Org Admin 01", roles: [{ role: "org_admin", department_scope_id: null }] };
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: orgAdmin } },
      "GET /api/v1/admin/users?page=1&page_size=20": { body: page([learnerUser, self]) },
      "GET /api/v1/admin/departments": { body: [] },
    });
    renderAt("/admin/users");
    const user = userEvent.setup();
    await user.click((await screen.findAllByRole("button", { name: "Manage Asha Verma" }))[0]);
    let dialog = await screen.findByRole("dialog", { name: "Asha Verma" });
    expect((within(dialog).getByRole("checkbox", { name: "Platform administrator" }) as HTMLInputElement).disabled).toBe(true);
    expect((within(dialog).getByRole("checkbox", { name: "Trainer" }) as HTMLInputElement).disabled).toBe(false);
    await user.click(within(dialog).getByRole("button", { name: "Cancel" }));
    await user.click((await screen.findAllByRole("button", { name: "Manage Demo Org Admin 01" }))[0]);
    dialog = await screen.findByRole("dialog", { name: "Demo Org Admin 01" });
    expect((within(dialog).getByRole("checkbox", { name: "Trainer" }) as HTMLInputElement).disabled).toBe(true);
    expect(within(dialog).queryByRole("button", { name: "Deactivate account" })).toBeNull();
  });

  it("renders the permission matrix from the API", async () => {
    mockFetch({
      "GET /api/v1/auth/session": { body: { ...session, user: orgAdmin } },
      "GET /api/v1/admin/roles": { body: [{ role: "auditor", label: "Auditor", description: "Read-only.", capabilities: ["audit.view"], user_count: 2, department_scoped: false }] },
    });
    renderAt("/admin/roles");
    const table = await screen.findByRole("table", { name: "Which access role holds which permission" });
    const auditRow = within(table).getByRole("row", { name: /Audit trail/ });
    expect(within(auditRow).getByText("Allowed")).toBeTruthy();
    expect(screen.getByRole("link", { name: "2 accounts" }).getAttribute("href")).toBe("/admin/users?role=auditor");
  });
});
