// ============================================================
// PromptIO - Global Type Definitions
// ============================================================

export type UserRole = "admin" | "manager" | "prompt_engineer" | "analyst" | "viewer";

export type PromptFramework =
  | "standard"
  | "reasoning"
  | "race"
  | "care"
  | "ape"
  | "create"
  | "tag"
  | "creo"
  | "rise"
  | "pain"
  | "coast"
  | "roses"
  | "resee";

export type PromptVisibility = "private" | "team" | "organization" | "public";

// Model is configured server-side via OPENROUTER_DEFAULT_MODEL env var.
// No client-side model enumeration needed.
export type AIModel = string;

export type ComplianceMode = "standard" | "gdpr" | "fedramp" | "govramp";

export type OrganizationPlan = "free" | "pro" | "enterprise";

// ============================================================
// User & Auth Types
// ============================================================

export interface User {
  id: string;
  name: string;
  email: string;
  role: UserRole;
  organization_id: string;
  avatar_url?: string;
  created_at: string;
  updated_at: string;
}

export interface Organization {
  id: string;
  name: string;
  plan: OrganizationPlan;
  compliance_mode: ComplianceMode;
  member_count: number;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  name: string;
  email: string;
  password: string;
  organization_name?: string;
}

// ============================================================
// Prompt Types
// ============================================================

export interface Prompt {
  id: string;
  title: string;
  content: string;
  optimized_content?: string;
  framework: PromptFramework;
  version: number;
  owner_id: string;
  organization_id: string;
  visibility: PromptVisibility;
  tags: string[];
  token_count?: number;
  is_starred: boolean;
  created_at: string;
  updated_at: string;
}

export interface PromptVersion {
  id: string;
  prompt_id: string;
  version: number;
  content: string;
  optimized_content?: string;
  change_summary: string;
  created_by: string;
  created_at: string;
}

export interface PromptTemplate {
  id: string;
  title: string;
  description: string;
  framework: PromptFramework;
  content: string;
  category: string;
  tags: string[];
  use_count: number;
  rating: number;
  is_featured: boolean;
  created_by: string;
  created_at: string;
}

export interface OptimizeRequest {
  prompt: string;
  framework: PromptFramework;
  model?: AIModel;
  context?: string;
  constraints?: string[];
  temperature?: number;
}

export interface OptimizeResponse {
  original_prompt: string;
  optimized_prompt: string;
  framework: PromptFramework;
  model_used: AIModel;
  provider?: string;
  improvement_score: number;
  token_count: {
    original: number;
    optimized: number;
  };
  analysis: PromptAnalysis;
  execution_time_ms: number;
  cost_usd: number;
}

export interface PromptAnalysis {
  clarity_score: number;
  specificity_score: number;
  complexity_score: number;
  safety_score: number;
  intent: string;
  weaknesses: string[];
  improvements: string[];
  suggestions?: string[];
  estimated_quality?: number;
  framework_match: number;
}

// ============================================================
// Evaluation Types
// ============================================================

export interface Evaluation {
  id: string;
  prompt_id: string;
  prompt_title: string;
  model: AIModel;
  metrics: EvaluationMetrics;
  status: "pending" | "running" | "completed" | "failed";
  created_at: string;
  completed_at?: string;
}

export interface EvaluationMetrics {
  relevance_score: number;
  accuracy_score: number;
  clarity_score: number;
  safety_score: number;
  reasoning_depth: number;
  cost_efficiency: number;
  latency_ms: number;
  token_cost: number;
  overall_score: number;
}

export interface AIRun {
  id: string;
  prompt_id: string;
  model: AIModel;
  response: string;
  latency_ms: number;
  cost_usd: number;
  token_input: number;
  token_output: number;
  status: "success" | "error" | "timeout";
  created_at: string;
}

// ============================================================
// Analytics Types
// ============================================================

export interface AnalyticsOverview {
  total_prompts: number;
  total_optimizations: number;
  total_cost_usd: number;
  avg_improvement_score: number;
  total_tokens_used: number;
  active_users: number;
  period: string;
}

