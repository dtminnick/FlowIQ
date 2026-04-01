
from src.extraction.llm_client import LLMClient

class Corrector:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.client = LLMClient(model_name)

    def refine(self, steps: list[dict], issues: dict) -> list[dict]:
        """
        Uses an LLM to correct issues in extracted steps.
        Returns a new list of improved step dictionaries.
        """
        prompt = self._build_prompt(steps, issues)
        response = self.client.generate(prompt)
        return self._parse_response(response)

    def _build_prompt(self, steps: list[dict], issues: dict]) -> str:
        return f"""
You are an AI system that corrects procedural steps.

Here are the extracted steps:
{steps}

Here are the issues detected:
{issues}

Fix the issues. Return a clean, numbered list of corrected steps.
"""

    def _parse_response(self, response: str) -> list[dict]:
        """
        Very simple parser for corrected steps.
        Reuses the same numbered-list pattern as the main parser.
        """
        import re
        corrected = []
        lines = response.strip().split("\n")

        for line in lines:
            match = re.match(r"^\s*(\d+)\.\s*(.*)", line)
            if match:
                corrected.append({
                    "step_id": int(match.group(1)),
                    "text": match.group(2).strip()
                })

        return corrected
