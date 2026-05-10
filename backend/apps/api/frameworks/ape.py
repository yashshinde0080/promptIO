class APEFramework:
    """
    APE Framework: Action, Purpose, Execution
    Clear task execution with defined goals and outcomes
    """

    NAME = "ape"
    DESCRIPTION = "APE Framework - Action, Purpose, Execution"

    SYSTEM_PROMPT = """You are PromptIO's APE framework specialist. Transform prompts using APE:

**A - Action**: The specific task or directive to complete
**P - Purpose**: The why behind the task - goals and objectives
**E - Execution**: How the task should be carried out - methodology and steps

Return JSON:
{
  "optimized_prompt": "complete APE-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "action": "specific task defined",
    "purpose": "goal and objectives clarified",
    "execution": "methodology and approach defined",
    "success_criteria": ["criterion 1", "criterion 2"],
    "output_format": "expected output format"
  },
  "optimization_score": 0.86
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using APE Framework:
{original_prompt}

Apply APE framework:
- A (Action): What specific task needs to be done?
- P (Purpose): Why is this being done? What are the goals?
- E (Execution): How should it be executed? What methodology?"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]