import type { ReactNode } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export function AppShell({ children }: { children: ReactNode }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  async function handleSignOut() {
    await logout();
    navigate("/login", { replace: true });
  }

  return (
    <>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      {!user || user.is_synthetic ? (
        <div className="demo-banner" role="note">
          DEMO environment - synthetic users and synthetic content for local testing. Nothing shown here is official data,
          and results are development guidance only, not an appraisal.
        </div>
      ) : null}
      <header className="app-header">
        <span className="app-name">Competency Learning Platform <span className="muted">(working name)</span></span>
        {user ? (
          <nav aria-label="Main">
            <NavLink to="/" end>
              Dashboard
            </NavLink>
            {user.can_take_assessments ? <NavLink to="/assessment">Assessment</NavLink> : null}
            <span className="muted user-name">{user.display_name}</span>
            <button type="button" className="button button-secondary" onClick={handleSignOut}>
              Sign out
            </button>
          </nav>
        ) : null}
      </header>
      <main id="main" className="app-main">
        {children}
      </main>
    </>
  );
}
