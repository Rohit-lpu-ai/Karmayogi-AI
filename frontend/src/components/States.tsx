import type { ReactNode } from "react";
import type { ApiError } from "../api/client";

export function DemoBadge({ label = "DEMO - synthetic" }: { label?: string }) {
  return <span className="badge badge-demo">{label}</span>;
}

export function StatusBadge({ tone, children }: { tone: "info" | "warning" | "success" | "neutral"; children: ReactNode }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

export function LoadingState({ label = "Loading" }: { label?: string }) {
  return (
    <p className="state state-loading" role="status" aria-live="polite">
      {label}...
    </p>
  );
}

export function EmptyState({ title, children }: { title: string; children?: ReactNode }) {
  return (
    <div className="state state-empty">
      <p className="state-title">{title}</p>
      {children}
    </div>
  );
}

export function ErrorState({ error, onRetry }: { error: ApiError; onRetry?: () => void }) {
  return (
    <div className="state state-error" role="alert">
      <p className="state-title">{error.detail ?? error.message}</p>
      <p className="state-meta">
        Code: <code>{error.code}</code>
        {error.correlationId ? (
          <>
            {" "}
            · Reference: <code>{error.correlationId}</code>
          </>
        ) : null}
      </p>
      {onRetry ? (
        <button type="button" className="button button-secondary" onClick={onRetry}>
          Try again
        </button>
      ) : null}
    </div>
  );
}
