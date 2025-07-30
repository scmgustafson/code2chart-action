import config
import prompts.templates as prompts
import os
import requests
import logging
import argparse
import tiktoken
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
        "Authorization": f"Bearer {OPENAI_API_KEY}",
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
    prompt = prompts.summarize_key_files_prompt(data)
    
    logging.info("Beginning repo file summarization")
    summary = prompt_model(prompt)

    return summary

def determine_relationships(data):
    prompt = prompts.determine_relationships_prompt(data)

    logging.info("Determining relationships between processed chunks/files")
    relationships = prompt_model(prompt)

    return relationships

def output_mermaid(data):
    
    # Take each input file and format separately into a single string
    prompt_input = ""
    for dict in data:
        prompt_input += str(dict)
        prompt_input += "\n---\n"

    logging.debug("\n----------- Start Mermaid Prompt Input -----------")
    logging.debug(input)
    logging.debug("----------- End Mermaid Prompt Input -----------\n")
        
    prompt = prompts.output_mermaid_prompt(prompt_input)

    logging.info("Prompting for Mermaid")
    mermaid = prompt_model(prompt)

    logging.debug(mermaid)

    logging.info(f"Mermaid output ready")
    return mermaid

def chunk_by_tokens(file_data_map, max_tokens=config.MAX_TOKENS, model=OPENAI_MODEL):
    """
    Chunk files by token count rather than file count.
    Ensures that no chunk exceeds max_tokens and files are not split.
    """
    try:
        enc = tiktoken.encoding_for_model(model)
    except KeyError:
        # Default to cl100k_base for newer models like o4-mini
        enc = tiktoken.get_encoding("cl100k_base")
    chunked_summaries = {}
    current_chunk = []
    current_token_count = 0
    chunk_index = 0

    sorted_items = list(file_data_map.items())  # Ensure order is consistent

    # Precompute token counts for each file
    token_counts = []
    for file_path, file_content in sorted_items:
        file_tokens = enc.encode(file_content)
        file_token_count = len(file_tokens)
        token_counts.append(file_token_count)

    # Estimate total chunks
    total_tokens = 0
    estimated_chunks = 0
    for count in token_counts:
        if count > max_tokens:
            continue
        if total_tokens + count > max_tokens:
            estimated_chunks += 1
            total_tokens = 0
        total_tokens += count
    if total_tokens > 0:
        estimated_chunks += 1

    chunk_counter = 1

    for idx, (file_path, file_content) in enumerate(sorted_items):
        file_tokens = enc.encode(file_content)
        file_token_count = len(file_tokens)

        if file_token_count > max_tokens:
            logging.warning(f"File {file_path} exceeds token limit alone ({file_token_count} > {max_tokens}), skipping.")
            continue

        if current_token_count + file_token_count > max_tokens:
            logging.info(f"Processing chunk {chunk_counter} of {estimated_chunks} total chunks")
            # Finalize current chunk and reset
            chunk_prompt = "".join(
                f"\n--- {path} ---\n{content}\n" for path, content in current_chunk
            )
            summary = summarize_key_files(chunk_prompt)
            chunked_summaries[chunk_index] = summary

            chunk_index += 1
            chunk_counter += 1
            current_chunk = []
            current_token_count = 0

        # Add file to current chunk
        current_chunk.append((file_path, file_content))
        current_token_count += file_token_count

    # Handle any remaining files in the last chunk
    if current_chunk:
        logging.info(f"Processing chunk {chunk_counter} of {estimated_chunks} total chunks")
        chunk_prompt = "".join(
            f"\n--- {path} ---\n{content}\n" for path, content in current_chunk
        )
        summary = summarize_key_files(chunk_prompt)
        chunked_summaries[chunk_index] = summary

    return chunked_summaries

def get_file_data_map(folder_path: str):
    logging.info(f"Processing directory {folder_path} into file data map")
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
    # Check if attempting to write to an existing file and not in apend mode to stop program
    if os.path.exists(destination_path) and not is_in_apend_mode:
        raise Exception("Attempting to write Mermaid to existing file while not in append mode.\n \
                        Use --apend to allow writing to existing file.")

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
        raise Exception("OpenAI API key not set.\n"
        "Set via env var or use `credentials.py` and set OPENAI_API_KEY var")

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
    summaries = chunk_by_tokens(file_data_map)
    relationships = determine_relationships(summaries)
    mermaid_output = str(output_mermaid([summaries, relationships]))
    #mermaid_output="test"

    # Output Mermaid to destination file via apend or creating new
    write_mermaid_to_file(destination_file, mermaid_output)

    #TODO add unit tests
    #TODO check for valid mermaid syntax or retry that step
    #TODO break prompts into a prompts.py file
    #TODO break functions out of main and into utilities file
    #TODO Setup everything need to put workflow on marketplace