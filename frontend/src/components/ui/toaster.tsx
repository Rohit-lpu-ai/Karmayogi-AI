import { Toaster as Sonner, toast } from "sonner";

/**
 * Toasts confirm actions; they are announced politely and never carry the only copy of important
 * information (UI_UX_SPEC.md §8.8). Keep an inline status as well.
 */
export function Toaster() {
  return (
    <Sonner
      position="top-right"
      offset="5rem" // below the sticky header, away from page actions at the bottom of forms
      closeButton
      toastOptions={{
        classNames: {
          toast: "!rounded-lg !border !border-border !bg-card !text-card-foreground !shadow-raised !font-sans",
          description: "!text-muted-foreground",
        },
      }}
    />
  );
}

export { toast };
