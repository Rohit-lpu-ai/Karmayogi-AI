import { ArrowRight, BookOpenCheck, Building2, ClipboardCheck, ShieldCheck, Target, UserPlus, Users } from "lucide-react";
import { Link } from "react-router-dom";
import type { AdminDepartment, AdminUserPage } from "@/api/types";
import { useApi } from "@/api/useApi";
import { can, useAuth } from "@/auth/AuthContext";
import { ErrorState, LoadingState } from "@/components/States";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CAPABILITY_GROUPS, roleLabel } from "@/config/roles";
import { countText, type InsightSummary } from "./InsightPages";

/** Administration home: account counts from the live API and the capabilities this account holds. */
export function AdminOverviewPage() {
  const { user } = useAuth();
  if (!user) return null;
  const canViewUsers = can(user, "users.view");
  const adminRoles = user.access_roles.filter((role) => role !== "learner");

  return (
    <div className="space-y-8">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-1">
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Overview</h1>
          <p className="text-muted-foreground">
            Signed in as {adminRoles.map(roleLabel).join(", ")}. Every action here is checked by the server and recorded in the audit trail.
          </p>
        </div>
        {can(user, "users.manage") ? (
          <Button asChild>
            <Link to="/admin/users?new=1">
              <UserPlus aria-hidden="true" />
              Add a user
            </Link>
          </Button>
        ) : null}
      </header>

      {can(user, "insight.view") ? <LearningSummary /> : null}
      {canViewUsers ? <PeopleSummary /> : null}

      <section aria-labelledby="capabilities-title" className="space-y-3">
        <div className="flex items-center justify-between gap-3">
          <h2 id="capabilities-title" className="text-lg font-semibold">What your access allows</h2>
          {canViewUsers ? (
            <Link to="/admin/roles" className="text-sm font-medium text-primary underline-offset-4 hover:underline">
              All roles and permissions
            </Link>
          ) : null}
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {CAPABILITY_GROUPS.map((group) => {
            const held = group.items.filter((item) => can(user, item.id));
            return (
              <Card key={group.label} className="p-5">
                <h3 className="font-semibold">{group.label}</h3>
                {held.length ? (
                  <ul className="mt-2 flex flex-wrap gap-1.5">
                    {held.map((item) => (
                      <li key={item.id}>
                        <Badge tone="primary">{item.label}</Badge>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="mt-2 text-sm text-muted-foreground">No permissions in this area.</p>
                )}
              </Card>
            );
          })}
        </div>

      </section>
    </div>
  );
}

function PeopleSummary() {
  const all = useApi<AdminUserPage>("/api/v1/admin/users?page_size=1");
  const active = useApi<AdminUserPage>("/api/v1/admin/users?status=active&page_size=1");
  const invited = useApi<AdminUserPage>("/api/v1/admin/users?status=invited&page_size=1");
  const inactive = useApi<AdminUserPage>("/api/v1/admin/users?status=inactive&page_size=1");
  const departments = useApi<AdminDepartment[]>("/api/v1/admin/departments");

  if (all.loading || departments.loading) return <LoadingState label="Loading account summary" />;
  if (all.error) return <ErrorState error={all.error} onRetry={all.reload} />;

  const tiles = [
    { label: "User accounts", value: all.data?.total, icon: Users, to: "/admin/users" },
    { label: "Active", value: active.data?.total, icon: ShieldCheck, to: "/admin/users?status=active" },
    { label: "Invited, not set up", value: invited.data?.total, icon: UserPlus, to: "/admin/users?status=invited" },
    { label: "Inactive", value: inactive.data?.total, icon: Users, to: "/admin/users?status=inactive" },
  ];

  return (
    <section aria-labelledby="people-title" className="space-y-3">
      <h2 id="people-title" className="text-lg font-semibold">People</h2>
      <ul className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {tiles.map((tile) => (
          <li key={tile.label}>
            <Link
              to={tile.to}
              data-focus-ring=""
              className="group flex h-full flex-col gap-2 rounded-lg border border-border bg-card p-4 transition-colors hover:border-primary/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <span className="flex items-center gap-2 text-sm text-muted-foreground">
                <tile.icon className="size-4" aria-hidden="true" />
                {tile.label}
              </span>
              <span className="text-2xl font-semibold tabular-nums">{tile.value ?? "-"}</span>
            </Link>
          </li>
        ))}
      </ul>
      {departments.data ? (
        <Card className="p-5">
          <h3 className="flex items-center gap-2 font-semibold">
            <Building2 className="size-4 text-muted-foreground" aria-hidden="true" />
            Departments
          </h3>
          {departments.data.length ? (
            <ul className="mt-3 divide-y divide-border">
              {departments.data.map((d) => (
                <li key={d.id} className="flex flex-wrap items-center justify-between gap-2 py-2 text-sm">
                  <span className="font-medium">
                    {d.name}
                    {d.status !== "active" ? <Badge className="ml-2">Inactive</Badge> : null}
                  </span>
                  <Link
                    to={`/admin/users?department_id=${d.id}`}
                    className="inline-flex items-center gap-1 text-muted-foreground underline-offset-4 hover:text-foreground hover:underline"
                  >
                    {d.user_count} {d.user_count === 1 ? "account" : "accounts"}
                    <ArrowRight className="size-3.5" aria-hidden="true" />
                  </Link>
                </li>
              ))}
            </ul>
          ) : (
            <p className="mt-2 text-sm text-muted-foreground">No departments yet.</p>
          )}
        </Card>
      ) : null}
    </section>
  );
}

function LearningSummary() {
  const summary = useApi<InsightSummary>("/api/v1/admin/insight/summary");
  if (summary.loading) return <LoadingState label="Loading learning summary" />;
  if (summary.error) return <ErrorState error={summary.error} onRetry={summary.reload} />;
  const s = summary.data!;
  const tiles = [
    { label: "Learners", value: countText(s.learners, s.min_group_size), icon: Users, to: "/admin/skill-gaps" },
    { label: "Baseline completed", value: countText(s.baseline_completed, s.min_group_size), icon: ClipboardCheck, to: "/admin/skill-gaps" },
    { label: "With a confirmed gap", value: countText(s.learners_with_confirmed_gaps, s.min_group_size), icon: Target, to: "/admin/training-needs" },
    { label: "Completed a course", value: countText(s.learners_completed_a_course, s.min_group_size), icon: BookOpenCheck, to: "/admin/training-needs" },
  ];
  return (
    <section aria-labelledby="learning-title" className="space-y-3">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <h2 id="learning-title" className="text-lg font-semibold">Learning {s.scope === "department" ? "in your department" : "across the organisation"}</h2>
        <p className="text-sm text-muted-foreground">Aggregates only; groups under {s.min_group_size} are withheld.</p>
      </div>
      <ul className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {tiles.map((tile) => (
          <li key={tile.label}>
            <Link to={tile.to} data-focus-ring=""
              className="flex h-full flex-col gap-2 rounded-lg border border-border bg-card p-4 transition-colors hover:border-primary/40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
              <span className="flex items-center gap-2 text-sm text-muted-foreground"><tile.icon className="size-4" aria-hidden="true" />{tile.label}</span>
              <span className="text-2xl font-semibold tabular-nums">{tile.value}</span>
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
