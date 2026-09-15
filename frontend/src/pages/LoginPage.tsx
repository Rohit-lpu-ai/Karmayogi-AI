import { ArrowRight, BookOpen, ClipboardCheck, GraduationCap, Info, Loader2, ShieldCheck, Target, UserCog } from "lucide-react";
import { useEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import { Link, Navigate, useLocation, useNavigate, useSearchParams } from "react-router-dom";
import { ApiError } from "@/api/client";
import { homeFor, isAdministrator, useAuth } from "@/auth/AuthContext";
import { EMAIL_RE, ErrorSummary, PasswordInput, describedBy, type FieldErrors } from "@/components/product/forms";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field, Input } from "@/components/ui/form";
import { toast } from "@/components/ui/toaster";
import { PRODUCT } from "@/config/product";
import { cn } from "@/lib/utils";

type Mode = "learner" | "admin";

function messageFor(error: ApiError): { title: string; body: string; reference?: string } {
  const reference = error.correlationId;
  switch (error.code) {
    case "INVALID_CREDENTIALS":
      return { title: "Email or password is incorrect.", body: "Check both and try again. After several failed attempts the account is locked for a short time.", reference };
    case "ACCOUNT_LOCKED":
      return { title: "This account is temporarily locked.", body: error.detail ?? "Too many failed sign-ins. Wait a few minutes, or contact your administrator.", reference };
    case "BACKEND_UNAVAILABLE":
    case "NETWORK_ERROR":
      return { title: "The platform cannot be reached right now.", body: error.detail ?? "Check your connection and try again.", reference };
    case "VALIDATION_FAILED":
      return { title: "Check the details you entered.", body: "Enter a valid email address and your password.", reference };
    default:
      return { title: "Sign-in did not work.", body: error.detail ?? "Try again in a moment.", reference };
  }
}

const MODES: { id: Mode; label: string; icon: ReactNode }[] = [
  { id: "learner", label: "Learner", icon: <GraduationCap aria-hidden="true" /> },
  { id: "admin", label: "Administration", icon: <UserCog aria-hidden="true" /> },
];

