from typing import Optional


class ReasoningFramework:
    """
    Reasoning Prompt Framework
    For reasoning tasks and complex problem solving
    Structures prompts to elicit step-by-step logical thinking
    """

    NAME = "reasoning"
    DESCRIPTION = "Multi-step reasoning and complex problem solving"

    SYSTEM_PROMPT = """You are PromptIO's reasoning optimization specialist. Transform the given prompt into a 
structured reasoning prompt that elicits systematic, logical, step-by-step thinking.

Apply Chain-of-Thought (CoT) and Tree-of-Thought (ToT) principles:
1. Break complex problems into sub-problems
2. Require explicit reasoning steps
3. Add verification checkpoints  
4. Include self-correction mechanisms
5. Specify the reasoning format expected
6. Add "Let's think step by step" style directives

Return JSON:
{
  "optimized_prompt": "enhanced reasoning prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "problem_type": "logical|mathematical|analytical|creative|ethical",
    "reasoning_depth": "surface|moderate|deep",
    "steps_required": 5,
    "verification_points": ["checkpoint 1", "checkpoint 2"],
    "chain_of_thought_applied": true
  },
  "optimization_score": 0.90
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize for Reasoning:
{original_prompt}

Transform this into a structured reasoning prompt that forces the AI to think systematically.
Include explicit reasoning steps, verification checkpoints, and self-correction directives."""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]