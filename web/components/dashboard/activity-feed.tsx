"use client";

import React from "react";
import {
  Zap,
  FileText,
  Users,
  Settings,
  BarChart3,
  Clock,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { ScrollArea } from "@/components/ui/scroll-area";
import { formatRelativeTime } from "@/lib/utils";
import { ActivityItem } from "@/types";

const resourceIcons = {
  prompt: FileText,
  evaluation: BarChart3,
  team: Users,
  settings: Settings,
  api: Zap,
};

const resourceColors = {
  prompt: "text-blue-400",
  evaluation: "text-violet-400",
  team: "text-emerald-400",
  settings: "text-muted-foreground",
  api: "text-amber-400",
};

interface ActivityFeedProps {
  data?: any;
  isLoading?: boolean;
}

const mockActivities: ActivityItem[] = [
  {
    id: "1",
    user_id: "u1",
    user_name: "Alex Chen",
    action: "optimized prompt",
    resource_type: "prompt",
    resource_name: "Customer Support Bot",
    created_at: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
  },
  {
    id: "2",
    user_id: "u2",
    user_name: "Sarah Kim",
    action: "created evaluation",
    resource_type: "evaluation",
    resource_name: "GPT-4o vs Claude benchmark",
    created_at: new Date(Date.now() - 18 * 60 * 1000).toISOString(),
  },
  {
    id: "3",
    user_id: "u3",
    user_name: "Marcus Liu",
    action: "invited team member",
    resource_type: "team",
    resource_name: "john@company.com",
    created_at: new Date(Date.now() - 45 * 60 * 1000).toISOString(),
  },
  {
    id: "4",
    user_id: "u1",
    user_name: "Alex Chen",
    action: "created prompt",
    resource_type: "prompt",
    resource_name: "Code Review Assistant",
    created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: "5",
    user_id: "u4",
    user_name: "Priya Patel",
    action: "ran evaluation",
    resource_type: "evaluation",
    resource_name: "Marketing Copy Generator",
    created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
  },
];

// Simple color picker by name hash
function getAvatarColor(name: string) {
  const colors = [
    "from-blue-500 to-indigo-600",
    "from-violet-500 to-purple-600",
    "from-emerald-500 to-teal-600",
    "from-amber-500 to-orange-600",
    "from-rose-500 to-pink-600",
    "from-cyan-500 to-blue-600",
  ];
  const hash = name.split("").reduce((acc, c) => acc + c.charCodeAt(0), 0);
  return colors[hash % colors.length];
}

export function ActivityFeed({ data, isLoading }: ActivityFeedProps) {
  const activities: any[] = Array.isArray(data) 
    ? data 
    : data?.items || data?.data || mockActivities;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Recent Activity</CardTitle>
        <Badge variant="secondary" className="text-xs gap-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
          Live
        </Badge>
      </CardHeader>
      <CardContent className="p-0">
        {isLoading ? (
          <div className="p-6 space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex gap-3">
                <Skeleton className="h-9 w-9 rounded-full shrink-0" />
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-3 w-3/4" />
                  <Skeleton className="h-3 w-1/2" />
                </div>
              </div>
            ))}
          </div>
        ) : (
          <ScrollArea className="max-h-[380px]">
            <div className="divide-y divide-border/50">
              {activities.map((activity, idx) => {
                const resourceType = activity?.resource_type || "prompt";
                const ResourceIcon =
                  (resourceIcons as Record<string, any>)[resourceType] || FileText;
                const iconColor =
                  (resourceColors as Record<string, any>)[resourceType] || "text-muted-foreground";
                const userName = activity?.user_name || "System";
                const action = activity?.action || "performed action";
                const resourceName = activity?.resource_name || activity?.resource_id;

                return (
                  <div
                    key={activity?.id || idx}
                    className="flex gap-3 p-4 hover:bg-muted/30 transition-colors"
                  >
                    {/* Gradient avatar */}
                    <div
                      className={`w-9 h-9 rounded-full bg-gradient-to-br ${getAvatarColor(userName)} flex items-center justify-center text-white text-xs font-bold shrink-0`}
                    >
                      {userName.charAt(0)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className="text-sm font-medium text-foreground">
                          {userName}
                        </span>
                        <span className="text-sm text-muted-foreground">{action}</span>
                      </div>
                      {resourceName && (
                        <div className="flex items-center gap-1.5 mt-1">
                          <ResourceIcon className={`h-3.5 w-3.5 ${iconColor}`} />
                          <span className="text-xs text-muted-foreground/70 truncate">
                            {resourceName}
                          </span>
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-1 text-xs text-muted-foreground/50 shrink-0">
                      <Clock className="h-3 w-3" />
                      <span>{activity?.created_at ? formatRelativeTime(activity.created_at) : "just now"}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </ScrollArea>
        )}
      </CardContent>
    </Card>
  );
}