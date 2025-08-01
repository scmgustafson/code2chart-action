import os
import pytest # type: ignore
import importlib

import main

def test_check_apend_to_existing_file_raises(tmp_path):
    dest_file = tmp_path / "README.md"
    dest_file.write_text("existing content")
    with pytest.raises(Exception, match="Attempting to write Mermaid to existing file"):
        main.check_apend_to_existing_file(str(dest_file), is_apend=False)

def test_check_apend_to_existing_file_allows_append(tmp_path):
    dest_file = tmp_path / "README.md"
    dest_file.write_text("existing content")
    main.check_apend_to_existing_file(str(dest_file), is_apend=True)

def test_check_apend_to_existing_file_new_file(tmp_path):
    dest_file = tmp_path / "NEWFILE.md"
    main.check_apend_to_existing_file(str(dest_file), is_apend=False)
