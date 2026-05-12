"use client";

import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { formatCurrency } from "@/lib/utils";
import { CHART_COLOR_PALETTE } from "@/lib/constants";

interface CostData {
  model: string;
  cost: number;
}

interface CostChartProps {
  data?: CostData[];
  isLoading?: boolean;
  totalCost?: number;
}

const mockData: CostData[] = [
  { model: "GPT-4o", cost: 12.45 },
  { model: "Claude 3.5", cost: 8.32 },
  { model: "Gemini Pro", cost: 4.21 },
  { model: "GPT-4o Mini", cost: 2.11 },
  { model: "Llama 3.1", cost: 1.05 },
];

const CustomTooltip = ({ active, payload }: {
  active?: boolean;
  payload?: { name: string; value: number; payload: CostData }[];
}) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-gray-900/95 border border-white/10 rounded-xl p-3 shadow-2xl backdrop-blur-xl">
      <p className="text-sm font-medium text-white">{payload[0].name}</p>
      <p className="text-sm text-gray-300">{formatCurrency(payload[0].value)}</p>
    </div>
  );
};

const CustomLegend = ({ data }: { data: CostData[] }) => {
  const total = data.reduce((sum, d) => sum + d.cost, 0);

  return (
    <div className="space-y-2 mt-4">
      {data.map((item, index) => (
        <div key={item.model} className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div
              className="h-3 w-3 rounded-full shrink-0"
              style={{ backgroundColor: CHART_COLOR_PALETTE[index % CHART_COLOR_PALETTE.length] }}
            />
            <span className="text-sm text-gray-400">{item.model}</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-500">
              {((item.cost / total) * 100).toFixed(1)}%
            </span>
            <span className="text-sm font-medium text-white w-16 text-right">
              {formatCurrency(item.cost)}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export function CostChart({ data, isLoading, totalCost }: CostChartProps) {
  const chartData = data || mockData;
  const total = totalCost || chartData.reduce((sum, d) => sum + d.cost, 0);

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <Skeleton className="h-5 w-32" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-48 w-48 rounded-full mx-auto" />
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Cost Breakdown</CardTitle>
            <CardDescription>By AI model usage</CardDescription>
          </div>
          <div className="text-right">
            <p className="text-2xl font-bold text-white">{formatCurrency(total)}</p>
            <p className="text-xs text-gray-500">total spend</p>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={200}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={90}
              paddingAngle={3}
              dataKey="cost"
              nameKey="model"
            >
              {chartData.map((_, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={CHART_COLOR_PALETTE[index % CHART_COLOR_PALETTE.length]}
                  stroke="transparent"
                />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
        <CustomLegend data={chartData} />
      </CardContent>
    </Card>
  );
}