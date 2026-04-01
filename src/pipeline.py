
from src.preprocessing.cleaner import Cleaner
from src.chunking.chunker import Chunker

class FlowIQPipeline:
    def __init__(self, config=None):
        self.config = config
        # placeholders for modules
        self.cleaner = Cleaner()
        self.chunker = Chunker()
        self.extractor = None
        self.parser = None
        self.validator = None
        self.corrector = None
        self.postprocessor = None

    def run(self, text: str):
        """Main pipeline execution method."""
        cleaned = self.cleaner.clean(text)
        chunks = self.chunker.chunk(cleaned)
        return chunks
