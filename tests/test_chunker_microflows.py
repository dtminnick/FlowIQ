
from src.chunking.chunker import SOPChunker

def test_microflows_basic_steps():
    text = "- Step one\nContinuation\n- Step two\nMore"
    chunker = SOPChunker(max_lines=10)

    flows = chunker._build_micro_flows(text.split("\n"))

    assert len(flows) == 2
    assert flows[0]["text"] == "- Step one\nContinuation"
    assert flows[1]["text"] == "- Step two\nMore"
