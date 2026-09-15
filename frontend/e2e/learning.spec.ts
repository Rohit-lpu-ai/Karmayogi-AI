import { expect, test, type Page } from "@playwright/test";
import { capture, completeOnboarding, createLearner, expectAccessible, signIn } from "./support";

/** Phase 4B journey: baseline -> learning path -> course -> lesson player -> complete every lesson -> progress. */

async function noHorizontalScroll(page: Page, context: string) {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow, `horizontal overflow on ${context}`).toBeLessThanOrEqual(0);
}

async function takeBaseline(page: Page) {
  await page.goto("/assessment");
  await page.getByRole("button", { name: "Start assessment" }).click();
  const heading = page.getByRole("heading", { level: 1, name: /^Question \d+ of \d+$/ });
  await expect(heading).toBeVisible();
  const total = Number((await heading.textContent())!.match(/of (\d+)/)![1]);
  for (let i = 1; i <= total; i++) {
    await expect(page.getByRole("heading", { level: 1, name: `Question ${i} of ${total}` })).toBeVisible();
    await page.getByRole("radio").first().check();
    await expect(page.getByText(`${i} of ${total} answered`)).toBeVisible();
    if (i < total) await page.getByRole("button", { name: "Next" }).click();
  }
  await expect(page.getByRole("status").filter({ hasText: /saved/i })).toContainText("All answers saved");
  await page.getByRole("button", { name: "Review and submit" }).first().click();
  await page.getByRole("dialog").getByRole("button", { name: "Submit answers" }).click();
  await expect(page.getByRole("heading", { level: 1, name: "Your baseline result" })).toBeVisible();
}

test("a learner follows the learning path, completes a course lesson by lesson, and sees progress", async ({ page }, testInfo) => {
  test.setTimeout(180_000);
  const failures: string[] = [];
  page.on("response", (r) => { if (r.status() >= 400 && r.status() !== 401) failures.push(`${r.status()} ${new URL(r.url()).pathname}`); });
  page.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) failures.push(m.text()); });
  const mobile = testInfo.project.name.startsWith("mobile");

  await signIn(page, createLearner());
  await completeOnboarding(page);

  // Before the baseline the path explains what to do
  await page.goto("/learning-path");
  await expect(page.getByText("Take your baseline assessment to build your path")).toBeVisible();
  await takeBaseline(page);

  // Learning path
  await page.goto("/learning-path");
  await expect(page.getByRole("heading", { level: 1, name: "Your learning path" })).toBeVisible();
  await expect(page.getByText("Up next")).toBeVisible();
  await expectAccessible(page, "learning path");
  await noHorizontalScroll(page, "learning path");
  await capture(page, testInfo, "4b-01-learning-path");

  // Open the up-next course hub
  await page.getByRole("link", { name: "Open course" }).click();
  await expect(page.getByText("Course contents", { exact: true })).toBeVisible();
  await expectAccessible(page, "course contents");
  await noHorizontalScroll(page, "course contents");
  await capture(page, testInfo, "4b-02-course-contents");
  await page.getByRole("button", { name: "Start course" }).click();

  // Lesson player: complete every lesson using the primary actions
  let completed = 0;
  for (let guard = 0; guard < 12; guard++) {
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await expect(page.getByText(/^Lesson \d+ of \d+/)).toBeVisible();
    if (completed === 0) {
      await expectAccessible(page, "lesson player");
      await noHorizontalScroll(page, "lesson player");
      await capture(page, testInfo, "4b-03-lesson-player");
      if (mobile) {
        await page.getByRole("button", { name: "Course contents" }).click();
        await expect(page.getByRole("dialog").locator('a[aria-current="page"]')).toBeVisible();
        await capture(page, testInfo, "4b-04-lesson-contents-drawer", false);
        await page.keyboard.press("Escape");
      }
    }
    const markComplete = page.getByRole("button", { name: "Mark as complete" });
    if (await markComplete.isVisible()) {
      await markComplete.click();
      await expect(markComplete).toBeHidden(); // saved
      completed++;
    }
    const next = page.getByRole("link", { name: /^Next:/ });
    if (await next.isVisible()) {
      await next.click();
      continue;
    }
    break;
  }
  await expect(page.getByText("Course complete")).toBeVisible();
  expect(completed).toBeGreaterThanOrEqual(2);
  await expectAccessible(page, "course complete");
  await capture(page, testInfo, "4b-05-course-complete");

  // Progress everywhere: path, catalogue filter, dashboard
  await page.goto("/learning-path");
  await expect(page.getByRole("link", { name: /^Review / }).first()).toBeVisible();
  await page.goto("/courses?progress=completed");
  await expect(page.getByRole("article")).toHaveCount(1);
  await expect(page.getByRole("article").getByText("Completed")).toBeVisible();
  await capture(page, testInfo, "4b-06-catalogue-completed");
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1, name: /Welcome back/ })).toBeVisible();
  await expect(page.getByText(/lessons completed/)).toBeVisible();
  await noHorizontalScroll(page, "dashboard");
  await capture(page, testInfo, "4b-07-dashboard-after-learning");

  await page.goto("/me/attempts");
  await expect(page.getByRole("heading", { level: 1, name: "Assessment history" })).toBeVisible();
  await expect(page.getByRole("link", { name: "View result" })).toBeVisible();
  await expectAccessible(page, "assessment history");
  await capture(page, testInfo, "4b-08-assessment-history");
  expect(failures).toEqual([]);
});
