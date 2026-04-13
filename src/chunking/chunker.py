
import re
from typing import List, Dict

class SOPChunker:
    def __init__(self, max_lines: int = 8, max_chars: int = 800):
        self.max_lines = max_lines
        self.max_chars = max_chars

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def chunk(self, text: str) -> List[Dict]:
        lines = text.split("\n")

        microflows = self._build_micro_flows(lines)
        chunks = self._group_flows_into_chunks(microflows)

        return chunks

    # ---------------------------------------------------------
    # Step 1 — Build micro-flows (structure-aware)
    # ---------------------------------------------------------

    def _build_micro_flows(self, lines: List[str]) -> List[Dict]:
        flows = []
        current_flow = []
        start_idx = 0
        step_id = 0
        parent_step_id = None

        for i, line in enumerate(lines):
            stripped = line.strip()

            # --- HEADER ---
            if self._is_header(stripped):
                # close previous flow
                if current_flow:
                    flows.append(self._create_flow(current_flow, start_idx, i - 1))
                # start new header flow
                current_flow = [line]
                start_idx = i
                parent_step_id = None
                continue

            # --- NEW STEP ---
            if self._is_new_step(stripped):
                # close previous flow
                if current_flow:
                    flows.append(self._create_flow(current_flow, start_idx, i - 1))
                # start new step flow
                current_flow = [line]
                start_idx = i
                step_id += 1
                parent_step_id = step_id
                continue

            # --- DECISION LINE ---
            if self._is_decision_line(stripped):
                # decision lines attach to parent step
                current_flow.append(line)
                continue

            # --- CONTINUATION LINE ---
            current_flow.append(line)

        # close final flow
        if current_flow:
            flows.append(self._create_flow(current_flow, start_idx, len(lines) - 1))

        return flows

    # ---------------------------------------------------------
    # Step 2 — Group micro-flows into chunks (hybrid)
    # ---------------------------------------------------------

    def _group_flows_into_chunks(self, flows: List[Dict]) -> List[Dict]:
        chunks = []
        current_chunk = []
        current_lines = 0
        chunk_id = 0

        for flow in flows:

            # Header starts new chunk
            if self._flow_is_header(flow) and current_chunk:
                chunks.append(self._build_chunk(current_chunk, chunk_id))
                chunk_id += 1
                current_chunk = []
                current_lines = 0

            # Max-lines split
            if current_lines + flow["line_count"] > self.max_lines and current_chunk:
                chunks.append(self._build_chunk(current_chunk, chunk_id))
                chunk_id += 1
                current_chunk = []
                current_lines = 0

            # ALWAYS add the flow after handling splits
            current_chunk.append(flow)
            current_lines += flow["line_count"]

        # Final chunk
        if current_chunk:
            chunks.append(self._build_chunk(current_chunk, chunk_id))

        return chunks


    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def _is_new_step(self, line: str) -> bool:
        return line.startswith("-")

    def _is_header(self, line: str) -> bool:
        # Steps are not headers
        if line.startswith("-"):
            return False

        # Must contain at least one letter
        if not any(c.isalpha() for c in line):
            return False

        # ALL CAPS rule
        if line.isupper() and len(line.split()) <= 6:
            return True

        return False

    def _is_decision_line(self, line: str) -> bool:
        return bool(re.search(r"\b(if|when|otherwise|else)\b", line.lower()))

    def _flow_is_header(self, flow: Dict) -> bool:
        first_line = flow["text"].split("\n")[0].strip()
        return self._is_header(first_line)

    def _create_flow(self, lines: List[str], start: int, end: int) -> Dict:
        return {
            "text": "\n".join(lines),
            "start_line": start,
            "end_line": end,
            "line_count": len(lines)
        }

    def _build_chunk(self, flows: List[Dict], chunk_id: int) -> Dict:
        return {
            "chunk_id": chunk_id,
            "text": "\n".join(flow["text"] for flow in flows),
            "start_line": flows[0]["start_line"],
            "end_line": flows[-1]["end_line"]
        }
