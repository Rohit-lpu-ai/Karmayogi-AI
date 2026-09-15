import {
  ArrowLeftRight,
  BookOpenCheck,
  ClipboardList,
  FileQuestion,
  Gavel,
  Grid3x3,
  TrendingUp,
  Network,
  ScrollText,
  ClipboardCheck,
  History,
  Route as RouteIcon,
  Gauge,
  LayoutDashboard,
  Library,
  ShieldCheck,
  Target,
  UserCircle,
  Users,
  type LucideIcon,
} from "lucide-react";
import type { Me } from "@/api/types";

export interface NavItem {
  label: string;
  to: string;
  icon: LucideIcon;
  /** Match only the exact path (for "/" and "/admin"). */
  end?: boolean;
  /** Hide when this returns false. Hiding is cosmetic; the server enforces access (UI_UX_SPEC.md §3.1). */
  visible?: (user: Me) => boolean;
}

export interface NavSection {
  label: string;
  items: NavItem[];
}

export type Area = "learning" | "admin";

const caps = (user: Me) => user.admin_capabilities ?? [];
const hasCap = (capability: string) => (user: Me) => caps(user).includes(capability);

/** Learning space. Only routes that exist are listed - no placeholder screens (IMPLEMENTATION_ROADMAP.md Phase 8). */
export const NAVIGATION: NavSection[] = [
  {
    label: "Learning",
    items: [
      { label: "Home", to: "/", icon: LayoutDashboard, end: true },
      { label: "My competencies", to: "/competencies", icon: Gauge, end: true, visible: (user) => user.can_take_assessments },
      { label: "Gap analysis", to: "/competencies/gaps", icon: Target, visible: (user) => user.can_take_assessments },
      { label: "Learning path", to: "/learning-path", icon: RouteIcon, visible: (user) => user.can_take_assessments },
      { label: "Courses", to: "/courses", icon: Library },
      { label: "Baseline assessment", to: "/assessment", icon: ClipboardCheck, visible: (user) => user.can_take_assessments },
      { label: "Assessment history", to: "/me/attempts", icon: History, visible: (user) => user.can_take_assessments },
    ],
  },
  {
    label: "Account",
    items: [{ label: "Profile", to: "/profile", icon: UserCircle }],
  },
  {
    label: "Switch",
    items: [{ label: "Administration", to: "/admin", icon: ArrowLeftRight, visible: (user) => caps(user).length > 0 }],
  },
];

/** Administration space (Phase 4A). Sections grow with 4C/4D; each item needs the capability its API checks. */
export const ADMIN_NAVIGATION: NavSection[] = [
  {
    label: "Administration",
    items: [
      { label: "Overview", to: "/admin", icon: LayoutDashboard, end: true },
      { label: "Users", to: "/admin/users", icon: Users, visible: hasCap("users.view") },
      { label: "Roles and permissions", to: "/admin/roles", icon: ShieldCheck, visible: hasCap("users.view") },
    ],
  },
  {
    label: "Content",
    items: [
      { label: "Review queue", to: "/admin/review", icon: Gavel, visible: (user) => hasCap("questions.review")(user) || hasCap("courses.review")(user) },
      { label: "Questions", to: "/admin/questions", icon: FileQuestion, visible: hasCap("questions.author") },
      { label: "Courses", to: "/admin/courses", icon: BookOpenCheck, visible: hasCap("courses.manage") },
      { label: "Assessments", to: "/admin/assessments", icon: ClipboardList, visible: hasCap("assessments.manage") },
      { label: "Competencies", to: "/admin/competencies", icon: Network, visible: hasCap("frameworks.view") },
    ],
  },
  {
    label: "Insight",
    items: [
      { label: "Skill gaps", to: "/admin/skill-gaps", icon: Grid3x3, visible: hasCap("insight.view") },
      { label: "Training needs", to: "/admin/training-needs", icon: TrendingUp, visible: hasCap("insight.view") },
    ],
  },
  {
    label: "Governance",
    items: [{ label: "Audit trail", to: "/admin/audit", icon: ScrollText, visible: hasCap("audit.view") }],
  },
  {
    label: "Account",
    items: [{ label: "Profile", to: "/profile", icon: UserCircle }],
  },
  {
    label: "Switch",
    items: [{ label: "My learning", to: "/", icon: ArrowLeftRight, visible: (user) => user.can_take_assessments }],
  },
];

export function areaFor(pathname: string): Area {
  return pathname === "/admin" || pathname.startsWith("/admin/") ? "admin" : "learning";
}

export function visibleNavigation(user: Me, area: Area = "learning"): NavSection[] {
  return (area === "admin" ? ADMIN_NAVIGATION : NAVIGATION)
    .map((section) => ({ ...section, items: section.items.filter((item) => (item.visible ? item.visible(user) : true)) }))
    .filter((section) => section.items.length > 0);
}
