"use client";

import React from "react";
import Link from "next/link";
import {
  Plus,
  Zap,
  BarChart3,
  Library,
  ArrowRight,
  FileText,
  GitBranch,
} from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const quickActions = [
  {
    title: "New Prompt",
    description: "Create and optimize a new prompt",
    icon: Plus,
    href: "/prompt-studio",
    gradient: "from-blue-600 to-indigo-700",
    shortcut: "⌘N",
  },
  {
    title: "Optimize Existing",
    description: "Improve a saved prompt",
    icon: Zap,
    href: "/prompt-studio",
    gradient: "from-violet-600 to-purple-700",
    shortcut: "⌘O",
  },
  {
    title: "Run Evaluation",
    description: "Benchmark prompt quality",
    icon: BarChart3,
    href: "/evaluations",
    gradient: "from-emerald-600 to-teal-700",
    shortcut: "⌘E",
  },
  {
    title: "Browse Templates",
    description: "Use pre-built frameworks",
    icon: Library,
    href: "/templates",
    gradient: "from-amber-600 to-orange-700",
    shortcut: "⌘T",
  },
];

const recentPrompts = [
  { id: "1", title: "Customer Support Bot", framework: "RACE", updated: "2h ago" },
  { id: "2", title: "Code Review Assistant", framework: "APE", updated: "4h ago" },
  { id: "3", title: "Marketing Copy Generator", framework: "CREATE", updated: "1d ago" },
];

export function QuickActions() {
  return (
    <div className="space-y-4">
      {/* Quick Action Buttons */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-3">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Link key={action.title} href={action.href}>
                <div
                  className={`
                    group relative overflow-hidden rounded-xl p-4 cursor-pointer
                    bg-gradient-to-br ${action.gradient}
                    border border-white/10 hover:border-white/25
                    transition-all duration-200 hover:shadow-lg hover:shadow-black/20
                  `}
                >
                  <div className="flex items-center gap-2 mb-2">
                    <Icon className="h-5 w-5 text-white" />
                    <kbd className="text-[10px] text-white/50 ml-auto font-mono bg-white/10 px-1.5 py-0.5 rounded">
                      {action.shortcut}
                    </kbd>
                  </div>
                  <p className="text-sm font-semibold text-white">{action.title}</p>
                  <p className="text-xs text-white/60 mt-0.5">{action.description}</p>
                  <ArrowRight className="absolute right-3 bottom-3 h-4 w-4 text-white/30 group-hover:text-white/70 group-hover:translate-x-0.5 transition-all" />
                </div>
              </Link>
            );
          })}
        </CardContent>
      </Card>

      {/* Recent Prompts */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle className="text-base">Recent Prompts</CardTitle>
          <Link href="/prompt-studio">
            <Button variant="ghost" size="sm" className="text-xs text-muted-foreground hover:text-foreground">
              View all <ArrowRight className="h-3 w-3 ml-1" />
            </Button>
          </Link>
        </CardHeader>
        <CardContent className="space-y-1">
          {recentPrompts.map((prompt) => (
            <Link
              key={prompt.id}
              href={`/prompt-studio?id=${prompt.id}`}
              className="flex items-center gap-3 p-3 rounded-lg hover:bg-muted/50 transition-colors group cursor-pointer"
            >
              <div className="h-8 w-8 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center shrink-0">
                <FileText className="h-4 w-4 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-foreground group-hover:text-primary transition-colors truncate">
                  {prompt.title}
                </p>
                <div className="flex items-center gap-2 mt-0.5">
                  <span className="text-xs text-muted-foreground">{prompt.framework}</span>
                  <span className="text-muted-foreground/40">·</span>
                  <span className="text-xs text-muted-foreground">{prompt.updated}</span>
                </div>
              </div>
              <GitBranch className="h-4 w-4 text-muted-foreground/40 group-hover:text-muted-foreground transition-colors shrink-0" />
            </Link>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}