/** Sign-in with two entry points (Phase 4A): learners, and administrators, trainers and auditors. */
export function LoginPage() {
  const { user, login, environment } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as { from?: string; notice?: string } | null;
  // The mode lives in the URL: signing in swaps the signed-out frame for the signed-in one, which remounts this page.
  const [searchParams, setSearchParams] = useSearchParams();
  const mode: Mode = searchParams.get("as") === "admin" ? "admin" : "learner";
  const setMode = (next: Mode) => setSearchParams(next === "admin" ? { as: "admin" } : {}, { replace: true, state: location.state });
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [error, setError] = useState<ApiError | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);

  const adminDenied = Boolean(user && mode === "admin" && !state?.from && !isAdministrator(user));
  useEffect(() => {
    if (adminDenied) toast("This account has no administration access.", { description: "You are signed in to your learning space." });
  }, [adminDenied]);

  if (user && !submitting) {
    const target = state?.from ?? (mode === "admin" && isAdministrator(user) ? "/admin" : homeFor(user));
    return <Navigate to={target} replace />;
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const errors: FieldErrors = {};
    if (!email.trim()) errors.email = "Enter your email address.";
    else if (!EMAIL_RE.test(email.trim())) errors.email = "Enter an email address in the format name@example.org.";
    if (!password) errors.password = "Enter your password.";
    setFieldErrors(errors);
    setError(null);
    if (Object.keys(errors).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setSubmitting(true);
    try {
      const signedIn = await login(email.trim(), password);
      navigate(state?.from ?? (mode === "admin" && isAdministrator(signedIn) ? "/admin" : homeFor(signedIn)), { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Sign-in failed"));
      setSubmitting(false);
      window.setTimeout(() => summaryRef.current?.focus(), 0);
    }
  }

  const registrationOpen = environment?.self_registration_enabled === true;

  return (
    <div className="mx-auto grid w-full max-w-6xl items-center gap-10 lg:grid-cols-[minmax(0,1.1fr)_minmax(0,28rem)] lg:gap-16">
      <Card as="section" aria-labelledby="login-title" className="p-6 shadow-raised sm:p-8 lg:order-2">
        <div className="space-y-1.5">
          <h1 id="login-title" className="text-2xl font-semibold tracking-tight">Sign in</h1>
          <p className="text-muted-foreground">
            {mode === "learner" ? "Continue your assessment and learning." : "For administrators, trainers and auditors."}
          </p>
        </div>

        <div role="group" aria-label="Sign in as" className="mt-5 grid grid-cols-2 gap-1 rounded-lg bg-muted p-1">
          {MODES.map((item) => (
            <button
              key={item.id}
              type="button"
              aria-pressed={mode === item.id}
              data-focus-ring=""
              onClick={() => setMode(item.id)}
              className={cn(
                "flex h-10 items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors [&_svg]:size-4",
                "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                mode === item.id ? "bg-card text-foreground shadow-card" : "text-muted-foreground hover:text-foreground",
              )}
            >
              {item.icon}
              {item.label}
            </button>
          ))}
        </div>

        {state?.notice ? (
          <Alert tone="success" role="status" className="mt-5">
            {state.notice}
          </Alert>
        ) : null}

        <div className="mt-5 empty:hidden">
          <ErrorSummary ref={summaryRef} errors={fieldErrors} labels={{}} problem={error ? messageFor(error) : null} />
        </div>

        <form onSubmit={handleSubmit} noValidate className="mt-5 space-y-5">
          <Field id="email" label="Email" error={fieldErrors.email}>
            <Input
              id="email"
              type="email"
              autoComplete="username"
              inputMode="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={submitting}
              aria-invalid={fieldErrors.email ? true : undefined}
              aria-describedby={describedBy("email", fieldErrors.email)}
            />
          </Field>
          <Field id="password" label="Password" error={fieldErrors.password}>
            <PasswordInput
              id="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={submitting}
              aria-invalid={fieldErrors.password ? true : undefined}
              aria-describedby={describedBy("password", fieldErrors.password)}
            />
          </Field>

          <Button type="submit" size="lg" className="w-full" disabled={submitting}>
            {submitting ? <Loader2 className="animate-spin" aria-hidden="true" /> : null}
            {submitting ? "Signing in..." : mode === "admin" ? "Sign in to administration" : "Sign in"}
            {submitting ? null : <ArrowRight aria-hidden="true" />}
          </Button>
        </form>

        <div className="mt-6 space-y-3 border-t border-border pt-5 text-sm">
          {mode === "learner" && registrationOpen ? (
            <p>
              New learner?{" "}
              <Link to="/register" className="font-medium text-primary underline-offset-4 hover:underline">
                Create a learner account
              </Link>
            </p>
          ) : null}
          <p className="flex gap-2 text-muted-foreground">
            <Info className="mt-0.5 size-4 shrink-0" aria-hidden="true" />
            <span>
              {mode === "admin"
                ? "Administration accounts are created by an organisation administrator. There is no public sign-up for administration."
                : "Forgot your password? Ask your administrator for a password reset link."}
            </span>
          </p>
          {environment?.synthetic_data ?? true ? (
            <p className="rounded-md bg-demo-soft px-3 py-2 text-demo">
              <span className="font-semibold">Local demo:</span> synthetic accounts such as{" "}
              <code>{mode === "admin" ? "org-admin01@example.invalid" : "learner01@example.invalid"}</code> use the demo password from the
              project's <code>.env</code>.
            </p>
          ) : null}
        </div>
      </Card>

      <section aria-labelledby="product-pitch" className="space-y-8 lg:order-1">
        <div className="space-y-4">
          <p className="text-sm font-semibold uppercase tracking-wide text-primary">For officials in statistical roles</p>
          <h2 id="product-pitch" className="text-3xl font-semibold leading-tight tracking-tight text-balance sm:text-4xl">
            Know what your role needs. See where you stand. Learn what closes the gap.
          </h2>
          <p className="max-w-xl text-lg text-muted-foreground">
            {PRODUCT.name} turns job-role competency requirements and assessment evidence into a clear, personal learning plan.
          </p>
        </div>

        <ol className="grid gap-3 sm:grid-cols-2">
          <LoopStep n={1} icon={<UserCog />} title="Your role's requirements">Competencies and the level each one needs.</LoopStep>
          <LoopStep n={2} icon={<ClipboardCheck />} title="Baseline assessment">Scenario questions give evidence of where you stand.</LoopStep>
          <LoopStep n={3} icon={<Target />} title="Gap analysis">Priorities, explained in plain language.</LoopStep>
          <LoopStep n={4} icon={<BookOpen />} title="Recommended learning">Courses matched to your gaps, with the reason.</LoopStep>
        </ol>

        <ul className="flex flex-col gap-2 text-sm text-muted-foreground sm:flex-row sm:flex-wrap sm:gap-x-6">
          <li className="flex items-center gap-2"><ShieldCheck className="size-4 text-success" aria-hidden="true" />Scored by transparent rules, not AI</li>
          <li className="flex items-center gap-2"><ShieldCheck className="size-4 text-success" aria-hidden="true" />Development guidance, never an appraisal</li>
        </ul>
      </section>
    </div>
  );
}

function LoopStep({ n, icon, title, children }: { n: number; icon: ReactNode; title: string; children: ReactNode }) {
  return (
    <li className="flex gap-3 rounded-lg border border-border bg-card p-4">
      <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary-soft text-primary [&_svg]:size-4" aria-hidden="true">
        {icon}
      </span>
      <div>
        <p className="text-sm font-semibold"><span className="sr-only">Step {n}: </span>{title}</p>
        <p className="text-sm text-muted-foreground">{children}</p>
      </div>
    </li>
  );
}
