import { useQuery } from "@tanstack/react-query"

import { api } from "@/lib/api"
import { queryKeys } from "@/lib/query-keys"
import type { ProductsListParams, ProductsListResponse } from "@/types/products"

export function useProducts(params?: ProductsListParams) {
  return useQuery({
    queryKey: queryKeys.products.list(params),
    queryFn: async () => {
      const res = await api.get<ProductsListResponse>("/api/products", { params })
      return res.data
    },
  })
}
