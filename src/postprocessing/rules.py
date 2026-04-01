
class PostProcessor:
    def apply(self, steps: list[dict]) -> list[dict]:
        """
        Applies deterministic cleanup rules to corrected steps.
        Ensures sequential numbering, trims whitespace, and removes duplicates.
        """
        cleaned = []
        seen_texts = set()

        for step in steps:
            text = step["text"].strip()

            # Deduplicate based on text content
            if text.lower() in seen_texts:
                continue
            seen_texts.add(text.lower())

            cleaned.append({
                "step_id": step["step_id"],
                "text": text
            })

        # Reassign step IDs sequentially
        for i, step in enumerate(cleaned, start=1):
            step["step_id"] = i

        return cleaned
