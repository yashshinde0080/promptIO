"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Clock, RotateCcw } from "lucide-react";
import { relativeTime } from "@/lib/utils";

const mockVersions = [
  {
    id: "v3",
    version: 3,
    summary: "Added role context, refined output format",
    author: "You",
    created_at: new Date(Date.now() - 5 * 60000).toISOString(),
    score: 91,
  },
  {
    id: "v2",
    version: 2,
    summary: "Improved specificity and added constraints",
    author: "You",
    created_at: new Date(Date.now() - 2 * 3600000).toISOString(),
    score: 84,
  },
  {
    id: "v1",
    version: 1,
    summary: "Initial version",
    author: "You",
    created_at: new Date(Date.now() - 24 * 3600000).toISOString(),
    score: 72,
  },
];

export function VersionHistory() {
  const [activeVersion, setActiveVersion] = useState("v3");

  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
        Version History
      </p>
      <ScrollArea className="h-48">
        <div className="space-y-1 pr-2">
          {mockVersions.map((v) => (
            <div
              key={v.id}
              onClick={() => setActiveVersion(v.id)}
              className={`p-2.5 rounded-lg border cursor-pointer transition-all duration-200 ${
                activeVersion === v.id
                  ? "border-primary/30 bg-primary/5"
                  : "border-transparent hover:border-border/50 hover:bg-muted/30"
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <div className="flex items-center gap-1.5">
                  <Clock className="w-3 h-3 text-muted-foreground" />
                  <span className="text-xs font-semibold">v{v.version}</span>
                </div>
                <span className="text-xs text-green-400 font-medium">
                  {v.score}
                </span>
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                {v.summary}
              </p>
              <p className="text-xs text-muted-foreground/60 mt-1">
                {relativeTime(v.created_at)}
              </p>
            </div>
          ))}
        </div>
      </ScrollArea>
      <Button
        variant="outline"
        size="sm"
        className="w-full h-7 text-xs border-border/50"
      >
        <RotateCcw className="w-3 h-3 mr-1.5" />
        Restore version
      </Button>
    </div>
  );
}