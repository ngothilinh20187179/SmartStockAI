"use client"

import { usePathname } from "next/navigation"

import { AppSidebar } from "@/components/layout/app-sidebar"
import { ThemeToggle } from "@/components/layout/theme-toggle"

type AppShellProps = {
  children: React.ReactNode
}

export function AppShell({ children }: AppShellProps) {
  const pathname = usePathname()

  return (
    <div className="flex min-h-screen bg-background">
      <AppSidebar pathname={pathname} />
      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center justify-end gap-2 border-b border-border px-4">
          <ThemeToggle />
        </header>
        <main className="flex-1 p-6">{children}</main>
      </div>
    </div>
  )
}
