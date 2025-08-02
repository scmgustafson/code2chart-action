# Code2Chart Action — Auto-Generate MermaidJS Diagrams for Your Codebase

[![Code2Chart](https://img.shields.io/badge/GitHub-Marketplace-blue?logo=github)](https://github.com/marketplace/actions/code2chart)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Code2Chart** is a GitHub Action that uses OpenAI to automatically generate [MermaidJS](https://mermaid-js.github.io/) diagrams from your Python project source code. Visualize file structure, dependencies, and testing coverage — updated live with every PR or push.

> Keep your architecture diagrams fresh, automated, and documentation-friendly — straight from your CI.

---

## 📦 Features

- Uses `OpenAI` to analyze code and infer relationships between modules
- Outputs `MermaidJS` diagrams directly to your `README.md` or a markdown doc
- Supports integration into existing PR/CI workflows
- Append to or overwrite existing markdown content

---

## 🔧 Inputs

| Name      | Description                    | Required | Default |
| --------- | ------------------------------ | -------- | ------- |
| `api_key` | Your OpenAI API key            | ✅ Yes   | N/A     |
| `args`    | Arguments to pass to `main.py` | ❌ No    | `.`     |

---

## 🔐 Environment Variables / Secrets

| Name             | Description                  |
| ---------------- | ---------------------------- |
| `OPENAI_API_KEY` | Your OpenAI API key (secret) |

> ⚠️ Make sure to add `OPENAI_API_KEY` as a repository secret.

---

## Usage

### Minimal Example

```yaml
name: Generate Diagram

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Generate Mermaid Diagram
        uses: scmgustafson/code2chart-action@1.0
        with:
          api_key: ${{ secrets.OPENAI_API_KEY }}
```

### With Custom Arguments

```yaml
- name: Generate Diagram and Append
  uses: scmgustafson/code2chart-action@1.0
  with:
    api_key: ${{ secrets.OPENAI_API_KEY }}
    args: ". --append"
```

## Example Output

```
# MermaidJS example
graph LR
  main.py --> config.py
  main.py --> utilities/file_utils.py
  ...
```

See [samples/nextjs_mermaid_example.md](https://github.com/scmgustafson/code2chart/blob/main/samples/nextjs_mermaid_example.md) in the main repo for a full output example.

## License

MIT License. Do whatever you want — just don’t claim you wrote it all 😉

## Credits

- [MermaidJS](https://mermaid-js.github.io/)
- [OpenAI](https://openai.com/)

# Code2Chart as a Reusable GitHub Action

This repo is used for turning Code2Chart into a reusable, marketplace ready GitHub Action. See [the Code2Chart Main Repo](https://github.com/scmgustafson/code2chart) for more details.
