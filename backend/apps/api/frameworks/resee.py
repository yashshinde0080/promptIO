class RESEEFramework:
    """
    RESEE Framework: Role, Elaboration of role, Scenario, 
    Elaboration of Scenario, Examples
    For deep role-based work
    """

    NAME = "resee"
    DESCRIPTION = "RESEE Framework - Role, Elaboration, Scenario, Elaboration, Examples"

    SYSTEM_PROMPT = """You are PromptIO's RESEE framework specialist. Transform prompts using RESEE:

**R - Role**: The specific role to be adopted
**E - Elaboration of Role**: Detailed description of role expertise, background, and capabilities
**S - Scenario**: The specific scenario or situation
**E - Elaboration of Scenario**: Deep dive into scenario details, nuances, and complexities
**E - Examples**: Rich, concrete examples demonstrating expected behavior in this role+scenario

Return JSON:
{
  "optimized_prompt": "complete RESEE-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "role": "role name",
    "role_elaboration": "detailed role description with expertise and background",
    "scenario": "scenario overview",
    "scenario_elaboration": "deep scenario details and complexities",
    "examples": ["detailed example 1", "detailed example 2"],
    "immersion_depth": "surface|moderate|deep|expert",
    "domain_specificity": "general|specialized|highly-specialized"
  },
  "optimization_score": 0.92
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using RESEE Framework:
{original_prompt}

Apply RESEE framework for deep role simulation:
R-Role, E-Elaboration of Role, S-Scenario, E-Elaboration of Scenario, E-Examples

Make the role deeply immersive with rich contextual examples."""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]