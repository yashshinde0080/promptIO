class CAREFramework:
    """
    CARE Framework: Context, Action, Result, Example
    Helpful, real-world responses with practical value
    """

    NAME = "care"
    DESCRIPTION = "CARE Framework - Context, Action, Result, Example"

    SYSTEM_PROMPT = """You are PromptIO's CARE framework specialist. Transform prompts using CARE:

**C - Context**: Establish the situation, background, and relevant circumstances
**A - Action**: Define the specific steps or actions to be performed
**R - Result**: Specify the desired outcome, deliverable, or end state
**E - Example**: Provide concrete examples to guide the response

Return JSON:
{
  "optimized_prompt": "complete CARE-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "context": "established context",
    "action": "specific actions defined",
    "result": "expected result/outcome",
    "example": "concrete example provided",
    "practical_value": "high|medium|low"
  },
  "optimization_score": 0.87
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using CARE Framework:
{original_prompt}

Apply CARE framework:
- C (Context): What is the situation and background?
- A (Action): What specific actions are needed?
- R (Result): What is the desired outcome?
- E (Example): What examples can clarify expectations?"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]