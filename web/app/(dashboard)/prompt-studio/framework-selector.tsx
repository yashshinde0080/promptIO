"use client";

import { motion } from "framer-motion";
import { FRAMEWORKS } from "@/lib/constants";
import { usePromptStore } from "@/store/prompt-store";
import { cn } from "@/lib/utils";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { PromptFramework } from "@/types";

export function FrameworkSelector() {
  const { selectedFramework, setSelectedFramework } = usePromptStore();

  return (
    <div className="space-y-2">
      <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider px-1">
        Framework
      </p>
      <ScrollArea className="h-[calc(100vh-280px)]">
        <div className="space-y-1 pr-2">
          {FRAMEWORKS.map((fw) => (
            <motion.button
              key={fw.id}
              onClick={() =>
                setSelectedFramework(fw.id as PromptFramework)
              }
              whileHover={{ x: 2 }}
              className={cn(
                "w-full text-left p-3 rounded-lg border transition-all duration-200 group",
                selectedFramework === fw.id
                  ? `${fw.accentColor} border-current`
                  : "border-transparent hover:border-border/50 hover:bg-muted/30"
              )}
            >
              <div className="flex items-center gap-2.5">
                <span className="text-base">{fw.icon}</span>
                <div className="min-w-0">
                  <div className="flex items-center gap-1.5">
                    <span className="text-xs font-semibold">{fw.name}</span>
                  </div>
                  <p className="text-xs text-muted-foreground truncate mt-0.5 leading-relaxed">
                    {fw.useCase}
                  </p>
                </div>
              </div>
              {selectedFramework === fw.id && (
                <div className="mt-2 flex flex-wrap gap-1">
                  {fw.components.map((c) => (
                    <span
                      key={c}
                      className="text-xs bg-current/10 px-1.5 py-0.5 rounded text-current opacity-80"
                    >
                      {c}
                    </span>
                  ))}
                </div>
              )}
            </motion.button>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}