import { defineConfig, devices } from "@playwright/test";

/**
 * Browser journeys against the real local stack (database + backend + Vite proxy).
 * Start the stack first (start-dev.bat), then: npm run e2e
 * Uses the installed Microsoft Edge (channel "msedge"), so no browser download is needed.
 * Screenshots for review: CAPTURE_SCREENSHOTS=1 npm run e2e  (written to docs/evidence/.../screenshots)
 */
const baseURL = process.env.E2E_BASE_URL ?? "http://localhost:5173";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 90_000,
  expect: { timeout: 10_000 },
  reporter: [["list"]],
  globalSetup: "./e2e/global-setup.ts",
  use: {
    baseURL,
    channel: "msedge",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "desktop", use: { ...devices["Desktop Edge"], viewport: { width: 1440, height: 900 } } },
    { name: "mobile-360", use: { ...devices["Desktop Edge"], viewport: { width: 360, height: 760 }, hasTouch: true } },
  ],
});
