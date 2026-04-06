import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function NewInvoicePage() {
  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div className="flex items-center gap-4">
        <Button
          variant="ghost"
          size="sm"
          nativeButton={false}
          render={<Link href="/invoices" />}
        >
          ← Back
        </Button>
      </div>
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Upload invoice</h1>
        <p className="text-muted-foreground">
          Drag-and-drop or pick PDF / PNG / JPG (max 5MB per PRD).
        </p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>File upload</CardTitle>
          <CardDescription>
            Wire this zone to presigned S3/Supabase upload and extraction job polling.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex min-h-[200px] items-center justify-center rounded-lg border border-dashed border-border bg-muted/30 text-sm text-muted-foreground">
            Upload UI placeholder
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
