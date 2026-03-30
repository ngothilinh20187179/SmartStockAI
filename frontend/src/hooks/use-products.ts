import { useQuery } from "@tanstack/react-query"

import { queryKeys } from "@/lib/query-keys"

export function useProducts(filters?: Record<string, unknown>) {
  return useQuery({
    queryKey: queryKeys.products.list(filters),
    queryFn: async () => {
      // TODO: replace with api.get("/api/products", { params: filters })
      return [] as const
    },
  })
}
