import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

type InvoiceDetailPageProps = {
  params: Promise<{ id: string }>
}

export default async function InvoiceDetailPage({ params }: InvoiceDetailPageProps) {
  const { id } = await params

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-4">
        <Button
          variant="ghost"
          size="sm"
          nativeButton={false}
          render={<Link href="/invoices" />}
        >
          ← Invoices
        </Button>
      </div>
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Invoice {id}</h1>
        <p className="text-muted-foreground">
          Split-view review, line items, SKU matching, and confirm stock (UC-03–UC-05).
        </p>
      </div>
      <div className="grid gap-4 lg:grid-cols-2">
        <Card className="min-h-[320px]">
          <CardHeader>
            <CardTitle className="text-base">Document preview</CardTitle>
            <CardDescription>PDF/image viewer placeholder</CardDescription>
          </CardHeader>
          <CardContent />
        </Card>
        <Card className="min-h-[320px]">
          <CardHeader>
            <CardTitle className="text-base">Extracted lines</CardTitle>
            <CardDescription>Editable table with confidence highlights</CardDescription>
          </CardHeader>
          <CardContent />
        </Card>
      </div>
    </div>
  )
}
