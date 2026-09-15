import { ArrowRight, BookOpen, ClipboardCheck, Target } from "lucide-react";
import { Link } from "react-router-dom";
import type { GapItem, Gaps, JobRoleCompetencies, Level, Recommendations } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { PageHeader } from "@/components/layout/PageHeader";
import { cleanName, CompetencyStatusBadge, gapSentence, levelName, STATUS_META } from "@/components/product/competency";
import { LevelScale } from "@/components/product/LevelScale";
import { DemoBadge, EmptyState, ErrorState, EvidenceBadge, LoadingState } from "@/components/States";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Disclosure } from "@/components/ui/collapsible";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { cn } from "@/lib/utils";

type Rec = Recommendations["items"][number];

/** Gap analysis (UI_UX_SPEC.md S-05, MVP-08): prioritised gaps with required vs estimated level and what to do next. */
export function GapsPage() {
  const { user } = useAuth();
  const gaps = useApi<Gaps>("/api/v1/me/competency-gaps");
  const recommendations = useApi<Recommendations>("/api/v1/me/recommendations");
  const requirements = useApi<JobRoleCompetencies>(user?.job_role ? `/api/v1/job-roles/${user.job_role.id}/competencies` : null);
  const levelsById = new Map((requirements.data?.requirements ?? []).map((r) => [r.competency.id, r.levels]));

  return (
    <div className="flex flex-col gap-8">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "My competencies", to: "/competencies" }, { label: "Gap analysis" }]}
        title="Gap analysis"
        description="Where your estimated level is below what your job role requires, in priority order, with the learning that helps most."
        meta={user?.job_role ? <><Badge tone="neutral">{cleanName(user.job_role.name)}</Badge>{user.job_role.is_demo ? <DemoBadge /> : null}</> : null}
        className="pb-0"
      />

      {gaps.loading ? (
        <Card className="p-6"><LoadingState label="Loading your gap analysis" lines={6} /></Card>
      ) : gaps.error ? (
        <ErrorState error={gaps.error} onRetry={gaps.reload} />
      ) : gaps.data && gaps.data.items.length === 0 ? (
        <EmptyState title="Your job role's requirements haven't been approved yet." icon={<Target className="size-5" />}>
          <p>Gaps appear once the competencies for your role are approved.</p>
        </EmptyState>
      ) : gaps.data && gaps.data.items.every((i) => i.status === "not_assessed") ? (
        <EmptyState
          title="Take the baseline assessment to see your gaps."
          icon={<ClipboardCheck className="size-5" />}
          action={<Button asChild><Link to="/assessment">Go to the baseline assessment</Link></Button>}
        >
          <p>Your role requires {gaps.data.items.length} competencies. The assessment estimates where you stand in each.</p>
        </EmptyState>
      ) : gaps.data ? (
        <GapsContent gaps={gaps.data} recs={recommendations} levelsById={levelsById} />
      ) : null}
    </div>
  );
}

