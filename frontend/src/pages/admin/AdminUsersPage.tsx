import { Check, ChevronLeft, ChevronRight, Copy, KeyRound, Loader2, Search, UserPlus } from "lucide-react";
import { useEffect, useMemo, useRef, useState, type FormEvent } from "react";
import { useSearchParams } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { AdminDepartment, AdminUser, AdminUserPage, Me, PasswordLink } from "@/api/types";
import { useApi } from "@/api/useApi";
import { can, useAuth } from "@/auth/AuthContext";
import { EMAIL_RE, ErrorSummary, REGISTRATION_ID_RE, describedBy, serverFieldErrors, type FieldErrors } from "@/components/product/forms";
import { EmptyState, ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Field, Input } from "@/components/ui/form";
import { Checkbox, Select } from "@/components/ui/select";
import { toast } from "@/components/ui/toaster";
import { ROLE_ORDER, USER_STATUS, roleLabel } from "@/config/roles";

const PAGE_SIZE = 20;

function formatDate(value: string | null): string {
  return value ? new Date(value).toLocaleDateString("en-IN", { dateStyle: "medium" }) : "Never";
}

function StatusBadge({ status }: { status: string }) {
  const meta = USER_STATUS[status] ?? { label: status, tone: "neutral" as const };
  return <Badge tone={meta.tone}>{meta.label}</Badge>;
}

