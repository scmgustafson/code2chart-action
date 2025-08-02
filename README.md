# Automated Diagram Generator via Mermaid and AI

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Automated Diagram Generator is a tool that leverages AI to analyze your codebase and generate [MermaidJS](https://mermaid-js.github.io/) diagrams automatically. It is designed to help developers visualize project structure, dependencies, and relationships with minimal manual effort.

## Features

- **Automated Codebase Analysis:** Uses AI to summarize and infer relationships between files.
- **MermaidJS Output:** Generates ready-to-use Mermaid diagrams for documentation.
- **CLI Tool:** Simple command-line interface for easy integration into workflows.
- **Append or Overwrite:** Choose to append diagrams to existing markdown files or create new ones.
- **Customizable:** Easily extend or adapt for different project structures.

## Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/yourusername/genai-diagram-generator.git
cd genai-diagram-generator
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up your API key:**

- Ensure you have an OpenAI API key set in your environment variables.

4. **Run the generator:**

```bash
python main.py <input_directory> --output README.md
```

- Use `--apend` if you want to append to an existing file.

## Example

See [`samples/nextjs_mermaid_example.md`](samples/nextjs_mermaid_example.md) for a sample output.

## License

This project is licensed under the MIT License. Do whatever you want with it!

## Acknowledgements

- Inspired by [MermaidJS](https://mermaid-js.github.io/).
- Example SaaS starter code sample from [Vercel's Next.js SaaS Starter](https://github.com/vercel/nextjs-saas-starter) (MIT License).
- Uses [OpenAI](https://platform.openai.com/) for code summarization and relationship inference.

## Contributing

Contributions are welcome! Please open issues or submit pull requests to help improve this project. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## MermaidJS Diagram - Generated via Automation
