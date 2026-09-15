import { BookOpenCheck, BriefcaseBusiness, ChevronDown, LogOut, Menu, UserCircle, UserCog } from "lucide-react";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { Link, NavLink, useLocation, useNavigate } from "react-router-dom";
import type { Me } from "@/api/types";
import { useAuth } from "@/auth/AuthContext";
import { DemoDataNotice } from "@/components/product/DemoDataNotice";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogDescription, DialogTitle, DialogTrigger, SheetContent } from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Toaster } from "@/components/ui/toaster";
import { areaFor, visibleNavigation, type Area } from "@/config/navigation";
import { PRODUCT } from "@/config/product";
import { cn } from "@/lib/utils";

/**
 * Application frame (UI_UX_SPEC.md §3-4): skip link, persistent left navigation on desktop, drawer on smaller
 * screens, top bar with the user menu, the DEMO notice and one <main> landmark.
 */
export function AppShell({ children }: { children: ReactNode }) {
  const { user, checking, environment } = useAuth();
  // One environment-level banner (K-2). Falls back to the account flag when the environment endpoint is unavailable.
  const showDemoNotice = environment ? environment.synthetic_data : !user || user.is_synthetic;
  useFocusMainOnNavigation();

  if (checking) {
    // Neutral frame while the session is checked, so the signed-out layout never flashes before the signed-in one.
    return (
      <div className="flex min-h-screen items-center justify-center p-6">
        <div className="flex flex-col items-center gap-3 text-muted-foreground">
          <span className="flex size-10 items-center justify-center rounded-lg bg-primary text-primary-foreground" aria-hidden="true">
            <BookOpenCheck className="size-5" />
          </span>
          <p role="status" aria-live="polite" className="text-sm">
            Checking your session...
          </p>
        </div>
      </div>
    );
  }

  return (
    <>
      <a
        href="#main"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[60] focus:rounded-md focus:bg-card focus:px-4 focus:py-2 focus:shadow-raised"
      >
        Skip to content
      </a>
      {user ? (
        <SignedInLayout user={user} showDemoNotice={showDemoNotice}>
          {children}
        </SignedInLayout>
      ) : (
        <SignedOutLayout showDemoNotice={showDemoNotice}>{children}</SignedOutLayout>
      )}
      <Toaster />
    </>
  );
}

/** Move focus to <main> after client-side navigation so screen-reader and keyboard users start at the new page. */
function useFocusMainOnNavigation() {
  const { pathname } = useLocation();
  const first = useRef(true);
  useEffect(() => {
    if (first.current) {
      first.current = false;
      return;
    }
    document.getElementById("main")?.focus({ preventScroll: false });
  }, [pathname]);
}

function BrandMark({ compact = false }: { compact?: boolean }) {
  return (
    <Link
      to="/"
      aria-label={`${PRODUCT.name} (${PRODUCT.nameStatus.toLowerCase()}) - home`}
      className="flex items-center gap-2.5 rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
      data-focus-ring=""
    >
      <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary text-primary-foreground" aria-hidden="true">
        <BookOpenCheck className="size-5" />
      </span>
      <span className="flex min-w-0 flex-col leading-tight">
        <span className={cn("font-semibold text-foreground text-balance", compact ? "text-sm" : "text-[15px]")}>
          {compact ? PRODUCT.shortName : PRODUCT.name}
        </span>
        <span className={cn("text-xs text-muted-foreground", compact && "hidden sm:block")}>{PRODUCT.nameStatus}</span>
      </span>
    </Link>
  );
}

