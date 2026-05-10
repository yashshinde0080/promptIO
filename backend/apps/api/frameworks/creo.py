class CREOFramework:
    """
    CREO Framework: Context, Request, Explanation, Outcome
    Structured ideas, strategies, or problem-solving
    """

    NAME = "creo"
    DESCRIPTION = "CREO Framework - Context, Request, Explanation, Outcome"

    SYSTEM_PROMPT = """You are PromptIO's CREO framework specialist. Transform prompts using CREO:

**C - Context**: The situational context, background and relevant environment
**R - Request**: The specific request with precision and clarity  
**E - Explanation**: Detailed explanation of requirements, rationale, and constraints
**O - Outcome**: The desired outcome with measurable success criteria

Return JSON:
{
  "optimized_prompt": "complete CREO-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "context": "detailed context established",
    "request": "precise request stated",
    "explanation": "detailed explanation and rationale",
    "outcome": "desired outcome with metrics",
    "strategy_type": "analytical|creative|tactical|strategic"
  },
  "optimization_score": 0.88
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using CREO Framework:
{original_prompt}

Apply CREO framework for strategic structured outputs:
C-Context, R-Request, E-Explanation, O-Outcome"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]