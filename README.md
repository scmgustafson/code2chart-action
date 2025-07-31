# Automated Diagram Generator via Mermaid and AI

## MermaidJS Diagram - Generated via Automation
```mermaid
%%{init: {"theme": "default"}}%%
graph TD
    subgraph Root
        CONF[config.py]
        MAIN[main.py]
    end
    subgraph utilities
        FU[file_utils.py]
        AUTH[auth.py]
        AIREQ[ai_requests.py]
        INIT[__init__.py]
    end
    subgraph prompts
        TEMP[templates.py]
    end
    subgraph tests
        TM[tests_main.py]
    end
    CRED[credentials.py]

    MAIN -->|imports settings| CONF
    MAIN -->|uses file I/O utilities| FU
    MAIN -->|performs auth check| AUTH
    MAIN -->|integrates with AI requests| AIREQ

    FU -->|uses IGNORE_PATTERNS| CONF
    AUTH -->|reads API key from env or credentials.py| CRED
    AIREQ -->|reads settings| CONF
    AIREQ -->|uses prompt templates| TEMP

    TM -->|tests main entry| MAIN

    classDef file fill:#d5f5e3,stroke:#333,color:#333
    class CONF,MAIN,FU,AUTH,AIREQ,INIT,TEMP,TM,CRED file
```
<!-- END AUTOMATED MERMAID -->
