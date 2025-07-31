import credentials
import os

# Default to env variable, then check credentials.py, otherwise None
if os.environ.get("OPENAI_API_KEY"):
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
elif credentials != None:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", credentials.OPENAI_API_KEY)
else:
    OPENAI_API_KEY = None

def check_for_api_key():
    if not OPENAI_API_KEY:
        raise Exception("OpenAI API key not set.\n"
        "Set via env var or use `credentials.py` and set OPENAI_API_KEY var")
