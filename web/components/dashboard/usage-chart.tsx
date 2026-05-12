"use client";

import React, { useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { UsageDataPoint } from "@/types";

interface UsageChartProps {
  data?: UsageDataPoint[];
  isLoading?: boolean;
  onPeriodChange?: (period: string) => void;
}

const CustomTooltip = ({ active, payload, label }: {
  active?: boolean;
  payload?: { name: string; value: number; color: string }[];
  label?: string;
}) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-card/95 border border-border/50 rounded-xl p-3 shadow-2xl backdrop-blur-xl">
      <p className="text-xs text-muted-foreground mb-2">{label}</p>
      {payload.map((entry) => (
        <div key={entry.name} className="flex items-center gap-2 text-sm">
          <div className="h-2 w-2 rounded-full" style={{ backgroundColor: entry.color }} />
          <span className="text-muted-foreground capitalize">{entry.name}:</span>
          <span className="text-foreground font-medium">{entry.value}</span>
        </div>
      ))}
    </div>
  );
};

export function UsageChart({ data, isLoading, onPeriodChange }: UsageChartProps) {
  const [activeMetric, setActiveMetric] = useState<"all" | "prompts" | "optimizations" | "cost">(
    "all"
  );

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <Skeleton className="h-5 w-32" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-64 w-full" />
        </CardContent>
      </Card>
    );
  }

  // Mock data if none provided
  const chartData = data || Array.from({ length: 14 }, (_, i) => ({
    date: new Date(Date.now() - (13 - i) * 24 * 60 * 60 * 1000).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    }),
    prompts: Math.floor(Math.random() * 80 + 20),
    optimizations: Math.floor(Math.random() * 60 + 10),
    cost: parseFloat((Math.random() * 5 + 1).toFixed(2)),
    tokens: Math.floor(Math.random() * 50000 + 10000),
  }));

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Usage Overview</CardTitle>
        <div className="flex items-center gap-3">
          <Tabs defaultValue="7d" onValueChange={(v) => onPeriodChange?.(v)}>
            <TabsList className="h-8">
              <TabsTrigger value="7d" className="text-xs px-2.5 py-1">7D</TabsTrigger>
              <TabsTrigger value="30d" className="text-xs px-2.5 py-1">30D</TabsTrigger>
              <TabsTrigger value="90d" className="text-xs px-2.5 py-1">90D</TabsTrigger>
            </TabsList>
          </Tabs>
        </div>
      </CardHeader>
      <CardContent>
        {/* Metric Filter */}
        <div className="flex gap-2 mb-4">
          {["all", "prompts", "optimizations"].map((metric) => (
            <button
              key={metric}
              onClick={() => setActiveMetric(metric as typeof activeMetric)}
              className={`px-3 py-1 text-xs rounded-full border transition-colors cursor-pointer ${
                activeMetric === metric
                  ? "bg-primary/15 border-primary/40 text-primary"
                  : "border-border text-muted-foreground hover:text-foreground hover:border-border/80"
              }`}
            >
              {metric.charAt(0).toUpperCase() + metric.slice(1)}
            </button>
          ))}
        </div>

        <ResponsiveContainer width="100%" height={280}>
          <AreaChart data={chartData} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <defs>
              <linearGradient id="promptsGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="optimizationsGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a78bfa" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#a78bfa" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.04)" />
            <XAxis
              dataKey="date"
              tick={{ fill: "#6b7280", fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: "#6b7280", fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            {(activeMetric === "all" || activeMetric === "prompts") && (
              <Area
                type="monotone"
                dataKey="prompts"
                name="Prompts"
                stroke="#6366f1"
                strokeWidth={2}
                fill="url(#promptsGrad)"
              />
            )}
            {(activeMetric === "all" || activeMetric === "optimizations") && (
              <Area
                type="monotone"
                dataKey="optimizations"
                name="Optimizations"
                stroke="#a78bfa"
                strokeWidth={2}
                fill="url(#optimizationsGrad)"
              />
            )}
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}