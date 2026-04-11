
import re
from typing import List, Dict

class SOPChunker:
    def __init__(self, max_lines: int = 8):
        self.max_lines = max_lines

    def chunk(self, text: str) -> List[Dict]:
        lines = text.split("\n")

        flows = self._build_micro_flows(lines)
        chunks = self._group_flows_into_chunks(flows)

        return chunks

    # --- Step 1: Build micro-flows ---

    def _build_micro_flows(self, lines: List[str]) -> List[Dict]:
        flows = []
        current_flow = []
        start_idx = 0

        for i, line in enumerate(lines):
            if self._is_new_step(line) and current_flow:
                flows.append(self._create_flow(current_flow, start_idx, i - 1))
                current_flow = []
                start_idx = i

            current_flow.append(line)

        if current_flow:
            flows.append(self._create_flow(current_flow, start_idx, len(lines) - 1))

        return flows

    def _is_new_step(self, line: str) -> bool:
        # Treat "-" as primary step indicator
        return line.strip().startswith("-")

    def _is_decision_line(self, line: str) -> bool:
        return bool(re.search(r'\b(if|when|otherwise|else)\b', line.lower()))

    def _create_flow(self, lines: List[str], start: int, end: int) -> Dict:
        return {
            "text": "\n".join(lines),
            "start_line": start,
            "end_line": end,
            "line_count": len(lines)
        }

    # --- Step 2: Group flows into chunks ---

    def _group_flows_into_chunks(self, flows: List[Dict]) -> List[Dict]:
        chunks = []
        current_chunk = []
        current_count = 0
        chunk_id = 0

        for flow in flows:
            if current_count + flow["line_count"] > self.max_lines and current_chunk:
                chunks.append(self._build_chunk(current_chunk, chunk_id))
                chunk_id += 1
                current_chunk = []
                current_count = 0

            current_chunk.append(flow)
            current_count += flow["line_count"]

        if current_chunk:
            chunks.append(self._build_chunk(current_chunk, chunk_id))

        return chunks

    def _build_chunk(self, flows: List[Dict], chunk_id: int) -> Dict:
        return {
            "chunk_id": chunk_id,
            "text": "\n".join(flow["text"] for flow in flows),
            "start_line": flows[0]["start_line"],
            "end_line": flows[-1]["end_line"]
        }
    