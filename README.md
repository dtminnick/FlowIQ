# FlowIQ

Process intelligence pipeline for extracting structured process models from standard operating procedures and similar documents.

```mermaid
flowchart TD

    %% Main pipeline
    A[Raw Procedure Document] --> B[preprocessing/]
    B --> C[chunking/]
    C --> D[extraction/]
    D --> E[structuring/]
    E --> F[validation/]
    F --> G[postprocessing/]
    G --> H[Structured Process Model]

    %% Preprocessing
    B --> B1
    subgraph preprocessing/
        direction TB
        B1[Cleaner]
    end

    %% Chunking
    C --> C1
    subgraph chunking/
        direction TB
        C1[Chunker]
    end

    %% Extraction
    D --> D1
    subgraph extraction/
        direction TB
        D1[Extractor]
        D2[LLM Client]
        D3[Prompts]
    end

    %% Structuring
    E --> E1
    subgraph structuring/
        direction TB
        E1[Parser]
    end

    %% Validation
    F --> F1
    subgraph validation/
        direction TB
        F1[Validator]
        F2[Corrector]
    end

    %% Postprocessing
    G --> G1
    subgraph postprocessing/
        direction TB
        G1[Formatter / Exporter]
    end

```

For a detailed view of FlowIQ’s internal architecture, see [Architecture Overview](docs/architecture.md).
