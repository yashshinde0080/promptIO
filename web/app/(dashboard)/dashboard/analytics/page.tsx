"use client";

import React, { useState } from "react";
import { BarChart3, Download, Calendar as CalendarIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { CostChart } from "@/components/analytics/cost-chart";
import { PerformanceMetrics } from "@/components/analytics/performance-metrics";
import { ModelComparison } from "@/components/analytics/model-comparison";

export default function AnalyticsPage() {
  const [period, setPeriod] = useState("30d");

  return (
    <div className="p-6 space-y-6 max-w-screen-2xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <BarChart3 className="h-6 w-6 text-blue-400" />
            Analytics & Reports
          </h1>
          <p className="text-gray-400 mt-1 text-sm">
            Deep dive into your prompt performance, usage, and costs.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Select value={period} onValueChange={setPeriod}>
            <SelectTrigger className="w-40">
              <SelectValue placeholder="Select period" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="7d">Last 7 days</SelectItem>
              <SelectItem value="30d">Last 30 days</SelectItem>
              <SelectItem value="90d">Last 90 days</SelectItem>
              <SelectItem value="1y">Last year</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" className="gap-2">
            <Download className="h-4 w-4" />
            Export CSV
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div className="space-y-6">
          <PerformanceMetrics period={period} />
          <CostChart isLoading={false} />
        </div>
        <div className="space-y-6">
          <ModelComparison period={period} />
        </div>
      </div>
    </div>
  );
}
