
from src.utils.reader import FileReader
from src.preprocessing.cleaner import Cleaner

def run_reader_test(filepath):
    reader = FileReader()
    cleaner = Cleaner()

    raw_text = reader.read(filepath)
    cleaned_text = cleaner.clean(raw_text)

    print("\n=== RAW TEXT ===")
    print(raw_text[:500])  # show first 500 chars

    print("\n=== CLEANED TEXT ===")
    print(cleaned_text[:500])

if __name__ == "__main__":
    run_reader_test("data/raw/sample.docx")  # change path as needed
