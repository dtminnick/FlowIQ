
from src.preprocessing.cleaner import Cleaner

class FlowIQPipeline:
    def __init__(self, config=None):
        self.config = config
        # placeholders for modules
        self.cleaner = Cleaner()
        self.chunker = None
        self.extractor = None
        self.parser = None
        self.validator = None
        self.corrector = None
        self.postprocessor = None

    def run(self, text: str):
        """Main pipeline execution method."""
        raise NotImplementedError("Pipeline stages not yet implemented.")
