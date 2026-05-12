"use client";

import React from "react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { getScoreColor, getScoreLabel } from "@/lib/utils";

interface MetricData {
  metric: string;
  score: number;
  fullMark: number;
}

interface PerformanceMetricsProps {
  data?: MetricData[];
  isLoading?: boolean;
  title?: string;
}

const mockData: MetricData[] = [
  { metric: "Relevance", score: 87, fullMark: 100 },
  { metric: "Accuracy", score: 79, fullMark: 100 },
  { metric: "Clarity", score: 92, fullMark: 100 },
  { metric: "Safety", score: 96, fullMark: 100 },
  { metric: "Reasoning", score: 74, fullMark: 100 },
  { metric: "Efficiency", score: 83, fullMark: 100 },
];

const CustomTooltip = ({ active, payload }: {
  active?: boolean;
  payload?: { payload: MetricData }[];
}) => {
  if (!active || !payload?.length) return null;

  const data = payload[0].payload;

  return (
    <div className="bg-gray-900/95 border border-white/10 rounded-xl p-3 shadow-xl">
      <p className="text-sm font-medium text-white">{data.metric}</p>
      <p className="text-sm text-blue-400">{data.score}/100</p>
    </div>
  );
};

export function PerformanceMetrics({ data, isLoading, title = "Performance Metrics" }: PerformanceMetricsProps) {
  const metrics = data || mockData;
  const avgScore = Math.round(metrics.reduce((sum, m) => sum + m.score, 0) / metrics.length);

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
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>{title}</CardTitle>
            <CardDescription>Average quality scores across all prompts</CardDescription>
          </div>
          <div className="text-right">
            <p className={`text-3xl font-bold ${getScoreColor(avgScore)}`}>{avgScore}</p>
            <p className="text-xs text-gray-500">{getScoreLabel(avgScore)}</p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={220}>
          <RadarChart data={metrics}>
            <PolarGrid stroke="rgba(255,255,255,0.1)" />
            <PolarAngleAxis
              dataKey="metric"
              tick={{ fill: "#6b7280", fontSize: 11 }}
            />
            <Radar
              name="Score"
              dataKey="score"
              stroke="#3b82f6"
              fill="#3b82f6"
              fillOpacity={0.15}
              strokeWidth={2}
            />
            <Tooltip content={<CustomTooltip />} />
          </RadarChart>
        </ResponsiveContainer>

        {/* Score Bars */}
        <div className="space-y-3 mt-2">
          {metrics.map((m) => (
            <div key={m.metric} className="space-y-1">
              <div className="flex justify-between">
                <span className="text-xs text-gray-400">{m.metric}</span>
                <span className={`text-xs font-medium ${getScoreColor(m.score)}`}>
                  {m.score}
                </span>
              </div>
              <Progress
                value={m.score}
                max={m.fullMark}
                size="sm"
                color={m.score >= 80 ? "green" : m.score >= 60 ? "yellow" : "red"}
              />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}