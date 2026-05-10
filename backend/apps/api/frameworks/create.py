class CREATEFramework:
    """
    CREATE Framework: Character, Request, Examples, Adjustments, Type, Extras
    Clear, specific and guided task execution
    """

    NAME = "create"
    DESCRIPTION = "CREATE Framework - Character, Request, Examples, Adjustments, Type, Extras"

    SYSTEM_PROMPT = """You are PromptIO's CREATE framework specialist. Transform prompts using CREATE:

**C - Character**: The persona, role, or character the AI should embody
**R - Request**: The specific request or task in clear terms
**E - Examples**: Concrete examples of expected input/output
**A - Adjustments**: Fine-tuning instructions, constraints, and modifications
**T - Type**: The type of response format expected (essay, list, code, etc.)
**E - Extras**: Additional context, constraints, or special requirements

Return JSON:
{
  "optimized_prompt": "complete CREATE-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "character": "persona defined",
    "request": "clear request statement",
    "examples": ["example 1", "example 2"],
    "adjustments": ["adjustment 1", "adjustment 2"],
    "type": "response type",
    "extras": "additional requirements"
  },
  "optimization_score": 0.89
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using CREATE Framework:
{original_prompt}

Apply full CREATE framework with all six components:
C-Character, R-Request, E-Examples, A-Adjustments, T-Type, E-Extras"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]