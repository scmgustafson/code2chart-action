import os
import tempfile
import shutil
import pytest # type: ignore
from utilities import file_utils

def test_get_file_data_map_reads_files(tmp_path):
    # Create a test directory and file
    test_dir = tmp_path / "testdir"
    test_dir.mkdir()
    test_file = test_dir / "file1.txt"
    test_file.write_text("hello world")

    # Should read the file and return its contents
    result = file_utils.get_file_data_map(str(test_dir))
    assert str(test_file) in result
    assert result[str(test_file)] == "hello world"

def test_get_file_data_map_ignores_patterns(tmp_path, monkeypatch):
    # Patch config to ignore .txt files
    monkeypatch.setattr(file_utils.config, "IGNORE_PATTERNS", (".txt",))
    test_dir = tmp_path / "testdir"
    test_dir.mkdir()
    test_file = test_dir / "file1.txt"
    test_file.write_text("should be ignored")
    result = file_utils.get_file_data_map(str(test_dir))
    assert str(test_file) not in result

def test_write_mermaid_to_file_creates_new_file(tmp_path, monkeypatch):
    # Patch config header/footer
    monkeypatch.setattr(file_utils.config, "MERMAID_HEADER", "HEADER")
    monkeypatch.setattr(file_utils.config, "MERMAID_FOOTER", "FOOTER")
    dest_file = tmp_path / "mermaid.md"
    mermaid = "graph TD; A-->B"
    file_utils.write_mermaid_to_file(str(dest_file), mermaid)
    content = dest_file.read_text()
    assert "HEADER" in content
    assert "FOOTER" in content
    assert mermaid in content

def test_write_mermaid_to_file_appends_to_existing(tmp_path, monkeypatch):
    monkeypatch.setattr(file_utils.config, "MERMAID_HEADER", "HEADER")
    monkeypatch.setattr(file_utils.config, "MERMAID_FOOTER", "FOOTER")
    dest_file = tmp_path / "mermaid.md"
    # Write initial content
    dest_file.write_text("existing content\n")
    mermaid = "graph TD; A-->B"
    file_utils.write_mermaid_to_file(str(dest_file), mermaid)
    content = dest_file.read_text()
    assert "existing content" in content
    assert "HEADER" in content
    assert "FOOTER" in content
    assert mermaid in content

def test_write_mermaid_to_file_replaces_existing_mermaid_block(tmp_path, monkeypatch):
    monkeypatch.setattr(file_utils.config, "MERMAID_HEADER", "HEADER")
    monkeypatch.setattr(file_utils.config, "MERMAID_FOOTER", "FOOTER")
    dest_file = tmp_path / "mermaid.md"
    # Write file with existing mermaid block
    dest_file.write_text("pre\nHEADER\nold_mermaid\nFOOTER\npost")
    new_mermaid = "graph TD; X-->Y"
    file_utils.write_mermaid_to_file(str(dest_file), new_mermaid)
    content = dest_file.read_text()
    assert "old_mermaid" not in content
    assert new_mermaid in content
    assert content.startswith("pre\nHEADER")