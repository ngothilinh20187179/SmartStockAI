"use client"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

import * as React from "react"

import { useProducts } from "@/hooks/use-products"

export default function ProductsPage() {
  const [q, setQ] = React.useState("")
  const [page, setPage] = React.useState(0)
  const limit = 25
  const offset = page * limit

  const { data, isLoading, isError, error, isFetching } = useProducts({
    q: q.trim() ? q.trim() : undefined,
    limit,
    offset,
  })

  const total = data?.meta.total ?? 0
  const pageCount = Math.max(1, Math.ceil(total / limit))
  const canPrev = page > 0
  const canNext = page + 1 < pageCount

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Products</h1>
        <p className="text-muted-foreground">
          SKU master data — searchable, filterable CRUD (UC-06).
        </p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Catalog</CardTitle>
          <CardDescription>
            Search by name / SKU / barcode. Showing {data ? data.items.length : 0} of{" "}
            {total}.
            {isFetching && !isLoading ? " Updating…" : null}
          </CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="mb-3 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex w-full max-w-md items-center gap-2">
              <Input
                value={q}
                onChange={(e) => {
                  setQ(e.target.value)
                  setPage(0)
                }}
                placeholder="Search products…"
              />
              <Button
                variant="outline"
                onClick={() => {
                  setQ("")
                  setPage(0)
                }}
                disabled={!q.trim()}
              >
                Clear
              </Button>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                onClick={() => setPage((p) => Math.max(0, p - 1))}
                disabled={!canPrev || isLoading}
              >
                Prev
              </Button>
              <div className="text-sm text-muted-foreground">
                Page <span className="text-foreground">{page + 1}</span> /{" "}
                <span className="text-foreground">{pageCount}</span>
              </div>
              <Button
                variant="outline"
                onClick={() => setPage((p) => (canNext ? p + 1 : p))}
                disabled={!canNext || isLoading}
              >
                Next
              </Button>
            </div>
          </div>

          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>SKU</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>Category</TableHead>
                <TableHead>Status</TableHead>
                <TableHead className="text-right">Stock</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center text-muted-foreground">
                    Loading…
                  </TableCell>
                </TableRow>
              ) : isError ? (
                <TableRow>
                  <TableCell colSpan={5} className="text-center text-destructive">
                    Failed to load products{error instanceof Error ? `: ${error.message}` : "."}
                  </TableCell>
                </TableRow>
              ) : data && data.items.length > 0 ? (
                data.items.map((p) => (
                  <TableRow key={p.id}>
                    <TableCell className="font-medium">{p.sku_code ?? "—"}</TableCell>
                    <TableCell>{p.product_name}</TableCell>
                    <TableCell>{p.category_name ?? "—"}</TableCell>
                    <TableCell className="capitalize">{String(p.status).replaceAll("_", " ")}</TableCell>
                    <TableCell className="text-right tabular-nums">
                      {typeof p.stock_quantity === "number"
                        ? p.stock_quantity
                        : p.stock_quantity ?? "0"}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} className="text-center text-muted-foreground">
                    No products found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
