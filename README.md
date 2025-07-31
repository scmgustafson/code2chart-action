# Automated Diagram Generator via Mermaid and AI

## MermaidJS Diagram - Generated via Automation
```mermaid
%%{init: {"theme":"neutral"}}%%
graph TD
  subgraph "Root Files"
    config["config.py\nCentral configuration for AI model, tool output, and file-traversal settings\nTechnologies: Python\n- Defines OPENAI_MODEL, OPENAI_ENDPOINT, MAX_TOKENS\n- Specifies MERMAID_HEADER, MERMAID_FOOTER, DESTINATION_FILE\n- Lists IGNORE_PATTERNS for directory and file exclusion"]
    main["main.py\nCLI entrypoint orchestrating file ingestion, AI summarization, relationship analysis, and Mermaid diagram generation\nTechnologies: Python,argparse,logging,requests\n- Parses input/output paths and append flag\n- Validates API key via utilities/auth\n- Builds file_data_map from utilities/file_utils\n- Generates summaries, relationships, and Mermaid via utilities/ai_requests\n- Writes or appends Mermaid output to target file"]
  end

  subgraph "Utilities"
    file_utils["utilities/file_utils.py\nFilesystem utilities for reading code files and writing Mermaid markdown\nTechnologies: Python,os,logging\n- Recursively walks input directory, applies IGNORE_PATTERNS\n- Reads file contents into a dict (file_data_map)\n- Writes or replaces Mermaid section in README or specified output"]
    auth["utilities/auth.py\nHandles retrieval and validation of OpenAI API key\nTechnologies: Python,os,sys\n- Loads key from environment or credentials.py\n- Exposes check_for_api_key to enforce presence"]
    ai_requests["utilities/ai_requests.py\nInteracts with OpenAI endpoint: prompt construction, chunking, summarization, relationship inference, Mermaid output\nTechnologies: Python,requests,tiktoken\n- prompt_model posts to OPENAI_ENDPOINT and parses output\n- summarize_key_files,determine_relationships,output_mermaid wrap specific prompts\n- chunk_by_tokens splits large repos into token-bounded summaries"]
  end

  subgraph "Prompts"
    templates["prompts/templates.py\nDefines prompt templates for summarization, relationship inference, and Mermaid diagram generation\nTechnologies: Python\n- summarize_key_files_prompt embeds user instructions and file data\n- determine_relationships_prompt specifies dependency-style output\n- output_mermaid_prompt includes Mermaid syntax rules and example"]
  end

  subgraph "Tests"
    tests_main["tests/tests_main.py\nPlaceholder for future unit tests of main functionality\nTechnologies: Python,pytest\n- Currently empty; TODOs in main.py reference added tests"]
  end

  main -->|validates API key via| auth
  main -->|builds file_data_map via| file_utils
  main -->|generates summaries & Mermaid via| ai_requests
  file_utils -->|uses configuration from| config
  ai_requests -->|uses configuration from| config
  ai_requests -->|uses prompt templates from| templates
  tests_main -->|tests functionality of| main

  classDef file fill:#d5f5e3,stroke:#333,color:#333
  class config,main,file_utils,auth,ai_requests,templates,tests_main file
```
<!-- END AUTOMATED MERMAID -->
