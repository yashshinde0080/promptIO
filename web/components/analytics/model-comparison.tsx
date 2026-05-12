"use client";

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { formatLatency, formatCurrency } from "@/lib/utils";
import { ModelUsageStat } from "@/types";

interface ModelComparisonProps {
  data?: ModelUsageStat[];
  isLoading?: boolean;
}

const mockData: ModelUsageStat[] = [
  { model: "GPT-4o", usage_count: 245, total_cost: 12.45, avg_latency: 1840, success_rate: 98.2 },
  { model: "Claude 3.5", usage_count: 189, total_cost: 8.32, avg_latency: 2100, success_rate: 97.8 },
  { model: "Gemini Pro", usage_count: 134, total_cost: 4.21, avg_latency: 1620, success_rate: 96.5 },
  { model: "GPT-4o Mini", usage_count: 98, total_cost: 2.11, avg_latency: 890, success_rate: 99.1 },
  { model: "Llama 3.1", usage_count: 67, total_cost: 1.05, avg_latency: 2340, success_rate: 94.3 },
];

const CustomTooltip = ({ active, payload, label }: {
  active?: boolean;
  payload?: { value: number; name: string }[];
  label?: string;
}) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-gray-900/95 border border-white/10 rounded-xl p-3 shadow-2xl backdrop-blur-xl">
      <p className="text-sm font-medium text-white mb-2">{label}</p>
      {payload.map((p) => (
        <div key={p.name} className="text-xs text-gray-400">
          <span className="capitalize">{p.name}:</span>{" "}
          <span className="text-white font-medium">{p.value}</span>
        </div>
      ))}
    </div>
  );
};

export function ModelComparison({ data, isLoading }: ModelComparisonProps) {
  const chartData = (data || mockData).map((d) => ({
    ...d,
    model: d.model.replace("anthropic/", "").replace("openai/", "").replace("google/", ""),
    success_rate: parseFloat(d.success_rate.toFixed(1)),
  }));

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <Skeleton className="h-5 w-40" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-64 w-full" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Model Comparison</CardTitle>
        <CardDescription>Usage count and success rates by model</CardDescription>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={240}>
          <BarChart data={chartData} margin={{ top: 5, right: 5, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis
              dataKey="model"
              tick={{ fill: "#6b7280", fontSize: 10 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: "#6b7280", fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="usage_count" name="Usage" fill="#3b82f6" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>

        {/* Model Table */}
        <div className="mt-4 space-y-2">
          <div className="grid grid-cols-5 text-xs text-gray-500 pb-2 border-b border-white/10">
            <span>Model</span>
            <span className="text-right">Uses</span>
            <span className="text-right">Cost</span>
            <span className="text-right">Latency</span>
            <span className="text-right">Success</span>
          </div>
          {(data || mockData).map((item) => {
            const shortName = item.model
              .replace("anthropic/", "")
              .replace("openai/", "")
              .replace("google/", "")
              .replace("meta-llama/", "")
              .replace("mistralai/", "")
              .replace("deepseek/", "");

            return (
              <div
                key={item.model}
                className="grid grid-cols-5 text-xs py-2 hover:bg-white/5 rounded-lg transition-colors"
              >
                <span className="text-gray-300 font-medium">{shortName}</span>
                <span className="text-right text-gray-400">{item.usage_count}</span>
                <span className="text-right text-gray-400">{formatCurrency(item.total_cost)}</span>
                <span className="text-right text-gray-400">{formatLatency(item.avg_latency)}</span>
                <div className="flex justify-end">
                  <Badge
                    variant={item.success_rate >= 97 ? "success" : item.success_rate >= 90 ? "warning" : "destructive"}
                    className="text-xs"
                  >
                    {item.success_rate.toFixed(1)}%
                  </Badge>
                </div>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}