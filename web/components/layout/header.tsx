"use client";

import { Menu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useUIStore } from "@/store/ui-store";
import { usePathname } from "next/navigation";

const pageTitles: Record<string, string> = {
  "/prompt-studio": "Prompt Studio",
  "/templates": "Templates",
};

export function Header() {
  const { toggleSidebar } = useUIStore();
  const pathname = usePathname();

  const title =
    Object.entries(pageTitles).find(([key]) =>
      pathname.startsWith(key)
    )?.[1] ?? "PromptIO";

  return (
    <header className="h-16 border-b border-border/50 bg-card/40 backdrop-blur-xl flex items-center px-4 gap-4 flex-shrink-0 sticky top-0 z-20">
      {/* Mobile menu */}
      <Button
        variant="ghost"
        size="icon"
        className="md:hidden"
        onClick={toggleSidebar}
      >
        <Menu className="w-5 h-5" />
      </Button>

      {/* Page title */}
      <h1 className="font-semibold text-foreground hidden md:block">
        {title}
      </h1>

    </header>
  );
}