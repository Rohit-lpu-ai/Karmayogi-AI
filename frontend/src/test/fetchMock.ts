import { vi } from "vitest";

export interface Call {
  method: string;
  url: string;
  headers: Record<string, string>;
  body: unknown;
}

type Handler = (call: Call) => { status?: number; body?: unknown };

/** Routes fetch calls by "METHOD path" to canned responses and records every call. */
export function mockFetch(routes: Record<string, Handler | { status?: number; body?: unknown }>) {
  const calls: Call[] = [];
  const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === "string" ? input : input.toString();
    const method = (init?.method ?? "GET").toUpperCase();
    const call: Call = {
      method,
      url,
      headers: (init?.headers ?? {}) as Record<string, string>,
      body: init?.body ? JSON.parse(String(init.body)) : undefined,
    };
    calls.push(call);
    const route = routes[`${method} ${url}`];
    if (!route) {
      return new Response(JSON.stringify({ code: "NOT_FOUND", title: "Not found", status: 404 }), {
        status: 404,
        headers: { "content-type": "application/problem+json" },
      });
    }
    const { status = 200, body } = typeof route === "function" ? route(call) : route;
    if (status === 204) return new Response(null, { status });
    const contentType = status >= 400 ? "application/problem+json" : "application/json";
    return new Response(JSON.stringify(body), { status, headers: { "content-type": contentType } });
  });
  vi.stubGlobal("fetch", fetchMock);
  return calls;
}
