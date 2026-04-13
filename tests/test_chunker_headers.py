
from src.chunking.chunker import SOPChunker

def test_header_starts_new_chunk():
    text = "PURPOSE\n- Step one\n- Step two\nSCOPE\n- Step three"
    chunker = SOPChunker(max_lines=10)

    chunks = chunker.chunk(text)

    assert len(chunks) == 2
    assert chunks[0]["text"].startswith("PURPOSE")
    assert chunks[1]["text"].startswith("SCOPE")
