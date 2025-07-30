# Automated Diagram Generator via Mermaid and AI

## MermaidJS Diagram - Generated via Automation
```mermaid
%%{init: {"theme":"default"}}%%
graph LR
  subgraph "Repository"
    config[config.py]
    requirements[requirements.txt]
    main[main.py]
    subgraph "prompts"
      templates[prompts/templates.py]
    end
  end

  subgraph "External Tools"
    requests[requests]
    tiktoken[tiktoken]
    OpenAI_API[OpenAI API]
    MermaidJS[MermaidJS]
    argparse[argparse]
    logging[logging]
    LLM_prompt_engineering[LLM prompt engineering]
  end

  main -->|uses constants from| config
  main -->|uses prompt templates from| templates
  main -->|chunks tokens via| tiktoken
  main -->|communicates via HTTP| requests
  main -->|calls for summarization| OpenAI_API
  main -->|generates diagram with| MermaidJS
  main -->|parses CLI args with| argparse
  main -->|logs progress with| logging

  templates -->|built on| LLM_prompt_engineering

  requirements ---|pins dependency| requests
  requirements ---|pins dependency| tiktoken
  requirements ---|underpins codebase| main
  requirements ---|underpins codebase| config
  requirements ---|underpins codebase| templates

  classDef file fill:#d5f5e3,stroke:#333,color:#333
  classDef tool fill:#fef5e7,stroke:#333,color:#333
  class config,requirements,main,templates file
  class requests,tiktoken,OpenAI_API,MermaidJS,argparse,logging,LLM_prompt_engineering tool
```
<!-- END AUTOMATED MERMAID -->
