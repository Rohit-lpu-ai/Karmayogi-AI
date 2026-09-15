import { lazy, Suspense, type ReactNode } from "react";
import { Link, Navigate, Route, Routes, useLocation } from "react-router-dom";
import { can, isAdministrator, useAuth } from "./auth/AuthContext";
import { AppShell } from "./components/layout/AppShell";
import { EmptyState, LoadingState } from "./components/States";
import { Button } from "./components/ui/button";
import { ProfilePage } from "./pages/account/ProfilePage";
import { RegisterPage } from "./pages/account/RegisterPage";
import { SetPasswordPage } from "./pages/account/SetPasswordPage";
import { AssessmentIntroPage } from "./pages/assessment/AssessmentIntroPage";
import { AttemptPage } from "./pages/assessment/AttemptPage";
import { CompetencyProfilePage } from "./pages/competencies/CompetencyProfilePage";
import { GapsPage } from "./pages/competencies/GapsPage";
import { CataloguePage } from "./pages/courses/CataloguePage";
import { CourseDetailPage } from "./pages/courses/CourseDetailPage";
import { DashboardPage } from "./pages/DashboardPage";
import { LoginPage } from "./pages/LoginPage";
import { OnboardingPage } from "./pages/OnboardingPage";
import { ResultPage } from "./pages/results/ResultPage";

// Route-level code splitting: administration and the learning player load on demand.
const content = () => import("./pages/admin/content/QuestionPages");
const AdminQuestionsPage = lazy(() => content().then((m) => ({ default: m.AdminQuestionsPage })));
const AdminQuestionNewPage = lazy(() => content().then((m) => ({ default: m.AdminQuestionNewPage })));
const AdminQuestionDetailPage = lazy(() => content().then((m) => ({ default: m.AdminQuestionDetailPage })));
const courseAdmin = () => import("./pages/admin/content/CoursePages");
const AdminCoursesPage = lazy(() => courseAdmin().then((m) => ({ default: m.AdminCoursesPage })));
const AdminCourseNewPage = lazy(() => courseAdmin().then((m) => ({ default: m.AdminCourseNewPage })));
const AdminCourseDetailPage = lazy(() => courseAdmin().then((m) => ({ default: m.AdminCourseDetailPage })));
const governance = () => import("./pages/admin/content/GovernancePages");
const AdminCompetenciesPage = lazy(() => governance().then((m) => ({ default: m.AdminCompetenciesPage })));
const AdminAssessmentsPage = lazy(() => governance().then((m) => ({ default: m.AdminAssessmentsPage })));
const AdminAuditPage = lazy(() => governance().then((m) => ({ default: m.AdminAuditPage })));
const insight = () => import("./pages/admin/InsightPages");
const SkillGapsPage = lazy(() => insight().then((m) => ({ default: m.SkillGapsPage })));
const TrainingNeedsPage = lazy(() => insight().then((m) => ({ default: m.TrainingNeedsPage })));
const ReviewQueuePage = lazy(() => import("./pages/admin/content/ReviewQueuePage").then((m) => ({ default: m.ReviewQueuePage })));
const AdminOverviewPage = lazy(() => import("./pages/admin/AdminOverviewPage").then((m) => ({ default: m.AdminOverviewPage })));
const AdminRolesPage = lazy(() => import("./pages/admin/AdminRolesPage").then((m) => ({ default: m.AdminRolesPage })));
const AdminUsersPage = lazy(() => import("./pages/admin/AdminUsersPage").then((m) => ({ default: m.AdminUsersPage })));
const AttemptsPage = lazy(() => import("./pages/learning/AttemptsPage").then((m) => ({ default: m.AttemptsPage })));
const CourseLearnPage = lazy(() => import("./pages/learning/CourseLearnPage").then((m) => ({ default: m.CourseLearnPage })));
const LearningPathPage = lazy(() => import("./pages/learning/LearningPathPage").then((m) => ({ default: m.LearningPathPage })));
const LessonPage = lazy(() => import("./pages/learning/LessonPage").then((m) => ({ default: m.LessonPage })));

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

/**
 * Administration routes need an administrative capability. Learners who open an admin URL see a plain explanation,
 * never admin data: the admin APIs return 403 for them regardless of what the page does.
 */
function RequireAdmin({ children, capability }: { children: ReactNode; capability?: string | string[] }) {
  const { user, checking } = useAuth();
  const location = useLocation();
  if (checking) return <LoadingState label="Checking your session" />;
  if (!user) return <Navigate to="/login?as=admin" replace state={{ from: location.pathname + location.search }} />;
  const needed = capability === undefined ? [] : Array.isArray(capability) ? capability : [capability];
  if (!isAdministrator(user) || (needed.length > 0 && !needed.some((cap) => can(user, cap)))) {
    return (
      <div className="mx-auto max-w-xl py-8">
        <h1 className="mb-4 text-2xl font-semibold tracking-tight">No access to this page</h1>
        <EmptyState
          title="Your account does not include this administration permission."
          action={
            <Button asChild variant="secondary">
              <Link to={isAdministrator(user) ? "/admin" : "/"}>{isAdministrator(user) ? "Go to administration" : "Go to your learning"}</Link>
            </Button>
          }
        >
          If you need it, ask your organisation administrator.
        </EmptyState>
      </div>
    );
  }
  return <>{children}</>;
}

