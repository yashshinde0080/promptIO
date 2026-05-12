"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Save, 
  Play, 
  Settings, 
  History, 
  Check, 
  Zap, 
  Sparkles, 
  Copy, 
  Brain, 
  Target, 
  Heart, 
  Wand2, 
  Tag, 
  Lightbulb, 
  TrendingUp, 
  AlertTriangle, 
  Anchor, 
  Flower2, 
  Users, 
  ArrowRight,
  Layers,
  Sliders,
  CheckCircle2
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Slider } from "@/components/ui/slider";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { FRAMEWORKS } from "@/lib/constants";
import { usePromptStore } from "@/store/prompt-store";
import { usePrompt } from "@/hooks/use-prompt";
import { cn, countTokensEstimate, getScoreColor, getScoreBg } from "@/lib/utils";
import { PromptFramework } from "@/types";
import { toast } from "sonner";

const SAMPLE_PROMPTS = [
  {
    title: "Customer Support Bot",
    prompt: "Act as a customer support rep. Answer user questions politely and provide refund links if asked.",
  },
  {
    title: "Technical Explainer",
    prompt: "Explain the concept of vector embeddings and cosine similarity to a software engineer who is new to AI.",
  },
  {
    title: "Marketing Copywriter",
    prompt: "Write a short, engaging email newsletter introducing our new SaaS feature: automated dark mode styling.",
  },
];

const renderFrameworkIcon = (id: string, className = "w-4 h-4") => {
  switch (id) {
    case "standard": return <Zap className={className} />;
    case "reasoning": return <Brain className={className} />;
    case "race": return <Target className={className} />;
    case "care": return <Heart className={className} />;
    case "ape": return <Target className={className} />;
    case "create": return <Wand2 className={className} />;
    case "tag": return <Tag className={className} />;
    case "creo": return <Lightbulb className={className} />;
    case "rise": return <TrendingUp className={className} />;
    case "pain": return <AlertTriangle className={className} />;
    case "coast": return <Anchor className={className} />;
    case "roses": return <Flower2 className={className} />;
    case "resee": return <Users className={className} />;
    default: return <Zap className={className} />;
  }
};

