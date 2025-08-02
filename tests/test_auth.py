import importlib
import pytest # type: ignore
from utilities import auth

def test_check_for_api_key_raises(monkeypatch):
    # Unset env
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # Import module to access credentials
    import utilities.auth

    # Patch credentials fallback
    # Only patch if credentials is not None
    if utilities.auth.credentials is not None:
        monkeypatch.setattr(utilities.auth.credentials, "OPENAI_API_KEY", None)

    # Reload auth so it re-evaluates the patched credentials
    importlib.reload(utilities.auth)

    # Now this should raise
    with pytest.raises(Exception, match="OpenAI API key not set"):
        utilities.auth.check_for_api_key()

def test_check_for_api_key_env(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-api-key-env")

    # Reload module to pick up the new env
    importlib.reload(auth)

    # Should not raise
    auth.check_for_api_key()

def test_check_for_api_key_credentials_file(monkeypatch):
    # Unset env
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # Import module to access credentials and patch credentials attribute to make sure its set
    import utilities.auth
    monkeypatch.setattr(utilities.auth.credentials, "OPENAI_API_KEY", "fake-api-key-from-file")

    # Reload module to pick up the new env
    importlib.reload(auth)

    # Should not raise
    auth.check_for_api_key()
