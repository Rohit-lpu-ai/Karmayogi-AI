import { ArrowRight, CalendarClock, ClipboardCheck, Target } from "lucide-react";
import { Link } from "react-router-dom";
import type { AttemptHistoryItem, GapItem, Gaps, JobRoleCompetencies, Level, Profile, ProfileItem } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName, CompetencyStatusBadge, gapSentence, levelName } from "@/components/product/competency";
import { LevelScale } from "@/components/product/LevelScale";
import { DemoBadge, EmptyState, ErrorState, EvidenceBadge, LoadingState } from "@/components/States";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Disclosure } from "@/components/ui/collapsible";
import { cn } from "@/lib/utils";

/** Competency profile (UI_UX_SPEC.md S-04, MVP-07): every role competency with estimate, evidence, meaning and action. */
export function CompetencyProfilePage() {
  const { user } = useAuth();
  const gaps = useApi<Gaps>("/api/v1/me/competency-gaps");
  const profile = useApi<Profile>("/api/v1/me/competency-profile");
  const requirements = useApi<JobRoleCompetencies>(user?.job_role ? `/api/v1/job-roles/${user.job_role.id}/competencies` : null);
  const attempts = useApi<AttemptHistoryItem[]>("/api/v1/me/attempts");

  const levelsById = new Map((requirements.data?.requirements ?? []).map((r) => [r.competency.id, r.levels]));
  const profileById = new Map((profile.data?.items ?? []).map((p) => [p.competency.id, p]));
  const items = gaps.data?.items ?? [];
  const atLevel = items.filter((i) => i.status === "meets_requirement").length;
  const assessed = items.filter((i) => i.status !== "not_assessed").length;

  return (
    <div className="flex flex-col gap-8">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "My competencies" }]}
        title="My competencies"
        description="What your job role requires, where your evidence places you today, and what to do next for each competency."
        meta={user?.job_role ? <><Badge tone="neutral">{cleanName(user.job_role.name)}</Badge>{user.job_role.is_demo ? <DemoBadge /> : null}</> : null}
        actions={
          items.some((i) => i.status === "gap") ? (
            <Button asChild>
              <Link to="/competencies/gaps">
                <Target aria-hidden="true" />
                View gap analysis
              </Link>
            </Button>
          ) : null
        }
        className="pb-0"
      />

      {gaps.loading ? (
        <Card className="p-6"><LoadingState label="Loading your competency profile" lines={6} /></Card>
      ) : gaps.error ? (
        <ErrorState error={gaps.error} onRetry={gaps.reload} />
      ) : items.length === 0 ? (
        <EmptyState title="Your job role's requirements haven't been approved yet." />
      ) : (
        <>
          <Card as="section" aria-labelledby="profile-overview" className="grid gap-6 p-6 md:grid-cols-[minmax(0,1fr)_auto] md:items-center">
            <div className="space-y-2">
              <h2 id="profile-overview" className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">Overview</h2>
              <p className="text-2xl font-semibold leading-snug text-balance">
                {assessed === 0
                  ? `Your role requires ${items.length} competencies. None has been assessed yet.`
                  : `${atLevel} of ${items.length} competencies are at the level your role requires.`}
              </p>
              <p className="text-muted-foreground">
                Estimates come from assessment evidence using fixed rules. They are development guidance, not an appraisal.
              </p>
            </div>
            {assessed === 0 ? (
              <Button size="lg" asChild>
                <Link to="/assessment">
                  <ClipboardCheck aria-hidden="true" />
                  Take the baseline assessment
                </Link>
              </Button>
            ) : (
              <div className="flex flex-col items-start gap-2 md:items-end">
              <ol className="flex flex-wrap gap-1.5" aria-label="Competencies at the required level">
                {items.map((i) => (
                  <li key={i.competency.id} title={`${i.competency.name}: ${gapSentence(i)}`}>
                    <span className={cn("block h-10 w-3 rounded-sm", i.status === "meets_requirement" ? "bg-success" : i.status === "gap" ? "bg-warning/80" : "bg-muted")} aria-hidden="true" />
                    <span className="sr-only">{i.competency.name}: {gapSentence(i)}</span>
                  </li>
                ))}
              </ol>
              <p className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-muted-foreground" aria-hidden="true">
                <span className="flex items-center gap-1"><span className="size-2.5 rounded-sm bg-success" />Meets</span>
                <span className="flex items-center gap-1"><span className="size-2.5 rounded-sm bg-warning/80" />Developing</span>
                <span className="flex items-center gap-1"><span className="size-2.5 rounded-sm bg-muted" />Needs evidence</span>
              </p>
              </div>
            )}
          </Card>

          <section aria-labelledby="competency-list" className="space-y-4">
            <h2 id="competency-list" className="text-xl font-semibold">Competencies for your role</h2>
            <ul className="grid gap-4 xl:grid-cols-2">
              {items.map((item) => (
                <CompetencyCard key={item.competency.id} item={item} levels={levelsById.get(item.competency.id)} estimate={profileById.get(item.competency.id)} />
              ))}
            </ul>
          </section>

          <section aria-labelledby="history" className="space-y-3">
            <h2 id="history" className="text-xl font-semibold">Assessment history</h2>
            {attempts.loading ? (
              <LoadingState label="Loading history" lines={2} />
            ) : attempts.error ? (
              <ErrorState error={attempts.error} onRetry={attempts.reload} />
            ) : !attempts.data || attempts.data.length === 0 ? (
              <EmptyState title="No assessments yet." icon={<CalendarClock className="size-5" />} />
            ) : (
              <Card>
                <ol className="divide-y divide-border">
                  {attempts.data.map((a) => (
                    <li key={a.id} className="flex flex-wrap items-center justify-between gap-3 px-5 py-4">
                      <div className="min-w-0">
                        <p className="font-medium">{cleanName(a.assessment.title)} {a.assessment.is_demo ? <DemoBadge label="DEMO" /> : null}</p>
                        <p className="text-sm text-muted-foreground">
                          {a.scored_at ? `Completed ${new Date(a.scored_at).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" })}` : `Started ${new Date(a.started_at).toLocaleDateString(undefined, { day: "numeric", month: "short", year: "numeric" })}`}
                          {a.score_total !== null ? ` · score ${Math.round(Number(a.score_total) * 100)} / 100` : ""}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        {a.is_baseline ? <Badge tone="info">Baseline</Badge> : null}
                        {a.status === "scored" ? (
                          <Button variant="secondary" size="sm" asChild>
                            <Link to={`/attempts/${a.id}/result`}>View result</Link>
                          </Button>
                        ) : a.status === "in_progress" ? (
                          <Button variant="secondary" size="sm" asChild>
                            <Link to={`/assessment/attempts/${a.id}`}>Resume</Link>
                          </Button>
                        ) : null}
                      </div>
                    </li>
                  ))}
                </ol>
              </Card>
            )}
          </section>

          <Disclosure title="How are estimates calculated?" className="bg-card">
            <div className="space-y-2 text-foreground">
              <p>Each answer is marked correct or not correct by fixed rules; no AI is involved. Harder questions carry more weight (foundational 1, intermediate 1.5, advanced 2).</p>
              <p>Your score for a competency is the weighted share of marks on the questions that measured it. Levels come from provisional thresholds.</p>
              <p>Evidence strength reflects how many questions measured the competency: fewer than 3 insufficient, 3-4 low, 5-9 medium, 10 or more high.</p>
              <p className="text-muted-foreground">If you think a result is wrong, you will be able to request a review in a later release.</p>
            </div>
          </Disclosure>
        </>
      )}
    </div>
  );
}

