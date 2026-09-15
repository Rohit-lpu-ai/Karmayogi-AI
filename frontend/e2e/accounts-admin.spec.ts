import { expect, test, type Page } from "@playwright/test";
import { randomBytes } from "node:crypto";
import { capture, createLearner, expectAccessible, signIn } from "./support";

/**
 * Phase 4A journeys: learner registration, sign-in entry points, profile, and user administration.
 * Passwords for newly created accounts are random per run and never printed.
 */

const ADMIN_EMAIL = process.env.E2E_ADMIN_EMAIL ?? "org-admin01@example.invalid";

function unique(prefix: string) {
  const stamp = new Date().toISOString().replace(/\D/g, "").slice(0, 14);
  return `${prefix}-${stamp}-${randomBytes(3).toString("hex")}`;
}

async function expectNoHorizontalScroll(page: Page, context: string) {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow, `horizontal overflow on ${context}`).toBeLessThanOrEqual(0);
}

/** Console errors plus failed responses, except statuses a journey provokes on purpose. */
function watchConsole(page: Page, expected: number[] = [401]) {
  const errors: string[] = [];
  page.on("console", (message) => {
    if (message.type() === "error" && !/Failed to load resource/.test(message.text())) errors.push(message.text());
  });
  page.on("response", (response) => {
    if (response.status() >= 400 && !expected.includes(response.status())) errors.push(`${response.status()} ${new URL(response.url()).pathname}`);
  });
  return errors;
}

