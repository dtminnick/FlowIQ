
def build_extraction_prompt(chunk: str) -> str:
    """Builds the prompt used to extract steps from a chunk of text."""
    return f"""
You are an AI system that extracts procedural steps from text.

Extract any explicit or implicit steps from the following text.
Return them as a numbered list of short, clear actions.

Text:
\"\"\"{chunk}\"\"\"
"""
