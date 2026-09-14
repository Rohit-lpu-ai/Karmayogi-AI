import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from "react";
import { api, ApiError, setCsrfToken } from "../api/client";
import type { Me, SessionInfo } from "../api/types";

interface AuthValue {
  user: Me | null;
  checking: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  setUser: (user: Me) => void;
}

const AuthContext = createContext<AuthValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUserState] = useState<Me | null>(null);
  const [checking, setChecking] = useState(true);

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
      .finally(() => setChecking(false));
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const session = await api<SessionInfo>("/api/v1/auth/login", { method: "POST", body: { email, password } });
    setCsrfToken(session.csrf_token);
    setUserState(session.user);
  }, []);

  const logout = useCallback(async () => {
    try {
      await api<void>("/api/v1/auth/logout", { method: "POST" });
    } finally {
      setCsrfToken(null);
      setUserState(null);
    }
  }, []);

  const value = useMemo(() => ({ user, checking, login, logout, setUser: setUserState }), [user, checking, login, logout]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthValue {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}
