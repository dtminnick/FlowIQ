
from src.preprocessing.cleaner import Cleaner
from src.chunking.chunker import Chunker
from src.extraction.extractor import Extractor
from src.structuring.parser import Parser

class FlowIQPipeline:
    def __init__(self, config=None):
        self.config = config
        # placeholders for modules
        self.cleaner = Cleaner()
        self.chunker = Chunker()
        self.extractor = Extractor()
        self.parser = Parser()
        self.validator = None
        self.corrector = None
        self.postprocessor = None

    def run(self, text: str):
        cleaned = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned)

    parsed_steps = []

    for chunk in chunks:
        raw = self.extractor.extract(chunk["text"])
        steps = self.parser.parse(raw)

        parsed_steps.append({
            "chunk_id": chunk["chunk_id"],
            "steps": steps
        })

        return parsed_steps
