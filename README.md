# Automated Diagram Generator via Mermaid and AI

## MermaidJS Diagram - Generated via Automation
```mermaid
%%{init: {"theme":"forest"}}%%
graph TB
  subgraph "Root Files"
    config[config.py]
    main[main.py]
    ini[pytest.ini]
  end

  subgraph "utilities"
    auth[utilities/auth.py]
    file_utils[utilities/file_utils.py]
    ai_requests[utilities/ai_requests.py]
  end

  subgraph "prompts"
    templates[prompts/templates.py]
  end

  tests_dir[tests/]

  %% Dependencies %%
  main -->|reads settings| config
  main -->|auth validation| auth
  main -->|file operations| file_utils
  main -->|AI summarization| ai_requests

  file_utils -->|uses settings| config

  ai_requests -->|uses templates| templates
  ai_requests -->|uses settings| config

  tests_dir -->|pytest config| ini
  tests_dir -->|tests CLI| main
  tests_dir -->|tests auth| auth
  tests_dir -->|tests file utils| file_utils
  tests_dir -->|tests AI requests| ai_requests
  tests_dir -->|tests templates| templates

  %% Styling %%
  classDef pythonfile fill:#d5f5e3,stroke:#333,color:#333
  classDef inifile fill:#fcf3cf,stroke:#333,color:#333
  classDef dir fill:#d6eaf8,stroke:#333,color:#333

  class config,main,auth,file_utils,ai_requests,templates pythonfile
  class ini inifile
  class tests_dir dir
```
<!-- END AUTOMATED MERMAID -->
