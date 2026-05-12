"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import {
  Search,
  Library,
  Star,
  Zap,
  Filter,
  Grid,
  List,
  ArrowRight,
  Tag,
  TrendingUp,
} from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { templatesAPI } from "@/lib/apis";
import { getFrameworkColor, formatNumber, truncate } from "@/lib/utils";
import { TEMPLATE_CATEGORIES, PROMPT_FRAMEWORKS } from "@/lib/constants";
import { FRAMEWORK_META } from "@/types";
import { PromptTemplate, PromptFramework } from "@/types";
import { useRouter } from "next/navigation";

export default function TemplatesPage() {
  const router = useRouter();
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [framework, setFramework] = useState<string>("all");
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [featured, setFeatured] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ["templates", { search, category, framework, featured }],
    queryFn: () =>
      templatesAPI.list({
        search: search || undefined,
        category: category !== "All" ? category : undefined,
        framework: framework !== "all" ? framework : undefined,
        featured: featured || undefined,
        limit: 50,
      }),
    staleTime: 60_000,
  });

  const templates = data?.data || [];

  const handleUseTemplate = async (template: PromptTemplate) => {
    router.push(`/prompt-studio?template=${template.id}`);
  };

  return (
    <div className="p-6 space-y-6 max-w-screen-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <Library className="h-6 w-6 text-blue-400" />
            Templates
          </h1>
          <p className="text-gray-400 mt-1 text-sm">
            Pre-built prompts using proven frameworks. Start faster.
          </p>
        </div>
        <Button
          onClick={() => setFeatured(!featured)}
          variant={featured ? "default" : "outline"}
          size="sm"
          className="gap-2"
        >
          <Star className="h-4 w-4" />
          {featured ? "Showing Featured" : "Show Featured"}
        </Button>
      </div>

      {/* Filters */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search templates..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select value={category} onValueChange={setCategory}>
          <SelectTrigger className="w-full sm:w-48">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            {TEMPLATE_CATEGORIES.map((c) => (
              <SelectItem key={c} value={c}>{c}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={framework} onValueChange={setFramework}>
          <SelectTrigger className="w-full sm:w-48">
            <SelectValue placeholder="All Frameworks" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Frameworks</SelectItem>
            {PROMPT_FRAMEWORKS.map((f) => (
              <SelectItem key={f} value={f}>{FRAMEWORK_META[f].name}</SelectItem>
            ))}
          </SelectContent>
        </Select>
        <div className="flex border border-white/10 rounded-lg overflow-hidden">
          <button
            onClick={() => setViewMode("grid")}
            className={`p-2 transition-colors ${
              viewMode === "grid" ? "bg-blue-600/30 text-blue-400" : "text-gray-500 hover:text-gray-300"
            }`}
          >
            <Grid className="h-4 w-4" />
          </button>
          <button
            onClick={() => setViewMode("list")}
            className={`p-2 transition-colors ${
              viewMode === "list" ? "bg-blue-600/30 text-blue-400" : "text-gray-500 hover:text-gray-300"
            }`}
          >
            <List className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Framework Quick Filter */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-none">
        <button
          onClick={() => setFramework("all")}
          className={`shrink-0 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
            framework === "all"
              ? "bg-blue-600/30 border-blue-500/40 text-blue-300"
              : "border-white/10 text-gray-500 hover:text-gray-300 hover:border-white/20"
          }`}
        >
          All
        </button>
        {PROMPT_FRAMEWORKS.map((f) => (
          <button
            key={f}
            onClick={() => setFramework(f)}
            className={`shrink-0 px-3 py-1.5 rounded-full text-xs font-medium border transition-colors ${
              framework === f
                ? "bg-blue-600/30 border-blue-500/40 text-blue-300"
                : "border-white/10 text-gray-500 hover:text-gray-300 hover:border-white/20"
            }`}
          >
            {FRAMEWORK_META[f].name}
          </button>
        ))}
      </div>

      {/* Results Count */}
      {!isLoading && (
        <p className="text-sm text-gray-500">
          {templates.length} template{templates.length !== 1 ? "s" : ""} found
        </p>
      )}

      {/* Templates Grid/List */}
      {isLoading ? (
        <div
          className={
            viewMode === "grid"
              ? "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"
              : "space-y-3"
          }
        >
          {Array.from({ length: 9 }).map((_, i) => (
            <Card key={i}>
              <CardContent className="p-5 space-y-3">
                <Skeleton className="h-4 w-2/3" />
                <Skeleton className="h-3 w-full" />
                <Skeleton className="h-3 w-3/4" />
                <div className="flex gap-2">
                  <Skeleton className="h-6 w-16 rounded-full" />
                  <Skeleton className="h-6 w-20 rounded-full" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : templates.length === 0 ? (
        <EmptyState onClear={() => { setSearch(""); setCategory("All"); setFramework("all"); }} />
      ) : viewMode === "grid" ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {templates.map((template) => (
            <TemplateCard
              key={template.id}
              template={template}
              onUse={handleUseTemplate}
            />
          ))}
        </div>
      ) : (
        <div className="space-y-3">
          {templates.map((template) => (
            <TemplateListItem
              key={template.id}
              template={template}
              onUse={handleUseTemplate}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function TemplateCard({
  template,
  onUse,
}: {
  template: PromptTemplate;
  onUse: (t: PromptTemplate) => void;
}) {
  const frameworkMeta = FRAMEWORK_META[template.framework as PromptFramework];
  const colorClass = getFrameworkColor(template.framework as PromptFramework);

  return (
    <Card className="group hover:border-white/20 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/5">
      <CardContent className="p-5">
        {/* Header */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1.5">
              {template.is_featured && (
                <Star className="h-3.5 w-3.5 text-yellow-400 fill-yellow-400 shrink-0" />
              )}
              <span
                className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold border ${colorClass}`}
              >
                {frameworkMeta?.name || template.framework.toUpperCase()}
              </span>
            </div>
            <h3 className="font-semibold text-white text-sm group-hover:text-blue-300 transition-colors">
              {template.title}
            </h3>
          </div>
        </div>

        {/* Description */}
        <p className="text-xs text-gray-400 mb-4 line-clamp-2">
          {truncate(template.description, 120)}
        </p>

        {/* Tags */}
        <div className="flex flex-wrap gap-1.5 mb-4">
          {template.tags.slice(0, 3).map((tag) => (
            <span
              key={tag}
              className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs text-gray-500 bg-white/5 border border-white/10"
            >
              <Tag className="h-2.5 w-2.5" />
              {tag}
            </span>
          ))}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between pt-3 border-t border-white/10">
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <div className="flex items-center gap-1">
              <TrendingUp className="h-3.5 w-3.5" />
              <span>{formatNumber(template.use_count)} uses</span>
            </div>
            <div className="flex items-center gap-1">
              <Star className="h-3.5 w-3.5 text-yellow-400" />
              <span>{template.rating.toFixed(1)}</span>
            </div>
          </div>
          <Button
            size="sm"
            onClick={() => onUse(template)}
            className="h-7 text-xs gap-1"
          >
            Use <ArrowRight className="h-3 w-3" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function TemplateListItem({
  template,
  onUse,
}: {
  template: PromptTemplate;
  onUse: (t: PromptTemplate) => void;
}) {
  const frameworkMeta = FRAMEWORK_META[template.framework as PromptFramework];
  const colorClass = getFrameworkColor(template.framework as PromptFramework);

  return (
    <Card className="hover:border-white/20 transition-all duration-200">
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          {/* Framework Badge */}
          <span
            className={`shrink-0 inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border ${colorClass}`}
          >
            {frameworkMeta?.name || template.framework.toUpperCase()}
          </span>

          {/* Info */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="font-medium text-white text-sm truncate">{template.title}</h3>
              {template.is_featured && (
                <Star className="h-3.5 w-3.5 text-yellow-400 fill-yellow-400 shrink-0" />
              )}
            </div>
            <p className="text-xs text-gray-400 truncate">{template.description}</p>
          </div>

          {/* Stats */}
          <div className="hidden md:flex items-center gap-4 text-xs text-gray-500">
            <span>{formatNumber(template.use_count)} uses</span>
            <div className="flex items-center gap-1">
              <Star className="h-3 w-3 text-yellow-400" />
              <span>{template.rating.toFixed(1)}</span>
            </div>
          </div>

          {/* Action */}
          <Button size="sm" onClick={() => onUse(template)} className="shrink-0 gap-1">
            Use <ArrowRight className="h-3 w-3" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function EmptyState({ onClear }: { onClear: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <div className="h-16 w-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-4">
        <Library className="h-8 w-8 text-gray-600" />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">No templates found</h3>
      <p className="text-gray-400 text-sm mb-4 max-w-xs">
        Try adjusting your filters or search terms to find what you&apos;re looking for.
      </p>
      <Button variant="outline" size="sm" onClick={onClear}>
        Clear Filters
      </Button>
    </div>
  );
}