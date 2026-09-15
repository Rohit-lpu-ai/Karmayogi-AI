import { BookOpen, ClipboardCheck, Target } from "lucide-react";
import { useState } from "react";
import { ApiError } from "@/api/client";
import { PageHeader } from "@/components/layout/PageHeader";
import { ConfirmationDialog } from "@/components/product/ConfirmationDialog";
import { StatCard } from "@/components/product/StatCard";
import { DemoBadge, EmptyState, ErrorState, EvidenceBadge, LoadingState, StatusBadge } from "@/components/States";
import { Alert } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Disclosure } from "@/components/ui/collapsible";
import { Field, Input } from "@/components/ui/form";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { toast } from "@/components/ui/toaster";

/**
 * Component gallery for design review. Registered only in the Vite dev server (import.meta.env.DEV).
 * Uses static sample text, no API calls; nothing here is product data.
 */
export default function DesignSystemPage() {
  const [confirmOpen, setConfirmOpen] = useState(false);
  const sampleError = new ApiError(503, "BACKEND_UNAVAILABLE", "Service unavailable",
    "The platform service is not running. Start it with start-dev.bat, then try again.", "3f2a9c0e1b7d4e55");

  return (
    <div className="space-y-10">
      <PageHeader
        breadcrumbs={[{ label: "Home", to: "/" }, { label: "Design system" }]}
        eyebrow="Development only"
        title="Design system"
        description="Tokens and components used across the platform. This page exists only in the local development server."
        meta={<Badge tone="neutral">DEC-050</Badge>}
        actions={<Button onClick={() => toast.success("Saved", { description: "Toasts confirm actions; the page also shows the status inline." })}>Show toast</Button>}
      />

      <Section title="Colour roles" description="Text colours meet 4.5:1 on their backgrounds; borders of form controls meet 3:1.">
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-6">
          {[
            ["primary", "bg-primary text-primary-foreground"],
            ["primary-soft", "bg-primary-soft text-primary-soft-foreground"],
            ["muted", "bg-muted text-muted-foreground"],
            ["success", "bg-success-soft text-success"],
            ["warning", "bg-warning-soft text-warning"],
            ["danger", "bg-danger-soft text-danger"],
            ["info", "bg-info-soft text-info"],
            ["demo", "bg-demo-soft text-demo"],
            ["ai", "bg-ai-soft text-ai"],
            ["card", "bg-card text-card-foreground border border-border"],
          ].map(([name, classes]) => (
            <div key={name} className={`flex h-20 items-end rounded-lg p-3 text-sm font-medium ${classes}`}>
              {name}
            </div>
          ))}
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-2 text-sm">
          <span className="text-muted-foreground">Level scale (always shown with text):</span>
          {["bg-level-1", "bg-level-2", "bg-level-3", "bg-level-4", "bg-level-5"].map((swatch, index) => (
            <span key={swatch} className="flex items-center gap-1.5">
              <span className={`inline-block size-4 rounded-sm ${swatch}`} aria-hidden="true" />
              Level {index + 1}
            </span>
          ))}
        </div>
      </Section>

      <Section title="Typography" description="System font stack with Devanagari fallback; scale 12 / 14 / 16 / 18 / 20 / 24 / 30 px.">
        <div className="space-y-2">
          <p className="text-3xl font-semibold tracking-tight">Page title - 30 px</p>
          <p className="text-2xl font-semibold">Section title - 24 px</p>
          <p className="text-xl font-semibold">Card title - 20 px</p>
          <p className="text-lg">Lead text - 18 px</p>
          <p className="text-base">Body text - 16 px with 1.5 line height for comfortable reading.</p>
          <p className="text-sm text-muted-foreground">Supporting text - 14 px</p>
          <p className="text-xs text-muted-foreground">Caption - 12 px</p>
          <p className="text-2xl font-semibold tabular-nums">64 / 100 · 1,280</p>
        </div>
      </Section>

      <Section title="Buttons" description="One primary action per view. Minimum height 44 px.">
        <div className="flex flex-wrap items-center gap-3">
          <Button>Primary</Button>
          <Button variant="secondary">Secondary</Button>
          <Button variant="soft">Soft</Button>
          <Button variant="ghost">Ghost</Button>
          <Button variant="link">Link</Button>
          <Button variant="danger">Destructive</Button>
          <Button disabled>Disabled</Button>
          <Button size="sm" variant="secondary">
            Small
          </Button>
        </div>
      </Section>

      <Section title="Badges" description="Status is always written out; colour supports the text.">
        <div className="flex flex-wrap items-center gap-2">
          <DemoBadge />
          <StatusBadge tone="success">Meets requirement</StatusBadge>
          <StatusBadge tone="warning">Provisional</StatusBadge>
          <StatusBadge tone="info">Baseline</StatusBadge>
          <StatusBadge tone="neutral">Not started</StatusBadge>
          <StatusBadge tone="primary">In progress</StatusBadge>
          <EvidenceBadge band="insufficient" count={2} />
          <EvidenceBadge band="medium" count={5} />
          <EvidenceBadge band="high" count={12} />
          <EvidenceBadge band={null} />
          <Badge tone="ai">AI-generated (future)</Badge>
        </div>
      </Section>

      <Section title="Alerts">
        <div className="grid gap-3 md:grid-cols-2">
          <Alert tone="info" title="Thresholds are provisional">Levels have not been statistically validated.</Alert>
          <Alert tone="success" title="Answers saved">Your progress is stored on the server.</Alert>
          <Alert tone="warning" title="Reassess to confirm">Not enough evidence to confirm a gap yet.</Alert>
          <Alert tone="danger" title="Could not save">Check your connection and try again.</Alert>
          <Alert tone="demo" title="Synthetic content">This course is demo material, not an approved programme.</Alert>
          <Alert tone="neutral" title="Neutral note">Supporting information without emphasis.</Alert>
        </div>
      </Section>

      <Section title="Cards and statistics">
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard label="Competencies for your role" value="2" description="Required by the selected job role" icon={<Target />} />
          <StatCard label="Baseline assessment" value="Completed" description="10 questions answered" icon={<ClipboardCheck />} />
          <StatCard label="Recommended courses" value="3" description="Linked to your gaps" icon={<BookOpen />} />
        </div>
        <Card className="mt-4 max-w-xl">
          <CardHeader>
            <CardTitle as="h3">Card title</CardTitle>
            <CardDescription>Cards group one topic with one clear action.</CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={40} label="Example progress" valueText="4 of 10 complete" />
            <p className="mt-2 text-sm text-muted-foreground">4 of 10 complete</p>
          </CardContent>
          <CardFooter>
            <Button size="sm">Continue</Button>
            <Button size="sm" variant="ghost">
              Details
            </Button>
          </CardFooter>
        </Card>
      </Section>

      <Section title="Tabs and disclosure">
        <Tabs defaultValue="completed">
          <TabsList aria-label="Example tabs">
            <TabsTrigger value="completed">Completed</TabsTrigger>
            <TabsTrigger value="pending">Pending</TabsTrigger>
            <TabsTrigger value="recommended">Recommended</TabsTrigger>
          </TabsList>
          <TabsContent value="completed">Completed items appear here.</TabsContent>
          <TabsContent value="pending">Pending items appear here.</TabsContent>
          <TabsContent value="recommended">Recommended items appear here.</TabsContent>
        </Tabs>
        <Disclosure title="How was this calculated?" className="mt-4 max-w-xl">
          Each question is marked by fixed rules. Harder questions count more. No AI is used.
        </Disclosure>
      </Section>

      <Section title="Forms">
        <div className="grid max-w-md gap-4">
          <Field id="ds-email" label="Email" hint="Use your work email.">
            <Input id="ds-email" type="email" aria-describedby="ds-email-hint" placeholder="name@example.invalid" />
          </Field>
          <Field id="ds-code" label="Organisation code" error="Enter the code your administrator gave you.">
            <Input id="ds-code" aria-invalid="true" aria-describedby="ds-code-error" />
          </Field>
        </div>
      </Section>

      <Section title="States" description="Loading appears after 300 ms; errors show a reference ID, not technical codes.">
        <div className="grid gap-4 md:grid-cols-3">
          <Card className="p-5">
            <LoadingState label="Loading example" />
            <div className="mt-4 flex items-center gap-3">
              <Skeleton className="size-10 rounded-full" />
              <div className="flex-1 space-y-2">
                <Skeleton className="h-4 w-1/2" />
                <Skeleton className="h-3 w-3/4" />
              </div>
            </div>
          </Card>
          <EmptyState title="No recommendations yet." action={<Button size="sm">Start assessment</Button>}>
            <p>Recommendations appear after your baseline assessment.</p>
          </EmptyState>
          <ErrorState error={sampleError} onRetry={() => toast("Retrying")} />
        </div>
      </Section>

      <Section title="Dialogs">
        <Button variant="secondary" onClick={() => setConfirmOpen(true)}>
          Open confirmation dialog
        </Button>
        <ConfirmationDialog
          open={confirmOpen}
          onOpenChange={setConfirmOpen}
          title="Submit your answers?"
          description="You cannot change answers after submitting."
          confirmLabel="Submit answers"
          onConfirm={() => {
            setConfirmOpen(false);
            toast.success("Submitted (example)");
          }}
        >
          1 question is unanswered and will be scored as not correct.
        </ConfirmationDialog>
      </Section>
    </div>
  );
}

function Section({ title, description, children }: { title: string; description?: string; children: React.ReactNode }) {
  return (
    <section aria-labelledby={`ds-${title}`} className="space-y-4">
      <div className="space-y-1 border-b border-border pb-2">
        <h2 id={`ds-${title}`} className="text-xl font-semibold">
          {title}
        </h2>
        {description ? <p className="text-sm text-muted-foreground">{description}</p> : null}
      </div>
      {children}
    </section>
  );
}
