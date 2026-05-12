"use client";

import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  BarChart3,
  Plus,
  Play,
  Trash2,
  ChevronRight,
  CheckCircle2,
  Clock,
  XCircle,
  Loader2,
  Search,
  Filter,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Skeleton } from "@/components/ui/skeleton";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "@/components/ui/dialog";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { evaluationsAPI } from "@/lib/api";
import { formatDateTime, formatRelativeTime, formatLatency, getScoreColor, getScoreLabel } from "@/lib/utils";
import { Evaluation } from "@/types";

const STATUS_CONFIG = {
  pending: { icon: Clock, color: "text-yellow-400", bg: "bg-yellow-500/10 border-yellow-500/30", label: "Pending" },
  running: { icon: Loader2, color: "text-blue-400", bg: "bg-blue-500/10 border-blue-500/30", label: "Running" },
  completed: { icon: CheckCircle2, color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/30", label: "Completed" },
  failed: { icon: XCircle, color: "text-red-400", bg: "bg-red-500/10 border-red-500/30", label: "Failed" },
};

export default function EvaluationsPage() {
  const queryClient = useQueryClient();
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [selectedEval, setSelectedEval] = useState<Evaluation | null>(null);
  const [newEvalOpen, setNewEvalOpen] = useState(false);

  const { data, isLoading } = useQuery({
    queryKey: ["evaluations", { statusFilter }],
    queryFn: () =>
      evaluationsAPI.list({
        status: statusFilter !== "all" ? statusFilter : undefined,
        limit: 50,
      }),
    staleTime: 30_000,
    refetchInterval: 15_000,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => evaluationsAPI.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["evaluations"] });
    },
  });

  const evaluations = data?.data || [];

  const filtered = evaluations.filter((e) =>
    e.prompt_title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 space-y-6 max-w-screen-2xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-2">
            <BarChart3 className="h-6 w-6 text-violet-400" />
            Evaluations
          </h1>
          <p className="text-gray-400 mt-1 text-sm">
            Benchmark and score your prompts across quality metrics.
          </p>
        </div>
        <Button onClick={() => setNewEvalOpen(true)} className="gap-2">
          <Plus className="h-4 w-4" />
          New Evaluation
        </Button>
      </div>

      {/* Summary Cards */}
      <EvaluationSummaryCards evaluations={evaluations} />

      {/* Filters */}
      <div className="flex gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search evaluations..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9"
          />
        </div>
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder="Status" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Status</SelectItem>
            <SelectItem value="completed">Completed</SelectItem>
            <SelectItem value="running">Running</SelectItem>
            <SelectItem value="pending">Pending</SelectItem>
            <SelectItem value="failed">Failed</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Evaluations List */}
      {isLoading ? (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => (
            <Card key={i}>
              <CardContent className="p-5">
                <div className="flex items-center gap-4">
                  <Skeleton className="h-10 w-10 rounded-lg" />
                  <div className="flex-1 space-y-2">
                    <Skeleton className="h-4 w-48" />
                    <Skeleton className="h-3 w-32" />
                  </div>
                  <Skeleton className="h-8 w-24 rounded-full" />
                  <Skeleton className="h-8 w-16" />
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      ) : filtered.length === 0 ? (
        <EvaluationEmptyState onNew={() => setNewEvalOpen(true)} />
      ) : (
        <div className="space-y-3">
          {filtered.map((evaluation) => (
            <EvaluationRow
              key={evaluation.id}
              evaluation={evaluation}
              onView={setSelectedEval}
              onDelete={(id) => deleteMutation.mutate(id)}
            />
          ))}
        </div>
      )}

      {/* Detail Dialog */}
      {selectedEval && (
        <EvaluationDetailDialog
          evaluation={selectedEval}
          onClose={() => setSelectedEval(null)}
        />
      )}

      {/* New Evaluation Dialog */}
      <NewEvaluationDialog
        open={newEvalOpen}
        onOpenChange={setNewEvalOpen}
        onSuccess={() => {
          queryClient.invalidateQueries({ queryKey: ["evaluations"] });
          setNewEvalOpen(false);
        }}
      />
    </div>
  );
}

