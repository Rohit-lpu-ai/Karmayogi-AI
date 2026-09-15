import { useRef, type ReactNode } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

/**
 * Confirmation for consequential actions (UI_UX_SPEC.md §8.8): summarises the effect, focus is trapped,
 * Esc or Cancel closes and focus returns to the trigger.
 */
export function ConfirmationDialog({
  open,
  onOpenChange,
  title,
  description,
  children,
  confirmLabel,
  cancelLabel = "Cancel",
  onConfirm,
  busy = false,
  busyLabel,
  tone = "primary",
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  title: string;
  description?: ReactNode;
  children?: ReactNode;
  confirmLabel: string;
  cancelLabel?: string;
  onConfirm: () => void;
  busy?: boolean;
  busyLabel?: string;
  tone?: "primary" | "danger";
}) {
  // The dialog is opened from state, not a Radix trigger, so remember what had focus and restore it on close.
  // Captured during the render that opens the dialog, before Radix moves focus inside it.
  const returnFocusTo = useRef<HTMLElement | null>(null);
  const wasOpen = useRef(false);
  if (open && !wasOpen.current && typeof document !== "undefined" && document.activeElement instanceof HTMLElement) {
    returnFocusTo.current = document.activeElement;
  }
  wasOpen.current = open;

  return (
    <Dialog open={open} onOpenChange={(next) => (busy ? undefined : onOpenChange(next))}>
      <DialogContent
        hideClose={busy}
        onCloseAutoFocus={(event) => {
          const target = returnFocusTo.current;
          if (target && document.contains(target)) {
            event.preventDefault();
            target.focus();
          }
        }}
      >
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description ? <DialogDescription>{description}</DialogDescription> : null}
        </DialogHeader>
        {children ? <div className="text-sm text-foreground">{children}</div> : null}
        <DialogFooter>
          <Button variant="secondary" onClick={() => onOpenChange(false)} disabled={busy}>
            {cancelLabel}
          </Button>
          <Button variant={tone === "danger" ? "danger" : "primary"} onClick={onConfirm} disabled={busy}>
            {busy ? (busyLabel ?? `${confirmLabel}...`) : confirmLabel}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
