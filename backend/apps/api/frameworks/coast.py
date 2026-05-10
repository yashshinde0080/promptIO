class COASTFramework:
    """
    COAST Framework: Context, Objective, Actions, Scenario, Task
    For detailed workflows or process planning
    """

    NAME = "coast"
    DESCRIPTION = "COAST Framework - Context, Objective, Actions, Scenario, Task"

    SYSTEM_PROMPT = """You are PromptIO's COAST framework specialist. Transform prompts using COAST:

**C - Context**: Comprehensive background and environmental context
**O - Objective**: Clear, measurable objectives and goals
**A - Actions**: Specific actions with owners, timelines, and dependencies
**S - Scenario**: The specific scenario or situation being addressed
**T - Task**: The concrete task with deliverables and acceptance criteria

Return JSON:
{
  "optimized_prompt": "complete COAST-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "context": "comprehensive context",
    "objective": "measurable objectives",
    "actions": ["action 1", "action 2"],
    "scenario": "specific scenario",
    "task": "concrete task with deliverables",
    "workflow_complexity": "simple|moderate|complex|enterprise",
    "estimated_steps": 5
  },
  "optimization_score": 0.89
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using COAST Framework:
{original_prompt}

Apply COAST framework for detailed process workflows:
C-Context, O-Objective, A-Actions, S-Scenario, T-Task"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]