from credentials import OPENAI_API_KEY
import requests
import os

OPENAI_ENDPOINT = "https://api.openai.com/v1/responses"
REQUEST_METHOD = "POST"
MODEL = "gpt-4-turbo"

def prompt_model(prompt: str):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "input": prompt
    }

    response = requests.post(OPENAI_ENDPOINT, json=data, headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        for block in response_data.get("output", []):
            if block.get("type") == "message":
                for item in block.get("content", []):
                    if item.get("type") == "output_text":
                        return item.get("text")
        return "[No output_text found]"
    else:
        print(f"Error: {response.status_code}")

def summarize_key_files(data):
    prompt = (
        "You are summarizing the purpose and content of code files in a repository.\n"
        "- Identify important files and their roles\n"
        "- Each element should be labeled with whatever name or ID can be pulled from the source files\n"
        "- Mention key languages, frameworks, or tools used\n"
        "- Output as a bullet list\n"
        "- Include a header to describe your output\n"    
        "\n"
        f"{data}"
    )
    
    summary = prompt_model(prompt)
    return summary

def determine_relationships(data):
    prompt = (
        "Based on the summary of files below, infer the relationships between modules, components, or infrastructure.\n"
        "- Output as a bullet list of 'A depends on B' style\n"
        "- Include only logical, functional relationships\n"
        "- Output as a bullet list\n"
        "- Include a header to describe your output\n"    
        "\n"
        f"{data}"
    )
    
    relationships = prompt_model(prompt)
    return relationships

def output_mermaid(data):
    input = ""
    for str in data:
        input += str
        input += '\n'

    print("@@@@@@@@@@@@ Mermaid Input @@@@@@@@@@@@")
    print(input)
        
    prompt = (
        "Generate a Mermaid diagram from the following module information and relationships.\n"
        "- ONLY use correct syntax on the Mermaid diagram\n"
        "- Make sure that every piece of the summary is accounted for in the graph, it's important to be thorough\n"
        "- Determine the best graph type based on the format\n"
        "- Use subgraphs, classes, and labels where relevant\n"
        "- When referencing functions, you must avoid using () as that will give a syntax error. Omit that.\n"
        "- Class definition CSVs cannot include a space between the CSV items. Omit those."
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
        %%{init: {"theme": "forest", "themeVariables": {"primaryColor": "#e0f7e5","primaryTextColor": "#333"}}}%%
        graph TD
        subgraph "Frontend"
            FE[Browser]
            FE2((Mobile App))
        end

        subgraph "Backend Services"
            API["API Gateway"]
            Auth[Authentication Service]
            Users[User Service]
            DB[(User Database)]
        end

        subgraph "Infrastructure"
            LB[Load Balancer]
            CDN
        end

        %% Relationships
        FE -->|HTTPS| LB --> API
        FE2 -->|HTTPS| LB
        API --> Auth
        API --> Users
        Auth -.->|Token| Users
        Users --> DB
        CDN ==> FE
        CDN ==> FE2

        %% Styling with classes
        classDef infra fill:#f4e1d2,stroke:#333,color:#333;
        classDef svc fill:#d1e0f4,stroke:#333,color:#333;
        class LB,CDN infra
        class API,Auth,Users,DB svc
        '''
        "```"
        f"\n\nRelationships:\n{relationships}"
    )

    mermaid = prompt_model(prompt)
    return mermaid

def get_file_data(folder_path: str) -> str:
    file_data = ""

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith((".py", ".tf")):  # optional: filter to relevant files
                file_path = os.path.join(root, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        file_data += f"\n--- {file_path} ---\n"
                        file_data += f.read()
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return file_data

if __name__ == "__main__":
    sample_project = "./samples/python"
    file_data = get_file_data(sample_project)

    key_files_summary = summarize_key_files(file_data)
    print(key_files_summary)
    relationships = determine_relationships(key_files_summary)
    print(relationships)
    output = output_mermaid([key_files_summary, relationships])
    print(output)

    with open("MERMAID.md", "w+") as file:
        file.write(output)