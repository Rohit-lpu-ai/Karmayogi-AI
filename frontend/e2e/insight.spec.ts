import { expect, test, type Page } from "@playwright/test";
import { capture, expectAccessible, signInAs, signOut } from "./support";

/** Phase 4D: aggregated insight for administrators; small groups withheld; no personal data on screen. */

async function noHorizontalScroll(page: Page, context: string) {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow, `horizontal overflow on ${context}`).toBeLessThanOrEqual(0);
}

test("a training manager reads skill gaps and training needs without seeing any individual learner", async ({ page }, testInfo) => {
  const failures: string[] = [];
  page.on("response", (r) => { if (r.status() >= 400 && r.status() !== 401) failures.push(`${r.status()} ${new URL(r.url()).pathname}`); });

  await signInAs(page, "training-manager01@example.invalid");
  await expect(page.getByRole("heading", { level: 2, name: /Learning across the organisation/ })).toBeVisible();
  await expectAccessible(page, "admin overview with insight");
  await capture(page, testInfo, "4d-01-overview");

  await page.goto("/admin/skill-gaps");
  const table = page.getByRole("table");
  await expect(table.getByRole("row", { name: /Survey Operations Division/ })).toBeVisible();
  await expect(table.getByRole("row", { name: /Data Services Unit/ }).getByText("learners assessed; withheld").first()).toBeAttached();
  await expect(page.getByText(/Figures for fewer than 5 learners are withheld/)).toBeVisible();
  expect(await page.locator("body").textContent()).not.toMatch(/@example\.invalid|Cohort Learner/);
  await expectAccessible(page, "skill gaps");
  await noHorizontalScroll(page, "skill gaps");
  await capture(page, testInfo, "4d-02-skill-gaps");

  await page.getByLabel("Job role").selectOption({ label: "Price Statistics Analyst" });
  await expect(table.getByRole("row", { name: /Price Statistics Division/ })).toBeVisible();
  await expect(table.getByRole("row", { name: /Survey Operations Division/ })).toHaveCount(0);

  await page.goto("/admin/training-needs");
  await expect(page.getByRole("heading", { level: 1, name: "Training needs" })).toBeVisible();
  await expect(page.getByText(/learners with a gap/).first()).toBeVisible();
  await expectAccessible(page, "training needs");
  await noHorizontalScroll(page, "training needs");
  await capture(page, testInfo, "4d-03-training-needs");
  await signOut(page);

  // Roles without insight cannot open it
  await signInAs(page, "auditor01@example.invalid");
  await page.goto("/admin/skill-gaps");
  await expect(page.getByRole("heading", { level: 1, name: "No access to this page" })).toBeVisible();
  const status = await page.evaluate(async () => (await fetch("/api/v1/admin/insight/skill-gaps")).status);
  expect(status).toBe(403);
  expect(failures.filter((f) => !f.startsWith("403 /api/v1/admin/insight"))).toEqual([]);
});
