import config

import logging
import os
from typing import Tuple

def is_mermaid_syntax(text: str) -> bool:
    lines = text.strip().splitlines()

    # Strip ```mermaid ... ``` fencing
    if lines[0].strip().startswith("```mermaid"):
        lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

    found_diagram_start = False

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or config.COMMENT_DEF.match(stripped):
            continue
        if not found_diagram_start and config.DIAG_START.match(stripped):
            found_diagram_start = True
            continue
        if not found_diagram_start and not stripped.startswith("%%{"):
            logging.error(f"[FAIL] Line {lineno}: expected diagram start, got: {stripped}")
            return False

        matched = any([
            config.DIAG_START.match(stripped),
            config.NODE_DEF.match(stripped),
            config.EDGE_DEF.match(stripped),
            config.SUBGRAPH_DEF.match(stripped),
            config.SUBGRAPH_END.match(stripped),
            config.CLASS_DEF.match(stripped),
            config.CLASS_ASSIGN.match(stripped)
        ])
        if not matched:
            logging.error(f"[FAIL] Line {lineno}: unrecognized syntax: {stripped}")
            return False

    return found_diagram_start



def get_file_data_map(folder_path: str):
    '''For all of the files in a directory to be ingested, write them to a dict if they aren't ignored
    '''

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

def write_mermaid_to_file(destination_path: str, mermaid: str):
    header = config.MERMAID_HEADER
    footer = config.MERMAID_FOOTER

    # Output Mermaid to destination file via apend or creating new
    try:
        # Write new file if target doesn't exist
        if not os.path.exists(destination_path):
            logging.info(f"Writing mermaid to new file: {destination_path}")
            with open(destination_path, "w+") as file:
                file.write(f"{header}\n{str(mermaid)}\n{footer}")
            return
        else:
            # If target exists, load content into var for rewriting
            with open(destination_path, "r") as file:
                content = file.read()

            # If Mermaid has already been written to the target file via this script
            if header in content and footer in content:
                # Replace existing Mermaid block by rewriting existing file
                pre = content.split(header)[0]
                post = content.split(footer)[-1]
                new_content = f"{pre}{header}\n{mermaid}\n{footer}{post}"
            else:
                # Add Mermaid to existing file contents
                new_content = f"{content}\n{header}\n{mermaid}\n{footer}\n"
            
            logging.info(f"Writing mermaid to existing file: {destination_path}")
            with open(destination_path, "w+") as file:
                file.write(new_content)
            logging.info("Process complete")
            return
    except Exception as e:
        logging.error(f"Error occured while attempting to write Mermaid to file: {destination_path}")
        logging.error(f"Error: {e}")
        