import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

export default function ProductsPage() {
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
          Use TanStack Query with <code className="text-xs">queryKeys.products</code> when
          connecting to FastAPI.
        </CardDescription>
        </CardHeader>
        <CardContent className="pt-0">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>SKU</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Category</TableHead>
              <TableHead className="text-right">Stock</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            <TableRow>
              <TableCell colSpan={4} className="text-center text-muted-foreground">
                No products loaded.
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
        </CardContent>
      </Card>
    </div>
  )
}
