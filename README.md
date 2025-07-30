# Automated Diagram Generator via Mermaid and AI

## MermaidJS Diagram - Generated via Automation
```mermaid
%%{init: {"theme": "default","themeVariables":{"primaryColor":"#e8f4fd","edgeLabelBackground":"#ffffff"}}}%%
graph LR
  subgraph "Files"
    config_py[config.py]
    req_txt[requirements.txt]
    main_py[main.py]
  end

  subgraph "main.py Functions"
    gf[get_file_data_map]
    pm[prompt_model]
    cb[chunk_by_tokens]
    sk[summarize_key_files]
    dr[determine_relationships]
    om[output_mermaid]
    wm[write_mermaid_to_file]
    ck[check_for_api_key]
  end

  subgraph "External Dependencies"
    req[requests]
    tik[tiktoken]
    arg[argparse]
    log[logging]
    oa[OpenAI_API]
    cred[credentials.py]
    env[Environment_Variables]
    outf[Output_File(README/custom)]
  end

  main_py -->|uses constants & ignore patterns| config_py
  main_py -->|parses CLI args| arg
  main_py -->|logs diagnostics| log
  main_py -->|lists dependencies| req_txt

  req_txt -->|specifies version| req
  req_txt -->|specifies version| tik

  main_py --> gf
  main_py --> pm
  main_py --> cb
  main_py --> sk
  main_py --> dr
  main_py --> om
  main_py --> wm
  main_py --> ck

  gf -->|applies IGNORE_PATTERNS| config_py
  pm -->|sends HTTP calls| req
  pm -->|calls endpoint| oa
  cb -->|splits tokens| tik
  sk -->|invokes prompt_model| pm
  dr -->|analyzes summaries| sk
  om -->|builds diagram from| dr
  wm -->|writes Mermaid block| om
  wm -->|outputs to| outf
  ck -->|checks env vars| env
  ck -->|or optional| cred

  classDef file fill:#d5f5e3,stroke:#333,color:#333
  classDef func fill:#f5f5d5,stroke:#333,color:#333
  classDef lib fill:#e8f4fd,stroke:#333,color:#333

  class config_py,req_txt,main_py file
  class gf,pm,cb,sk,dr,om,wm,ck func
  class req,tik,arg,log,oa,cred,env,outf lib
```
<!-- END AUTOMATED MERMAID -->
