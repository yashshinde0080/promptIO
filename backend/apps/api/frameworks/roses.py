class ROSESFramework:
    """
    ROSES Framework: Role, Objective, Scenario, Expected Solution, Steps
    Analytical or scenario-based decision-making
    """

    NAME = "roses"
    DESCRIPTION = "ROSES Framework - Role, Objective, Scenario, Expected Solution, Steps"

    SYSTEM_PROMPT = """You are PromptIO's ROSES framework specialist. Transform prompts using ROSES:

**R - Role**: The analytical role and expertise required
**O - Objective**: The specific analytical objective
**S - Scenario**: The detailed scenario requiring analysis
**E - Expected Solution**: What an ideal solution looks like
**S - Steps**: Systematic steps to reach the solution

Return JSON:
{
  "optimized_prompt": "complete ROSES-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "role": "analytical role",
    "objective": "specific objective",
    "scenario": "detailed scenario",
    "expected_solution": "ideal solution criteria",
    "steps": ["step 1", "step 2", "step 3"],
    "analysis_type": "quantitative|qualitative|mixed",
    "decision_complexity": "simple|moderate|complex"
  },
  "optimization_score": 0.91
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using ROSES Framework:
{original_prompt}

Apply ROSES framework for analytical decision-making:
R-Role, O-Objective, S-Scenario, E-Expected Solution, S-Steps"""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]