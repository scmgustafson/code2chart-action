# Gen AI Settings
OPENAI_MODEL = 'o4-mini'
OPENAI_ENDPOINT = 'https://api.openai.com/v1/responses'
MAX_TOKENS = 100000

# Tool settings
DESTINATION_FILE = 'MERMAID.md'
MERMAID_HEADER = "## MermaidJS Diagram - Generated via Automation"
MERMAID_FOOTER = "<!-- END AUTOMATED MERMAID -->"

# File map settings
IGNORE_PATTERNS = (
    "venv", "samples", "favicon", ".git", 
    "node_modules", "public", ".next", "__tests__", "README.md", 
    "yarn.lock", ".DS_Store", ".env", "__pycache__", "lock",
    ".terraform", ".python", "requirements"
)