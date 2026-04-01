
from src.preprocessing.cleaner import Cleaner
from src.chunking.chunker import Chunker
from src.extraction.extractor import Extractor
from src.structuring.parser import Parser
from src.validation.validator import Validator
from src.validation.corrector import Corrector
from src.postprocessing.rules import PostProcessor

class FlowIQPipeline:
    def __init__(self, config=None):
        self.config = config
        self.cleaner = Cleaner()
        self.chunker = Chunker()
        self.extractor = Extractor()
        self.parser = Parser()
        self.validator = Validator()
        self.corrector = Corrector()
        self.postprocessor = PostProcessor()

    def run(self, text: str):
        cleaned = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned)

        parsed_steps = []

        for chunk in chunks:
            raw = self.extractor.extract(chunk["text"])
            steps = self.parser.parse(raw)

            issues = self.validator.validate(steps)
            corrected = self.corrector.refine(steps, issues)
            final_steps = self.postprocessor.apply(corrected)

            parsed_steps.append({
                "chunk_id": chunk["chunk_id"],
                "steps": final_steps,
                "issues": issues
            })

        return parsed_steps
