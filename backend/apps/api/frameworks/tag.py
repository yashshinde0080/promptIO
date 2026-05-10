class TAGFramework:
    """
    TAG Framework: Task, Action, Goal
    Step-by-step tasks aimed at achieving a specific result
    """

    NAME = "tag"
    DESCRIPTION = "TAG Framework - Task, Action, Goal"

    SYSTEM_PROMPT = """You are PromptIO's TAG framework specialist. Transform prompts using TAG:

**T - Task**: The specific task to be accomplished with clear boundaries
**A - Action**: The concrete steps and actions to execute the task
**G - Goal**: The ultimate goal and measurable success criteria

Return JSON:
{
  "optimized_prompt": "complete TAG-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "task": "specific task defined",
    "action": "concrete steps listed",
    "goal": "ultimate goal and success criteria",
    "milestones": ["milestone 1", "milestone 2"],
    "measurable_outcomes": ["outcome 1", "outcome 2"]
  },
  "optimization_score": 0.85
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using TAG Framework:
{original_prompt}

Apply TAG framework:
- T (Task): What is the specific task?
- A (Action): What concrete steps are needed?
- G (Goal): What is the ultimate goal and how is success measured?"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]