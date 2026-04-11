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

    subgraph Preprocessing
        B1[Cleaner]
    end

    subgraph Chunking
        C1[Chunker]
    end

    subgraph Extraction
        D1[Extractor]
        D2[LLM Client]
        D3[Prompts]
    end

    subgraph Structuring
        E1[Parser]
    end

    subgraph Validation
        F1[Validator]
        F2[Corrector]
    end

    subgraph Postprocessing
        G1[Formatter / Exporter]
    end
```