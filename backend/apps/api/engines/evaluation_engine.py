import asyncio
import time
from typing import Dict, Any, Optional
import structlog
from engines.safety_engine import safety_engine

logger = structlog.get_logger(__name__)


class EvaluationEngine:
    """
    Multi-dimensional prompt evaluation engine
    Scores prompts across 7 key dimensions
    """

    EVALUATION_SYSTEM_PROMPT = """You are an expert prompt quality evaluator. Evaluate the given prompt across these dimensions:

1. **Relevance** (0-1): How well the prompt addresses the intended task
2. **Clarity** (0-1): How clear and unambiguous the instructions are
3. **Specificity** (0-1): How specific and precise the requirements are
4. **Completeness** (0-1): How complete the context and instructions are
5. **Safety** (0-1): How safe and appropriate the prompt is
6. **Reasoning_Depth** (0-1): How well it elicits deep thinking
7. **Actionability** (0-1): How actionable and executable the instructions are

Also evaluate:
- **Hallucination_Risk** (0-1): Likelihood of generating false information
- **Ambiguity_Score** (0-1): Level of ambiguity (lower is better)
- **Complexity_Score** (0-1): Task complexity (not quality)

Return JSON only:
{
  "relevance": 0.85,
  "clarity": 0.90,
  "specificity": 0.75,
  "completeness": 0.80,
  "safety": 0.95,
  "reasoning_depth": 0.70,
  "actionability": 0.85,
  "hallucination_risk": 0.15,
  "ambiguity_score": 0.20,
  "complexity_score": 0.60,
  "strengths": ["Clear role definition", "Good context provision"],
  "weaknesses": ["Missing output format", "Vague constraints"],
  "suggestions": ["Add specific output format", "Define success criteria"],
  "detailed_feedback": "Brief overall assessment"
}"""

    async def evaluate_prompt(
        self,
        prompt_content: str,
        ai_router_service=None,
        model: Optional[str] = None,
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        try:
            safety_results = safety_engine.analyze(prompt_content)
            
            evaluation_result = {
                "relevance_score": 0.0,
                "clarity_score": 0.0,
                "specificity_score": 0.0,
                "completeness_score": 0.0,
                "safety_score": safety_results["safety_score"],
                "reasoning_depth_score": 0.0,
                "actionability_score": 0.0,
                "hallucination_risk": 0.0,
                "ambiguity_score": 0.0,
                "complexity_score": 0.0,
                "overall_quality_score": 0.0,
                "strengths": [],
                "weaknesses": [],
                "suggestions": [],
                "detailed_feedback": "",
                "pii_detected": safety_results["pii_detected"],
                "compliance_issues": safety_results["compliance_flags"],
            }

            if ai_router_service:
                try:
                    response = await ai_router_service.chat_completion(
                        messages=[
                            {"role": "system", "content": self.EVALUATION_SYSTEM_PROMPT},
                            {"role": "user", "content": f"Evaluate this prompt:\n\n{prompt_content}"},
                        ],
                        model=model or "openai/gpt-4o-mini",
                        response_format={"type": "json_object"},
                    )

                    import json
                    ai_eval = json.loads(response["content"])
                    
                    evaluation_result.update({
                        "relevance_score": ai_eval.get("relevance", 0.0),
                        "clarity_score": ai_eval.get("clarity", 0.0),
                        "specificity_score": ai_eval.get("specificity", 0.0),
                        "completeness_score": ai_eval.get("completeness", 0.0),
                        "reasoning_depth_score": ai_eval.get("reasoning_depth", 0.0),
                        "actionability_score": ai_eval.get("actionability", 0.0),
                        "hallucination_risk": ai_eval.get("hallucination_risk", 0.0),
                        "ambiguity_score": ai_eval.get("ambiguity_score", 0.0),
                        "complexity_score": ai_eval.get("complexity_score", 0.0),
                        "strengths": ai_eval.get("strengths", []),
                        "weaknesses": ai_eval.get("weaknesses", []),
                        "suggestions": ai_eval.get("suggestions", []),
                        "detailed_feedback": ai_eval.get("detailed_feedback", ""),
                    })

                    scores = [
                        evaluation_result["relevance_score"] * 0.2,
                        evaluation_result["clarity_score"] * 0.2,
                        evaluation_result["specificity_score"] * 0.15,
                        evaluation_result["completeness_score"] * 0.15,
                        evaluation_result["safety_score"] * 0.15,
                        evaluation_result["reasoning_depth_score"] * 0.1,
                        evaluation_result["actionability_score"] * 0.05,
                    ]
                    evaluation_result["overall_quality_score"] = sum(scores)

                except Exception as e:
                    logger.error("AI evaluation failed", error=str(e))
                    evaluation_result["overall_quality_score"] = safety_results["safety_score"] * 0.5
            else:
                score = self._heuristic_evaluation(prompt_content)
                evaluation_result.update(score)

            evaluation_result["latency_ms"] = (time.time() - start_time) * 1000
            return evaluation_result

        except Exception as e:
            logger.error("Evaluation engine error", error=str(e))
            raise

    def _heuristic_evaluation(self, prompt: str) -> Dict[str, Any]:
        words = len(prompt.split())
        has_context = any(w in prompt.lower() for w in ["context", "background", "given"])
        has_format = any(w in prompt.lower() for w in ["format", "list", "json", "table"])
        has_examples = any(w in prompt.lower() for w in ["example", "for instance", "such as"])
        has_constraints = any(w in prompt.lower() for w in ["must", "should", "require", "limit"])
        
        specificity = min(1.0, words / 100)
        clarity = 0.7 if words > 20 else 0.4
        completeness = sum([has_context, has_format, has_examples, has_constraints]) * 0.25

        overall = (specificity + clarity + completeness) / 3

        return {
            "relevance_score": 0.7,
            "clarity_score": clarity,
            "specificity_score": specificity,
            "completeness_score": completeness,
            "reasoning_depth_score": 0.5,
            "actionability_score": 0.6,
            "hallucination_risk": 0.3,
            "ambiguity_score": 1 - clarity,
            "complexity_score": min(1.0, words / 150),
            "overall_quality_score": overall,
            "strengths": ["Prompt submitted"],
            "weaknesses": ["Run AI evaluation for detailed feedback"],
            "suggestions": ["Use the full evaluation service for detailed analysis"],
            "detailed_feedback": "Heuristic evaluation. Enable AI evaluation for detailed scoring.",
        }


evaluation_engine = EvaluationEngine()