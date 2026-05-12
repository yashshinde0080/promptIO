"use client";

import React from "react";
import {
  Zap,
  DollarSign,
  TrendingUp,
  Users,
  FileText,
  Clock,
  ArrowUpRight,
  ArrowDownRight,
  Minus,
} from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { cn, formatCurrency, formatNumber, formatChange } from "@/lib/utils";

interface StatCard {
  label: string;
  value: string | number;
  change: number;
  changeType: "increase" | "decrease" | "neutral";
  icon: React.ElementType;
  gradient: string;
  iconBg: string;
  prefix?: string;
  suffix?: string;
  description?: string;
}

interface StatsCardsProps {
  data?: any;
  isLoading?: boolean;
  period?: string;
}

export function StatsCards({ data, isLoading, period = "7d" }: StatsCardsProps) {
  const statsData = data?.data || data;
  const totalPrompts = statsData?.total_prompts ?? statsData?.total_runs ?? 0;
  const totalOptimizations = statsData?.total_optimizations ?? statsData?.total_runs ?? 0;
  const totalCost = statsData?.total_cost_usd ?? statsData?.total_cost ?? 0;
  const avgImprovement = statsData?.avg_improvement_score ?? statsData?.avg_quality_score ?? 0;
  const totalTokens = statsData?.total_tokens_used ?? statsData?.total_tokens ?? 0;
  const activeUsers = statsData?.active_users ?? statsData?.member_count ?? statsData?.total_users ?? 0;

  const stats: StatCard[] = [
    {
      label: "Total Prompts",
      value: formatNumber(totalPrompts),
      change: 12.5,
      changeType: "increase",
      icon: FileText,
      gradient: "from-blue-500/15 to-blue-600/5",
      iconBg: "bg-blue-500/15 text-blue-400",
      description: `vs last ${period}`,
    },
    {
      label: "Optimizations",
      value: formatNumber(totalOptimizations),
      change: 23.1,
      changeType: "increase",
      icon: Zap,
      gradient: "from-violet-500/15 to-violet-600/5",
      iconBg: "bg-violet-500/15 text-violet-400",
      description: `vs last ${period}`,
    },
    {
      label: "Total Cost",
      value: formatCurrency(totalCost),
      change: -8.3,
      changeType: "decrease",
      icon: DollarSign,
      gradient: "from-emerald-500/15 to-emerald-600/5",
      iconBg: "bg-emerald-500/15 text-emerald-400",
      description: "lower is better",
    },
    {
      label: "Avg Improvement",
      value: `${(avgImprovement || 0).toFixed(0)}%`,
      change: 5.2,
      changeType: "increase",
      icon: TrendingUp,
      gradient: "from-amber-500/15 to-amber-600/5",
      iconBg: "bg-amber-500/15 text-amber-400",
      description: "quality score",
    },
    {
      label: "Tokens Used",
      value: formatNumber(totalTokens),
      change: 18.7,
      changeType: "increase",
      icon: Clock,
      gradient: "from-cyan-500/15 to-cyan-600/5",
      iconBg: "bg-cyan-500/15 text-cyan-400",
      description: `vs last ${period}`,
    },
    {
      label: "Active Users",
      value: formatNumber(activeUsers),
      change: 0,
      changeType: "neutral",
      icon: Users,
      gradient: "from-pink-500/15 to-pink-600/5",
      iconBg: "bg-pink-500/15 text-pink-400",
      description: "this period",
    },
  ];

  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <div key={i} className="rounded-xl border border-border/50 bg-card p-5">
            <Skeleton className="h-4 w-24 mb-4" />
            <Skeleton className="h-8 w-32 mb-2" />
            <Skeleton className="h-3 w-20" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {stats.map((stat) => (
        <StatCardItem key={stat.label} stat={stat} />
      ))}
    </div>
  );
}

function StatCardItem({ stat }: { stat: StatCard }) {
  const ChangeIcon =
    stat.changeType === "increase"
      ? ArrowUpRight
      : stat.changeType === "decrease"
      ? ArrowDownRight
      : Minus;

  const changeColor =
    stat.changeType === "increase"
      ? "text-emerald-400"
      : stat.changeType === "decrease"
      ? "text-red-400"
      : "text-muted-foreground";

  const Icon = stat.icon;

  return (
    <div
      className={cn(
        "relative group rounded-xl border border-border/50 bg-card p-5",
        "hover:border-primary/30 transition-all duration-300",
        "hover:shadow-lg hover:shadow-primary/5"
      )}
    >
      {/* Subtle gradient background */}
      <div className={cn("absolute inset-0 rounded-xl bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-opacity duration-300", stat.gradient)} />

      <div className="relative z-10">
        {/* Header row */}
        <div className="flex items-center justify-between mb-3">
          <div className={cn("p-2.5 rounded-lg", stat.iconBg)}>
            <Icon className="h-4.5 w-4.5" />
          </div>
          <div className={cn("flex items-center gap-1 text-xs font-medium tabular-nums", changeColor)}>
            <ChangeIcon className="h-3.5 w-3.5" />
            <span>{formatChange(stat.change)}</span>
          </div>
        </div>

        {/* Value */}
        <p className="text-2xl font-bold text-foreground tracking-tight mb-0.5">
          {stat.value}
        </p>
        <p className="text-sm font-medium text-muted-foreground">{stat.label}</p>
        {stat.description && (
          <p className="text-xs text-muted-foreground/60 mt-1">{stat.description}</p>
        )}
      </div>
    </div>
  );
}