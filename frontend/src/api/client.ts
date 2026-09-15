/**
 * Minimal API client: same-origin cookies, CSRF header on state-changing requests,
 * and RFC 9457 problem responses turned into typed errors.
 * Authorisation is enforced by the server; this client never decides permissions.
 */

export interface FieldError {
  field: string;
  code: string;
  message: string;
}

export class ApiError extends Error {
  readonly status: number;
  readonly code: string;
  readonly detail: string | undefined;
  readonly correlationId: string | undefined;
  readonly fieldErrors: FieldError[];

  constructor(status: number, code: string, title: string, detail?: string, correlationId?: string, fieldErrors: FieldError[] = []) {
    super(detail ?? title);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.detail = detail;
    this.correlationId = correlationId;
    this.fieldErrors = fieldErrors;
  }
}

let csrfToken: string | null = null;

export function setCsrfToken(token: string | null): void {
  csrfToken = token;
}

type Method = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

export async function api<T>(path: string, options: { method?: Method; body?: unknown } = {}): Promise<T> {
  const method = options.method ?? "GET";
  const headers: Record<string, string> = { Accept: "application/json" };
  if (options.body !== undefined) headers["Content-Type"] = "application/json";
  if (method !== "GET" && csrfToken) headers["X-CSRF-Token"] = csrfToken;

  let response: Response;
  try {
    response = await fetch(path, {
      method,
      headers,
      credentials: "same-origin",
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
    });
  } catch {
    throw new ApiError(0, "NETWORK_ERROR", "Network error", "The service could not be reached. Check your connection and try again.");
  }

  if (response.status === 204) return undefined as T;
  const text = await response.text();
  let payload: unknown = null;
  try {
    payload = text ? JSON.parse(text) : null;
  } catch {
    payload = null;
  }

  if (!response.ok) {
    const problem = (payload ?? {}) as { code?: string; title?: string; detail?: string; correlation_id?: string; errors?: FieldError[] };
    throw new ApiError(
      response.status,
      problem.code ?? "HTTP_ERROR",
      problem.title ?? "Request failed",
      problem.detail,
      problem.correlation_id ?? response.headers.get("x-correlation-id") ?? undefined,
      problem.errors ?? [],
    );
  }
  return payload as T;
}
