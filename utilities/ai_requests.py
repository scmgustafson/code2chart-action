import config
import prompts.templates as prompts
import utilities.auth as auth
import utilities.file_utils as file_utils

import requests
import logging
import tiktoken # type: ignore
import time

OPENAI_API_KEY = auth.OPENAI_API_KEY
OPENAI_MODEL = config.OPENAI_MODEL
OPENAI_ENDPOINT = config.OPENAI_ENDPOINT

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
        if "You exceeded your current quota" in response.text:
            raise Exception("OpenAI API quota exceeded.")
        else: 
            raise Exception(response.json())

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
    logging.debug(prompt_input)
    logging.debug("----------- End Mermaid Prompt Input -----------\n")
        
    prompt = prompts.output_mermaid_prompt(prompt_input)

    # Prompt GPT for mermaid then check if valid syntax, otherwise retry
    retries = config.TOTAL_RETRIES
    delay = config.RETRY_DELAY
    attempt_counter = 0
    while attempt_counter < retries:
        logging.info("Prompting for Mermaid")
        mermaid = str(prompt_model(prompt))
        logging.debug(mermaid)
        
        valid = file_utils.is_mermaid_syntax(mermaid)
        if valid:
                logging.info(f"Mermaid output ready")
                return mermaid
        logging.warning(f"Mermaid output failed validation (attempt {attempt_counter}/{retries}), retrying...")
        attempt_counter +=1
        time.sleep(delay)
    
    raise Exception(f"Output Mermaid invalid after {retries}. Exiting")



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