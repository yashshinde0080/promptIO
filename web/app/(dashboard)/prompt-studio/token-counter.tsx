"use client";

import { usePromptStore } from "@/store/prompt-store";
import { estimateTokens } from "@/lib/utils";
import { Progress } from "@/components/ui/progress";
import { cn } from "@/lib/utils";

export function TokenCounter() {
  const { currentPrompt } = usePromptStore();
  const tokens = estimateTokens(currentPrompt);
  const maxTokens = 4096;
  const percentage = Math.min((tokens / maxTokens) * 100, 100);

  const getColor = () => {
    if (percentage < 60) return "text-green-400";
    if (percentage < 80) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="space-y-1.5">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
          Tokens
        </p>
        <span className={cn("text-xs font-mono font-medium", getColor())}>
          {tokens.toLocaleString()} / {maxTokens.toLocaleString()}
        </span>
      </div>
      <Progress
        value={percentage}
        className="h-1.5 bg-muted/50"
      />
      <p className="text-xs text-muted-foreground">
        ~${((tokens / 1000) * 0.002).toFixed(4)} est. cost
      </p>
    </div>
  );
}