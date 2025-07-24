from credentials import OPENAI_API_KEY
import requests

OPENAI_ENDPOINT = "https://api.openai.com/v1/responses"
REQUEST_METHOD = "POST"
MODEL = "gpt-4-turbo"

def prompt_model(prompt: str) -> str:
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

def summarize_key_files(data) -> str:
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

def determine_relationships(data) -> str:
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

def output_mermaid(data: list[str]) -> str:
    input = ""
    for str in data:
        input += str
        input += '\n'

    print("@@@@@@@@@@@@ Mermaid Input @@@@@@@@@@@@")
    print(input)
        
    prompt = (
        "Generate a Mermaid diagram from the following module information and relationships.\n"
        "- Emphasize correct syntax on the Mermaid diagram"
        "- Make sure that every piece of the summary is accounted for in the graph, its important to be thorough"
        "- Use 'graph TD' format\n"
        "- Do not include styling or extra comments\n"
        "- Use subgraphs only if distinct groups are apparent\n\n"
        "- Output only the code block (example below):\n\n"
        '''```mermaid
        graph TD
        A[App Server] --> B[API Gateway]
        B --> C[Database]
        subgraph Frontend
            A
        end
        subgraph Backend
            B
            C
        end
        '''
        "```"
        f"\n\nRelationships:\n{relationships}"
    )

    mermaid = prompt_model(prompt)
    return mermaid

if __name__ == "__main__":
    with open("samples/main.tf", "r") as file:
        file_data = file.read()
    key_files_summary = summarize_key_files(file_data)
    print(key_files_summary)
    relationships = determine_relationships(key_files_summary)
    print(relationships)
    output = output_mermaid([key_files_summary, relationships])
    print(output)

    with open("MERMAID.md", "w+") as file:
        file.write(output)