/** User administration (Phase 4A). Filters live in the URL so views can be linked from the overview and roles pages. */
export function AdminUsersPage() {
  const { user } = useAuth();
  const [params, setParams] = useSearchParams();
  const q = params.get("q") ?? "";
  const status = params.get("status") ?? "";
  const role = params.get("role") ?? "";
  const departmentId = params.get("department_id") ?? "";
  const page = Math.max(1, Number(params.get("page") ?? "1") || 1);
  const [search, setSearch] = useState(q);
  const [creating, setCreating] = useState(params.get("new") === "1");
  const [editing, setEditing] = useState<AdminUser | null>(null);
  const [issuedLink, setIssuedLink] = useState<{ user: AdminUser; link: PasswordLink } | null>(null);

  const query = useMemo(() => {
    const search = new URLSearchParams({ page: String(page), page_size: String(PAGE_SIZE) });
    if (q) search.set("q", q);
    if (status) search.set("status", status);
    if (role) search.set("role", role);
    if (departmentId) search.set("department_id", departmentId);
    return search.toString();
  }, [q, status, role, departmentId, page]);
  const users = useApi<AdminUserPage>(`/api/v1/admin/users?${query}`);
  const departments = useApi<AdminDepartment[]>("/api/v1/admin/departments");

  if (!user) return null;
  const canManage = can(user, "users.manage");

  function update(changes: Record<string, string>) {
    const next = new URLSearchParams(params);
    for (const [key, value] of Object.entries(changes)) {
      if (value) next.set(key, value);
      else next.delete(key);
    }
    if (!("page" in changes)) next.delete("page");
    next.delete("new");
    setParams(next, { replace: true });
  }

  const total = users.data?.total ?? 0;
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  const filtered = Boolean(q || status || role || departmentId);

  return (
    <div className="space-y-6">
      <header className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-1">
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Users</h1>
          <p className="text-muted-foreground">Accounts are never deleted. Deactivate an account to remove access; its history is kept.</p>
        </div>
        {canManage ? (
          <Button onClick={() => setCreating(true)}>
            <UserPlus aria-hidden="true" />
            Add a user
          </Button>
        ) : null}
      </header>

      <Card as="section" aria-label="Filter users" className="p-4">
        <form
          role="search"
          className="grid gap-3 md:grid-cols-[minmax(0,2fr)_repeat(3,minmax(0,1fr))]"
          onSubmit={(event) => {
            event.preventDefault();
            update({ q: search.trim() });
          }}
        >
          <div className="flex flex-col gap-1.5">
            <label htmlFor="user-search" className="text-sm font-medium">Search</label>
            <div className="flex gap-2">
              <Input id="user-search" type="search" placeholder="Name, email or registration ID" value={search} onChange={(e) => setSearch(e.target.value)} />
              <Button type="submit" variant="secondary" size="icon" aria-label="Search">
                <Search aria-hidden="true" />
              </Button>
            </div>
          </div>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="filter-status" className="text-sm font-medium">Status</label>
            <Select id="filter-status" value={status} onChange={(e) => update({ status: e.target.value })}>
              <option value="">Any status</option>
              {Object.entries(USER_STATUS).map(([id, meta]) => (
                <option key={id} value={id}>{meta.label}</option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="filter-role" className="text-sm font-medium">Access role</label>
            <Select id="filter-role" value={role} onChange={(e) => update({ role: e.target.value })}>
              <option value="">Any role</option>
              {ROLE_ORDER.map((id) => (
                <option key={id} value={id}>{roleLabel(id)}</option>
              ))}
            </Select>
          </div>
          <div className="flex flex-col gap-1.5">
            <label htmlFor="filter-department" className="text-sm font-medium">Department</label>
            <Select id="filter-department" value={departmentId} onChange={(e) => update({ department_id: e.target.value })}>
              <option value="">Any department</option>
              {(departments.data ?? []).map((d) => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </Select>
          </div>
        </form>
      </Card>

      {issuedLink ? <PasswordLinkNotice user={issuedLink.user} link={issuedLink.link} onDismiss={() => setIssuedLink(null)} /> : null}

      <section aria-labelledby="results-title" className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 id="results-title" className="text-lg font-semibold">
            {users.data ? `${total} ${total === 1 ? "account" : "accounts"}` : "Accounts"}
          </h2>
          {filtered ? (
            <Button
              variant="link"
              onClick={() => {
                setSearch("");
                setParams(new URLSearchParams(), { replace: true });
              }}
            >
              Clear filters
            </Button>
          ) : null}
        </div>

        {users.loading && !users.data ? <LoadingState label="Loading users" lines={6} /> : null}
        {users.error ? <ErrorState error={users.error} onRetry={users.reload} /> : null}
        {users.data && users.data.items.length === 0 ? (
          <EmptyState title={filtered ? "No accounts match these filters" : "No accounts yet"}>
            {filtered ? "Change or clear the filters." : canManage ? "Add the first user." : null}
          </EmptyState>
        ) : null}

        {users.data && users.data.items.length > 0 ? (
          <>
            <div tabIndex={0} role="region" aria-label="User accounts table" data-focus-ring="" className="relative hidden overflow-x-auto rounded-lg border border-border bg-card focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring md:block">
              <table className="w-full border-collapse text-sm">
                <caption className="sr-only">User accounts, page {page} of {pages}</caption>
                <thead>
                  <tr className="border-b border-border bg-muted/60 text-left">
                    <th scope="col" className="px-4 py-2 font-semibold">Name</th>
                    <th scope="col" className="px-4 py-2 font-semibold">Access</th>
                    <th scope="col" className="px-4 py-2 font-semibold">Department</th>
                    <th scope="col" className="px-4 py-2 font-semibold">Status</th>
                    <th scope="col" className="px-4 py-2 font-semibold">Last sign-in</th>
                    <th scope="col" className="px-4 py-2"><span className="sr-only">Actions</span></th>
                  </tr>
                </thead>
                <tbody>
                  {users.data.items.map((item) => (
                    <tr key={item.id} className="border-b border-border last:border-0">
                      <td className="px-4 py-3">
                        <p className="font-medium">{item.display_name}</p>
                        <p className="text-muted-foreground">{item.email}</p>
                        {item.registration_id ? <p className="text-xs text-muted-foreground">ID {item.registration_id}</p> : null}
                      </td>
                      <td className="px-4 py-3">
                        <div className="flex max-w-64 flex-wrap gap-1">
                          {item.roles.map((r) => (
                            <Badge key={`${r.role}-${r.department_scope_id ?? ""}`} tone={r.role === "learner" ? "neutral" : "primary"}>
                              {roleLabel(r.role)}
                            </Badge>
                          ))}
                        </div>
                      </td>
                      <td className="px-4 py-3">{item.department?.name ?? <span className="text-muted-foreground">Not set</span>}</td>
                      <td className="px-4 py-3"><StatusBadge status={item.status} /></td>
                      <td className="px-4 py-3 tabular-nums text-muted-foreground">{formatDate(item.last_login_at)}</td>
                      <td className="px-4 py-3 text-right">
                        <Button variant="secondary" size="sm" onClick={() => setEditing(item)} aria-label={`${canManage ? "Manage" : "View"} ${item.display_name}`}>
                          {canManage ? "Manage" : "View"}
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <ul className="grid gap-3 md:hidden">
              {users.data.items.map((item) => (
                <Card as="li" key={item.id} className="flex flex-col gap-2 p-4">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0">
                      <p className="font-medium">{item.display_name}</p>
                      <p className="break-all text-sm text-muted-foreground">{item.email}</p>
                    </div>
                    <StatusBadge status={item.status} />
                  </div>
                  <div className="flex flex-wrap gap-1">
                    {item.roles.map((r) => (
                      <Badge key={`${r.role}-${r.department_scope_id ?? ""}`} tone={r.role === "learner" ? "neutral" : "primary"}>
                        {roleLabel(r.role)}
                      </Badge>
                    ))}
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {item.department?.name ?? "No department"} · Last sign-in {formatDate(item.last_login_at)}
                  </p>
                  <Button variant="secondary" size="sm" className="self-start" onClick={() => setEditing(item)} aria-label={`${canManage ? "Manage" : "View"} ${item.display_name}`}>
                    {canManage ? "Manage" : "View"}
                  </Button>
                </Card>
              ))}
            </ul>

            {pages > 1 ? (
              <nav aria-label="Pagination" className="flex items-center justify-between gap-3">
                <Button variant="secondary" size="sm" disabled={page <= 1} onClick={() => update({ page: String(page - 1) })}>
                  <ChevronLeft aria-hidden="true" />
                  Previous
                </Button>
                <p className="text-sm text-muted-foreground">Page {page} of {pages}</p>
                <Button variant="secondary" size="sm" disabled={page >= pages} onClick={() => update({ page: String(page + 1) })}>
                  Next
                  <ChevronRight aria-hidden="true" />
                </Button>
              </nav>
            ) : null}
          </>
        ) : null}
      </section>

      {canManage ? (
        <CreateUserDialog
          open={creating}
          onOpenChange={(open) => {
            setCreating(open);
            if (!open && params.get("new")) update({});
          }}
          viewer={user}
          departments={departments.data ?? []}
          onCreated={(created, link) => {
            setCreating(false);
            setIssuedLink({ user: created, link });
            users.reload();
          }}
        />
      ) : null}
      {editing ? (
        <ManageUserDialog
          key={editing.id}
          target={editing}
          viewer={user}
          departments={departments.data ?? []}
          onClose={() => setEditing(null)}
          onSaved={() => users.reload()}
          onLinkIssued={(link) => {
            setIssuedLink({ user: editing, link });
            setEditing(null);
          }}
        />
      ) : null}
    </div>
  );
}

function setPasswordUrl(link: PasswordLink): string {
  return `${window.location.origin}/set-password#token=${encodeURIComponent(link.token)}`;
}

/** Shown once, right after issuing. The token is not stored by the page and cannot be retrieved again. */
function PasswordLinkNotice({ user, link, onDismiss }: { user: AdminUser; link: PasswordLink; onDismiss: () => void }) {
  const [copied, setCopied] = useState(false);
  const url = setPasswordUrl(link);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => ref.current?.focus(), []);

  async function copy() {
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
    } catch {
      toast("Copy did not work", { description: "Select the link and copy it manually." });
    }
  }

  return (
    <div ref={ref} tabIndex={-1} className="focus:outline-none">
      <Alert tone="success" role="status" title={`${link.purpose === "account_setup" ? "Account setup" : "Password reset"} link for ${user.display_name}`}>
        <p>
          Give this link to {user.display_name} through a trusted channel. It works once and expires{" "}
          {new Date(link.expires_at).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" })}. It will not be shown again.
        </p>
        <div className="mt-3 flex flex-col gap-2 sm:flex-row">
          <label htmlFor="password-link" className="sr-only">Set-password link</label>
          <Input id="password-link" readOnly value={url} onFocus={(e) => e.currentTarget.select()} className="font-mono text-sm text-foreground" />
          <Button type="button" variant="secondary" onClick={() => void copy()}>
            {copied ? <Check aria-hidden="true" /> : <Copy aria-hidden="true" />}
            {copied ? "Copied" : "Copy link"}
          </Button>
          <Button type="button" variant="ghost" onClick={onDismiss}>Done</Button>
        </div>
        <p className="mt-2 text-xs">No email is sent: this environment has no email service.</p>
      </Alert>
    </div>
  );
}

interface RoleChoice {
  role: string;
  disabled: boolean;
  reason?: string;
}

function roleChoices(viewer: Me, targetId: string | null): RoleChoice[] {
  const canAssign = can(viewer, "roles.assign");
  return ROLE_ORDER.map((role) => {
    if (targetId === viewer.id) return { role, disabled: true, reason: "You cannot change your own access roles." };
    if (role === "learner") return { role, disabled: !canAssign && targetId !== null };
    if (!canAssign) return { role, disabled: true, reason: "Your access role can manage learner accounts only." };
    if (role === "platform_admin" && !viewer.access_roles.includes("platform_admin"))
      return { role, disabled: true, reason: "Only a platform administrator can grant this role." };
    return { role, disabled: false };
  });
}

function CreateUserDialog({
  open,
  onOpenChange,
  viewer,
  departments,
  onCreated,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  viewer: Me;
  departments: AdminDepartment[];
  onCreated: (user: AdminUser, link: PasswordLink) => void;
}) {
  const [values, setValues] = useState({ display_name: "", email: "", registration_id: "", designation: "", department_id: "" });
  const [roles, setRoles] = useState<string[]>(["learner"]);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [problem, setProblem] = useState<{ title: string; body?: string; reference?: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);
  const activeDepartments = departments.filter((d) => d.status === "active");

  useEffect(() => {
    if (!open) {
      setValues({ display_name: "", email: "", registration_id: "", designation: "", department_id: "" });
      setRoles(["learner"]);
      setErrors({});
      setProblem(null);
    }
  }, [open]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const found: FieldErrors = {};
    if (values.display_name.trim().length < 2) found.display_name = "Enter the person's full name.";
    if (!EMAIL_RE.test(values.email.trim())) found.email = "Enter an email address in the format name@example.org.";
    if (values.registration_id.trim() && !REGISTRATION_ID_RE.test(values.registration_id.trim()))
      found.registration_id = "Use 3 to 40 letters, numbers, hyphens or slashes.";
    if (roles.length === 0) found.roles = "Choose at least one access role.";
    if (roles.includes("department_admin") && !values.department_id) found.department_id = "A department administrator needs a department.";
    setErrors(found);
    setProblem(null);
    if (Object.keys(found).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setSaving(true);
    try {
      const created = await api<{ user: AdminUser; setup: PasswordLink }>("/api/v1/admin/users", {
        method: "POST",
        body: {
          display_name: values.display_name.trim(),
          email: values.email.trim(),
          registration_id: values.registration_id.trim() || null,
          designation: values.designation.trim() || null,
          department_id: values.department_id || null,
          roles: roles.map((role) => ({ role })),
        },
      });
      toast("User added", { description: "Share the account setup link shown on the page." });
      onCreated(created.user, created.setup);
    } catch (err) {
      const apiError = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Failed");
      const fields = serverFieldErrors(apiError);
      setErrors(fields);
      setProblem(Object.keys(fields).length ? null : { title: "The user was not added.", body: apiError.detail, reference: apiError.correlationId });
      window.setTimeout(() => summaryRef.current?.focus(), 0);
    } finally {
      setSaving(false);
    }
  }

  const set = (field: keyof typeof values) => (event: { target: { value: string } }) => setValues((v) => ({ ...v, [field]: event.target.value }));

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>Add a user</DialogTitle>
          <DialogDescription>The account starts as invited. You receive a one-time link for the person to set their own password.</DialogDescription>
        </DialogHeader>
        <div className="empty:hidden">
          <ErrorSummary
            ref={summaryRef}
            errors={errors}
            labels={{ display_name: "Full name", email: "Email", registration_id: "Registration ID", department_id: "Department", roles: "Access roles" }}
            problem={problem}
          />
        </div>
        <form id="create-user-form" onSubmit={handleSubmit} noValidate className="grid gap-4 sm:grid-cols-2">
          <Field id="display_name" label="Full name" error={errors.display_name}>
            <Input id="display_name" value={values.display_name} onChange={set("display_name")} aria-invalid={errors.display_name ? true : undefined} aria-describedby={describedBy("display_name", errors.display_name)} />
          </Field>
          <Field id="email" label="Email" error={errors.email}>
            <Input id="email" type="email" value={values.email} onChange={set("email")} aria-invalid={errors.email ? true : undefined} aria-describedby={describedBy("email", errors.email)} />
          </Field>
          <Field id="registration_id" label="Registration ID (optional)" error={errors.registration_id}>
            <Input id="registration_id" value={values.registration_id} onChange={set("registration_id")} spellCheck={false} aria-invalid={errors.registration_id ? true : undefined} aria-describedby={describedBy("registration_id", errors.registration_id)} />
          </Field>
          <Field id="designation" label="Designation (optional)">
            <Input id="designation" value={values.designation} onChange={set("designation")} />
          </Field>
          <Field id="department_id" label="Department" error={errors.department_id}>
            <Select id="department_id" value={values.department_id} onChange={set("department_id")} aria-invalid={errors.department_id ? true : undefined} aria-describedby={describedBy("department_id", errors.department_id)}>
              <option value="">Not set</option>
              {activeDepartments.map((d) => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </Select>
          </Field>
          <RolePicker id="roles" choices={roleChoices(viewer, null)} selected={roles} onChange={setRoles} error={errors.roles} />
        </form>
        <DialogFooter>
          <Button type="button" variant="ghost" onClick={() => onOpenChange(false)}>Cancel</Button>
          <Button type="submit" form="create-user-form" disabled={saving}>
            {saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : <UserPlus aria-hidden="true" />}
            {saving ? "Adding..." : "Add user"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function RolePicker({
  id,
  choices,
  selected,
  onChange,
  error,
}: {
  id: string;
  choices: RoleChoice[];
  selected: string[];
  onChange: (roles: string[]) => void;
  error?: string;
}) {
  const reasons = [...new Set(choices.filter((c) => c.disabled && c.reason).map((c) => c.reason))];
  return (
    <fieldset id={id} className="sm:col-span-2" aria-describedby={error ? `${id}-error` : undefined}>
      <legend className="text-sm font-medium">Access roles</legend>
      {reasons.length ? <p className="mt-1 text-sm text-muted-foreground">{reasons.join(" ")}</p> : null}
      <div className="mt-2 grid gap-2 sm:grid-cols-2">
        {choices.map((choice) => (
          <label key={choice.role} className="flex min-h-11 items-center gap-3 rounded-md border border-border px-3 py-2 text-sm has-[:disabled]:opacity-60">
            <Checkbox
              checked={selected.includes(choice.role)}
              disabled={choice.disabled}
              onChange={(e) => onChange(e.target.checked ? [...selected, choice.role] : selected.filter((r) => r !== choice.role))}
            />
            {roleLabel(choice.role)}
          </label>
        ))}
      </div>
      {error ? <p id={`${id}-error`} className="mt-1 text-sm font-medium text-danger">{error}</p> : null}
    </fieldset>
  );
}

function ManageUserDialog({
  target,
  viewer,
  departments,
  onClose,
  onSaved,
  onLinkIssued,
}: {
  target: AdminUser;
  viewer: Me;
  departments: AdminDepartment[];
  onClose: () => void;
  onSaved: () => void;
  onLinkIssued: (link: PasswordLink) => void;
}) {
  const canManage = can(viewer, "users.manage");
  const isSelf = target.id === viewer.id;
  const [current, setCurrent] = useState(target);
  const [values, setValues] = useState({
    display_name: target.display_name,
    registration_id: target.registration_id ?? "",
    designation: target.designation ?? "",
    department_id: target.department?.id ?? "",
  });
  const [roles, setRoles] = useState(target.roles.map((r) => r.role));
  const [errors, setErrors] = useState<FieldErrors>({});
  const [problem, setProblem] = useState<{ title: string; body?: string; reference?: string } | null>(null);
  const [busy, setBusy] = useState<"save" | "status" | "link" | null>(null);
  const summaryRef = useRef<HTMLDivElement>(null);
  const readOnly = !canManage;
  const rolesChanged = [...roles].sort().join() !== [...current.roles.map((r) => r.role)].sort().join();

  function fail(err: unknown, title: string) {
    const apiError = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Failed");
    const fields = serverFieldErrors(apiError);
    setErrors(fields);
    const body = apiError.code === "STALE_VERSION" ? "Someone else changed this account. Close this window and open it again." : apiError.detail;
    setProblem(Object.keys(fields).length ? null : { title, body, reference: apiError.correlationId });
    window.setTimeout(() => summaryRef.current?.focus(), 0);
  }

  async function patch(body: Record<string, unknown>) {
    const updated = await api<AdminUser>(`/api/v1/admin/users/${current.id}`, { method: "PATCH", body: { row_version: current.row_version, ...body } });
    setCurrent(updated);
    onSaved();
    return updated;
  }

  async function handleSave(event: FormEvent) {
    event.preventDefault();
    const found: FieldErrors = {};
    if (values.display_name.trim().length < 2) found.display_name = "Enter the person's full name.";
    if (values.registration_id.trim() && !REGISTRATION_ID_RE.test(values.registration_id.trim()))
      found.registration_id = "Use 3 to 40 letters, numbers, hyphens or slashes.";
    if (roles.length === 0) found.roles = "Keep at least one access role.";
    setErrors(found);
    setProblem(null);
    if (Object.keys(found).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setBusy("save");
    try {
      await patch({
        display_name: values.display_name.trim(),
        registration_id: values.registration_id.trim() || null,
        designation: values.designation.trim() || null,
        department_id: values.department_id || null,
        ...(rolesChanged ? { roles: roles.map((role) => ({ role })) } : {}),
      });
      toast("Changes saved", rolesChanged ? { description: "Role changes take effect when the person next signs in." } : undefined);
    } catch (err) {
      fail(err, "Changes were not saved.");
    } finally {
      setBusy(null);
    }
  }

  async function toggleStatus() {
    setBusy("status");
    setProblem(null);
    try {
      const next = current.status === "inactive" ? "active" : "inactive";
      await patch({ status: next });
      toast(next === "inactive" ? "Account deactivated" : "Account reactivated", next === "inactive" ? { description: "The person was signed out." } : undefined);
    } catch (err) {
      fail(err, "The status was not changed.");
    } finally {
      setBusy(null);
    }
  }

  async function issueLink() {
    setBusy("link");
    setProblem(null);
    try {
      const link = await api<PasswordLink>(`/api/v1/admin/users/${current.id}/password-link`, { method: "POST" });
      onLinkIssued(link);
    } catch (err) {
      fail(err, "No link was issued.");
      setBusy(null);
    }
  }

  const set = (field: keyof typeof values) => (event: { target: { value: string } }) => setValues((v) => ({ ...v, [field]: event.target.value }));

  return (
    <Dialog open onOpenChange={(open) => (open ? null : onClose())}>
      <DialogContent
        className="max-h-[90vh] overflow-y-auto sm:max-w-2xl"
        onOpenAutoFocus={(event) => {
          // Start on the dialog, not inside a text field: avoids selecting the name and opening the mobile keyboard.
          event.preventDefault();
          (event.currentTarget as HTMLElement).focus();
        }}
      >
        <DialogHeader>
          <DialogTitle>{current.display_name}</DialogTitle>
          <DialogDescription className="flex flex-wrap items-center gap-2">
            <span className="break-all">{current.email}</span>
            <StatusBadge status={current.status} />
            {current.is_synthetic ? <Badge tone="demo">Synthetic account</Badge> : null}
          </DialogDescription>
        </DialogHeader>

        <div className="empty:hidden">
          <ErrorSummary ref={summaryRef} errors={errors} labels={{ display_name: "Full name", registration_id: "Registration ID", roles: "Access roles" }} problem={problem} />
        </div>

        <form id="manage-user-form" onSubmit={handleSave} noValidate className="grid gap-4 sm:grid-cols-2">
          <Field id="display_name" label="Full name" error={errors.display_name}>
            <Input id="display_name" value={values.display_name} onChange={set("display_name")} readOnly={readOnly} aria-invalid={errors.display_name ? true : undefined} aria-describedby={describedBy("display_name", errors.display_name)} />
          </Field>
          <Field id="registration_id" label="Registration ID" error={errors.registration_id}>
            <Input id="registration_id" value={values.registration_id} onChange={set("registration_id")} readOnly={readOnly} spellCheck={false} aria-invalid={errors.registration_id ? true : undefined} aria-describedby={describedBy("registration_id", errors.registration_id)} />
          </Field>
          <Field id="designation" label="Designation">
            <Input id="designation" value={values.designation} onChange={set("designation")} readOnly={readOnly} />
          </Field>
          <Field id="department_id" label="Department">
            <Select id="department_id" value={values.department_id} onChange={set("department_id")} disabled={readOnly}>
              <option value="">Not set</option>
              {departments.map((d) => (
                <option key={d.id} value={d.id}>{d.name}</option>
              ))}
            </Select>
          </Field>
          <RolePicker id="roles" choices={readOnly ? ROLE_ORDER.map((role) => ({ role, disabled: true })) : roleChoices(viewer, current.id)} selected={roles} onChange={setRoles} error={errors.roles} />
          <dl className="grid gap-1 text-sm text-muted-foreground sm:col-span-2 sm:grid-cols-2">
            <div><dt className="inline">Created: </dt><dd className="inline">{formatDate(current.created_at)}</dd></div>
            <div><dt className="inline">Last sign-in: </dt><dd className="inline">{formatDate(current.last_login_at)}</dd></div>
          </dl>
        </form>

        {canManage && !isSelf ? (
          <section aria-labelledby="access-actions" className="space-y-3 rounded-lg border border-border p-4">
            <h3 id="access-actions" className="text-sm font-semibold">Access</h3>
            <div className="flex flex-col gap-2 sm:flex-row sm:flex-wrap">
              {current.status !== "inactive" ? (
                <Button type="button" variant="secondary" onClick={() => void issueLink()} disabled={busy !== null}>
                  {busy === "link" ? <Loader2 className="animate-spin" aria-hidden="true" /> : <KeyRound aria-hidden="true" />}
                  {current.has_password ? "Issue password reset link" : "Issue account setup link"}
                </Button>
              ) : null}
              {current.status !== "invited" || current.has_password ? (
                <Button type="button" variant={current.status === "inactive" ? "secondary" : "danger"} onClick={() => void toggleStatus()} disabled={busy !== null}>
                  {busy === "status" ? <Loader2 className="animate-spin" aria-hidden="true" /> : null}
                  {current.status === "inactive" ? "Reactivate account" : "Deactivate account"}
                </Button>
              ) : null}
            </div>
            <p className="text-sm text-muted-foreground">
              {current.status === "inactive"
                ? "Inactive accounts cannot sign in. Their assessment history is kept."
                : "Deactivating signs the person out immediately. Issuing a new link cancels any earlier link."}
            </p>
          </section>
        ) : null}
        {isSelf ? <p className="text-sm text-muted-foreground">This is your account. Change your password from your profile.</p> : null}

        <DialogFooter>
          <Button type="button" variant="ghost" onClick={onClose}>{readOnly ? "Close" : "Cancel"}</Button>
          {readOnly ? null : (
            <Button type="submit" form="manage-user-form" disabled={busy !== null}>
              {busy === "save" ? <Loader2 className="animate-spin" aria-hidden="true" /> : null}
              {busy === "save" ? "Saving..." : "Save changes"}
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
