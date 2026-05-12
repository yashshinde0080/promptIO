"use client";

import { useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { Button } from "@/components/ui/button";

const data7d = [
  { date: "Mon", prompts: 45, cost: 1.2, quality: 82 },
  { date: "Tue", prompts: 62, cost: 1.8, quality: 85 },
  { date: "Wed", prompts: 38, cost: 0.9, quality: 83 },
  { date: "Thu", prompts: 91, cost: 2.4, quality: 88 },
  { date: "Fri", prompts: 74, cost: 2.1, quality: 87 },
  { date: "Sat", prompts: 28, cost: 0.7, quality: 86 },
  { date: "Sun", prompts: 35, cost: 0.8, quality: 89 },
];

const data30d = Array.from({ length: 30 }, (_, i) => ({
  date: `Day ${i + 1}`,
  prompts: Math.floor(Math.random() * 100) + 20,
  cost: Math.random() * 3,
  quality: Math.floor(Math.random() * 20) + 75,
}));

const CustomTooltip = ({ active, payload, label }: {
  active?: boolean;
  payload?: { value: number; name: string; color: string }[];
  label?: string;
}) => {
  if (active && payload?.length) {
    return (
      <div className="bg-popover border border-border/50 rounded-lg p-3 shadow-xl">
        <p className="text-xs text-muted-foreground mb-2">{label}</p>
        {payload.map((p) => (
          <div key={p.name} className="flex items-center gap-2 text-xs">
            <span
              className="w-2 h-2 rounded-full"
              style={{ background: p.color }}
            />
            <span className="text-muted-foreground capitalize">{p.name}:</span>
            <span className="font-medium">{p.value}</span>
          </div>
        ))}
      </div>
    );
  }
  return null;
};

export function UsageChart() {
  const [period, setPeriod] = useState<"7d" | "30d">("7d");
  const data = period === "7d" ? data7d : data30d;

  return (
    <div className="glass-card rounded-xl p-5">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h3 className="font-semibold">Prompt Usage & Quality</h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            Overview of prompt activity
          </p>
        </div>
        <div className="flex gap-1">
          {(["7d", "30d"] as const).map((p) => (
            <Button
              key={p}
              size="sm"
              variant={period === p ? "default" : "ghost"}
              onClick={() => setPeriod(p)}
              className="h-7 text-xs"
            >
              {p}
            </Button>
          ))}
        </div>
      </div>

      <ResponsiveContainer width="100%" height={260}>
        <AreaChart data={data} margin={{ top: 5, right: 5, bottom: 5, left: 0 }}>
          <defs>
            <linearGradient id="colorPrompts" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#3B82F6" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorQuality" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1E2D40" />
          <XAxis
            dataKey="date"
            stroke="#475569"
            tick={{ fill: "#64748B", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            stroke="#475569"
            tick={{ fill: "#64748B", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: "12px", paddingTop: "16px" }}
            formatter={(value) => (
              <span style={{ color: "#94A3B8" }}>{value}</span>
            )}
          />
          <Area
            type="monotone"
            dataKey="prompts"
            stroke="#3B82F6"
            strokeWidth={2}
            fill="url(#colorPrompts)"
            dot={false}
          />
          <Area
            type="monotone"
            dataKey="quality"
            stroke="#8B5CF6"
            strokeWidth={2}
            fill="url(#colorQuality)"
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}