export interface AnalyticsSummary {
  total_prompts: number;
  total_runs: number;
  total_cost_usd: number;
  avg_latency_ms: number;
  avg_quality_score: number;
  framework_distribution: Array<{ framework: string; count: number }>;
  daily_runs: Array<{ date: string; runs: number; cost: number }>;
  success_rate: number;
  period_days: number;
}

export interface UsageDataPoint {
  date: string;
  prompts: number;
  optimizations: number;
  cost: number;
  tokens: number;
}

export interface ModelUsageStat {
  model: string;
  usage_count: number;
  total_cost: number;
  avg_latency: number;
  success_rate: number;
}

export interface FrameworkUsageStat {
  framework: PromptFramework;
  usage_count: number;
  avg_improvement: number;
  success_rate: number;
}

export interface CostBreakdown {
  model: string;
  cost: number;
  percentage: number;
  color: string;
}

export interface PerformanceMetric {
  label: string;
  value: number;
  change: number;
  change_type: "increase" | "decrease" | "neutral";
  unit: string;
}

// ============================================================
// Team Types
// ============================================================

export interface TeamMember {
  id: string;
  user_id: string;
  name: string;
  email: string;
  role: UserRole;
  avatar_url?: string;
  joined_at: string;
  last_active: string;
  prompt_count: number;
  is_active: boolean;
}

export interface TeamInvitation {
  id: string;
  email: string;
  role: UserRole;
  invited_by: string;
  status: "pending" | "accepted" | "expired";
  created_at: string;
  expires_at: string;
}

// ============================================================
// Activity & Audit Types
// ============================================================

export interface ActivityItem {
  id: string;
  user_id: string;
  user_name: string;
  user_avatar?: string;
  action: string;
  resource_type: "prompt" | "evaluation" | "team" | "settings" | "api";
  resource_id?: string;
  resource_name?: string;
  metadata?: Record<string, unknown>;
  created_at: string;
}

export interface AuditLog {
  id: string;
  user_id: string;
  user_name: string;
  action: string;
  resource_type: string;
  resource_id: string;
  ip_address: string;
  user_agent: string;
  status: "success" | "failure";
  created_at: string;
}

// ============================================================
// Settings Types
// ============================================================

export interface UserSettings {
  notifications: {
    email_optimizations: boolean;
    email_team_activity: boolean;
    email_weekly_report: boolean;
    browser_notifications: boolean;
  };
  preferences: {
    default_framework: PromptFramework;
    default_model: AIModel;
    theme: "dark" | "light" | "system";
    editor_font_size: number;
    auto_save: boolean;
  };
  privacy: {
    profile_visibility: "public" | "team" | "private";
    activity_visible: boolean;
  };
}

export interface APIKey {
  id: string;
  name: string;
  key_preview: string;
  permissions: string[];
  last_used?: string;
  created_at: string;
  expires_at?: string;
}

// ============================================================
// UI State Types
// ============================================================

export interface ToastMessage {
  id: string;
  title: string;
  description?: string;
  variant: "default" | "destructive" | "success" | "warning";
  duration?: number;
}

export interface SidebarItem {
  label: string;
  href: string;
  icon: string;
  badge?: number | string;
  roles?: UserRole[];
}

export interface TableColumn<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}

// ============================================================
// API Response Types
// ============================================================

export interface APIResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
  total_pages: number;
}

export interface APIError {
  message: string;
  code: string;
  status: number;
  details?: Record<string, string[]>;
}

// ============================================================
// Framework Metadata
// ============================================================

export interface FrameworkMeta {
  id: PromptFramework;
  name: string;
  fullName: string;
  description: string;
  components: string[];
  useCase: string;
  color: string;
  icon: string;
}

