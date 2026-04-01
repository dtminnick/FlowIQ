
# cd C:\Users\donni\FlowIQ
# python -m tests.test_reader_cleaner


from src.utils.reader import FileReader
from src.preprocessing.cleaner import Cleaner
import os

def test_file(filepath: str):
    reader = FileReader()
    cleaner = Cleaner()

    print(f"\n=== Testing File: {filepath} ===")

    # Read raw text
    raw_text = reader.read(filepath)

    print("\n--- RAW TEXT (first 800 chars) ---")
    print(raw_text[:800])

    # Clean text
    cleaned_text = cleaner.clean(raw_text)

    print("\n--- CLEANED TEXT (first 800 chars) ---")
    print(cleaned_text[:800])


if __name__ == "__main__":
    # Adjust this path to your actual file
    sample_path = os.path.join("data", "samples", "Sample Procedure 1.docx")
    test_file(sample_path)
