import { expect, test, type Page } from "@playwright/test";
import { capture, completeOnboarding, createLearner, expectAccessible, signIn } from "./support";

async function noHorizontalScroll(page: Page) {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
}

async function goViaNavigation(page: Page, mobile: boolean, name: string) {
  if (mobile) {
    await page.getByRole("button", { name: "Open menu" }).click();
    await page.getByRole("dialog", { name: "Menu" }).getByRole("link", { name, exact: true }).click();
  } else {
    await page.getByRole("navigation", { name: "Main" }).getByRole("link", { name, exact: true }).click();
  }
}

test("login explains the product and is accessible", async ({ page }, testInfo) => {
  await page.goto("/login");
  await expect(page.getByRole("heading", { level: 1, name: "Sign in" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 2, name: /Know what your role needs/ })).toBeVisible();
  await expect(page.getByText(/Forgot your password\? Ask your administrator/)).toBeVisible();
  await expectAccessible(page, "login");
  await capture(page, testInfo, "c1-login");

  // Keyboard: submitting empty moves focus to the error summary; the password toggle is reachable
  await page.getByRole("button", { name: "Sign in" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("alert")).toBeFocused();
  await expect(page.getByRole("alert")).toContainText("Enter your email address.");
  await page.getByLabel("Password").fill("not-a-real-password");
  await page.getByRole("button", { name: "Show password" }).click();
  await expect(page.getByLabel("Password")).toHaveAttribute("type", "text");
  await expectAccessible(page, "login with errors");
  await noHorizontalScroll(page);
});

test("the learner loop: dashboard, competencies, gaps, catalogue and course detail", async ({ page }, testInfo) => {
  const mobile = testInfo.project.name.startsWith("mobile");
  await signIn(page, createLearner());
  await completeOnboarding(page);

  // Before the baseline: the dashboard asks for it
  await page.getByRole("link", { name: "Go to my dashboard" }).click();
  await expect(page.getByRole("heading", { level: 1, name: /Welcome back/ })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Take your baseline assessment" })).toBeVisible();
  await expect(page.getByRole("navigation", { name: "Your learning journey" })).toBeVisible();
  await expectAccessible(page, "dashboard before baseline");
  await capture(page, testInfo, "c2-dashboard-0-new-learner");

  // Take the baseline quickly (first displayed option each time; options are shuffled per attempt)
  await page.getByRole("link", { name: "Start baseline assessment" }).click();
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

  // Dashboard after the baseline
  await goViaNavigation(page, mobile, "Home");
  await expect(page.getByRole("heading", { level: 1, name: /Welcome back/ })).toBeVisible();
  await expect(page.getByRole("region", { name: "Priority gaps" })).toBeVisible();
  await expect(page.getByText("At required level", { exact: true })).toBeVisible();
  await expect(page.getByRole("region", { name: "Recent assessment activity" }).getByText("Completed baseline assessment")).toBeVisible();
  await expectAccessible(page, "dashboard after baseline");
  await capture(page, testInfo, "c2-dashboard-1-after-baseline");
  await noHorizontalScroll(page);

  // Competency profile
  await goViaNavigation(page, mobile, "My competencies");
  await expect(page.getByRole("heading", { level: 1, name: "My competencies" })).toBeVisible();
  const list = page.getByRole("region", { name: "Competencies for your role" });
  await expect(list.getByRole("listitem").filter({ hasText: "Estimated" })).toHaveCount(4);
  await list.getByText("What the levels mean").first().click();
  await expect(list.getByText("Level 3 - Proficient").first()).toBeVisible();
  await expectAccessible(page, "competency profile");
  await capture(page, testInfo, "c3-competency-profile");
  await noHorizontalScroll(page);

  // Gap analysis
  await goViaNavigation(page, mobile, "Gap analysis");
  await expect(page.getByRole("heading", { level: 1, name: "Gap analysis" })).toBeVisible();
  await expect(page.getByRole("heading", { name: "Required and estimated level" })).toBeVisible();
  const priority = page.getByRole("region", { name: "Priority gaps" });
  const hasGaps = (await priority.count()) > 0;
  if (hasGaps) {
    await expect(priority.getByText("Where you are now").first()).toBeVisible();
    await expect(priority.getByText("Why it matters in your role").first()).toBeVisible();
  }
  await page.getByRole("tab", { name: "Table" }).focus();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("table", { name: "Required and estimated level by competency" })).toBeVisible();
  await expectAccessible(page, "gap analysis");
  await page.getByRole("tab", { name: "Chart" }).click();
  await capture(page, testInfo, "c4-gap-analysis");
  await noHorizontalScroll(page);

  // Catalogue with a filter chosen from the keyboard
  await goViaNavigation(page, mobile, "Courses");
  await expect(page.getByRole("heading", { level: 1, name: "Course catalogue" })).toBeVisible();
  const catalogueStatus = page.getByRole("status").filter({ hasText: /\d+ courses/ });
  await expect(catalogueStatus).toBeVisible();
  const allCourses = (await catalogueStatus.textContent())!.match(/(\d+) courses/)![0]; // content admins may publish more
  expect(Number(allCourses.split(" ")[0])).toBeGreaterThanOrEqual(15);
  await expect(page.getByText(/This catalogue currently contains synthetic learning examples/)).toBeVisible();
  await expectAccessible(page, "catalogue");
  await capture(page, testInfo, "c5-catalogue");
  await page.getByLabel("Difficulty").selectOption("advanced");
  await expect(page).toHaveURL(/difficulty=advanced/);
  await expect(page.getByRole("status").filter({ hasText: /courses/ })).toContainText(/^\d courses?/);
  await page.getByLabel("Search", { exact: true }).fill("rebasing");
  await expect(page.getByRole("article")).toHaveCount(1);
  await page.getByRole("button", { name: "Clear filters" }).first().click();
  await expect(page.getByRole("status").filter({ hasText: /courses/ })).toContainText(allCourses);
  await noHorizontalScroll(page);

  // Course detail from the first card (recommended first when there are gaps)
  const firstCard = page.getByRole("article").first();
  const title = (await firstCard.getByRole("heading", { level: 3 }).textContent())!.trim();
  await firstCard.getByRole("link").click();
  await expect(page.getByRole("heading", { level: 1, name: title })).toBeVisible();
  await expect(page.getByRole("region", { name: "What you will learn" })).toBeVisible();
  await expect(page.getByRole("region", { name: "Course structure" }).getByText(/^Module 1:/)).toBeVisible();
  if (hasGaps) await expect(page.getByRole("region", { name: "Why this course is recommended for you" })).toBeVisible();
  await expectAccessible(page, "course detail");
  await capture(page, testInfo, "c6-course-detail");
  await noHorizontalScroll(page);
});
