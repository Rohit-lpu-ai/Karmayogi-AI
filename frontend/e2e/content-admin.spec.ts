import { expect, test, type Page } from "@playwright/test";
import { randomBytes } from "node:crypto";
import { capture, completeOnboarding, createLearner, expectAccessible, signIn, signInAs, signOut } from "./support";

/**
 * Phase 4C journeys: question authoring -> review by a different person; course preparation -> review -> publish ->
 * visible to a learner; read-only governance screens. Uses synthetic demo accounts.
 */

async function noHorizontalScroll(page: Page, context: string) {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow, `horizontal overflow on ${context}`).toBeLessThanOrEqual(0);
}

function watch(page: Page, expected: number[] = [401]) {
  const failures: string[] = [];
  page.on("response", (r) => { if (r.status() >= 400 && !expected.includes(r.status())) failures.push(`${r.status()} ${new URL(r.url()).pathname}`); });
  page.on("console", (m) => { if (m.type() === "error" && !/Failed to load resource/.test(m.text())) failures.push(m.text()); });
  return failures;
}

async function settle(page: Page) {
  await page.waitForTimeout(350); // dialog fade-in, so axe measures final colours
}

test("a trainer authors a question and a different reviewer approves it", async ({ page }, testInfo) => {
  test.setTimeout(150_000);
  const failures = watch(page);
  const stamp = randomBytes(3).toString("hex");
  const stem = `A district table reports training enrolment in thousands (ref ${stamp}). What does the value 12.5 represent?`;

  await signInAs(page, "trainer01@example.invalid");
  await page.goto("/admin/questions");
  await expect(page.getByRole("heading", { level: 1, name: "Questions" })).toBeVisible();
  await expectAccessible(page, "questions list");
  await noHorizontalScroll(page, "questions list");
  await capture(page, testInfo, "4c-01-questions");

  await page.getByRole("link", { name: "New question" }).click();
  await page.getByLabel("Competency", { exact: true }).selectOption({ index: 1 });
  await page.getByLabel("Question").fill(stem);
  await page.getByLabel("Option 1 text").fill("12.5 people");
  await page.getByLabel("Option 2 text").fill("12,500 people");
  await page.getByLabel("Option 3 text").fill("1,25,000 people");
  await page.getByLabel("Option 4 text").fill("125 people");
  await page.getByLabel("Option 2 is correct").check();
  await page.getByLabel("Explanation").fill("The unit is thousands, so 12.5 represents 12,500 people.");
  await page.getByRole("button", { name: "Add source" }).click();
  await page.getByLabel("Note").fill("Invented scenario and figures written for practice.");
  await expectAccessible(page, "question editor");
  await noHorizontalScroll(page, "question editor");
  await capture(page, testInfo, "4c-02-question-editor");
  await page.getByRole("button", { name: "Save draft" }).click();

  await expect(page.getByRole("heading", { level: 1, name: "Question" })).toBeVisible();
  await expect(page.getByText("Invented for practice - not a citation")).toBeVisible();
  await page.getByRole("button", { name: "Send for review" }).click();
  await expect(page.getByText("Waiting for review")).toBeVisible();
  await expectAccessible(page, "question detail");
  await capture(page, testInfo, "4c-03-question-in-review");

  await page.goto("/admin/review");
  const ownCard = page.getByRole("listitem").filter({ hasText: stamp });
  await expect(ownCard.getByText(/another reviewer must decide it/)).toBeVisible();
  await expect(ownCard.getByRole("button", { name: "Decide" })).toHaveCount(0);
  await signOut(page);

  await signInAs(page, "competency-admin01@example.invalid");
  await page.goto("/admin/review");
  const card = page.getByRole("listitem").filter({ hasText: stamp });
  await expectAccessible(page, "review queue");
  await capture(page, testInfo, "4c-04-review-queue");
  await card.getByRole("button", { name: "Decide" }).click();
  const dialog = page.getByRole("dialog", { name: "Decide review" });
  await settle(page);
  await expectAccessible(page, "decision dialog");
  await capture(page, testInfo, "4c-05-decision-dialog", false);
  await dialog.getByRole("button", { name: "Record decision" }).click();
  await expect(dialog).toBeHidden();

  await page.goto("/admin/review?status=decided");
  const decided = page.getByRole("listitem").filter({ hasText: stamp });
  await expect(decided.getByText("Approved", { exact: true })).toBeVisible();
  await decided.getByRole("link", { name: "Open question" }).click();
  await expect(page.getByText("Approved", { exact: true }).first()).toBeVisible();
  expect(failures).toEqual([]);
});

