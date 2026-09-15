import { KeyRound, Loader2, Save, UserRound } from "lucide-react";
import { useRef, useState, type FormEvent } from "react";
import { Link } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import type { DepartmentRef, Me } from "@/api/types";
import { useApi } from "@/api/useApi";
import { useAuth } from "@/auth/AuthContext";
import { ErrorSummary, PASSWORD_MIN_LENGTH, PasswordInput, describedBy, serverFieldErrors, type FieldErrors } from "@/components/product/forms";
import { cleanName } from "@/components/product/competency";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/form";
import { Select } from "@/components/ui/select";
import { toast } from "@/components/ui/toaster";
import { roleLabel } from "@/config/roles";

function formatDateTime(value: string | null | undefined): string {
  if (!value) return "Not recorded";
  return new Date(value).toLocaleString("en-IN", { dateStyle: "medium", timeStyle: "short" });
}

/** The signed-in person's own account: details they may change, what is managed by an administrator, and password change. */
export function ProfilePage() {
  const { user } = useAuth();
  if (!user) return null;
  return (
    <div className="space-y-8">
      <header className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">Your profile</h1>
        <p className="text-muted-foreground">Your account details and password.</p>
      </header>
      <div className="grid gap-6 lg:grid-cols-[minmax(0,1.3fr)_minmax(0,1fr)]">
        <DetailsForm user={user} />
        <AccountFacts user={user} />
      </div>
      <PasswordForm />
    </div>
  );
}

