
import re

class Chunker:
    def chunk(self, text: str) -> list[dict]:
        """Basic sentence-based chunking placeholder."""
        # Split on periods, question marks, exclamation marks
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())

        chunks = []
        for i, sentence in enumerate(sentences, start=1):
            if sentence:
                chunks.append({
                    "chunk_id": i,
                    "text": sentence
                })

        return chunks
