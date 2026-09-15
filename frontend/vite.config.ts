/// <reference types="vitest/config" />
import type { EventEmitter } from "node:events";
import type { ServerResponse } from "node:http";
import { fileURLToPath } from "node:url";
import { defineConfig, type ProxyOptions } from "vite";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";

// The dev server proxies /api to the local FastAPI process so the session cookie stays same-origin.
// start-dev.bat sets API_PROXY_TARGET when the backend runs on a non-default port.
const apiTarget = process.env.API_PROXY_TARGET ?? "http://127.0.0.1:8000";

/** When the backend is down, answer with a problem+json 503 instead of an empty 500, so the UI can explain it. */
function backendUnavailable(res: ServerResponse | unknown) {
  const response = res as ServerResponse;
  if (!response || typeof response.writeHead !== "function" || response.headersSent) return;
  response.writeHead(503, { "Content-Type": "application/problem+json" });
  response.end(
    JSON.stringify({
      type: "urn:platform:problem:backend-unavailable",
      title: "Service unavailable",
      status: 503,
      code: "BACKEND_UNAVAILABLE",
      detail: "The platform service is not running. Start it with start-dev.bat, then try again.",
    }),
  );
}

const proxyOptions: ProxyOptions = {
  target: apiTarget,
  changeOrigin: false,
  configure: (proxy) => {
    (proxy as unknown as EventEmitter).on("error", (_err: Error, _req: unknown, res: unknown) => backendUnavailable(res));
  },
};

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
  server: {
    port: 5173,
    strictPort: true, // never drift to 5174 silently; start-dev.bat checks this port
    proxy: {
      "/api": proxyOptions,
      "/healthz": proxyOptions,
    },
  },
  test: {
    environment: "jsdom",
    include: ["src/**/*.test.{ts,tsx}"],
    setupFiles: ["./src/test/setup.ts"],
    css: false,
    restoreMocks: true,
  },
});
