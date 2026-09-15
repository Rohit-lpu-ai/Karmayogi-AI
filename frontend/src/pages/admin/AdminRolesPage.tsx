import { Check, Minus } from "lucide-react";
import { Link } from "react-router-dom";
import type { AdminRole } from "@/api/types";
import { useApi } from "@/api/useApi";
import { ErrorState, LoadingState } from "@/components/States";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { CAPABILITY_GROUPS } from "@/config/roles";

/** Read-only permission matrix served from the backend policy, so the page cannot drift from what the API enforces. */
export function AdminRolesPage() {
  const roles = useApi<AdminRole[]>("/api/v1/admin/roles");

  return (
    <div className="space-y-8">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Roles and permissions</h1>
        <p className="max-w-3xl text-muted-foreground">
          Access roles decide what a person can do in the platform. They are separate from job roles, which decide what competencies a
          learner is assessed against. Assign roles from a user's record.
        </p>
      </header>

      {roles.loading ? <LoadingState label="Loading roles" lines={6} /> : null}
      {roles.error ? <ErrorState error={roles.error} onRetry={roles.reload} /> : null}

      {roles.data ? (
        <>
          <ul className="grid gap-3 md:grid-cols-2">
            {roles.data.map((role) => (
              <Card as="li" key={role.role} className="flex flex-col gap-2 p-5">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <h2 className="font-semibold">{role.label}</h2>
                  <Link
                    to={`/admin/users?role=${role.role}`}
                    className="text-sm text-muted-foreground underline-offset-4 hover:text-foreground hover:underline"
                  >
                    {role.user_count} {role.user_count === 1 ? "account" : "accounts"}
                  </Link>
                </div>
                <p className="text-sm text-muted-foreground">{role.description}</p>
                {role.department_scoped ? <Badge tone="info" className="self-start">Limited to a department</Badge> : null}
              </Card>
            ))}
          </ul>

          <section aria-labelledby="matrix-title" className="space-y-3">
            <h2 id="matrix-title" className="text-lg font-semibold">Permission matrix</h2>
            <div tabIndex={0} role="region" aria-label="Permission matrix, scrolls sideways" data-focus-ring="" className="relative overflow-x-auto rounded-lg border border-border bg-card focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring">
              <table className="w-full min-w-[56rem] border-collapse text-sm">
                <caption className="sr-only">Which access role holds which permission</caption>
                <thead>
                  <tr className="border-b border-border bg-muted/60 text-left">
                    <th scope="col" className="sticky left-0 bg-muted px-3 py-2 font-semibold">Permission</th>
                    {roles.data.map((role) => (
                      <th key={role.role} scope="col" className="px-2 py-2 text-center text-xs font-semibold leading-tight">
                        {role.label}
                      </th>
                    ))}
                  </tr>
                </thead>
                {CAPABILITY_GROUPS.map((group) => (
                  <tbody key={group.label}>
                    <tr className="border-b border-border">
                      <th scope="colgroup" colSpan={roles.data!.length + 1} className="bg-background px-3 py-1.5 text-left text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                        {group.label}
                      </th>
                    </tr>
                    {group.items.map((item) => (
                      <tr key={item.id} className="border-b border-border last:border-0">
                        <th scope="row" className="sticky left-0 bg-card px-3 py-2 text-left font-medium">{item.label}</th>
                        {roles.data!.map((role) => {
                          const held = role.capabilities.includes(item.id);
                          return (
                            <td key={role.role} className="px-2 py-2 text-center">
                              {held ? (
                                <><Check className="mx-auto size-4 text-success" aria-hidden="true" /><span className="sr-only">Allowed</span></>
                              ) : (
                                <><Minus className="mx-auto size-4 text-muted-foreground/50" aria-hidden="true" /><span className="sr-only">Not allowed</span></>
                              )}
                            </td>
                          );
                        })}
                      </tr>
                    ))}
                  </tbody>
                ))}
              </table>
            </div>
            <p className="text-sm text-muted-foreground">
              Learners always see only their own results. Auditors are read-only. Platform administrators cannot see learner competency data.
            </p>
          </section>
        </>
      ) : null}
    </div>
  );
}
