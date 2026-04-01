
class LLMClient:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        """Placeholder LLM call."""
        # TODO: integrate actual LLM API
        return "1. Placeholder step extracted from text."