function DetailsForm({ user }: { user: Me }) {
  const { setUser } = useAuth();
  const departments = useApi<DepartmentRef[]>("/api/v1/departments");
  const [displayName, setDisplayName] = useState(user.display_name);
  const [designation, setDesignation] = useState(user.designation ?? "");
  const [departmentId, setDepartmentId] = useState(user.department?.id ?? "");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [problem, setProblem] = useState<{ title: string; body?: string; reference?: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const found: FieldErrors = {};
    if (displayName.trim().length < 2) found.display_name = "Enter your full name.";
    setErrors(found);
    setProblem(null);
    if (Object.keys(found).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setSaving(true);
    try {
      const updated = await api<Me>("/api/v1/me", {
        method: "PATCH",
        body: { display_name: displayName.trim(), designation: designation.trim() || null, department_id: departmentId || null },
      });
      setUser(updated);
      toast("Profile saved");
    } catch (err) {
      const apiError = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Failed");
      setErrors(serverFieldErrors(apiError));
      setProblem({ title: "Your changes were not saved.", body: apiError.detail, reference: apiError.correlationId });
      window.setTimeout(() => summaryRef.current?.focus(), 0);
    } finally {
      setSaving(false);
    }
  }

  return (
    <Card as="section" aria-labelledby="details-title" className="p-6">
      <h2 id="details-title" className="flex items-center gap-2 text-lg font-semibold">
        <UserRound className="size-5 text-muted-foreground" aria-hidden="true" />
        Details
      </h2>
      <div className="mt-4 empty:hidden">
        <ErrorSummary ref={summaryRef} errors={errors} labels={{ display_name: "Full name", department_id: "Department" }} problem={problem} />
      </div>
      <form onSubmit={handleSubmit} noValidate className="mt-4 space-y-5">
        <Field id="display_name" label="Full name" error={errors.display_name}>
          <Input
            id="display_name"
            autoComplete="name"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            aria-invalid={errors.display_name ? true : undefined}
            aria-describedby={describedBy("display_name", errors.display_name)}
          />
        </Field>
        <Field id="designation" label="Designation (optional)">
          <Input id="designation" autoComplete="organization-title" value={designation} onChange={(e) => setDesignation(e.target.value)} />
        </Field>
        <Field id="department_id" label="Department" error={errors.department_id}>
          <Select id="department_id" value={departmentId} onChange={(e) => setDepartmentId(e.target.value)} disabled={departments.loading}>
            <option value="">Not set</option>
            {(departments.data ?? []).map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
          </Select>
        </Field>
        <Button type="submit" disabled={saving}>
          {saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : <Save aria-hidden="true" />}
          {saving ? "Saving..." : "Save details"}
        </Button>
      </form>
    </Card>
  );
}

function AccountFacts({ user }: { user: Me }) {
  return (
    <Card as="section" aria-labelledby="account-title" className="p-6">
      <h2 id="account-title" className="text-lg font-semibold">Account</h2>
      <p className="mt-1 text-sm text-muted-foreground">Managed by your administrator.</p>
      <dl className="mt-4 grid gap-4 text-sm">
        <div>
          <dt className="text-muted-foreground">Email</dt>
          <dd className="break-all font-medium">{user.email}</dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Registration ID</dt>
          <dd className="font-medium">{user.registration_id ?? "Not recorded"}</dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Access</dt>
          <dd className="mt-1 flex flex-wrap gap-1.5">
            {user.access_roles.map((role) => (
              <Badge key={role} tone={role === "learner" ? "neutral" : "primary"}>
                {roleLabel(role)}
              </Badge>
            ))}
          </dd>
        </div>
        {user.can_take_assessments ? (
          <div>
            <dt className="text-muted-foreground">Job role</dt>
            <dd className="font-medium">
              {user.job_role ? cleanName(user.job_role.name) : "Not chosen"}{" "}
              <Link to="/get-started" className="ml-1 text-primary underline underline-offset-4">
                Change
              </Link>
            </dd>
          </div>
        ) : null}
        <div>
          <dt className="text-muted-foreground">Last sign-in</dt>
          <dd className="font-medium">{formatDateTime(user.last_login_at)}</dd>
        </div>
      </dl>
    </Card>
  );
}

function PasswordForm() {
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [confirm, setConfirm] = useState("");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [problem, setProblem] = useState<{ title: string; body?: string; reference?: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const found: FieldErrors = {};
    if (!current) found.current_password = "Enter your current password.";
    if (next.length < PASSWORD_MIN_LENGTH) found.new_password = `Use at least ${PASSWORD_MIN_LENGTH} characters.`;
    else if (next === current) found.new_password = "Choose a password different from your current one.";
    if (confirm !== next) found.confirm = "The passwords do not match.";
    setErrors(found);
    setProblem(null);
    if (Object.keys(found).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setSaving(true);
    try {
      await api<void>("/api/v1/auth/password/change", { method: "POST", body: { current_password: current, new_password: next } });
      setCurrent("");
      setNext("");
      setConfirm("");
      toast("Password changed", { description: "You were signed out on your other devices." });
    } catch (err) {
      const apiError = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Failed");
      const fields = serverFieldErrors(apiError);
      setErrors(fields);
      setProblem(Object.keys(fields).length ? null : { title: "Your password was not changed.", body: apiError.detail, reference: apiError.correlationId });
      window.setTimeout(() => summaryRef.current?.focus(), 0);
    } finally {
      setSaving(false);
    }
  }

  return (
    <Card as="section" aria-labelledby="password-title" className="p-6">
      <h2 id="password-title" className="flex items-center gap-2 text-lg font-semibold">
        <KeyRound className="size-5 text-muted-foreground" aria-hidden="true" />
        Change password
      </h2>
      <p className="mt-1 text-sm text-muted-foreground">Changing your password signs you out everywhere else.</p>
      <div className="mt-4 empty:hidden">
        <ErrorSummary
          ref={summaryRef}
          errors={errors}
          labels={{ current_password: "Current password", new_password: "New password", confirm: "Confirm new password" }}
          problem={problem}
        />
      </div>
      <form onSubmit={handleSubmit} noValidate className="mt-4 grid gap-5 md:grid-cols-3">
        <Field id="current_password" label="Current password" error={errors.current_password}>
          <PasswordInput
            id="current_password"
            autoComplete="current-password"
            value={current}
            onChange={(e) => setCurrent(e.target.value)}
            aria-invalid={errors.current_password ? true : undefined}
            aria-describedby={describedBy("current_password", errors.current_password)}
          />
        </Field>
        <Field id="new_password" label="New password" error={errors.new_password}>
          <PasswordInput
            id="new_password"
            autoComplete="new-password"
            value={next}
            onChange={(e) => setNext(e.target.value)}
            aria-invalid={errors.new_password ? true : undefined}
            aria-describedby={describedBy("new_password", errors.new_password)}
          />
        </Field>
        <Field id="confirm" label="Confirm new password" error={errors.confirm}>
          <PasswordInput
            id="confirm"
            autoComplete="new-password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            aria-invalid={errors.confirm ? true : undefined}
            aria-describedby={describedBy("confirm", errors.confirm)}
          />
        </Field>
        <div className="md:col-span-3">
          <Button type="submit" variant="secondary" disabled={saving}>
            {saving ? <Loader2 className="animate-spin" aria-hidden="true" /> : null}
            {saving ? "Changing..." : "Change password"}
          </Button>
        </div>
      </form>
    </Card>
  );
}
