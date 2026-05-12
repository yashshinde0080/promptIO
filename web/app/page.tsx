"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { PROMPT_FRAMEWORKS } from "@/lib/constants";
import { FRAMEWORK_META } from "@/types/indes";
import {
  ArrowRight,
  Zap,
  Shield,
  BarChart3,
  Users,
  Sparkles,
  CheckCircle2,
} from "lucide-react";

const features = [
  {
    icon: Sparkles,
    title: "13 Optimization Frameworks",
    description:
      "RACE, CARE, APE, CREATE, COAST, ROSES and more. Each framework engineered for specific AI tasks.",
    color: "text-blue-400",
    bg: "bg-blue-500/10",
  },
  {
    icon: Zap,
    title: "Multi-Model Routing",
    description:
      "Intelligent routing across GPT-4o, Claude, Gemini, Llama, Mistral via OpenRouter.",
    color: "text-violet-400",
    bg: "bg-violet-500/10",
  },
  {
    icon: Shield,
    title: "Enterprise Compliance",
    description:
      "GDPR, FedRAMP, GovRAMP ready. PII masking, audit trails, prompt injection detection.",
    color: "text-green-400",
    bg: "bg-green-500/10",
  },
  {
    icon: BarChart3,
    title: "Evaluation Engine",
    description:
      "Score prompts on relevance, accuracy, safety, reasoning depth, cost, and latency.",
    color: "text-cyan-400",
    bg: "bg-cyan-500/10",
  },
  {
    icon: Users,
    title: "Team Collaboration",
    description:
      "Role-based access, shared prompt libraries, version control, and approval workflows.",
    color: "text-orange-400",
    bg: "bg-orange-500/10",
  },
  {
    icon: BarChart3,
    title: "Rich Analytics",
    description:
      "Cost per team, token usage, model comparison, failure patterns, PDF reports.",
    color: "text-pink-400",
    bg: "bg-pink-500/10",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background grid-bg overflow-hidden">
      {/* Nav */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass-card border-b border-border/50">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center shadow-md shadow-primary/20">
              <Zap className="w-4 h-4 text-primary-foreground fill-current" />
            </div>
            <span className="font-bold text-lg text-gradient-primary">
              PromptIO
            </span>
          </div>
          <div className="hidden md:flex items-center gap-6 text-sm text-muted-foreground">
            <Link href="#features" className="hover:text-foreground transition-colors">
              Features
            </Link>
            <Link href="#frameworks" className="hover:text-foreground transition-colors">
              Frameworks
            </Link>
            <Link href="#pricing" className="hover:text-foreground transition-colors">
              Pricing
            </Link>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/auth/login">
              <Button variant="ghost" size="sm">
                Sign in
              </Button>
            </Link>
            <Link href="/auth/register">
              <Button size="sm" className="btn-primary-glow">
                Get started free
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 px-6 relative">
        {/* Glow effects */}
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute top-40 left-1/3 w-64 h-64 bg-secondary/10 rounded-full blur-3xl pointer-events-none" />

        <div className="max-w-5xl mx-auto text-center relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Badge
              variant="outline"
              className="mb-6 border-primary/30 text-primary bg-primary/10"
            >
              <Sparkles className="w-3 h-3 mr-1" />
              Enterprise-Grade Prompt Engineering
            </Badge>

            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              <span className="text-foreground">The Prompt IDE</span>
              <br />
              <span className="text-gradient-primary">Built for Scale</span>
            </h1>

            <p className="text-xl text-muted-foreground max-w-3xl mx-auto mb-10 leading-relaxed">
              PromptIO transforms raw prompts into precision-engineered
              instructions using 13 frameworks, multi-model routing, team
              collaboration, and enterprise compliance — all in one platform.
            </p>

            <div className="flex justify-center gap-4 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-300">
            <Link href="/auth/login">
              <Button size="lg" className="h-12 px-8 text-base shadow-[0_0_40px_-10px_rgba(255,255,255,0.3)] hover:shadow-[0_0_60px_-15px_rgba(255,255,255,0.5)] transition-all">
                  Start optimizing free
                  <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
              <Link href="/prompt-studio">
                <Button
                  size="lg"
                  variant="outline"
                  className="border-border/50 text-base px-8"
                >
                  View demo
                </Button>
              </Link>
            </div>
          </motion.div>

          {/* Stats bar */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4, duration: 0.6 }}
            className="mt-16 grid grid-cols-2 md:grid-cols-4 gap-4"
          >
            {[
              { label: "Frameworks", value: "13" },
              { label: "AI Models", value: "8+" },
              { label: "Avg Improvement", value: "80%" },
              { label: "Uptime", value: "99.9%" },
            ].map((stat) => (
              <div
                key={stat.label}
                className="glass-card rounded-xl p-4 text-center"
              >
                <div className="text-3xl font-bold text-gradient-primary">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground mt-1">
                  {stat.label}
                </div>
              </div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              Everything You Need for
              <span className="text-gradient-primary"> Serious Prompt Work</span>
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Not another prompt wrapper. A full engineering platform for teams
              that treat prompts as production assets.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="glass-card rounded-xl p-6 hover:border-primary/30 transition-all duration-300 group"
              >
                <div
                  className={`w-12 h-12 ${feature.bg} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}
                >
                  <feature.icon className={`w-6 h-6 ${feature.color}`} />
                </div>
                <h3 className="font-semibold text-lg mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Frameworks Grid */}
      <section id="frameworks" className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">
              13 Optimization
              <span className="text-gradient-violet"> Frameworks</span>
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Every prompt has a purpose. Choose the framework that matches your
              task.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {PROMPT_FRAMEWORKS.map((fwId, i) => {
              const fw = FRAMEWORK_META[fwId];
              return (
              <motion.div
                key={fw.id}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.05 }}
                className="glass-card rounded-xl p-4 hover:border-primary/30 transition-all duration-300 group cursor-pointer"
              >
                <div className="flex items-center gap-3 mb-3">
                  <div className={`p-2 rounded-lg bg-${fw.color}-500/10 text-${fw.color}-500 font-bold`}>
                    {fw.id.substring(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <div className="font-semibold text-sm">{fw.name}</div>
                    <Badge
                      variant="outline"
                      className={`text-xs mt-0.5 border-${fw.color}-500/30 text-${fw.color}-400`}
                    >
                      {fw.id.toUpperCase()}
                    </Badge>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {fw.useCase}
                </p>
                <div className="mt-3 flex flex-wrap gap-1">
                  {fw.components.slice(0, 3).map((c) => (
                    <span
                      key={c}
                      className="text-xs bg-muted/50 text-muted-foreground px-2 py-0.5 rounded"
                    >
                      {c}
                    </span>
                  ))}
                  {fw.components.length > 3 && (
                    <span className="text-xs text-muted-foreground px-1">
                      +{fw.components.length - 3}
                    </span>
                  )}
                </div>
              </motion.div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="glass-card rounded-2xl p-12 glow-blue">
            <h2 className="text-4xl font-bold mb-4">
              Ready to Engineer
              <span className="text-gradient-primary"> Better Prompts?</span>
            </h2>
            <p className="text-muted-foreground text-lg mb-8 max-w-2xl mx-auto">
              Join teams who ship production-grade AI workflows with PromptIO.
              No credit card required.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
              <Link href="/auth/register">
                <Button size="lg" className="btn-primary-glow gap-2 px-8">
                  <Zap className="w-4 h-4" />
                  Start for free
                </Button>
              </Link>
            </div>
            <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
              {["No credit card required", "GDPR compliant", "99.9% uptime"].map(
                (item) => (
                  <div key={item} className="flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-green-400" />
                    {item}
                  </div>
                )
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-8 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-blue-500 to-violet-600 flex items-center justify-center">
              <Zap className="w-3 h-3 text-white" />
            </div>
            <span className="font-bold text-sm text-gradient-primary">
              PromptIO
            </span>
          </div>
          <p className="text-xs text-muted-foreground">
            © 2025 PromptIO. Enterprise-grade prompt engineering platform.
          </p>
          <div className="flex gap-4 text-xs text-muted-foreground">
            <Link href="#" className="hover:text-foreground transition-colors">
              Privacy
            </Link>
            <Link href="#" className="hover:text-foreground transition-colors">
              Terms
            </Link>
            <Link href="#" className="hover:text-foreground transition-colors">
              Docs
            </Link>
          </div>
        </div>
      </footer>
    </div>
  );
}