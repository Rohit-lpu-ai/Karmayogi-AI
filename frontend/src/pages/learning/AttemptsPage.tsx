import { ArrowRight, ClipboardCheck } from "lucide-react";
import { Link } from "react-router-dom";
import type { AttemptHistoryItem } from "@/api/types";
import { useApi } from "@/api/useApi";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName } from "@/components/product/competency";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

const STATUS: Record<string, { label: string; tone: "success" | "info" | "neutral" }> = {
  scored: { label: "Scored", tone: "success" },
  submitted: { label: "Submitted", tone: "info" },
  in_progress: { label: "In progress", tone: "info" },
};

function when(value: string | null): string {
  return value ? new Date(value).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" }) : "-";
}

/** The learner's own assessment attempts (GET /me/attempts), newest first, with links to results. */
export function AttemptsPage() {
  const attempts = useApi<AttemptHistoryItem[]>("/api/v1/me/attempts");

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "Assessment history" }]}
        title="Assessment history"
        description="Your assessment attempts and their results. Results are development guidance, not an appraisal."
        className="pb-0"
      />
      {attempts.loading ? <Card className="p-6"><LoadingState label="Loading your attempts" lines={4} /></Card> : null}
      {attempts.error ? <ErrorState error={attempts.error} onRetry={attempts.reload} /> : null}
      {attempts.data && attempts.data.length === 0 ? (
        <EmptyState icon={<ClipboardCheck className="size-5" />} title="No assessments yet" action={<Button asChild><Link to="/assessment">Go to the baseline assessment</Link></Button>}>
          Your baseline assessment shows where you stand in the competencies your role requires.
        </EmptyState>
      ) : null}
      {attempts.data && attempts.data.length > 0 ? (
        <ol className="flex flex-col gap-3">
          {attempts.data.map((attempt) => {
            const status = STATUS[attempt.status] ?? { label: attempt.status, tone: "neutral" as const };
            const scored = attempt.status === "scored";
            return (
              <Card as="li" key={attempt.id} className="flex flex-col gap-3 p-5 sm:flex-row sm:items-center">
                <div className="min-w-0 flex-1 space-y-1.5">
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge tone={status.tone}>{status.label}</Badge>
                    {attempt.is_baseline ? <Badge tone="primary">Baseline</Badge> : null}
                  </div>
                  <h2 className="font-semibold leading-snug">{cleanName(attempt.assessment.title)}</h2>
                  <dl className="flex flex-wrap gap-x-5 gap-y-1 text-sm text-muted-foreground">
                    <div><dt className="inline">Started: </dt><dd className="inline">{when(attempt.started_at)}</dd></div>
                    {attempt.submitted_at ? <div><dt className="inline">Submitted: </dt><dd className="inline">{when(attempt.submitted_at)}</dd></div> : null}
                    {attempt.score_total !== null ? <div><dt className="inline">Overall: </dt><dd className="inline tabular-nums">{Math.round(Number(attempt.score_total) * 100)} / 100</dd></div> : null}
                  </dl>
                </div>
                {scored ? (
                  <Button variant="secondary" asChild className="self-start sm:self-center">
                    <Link to={`/attempts/${attempt.id}/result`}>View result<ArrowRight aria-hidden="true" /></Link>
                  </Button>
                ) : attempt.status === "in_progress" ? (
                  <Button asChild className="self-start sm:self-center">
                    <Link to={`/assessment/attempts/${attempt.id}`}>Resume<ArrowRight aria-hidden="true" /></Link>
                  </Button>
                ) : null}
              </Card>
            );
          })}
        </ol>
      ) : null}
    </div>
  );
}
