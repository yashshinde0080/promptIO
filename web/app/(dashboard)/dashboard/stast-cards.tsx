"use client";

import { motion } from "framer-motion";
import { Zap, TrendingUp, DollarSign, Clock, Target, Shield } from "lucide-react";
import { cn } from "@/lib/utils";

const stats = [
  {
    label: "Total Prompts",
    value: "1,284",
    change: "+12%",
    positive: true,
    icon: Zap,
    color: "text-blue-400",
    bg: "bg-blue-500/10",
    border: "border-blue-500/20",
  },
  {
    label: "Avg Quality Score",
    value: "87.4",
    change: "+5.2",
    positive: true,
    icon: Target,
    color: "text-green-400",
    bg: "bg-green-500/10",
    border: "border-green-500/20",
  },
  {
    label: "Total Cost",
    value: "$24.18",
    change: "-8%",
    positive: true,
    icon: DollarSign,
    color: "text-violet-400",
    bg: "bg-violet-500/10",
    border: "border-violet-500/20",
  },
  {
    label: "Avg Latency",
    value: "1.2s",
    change: "-0.3s",
    positive: true,
    icon: Clock,
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
    border: "border-cyan-500/20",
  },
  {
    label: "Success Rate",
    value: "99.2%",
    change: "+0.4%",
    positive: true,
    icon: TrendingUp,
    color: "text-orange-400",
    bg: "bg-orange-500/10",
    border: "border-orange-500/20",
  },
  {
    label: "Security Alerts",
    value: "0",
    change: "All clear",
    positive: true,
    icon: Shield,
    color: "text-emerald-400",
    bg: "bg-emerald-500/10",
    border: "border-emerald-500/20",
  },
];

export function StatsCards() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      {stats.map((stat, i) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.05 }}
          className={cn(
            "glass-card rounded-xl p-4 hover:border-primary/30 transition-all duration-300 group",
            "border",
            stat.border
          )}
        >
          <div
            className={cn(
              "w-9 h-9 rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform",
              stat.bg
            )}
          >
            <stat.icon className={cn("w-4 h-4", stat.color)} />
          </div>
          <p className="text-xl font-bold mb-0.5">{stat.value}</p>
          <p className="text-xs text-muted-foreground mb-1">{stat.label}</p>
          <p
            className={cn(
              "text-xs font-medium",
              stat.positive ? "text-green-400" : "text-red-400"
            )}
          >
            {stat.change}
          </p>
        </motion.div>
      ))}
    </div>
  );
}