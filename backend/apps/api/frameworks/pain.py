class PAINFramework:
    """
    PAIN Framework: Problem, Action, Information, Next Steps
    Solving problems or getting action-oriented information
    """

    NAME = "pain"
    DESCRIPTION = "PAIN Framework - Problem, Action, Information, Next Steps"

    SYSTEM_PROMPT = """You are PromptIO's PAIN framework specialist. Transform prompts using PAIN:

**P - Problem**: Clear identification and definition of the problem
**A - Action**: Immediate actions to address or investigate the problem
**I - Information**: Critical information needed to solve the problem
**N - Next Steps**: Concrete next steps and actionable recommendations

Return JSON:
{
  "optimized_prompt": "complete PAIN-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "problem": "problem clearly defined",
    "action": "immediate actions specified",
    "information": "required information listed",
    "next_steps": ["step 1", "step 2", "step 3"],
    "urgency": "critical|high|medium|low",
    "problem_category": "technical|business|personal|analytical"
  },
  "optimization_score": 0.86
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using PAIN Framework:
{original_prompt}

Apply PAIN framework for problem-solving:
P-Problem, A-Action, I-Information, N-Next Steps"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]