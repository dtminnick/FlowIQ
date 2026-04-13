
from src.chunking.chunker import SOPChunker

def test_chunking_respects_max_lines():
    text = "- A\n- B\n- C\n- D"
    chunker = SOPChunker(max_lines=2)

    chunks = chunker.chunk(text)

    assert len(chunks) == 2
    assert chunks[0]["text"].count("\n") + 1 == 2
    assert chunks[1]["text"].count("\n") + 1 == 2

