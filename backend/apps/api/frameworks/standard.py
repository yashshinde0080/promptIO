from typing import Dict, Any, Optional


class StandardFramework:
    """
    Standard Prompt Framework
    For general use prompt generation - optimizes prompts 
    for clarity, specificity, and actionability
    """

    NAME = "standard"
    DESCRIPTION = "General purpose optimized prompt generation"

    SYSTEM_PROMPT = """You are PromptIO's expert prompt engineer. Your task is to optimize the given prompt for maximum clarity, 
effectiveness, and actionability. Apply best practices in prompt engineering including:

1. Clear instruction specification
2. Appropriate context provision  
3. Output format definition
4. Constraint specification
5. Example inclusion where helpful
6. Tone and style consistency

Return a JSON response with this exact structure:
{
  "optimized_prompt": "the improved prompt text",
  "improvements": ["list", "of", "improvements", "made"],
  "framework_data": {
    "intent": "detected user intent",
    "complexity": "simple|moderate|complex",
    "domain": "detected domain",
    "output_format": "detected/suggested output format"
  },
  "optimization_score": 0.85
}"""

    def build_user_message(
        self,
        original_prompt: str,
        context: Optional[str] = None,
        target_audience: Optional[str] = None,
        tone: Optional[str] = None,
        additional_instructions: Optional[str] = None,
    ) -> str:
        parts = [f"Original Prompt:\n{original_prompt}"]

        if context:
            parts.append(f"\nContext: {context}")
        if target_audience:
            parts.append(f"\nTarget Audience: {target_audience}")
        if tone:
            parts.append(f"\nDesired Tone: {tone}")
        if additional_instructions:
            parts.append(f"\nAdditional Instructions: {additional_instructions}")

        parts.append("\nPlease optimize this prompt following the Standard framework.")
        return "\n".join(parts)

    def get_messages(
        self, original_prompt: str, **kwargs
    ) -> list:
        return [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": self.build_user_message(original_prompt, **kwargs)},
        ]