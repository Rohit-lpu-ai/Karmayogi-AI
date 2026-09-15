const baseURL = process.env.E2E_BASE_URL ?? "http://localhost:5173";

/** Fail fast with a clear message when the local stack is not running. */
export default async function globalSetup() {
  let status = 0;
  let body = "";
  try {
    const response = await fetch(`${baseURL}/api/v1/auth/session`);
    status = response.status;
    body = await response.text();
  } catch {
    throw new Error(`The app is not reachable at ${baseURL}. Start it with start-dev.bat, then run the journeys again.`);
  }
  if (status !== 401 || !body.includes("urn:platform:problem")) {
    throw new Error(`${baseURL} did not answer like this platform's API (status ${status}). Is the backend running behind the Vite proxy?`);
  }
}
