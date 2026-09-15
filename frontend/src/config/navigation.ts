import { ClipboardCheck, LayoutDashboard, type LucideIcon } from "lucide-react";
import type { Me } from "@/api/types";

export interface NavItem {
  label: string;
  to: string;
  icon: LucideIcon;
  /** Match only the exact path (for "/"). */
  end?: boolean;
  /** Hide when this returns false. Hiding is cosmetic; the server enforces access (UI_UX_SPEC.md §3.1). */
  visible?: (user: Me) => boolean;
}

export interface NavSection {
  label: string;
  items: NavItem[];
}

/**
 * Primary navigation. Only routes that exist are listed - no placeholder screens (IMPLEMENTATION_ROADMAP.md Phase 8).
 * Add competencies, courses and progress here when their screens ship.
 */
export const NAVIGATION: NavSection[] = [
  {
    label: "Learning",
    items: [
      { label: "Home", to: "/", icon: LayoutDashboard, end: true },
      { label: "Baseline assessment", to: "/assessment", icon: ClipboardCheck, visible: (user) => user.can_take_assessments },
    ],
  },
];

export function visibleNavigation(user: Me): NavSection[] {
  return NAVIGATION.map((section) => ({
    ...section,
    items: section.items.filter((item) => (item.visible ? item.visible(user) : true)),
  })).filter((section) => section.items.length > 0);
}
