# Automated Diagram Generator via Mermaid and AI

## MermaidJS Diagram - Generated via Automation
```mermaid
%%{init: {"theme":"default"}}%%
graph TD
  subgraph "Repository Files"
    config[config.py<br>Defines FILES_PER_CHUNK, DESTINATION_FILE, IGNORE_PATTERNS]
    requirements[requirements.txt<br>Specifies requests==2.32.4]
    main[main.py<br>Parses args, reads files into map, chunks files, calls OpenAI API, generates MermaidJS diagrams, writes/appends output]
  end

  subgraph "External Dependencies"
    requests[requests]
    openai[OpenAI API]
    argparse[argparse]
    logging[logging]
    itertools[itertools]
    mermaid[MermaidJS]
    fs[File System I/O]
  end

  main -->|uses constants from| config
  main -->|uses HTTP library| requests
  requirements -->|provides library| requests
  main -->|calls service| openai
  main -->|parses CLI args| argparse
  main -->|logs events/errors via| logging
  main -->|implements chunking logic via| itertools
  main -->|generates diagrams with| mermaid
  main -->|reads/writes files via| fs

  classDef file fill:#d5f5e3,stroke:#333,color:#333
  classDef external fill:#f0e68c,stroke:#333,color:#333
  class config,requirements,main file
  class requests,openai,argparse,logging,itertools,mermaid,fs external
```
<!-- END AUTOMATED MERMAID -->
