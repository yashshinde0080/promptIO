"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Wand2, FileText, FlaskConical, Users, Download, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";

const actions = [
  {
    label: "New Prompt",
    description: "Open Prompt Studio",
    icon: Wand2,
    href: "/prompt-studio",
    color: "from-blue-500 to-violet-600",
    primary: true,
  },
  {
    label: "Browse Templates",
    description: "Use a pre-built template",
    icon: FileText,
    href: "/templates",
    color: "from-violet-500 to-purple-600",
  },
  {
    label: "Run Evaluation",
    description: "Score your prompts",
    icon: FlaskConical,
    href: "/evaluations",
    color: "from-cyan-500 to-blue-600",
  },
  {
    label: "Invite Team",
    description: "Collaborate with others",
    icon: Users,
    href: "/teams",
    color: "from-green-500 to-emerald-600",
  },
  {
    label: "Export Report",
    description: "Download PDF analytics",
    icon: Download,
    href: "/analytics",
    color: "from-orange-500 to-red-600",
  },
  {
    label: "Audit Log",
    description: "Review compliance trail",
    icon: Shield,
    href: "/admin",
    color: "from-pink-500 to-rose-600",
  },
];

export function QuickActions() {
  return (
    <div className="glass-card rounded-xl p-5">
      <h3 className="font-semibold mb-4">Quick Actions</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        {actions.map((action, i) => (
          <motion.div
            key={action.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
          >
            <Link href={action.href}>
              <div className="group p-4 rounded-xl border border-border/50 hover:border-primary/30 bg-muted/20 hover:bg-muted/40 transition-all duration-200 cursor-pointer text-center">
                <div
                  className={`w-10 h-10 rounded-xl bg-gradient-to-br ${action.color} flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform shadow-lg`}
                >
                  <action.icon className="w-5 h-5 text-white" />
                </div>
                <p className="text-sm font-medium">{action.label}</p>
                <p className="text-xs text-muted-foreground mt-0.5 hidden md:block">
                  {action.description}
                </p>
              </div>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  );
}