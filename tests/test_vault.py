import os
import pytest
from cryptography.fernet import Fernet
from src.security.vault import Vault

def test_vault_generate_key():
    """Test the static method generate_key returns a valid Fernet key."""
    key = Vault.generate_key()
    assert isinstance(key, bytes)
    # A valid fernet key string should be url-safe base64 encoded, length 44
    assert len(key) == 44
    
def test_vault_initialization_with_explicit_key():
    """Test that Vault can be initialized with an explicit key."""
    key = Vault.generate_key()
    vault = Vault(key=key)
    assert vault.key == key

def test_vault_initialization_missing_key(monkeypatch):
    """Test that Vault raises ValueError if NPO_MASTER_KEY is missing."""
    monkeypatch.delenv("NPO_MASTER_KEY", raising=False)
    with pytest.raises(ValueError, match="Master key is missing"):
        Vault()

def test_vault_initialization_with_env_key(monkeypatch):
    """Test that Vault properly loads key from environment variable."""
    key = Vault.generate_key()
    monkeypatch.setenv("NPO_MASTER_KEY", key.decode("utf-8"))
    vault = Vault()
    assert vault.key == key

def test_vault_encrypt_decrypt():
    """Test encryption and decryption roundtrip."""
    key = Vault.generate_key()
    vault = Vault(key=key)
    
    original_secret = "gemini_api_key_12345"
    encrypted = vault.encrypt_api_key(original_secret)
    
    assert isinstance(encrypted, bytes)
    assert encrypted != original_secret.encode("utf-8")
    
    decrypted = vault.decrypt_api_key(encrypted)
    assert decrypted == original_secret

def test_vault_decrypt_invalid_token():
    """Test that decryption fails if token is invalid or tampered with."""
    key = Vault.generate_key()
    vault = Vault(key=key)
    
    # Encrypt some text
    encrypted = vault.encrypt_api_key("secret")
    
    # Tamper with the encrypted bytes
    tampered = encrypted[:-1] + (b"0" if encrypted[-1:] != b"0" else b"1")
    
    from cryptography.fernet import InvalidToken
    with pytest.raises(InvalidToken):
        vault.decrypt_api_key(tampered)
