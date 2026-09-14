import type { ReactNode } from "react";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { useAuth } from "./auth/AuthContext";
import { AppShell } from "./components/AppShell";
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

export function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/get-started" element={<RequireAuth onboarded={false}><OnboardingPage /></RequireAuth>} />
        <Route path="/" element={<RequireAuth><DashboardPage /></RequireAuth>} />
        <Route path="/assessment" element={<RequireAuth><AssessmentPage /></RequireAuth>} />
        <Route path="/attempts/:attemptId/result" element={<RequireAuth><ResultPage /></RequireAuth>} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AppShell>
  );
}
