import re
from typing import Dict, Any
from models.prompt import PromptFramework


class IntentClassifier:
    """
    Classifies user intent and suggests optimal framework
    Uses keyword matching + heuristics for fast classification
    """

    FRAMEWORK_SIGNALS = {
        PromptFramework.REASONING: [
            "analyze", "think", "reason", "solve", "logic", "proof",
            "why", "how does", "explain mathematically", "step by step",
            "complex", "multi-step", "deduce", "infer"
        ],
        PromptFramework.RACE: [
            "act as", "role", "you are a", "pretend", "expert",
            "consultant", "as a", "role-play", "persona"
        ],
        PromptFramework.CARE: [
            "practical", "real-world", "example", "help me",
            "everyday", "useful", "actionable", "workflow"
        ],
        PromptFramework.APE: [
            "complete", "execute", "perform", "deliver", "produce",
            "accomplish", "achieve", "task", "goal", "objective"
        ],
        PromptFramework.CREATE: [
            "create", "generate", "write", "build", "design",
            "develop", "craft", "compose", "make"
        ],
        PromptFramework.TAG: [
            "step", "process", "procedure", "how to", "tutorial",
            "guide", "instructions", "checklist"
        ],
        PromptFramework.CREO: [
            "strategy", "plan", "idea", "brainstorm", "approach",
            "solution", "framework", "method", "tackle"
        ],
        PromptFramework.RISE: [
            "learn", "teach", "educate", "course", "lesson",
            "training", "skill", "beginner", "guide me through"
        ],
        PromptFramework.PAIN: [
            "problem", "issue", "error", "bug", "fix", "broken",
            "trouble", "challenge", "difficulty", "stuck"
        ],
        PromptFramework.COAST: [
            "workflow", "process", "pipeline", "system", "automate",
            "orchestrate", "coordinate", "manage", "enterprise"
        ],
        PromptFramework.ROSES: [
            "scenario", "case study", "decision", "evaluate",
            "assess", "compare", "analyze situation", "recommend"
        ],
        PromptFramework.RESEE: [
            "deep dive", "immerse", "detailed role", "expert simulation",
            "comprehensive", "elaborate", "thorough", "in-depth"
        ],
    }

    COMPLEXITY_INDICATORS = {
        "simple": ["quick", "brief", "simple", "basic", "short"],
        "moderate": ["detailed", "explain", "describe", "help"],
        "complex": ["comprehensive", "enterprise", "advanced", "complex", "thorough"],
    }

    def classify_intent(self, prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        word_count = len(prompt.split())
        
        framework_scores: Dict[PromptFramework, int] = {}
        
        for framework, signals in self.FRAMEWORK_SIGNALS.items():
            score = sum(1 for signal in signals if signal in prompt_lower)
            if score > 0:
                framework_scores[framework] = score

        suggested_framework = PromptFramework.STANDARD
        if framework_scores:
            suggested_framework = max(framework_scores, key=lambda k: framework_scores[k])

        complexity = "simple"
        if word_count > 50:
            complexity = "complex"
        elif word_count > 20:
            complexity = "moderate"
            
        for level, indicators in self.COMPLEXITY_INDICATORS.items():
            if any(ind in prompt_lower for ind in indicators):
                complexity = level
                break

        return {
            "suggested_framework": suggested_framework,
            "framework_confidence": framework_scores.get(suggested_framework, 0),
            "complexity": complexity,
            "word_count": word_count,
            "has_role_requirement": any(
                s in prompt_lower for s in ["act as", "you are", "role"]
            ),
            "has_example_request": any(
                s in prompt_lower for s in ["example", "for instance", "such as"]
            ),
            "has_format_requirement": any(
                s in prompt_lower for s in ["list", "table", "json", "markdown", "format"]
            ),
            "domain": self._detect_domain(prompt_lower),
        }

    def _detect_domain(self, prompt_lower: str) -> str:
        domains = {
            "technology": ["code", "software", "programming", "api", "database", "system"],
            "business": ["revenue", "marketing", "sales", "strategy", "business", "roi"],
            "science": ["research", "scientific", "experiment", "hypothesis", "data"],
            "creative": ["story", "creative", "write", "poem", "fiction", "narrative"],
            "education": ["learn", "teach", "explain", "course", "education", "student"],
            "healthcare": ["medical", "health", "patient", "clinical", "diagnosis"],
            "legal": ["legal", "law", "contract", "compliance", "regulation"],
            "finance": ["financial", "investment", "budget", "accounting", "money"],
        }
        
        for domain, keywords in domains.items():
            if any(kw in prompt_lower for kw in keywords):
                return domain
        return "general"


intent_classifier = IntentClassifier()