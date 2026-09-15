import { Loader2 } from "lucide-react";
import { useEffect, useRef, useState, type FormEvent } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { api, ApiError } from "@/api/client";
import { useAuth } from "@/auth/AuthContext";
import { ErrorSummary, PASSWORD_MIN_LENGTH, PasswordInput, describedBy, type FieldErrors } from "@/components/product/forms";
import { Alert } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Field } from "@/components/ui/form";

/**
 * Set a password from an administrator-issued one-time link (SECURITY_RESPONSIBLE_AI.md §3).
 * The token travels in the URL fragment (#token=...), which browsers never send to the server or proxies, and is
 * removed from the address bar as soon as the page reads it.
 */
export function SetPasswordPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { hash } = useLocation();
  const [token] = useState(() => new URLSearchParams(hash.replace(/^#/, "")).get("token") ?? "");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [errors, setErrors] = useState<FieldErrors>({});
  const [problem, setProblem] = useState<{ title: string; body?: string; reference?: string } | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const summaryRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (hash) window.history.replaceState(window.history.state, "", window.location.pathname);
  }, [hash]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    const found: FieldErrors = {};
    if (password.length < PASSWORD_MIN_LENGTH) found.password = `Use at least ${PASSWORD_MIN_LENGTH} characters.`;
    if (confirm !== password) found.confirm = "The passwords do not match.";
    setErrors(found);
    setProblem(null);
    if (Object.keys(found).length) {
      window.setTimeout(() => summaryRef.current?.focus(), 0);
      return;
    }
    setSubmitting(true);
    try {
      await api<void>("/api/v1/auth/password/set", { method: "POST", body: { token, new_password: password } });
      if (user) await logout(); // every session was revoked by the server
      navigate("/login", { replace: true, state: { notice: "Your password is set. Sign in with your new password." } });
    } catch (err) {
      const apiError = err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Failed");
      setProblem(
        apiError.code === "TOKEN_INVALID"
          ? { title: "This link cannot be used.", body: "It is invalid, already used or expired. Ask your administrator for a new link." }
          : { title: "Your password was not set.", body: apiError.detail ?? "Try again in a moment.", reference: apiError.correlationId },
      );
      setSubmitting(false);
      window.setTimeout(() => summaryRef.current?.focus(), 0);
    }
  }

  return (
    <Card as="section" aria-labelledby="set-password-title" className="mx-auto w-full max-w-md p-6 shadow-raised sm:p-8">
      <div className="space-y-1.5">
        <h1 id="set-password-title" className="text-2xl font-semibold tracking-tight">Set your password</h1>
        <p className="text-muted-foreground">Choose a password for your account. The link works once.</p>
      </div>
      {!token ? (
        <Alert tone="warning" title="This link is incomplete" className="mt-6">
          Open the full link your administrator gave you, or ask them for a new one. <Link to="/login">Go to sign in</Link>
        </Alert>
      ) : (
        <>
          <div className="mt-6 empty:hidden">
            <ErrorSummary ref={summaryRef} errors={errors} labels={{ password: "New password", confirm: "Confirm password" }} problem={problem} />
          </div>
          <form onSubmit={handleSubmit} noValidate className="mt-6 space-y-5">
            <Field id="password" label="New password" hint={`At least ${PASSWORD_MIN_LENGTH} characters.`} error={errors.password}>
              <PasswordInput
                id="password"
                autoComplete="new-password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={submitting}
                aria-invalid={errors.password ? true : undefined}
                aria-describedby={describedBy("password", errors.password, true)}
              />
            </Field>
            <Field id="confirm" label="Confirm password" error={errors.confirm}>
              <PasswordInput
                id="confirm"
                autoComplete="new-password"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                disabled={submitting}
                aria-invalid={errors.confirm ? true : undefined}
                aria-describedby={describedBy("confirm", errors.confirm)}
              />
            </Field>
            <Button type="submit" size="lg" className="w-full" disabled={submitting}>
              {submitting ? <Loader2 className="animate-spin" aria-hidden="true" /> : null}
              {submitting ? "Saving..." : "Set password"}
            </Button>
          </form>
        </>
      )}
    </Card>
  );
}