function GapsContent({ gaps, recs, levelsById }: { gaps: Gaps; recs: { data: Recommendations | null; loading: boolean; error: import("@/api/client").ApiError | null; reload: () => void }; levelsById: Map<string, Level[]> }) {
  const developing = gaps.items.filter((i) => i.status === "gap").sort((a, b) => (b.gap ?? 0) - (a.gap ?? 0));
  const unsure = gaps.items.filter((i) => i.status === "insufficient_evidence" || i.status === "level_unavailable" || i.status === "not_assessed");
  const strengths = gaps.items.filter((i) => i.status === "meets_requirement");
  const total = gaps.items.length;
  const recsFor = (competencyId: string): Rec[] =>
    (recs.data?.items ?? []).filter((r) => r.reasons.some((reason) => reason.rule === "gap_match" && reason.competency_code === gaps.items.find((g) => g.competency.id === competencyId)?.competency.code));

  return (
    <>
      <section aria-labelledby="gap-summary" className="grid gap-5 lg:grid-cols-[minmax(0,22rem)_minmax(0,1fr)]">
        <Card className="flex flex-col justify-between gap-4 p-6">
          <div className="space-y-2">
            <h2 id="gap-summary" className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">Summary</h2>
            <p className="text-2xl font-semibold leading-snug text-balance">
              {developing.length === 0
                ? "No confirmed gaps for your role."
                : `${developing.length} of ${total} competencies need development for your role.`}
            </p>
            <p className="text-muted-foreground">
              {strengths.length} at or above the required level{unsure.length ? `, ${unsure.length} need more evidence` : ""}.
            </p>
          </div>
          <dl className="grid grid-cols-3 gap-2 text-center">
            {(["gap", "meets_requirement", "insufficient_evidence"] as const).map((status) => {
              const count = status === "insufficient_evidence" ? unsure.length : status === "gap" ? developing.length : strengths.length;
              const tone = STATUS_META[status].tone;
              return (
                <div key={status} className={cn("rounded-lg px-2 py-3", tone === "warning" && "bg-warning-soft text-warning", tone === "success" && "bg-success-soft text-success", tone === "info" && "bg-info-soft text-info")}>
                  <dt className="text-xs font-medium">{STATUS_META[status].label}</dt>
                  <dd className="text-2xl font-semibold tabular-nums">{count}</dd>
                </div>
              );
            })}
          </dl>
        </Card>

        <Card className="p-6">
          <Tabs defaultValue="chart">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <h2 className="text-base font-semibold">Required and estimated level</h2>
              <TabsList aria-label="Choose how to view the comparison">
                <TabsTrigger value="chart">Chart</TabsTrigger>
                <TabsTrigger value="table">Table</TabsTrigger>
              </TabsList>
            </div>
            <p className="mt-1 text-sm text-muted-foreground">
              {developing.length} of {total} competencies are below the level required for your role.
            </p>
            <TabsContent value="chart">
              <ul className="space-y-4">
                {gaps.items.map((item) => (
                  <li key={item.competency.id} className="grid gap-2 sm:grid-cols-[minmax(0,14rem)_minmax(0,1fr)] sm:items-center sm:gap-4">
                    <span className="text-sm font-medium text-foreground">{cleanName(item.competency.name)}</span>
                    <LevelScale
                      levels={levelsById.get(item.competency.id)?.length ?? item.max_level_span + 1}
                      estimated={item.estimated_level}
                      required={item.required_level}
                      label={item.competency.name}
                    />
                  </li>
                ))}
              </ul>
            </TabsContent>
            <TabsContent value="table">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <caption className="sr-only">Required and estimated level by competency</caption>
                  <thead className="border-b border-border text-muted-foreground">
                    <tr>
                      <th scope="col" className="py-2 pr-3 font-medium">Competency</th>
                      <th scope="col" className="px-3 py-2 font-medium">Estimated</th>
                      <th scope="col" className="px-3 py-2 font-medium">Required</th>
                      <th scope="col" className="px-3 py-2 font-medium">Gap</th>
                      <th scope="col" className="py-2 pl-3 font-medium">Evidence</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border">
                    {gaps.items.map((item) => (
                      <tr key={item.competency.id}>
                        <th scope="row" className="py-2.5 pr-3 font-medium text-foreground">{cleanName(item.competency.name)}</th>
                        <td className="px-3 py-2.5 tabular-nums">{item.estimated_level ?? "-"}</td>
                        <td className="px-3 py-2.5 tabular-nums">{item.required_level}</td>
                        <td className="px-3 py-2.5 tabular-nums">{item.status === "gap" ? item.gap : item.status === "meets_requirement" ? "None" : "Not confirmed"}</td>
                        <td className="py-2.5 pl-3"><EvidenceBadge band={item.evidence_band} count={item.evidence_count} /></td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </TabsContent>
          </Tabs>
        </Card>
      </section>

      {developing.length > 0 ? (
        <section aria-labelledby="priority-gaps" className="space-y-4">
          <div>
            <h2 id="priority-gaps" className="text-xl font-semibold">Priority gaps</h2>
            <p className="text-muted-foreground">Largest gaps first. Each one links to the learning that addresses it.</p>
          </div>
          <ol className="space-y-4">
            {developing.map((item, index) => (
              <GapCard key={item.competency.id} priority={index + 1} item={item} levels={levelsById.get(item.competency.id)} recs={recsFor(item.competency.id)} recsLoading={recs.loading} />
            ))}
          </ol>
          {recs.error ? <ErrorState error={recs.error} onRetry={recs.reload} /> : null}
        </section>
      ) : null}

      {unsure.length > 0 ? (
        <section aria-labelledby="needs-evidence" className="space-y-3">
          <h2 id="needs-evidence" className="text-xl font-semibold">Needs more evidence</h2>
          <ul className="grid gap-3 md:grid-cols-2">
            {unsure.map((item) => (
              <Card as="li" key={item.competency.id} className="flex flex-col gap-2 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="font-medium">{cleanName(item.competency.name)}</span>
                  <CompetencyStatusBadge status={item.status} />
                </div>
                <p className="text-sm text-muted-foreground">{gapSentence(item)}</p>
              </Card>
            ))}
          </ul>
        </section>
      ) : null}

      {strengths.length > 0 ? (
        <section aria-labelledby="strengths" className="space-y-3">
          <h2 id="strengths" className="text-xl font-semibold">Strengths</h2>
          <ul className="grid gap-3 md:grid-cols-2">
            {strengths.map((item) => (
              <Card as="li" key={item.competency.id} className="flex flex-col gap-2 p-4">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="font-medium">{cleanName(item.competency.name)}</span>
                  <CompetencyStatusBadge status="meets_requirement" />
                </div>
                <p className="text-sm text-muted-foreground">
                  Estimated level {item.estimated_level} ({levelName(levelsById.get(item.competency.id), item.estimated_level)}); your role requires {item.required_level}.
                </p>
              </Card>
            ))}
          </ul>
        </section>
      ) : null}

      <Disclosure title="How are gaps identified?" className="bg-card">
        <div className="space-y-2 text-foreground">
          <p>A gap is the difference between the level your role requires and your estimated level from the baseline assessment.</p>
          <p>A gap is only confirmed when at least 5 questions measured the competency (medium or high evidence). With fewer questions the competency is listed under "Needs more evidence".</p>
          <p>Levels come from provisional score thresholds that have not been statistically validated. This is development guidance, not an appraisal.</p>
        </div>
      </Disclosure>
    </>
  );
}

function GapCard({ priority, item, levels, recs, recsLoading }: { priority: number; item: GapItem; levels: Level[] | undefined; recs: Rec[]; recsLoading: boolean }) {
  const primary = priority === 1; // one primary action per view (UI_UX_SPEC.md §2)
  const current = levels?.find((l) => l.level_number === item.estimated_level);
  const required = levels?.find((l) => l.level_number === item.required_level);
  const top = recs[0];
  return (
    <Card as="li" className="overflow-hidden">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-border px-5 py-4 sm:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-warning-soft text-sm font-semibold text-warning" aria-hidden="true">
            {priority}
          </span>
          <h3 className="min-w-0 text-lg font-semibold">
            <span className="sr-only">Priority {priority}: </span>
            {cleanName(item.competency.name)}
          </h3>
          {item.competency.is_demo ? <DemoBadge label="DEMO" /> : null}
        </div>
        <Badge tone="warning">
          {item.gap} level{item.gap === 1 ? "" : "s"} to go
        </Badge>
      </div>

      <div className="grid gap-6 px-5 py-5 sm:px-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,20rem)]">
        <div className="space-y-4">
          <LevelScale levels={levels?.length ?? item.max_level_span + 1} estimated={item.estimated_level} required={item.required_level} label={item.competency.name} />
          <dl className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-lg bg-muted/60 p-3">
              <dt className="text-xs font-medium uppercase tracking-wide text-muted-foreground">Where you are now</dt>
              <dd className="mt-1">
                <span className="font-semibold">Level {item.estimated_level}{current ? ` - ${levelName(levels, item.estimated_level)}` : ""}</span>
                {current?.description ? <span className="mt-0.5 block text-sm text-muted-foreground">{current.description}</span> : null}
              </dd>
            </div>
            <div className="rounded-lg bg-primary-soft/60 p-3">
              <dt className="text-xs font-medium uppercase tracking-wide text-primary-soft-foreground">What your role requires</dt>
              <dd className="mt-1">
                <span className="font-semibold">Level {item.required_level}{required ? ` - ${levelName(levels, item.required_level)}` : ""}</span>
                {required?.description ? <span className="mt-0.5 block text-sm text-muted-foreground">{required.description}</span> : null}
              </dd>
            </div>
          </dl>
          {item.competency.description ? (
            <div>
              <h4 className="text-sm font-semibold">Why it matters in your role</h4>
              <p className="mt-1 text-sm text-muted-foreground">{item.competency.description}</p>
            </div>
          ) : null}
          <EvidenceBadge band={item.evidence_band} count={item.evidence_count} />
        </div>

        <div className="flex flex-col gap-3 rounded-lg border border-border p-4">
          <h4 className="flex items-center gap-2 text-sm font-semibold">
            <BookOpen className="size-4 text-primary" aria-hidden="true" />
            Recommended learning
          </h4>
          {recsLoading ? (
            <LoadingState label="Loading recommendations" lines={2} />
          ) : recs.length === 0 ? (
            <p className="text-sm text-muted-foreground">No approved learning content matches this gap yet.</p>
          ) : (
            <ul className="space-y-2">
              {recs.slice(0, 3).map((rec) => (
                <li key={rec.course.id}>
                  <Link to={`/courses/${rec.course.id}`} className="block rounded-md px-2 py-1.5 text-sm font-medium text-primary hover:bg-primary-soft focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
                    {cleanName(rec.course.title)}
                  </Link>
                </li>
              ))}
            </ul>
          )}
          {top ? (
            <Button variant={primary ? "primary" : "secondary"} className="mt-auto" asChild>
              <Link to={`/courses/${top.course.id}`}>
                Next: open the top course
                <ArrowRight aria-hidden="true" />
              </Link>
            </Button>
          ) : (
            <Button variant="secondary" className="mt-auto" asChild>
              <Link to="/courses">Browse all courses</Link>
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}
