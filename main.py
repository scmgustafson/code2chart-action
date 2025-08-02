# Local imports
import config
import utilities.ai_requests as ai_requests
import utilities.auth as auth
import utilities.file_utils as file_utils

# Other imports
import os
import logging
import argparse
from itertools import islice

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a MermaidJS diagram from a directory of code files using an LLM.",
        epilog="Example usage:\n"
               "  python main.py ./src --output diagram.md --append --debug",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "input",
        help="Path to the input directory containing code files to analyze."
    )
    parser.add_argument(
        "--output",
        default="README.md",
        help="Path to the output Markdown file for MermaidJS diagram (default: README.md)."
    )
    parser.add_argument(
        "--append",
        default=False,
        action="store_true",
        help="Append MermaidJS output to an existing file. Required if the output file already exists."
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Enable debug logging for troubleshooting."
    )

    return parser.parse_args()

def check_apend_to_existing_file(destination_path, is_apend):
    if os.path.exists(destination_path) and not is_apend:
        raise Exception("Attempting to write Mermaid to existing file while not in append mode.\n \
                        Use --apend to allow writing to existing file.")


if __name__ == "__main__":
    # Parse CLI arguments
    args = parse_args()
    input_directory = args.input
    destination_file = args.output
    is_in_apend_mode = args.append
    is_in_debug_mode = args.debug

    if is_in_debug_mode:
        logging.debug("Program running in debug logging level")
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(message)s",
            force=True
        )   

    # Prechecks
    auth.check_for_api_key()
    check_apend_to_existing_file(destination_file, is_in_apend_mode)

    # Main function calls to GPT
    file_data_map = file_utils.get_file_data_map(input_directory)
    summaries = ai_requests.chunk_by_tokens(file_data_map)
    relationships = ai_requests.determine_relationships(summaries)
    mermaid_output = str(ai_requests.output_mermaid([summaries, relationships]))

    # Output Mermaid to destination file via apend or creating new
    file_utils.write_mermaid_to_file(destination_file, mermaid_output)

    #TODO check for valid mermaid syntax or retry that step
    #TODO Setup everything need to put workflow on marketplace