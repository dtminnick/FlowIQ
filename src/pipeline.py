
from src.preprocessing.cleaner import Cleaner
from src.chunking.chunker import Chunker
from src.extraction.extractor import Extractor

class FlowIQPipeline:
    def __init__(self, config=None):
        self.config = config
        # placeholders for modules
        self.cleaner = Cleaner()
        self.chunker = Chunker()
        self.extractor = Extractor()
        self.parser = None
        self.validator = None
        self.corrector = None
        self.postprocessor = None

    def run(self, text: str):
        cleaned = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned)

    extracted = []
    
    for chunk in chunks:
        raw = self.extractor.extract(chunk["text"])
        extracted.append({
            "chunk_id": chunk["chunk_id"],
            "raw_output": raw
        })

        return extracted
