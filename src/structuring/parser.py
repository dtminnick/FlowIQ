
import re

class Parser:
    def parse(self, raw_output: str) -> list[dict]:
        """
        Parses raw LLM output into a list of structured step dictionaries.
        Expected format:
            1. Step text
            2. Step text
        """
        steps = []
        lines = raw_output.strip().split("\n")

        for line in lines:
            match = re.match(r"^\s*(\d+)\.\s*(.*)", line)
            if match:
                step_num = int(match.group(1))
                step_text = match.group(2).strip()
                steps.append({
                    "step_id": step_num,
                    "text": step_text
                })

        return steps