function SidebarNav({ user, area, onNavigate }: { user: Me; area: Area; onNavigate?: () => void }) {
  return (
    <nav aria-label={area === "admin" ? "Administration" : "Main"} className="flex flex-col gap-6">
      {area === "admin" ? (
        <p className="flex items-center gap-2 rounded-md bg-muted px-3 py-2 text-sm font-semibold text-foreground">
          <UserCog className="size-4 text-primary" aria-hidden="true" />
          Administration
        </p>
      ) : null}
      {visibleNavigation(user, area).map((section) => (
        <div key={section.label} className="flex flex-col gap-1">
          <p className="px-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">{section.label}</p>
          <ul className="flex flex-col gap-0.5">
            {section.items.map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  end={item.end}
                  onClick={onNavigate}
                  data-focus-ring=""
                  className={({ isActive }) =>
                    cn(
                      "flex min-h-11 items-center gap-3 rounded-md px-3 text-sm font-medium transition-colors",
                      "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                      isActive
                        ? "bg-primary-soft text-primary-soft-foreground"
                        : "text-muted-foreground hover:bg-muted hover:text-foreground",
                    )
                  }
                >
                  <item.icon className="size-[18px] shrink-0" aria-hidden="true" />
                  {item.label}
                </NavLink>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </nav>
  );
}

function SidebarFooter() {
  return (
    <p className="text-xs leading-relaxed text-muted-foreground">
      Development guidance only. Not an official government service and not connected to any government system.
    </p>
  );
}

function SignedInLayout({ user, showDemoNotice, children }: { user: Me; showDemoNotice: boolean; children: ReactNode }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const { pathname } = useLocation();
  const area = areaFor(pathname);
  useEffect(() => setMenuOpen(false), [pathname]);

  return (
    <div className="min-h-screen lg:grid lg:grid-cols-[var(--sidebar-width)_minmax(0,1fr)] lg:bg-[linear-gradient(to_right,var(--card)_calc(var(--sidebar-width)-1px),var(--border)_calc(var(--sidebar-width)-1px),var(--border)_var(--sidebar-width),transparent_var(--sidebar-width))]">
      <aside className="hidden border-r border-border bg-card lg:sticky lg:top-0 lg:flex lg:h-screen lg:flex-col lg:gap-8 lg:px-4 lg:py-5">
        <div className="px-1">
          <BrandMark />
        </div>
        <div className="flex-1 overflow-y-auto">
          <SidebarNav user={user} area={area} />
        </div>
        <div className="px-1">
          <SidebarFooter />
        </div>
      </aside>

      <div className="flex min-w-0 flex-col">
        {showDemoNotice ? <DemoDataNotice /> : null}
        <header className="sticky top-0 z-30 border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/85">
          <div className="flex h-16 items-center gap-3 px-4 sm:px-6 lg:px-8">
            <Dialog open={menuOpen} onOpenChange={setMenuOpen}>
              <DialogTrigger asChild>
                <Button variant="ghost" size="icon" className="lg:hidden" aria-label="Open menu">
                  <Menu className="size-5" aria-hidden="true" />
                </Button>
              </DialogTrigger>
              <SheetContent aria-describedby="mobile-nav-description">
                <div className="flex flex-col gap-6 overflow-y-auto px-4 pb-5 pt-5">
                  <DialogTitle className="sr-only">Menu</DialogTitle>
                  <DialogDescription id="mobile-nav-description" className="sr-only">
                    Main navigation
                  </DialogDescription>
                  <div className="pr-10">
                    <BrandMark compact />
                  </div>
                  <SidebarNav user={user} area={area} onNavigate={() => setMenuOpen(false)} />
                  <SidebarFooter />
                </div>
              </SheetContent>
            </Dialog>
            <div className="min-w-0 lg:hidden">
              <BrandMark compact />
            </div>
            {area === "admin" ? (
              <Badge tone="primary" className="hidden sm:inline-flex">
                Administration
              </Badge>
            ) : null}
            <div className="flex-1" />
            {area === "learning" && user.job_role ? (
              <Link
                to="/get-started"
                className="hidden max-w-xs items-center gap-2 rounded-md px-2 py-1 text-sm text-muted-foreground hover:bg-muted hover:text-foreground md:flex"
                aria-label={`Job role: ${user.job_role.name}${user.job_role.is_demo ? " (demo)" : ""}. Change job role`}
                title="Your job role - select to change"
              >
                <BriefcaseBusiness className="size-4 shrink-0" aria-hidden="true" />
                <span className="truncate">{user.job_role.name.replace(/^DEMO - /, "").replace(/\s*\(synthetic[^)]*\)$/, "")}</span>
              </Link>
            ) : null}
            <UserMenu user={user} />
          </div>
        </header>
        <main id="main" tabIndex={-1} className="mx-auto w-full max-w-[var(--content-max)] flex-1 px-4 py-6 focus:outline-none sm:px-6 lg:px-8 lg:py-8">
          {children}
        </main>
      </div>
    </div>
  );
}

function initials(name: string): string {
  const parts = name.replace(/\([^)]*\)/g, " ").split(/\s+/).map((part) => part.replace(/[^\p{L}\p{N}]/gu, "")).filter(Boolean);
  return ((parts[0]?.[0] ?? "") + (parts.length > 1 ? (parts[parts.length - 1]?.[0] ?? "") : "")).toUpperCase() || "?";
}

function UserMenu({ user }: { user: Me }) {
  const { logout } = useAuth();
  const navigate = useNavigate();

  async function handleSignOut() {
    // Leave protected pages first, so no route guard records this page as "return here" for the next person.
    navigate("/login", { replace: true, state: null });
    await logout();
  }

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="h-11 gap-2 px-2" aria-label={`Account menu for ${user.display_name}`}>
          <span className="flex size-8 items-center justify-center rounded-full bg-primary-soft text-xs font-semibold text-primary-soft-foreground" aria-hidden="true">
            {initials(user.display_name)}
          </span>
          <span className="hidden max-w-40 truncate text-sm font-medium sm:inline">{user.display_name}</span>
          <ChevronDown className="size-4 text-muted-foreground" aria-hidden="true" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuLabel>
          <span className="block font-semibold">{user.display_name}</span>
          <span className="block truncate text-xs font-normal text-muted-foreground">{user.email}</span>
          {user.is_synthetic ? (
            <Badge tone="demo" className="mt-1.5">
              Synthetic demo account
            </Badge>
          ) : null}
        </DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onSelect={() => navigate("/profile")}>
          <UserCircle aria-hidden="true" />
          Profile
        </DropdownMenuItem>
        {user.can_take_assessments ? (
          <DropdownMenuItem onSelect={() => navigate("/get-started")}>
            <BriefcaseBusiness aria-hidden="true" />
            {user.job_role ? "Change job role" : "Choose job role"}
          </DropdownMenuItem>
        ) : null}
        <DropdownMenuSeparator />
        <DropdownMenuItem onSelect={() => void handleSignOut()}>
          <LogOut aria-hidden="true" />
          Sign out
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

function SignedOutLayout({ showDemoNotice, children }: { showDemoNotice: boolean; children: ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col">
      {showDemoNotice ? <DemoDataNotice /> : null}
      <header className="border-b border-border bg-card">
        <div className="mx-auto flex h-16 max-w-[var(--content-max)] items-center px-4 sm:px-6">
          <BrandMark />
        </div>
      </header>
      <main id="main" tabIndex={-1} className="flex flex-1 items-center px-4 py-8 focus:outline-none sm:px-6 sm:py-12">
        {children}
      </main>
      <footer className="border-t border-border bg-card">
        <p className="mx-auto max-w-[var(--content-max)] px-4 py-4 text-xs text-muted-foreground sm:px-6">
          {PRODUCT.name} ({PRODUCT.nameStatus.toLowerCase()}). Not an official government service.
        </p>
      </footer>
    </div>
  );
}
