import { create } from "zustand";
import type {
  Prompt,
  PromptFramework,
  OptimizeResponse,
  PromptAnalysis,
} from "@/types";

interface PromptState {
  // Editor state
  currentPrompt: string;
  optimizedPrompt: string;
  selectedFramework: PromptFramework;
  isOptimizing: boolean;
  isStreaming: boolean;

  // Results
  lastResponse: OptimizeResponse | null;
  analysis: PromptAnalysis | null;

  // Saved prompts
  savedPrompts: Prompt[];
  activePromptId: string | null;

  // Actions
  setCurrentPrompt: (prompt: string) => void;
  setOptimizedPrompt: (prompt: string) => void;
  setSelectedFramework: (framework: PromptFramework) => void;
  setIsOptimizing: (val: boolean) => void;
  setIsStreaming: (val: boolean) => void;
  setLastResponse: (response: OptimizeResponse | null) => void;
  setAnalysis: (analysis: PromptAnalysis | null) => void;
  setSavedPrompts: (prompts: Prompt[]) => void;
  setActivePromptId: (id: string | null) => void;
  resetEditor: () => void;
}

export const usePromptStore = create<PromptState>((set) => ({
  currentPrompt: "",
  optimizedPrompt: "",
  selectedFramework: "standard",
  isOptimizing: false,
  isStreaming: false,
  lastResponse: null,
  analysis: null,
  savedPrompts: [],
  activePromptId: null,

  setCurrentPrompt: (currentPrompt) => set({ currentPrompt }),
  setOptimizedPrompt: (optimizedPrompt) => set({ optimizedPrompt }),
  setSelectedFramework: (selectedFramework) => set({ selectedFramework }),
  setIsOptimizing: (isOptimizing) => set({ isOptimizing }),
  setIsStreaming: (isStreaming) => set({ isStreaming }),
  setLastResponse: (lastResponse) => set({ lastResponse }),
  setAnalysis: (analysis) => set({ analysis }),
  setSavedPrompts: (savedPrompts) => set({ savedPrompts }),
  setActivePromptId: (activePromptId) => set({ activePromptId }),

  resetEditor: () =>
    set({
      currentPrompt: "",
      optimizedPrompt: "",
      lastResponse: null,
      analysis: null,
      activePromptId: null,
    }),
}));