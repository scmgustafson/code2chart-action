def summarize_key_files_prompt(data: str) -> str:
        return (
            "You are summarizing the purpose and content of code files in a repository. You will be given them in chunks of N files.\n" \
            "- Provide the output in JSON so it is token efficient\n" \
            "- Identify important files and their roles\n" \
            "- Each element should be labeled with whatever name or ID can be pulled from the source files\n" \
            "- Mention key languages, frameworks, or tools used\n" \
            "- Output as a bullet list\n" \
            "- Include a header to describe your output\n" \
            "The file data is as follows:\n"
            f"{data}"
        )

def determine_relationships_prompt(data: str) -> str:
        return (
        "Based on the summary of files below, infer the relationships between modules, components, or infrastructure.\n" \
        "- Output as a bullet list of 'A depends on B' style\n" \
        "- Include only logical, functional relationships\n" \
        "- Output as a bullet list\n" \
        "- Include a header to describe your output\n" \
        f"{data}"
    )

def output_mermaid_prompt(data: str) -> str:
    return (
        "Generate a Mermaid diagram from the following module information and relationships.\n"
        "- ONLY use correct syntax on the Mermaid diagram\n"
        "- Make sure that every piece of the summary is accounted for in the graph, it's important to be thorough\n"
        "- Determine the best graph type based on the format\n"
        "- Use subgraphs, classes, and labels where relevant\n"
        "- When referencing functions, you must avoid using () as that will give a syntax error. Omit that.\n"
        "- Class definition CSVs cannot include a space between the CSV items. Omit those.\n"
        "- Use styling that is easy to read and make sure to label arrows with some detail about the relationship between entities\n"
        "- Output only the code block\n"
        "\n"
        "Available MermaidJS themes:\n"
        '["default", "forest", "dark", "neutral", "base", "null"]\n'
        "\n"
        "Available arrow types:\n"
        '["-->", "<--", "<-->", "---", "==>", "===", "-.->", "x--", "o--"]\n'
        "\n"
        "Here is an example of MermaidJS syntax for a complex diagram:\n\n"
        '''```mermaid
            %%{init: {"theme": "dark", "themeVariables": {"primaryColor": "#e8f4fd","edgeLabelBackground":"#ffffff"}}}%%
            graph TD
            subgraph "samples/python"
                MP[samples/python/main.py]
                subgraph "app"
                RT[samples/python/app/routes.py]
                end
                subgraph "services"
                US[samples/python/services/user_service.py]
                end
                subgraph "utils"
                FM[samples/python/utils/formatter.py]
                end
            end

            MP -->|imports routes.py| RT
            RT -->|calls user_service.py| US
            US -->|uses formatter.py| FM

            classDef file fill:#d5f5e3,stroke:#333,color:#333
            class MP,RT,US,FM file
            ```
        '''
        f"\n\Data to generate Mermaid from:\n{data}"
    )