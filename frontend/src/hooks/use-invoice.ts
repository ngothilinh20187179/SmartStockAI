import { useQuery } from "@tanstack/react-query"

import { queryKeys } from "@/lib/query-keys"

export function useInvoice(id: string | undefined) {
  return useQuery({
    queryKey: id ? queryKeys.invoices.detail(id) : ["invoices", "detail", "none"],
    queryFn: async () => {
      // TODO: replace with api.get(`/api/invoices/${id}`)
      return { id, status: "placeholder" as const }
    },
    enabled: Boolean(id),
  })
}
