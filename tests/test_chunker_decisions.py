
from src.chunking.chunker import SOPChunker

def test_decision_attaches_to_step():
    text = "- Verify identity\nIf missing ID, escalate\n- Continue processing"
    chunker = SOPChunker(max_lines=10)

    flows = chunker._build_micro_flows(text.split("\n"))

    assert len(flows) == 2
    assert "If missing ID" in flows[0]["text"]
