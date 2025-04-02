"""
Security utilities for the Cerebritron system.

This module provides functionality for security-related operations such as
encryption, decryption, and secure storage of sensitive information.
"""

import base64
import os
from typing import Any, Dict, Optional

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecureStorage:
    """Provides secure storage for sensitive information."""
    
    def __init__(self, key: Optional[bytes] = None, password: Optional[str] = None):
        """Initialize the secure storage.
        
        Args:
            key: Encryption key (optional)
            password: Password for deriving key (optional)
        """
        if key:
            self._key = key
        elif password:
            self._key = self._derive_key_from_password(password)
        else:
            self._key = Fernet.generate_key()
        
        self._cipher = Fernet(self._key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt data.
        
        Args:
            data: Data to encrypt
            
        Returns:
            Encrypted data as a base64-encoded string
        """
        encrypted_data = self._cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data.
        
        Args:
            encrypted_data: Encrypted data as a base64-encoded string
            
        Returns:
            Decrypted data
        """
        decoded_data = base64.b64decode(encrypted_data)
        decrypted_data = self._cipher.decrypt(decoded_data)
        return decrypted_data.decode()
    
    def get_key(self) -> bytes:
        """Get the encryption key.
        
        Returns:
            Encryption key
        """
        return self._key
    
    def _derive_key_from_password(self, password: str, salt: Optional[bytes] = None) -> bytes:
        """Derive an encryption key from a password.
        
        Args:
            password: Password to derive key from
            salt: Salt for key derivation (optional)
            
        Returns:
            Derived key
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key


def hash_password(password: str) -> str:
    """Hash a password.
    
    Args:
        password: Password to hash
        
    Returns:
        Hashed password
    """
    import hashlib
    
    # Generate a random salt
    salt = os.urandom(32)
    
    # Hash the password with the salt
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        100000
    )
    
    # Combine salt and hash
    storage = salt + hash_obj
    
    # Return as a hex string
    return storage.hex()


def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a password against a stored hash.
    
    Args:
        stored_password: Stored password hash
        provided_password: Password to verify
        
    Returns:
        True if the password is correct, False otherwise
    """
    import hashlib
    
    # Convert stored password from hex to bytes
    storage = bytes.fromhex(stored_password)
    
    # Extract salt
    salt = storage[:32]
    
    # Extract stored hash
    stored_hash = storage[32:]
    
    # Hash the provided password with the same salt
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode(),
        salt,
        100000
    )
    
    # Compare hashes
    return hash_obj == stored_hash
