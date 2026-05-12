"use client";

import { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { usePromptStore } from "@/store/prompt-store";
import { usePrompt } from "@/hooks/use-prompt";
import { FrameworkSelector } from "./framework-selector";
import { ModelSelector } from "./model-selector";
import { TokenCounter } from "./token-counter";
import { OutputPanel } from "./output-panel";
import { VersionHistory } from "./version-history";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Wand2,
  Save,
  RotateCcw,
  ChevronDown,
  Layers,
  GitBranch,
  Sliders,
  Play,
} from "lucide-react";
import { FRAMEWORKS } from "@/lib/constants";
import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function PromptStudioLayout() {
  const {
    currentPrompt,
    setCurrentPrompt,
    selectedFramework,
    resetEditor,
    isOptimizing,
  } = usePromptStore();
  const { optimize, savePrompt } = usePrompt();
  const [saveTitle, setSaveTitle] = useState("");
  const [saveOpen, setSaveOpen] = useState(false);

  const framework = FRAMEWORKS.find((f) => f.id === selectedFramework);

  const handleSave = async () => {
    if (!saveTitle.trim()) {
      toast.error("Please enter a title");
      return;
    }
    await savePrompt(saveTitle);
    setSaveOpen(false);
    setSaveTitle("");
  