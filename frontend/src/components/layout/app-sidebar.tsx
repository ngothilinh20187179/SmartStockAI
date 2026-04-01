import {
  LayoutDashboard,
  Package,
  Settings,
  FileSpreadsheet,
} from "lucide-react"
import Link from "next/link"

import { cn } from "@/lib/utils"

const nav = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/invoices", label: "Invoices", icon: FileSpreadsheet },
  { href: "/products", label: "Products", icon: Package },
  { href: "/settings", label: "Settings", icon: Settings },
] as const

type AppSidebarProps = {
  pathname: string
}

export function AppSidebar({ pathname }: AppSidebarProps) {
  return (
    <aside className="flex w-56 shrink-0 flex-col border-r border-border bg-sidebar text-sidebar-foreground">
      <div className="flex h-14 items-center border-b border-sidebar-border px-4">
        <Link href="/" className="font-semibold tracking-tight">
          SmartStock AI
        </Link>
      </div>
      <nav className="flex flex-1 flex-col gap-1 p-2">
        {nav.map(({ href, label, icon: Icon }) => {
          const active =
            href === "/"
              ? pathname === "/"
              : pathname === href || pathname.startsWith(`${href}/`)
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                active
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-sidebar-foreground/80 hover:bg-sidebar-accent/50 hover:text-sidebar-accent-foreground"
              )}
            >
              <Icon className="size-4 shrink-0" />
              {label}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}
