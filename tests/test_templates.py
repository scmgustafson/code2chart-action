from prompts import templates
import config

def test_summarize_key_files_prompt_includes_data():
    data = "file1.py: print('hello')"
    result = templates.summarize_key_files_prompt(data)

    # Check formatting and f string
    assert result.startswith("You are summarizing the purpose")
    assert "The file data is as follows:" in result
    assert data in result


def test_determine_relationships_prompt_includes_data():
    data = "- file1 depends on file2"
    result = templates.determine_relationships_prompt(data)

    # Check formatting and f string
    assert result.startswith("Based on the summary of files below")
    assert "infer the relationships between modules" in result
    assert data in result


def test_output_mermaid_prompt_includes_data_and_example():
    data = "moduleA --> moduleB"
    result = templates.output_mermaid_prompt(data)
    assert "Generate a Mermaid diagram" in result
    assert "Available MermaidJS themes:" in result
    assert "Available arrow types:" in result
    assert "Here is an example of MermaidJS syntax" in result
    assert "\n\Data to generate Mermaid from:" in result
    assert data in result