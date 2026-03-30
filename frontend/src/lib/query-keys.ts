export const queryKeys = {
  invoices: {
    all: ["invoices"] as const,
    list: (filters?: Record<string, unknown>) =>
      [...queryKeys.invoices.all, "list", filters] as const,
    detail: (id: string) => [...queryKeys.invoices.all, "detail", id] as const,
  },
  products: {
    all: ["products"] as const,
    list: (filters?: Record<string, unknown>) =>
      [...queryKeys.products.all, "list", filters] as const,
    detail: (id: string) => [...queryKeys.products.all, "detail", id] as const,
  },
} as const