function CompetencyCard({ item, levels, estimate }: { item: GapItem; levels: Level[] | undefined; estimate: ProfileItem | undefined }) {
  const evidence = (estimate?.explanation.items ?? []) as { correct?: boolean }[];
  const correct = evidence.filter((e) => e.correct).length;
  const action =
    item.status === "gap"
      ? { to: "/competencies/gaps", label: "See learning for this gap" }
      : item.status === "not_assessed" || item.status === "insufficient_evidence"
        ? { to: "/assessment", label: "Go to the assessment" }
        : { to: "/courses", label: "Explore related courses" };

  return (
    <Card as="li" className="flex flex-col gap-4 p-5">
      <div className="flex flex-wrap items-start justify-between gap-2">
        <h3 className="min-w-0 text-base font-semibold">{cleanName(item.competency.name)} {item.competency.is_demo ? <DemoBadge label="DEMO" /> : null}</h3>
        <CompetencyStatusBadge status={item.status} />
      </div>
      {item.competency.description ? <p className="text-sm text-muted-foreground">{item.competency.description}</p> : null}

      <div className="grid gap-4 sm:grid-cols-[auto_minmax(0,1fr)] sm:items-center">
        <dl className="flex gap-4">
          <div>
            <dt className="text-xs text-muted-foreground">Estimated</dt>
            <dd className="text-2xl font-semibold tabular-nums">{item.estimated_level ?? "-"}</dd>
          </div>
          <div>
            <dt className="text-xs text-muted-foreground">Required</dt>
            <dd className="text-2xl font-semibold tabular-nums text-muted-foreground">{item.required_level}</dd>
          </div>
        </dl>
        <LevelScale levels={levels?.length ?? item.max_level_span + 1} estimated={item.estimated_level} required={item.required_level} label={item.competency.name} />
      </div>

      <p className="text-sm font-medium text-foreground">{gapSentence(item)}</p>

      <div className="flex flex-wrap items-center gap-2">
        <EvidenceBadge band={item.evidence_band} count={item.evidence_count} />
        {evidence.length > 0 ? (
          <span className="text-sm text-muted-foreground">
            {correct} of {evidence.length} questions answered correctly
          </span>
        ) : null}
      </div>

      {levels && levels.some((l) => l.description) ? (
        <details className="group rounded-lg border border-border">
          <summary className="flex min-h-10 cursor-pointer list-none items-center justify-between rounded-lg px-3 text-sm font-medium hover:bg-muted/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring [&::-webkit-details-marker]:hidden">
            What the levels mean
            <span className="text-xs text-muted-foreground group-open:hidden">Show</span>
            <span className="hidden text-xs text-muted-foreground group-open:inline">Hide</span>
          </summary>
          <ol className="space-y-2 border-t border-border px-3 py-3">
            {levels.map((level) => (
              <li key={level.level_number} className={cn("rounded-md px-2 py-1.5 text-sm", level.level_number === item.estimated_level && "bg-primary-soft", level.level_number === item.required_level && "ring-1 ring-primary/40")}>
                <span className="font-medium">{levelName(levels, level.level_number) === `Level ${level.level_number}` ? `Level ${level.level_number}` : `Level ${level.level_number} - ${levelName(levels, level.level_number)}`}</span>
                {level.level_number === item.estimated_level ? <Badge tone="primary" className="ml-2">You</Badge> : null}
                {level.level_number === item.required_level ? <Badge tone="neutral" className="ml-2">Required</Badge> : null}
                {level.description ? <span className="mt-0.5 block text-muted-foreground">{level.description}</span> : null}
              </li>
            ))}
          </ol>
        </details>
      ) : null}

      <Link to={action.to} className="mt-auto inline-flex items-center gap-1.5 self-start rounded-md text-sm font-medium text-primary underline-offset-4 hover:underline focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
        {action.label}
        <ArrowRight className="size-4" aria-hidden="true" />
      </Link>
    </Card>
  );
}
