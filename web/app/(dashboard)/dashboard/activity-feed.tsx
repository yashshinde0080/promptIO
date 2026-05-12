"use client";

import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { FRAMEWORKS } from "@/lib/constants";
import { relativeTime } from "@/lib/utils";

const activities = [
  {
    id: "1",
    action: "Optimized",
    prompt: "Customer support chatbot",
    framework: "race",
    user: "Alice K.",
    time: new Date(Date.now() - 5 * 60000).toISOString(),
    score: 91,
  },
  {
    id: "2",
    action: "Created",
    prompt: "Market analysis report",
    framework: "coast",
    user: "Bob M.",
    time: new Date(Date.now() - 18 * 60000).toISOString(),
    score: 87,
  },
  {
    id: "3",
    action: "Evaluated",
    prompt: "Code review assistant",
    framework: "ape",
    user: "Carol S.",
    time: new Date(Date.now() - 45 * 60000).toISOString(),
    score: 94,
  },
  {
    id: "4",
    action: "Optimized",
    prompt: "Legal contract summary",
    framework: "create",
    user: "David L.",
    time: new Date(Date.now() - 2 * 3600000).toISOString(),
    score: 89,
  },
  {
    id: "5",
    action: "Shared",
    prompt: "Email campaign writer",
    framework: "care",
    user: "Eve R.",
    time: new Date(Date.now() - 4 * 3600000).toISOString(),
    score: 85,
  },
  {
    id: "6",
    action: "Optimized",
    prompt: "Technical doc generator",
    framework: "rise",
    user: "Frank T.",
    time: new Date(Date.now() - 6 * 3600000).toISOString(),
    score: 92,
  },
];

export function ActivityFeed() {
  return (
    <div className="glass-card rounded-xl p-5 h-full">
      <div className="flex items-center justify-between mb-5">
        <div>
          <h3 className="font-semibold">Team Activity</h3>
          <p className="text-xs text-muted-foreground mt-0.5">
            Recent prompt actions
          </p>
        </div>
        <Badge
          variant="outline"
          className="text-xs border-green-500/30 text-green-400 bg-green-500/10"
        >
          Live
        </Badge>
      </div>

      <ScrollArea className="h-72">
        <div className="space-y-3">
          {activities.map((activity) => {
            const fw = FRAMEWORKS.find((f) => f.id === activity.framework);
            return (
              <div
                key={activity.id}
                className="flex items-start gap-3 p-2 rounded-lg hover:bg-muted/30 transition-colors group"
              >
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500/30 to-violet-500/30 flex items-center justify-center text-xs font-bold flex-shrink-0 border border-border/50">
                  {activity.user.charAt(0)}
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-1.5 flex-wrap">
                    <span className="text-xs font-medium">
                      {activity.user}
                    </span>
                    <span className="text-xs text-muted-foreground">
                      {activity.action.toLowerCase()}
                    </span>
                  </div>
                  <p className="text-xs text-foreground/70 truncate mt-0.5">
                    {activity.prompt}
                  </p>
                  <div className="flex items-center gap-2 mt-1">
                    <Badge
                      variant="outline"
                      className={`text-xs py-0 px-1.5 ${fw?.accentColor}`}
                    >
                      {fw?.name ?? activity.framework}
                    </Badge>
                    <span className="text-xs text-green-400 font-medium">
                      {activity.score}
                    </span>
                    <span className="text-xs text-muted-foreground ml-auto">
                      {relativeTime(activity.time)}
                    </span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </ScrollArea>
    </div>
  );
}