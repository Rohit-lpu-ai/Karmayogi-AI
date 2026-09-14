import { useState, type FormEvent } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { ApiError } from "../api/client";
import { useAuth } from "../auth/AuthContext";
import { ErrorState } from "../components/States";

export function LoginPage() {
  const { user, login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<ApiError | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (user) return <Navigate to="/" replace />;

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await login(email.trim(), password);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err instanceof ApiError ? err : new ApiError(0, "UNKNOWN", "Sign-in failed"));
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <section className="card narrow" aria-labelledby="login-title">
      <h1 id="login-title">Sign in</h1>
      <p className="muted">Accounts are created by administrators. In this local demo, use a synthetic account such as learner01@example.invalid.</p>
      {error ? <ErrorState error={error} /> : null}
      <form onSubmit={handleSubmit} noValidate>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" autoComplete="username" required value={email} onChange={(e) => setEmail(e.target.value)} />
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="button" disabled={submitting || !email || !password}>
          {submitting ? "Signing in..." : "Sign in"}
        </button>
      </form>
      <p className="muted small">Forgot your password? Contact your administrator.</p>
    </section>
  );
}
