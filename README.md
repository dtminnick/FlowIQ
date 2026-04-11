# FlowIQ

Process intelligence pipeline for extracting structured process models from standard operating procedures and similar documents.

```mermaid
flowchart TD
    A[Raw Procedure Document] --> B[Preprocessing]
    B --> C[Chunking]
    C --> D[Extraction]
    D --> E[Structuring]
    E --> F[Validation]
    F --> G[Postprocessing]
    G --> H[Final Structured Process Model]
```