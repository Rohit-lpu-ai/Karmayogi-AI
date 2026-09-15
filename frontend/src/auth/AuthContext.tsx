import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { api, ApiError, setCsrfToken } from "../api/client";
import type { EnvironmentInfo, Me, SessionInfo } from "../api/types";

export interface RegisterInput {
  display_name: string;
  email: string;
  password: string;
  registration_id: string;
  department_id?: string;
}

interface AuthValue {
  user: Me | null;
  checking: boolean;
  /** Public environment flags; null until loaded or when the endpoint is unavailable. */
  environment: EnvironmentInfo | null;
  login: (email: string, password: string) => Promise<Me>;
  register: (input: RegisterInput) => Promise<Me>;
  logout: () => Promise<void>;
  setUser: (user: Me) => void;
}

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<Me | null>(null);
  const [checking, setChecking] = useState(true);
  const [environment, setEnvironment] = useState<EnvironmentInfo | null>(null);

  useEffect(() => {
    api<SessionInfo>("/api/v1/auth/session")
      .then((session) => {
        setCsrfToken(session.csrf_token);
        setUserState(session.user);
      })
      .catch((err: unknown) => {
        if (!(err instanceof ApiError && err.status === 401)) console.error("session check failed", err);
        setCsrfToken(null);
      })
      .finally(() => {
        setChecking(false);
        api<EnvironmentInfo>("/api/v1/environment")
          .then(setEnvironment)
          .catch(() => setEnvironment(null));
      });
  }, []);

  const startSession = useCallback((session: SessionInfo) => {
    setCsrfToken(session.csrf_token);
    setUserState(session.user);
    return session.user;
  }, []);

  const login = useCallback(
    async (email: string, password: string) =>
      startSession(await api<SessionInfo>("/api/v1/auth/login", { method: "POST", body: { email, password } })),
    [startSession],
  );

  const register = useCallback(
    async (input: RegisterInput) => startSession(await api<SessionInfo>("/api/v1/auth/register", { method: "POST", body: input })),
    [startSession],
  );

  const logout = useCallback(async () => {
    try {
      await api<void>("/api/v1/auth/logout", { method: "POST" });
    } finally {
      setCsrfToken(null);
      setUserState(null);
    }
  }, []);

  const value = useMemo(
    () => ({ user, checking, environment, login, register, logout, setUser: setUserState }),
    [user, checking, environment, login, register, logout],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthValue {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}

/** True when the account holds any administrative capability (navigation only; the server enforces access). */
export function isAdministrator(user: Me): boolean {
  return (user.admin_capabilities ?? []).length > 0;
}

export function can(user: Me, capability: string): boolean {
  return (user.admin_capabilities ?? []).includes(capability);
}

/** Where an account lands after signing in when no earlier page was requested. */
export function homeFor(user: Me): string {
  return isAdministrator(user) && !user.can_take_assessments ? "/admin" : "/";
}
