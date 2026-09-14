import { afterEach, describe, expect, it, vi } from "vitest";
import { mockFetch } from "../test/fetchMock";
import { api, ApiError, setCsrfToken } from "./client";

afterEach(() => {
  setCsrfToken(null);
  vi.unstubAllGlobals();
});

describe("api client", () => {
  it("sends the CSRF token on state-changing requests only", async () => {
    const calls = mockFetch({ "GET /api/v1/me": { body: { ok: true } }, "PUT /api/v1/me/job-role": { body: { ok: true } } });
    setCsrfToken("csrf-123");
    await api("/api/v1/me");
    await api("/api/v1/me/job-role", { method: "PUT", body: { job_role_id: "r" } });
    expect(calls[0].headers["X-CSRF-Token"]).toBeUndefined();
    expect(calls[1].headers["X-CSRF-Token"]).toBe("csrf-123");
    expect(calls[1].body).toEqual({ job_role_id: "r" });
  });

  it("turns problem responses into ApiError with code and correlation ID", async () => {
    mockFetch({
      "POST /api/v1/auth/login": {
        status: 401,
        body: { code: "INVALID_CREDENTIALS", title: "Sign-in failed", detail: "Email or password is incorrect.", correlation_id: "corr-1" },
      },
    });
    const error = await api("/api/v1/auth/login", { method: "POST", body: {} }).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ status: 401, code: "INVALID_CREDENTIALS", detail: "Email or password is incorrect.", correlationId: "corr-1" });
  });

  it("exposes field errors from validation problems", async () => {
    mockFetch({
      "POST /api/v1/auth/login": {
        status: 422,
        body: { code: "VALIDATION_FAILED", title: "Validation failed", errors: [{ field: "email", code: "STRING_PATTERN_MISMATCH", message: "bad" }] },
      },
    });
    const error = (await api("/api/v1/auth/login", { method: "POST", body: {} }).catch((e: unknown) => e)) as ApiError;
    expect(error.fieldErrors[0].field).toBe("email");
  });

  it("reports network failures as NETWORK_ERROR", async () => {
    vi.stubGlobal("fetch", vi.fn(async () => {
      throw new TypeError("offline");
    }));
    await expect(api("/api/v1/me")).rejects.toMatchObject({ code: "NETWORK_ERROR", status: 0 });
  });

  it("returns undefined for 204 responses", async () => {
    mockFetch({ "POST /api/v1/auth/logout": { status: 204 } });
    await expect(api("/api/v1/auth/logout", { method: "POST" })).resolves.toBeUndefined();
  });
});
