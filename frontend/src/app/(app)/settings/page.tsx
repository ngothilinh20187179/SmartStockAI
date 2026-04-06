import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Profile, organization, and price anomaly thresholds (UC-3.1).
        </p>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Account</CardTitle>
          <CardDescription>Placeholder for user and session preferences.</CardDescription>
        </CardHeader>
      </Card>
    </div>
  )
}
