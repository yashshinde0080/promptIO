import { Metadata } from "next";
import { PromptStudioLayout } from "@/components/prompt-studio/prompt-editor";

export const metadata: Metadata = { title: "Prompt Studio - PromptIO" };

export default function PromptStudioPage() {
  return <PromptStudioLayout />;
}