test("a course is prepared, reviewed by someone else, published, and then visible to learners", async ({ page }, testInfo) => {
  test.setTimeout(180_000);
  const failures = watch(page);
  const stamp = randomBytes(3).toString("hex");
  const title = `Units and footnotes clinic ${stamp}`;

  await signInAs(page, "training-manager01@example.invalid");
  await page.goto("/admin/courses");
  await expect(page.getByRole("heading", { level: 1, name: "Courses" })).toBeVisible();
  await expectAccessible(page, "courses list");
  await noHorizontalScroll(page, "courses list");
  await capture(page, testInfo, "4c-06-courses");

  await page.getByRole("link", { name: "New course" }).click();
  await page.getByLabel("Title").fill(title);
  await page.getByLabel("Description").fill("A short clinic on reading units and footnotes before quoting a figure. Synthetic example.");
  await page.getByLabel("Provider").fill("Internal training team (synthetic)");
  await page.getByLabel("Difficulty").selectOption("foundational");
  await page.getByLabel("Learning objectives").fill("Find the unit of a table\nRead footnotes before quoting");
  await page.getByRole("button", { name: "Create draft" }).click();

  await expect(page.getByRole("heading", { level: 1, name: title })).toBeVisible();
  await page.getByLabel("New module title").fill("Units first");
  await page.getByRole("button", { name: "Add module" }).click();
  await page.getByRole("button", { name: "Add lesson" }).click();
  const lessonDialog = page.getByRole("dialog", { name: "Add lesson" });
  await lessonDialog.getByLabel("Title").fill("Where the unit hides");
  await lessonDialog.getByLabel("Lesson text").fill("## Look for the unit\n\nUnits appear in the **title**, a column header, or a footnote.\n\n- thousands\n- lakh\n- percent");
  await lessonDialog.getByRole("button", { name: "Preview" }).click();
  await expect(lessonDialog.getByRole("heading", { name: "Look for the unit" })).toBeVisible();
  await settle(page);
  await expectAccessible(page, "lesson dialog");
  await capture(page, testInfo, "4c-07-lesson-dialog", false);
  await lessonDialog.getByRole("button", { name: "Save lesson" }).click();
  await expect(lessonDialog).toBeHidden();
  await page.getByLabel("Competency", { exact: true }).selectOption({ index: 1 });
  await page.getByRole("button", { name: "Link", exact: true }).click();
  await expect(page.getByText("Awaiting review")).toBeVisible();
  await page.waitForTimeout(600); // let confirmation toasts finish animating before measuring contrast
  await expectAccessible(page, "course detail draft");
  await noHorizontalScroll(page, "course detail");
  await capture(page, testInfo, "4c-08-course-draft");
  await page.getByRole("button", { name: "Send for review" }).click();
  await expect(page.getByText("In review").first()).toBeVisible();
  const courseUrl = page.url();
  await signOut(page);

  await signInAs(page, "org-admin01@example.invalid");
  await page.goto("/admin/review");
  await page.getByRole("listitem").filter({ hasText: title }).getByRole("button", { name: "Decide" }).click();
  await page.getByRole("dialog", { name: "Decide review" }).getByRole("button", { name: "Record decision" }).click();
  await expect(page.getByRole("dialog")).toBeHidden();
  await page.goto(courseUrl);
  await expect(page.getByText("Approved, not live")).toBeVisible();
  await page.getByRole("button", { name: "Publish to learners" }).click();
  await page.getByRole("dialog", { name: "Publish this course?" }).getByRole("button", { name: "Publish" }).click();
  await expect(page.getByText("Published", { exact: true }).first()).toBeVisible();
  await capture(page, testInfo, "4c-09-course-published");
  await signOut(page);

  await signIn(page, createLearner());
  await completeOnboarding(page);
  await page.goto(`/courses?q=${encodeURIComponent(stamp)}`);
  await expect(page.getByRole("article").filter({ hasText: title })).toBeVisible();

  // Clean up: unpublish the test course so the shared demo catalogue stays as seeded.
  await signOut(page);
  await signInAs(page, "org-admin01@example.invalid");
  await page.goto(courseUrl);
  await page.getByRole("button", { name: "Unpublish" }).click();
  const unpublish = page.getByRole("dialog", { name: "Unpublish this course?" });
  await unpublish.getByLabel(/Reason/).fill("Browser journey clean-up");
  await unpublish.getByRole("button", { name: "Unpublish" }).click();
  await expect(page.getByText("Approved, not live")).toBeVisible();
  expect(failures).toEqual([]);
});

test("governance screens: competencies, assessments and the audit trail are readable and accessible", async ({ page }, testInfo) => {
  const failures = watch(page);
  await signInAs(page, "competency-admin01@example.invalid");
  await page.goto("/admin/competencies");
  await expect(page.getByRole("heading", { level: 2, name: "Job-role requirements" })).toBeVisible();
  await expectAccessible(page, "competencies");
  await noHorizontalScroll(page, "competencies");
  await capture(page, testInfo, "4c-10-competencies");
  await page.goto("/admin/assessments");
  await expect(page.getByText("Quality checks").first()).toBeVisible();
  await expectAccessible(page, "assessments");
  await noHorizontalScroll(page, "assessments");
  await capture(page, testInfo, "4c-11-assessments");
  await signOut(page);

  await signInAs(page, "auditor01@example.invalid");
  await expect(page).toHaveURL(/\/admin$/);
  await page.goto("/admin/audit");
  await expect(page.getByRole("heading", { level: 1, name: "Audit trail" })).toBeVisible();
  await page.getByRole("list", { name: "Audit entries" }).getByRole("button").first().click();
  await expect(page.getByText("Reference").first()).toBeVisible();
  await expectAccessible(page, "audit trail");
  await noHorizontalScroll(page, "audit trail");
  await capture(page, testInfo, "4c-12-audit");
  await page.goto("/admin/courses");
  await expect(page.getByRole("heading", { level: 1, name: "No access to this page" })).toBeVisible();
  expect(failures).toEqual([]);
});