test("a new learner registers, is signed in, onboards and cannot reach administration", async ({ page }, testInfo) => {
  const errors = watchConsole(page, [401, 403, 409]);
  const email = `${unique("e2e-reg")}@example.invalid`;
  const password = randomBytes(12).toString("base64url");

  await page.goto("/login");
  await page.getByRole("link", { name: "Create a learner account" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Create a learner account" })).toBeVisible();
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page.getByRole("alert")).toBeFocused();
  await expectAccessible(page, "registration with errors");
  await capture(page, testInfo, "4a-01-register-errors");

  await page.getByLabel("Full name").fill("Asha Verma (e2e)");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Registration ID").fill(unique("STA").toUpperCase());
  const department = page.getByLabel("Department (optional)");
  if ((await department.locator("option").count()) > 1) await department.selectOption({ label: "Demo Department (synthetic)" }); // not the insight cohort's departments
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByLabel("Confirm password").fill(password);
  await expectNoHorizontalScroll(page, "registration");
  await capture(page, testInfo, "4a-02-register-filled");
  await page.getByRole("button", { name: "Create account" }).click();

  await expect(page).toHaveURL(/\/get-started$/);
  await expect(page.getByRole("button", { name: "Get started" })).toBeVisible();

  await page.goto("/admin/users");
  await expect(page.getByRole("heading", { level: 1, name: "No access to this page" })).toBeVisible();
  const status = await page.evaluate(async () => (await fetch("/api/v1/admin/users")).status);
  expect(status).toBe(403);
  await expectAccessible(page, "admin page as learner");
  await capture(page, testInfo, "4a-03-learner-blocked-from-admin");

  // Registering again with the same email is refused and explained on the field.
  await page.goto("/profile");
  await page.getByRole("button", { name: /Account menu/ }).click();
  await page.getByRole("menuitem", { name: "Sign out" }).click();
  await page.goto("/register");
  await page.getByLabel("Full name").fill("Duplicate person");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Registration ID").fill(unique("DUP").toUpperCase());
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page.getByLabel("Confirm password").fill(password);
  await page.getByRole("button", { name: "Create account" }).click();
  await expect(page.getByLabel("Email")).toHaveAttribute("aria-invalid", "true");
  expect(errors).toEqual([]);
});

test("the profile shows account details and changes the password", async ({ page }, testInfo) => {
  const errors = watchConsole(page);
  const email = createLearner();
  await signIn(page, email);
  await expect(page).toHaveURL(/\/get-started$/);
  await page.goto("/profile");
  await expect(page.getByRole("heading", { level: 1, name: "Your profile" })).toBeVisible();
  await page.getByRole("button", { name: "Change password" }).click();
  await expect(page.getByRole("alert")).toBeFocused();
  await expectAccessible(page, "profile with password errors");
  await expectNoHorizontalScroll(page, "profile");
  await capture(page, testInfo, "4a-04-profile");
  expect(errors).toEqual([]);
});

test("an administrator signs in to administration, adds a user, and the user sets a password with the one-time link", async ({ page, browser }, testInfo) => {
  const errors = watchConsole(page);
  await page.goto("/login");
  await page.getByRole("button", { name: "Administration" }).click();
  await expectAccessible(page, "sign-in administration mode");
  await capture(page, testInfo, "4a-05-login-admin-mode");
  await expect(page).toHaveURL(/\/login\?as=admin$/);
  await signInAsAdmin(page);

  await expect(page).toHaveURL(/\/admin$/);
  await expect(page.getByRole("heading", { level: 1, name: "Overview" })).toBeVisible();
  const mobile = (page.viewportSize()?.width ?? 1440) < 1024;
  if (mobile) {
    await page.getByRole("button", { name: "Open menu" }).click();
    await expect(page.getByRole("dialog").getByRole("navigation", { name: "Administration" })).toBeVisible();
    await capture(page, testInfo, "4a-06b-admin-menu", false);
    await page.keyboard.press("Escape");
  } else {
    await expect(page.getByRole("navigation", { name: "Administration" })).toBeVisible();
  }
  await expect(page.getByRole("link", { name: /User accounts/ })).toBeVisible();
  await expectAccessible(page, "admin overview");
  await expectNoHorizontalScroll(page, "admin overview");
  await capture(page, testInfo, "4a-06-admin-overview");

  await page.goto("/admin/users");
  await expect(page.getByRole("heading", { level: 1, name: "Users" })).toBeVisible();
  await expectAccessible(page, "admin users");
  await expectNoHorizontalScroll(page, "admin users");
  await capture(page, testInfo, "4a-07-admin-users");

  const name = unique("Ravi E2E");
  const email = `${unique("e2e-invite")}@example.invalid`;
  await page.getByRole("button", { name: "Add a user" }).click();
  const dialog = page.getByRole("dialog", { name: "Add a user" });
  await dialog.getByLabel("Full name").fill(name);
  await dialog.getByLabel("Email").fill(email);
  await dialog.getByRole("checkbox", { name: "Trainer" }).check();
  await expectAccessible(page, "add user dialog");
  await capture(page, testInfo, "4a-08-admin-add-user", false);
  await dialog.getByRole("button", { name: "Add user" }).click();

  const linkField = page.getByLabel("Set-password link");
  await expect(linkField).toBeVisible();
  const link = await linkField.inputValue();
  expect(link).toMatch(/\/set-password#token=/);
  await capture(page, testInfo, "4a-09-admin-setup-link");

  // The invited person, in a separate browser context with no admin session.
  const invitee = await browser.newContext({ viewport: page.viewportSize() ?? undefined });
  const invitePage = await invitee.newPage();
  const password = randomBytes(12).toString("base64url");
  await invitePage.goto(link);
  await expect(invitePage).toHaveURL(/\/set-password$/); // the token is removed from the address bar
  await invitePage.getByLabel("New password").fill(password);
  await invitePage.getByLabel("Confirm password").fill(password);
  await expectAccessible(invitePage, "set password");
  await capture(invitePage, testInfo, "4a-10-set-password");
  await invitePage.getByRole("button", { name: "Set password" }).click();
  await expect(invitePage.getByText("Your password is set.")).toBeVisible();
  await invitePage.getByLabel("Email").fill(email);
  await invitePage.getByLabel("Password").fill(password);
  await invitePage.getByRole("button", { name: "Sign in", exact: true }).click();
  await expect(invitePage).toHaveURL(/\/get-started$/);

  // Reusing the link fails.
  await invitePage.goto(link);
  await invitePage.getByLabel("New password").fill(password);
  await invitePage.getByLabel("Confirm password").fill(password);
  await invitePage.getByRole("button", { name: "Set password" }).click();
  await expect(invitePage.getByText("This link cannot be used.")).toBeVisible();
  await invitee.close();

  // Deactivate the new account from the admin side.
  await page.getByRole("button", { name: "Done" }).click();
  await page.getByRole("searchbox", { name: "Search" }).fill(email);
  await page.getByRole("button", { name: "Search", exact: true }).click();
  await page.getByRole("button", { name: `Manage ${name}` }).first().click();
  const manage = page.getByRole("dialog", { name });
  await expect(manage.getByRole("button", { name: "Deactivate account" })).toBeVisible();
  await page.waitForTimeout(400); // let the dialog fade-in finish so axe measures final colours
  await expectAccessible(page, "manage user dialog");
  await capture(page, testInfo, "4a-11-admin-manage-user", false);
  await manage.getByRole("button", { name: "Deactivate account" }).click();
  await expect(manage.getByText("Inactive", { exact: true })).toBeVisible();
  await manage.getByRole("button", { name: "Cancel" }).click();

  await page.goto("/admin/roles");
  await expect(page.getByRole("table", { name: "Which access role holds which permission" })).toBeVisible();
  await expectAccessible(page, "roles and permissions");
  await expectNoHorizontalScroll(page, "roles and permissions");
  await capture(page, testInfo, "4a-12-admin-roles");
  expect(errors).toEqual([]);
});

async function signInAsAdmin(page: Page) {
  const { readFileSync } = await import("node:fs");
  const { join } = await import("node:path");
  const { REPO_ROOT } = await import("./support");
  const line = readFileSync(join(REPO_ROOT, ".env"), "utf8").split(/\r?\n/).find((l) => l.startsWith("DEMO_USER_PASSWORD="));
  const password = process.env.DEMO_USER_PASSWORD ?? line?.slice("DEMO_USER_PASSWORD=".length) ?? "";
  await page.getByLabel("Email").fill(ADMIN_EMAIL);
  await page.getByLabel("Password").fill(password);
  await page.getByRole("button", { name: "Sign in to administration" }).click();
}