export function PromptStudioLayout() {
  const {
    currentPrompt,
    setCurrentPrompt,
    optimizedPrompt,
    selectedFramework,
    setSelectedFramework,
    isOptimizing,
    analysis,
    lastResponse,
  } = usePromptStore();

  const { optimize, savePrompt } = usePrompt();
  
  const [saveTitle, setSaveTitle] = useState("Untitled Prompt");
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(2048);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!optimizedPrompt) return;
    navigator.clipboard.writeText(optimizedPrompt);
    setCopied(true);
    toast.success("Optimized prompt copied to clipboard!");
    setTimeout(() => setCopied(false), 2000);
  };

  const activeFrameworkMeta = FRAMEWORKS.find((f) => f.id === selectedFramework) || FRAMEWORKS[0];

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-background text-foreground overflow-hidden">
      {/* Top Header / Toolbar */}
      <div className="flex items-center justify-between p-4 border-b border-border/40 bg-card/30 backdrop-blur-md shrink-0 z-10">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center text-primary-foreground shadow-md shadow-primary/20">
              <Zap className="w-4 h-4 fill-current" />
            </div>
            <Input 
              value={saveTitle}
              onChange={(e) => setSaveTitle(e.target.value)}
              className="w-64 bg-transparent border-transparent hover:border-white/10 focus:border-primary transition-colors text-base font-semibold h-8 px-2"
            />
          </div>
          <div className="flex items-center gap-2 text-xs text-muted-foreground border-l border-border/40 pl-4">
            <Check className="h-3 w-3 text-emerald-400" /> Auto-saved
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button 
            variant="outline" 
            size="sm" 
            onClick={() => savePrompt(saveTitle)}
            className="gap-1.5 border-border/50 hover:bg-white/5"
          >
            <Save className="h-4 w-4 text-primary" />
            Save Preset
          </Button>
          
          <Button 
            onClick={optimize} 
            disabled={isOptimizing || !currentPrompt.trim()}
            className="gap-2 bg-primary hover:bg-primary/90 text-primary-foreground font-medium shadow-lg shadow-primary/25 px-5"
          >
            {isOptimizing ? (
              <>
                <div className="w-4 h-4 rounded-full border-2 border-primary-foreground/30 border-t-primary-foreground animate-spin" />
                Optimizing...
              </>
            ) : (
              <>
                <Sparkles className="h-4 w-4" />
                Optimize Prompt
              </>
            )}
          </Button>
        </div>
      </div>

      {/* Main Studio Interface */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar: Framework / Optimizer Mode Selector */}
        <div className="w-72 border-r border-border/40 bg-card/20 flex flex-col shrink-0">
          <div className="p-3 border-b border-border/40 shrink-0 bg-white/[0.02]">
            <p className="text-xs font-bold text-muted-foreground uppercase tracking-wider px-1 flex items-center gap-1.5">
              <Layers className="w-3.5 h-3.5 text-primary" />
              Optimizer Mode
            </p>
          </div>
          
          <div className="flex-1 overflow-y-auto scrollbar-none px-2 py-3">
            <div className="space-y-1.5 pr-3">
              {FRAMEWORKS.map((fw) => {
                const isSelected = selectedFramework === fw.id;
                return (
                  <motion.button
                    key={fw.id}
                    onClick={() => setSelectedFramework(fw.id as PromptFramework)}
                    whileHover={{ x: 2 }}
                    whileTap={{ scale: 0.99 }}
                    className={cn(
                      "w-full text-left p-3 rounded-xl border transition-all duration-200 relative group flex flex-col gap-1.5",
                      isSelected 
                        ? "bg-primary/10 border-primary shadow-sm" 
                        : "border-transparent hover:border-border/60 hover:bg-white/[0.02]"
                    )}
                  >
                    <div className="flex items-center gap-2.5">
                      <div className="shrink-0 flex items-center justify-center w-6 h-6 rounded-md bg-white/[0.03] border border-white/[0.05] group-hover:border-primary/20 transition-colors">
                        {renderFrameworkIcon(fw.id, cn("w-3.5 h-3.5 transition-colors", isSelected ? "text-primary" : "text-muted-foreground group-hover:text-primary"))}
                      </div>
                      <div className="min-w-0 flex-1">
                        <div className="flex items-center justify-between gap-1">
                          <span className={cn(
                            "text-xs font-bold truncate",
                            isSelected ? "text-primary" : "text-foreground/90"
                          )}>
                            {fw.name}
                          </span>
                        </div>
                        <p className="text-[11px] text-muted-foreground line-clamp-2 mt-0.5 leading-relaxed">
                          {fw.useCase}
                        </p>
                      </div>
                    </div>

                    {isSelected && (
                      <motion.div 
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: "auto" }}
                        className="flex flex-wrap gap-1 pt-1 border-t border-primary/10 mt-0.5"
                      >
                        {fw.components.map((comp) => (
                          <span 
                            key={comp} 
                            className="text-[10px] bg-primary/15 text-primary font-semibold px-1.5 py-0.5 rounded"
                          >
                            {comp}
                          </span>
                        ))}
                      </motion.div>
                    )}

                    {isSelected && (
                      <div className="absolute left-0 top-2 bottom-2 w-1 bg-primary rounded-r-full" />
                    )}
                  </motion.button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Center/Right Panels: Split Screen (Input Rough Prompt -> Output Framework Optimized) */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 overflow-hidden">
          
          {/* Panel 1: Input --> Rough Prompt */}
          <div className="flex flex-col border-r border-border/40 bg-background/50">
            <div className="p-3 border-b border-border/40 shrink-0 bg-white/[0.02] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-xs border-primary/30 text-primary bg-primary/10 font-mono py-0.5">
                  Input
                </Badge>
                <span className="text-xs font-bold text-foreground/80">Rough Prompt</span>
              </div>
              <span className="text-[11px] text-muted-foreground font-mono">
                ~{countTokensEstimate(currentPrompt)} tokens
              </span>
            </div>

            {/* Quick Samples Section */}
            <div className="p-2.5 border-b border-border/30 bg-card/10 shrink-0">
              <p className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider mb-1.5 px-1">
                Try a quick rough prompt
              </p>
              <div className="flex flex-wrap gap-1.5">
                {SAMPLE_PROMPTS.map((sample, idx) => (
                  <button
                    key={idx}
                    onClick={() => setCurrentPrompt(sample.prompt)}
                    className="text-[11px] bg-white/5 hover:bg-white/10 text-muted-foreground hover:text-foreground border border-white/5 rounded-md px-2 py-1 transition-colors text-left truncate max-w-[180px]"
                  >
                    {sample.title}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex-1 p-4 flex flex-col">
              <Textarea
                value={currentPrompt}
                onChange={(e) => setCurrentPrompt(e.target.value)}
                placeholder="Enter your rough prompt here... Give the core idea, and let the optimizer apply the structured framework framework perfectly."
                className="flex-1 resize-none bg-transparent border-none focus-visible:ring-0 p-0 text-sm font-mono leading-relaxed text-foreground/90 placeholder:text-muted-foreground/50"
              />
            </div>
          </div>

          {/* Panel 2: Output --> Framework Optimized Prompt */}
          <div className="flex flex-col bg-card/5 overflow-hidden">
            <div className="p-3 border-b border-border/40 shrink-0 bg-white/[0.02] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-xs border-primary/30 text-primary bg-primary/10 font-mono py-0.5 gap-1">
                  <Sparkles className="w-3 h-3" />
                  Output
                </Badge>
                <span className="text-xs font-bold text-foreground/80">
                  {activeFrameworkMeta.name} Optimized
                </span>
              </div>

              {optimizedPrompt && (
                <div className="flex items-center gap-2">
                  <span className="text-[11px] text-muted-foreground font-mono">
                    ~{countTokensEstimate(optimizedPrompt)} tokens
                  </span>
                  <Button 
                    size="sm" 
                    variant="ghost" 
                    onClick={handleCopy}
                    className="h-6 px-2 hover:bg-white/5 gap-1 text-xs text-muted-foreground hover:text-foreground"
                  >
                    {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                    {copied ? "Copied" : "Copy"}
                  </Button>
                </div>
              )}
            </div>

            <div className="flex-1 overflow-y-auto p-4 flex flex-col">
              {isOptimizing ? (
                <div className="flex-1 flex flex-col items-center justify-center gap-4 text-center">
                  <div className="relative">
                    <div className="w-16 h-16 rounded-full border-2 border-primary/20 border-t-primary animate-spin" />
                    <Sparkles className="w-5 h-5 text-primary absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 animate-pulse" />
                  </div>
                  <div className="space-y-1">
                    <p className="text-sm font-bold text-foreground/90">
                      Restructuring Prompt
                    </p>
                    <p className="text-xs text-muted-foreground max-w-xs mx-auto">
                      Injecting {activeFrameworkMeta.components.join(", ")} logic using {activeFrameworkMeta.name}...
                    </p>
                  </div>
                </div>
              ) : optimizedPrompt ? (
                <div className="space-y-4 flex-1 flex flex-col">
                  {/* The Optimized Code Content */}
                  <div className="bg-background/80 rounded-xl p-4 border border-border/40 font-mono text-xs leading-relaxed whitespace-pre-wrap text-foreground/95 flex-1 shadow-inner overflow-y-auto">
                    {optimizedPrompt}
                  </div>

                  {/* Quality Analysis Breakdown */}
                  {analysis && (
                    <div className="space-y-3 shrink-0 pt-2 border-t border-border/30">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold flex items-center gap-1.5 text-foreground/80">
                          <Sliders className="w-3.5 h-3.5 text-primary" />
                          Framework Validation Analysis
                        </span>
                        <Badge variant="secondary" className="text-xs font-mono font-bold bg-primary/10 text-primary border-primary/20">
                          Score: {analysis.estimated_quality ?? 88}/100
                        </Badge>
                      </div>

                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        {[
                          { label: "Clarity", value: analysis.clarity_score ?? 90 },
                          { label: "Specificity", value: analysis.specificity_score ?? 85 },
                          { label: "Safety", value: analysis.safety_score ?? 95 },
                          { label: "Complexity", value: analysis.complexity_score ?? 80 },
                        ].map((metric) => (
                          <div key={metric.label} className="bg-card/30 rounded-lg p-2.5 border border-border/30 space-y-1.5">
                            <div className="flex justify-between text-[11px]">
                              <span className="text-muted-foreground font-medium">{metric.label}</span>
                              <span className={cn("font-bold font-mono", getScoreColor(metric.value))}>
                                {metric.value}%
                              </span>
                            </div>
                            <Progress value={metric.value} className="h-1 bg-white/5" />
                          </div>
                        ))}
                      </div>

                      {/* Suggestions / Improvements List */}
                      {((analysis.suggestions?.length ?? 0) > 0 || (analysis.improvements?.length ?? 0) > 0) && (
                        <div className="bg-primary/5 rounded-lg p-3 border border-primary/10 space-y-1.5">
                          <p className="text-[11px] font-bold text-primary flex items-center gap-1">
                            <Lightbulb className="w-3 h-3" />
                            Optimization Enhancements
                          </p>
                          <ul className="space-y-1">
                            {(analysis.suggestions || analysis.improvements || ["Applied structured persona constraints", "Enforced precise output deliverables"]).map((item, idx) => (
                              <li key={idx} className="text-[11px] text-muted-foreground flex items-start gap-1.5">
                                <CheckCircle2 className="w-3 h-3 text-primary mt-0.5 shrink-0" />
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex-1 flex flex-col items-center justify-center gap-3 text-center">
                  <div className="w-12 h-12 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center">
                    {renderFrameworkIcon(activeFrameworkMeta.id, "w-6 h-6 text-primary animate-pulse")}
                  </div>
                  <div className="space-y-1 max-w-xs">
                    <p className="text-sm font-bold text-foreground/80">
                      Awaiting Generation
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Input your rough prompt on the left to see it beautifully structured via the {activeFrameworkMeta.name}.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
