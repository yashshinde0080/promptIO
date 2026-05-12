"use client";

import { useQuery } from "@tanstack/react-query";
import { analyticsApi } from "@/lib/api";

export function useAnalytics(period: "7d" | "30d" | "90d" = "30d") {
  const summary = useQuery({
    queryKey: ["analytics", "summary", period],
    queryFn: () => analyticsApi.summary(period).then((r) => r.data),
    staleTime: 5 * 60 * 1000,
  });

  const cost = useQuery({
    queryKey: ["analytics", "cost", period],
    queryFn: () => analyticsApi.cost(period).then((r) => r.data),
    staleTime: 5 * 60 * 1000,
  });

  const performance = useQuery({
    queryKey: ["analytics", "performance"],
    queryFn: () => analyticsApi.performance().then((r) => r.data),
    staleTime: 5 * 60 * 1000,
  });

  return { summary, cost, performance };
}