function EvaluationSummaryCards({ evaluations }: { evaluations: Evaluation[] }) {
  const completed = evaluations.filter((e) => e.status === "completed");
  const running = evaluations.filter((e) => e.status === "running");
  const avgScore =
    completed.length > 0
      ? Math.round(
          completed.reduce((sum, e) => sum + (e.metrics?.overall_score || 0), 0) /
            completed.length
        )
      : 0;

  const cards = [
    { label: "Total", value: evaluations.length, color: "text-blue-400" },
    { label: "Completed", value: completed.length, color: "text-emerald-400" },
    { label: "Running", value: running.length, color: "text-yellow-400" },
    { label: "Avg Score", value: `${avgScore}`, color: getScoreColor(avgScore) },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => (
        <Card key={card.label}>
          <CardContent className="p-4">
            <p className="text-xs text-gray-400 mb-1">{card.label}</p>
            <p className={`text-2xl font-bold ${card.color}`}>{card.value}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

function EvaluationRow({
  evaluation,
  onView,
  onDelete,
}: {
  evaluation: Evaluation;
  onView: (e: Evaluation) => void;
  onDelete: (id: string) => void;
}) {
  const statusConfig = STATUS_CONFIG[evaluation.status];
  const StatusIcon = statusConfig.icon;

  return (
    <Card className="hover:border-white/20 transition-all duration-200 group">
      <CardContent className="p-4">
        <div className="flex items-center gap-4">
          {/* Status Icon */}
          <div className={`p-2 rounded-lg border ${statusConfig.bg}`}>
            <StatusIcon
              className={`h-5 w-5 ${statusConfig.color} ${
                evaluation.status === "running" ? "animate-spin" : ""
              }`}
            />
          </div>

          {/* Info */}
          <div className="flex-1 min-w-0">
            <p className="font-medium text-white text-sm truncate">{evaluation.prompt_title}</p>
            <div className="flex items-center gap-3 mt-1">
              <span className="text-xs text-gray-500">{evaluation.model}</span>
              <span className="text-gray-700">·</span>
              <span className="text-xs text-gray-500">
                {formatRelativeTime(evaluation.created_at)}
              </span>
            </div>
          </div>

          {/* Score */}
          {evaluation.status === "completed" && evaluation.metrics && (
            <div className="hidden md:flex items-center gap-4">
              <div className="text-center">
                <p className={`text-xl font-bold ${getScoreColor(evaluation.metrics.overall_score)}`}>
                  {evaluation.metrics.overall_score.toFixed(0)}
                </p>
                <p className="text-xs text-gray-500">Score</p>
              </div>
              <div className="text-center">
                <p className="text-sm font-medium text-white">
                  {formatLatency(evaluation.metrics.latency_ms)}
                </p>
                <p className="text-xs text-gray-500">Latency</p>
              </div>
            </div>
          )}

          {/* Status Badge */}
          <Badge
            variant={
              evaluation.status === "completed"
                ? "success"
                : evaluation.status === "failed"
                ? "destructive"
                : evaluation.status === "running"
                ? "default"
                : "warning"
            }
          >
            {statusConfig.label}
          </Badge>

          {/* Actions */}
          <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={() => onView(evaluation)}
              className="p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-white/10 transition-colors"
            >
              <ChevronRight className="h-4 w-4" />
            </button>
            <button
              onClick={() => onDelete(evaluation.id)}
              className="p-1.5 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition-colors"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Progress for running */}
        {evaluation.status === "running" && (
          <div className="mt-3">
            <Progress value={65} color="blue" size="sm" animated />
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function EvaluationDetailDialog({
  evaluation,
  onClose,
}: {
  evaluation: Evaluation;
  onClose: () => void;
}) {
  const metrics = evaluation.metrics;

  const metricItems = metrics
    ? [
        { label: "Relevance", value: metrics.relevance_score, color: "blue" as const },
        { label: "Accuracy", value: metrics.accuracy_score, color: "green" as const },
        { label: "Clarity", value: metrics.clarity_score, color: "purple" as const },
        { label: "Safety", value: metrics.safety_score, color: "yellow" as const },
        { label: "Reasoning Depth", value: metrics.reasoning_depth, color: "blue" as const },
        { label: "Cost Efficiency", value: metrics.cost_efficiency, color: "green" as const },
      ]
    : [];

  return (
    <Dialog open={true} onOpenChange={onClose}>
      <DialogContent onClose={onClose} className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Evaluation Details</DialogTitle>
          <p className="text-sm text-gray-400 mt-1">{evaluation.prompt_title}</p>
        </DialogHeader>
        <div className="p-6 space-y-6">
          {/* Overview */}
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-3 rounded-xl bg-white/5 border border-white/10">
              <p className={`text-3xl font-bold ${metrics ? getScoreColor(metrics.overall_score) : "text-gray-400"}`}>
                {metrics ? metrics.overall_score.toFixed(0) : "—"}
              </p>
              <p className="text-xs text-gray-500 mt-1">Overall Score</p>
              {metrics && <p className="text-xs text-gray-400">{getScoreLabel(metrics.overall_score)}</p>}
            </div>
            <div className="text-center p-3 rounded-xl bg-white/5 border border-white/10">
              <p className="text-3xl font-bold text-white">
                {metrics ? formatLatency(metrics.latency_ms) : "—"}
              </p>
              <p className="text-xs text-gray-500 mt-1">Latency</p>
            </div>
            <div className="text-center p-3 rounded-xl bg-white/5 border border-white/10">
              <p className="text-3xl font-bold text-white">
                {metrics ? `${(metrics.cost_efficiency * 100).toFixed(0)}%` : "—"}
              </p>
              <p className="text-xs text-gray-500 mt-1">Cost Efficiency</p>
            </div>
          </div>

          {/* Detailed Metrics */}
          {metrics && (
            <div className="space-y-4">
              <h4 className="text-sm font-semibold text-white">Detailed Scores</h4>
              <div className="grid grid-cols-2 gap-4">
                {metricItems.map((item) => (
                  <div key={item.label} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">{item.label}</span>
                      <span className="font-medium text-white">{item.value.toFixed(1)}/10</span>
                    </div>
                    <Progress value={item.value * 10} color={item.color} size="sm" />
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        <DialogFooter className="px-6 py-4 border-t border-border/50">
          <Button onClick={onClose} variant="secondary">Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function NewEvaluationDialog({
  open,
  onOpenChange,
  onSuccess,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: () => void;
}) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>New Evaluation</DialogTitle>
        </DialogHeader>
        <div className="p-4 py-6 space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Prompt</label>
            <Input placeholder="Select a prompt..." />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Model</label>
            <p className="text-xs text-muted-foreground">Uses configured backend model</p>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>Cancel</Button>
          <Button onClick={onSuccess}>Start Evaluation</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function EvaluationEmptyState({ onNew }: { onNew: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center py-24 text-center">
      <div className="h-16 w-16 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-4">
        <BarChart3 className="h-8 w-8 text-gray-600" />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">No evaluations found</h3>
      <p className="text-gray-400 text-sm mb-4 max-w-sm">
        Benchmark your prompts against different models to see how they perform.
      </p>
      <Button onClick={onNew} className="gap-2">
        <Plus className="h-4 w-4" />
        New Evaluation
      </Button>
    </div>
  );
}