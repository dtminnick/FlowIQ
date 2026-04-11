
from src.preprocessing.cleaner import Cleaner
from src.utils.writer import FileWriter
from src.utils.reader import FileReader
from datetime import datetime

def test_clean_sample_procedure():
    reader = FileReader()
    cleaner = Cleaner()
    writer = FileWriter()

    # Load sample document
    text = reader.read("data/samples/Sample Procedure 1.docx")

    # Run cleaner
    cleaned = cleaner.clean(text)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save output
    output_path = writer.save_text(cleaned, f"sample_procedure_1_cleaned_{timestamp}.txt")

    # Basic assertion (not strict—just sanity)
    assert len(cleaned) > 0

    print(f"\nCleaned output saved to: {output_path}")
