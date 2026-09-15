import { lazy, Suspense, type ReactNode } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";
import { AppShell } from "./components/layout/AppShell";
import { LoadingState } from "./components/States";
import { AssessmentPage } from "./pages/AssessmentPage";
import { DashboardPage } from "./pages/DashboardPage";
import { LoginPage } from "./pages/LoginPage";
import { OnboardingPage } from "./pages/OnboardingPage";
import { ResultPage } from "./pages/ResultPage";

/** Client-side routing only improves navigation; every endpoint enforces authentication itself. */
function RequireAuth({ children, onboarded = true }: { children: ReactNode; onboarded?: boolean }) {
  const { user, checking } = useAuth();
  const location = useLocation();
  if (checking) return <LoadingState label="Checking your session" />;
  if (!user) return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  const needsOnboarding = user.can_take_assessments && (user.notice.acknowledged_at === null || user.job_role === null);
  if (onboarded && needsOnboarding) return <Navigate to="/get-started" replace />;
  return <>{children}</>;
}

/** Screens not yet migrated to the design system keep their scoped legacy styles (DEC-050). */
function Legacy({ children }: { children: ReactNode }) {
  return <div className="legacy">{children}</div>;
}

// Component gallery for reviewing the design system; only in the Vite dev server, never in production builds.
const DesignSystemPage = import.meta.env.DEV ? lazy(() => import("./pages/dev/DesignSystemPage")) : null;

export function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/login" element={<Legacy><LoginPage /></Legacy>} />
        <Route path="/get-started" element={<RequireAuth onboarded={false}><Legacy><OnboardingPage /></Legacy></RequireAuth>} />
        <Route path="/" element={<RequireAuth><Legacy><DashboardPage /></Legacy></RequireAuth>} />
        <Route path="/assessment" element={<RequireAuth><Legacy><AssessmentPage /></Legacy></RequireAuth>} />
        <Route path="/attempts/:attemptId/result" element={<RequireAuth><Legacy><ResultPage /></Legacy></RequireAuth>} />
        {DesignSystemPage ? (
          <Route
            path="/dev/design-system"
            element={<RequireAuth onboarded={false}><Suspense fallback={<LoadingState label="Loading" />}><DesignSystemPage /></Suspense></RequireAuth>}
          />
        ) : null}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  );
}
