import { ArrowRight, Loader2 } from "lucide-react";
import { useRef, useState, type FormEvent } from "react";
import { Link, Navigate, useNavigate } from "react-router-dom";
import { ApiError } from "@/api/client";
import type { RegistrationOptions } from "@/api/types";
import { useApi } from "@/api/useApi";
import { homeFor, useAuth } from "@/auth/AuthContext";
import {
  EMAIL_RE,
  ErrorSummary,
  PASSWORD_MIN_LENGTH,
  PasswordInput,
  REGISTRATION_ID_RE,
  describedBy,
  serverFieldErrors,
  type FieldErrors,
} from "@/components/product/forms";
import { ErrorState, LoadingState } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/form";
import { Select } from "@/components/ui/select";

const LABELS: Record<string, string> = {
  display_name: "Full name",
  email: "Email",
  registration_id: "Registration ID",
  department_id: "Department",
  password: "Password",
  confirm: "Confirm password",
};

function problemFor(error: ApiError): { title: string; body?: string; reference?: string } | null {
  if (error.code === "EMAIL_IN_USE" || error.code === "REGISTRATION_ID_IN_USE" || error.code === "VALIDATION_FAILED") return null;
  if (error.code === "REGISTRATION_DISABLED") return { title: "Registration is not available.", body: error.detail };
  return { title: "Your account was not created.", body: error.detail ?? "Try again in a moment.", reference: error.correlationId };
}

/** Learner self-registration (Phase 4A, assumption A-1). Creates a learner account only; administrators are never self-registered. */
export function RegisterPage() {
  const { user, register } = useAuth();
  const navigate = useNavigate();
  const options = useApi<RegistrationOptions>("/api/v1/auth/registration-options");
  const [values, setValues] = useState({ display_name: "", email: "", registration_id: "", department_id: "", password: "", confirm: "" });
  const [errors, setErrors] = useState<FieldErrors>({});
  const [problem, setProblem] = useState<ReturnType<typeof problemFor>>(null);
  const [submitting, setSubmitting] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);

  if (user && !submitting) return <Navigate to={homeFor(user)} replace />;

  const set = (field: keyof typeof values) => (event: { target: { value: string } }) =>
    setValues((current) => ({ ...current, [field]: event.target.value }));

  function validate(): FieldErrors {
    const out: FieldErrors = {};
    if (values.display_name.trim().length < 2) out.display_name = "Enter your full name.";
    if (!EMAIL_RE.test(values.email.trim())) out.email = "Enter an email address in the format name@example.org.";
    if (!REGISTRATION_ID_RE.test(values.registration_id.trim()))
      out.registration_id = "Use 3 to 40 letters, numbers, hyphens or slashes, starting with a letter or number.";
    if (values.password.length < PASSWORD_MIN_LENGTH) out.password = `Use at least ${PASSWORD_MIN_LENGTH} characters.`;
    if (values.confirm !== values.password) out.confirm = "The passwords do not match.";
    return out;
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const found = validate();
    setErrors(found);
    setProblem(null);
    if (Object.keys(found).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setSubmitting(true);
    try {
      await register({
        display_name: values.display_name.trim(),
        email: values.email.trim(),
        registration_id: values.registration_id.trim(),
        password: values.password,
        ...(values.department_id ? { department_id: values.department_id } : {}),
      });
      navigate("/get-started", { replace: true });
    } catch (err) {
      const apiError = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Registration failed");
      const fromServer = serverFieldErrors(apiError);
      if (apiError.code === "EMAIL_IN_USE") fromServer.email = "An account with this email already exists. Sign in instead.";
      if (apiError.code === "REGISTRATION_ID_IN_USE") fromServer.registration_id = "This registration ID is already linked to an account.";
      setErrors(fromServer);
      setProblem(problemFor(apiError) ?? (Object.keys(fromServer).length ? null : { title: "Check the details you entered." }));
      setSubmitting(false);
      window.setTimeout(() => summaryRef.current?.focus(), 0);
    }
  }

  const inputProps = (field: keyof typeof values, hint = false) => ({
    id: field,
    value: values[field],
    onChange: set(field),
    disabled: submitting,
    "aria-invalid": errors[field] ? true : undefined,
    "aria-describedby": describedBy(field, errors[field], hint),
  });

  return (
    <Card as="section" aria-labelledby="register-title" className="mx-auto w-full max-w-xl p-6 shadow-raised sm:p-8">
      <div className="space-y-1.5">
        <h1 id="register-title" className="text-2xl font-semibold tracking-tight">Create a learner account</h1>
        <p className="text-muted-foreground">
          For learners only. Trainers and administrators receive their accounts from an organisation administrator.
        </p>
      </div>

      {options.loading ? <LoadingState label="Loading registration" className="mt-6" /> : null}
      {options.error ? <ErrorState error={options.error} onRetry={options.reload} className="mt-6" /> : null}
      {options.data && !options.data.enabled ? (
        <Alert tone="info" title="Registration is not available here" className="mt-6">
          Accounts in this environment are created by an administrator. <Link to="/login">Go to sign in</Link>
        </Alert>
      ) : null}

      {options.data?.enabled ? (
        <>
          <div className="mt-6 empty:hidden">
            <ErrorSummary ref={summaryRef} errors={errors} labels={LABELS} problem={problem} />
          </div>
          <form onSubmit={handleSubmit} noValidate className="mt-6 space-y-5">
            {options.data.organization_name ? (
              <p className="text-sm text-muted-foreground">
                Organisation: <span className="font-medium text-foreground">{options.data.organization_name}</span>
              </p>
            ) : null}
            <Field id="display_name" label="Full name" error={errors.display_name}>
              <Input {...inputProps("display_name")} autoComplete="name" />
            </Field>
            <Field id="email" label="Email" error={errors.email}>
              <Input {...inputProps("email")} type="email" inputMode="email" autoComplete="email" />
            </Field>
            <Field id="registration_id" label="Registration ID" hint="Your staff or learner identifier, for example STA-2026-0142." error={errors.registration_id}>
              <Input {...inputProps("registration_id", true)} autoComplete="off" spellCheck={false} />
            </Field>
            <Field id="department_id" label="Department (optional)" error={errors.department_id}>
              <Select {...inputProps("department_id")}>
                <option value="">Choose later</option>
                {options.data.departments.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name}
                  </option>
                ))}
              </Select>
            </Field>
            <Field id="password" label="Password" hint={`At least ${PASSWORD_MIN_LENGTH} characters. A short phrase is easier to remember.`} error={errors.password}>
              <PasswordInput {...inputProps("password", true)} autoComplete="new-password" />
            </Field>
            <Field id="confirm" label="Confirm password" error={errors.confirm}>
              <PasswordInput {...inputProps("confirm")} autoComplete="new-password" />
            </Field>
            <Button type="submit" size="lg" className="w-full" disabled={submitting}>
              {submitting ? <Loader2 className="animate-spin" aria-hidden="true" /> : null}
              {submitting ? "Creating account..." : "Create account"}
              {submitting ? null : <ArrowRight aria-hidden="true" />}
            </Button>
            <p className="text-sm text-muted-foreground">
              Your job role is chosen in the next step. Results are development guidance only, never an appraisal.
            </p>
          </form>
        </>
      ) : null}

      <p className="mt-6 border-t border-border pt-5 text-sm">
        Already have an account?{" "}
        <Link to="/login" className="font-medium text-primary underline-offset-4 hover:underline">
          Sign in
        </Link>
      </p>
    </Card>
  );
}
