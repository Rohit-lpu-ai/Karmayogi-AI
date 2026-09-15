import AxeBuilder from "@axe-core/playwright";
import { expect, type Page, type TestInfo } from "@playwright/test";
import { execFileSync } from "node:child_process";
import { mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
export const REPO_ROOT = resolve(here, "..", "..");
const BACKEND = join(REPO_ROOT, "backend");
// Phase evidence folder for review screenshots; override with CAPTURE_PHASE (e.g. product-upgrade-phase-b).
const SCREENSHOT_DIR = join(REPO_ROOT, "docs", "evidence", "implementation", process.env.CAPTURE_PHASE ?? "product-upgrade-phase-c", "screenshots");

function demoPassword(): string {
  if (process.env.DEMO_USER_PASSWORD) return process.env.DEMO_USER_PASSWORD;
  const line = readFileSync(join(REPO_ROOT, ".env"), "utf8").split(/\r?\n/).find((l) => l.startsWith("DEMO_USER_PASSWORD="));
  if (!line) throw new Error("DEMO_USER_PASSWORD is not set in the environment or the repository .env");
  return line.slice("DEMO_USER_PASSWORD=".length);
}

/** A brand-new synthetic learner (no notice acknowledgement, no job role) created by backend/scripts/e2e_learner.py. */
export function createLearner(): string {
  const python = join(BACKEND, ".venv", "Scripts", "python.exe");
  const out = execFileSync(python, ["scripts/e2e_learner.py", "--org-code", process.env.E2E_ORG_CODE ?? "local-demo"], {
    cwd: BACKEND,
    encoding: "utf8",
  });
  return (JSON.parse(out.trim().split(/\r?\n/).pop()!) as { email: string }).email;
}

export async function signIn(page: Page, email: string) {
  await page.goto("/login");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password").fill(demoPassword());
  await page.getByRole("button", { name: "Sign in" }).click();
}

/** Automated accessibility check: no serious or critical axe violations (MVP-F4, invariant M-14). */
export async function expectAccessible(page: Page, context: string) {
  // Toasts are transient and animate in; their resting colours are the card tokens checked elsewhere.
  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).exclude("[data-sonner-toaster]").analyze();
  const blocking = results.violations.filter((v) => v.impact === "serious" || v.impact === "critical");
  const summary = blocking.map((v) => `${v.id} (${v.impact}): ${v.help} -> ${v.nodes.map((n) => n.target.join(" ")).slice(0, 3).join(" | ")}`);
  expect(summary, `axe violations on ${context}`).toEqual([]);
}

/** Saves a review screenshot into the phase evidence folder when CAPTURE_SCREENSHOTS=1. */
export async function capture(page: Page, testInfo: TestInfo, name: string, fullPage = true) {
  if (process.env.CAPTURE_SCREENSHOTS !== "1") return;
  mkdirSync(SCREENSHOT_DIR, { recursive: true });
  await page.evaluate(() => window.scrollTo(0, 0)); // keep sticky header and sidebar at the top of full-page captures
  await page.waitForTimeout(350); // let the 300 ms delayed skeletons and transitions settle
  await page.screenshot({ path: join(SCREENSHOT_DIR, `${name}-${testInfo.project.name}.png`), fullPage });
}

/** Walks the onboarding quickly (used by journeys that start after onboarding). */
export async function completeOnboarding(page: Page) {
  await page.getByRole("button", { name: "Get started" }).click();
  await page.getByRole("checkbox", { name: /learning and development only/ }).check();
  await page.getByRole("button", { name: "Acknowledge and continue" }).click();
  await page.getByRole("radio").first().check();
  await page.getByRole("button", { name: "Confirm job role" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Your baseline assessment" })).toBeVisible();
}

/** Signs in a synthetic account through the given entry point and waits until the app has navigated away. */
export async function signInAs(page: Page, email: string, mode: "learner" | "admin" = "admin") {
  await page.goto(mode === "admin" ? "/login?as=admin" : "/login");
  await page.getByLabel("Email").fill(email);
  await page.getByLabel("Password").fill(demoPassword());
  await page.getByRole("button", { name: mode === "admin" ? "Sign in to administration" : "Sign in", exact: true }).click();
  await expect(page).not.toHaveURL(/\/login/);
}

export async function signOut(page: Page) {
  await page.getByRole("button", { name: /Account menu/ }).click();
  await page.getByRole("menuitem", { name: "Sign out" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Sign in" })).toBeVisible();
  await expect(page.getByRole("button", { name: /Account menu/ })).toHaveCount(0);
}
