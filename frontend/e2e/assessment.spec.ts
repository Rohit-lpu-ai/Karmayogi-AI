import { expect, test } from "@playwright/test";
import { capture, completeOnboarding, createLearner, expectAccessible, signIn } from "./support";

test("a learner takes the baseline assessment with the keyboard and submits it", async ({ page }, testInfo) => {
  const mobile = testInfo.project.name.startsWith("mobile");
  await signIn(page, createLearner());
  await completeOnboarding(page);
  await page.getByRole("button", { name: "Continue to the assessment" }).click();

  // Introduction
  await expect(page.getByRole("heading", { level: 1, name: "Baseline assessment" })).toBeVisible();
  await expect(page.getByText("Not started")).toBeVisible();
  await expectAccessible(page, "assessment introduction");
  await capture(page, testInfo, "b2-assessment-1-intro");
  await page.getByRole("button", { name: "Start assessment" }).click();

  // Question 1: one question on screen, answered with arrow keys on the native radio group
  await expect(page.getByRole("heading", { level: 1, name: /^Question 1 of \d+$/ })).toBeVisible();
  await expect(page).toHaveURL(/\/assessment\/attempts\/[0-9a-f-]+/);
  const total = Number((await page.getByRole("heading", { level: 1 }).textContent())!.match(/of (\d+)/)![1]);
  await expect(page.getByRole("radio")).toHaveCount(4);
  await page.getByRole("radio").first().focus();
  await page.keyboard.press("Space");
  await expect(page.getByRole("status").filter({ hasText: /saved/i })).toContainText("All answers saved");
  await expect(page.getByText(`1 of ${total} answered`)).toBeVisible();
  await expectAccessible(page, "assessment question");
  await capture(page, testInfo, "b2-assessment-2-question", false);

  // Next moves focus to the new question heading; a keyboard user continues without the mouse
  await page.getByRole("button", { name: "Next" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("heading", { level: 1, name: `Question 2 of ${total}` })).toBeFocused();
  await page.getByRole("radio").nth(1).focus();
  await page.keyboard.press("Space");
  await expect(page.getByText(`2 of ${total} answered`)).toBeVisible();

  // Reload keeps the place and the saved answers (server is authoritative)
  await page.reload();
  await expect(page.getByRole("heading", { level: 1, name: `Question 2 of ${total}` })).toBeVisible();
  await expect(page.getByRole("radio").nth(1)).toBeChecked();

  // Question grid: jump to the last question
  if (mobile) await page.getByRole("button", { name: /All questions/ }).click();
  const gridScope = mobile ? page : page.getByRole("complementary", { name: "Question overview" });
  await expect(gridScope.getByRole("button", { name: "Question 1, answered" })).toBeVisible();
  await expect(gridScope.getByRole("button", { name: "Question 3, not answered" })).toBeVisible();
  if (!mobile) await capture(page, testInfo, "b2-assessment-3-grid", false);
  await gridScope.getByRole("button", { name: new RegExp(`^Question ${total}, not answered`) }).click();
  await expect(page.getByRole("heading", { level: 1, name: `Question ${total} of ${total}` })).toBeVisible();

  // Review: confirmation lists unanswered questions; Escape keeps answering
  await page.getByRole("button", { name: "Review and submit" }).first().click();
  const dialog = page.getByRole("dialog", { name: "Submit your answers?" });
  await expect(dialog).toBeVisible();
  await expect(dialog.getByText(`2 of ${total} questions answered`)).toBeVisible();
  await expect(dialog.getByRole("button", { name: "Go to question 3" })).toBeVisible();
  await expectAccessible(page, "submit confirmation");
  await capture(page, testInfo, "b2-assessment-4-confirm", false);
  await page.keyboard.press("Escape");
  await expect(dialog).toBeHidden();

  // Submit
  await page.getByRole("button", { name: "Review and submit" }).first().click();
  await dialog.getByRole("button", { name: "Submit answers" }).click();
  await expect(page).toHaveURL(/\/attempts\/[0-9a-f-]+\/result/);

  // The attempt cannot be reopened for answering
  await page.goBack();
  await expect(page).toHaveURL(/\/result/);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});
