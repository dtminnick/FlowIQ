from src.preprocessing.cleaner import Cleaner
from src.chunking.chunker import SOPChunker
from src.utils.writer import FileWriter
from src.utils.reader import FileReader
from datetime import datetime

def test_chunk_sample_procedure():
    reader = FileReader()
    cleaner = Cleaner()
    chunker = SOPChunker(max_lines=8)
    writer = FileWriter()

    # Load sample document
    text = reader.read("data/samples/Sample Procedure 1.docx")

    # Run cleaner
    cleaned = cleaner.clean(text)

    # Run chunker
    chunks = chunker.chunk(cleaned)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save cleaned output
    cleaned_path = writer.save_text(
        cleaned,
        f"sample_procedure_1_cleaned_{timestamp}.txt"
    )

    # Save chunked output (all chunks in one file)
    chunked_text = "\n\n--- CHUNK BREAK ---\n\n".join(
        chunk["text"] for chunk in chunks
    )

    chunked_path = writer.save_text(
        chunked_text,
        f"sample_procedure_1_chunked_{timestamp}.txt"
    )

    # Basic assertions
    assert len(cleaned) > 0
    assert len(chunks) > 0
    assert chunks[0]["text"].strip() != ""

    print(f"\nCleaned output saved to: {cleaned_path}")
    print(f"Chunked output saved to: {chunked_path}")