/** Accounts without a learning space (auditor, platform administrator) start in administration. */
function HomeRoute() {
  const { user } = useAuth();
  if (user && !user.can_take_assessments && isAdministrator(user)) return <Navigate to="/admin" replace />;
  return <DashboardPage />;
}

// Component gallery for reviewing the design system; only in the Vite dev server, never in production builds.
const DesignSystemPage = import.meta.env.DEV ? lazy(() => import("./pages/dev/DesignSystemPage")) : null;

export function App() {
  return (
    <AppShell>
      <Suspense fallback={<LoadingState label="Loading page" lines={4} />}>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/set-password" element={<SetPasswordPage />} />
        <Route path="/profile" element={<RequireAuth onboarded={false}><ProfilePage /></RequireAuth>} />
        <Route path="/admin" element={<RequireAdmin><AdminOverviewPage /></RequireAdmin>} />
        <Route path="/admin/users" element={<RequireAdmin capability="users.view"><AdminUsersPage /></RequireAdmin>} />
        <Route path="/admin/roles" element={<RequireAdmin capability="users.view"><AdminRolesPage /></RequireAdmin>} />
        <Route path="/admin/review" element={<RequireAdmin capability={["questions.review", "courses.review"]}><ReviewQueuePage /></RequireAdmin>} />
        <Route path="/admin/questions" element={<RequireAdmin capability="questions.author"><AdminQuestionsPage /></RequireAdmin>} />
        <Route path="/admin/questions/new" element={<RequireAdmin capability="questions.author"><AdminQuestionNewPage /></RequireAdmin>} />
        <Route path="/admin/questions/:questionId" element={<RequireAdmin capability={["questions.author", "questions.review"]}><AdminQuestionDetailPage /></RequireAdmin>} />
        <Route path="/admin/courses" element={<RequireAdmin capability="courses.manage"><AdminCoursesPage /></RequireAdmin>} />
        <Route path="/admin/courses/new" element={<RequireAdmin capability="courses.manage"><AdminCourseNewPage /></RequireAdmin>} />
        <Route path="/admin/courses/:courseId" element={<RequireAdmin capability={["courses.manage", "courses.review"]}><AdminCourseDetailPage /></RequireAdmin>} />
        <Route path="/admin/competencies" element={<RequireAdmin capability="frameworks.view"><AdminCompetenciesPage /></RequireAdmin>} />
        <Route path="/admin/assessments" element={<RequireAdmin capability="assessments.manage"><AdminAssessmentsPage /></RequireAdmin>} />
        <Route path="/admin/audit" element={<RequireAdmin capability="audit.view"><AdminAuditPage /></RequireAdmin>} />
        <Route path="/admin/skill-gaps" element={<RequireAdmin capability="insight.view"><SkillGapsPage /></RequireAdmin>} />
        <Route path="/admin/training-needs" element={<RequireAdmin capability="insight.view"><TrainingNeedsPage /></RequireAdmin>} />
        <Route path="/get-started" element={<RequireAuth onboarded={false}><OnboardingPage /></RequireAuth>} />
        <Route path="/" element={<RequireAuth><HomeRoute /></RequireAuth>} />
        <Route path="/competencies" element={<RequireAuth><CompetencyProfilePage /></RequireAuth>} />
        <Route path="/competencies/gaps" element={<RequireAuth><GapsPage /></RequireAuth>} />
        <Route path="/courses" element={<RequireAuth><CataloguePage /></RequireAuth>} />
        <Route path="/courses/:courseId" element={<RequireAuth><CourseDetailPage /></RequireAuth>} />
        <Route path="/courses/:courseId/learn" element={<RequireAuth><CourseLearnPage /></RequireAuth>} />
        <Route path="/courses/:courseId/lessons/:lessonId" element={<RequireAuth><LessonPage /></RequireAuth>} />
        <Route path="/learning-path" element={<RequireAuth><LearningPathPage /></RequireAuth>} />
        <Route path="/me/attempts" element={<RequireAuth><AttemptsPage /></RequireAuth>} />
        <Route path="/assessment" element={<RequireAuth><AssessmentIntroPage /></RequireAuth>} />
        <Route path="/assessment/attempts/:attemptId" element={<RequireAuth><AttemptPage /></RequireAuth>} />
        <Route path="/attempts/:attemptId/result" element={<RequireAuth><ResultPage /></RequireAuth>} />
        {DesignSystemPage ? (
          <Route
            path="/dev/design-system"
            element={<RequireAuth onboarded={false}><Suspense fallback={<LoadingState label="Loading" />}><DesignSystemPage /></Suspense></RequireAuth>}
          />
        ) : null}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      </Suspense>
    </AppShell>
  );
}
