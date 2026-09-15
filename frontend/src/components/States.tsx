import { FileQuestion, RotateCcw } from "lucide-react";
import type { ReactNode } from "react";
import type { ApiError } from "@/api/client";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { cn } from "@/lib/utils";

/**
 * Shared loading, empty and error states (UI_UX_SPEC.md §8.5-8.7) and status badges.
 * The exported names and props are kept stable for screens that have not been migrated yet (DEC-050).
 */

export function DemoBadge({ label = "DEMO - synthetic" }: { label?: string }) {
  return (
    <Badge tone="demo" title="Synthetic demo content - not official data">
      {label}
    </Badge>
  );
}

type Tone = "info" | "warning" | "success" | "neutral" | "danger" | "primary";

export function StatusBadge({ tone, children }: { tone: Tone; children: ReactNode }) {
  return <Badge tone={tone}>{children}</Badge>;
}

const EVIDENCE: Record<string, { label: string; tone: Tone; description: string }> = {
  insufficient: { label: "Insufficient evidence", tone: "warning", description: "Fewer than 3 questions measured this" },
  low: { label: "Low evidence", tone: "warning", description: "3-4 questions measured this" },
  medium: { label: "Medium evidence", tone: "info", description: "5-9 questions measured this" },
  high: { label: "High evidence", tone: "success", description: "10 or more questions measured this" },
};

/** How much assessment evidence supports an estimate, always as words (UI_UX_SPEC.md §7 EvidenceBand). */
export function EvidenceBadge({ band, count }: { band: string | null; count?: number }) {
  if (!band) return <Badge tone="neutral">Not assessed</Badge>;
  const entry = EVIDENCE[band] ?? { label: band, tone: "neutral" as Tone, description: "" };
  const suffix = count !== undefined ? ` (${count} question${count === 1 ? "" : "s"})` : "";
  return (
    <Badge tone={entry.tone} title={entry.description}>
      {entry.label}
      {suffix}
    </Badge>
  );
}

/** Content-shaped skeleton that appears after 300 ms, with a polite status for screen readers. */
export function LoadingState({ label = "Loading", lines = 3, className }: { label?: string; lines?: number; className?: string }) {
  return (
    <div className={cn("space-y-3 opacity-0 animate-delayed-appear [animation-fill-mode:forwards]", className)}>
      <p className="sr-only" role="status" aria-live="polite">
        {label}...
      </p>
      {Array.from({ length: lines }, (_, index) => (
        <Skeleton key={index} className={cn("h-4", index === 0 ? "w-2/3" : index % 2 ? "w-full" : "w-5/6")} />
      ))}
    </div>
  );
}

/** Explains why something is empty and what to do next. */
export function EmptyState({
  title,
  children,
  icon,
  action,
  className,
}: {
  title: string;
  children?: ReactNode;
  icon?: ReactNode;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("flex flex-col items-start gap-2 rounded-lg border border-dashed border-border bg-muted/50 p-5", className)}>
      <span className="text-muted-foreground" aria-hidden="true">
        {icon ?? <FileQuestion className="size-5" />}
      </span>
      <p className="font-semibold text-foreground">{title}</p>
      {children ? <div className="text-sm text-muted-foreground [&_p]:m-0">{children}</div> : null}
      {action ? <div className="mt-1">{action}</div> : null}
    </div>
  );
}

/** Human message, what to do, and the reference ID for support. Technical codes are not shown to learners. */
export function ErrorState({ error, onRetry, className }: { error: ApiError; onRetry?: () => void; className?: string }) {
  return (
    <div role="alert" className={cn("flex flex-col items-start gap-2 rounded-lg border border-danger/25 bg-danger-soft p-4 text-danger", className)}>
      <p className="font-semibold">{error.detail ?? error.message}</p>
      {error.correlationId ? (
        <p className="text-sm">
          Reference: <code className="select-all">{error.correlationId}</code>
        </p>
      ) : null}
      {onRetry ? (
        <Button variant="secondary" size="sm" onClick={onRetry}>
          <RotateCcw aria-hidden="true" />
          Try again
        </Button>
      ) : null}
    </div>
  );
}
