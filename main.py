import config
import os
import requests
import logging
import argparse
from itertools import islice
try:
    import credentials
except ImportError:
    credentials = None

OPENAI_ENDPOINT = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "o4-mini"
if os.environ.get("OPENAI_API_KEY"):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
elif credentials != None:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", credentials.OPENAI_API_KEY)
else:
    OPENAI_API_KEY = None
#OPENAI_MODEL = "gpt-4-turbo"

MERMAID_HEADER = "## MermaidJS Diagram - Generated via Automation"
MERMAID_FOOTER = "<!-- END AUTOMATED MERMAID -->"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

def parse_args():
    parser = argparse.ArgumentParser(description="description here")

    parser.add_argument("input", help="The directory to be ingested by the LLM and represented with MermaidJS")
    parser.add_argument("--output", default="README.md", help="The name/location of the MermaidJS markdown output file." \
    "Default appends to README.md")
    parser.add_argument("--apend", default=False, action="store_true", help="Must set if intending to write MermaidJS to an existing file")

    return parser.parse_args()

def prompt_model(prompt: str):
    headers = {
        "Authorization": f"Bearer {credentials.OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": OPENAI_MODEL,
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
        logging.error("No output_text found")
        return None
    else:
        logging.error(f"Error occured. Status code: {response.status_code}")
        logging.error(response.json())

def summarize_key_files(data):
    prompt = (
        "You are summarizing the purpose and content of code files in a repository. You will be given them in chunks of N files.\n"
        "- Provide the output in JSON so that another LLM can utilize it and it is token efficient.\n"
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

# def summarize_file(file_path: str, file_content: str) -> str:
#     prompt = (
#         f"You are summarizing the purpose and content of the following code file:\n"
#         f"File: {file_path}\n"
#         f"---\n"
#         f"{file_content}\n"
#         "\n"
#         "- Identify the file's role\n"
#         "- Mention key languages, frameworks, or tools used\n"
#         "- Output as a bullet list\n"
#         "- Include a header to describe your output\n"
#     )
#     return prompt_model(prompt)

def chunk_and_summarize_files(file_data_map, files_per_chunk=5):
    """
    Chunks the file_data_map into groups of files_per_chunk, summarizes each chunk,
    and returns a dict mapping chunk index to summary.
    """

    def chunk_dict(data, size):
        it = iter(data.items())
        for i in range(0, len(data), size):
            yield dict(islice(it, size))

    chunked_summaries = {}
    total_chunks = (len(file_data_map) + files_per_chunk - 1) // files_per_chunk
    for idx, chunk in enumerate(chunk_dict(file_data_map, files_per_chunk), start=1):
        logging.info(f"Processing chunk {idx} of {total_chunks}")
        chunk_prompt = ""
        for file_path, file_content in chunk.items():
            chunk_prompt += f"\n--- {file_path} ---\n{file_content}\n"
        summary = summarize_key_files(chunk_prompt)
        chunked_summaries[idx - 1] = summary
    return chunked_summaries

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

    logging.info("Determining relationships between processed chunks/files")
    relationships = prompt_model(prompt)

    return relationships

def output_mermaid(data):
    input = ""
    for dict in data:
        input += str(dict)
        input += "\n---\n"

    logging.debug("\n----------- Start Mermaid Prompt Input -----------")
    logging.debug(input)
    logging.debug("----------- End Mermaid Prompt Input -----------\n")
        
    prompt = (
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

    logging.info("Prompting for Mermaid")
    mermaid = prompt_model(prompt)
    logging.debug(mermaid)

    logging.info(f"Mermaid output ready")
    return mermaid

# def get_file_data(folder_path: str) -> str:
#     file_data = ""
#     ignore_patterns = (".git", "node_modules", "public", ".next", "__tests__", "README.md", "yarn.lock", ".DS_Store", ".env", "__pycache__")

#     for root, dirs, files in os.walk(folder_path):
#         # Remove ignored directories in-place
#         dirs[:] = [d for d in dirs if not any(pattern in d for pattern in ignore_patterns)]
#         for filename in files:
#             if any(pattern in filename for pattern in ignore_patterns):
#                 continue
#             file_path = os.path.join(root, filename)
#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     file_data += f"\n--- {file_path} ---\n"
#                     file_data += f.read()
#             except Exception as e:
#                 print(f"Error reading {file_path}: {e}")

#     return file_data

def get_file_data_map(folder_path: str):
    logging.info(f"Processing directory: {folder_path}")
    file_data_map = {}
    ignore_patterns = config.IGNORE_PATTERNS

    # Traverse the target directory
    for root, dirs, files in os.walk(folder_path):
        # Ignore any directories that match the ignore patterns by reprocessing directory list
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in ignore_patterns)]
        for filename in files:
            # Pass on files that match the pattern
            if any(pattern in filename for pattern in ignore_patterns):
                continue
            file_path = os.path.join(root, filename)
            # Read in the contents of the file and add it to the file_data_map
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    file_data_map[file_path] = f.read()
            # If fail to read file, just add the exception so the LLM can get that data too
            except Exception as e:
                logging.error(f"Error reading {file_path}: {e}")
                file_data_map[file_path] = e
    return file_data_map

def check_apend_to_existing_file(destination_path):
    if os.path.exists(destination_path) and not is_in_apend_mode:
        logging.error("Attempting to write Mermaid to existing file while not in append mode.")
        logging.error("Use --apend to allow writing to existing file.")
        exit(0)

def write_mermaid_to_file(destination_path: str, mermaid: str):
    # Output Mermaid to destination file via apend or creating new
    try:
        # Write new file if target doesn't exist
        if not os.path.exists(destination_path):
            logging.info(f"Writing mermaid to new file: {destination_path}")
            with open(destination_path, "w+") as file:
                file.write(f"{MERMAID_HEADER}\n{str(mermaid)}\n{MERMAID_FOOTER}")
            return
        else:
            # If target exists, load content into var for rewriting
            with open(destination_path, "r") as file:
                content = file.read()

            # If Mermaid has already been written to the target file via this script
            if MERMAID_HEADER in content and MERMAID_FOOTER in content:
                # Replace existing Mermaid block by rewriting existing file
                pre = content.split(MERMAID_HEADER)[0]
                post = content.split(MERMAID_FOOTER)[-1]
                new_content = f"{pre}{MERMAID_HEADER}\n{mermaid}\n{MERMAID_FOOTER}{post}"
            else:
                # Add Mermaid to existing file contents
                new_content = f"{content}\n{MERMAID_HEADER}\n{mermaid}\n{MERMAID_FOOTER}\n"
            
            logging.info(f"Writing mermaid to existing file: {destination_path}")
            with open(destination_path, "w+") as file:
                file.write(new_content)
            logging.info("Process complete")
            return
    except Exception as e:
        logging.error(f"Error occured while attempting to write Mermaid to file: {destination_path}")
        logging.error(f"Error: {e}")

def check_for_api_key():
    if not OPENAI_API_KEY:
        logging.error("OpenAI API key not set. Exiting.")
        logging.error("Set via env var or use `credentials.py` and set OPENAI_API_KEY var")
        exit(0)

if __name__ == "__main__":
    check_for_api_key()

    # Parse CLI arguments
    args = parse_args()
    input_directory = args.input
    destination_file = args.output
    is_in_apend_mode = args.apend

    check_apend_to_existing_file(destination_file)

    # Main function calls to GPT
    file_data_map = get_file_data_map(input_directory)
    summaries = chunk_and_summarize_files(file_data_map, config.FILES_PER_CHUNK)
    relationships = determine_relationships(summaries)
    mermaid_output = str(output_mermaid([summaries, relationships]))
    #mermaid_output="test"

    # Output Mermaid to destination file via apend or creating new
    write_mermaid_to_file(destination_file, mermaid_output)

    #TODO add unit tests
    #TODO finish implementing chunking based on tokens
    #TODO make API key paramertized so it can read from GitHub for workflow
    #TODO create workflow file