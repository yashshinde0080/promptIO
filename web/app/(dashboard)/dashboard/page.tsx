"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { RefreshCw, Sparkles } from "lucide-react";
import { StatsCards } from "@/components/dashboard/stats-cards";
import { UsageChart } from "@/components/dashboard/usage-chart";
import { ActivityFeed } from "@/components/dashboard/activity-feed";
import { QuickActions } from "@/components/dashboard/quick-actions";
import { Button } from "@/components/ui/button";
import { analyticsApi, auditApi } from "@/lib/apis";
import { useAuthStore } from "@/store/auth-store";

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [period, setPeriod] = useState<"7d" | "30d" | "90d" | "1y">("7d");

  const { data: overview, isLoading: overviewLoading, refetch } = useQuery({
    queryKey: ["analytics", "overview", period],
    queryFn: () => analyticsApi.summary(period),
    staleTime: 60_000,
  });

  const { data: usageData, isLoading: usageLoading } = useQuery({
    queryKey: ["analytics", "usage", period],
    queryFn: () => analyticsApi.usage(period),
    staleTime: 60_000,
  });

  const { data: activityData, isLoading: activityLoading } = useQuery({
    queryKey: ["analytics", "activity"],
    queryFn: () => auditApi.getLogs({ page: 1 }),
    staleTime: 30_000,
    refetchInterval: 30_000,
  });

  const greeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  };

  return (
    <div className="p-6 lg:p-8 space-y-6 max-w-screen-2xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-foreground tracking-tight">
            {greeting()},{" "}
            <span className="text-gradient-primary">
              {user?.name?.split(" ")[0] ?? "there"}
            </span>
          </h1>
          <p className="text-muted-foreground mt-1 text-sm">
            Here&apos;s what&apos;s happening with your prompts today.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            className="gap-2"
          >
            <RefreshCw className="h-3.5 w-3.5" />
            Refresh
          </Button>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-primary/20 bg-primary/5 text-xs text-primary font-medium">
            <Sparkles className="h-3.5 w-3.5" />
            Dashboard
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <StatsCards data={overview} isLoading={overviewLoading} period={period} />

      {/* Charts Row */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div className="xl:col-span-2">
          <UsageChart
            data={usageData}
            isLoading={usageLoading}
            onPeriodChange={(p) => setPeriod(p as typeof period)}
          />
        </div>
        <div>
          <QuickActions />
        </div>
      </div>

      {/* Activity Feed + Frameworks */}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <ActivityFeed
          data={activityData?.data}
          isLoading={activityLoading}
        />
        <div className="space-y-4">
          <TopFrameworksWidget />
        </div>
      </div>
    </div>
  );
}

function TopFrameworksWidget() {
  const frameworks = [
    { name: "RACE", usage: 89, color: "bg-red-500" },
    { name: "Standard", usage: 76, color: "bg-blue-500" },
    { name: "CREATE", usage: 65, color: "bg-pink-500" },
    { name: "APE", usage: 54, color: "bg-orange-500" },
    { name: "CARE", usage: 43, color: "bg-emerald-500" },
    { name: "PAIN", usage: 32, color: "bg-rose-500" },
  ];

  return (
    <div className="rounded-xl border border-border/50 bg-card p-6">
      <h3 className="text-base font-semibold text-foreground mb-5">Top Frameworks</h3>
      <div className="space-y-4">
        {frameworks.map((f) => (
          <div key={f.name} className="space-y-1.5">
            <div className="flex justify-between text-sm">
              <span className="text-muted-foreground font-medium">{f.name}</span>
              <span className="text-foreground font-semibold tabular-nums">{f.usage}</span>
            </div>
            <div className="h-1.5 w-full bg-muted rounded-full overflow-hidden">
              <div
                className={`h-full rounded-full ${f.color} transition-all duration-700`}
                style={{ width: `${(f.usage / 89) * 100}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}