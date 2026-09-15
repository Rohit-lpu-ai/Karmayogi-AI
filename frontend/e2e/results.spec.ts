import { expect, test } from "@playwright/test";
import { capture, completeOnboarding, createLearner, expectAccessible, signIn } from "./support";

test("after submitting, the result explains the outcome and what to do next", async ({ page }, testInfo) => {
  await signIn(page, createLearner());
  await completeOnboarding(page);
  await page.getByRole("button", { name: "Continue to the assessment" }).click();
  await page.getByRole("button", { name: "Start assessment" }).click();

  // Answer every question (alternating options so the result has a mix), then submit.
  const heading = page.getByRole("heading", { level: 1, name: /^Question \d+ of \d+$/ });
  await expect(heading).toBeVisible();
  const total = Number((await heading.textContent())!.match(/of (\d+)/)![1]);
  for (let i = 1; i <= total; i++) {
    await expect(page.getByRole("heading", { level: 1, name: `Question ${i} of ${total}` })).toBeVisible();
    await page.getByRole("radio").nth(i % 4).check();
    await expect(page.getByText(`${i} of ${total} answered`)).toBeVisible();
    if (i < total) await page.getByRole("button", { name: "Next" }).click();
  }
  await expect(page.getByRole("status").filter({ hasText: /saved/i })).toContainText("All answers saved");
  await page.getByRole("button", { name: "Review and submit" }).first().click();
  const dialog = page.getByRole("dialog", { name: "Submit your answers?" });
  await expect(dialog.getByText(`${total} of ${total} questions answered`)).toBeVisible();
  await dialog.getByRole("button", { name: "Submit answers" }).click();

  // Result: outcome first, labelled as development guidance and demo content
  await expect(page.getByRole("heading", { level: 1, name: "Your baseline result" })).toBeVisible();
  await expect(page.getByRole("img", { name: /^Overall score \d+ out of 100$/ })).toBeVisible();
  await expect(page.getByText("Development guidance, not an appraisal")).toBeVisible();
  await expect(page.getByText("DEMO - synthetic").first()).toBeVisible();
  const meaning = page.getByRole("region", { name: "What this means" });
  await expect(meaning.getByRole("term").filter({ hasText: "Developing" })).toBeVisible();
  const byCompetency = page.getByRole("region", { name: "Result by competency" });
  expect(await byCompetency.getByRole("listitem").count()).toBeGreaterThanOrEqual(2); // one card per role competency
  await expect(byCompetency.getByText("Estimated level").first()).toBeVisible();
  const next = page.getByRole("region", { name: "What to do next" });
  await expect(next.getByRole("link", { name: "See recommended learning" })).toBeVisible();
  await expect(page.getByText(/score-v1/)).toHaveCount(0); // method version only inside the disclosure
  await expectAccessible(page, "result page");
  await capture(page, testInfo, "b3-result-1-page");

  // Methodology disclosure and answer review, by keyboard
  const how = page.getByRole("button", { name: "How was this calculated?" });
  await how.focus();
  await page.keyboard.press("Enter");
  await expect(how).toHaveAttribute("aria-expanded", "true");
  await expect(page.getByText(/foundational 1, intermediate 1.5, advanced 2/)).toBeVisible();
  const firstQuestion = page.getByRole("region", { name: "Your answers" }).locator("summary").first();
  await firstQuestion.focus();
  await page.keyboard.press("Enter");
  await expect(page.getByText("Your answer:").first()).toBeVisible();
  await expectAccessible(page, "result page with disclosures open");
  await capture(page, testInfo, "b3-result-2-details");

  // Next step links land on the finished destinations (Phase C)
  await next.getByRole("link", { name: "See recommended learning" }).click();
  await expect(page).toHaveURL(/\/courses$/);
  await expect(page.getByRole("heading", { level: 1, name: "Course catalogue" })).toBeVisible();

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});
