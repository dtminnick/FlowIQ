
class Validator:
    def validate(self, steps: list[dict]) -> dict:
        """
        Validates a list of step dictionaries.
        Returns a dictionary of issues found.
        """
        issues = {
            "missing_step_ids": [],
            "empty_text": [],
            "non_actionable": []
        }

        for step in steps:
            step_id = step.get("step_id")
            text = step.get("text", "").strip()

            # Missing or invalid step ID
            if step_id is None:
                issues["missing_step_ids"].append(step)

            # Empty or whitespace-only text
            if not text:
                issues["empty_text"].append(step)

            # Very naive non-actionable check (expand later)
            if text and not any(text.lower().startswith(v) for v in [
                "turn", "open", "close", "check", "verify", "press", "ensure",
                "remove", "install", "connect", "disconnect", "start", "stop"
            ]):
                issues["non_actionable"].append(step)

        return issues
