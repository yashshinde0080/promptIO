"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { usePromptStore } from "@/store/prompt-store";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import {
  Copy,
  Check,
  Sparkles,
  AlertTriangle,
  CheckCircle2,
  Lightbulb,
} from "lucide-react";
import { getScoreBg, getScoreColor } from "@/lib/utils";
import ReactMarkdown from "react-markdown";

export function OutputPanel() {
  const { optimizedPrompt, analysis, lastResponse, isOptimizing } =
    usePromptStore();
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(optimizedPrompt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (isOptimizing) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-center p-8">
        <div className="w-14 h-14 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
        <div>
          <p className="font-medium">Optimizing your prompt...</p>
          <p className="text-sm text-muted-foreground mt-1">
            Applying {usePromptStore.getState().selectedFramework.toUpperCase()} framework
          </p>
        </div>
      </div>
    );
  }

  if (!optimizedPrompt) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-center p-8">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500/20 to-violet-500/20 border border-primary/20 flex items-center justify-center">
          <Sparkles className="w-8 h-8 text-primary" />
        </div>
        <div>
          <p className="font-medium">Optimized prompt appears here</p>
          <p className="text-sm text-muted-foreground mt-1 max-w-xs">
            Enter a prompt on the left, select a framework, and click
            Optimize.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border/50 flex-shrink-0">
        <div className="flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="font-medium text-sm">Optimized Result</span>
          {lastResponse && (
            <Badge
              variant="outline"
              className={`text-xs ${getScoreBg(analysis?.estimated_quality ?? 0)}`}
            >
              Score: {analysis?.estimated_quality ?? 0}
            </Badge>
          )}
        </div>
        <Button
          size="sm"
          variant="outline"
          className="h-7 text-xs gap-1.5 border-border/50"
          onClick={handleCopy}
        >
          {copied ? (
            <Check className="w-3 h-3 text-green-400" />
          ) : (
            <Copy className="w-3 h-3" />
          )}
          {copied ? "Copied!" : "Copy"}
        </Button>
      </div>

      {/* Output text */}
      <div className="flex-1 overflow-auto p-4">
        <AnimatePresence>
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-muted/20 rounded-lg p-4 border border-border/30 font-mono text-sm leading-relaxed whitespace-pre-wrap text-foreground/90"
          >
            {optimizedPrompt}
          </motion.div>
        </AnimatePresence>

        {/* Analysis breakdown */}
        {analysis && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="mt-4 space-y-4"
          >
            <div className="glass-card rounded-xl p-4 space-y-3">
              <h4 className="text-sm font-semibold">Quality Analysis</h4>
              {[
                {
                  label: "Clarity",
                  value: analysis.clarity_score,
                },
                {
                  label: "Specificity",
                  value: analysis.specificity_score,
                },
                {
                  label: "Safety",
                  value: analysis.safety_score,
                },
                {
                  label: "Complexity",
                  value: analysis.complexity_score,
                },
              ].map((metric) => (
                <div key={metric.label} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-muted-foreground">
                      {metric.label}
                    </span>
                    <span
                      className={getScoreColor(metric.value)}
                    >
                      {metric.value}
                    </span>
                  </div>
                  <Progress
                    value={metric.value}
                    className="h-1.5 bg-muted/50"
                  />
                </div>
              ))}
            </div>

            {/* Weaknesses */}
            {analysis.weaknesses?.length > 0 && (
              <div className="glass-card rounded-xl p-4">
                <div className="flex items-center gap-2 mb-3">
                  <AlertTriangle className="w-4 h-4 text-yellow-400" />
                  <h4 className="text-sm font-semibold">Detected Issues</h4>
                </div>
                <ul className="space-y-1.5">
                  {analysis.weaknesses.map((w, i) => (
                    <li
                      key={i}
                      className="text-xs text-muted-foreground flex items-start gap-2"
                    >
                      <span className="w-1.5 h-1.5 rounded-full bg-yellow-400 mt-1.5 flex-shrink-0" />
                      {w}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Suggestions */}
            {analysis.suggestions?.length > 0 && (
              <div className="glass-card rounded-xl p-4">
                <div className="flex items-center gap-2 mb-3">
                  <Lightbulb className="w-4 h-4 text-blue-400" />
                  <h4 className="text-sm font-semibold">Suggestions</h4>
                </div>
                <ul className="space-y-1.5">
                  {analysis.suggestions.map((s, i) => (
                    <li
                      key={i}
                      className="text-xs text-muted-foreground flex items-start gap-2"
                    >
                      <CheckCircle2 className="w-3.5 h-3.5 text-blue-400 mt-0.5 flex-shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Stats */}
            {lastResponse && (
              <div className="grid grid-cols-3 gap-2">
                {[
                  {
                    label: "Tokens",
                    value: lastResponse.tokens_used,
                  },
                  {
                    label: "Latency",
                    value: `${lastResponse.latency_ms}ms`,
                  },
                  {
                    label: "Cost",
                    value: `$${lastResponse.cost_usd.toFixed(4)}`,
                  },
                ].map((s) => (
                  <div
                    key={s.label}
                    className="glass-card rounded-lg p-2 text-center"
                  >
                    <p className="text-sm font-semibold">{s.value}</p>
                    <p className="text-xs text-muted-foreground">
                      {s.label}
                    </p>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        )}
      </div>
    </div>
  );
}