import pytest # type: ignore
from utilities import ai_requests

def test_summarize_key_files_mocks_api(monkeypatch):
    # Mock prompt_model to avoid real API call
    monkeypatch.setattr(ai_requests, "prompt_model", lambda prompt: "summary")
    result = ai_requests.summarize_key_files("some data")
    assert result == "summary"

def test_determine_relationships_mocks_api(monkeypatch):
    monkeypatch.setattr(ai_requests, "prompt_model", lambda prompt: "relationships")
    result = ai_requests.determine_relationships("some summary")
    assert result == "relationships"

def test_output_mermaid_mocks_api(monkeypatch):
    monkeypatch.setattr(ai_requests, "prompt_model", lambda prompt: "mermaid_output")
    monkeypatch.setattr(ai_requests.file_utils, "is_mermaid_syntax", lambda mermaid: True)
    data = [{"file": "file1.py"}, {"file": "file2.py"}]
    result = ai_requests.output_mermaid(data)
    assert result == "mermaid_output"

def test_chunk_by_tokens_chunks(monkeypatch):
    # Mock summarize_key_files to avoid API call
    monkeypatch.setattr(ai_requests, "summarize_key_files", lambda chunk_prompt: f"summary:{chunk_prompt[:10]}")
    # Mock tiktoken encoding
    class DummyEnc:
        def encode(self, s):
            return [1] * len(s)
    monkeypatch.setattr(ai_requests, "tiktoken", type("DummyTiktoken", (), {"encoding_for_model": lambda model: DummyEnc(), "get_encoding": lambda name: DummyEnc()}))
    file_data_map = {
        "file1.py": "a" * 5,
        "file2.py": "b" * 5,
        "file3.py": "c" * 5,
    }
    result = ai_requests.chunk_by_tokens(file_data_map, max_tokens=5)
    assert isinstance(result, dict)
    assert all("summary:" in v for v in result.values())