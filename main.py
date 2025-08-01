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

# if os.environ.get("OPENAI_API_KEY"):
#     OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# elif credentials != None:
#     OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", credentials.OPENAI_API_KEY)
# else:
#     OPENAI_API_KEY = None

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

def parse_args():
    parser = argparse.ArgumentParser(description="description here")

    parser.add_argument("input", help="The directory to be ingested by the LLM and represented with MermaidJS")
    parser.add_argument(
        "--output", default="README.md", help="The name/location of the MermaidJS markdown output file." \
        "Default appends to README.md"
    )
    parser.add_argument("--apend", default=False, action="store_true", help="Must set if intending to write MermaidJS to an existing file")

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
    is_in_apend_mode = args.apend

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

    #TODO add unit tests
    #TODO check for valid mermaid syntax or retry that step
    #TODO add debug mode with cli flag
    #TODO Setup everything need to put workflow on marketplace