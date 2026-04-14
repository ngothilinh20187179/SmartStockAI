import type { Pagination } from "@/types/common"

export type ProductsListParams = {
  q?: string
  limit?: number
  offset?: number
}

export type ProductListItem = {
  id: string
  sku_code: string | null
  product_code: string | null
  barcode: string | null
  product_name: string
  image_url: string | null
  description: string | null
  brand: string | null
  category_id: string | null
  category_name: string | null
  base_unit_id: string | null
  unit_name: string | null
  unit_symbol: string | null
  stock_quantity: string | number
  sales_volume: string | number
  reorder_level: string | number | null
  selling_price: string | number | null
  last_unit_price: string | number | null
  currency: string
  status: string
  warehouse_location: string | null
  is_batch_tracked: boolean
  batch_number: string | null
  expiry_date: string | null
}

export type ProductsListResponse = {
  items: ProductListItem[]
  meta: Pagination
}

