from typing import Optional


class RACEFramework:
    """
    RACE Framework: Role, Action, Context, Explanation
    Role-based responses with structured instructions
    """

    NAME = "race"
    DESCRIPTION = "RACE Framework - Role, Action, Context, Explanation"

    SYSTEM_PROMPT = """You are PromptIO's RACE framework specialist. Transform the given prompt using the RACE framework:

**R - Role**: Define who the AI should be (expert, consultant, teacher, etc.)
**A - Action**: Specify exactly what action to take (analyze, create, explain, etc.)  
**C - Context**: Provide relevant background and situational information
**E - Explanation**: Define the expected format and depth of explanation

Return JSON:
{
  "optimized_prompt": "complete RACE-structured prompt",
  "improvements": ["improvements made"],
  "framework_data": {
    "role": "defined role for AI",
    "action": "specific action required",
    "context": "contextual information added",
    "explanation": "expected output format and depth",
    "role_expertise_level": "junior|senior|expert|master"
  },
  "optimization_score": 0.88
}"""

    def get_messages(self, original_prompt: str, **kwargs) -> list:
        user_msg = f"""Original Prompt to optimize using RACE Framework:
{original_prompt}

Apply the RACE framework:
- R (Role): What expert role should the AI assume?
- A (Action): What specific action should be taken?
- C (Context): What context is needed?
- E (Explanation): What format and depth of explanation is needed?

Build a complete, well-structured RACE prompt."""

        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ]