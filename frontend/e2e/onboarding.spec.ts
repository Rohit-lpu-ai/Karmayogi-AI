import { expect, test } from "@playwright/test";
import { capture, createLearner, expectAccessible, signIn } from "./support";

test("a new learner completes onboarding with the keyboard", async ({ page }, testInfo) => {
  const email = createLearner();
  await signIn(page, email);

  // Step 1: welcome
  await expect(page.getByRole("heading", { level: 1, name: /Welcome, E2E Learner/ })).toBeVisible();
  await expect(page.getByRole("heading", { name: "How the platform helps you" })).toBeVisible();
  await expectAccessible(page, "onboarding welcome");
  await capture(page, testInfo, "b1-onboarding-1-welcome");
  await page.getByRole("button", { name: "Get started" }).focus();
  await page.keyboard.press("Enter");

  // Step 2: demo data and notice; focus moves to the step heading
  const noticeHeading = page.getByRole("heading", { level: 1, name: "Your data and this demo" });
  await expect(noticeHeading).toBeFocused();
  await expect(page.getByRole("heading", { name: "You are using a demo environment" })).toBeVisible();
  await expect(page.getByRole("button", { name: "Acknowledge and continue" })).toBeDisabled();
  await expectAccessible(page, "onboarding notice");
  await capture(page, testInfo, "b1-onboarding-2-notice");
  await page.getByRole("checkbox", { name: /learning and development only/ }).focus();
  await page.keyboard.press("Space");
  await page.getByRole("button", { name: "Acknowledge and continue" }).focus();
  await page.keyboard.press("Enter");

  // Step 3: job role, chosen with the keyboard
  await expect(page.getByRole("heading", { level: 1, name: "Select your job role" })).toBeFocused();
  const firstRole = page.getByRole("radio").first();
  await firstRole.focus();
  await page.keyboard.press("Space");
  await expect(firstRole).toBeChecked();
  await expect(page.getByRole("heading", { name: "What this role requires" })).toBeVisible();
  await expectAccessible(page, "onboarding job role");
  await capture(page, testInfo, "b1-onboarding-3-role");
  await page.getByRole("button", { name: "Confirm job role" }).click();

  // Step 4: assessment explained, then the learner can continue
  await expect(page.getByRole("heading", { level: 1, name: "Your baseline assessment" })).toBeFocused();
  await expect(page.getByText(/multiple choice/)).toBeVisible();
  await expectAccessible(page, "onboarding assessment step");
  await capture(page, testInfo, "b1-onboarding-4-assessment");
  await expect(page.getByRole("button", { name: "Continue to the assessment" })).toBeVisible();

  // No horizontal page scroll at this width (UI_UX_SPEC.md §4)
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});
