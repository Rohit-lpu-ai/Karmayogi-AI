import { CheckCircle2, Circle, CircleX } from "lucide-react";
import type { CourseState, QuestionStatus, ReviewHistoryItem } from "@/api/adminTypes";
import { Badge } from "@/components/ui/badge";

type Tone = "neutral" | "info" | "success" | "warning" | "danger" | "primary";

export const QUESTION_STATUS: Record<string, { label: string; tone: Tone }> = {
  draft: { label: "Draft", tone: "neutral" },
  in_review: { label: "In review", tone: "info" },
  approved: { label: "Approved", tone: "success" },
  rejected: { label: "Rejected", tone: "danger" },
  retired: { label: "Retired", tone: "neutral" },
  pending_validation: { label: "Pending validation", tone: "warning" },
  failed_validation: { label: "Failed validation", tone: "danger" },
  validation_incomplete: { label: "Validation incomplete", tone: "warning" },
  suspended: { label: "Suspended", tone: "warning" },
};

export const COURSE_STATE: Record<CourseState, { label: string; tone: Tone; description: string }> = {
  draft: { label: "Draft", tone: "neutral", description: "Being prepared. Not visible to learners." },
  in_review: { label: "In review", tone: "info", description: "Waiting for a reviewer. Not visible to learners." },
  approved: { label: "Approved, not live", tone: "warning", description: "Approved by a reviewer. Publish to make it visible." },
  published: { label: "Published", tone: "success", description: "Visible to learners in the catalogue." },
};

export const ORIGIN: Record<string, { label: string; tone: Tone }> = {
  synthetic: { label: "Synthetic example", tone: "neutral" },
  official_source: { label: "Official source, awaiting review", tone: "warning" },
  provider: { label: "Provider content", tone: "info" },
  human_authored: { label: "Authored here", tone: "neutral" },
  demo_seed: { label: "Synthetic seed", tone: "neutral" },
  ai_generated: { label: "AI generated", tone: "warning" },
};

export function QuestionStatusBadge({ status }: { status: QuestionStatus | string }) {
  const meta = QUESTION_STATUS[status] ?? { label: status, tone: "neutral" as Tone };
  return <Badge tone={meta.tone}>{meta.label}</Badge>;
}

export function CourseStateBadge({ state }: { state: CourseState }) {
  const meta = COURSE_STATE[state];
  return <Badge tone={meta.tone}>{meta.label}</Badge>;
}

export function OriginBadge({ origin }: { origin: string }) {
  const meta = ORIGIN[origin] ?? { label: origin, tone: "neutral" as Tone };
  return <Badge tone={meta.tone}>{meta.label}</Badge>;
}

export function GuardChecklist({ checks, title }: { checks: { id: string; label: string; passed: boolean; detail?: string | null }[]; title?: string }) {
  return (
    <div>
      {title ? <p className="text-sm font-semibold">{title}</p> : null}
      <ul className="mt-2 space-y-1.5">
        {checks.map((check) => (
          <li key={check.id} className="flex items-start gap-2 text-sm">
            {check.passed ? <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-success" aria-hidden="true" /> : <CircleX className="mt-0.5 size-4 shrink-0 text-danger" aria-hidden="true" />}
            <span>
              <span className="sr-only">{check.passed ? "Met: " : "Not met: "}</span>
              {check.label}
              {check.detail ? <span className="text-muted-foreground"> ({check.detail})</span> : null}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

const DECISION: Record<string, { label: string; tone: Tone }> = {
  approve: { label: "Approved", tone: "success" },
  reject: { label: "Rejected", tone: "danger" },
  request_changes: { label: "Changes requested", tone: "warning" },
};

export function formatDateTime(value: string | null | undefined): string {
  return value ? new Date(value).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" }) : "-";
}

export function ReviewHistory({ items }: { items: ReviewHistoryItem[] }) {
  if (items.length === 0) return <p className="text-sm text-muted-foreground">Not submitted for review yet.</p>;
  return (
    <ol className="space-y-3">
      {items.map((item) => (
        <li key={item.task_id} className="flex gap-3 text-sm">
          <Circle className="mt-1 size-2.5 shrink-0 fill-current text-muted-foreground" aria-hidden="true" />
          <div className="min-w-0 space-y-1">
            <p>
              Submitted by <span className="font-medium">{item.submitted_by ?? "unknown"}</span>, {formatDateTime(item.submitted_at)}
              {item.note ? <span className="text-muted-foreground"> - "{item.note}"</span> : null}
            </p>
            {item.decision ? (
              <p className="flex flex-wrap items-center gap-2">
                <Badge tone={DECISION[item.decision].tone}>{DECISION[item.decision].label}</Badge>
                <span>by {item.decided_by ?? "a reviewer"}, {formatDateTime(item.decided_at)}</span>
              </p>
            ) : item.status === "cancelled" ? (
              <p className="text-muted-foreground">Withdrawn before a decision.</p>
            ) : (
              <p className="text-muted-foreground">Waiting for a reviewer.</p>
            )}
            {item.reason ? <p className="rounded-md bg-muted px-3 py-2">{item.reason}</p> : null}
          </div>
        </li>
      ))}
    </ol>
  );
}
