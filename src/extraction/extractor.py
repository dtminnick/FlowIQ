
from src.extraction.prompts import build_extraction_prompt
from src.extraction.llm_client import LLMClient

class Extractor:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.client = LLMClient(model_name)

    def extract(self, chunk: str) -> str:
        """Runs the extraction prompt and returns raw LLM output."""
        prompt = build_extraction_prompt(chunk)
        response = self.client.generate(prompt)
        return response
