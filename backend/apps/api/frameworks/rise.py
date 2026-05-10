class RISEFramework:
    """
    RISE Framework: Role, Input, Steps, Execution
    Guided, step-by-step instructions or learning flows
    """

    NAME = "rise"
    DESCRIPTION = "RISE Framework - Role, Input, Steps, Execution"

    SYSTEM_PROMPT = """You are PromptIO's RISE framework specialist. Transform prompts using RISE:

**R - Role**: The expert role and perspective the AI should adopt
**I - Input**: The information, data, or context being provided as input
**S - Steps**: Explicit step-by-step breakdown of the process
**E - Execution**: How to execute each step with specific directives

Return JSON:
{
  "optimized_prompt": "complete RISE-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "role": "expert role defined",
    "input": "input specification",
    "steps": ["step 1", "step 2", "step 3"],
    "execution": "execution directives",
    "learning_flow": true,
    "difficulty_level": "beginner|intermediate|advanced|expert"
  },
  "optimization_score": 0.87
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using RISE Framework:
{original_prompt}

Apply RISE framework for guided step-by-step workflows:
R-Role, I-Input, S-Steps, E-Execution"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]