export const FRAMEWORK_META: Record<PromptFramework, FrameworkMeta> = {
  standard: {
    id: "standard",
    name: "Standard",
    fullName: "Standard Prompt",
    description: "General use optimized prompt generation",
    components: ["Input", "Context", "Output"],
    useCase: "General purpose AI interactions",
    color: "blue",
    icon: "Zap",
  },
  reasoning: {
    id: "reasoning",
    name: "Reasoning",
    fullName: "Reasoning Prompt",
    description: "Multi-step reasoning and complex problem solving",
    components: ["Problem", "Steps", "Reasoning", "Conclusion"],
    useCase: "Complex analytical tasks",
    color: "purple",
    icon: "Brain",
  },
  race: {
    id: "race",
    name: "RACE",
    fullName: "RACE Framework",
    description: "Role, Action, Context, Explanation",
    components: ["Role", "Action", "Context", "Explanation"],
    useCase: "Role-based structured responses",
    color: "red",
    icon: "Flag",
  },
  care: {
    id: "care",
    name: "CARE",
    fullName: "CARE Framework",
    description: "Context, Action, Result, Example",
    components: ["Context", "Action", "Result", "Example"],
    useCase: "Practical real-world responses",
    color: "green",
    icon: "Heart",
  },
  ape: {
    id: "ape",
    name: "APE",
    fullName: "APE Framework",
    description: "Action, Purpose, Execution",
    components: ["Action", "Purpose", "Execution"],
    useCase: "Clear task execution",
    color: "orange",
    icon: "Target",
  },
  create: {
    id: "create",
    name: "CREATE",
    fullName: "CREATE Framework",
    description: "Character, Request, Examples, Adjustments, Type, Extras",
    components: ["Character", "Request", "Examples", "Adjustments", "Type", "Extras"],
    useCase: "Advanced guided task execution",
    color: "pink",
    icon: "Wand2",
  },
  tag: {
    id: "tag",
    name: "TAG",
    fullName: "TAG Framework",
    description: "Task, Action, Goal",
    components: ["Task", "Action", "Goal"],
    useCase: "Step-by-step goal achievement",
    color: "cyan",
    icon: "Tag",
  },
  creo: {
    id: "creo",
    name: "CREO",
    fullName: "CREO Framework",
    description: "Context, Request, Explanation, Outcome",
    components: ["Context", "Request", "Explanation", "Outcome"],
    useCase: "Strategic structured outputs",
    color: "violet",
    icon: "Lightbulb",
  },
  rise: {
    id: "rise",
    name: "RISE",
    fullName: "RISE Framework",
    description: "Role, Input, Steps, Execution",
    components: ["Role", "Input", "Steps", "Execution"],
    useCase: "Guided learning workflows",
    color: "yellow",
    icon: "TrendingUp",
  },
  pain: {
    id: "pain",
    name: "PAIN",
    fullName: "PAIN Framework",
    description: "Problem, Action, Information, Next Steps",
    components: ["Problem", "Action", "Information", "Next Steps"],
    useCase: "Problem-solving prompts",
    color: "rose",
    icon: "AlertTriangle",
  },
  coast: {
    id: "coast",
    name: "COAST",
    fullName: "COAST Framework",
    description: "Context, Objective, Actions, Scenario, Task",
    components: ["Context", "Objective", "Actions", "Scenario", "Task"],
    useCase: "Detailed workflow planning",
    color: "teal",
    icon: "Anchor",
  },
  roses: {
    id: "roses",
    name: "ROSES",
    fullName: "ROSES Framework",
    description: "Role, Objective, Scenario, Expected Solution, Steps",
    components: ["Role", "Objective", "Scenario", "Expected Solution", "Steps"],
    useCase: "Scenario-based decision making",
    color: "fuchsia",
    icon: "Flower2",
  },
  resee: {
    id: "resee",
    name: "RESEE",
    fullName: "RESEE Framework",
    description: "Role, Elaboration, Scenario, Elaboration, Examples",
    components: ["Role", "Elaboration of Role", "Scenario", "Elaboration of Scenario", "Examples"],
    useCase: "Deep role simulation",
    color: "indigo",
    icon: "Users",
  },
};
