"""
Configuration Manager for secure storage and retrieval of configuration and secrets.

This module provides functionality for storing and retrieving configuration values
and sensitive information like API keys and passwords.
"""

import os
import json
import base64
import threading
from typing import Any, Dict, List, Optional, Set, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from .logging import setup_logging


class ConfigurationManager:
    """Manages configuration and secrets for the system."""
    
    def __init__(self, config_dir: Optional[str] = None, master_password: Optional[str] = None):
        """Initialize the configuration manager.
        
        Args:
            config_dir: Directory for storing configuration files (optional)
            master_password: Master password for encrypting secrets (optional)
        """
        self._config_dir = config_dir or os.path.expanduser("~/.cerebritron/config")
        self._master_password = master_password or os.environ.get("CEREBRITRON_MASTER_PASSWORD", "default_password")
        self._config_file = os.path.join(self._config_dir, "config.json")
        self._secrets_file = os.path.join(self._config_dir, "secrets.enc")
        self._config = {}
        self._secrets = {}
        self._key = None
        self._lock = threading.RLock()
        self._initialized = False
        self._logger = setup_logging(__name__)
    
    def initialize(self) -> bool:
        """Initialize the configuration manager.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        with self._lock:
            if self._initialized:
                return True
            
            try:
                self._logger.info("Initializing configuration manager")
                
                # Create config directory if it doesn't exist
                os.makedirs(self._config_dir, exist_ok=True)
                
                # Generate encryption key from master password
                self._generate_key()
                
                # Load configuration
                self._load_config()
                
                # Load secrets
                self._load_secrets()
                
                self._initialized = True
                self._logger.info("Configuration manager initialized successfully")
                return True
            except Exception as e:
                self._logger.error(f"Error initializing configuration manager: {e}")
                return False
    
    def shutdown(self) -> bool:
        """Shutdown the configuration manager.
        
        Returns:
            True if shutdown was successful, False otherwise
        """
        with self._lock:
            if not self._initialized:
                return True
            
            try:
                self._logger.info("Shutting down configuration manager")
                
                # Save configuration
                self._save_config()
                
                # Save secrets
                self._save_secrets()
                
                self._initialized = False
                self._logger.info("Configuration manager shutdown successfully")
                return True
            except Exception as e:
                self._logger.error(f"Error shutting down configuration manager: {e}")
                return False
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.
        
        Args:
            key: Key to get the value for
            default: Default value to return if key is not found
            
        Returns:
            Configuration value if found, default otherwise
        """
        with self._lock:
            # Split key into parts
            parts = key.split(".")
            
            # Navigate through config
            current = self._config
            for part in parts[:-1]:
                if part not in current or not isinstance(current[part], dict):
                    return default
                current = current[part]
            
            # Get value
            return current.get(parts[-1], default)
    
    def set_config(self, key: str, value: Any) -> bool:
        """Set a configuration value.
        
        Args:
            key: Key to set the value for
            value: Value to set
            
        Returns:
            True if setting was successful, False otherwise
        """
        with self._lock:
            try:
                # Split key into parts
                parts = key.split(".")
                
                # Navigate through config
                current = self._config
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    elif not isinstance(current[part], dict):
                        current[part] = {}
                    current = current[part]
                
                # Set value
                current[parts[-1]] = value
                
                # Save configuration
                self._save_config()
                
                return True
            except Exception as e:
                self._logger.error(f"Error setting configuration: {e}")
                return False
    
    def get_secret(self, key: str) -> Optional[str]:
        """Get a secret value.
        
        Args:
            key: Key to get the value for
            
        Returns:
            Secret value if found, None otherwise
        """
        with self._lock:
            return self._secrets.get(key)
    
    def set_secret(self, key: str, value: str) -> bool:
        """Set a secret value.
        
        Args:
            key: Key to set the value for
            value: Value to set
            
        Returns:
            True if setting was successful, False otherwise
        """
        with self._lock:
            try:
                # Set value
                self._secrets[key] = value
                
                # Save secrets
                self._save_secrets()
                
                return True
            except Exception as e:
                self._logger.error(f"Error setting secret: {e}")
                return False
    
    def delete_config(self, key: str) -> bool:
        """Delete a configuration value.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        with self._lock:
            try:
                # Split key into parts
                parts = key.split(".")
                
                # Navigate through config
                current = self._config
                for part in parts[:-1]:
                    if part not in current or not isinstance(current[part], dict):
                        return True  # Key doesn't exist, nothing to delete
                    current = current[part]
                
                # Delete value
                if parts[-1] in current:
                    del current[parts[-1]]
                
                # Save configuration
                self._save_config()
                
                return True
            except Exception as e:
                self._logger.error(f"Error deleting configuration: {e}")
                return False
    
    def delete_secret(self, key: str) -> bool:
        """Delete a secret value.
        
        Args:
            key: Key to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        with self._lock:
            try:
                # Delete value
                if key in self._secrets:
                    del self._secrets[key]
                
                # Save secrets
                self._save_secrets()
                
                return True
            except Exception as e:
                self._logger.error(f"Error deleting secret: {e}")
                return False
    
    def _generate_key(self) -> None:
        """Generate encryption key from master password."""
        try:
            # Generate salt
            salt = b'cerebritron_salt'
            
            # Generate key
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            
            # Derive key from password
            key = base64.urlsafe_b64encode(kdf.derive(self._master_password.encode()))
            
            # Create Fernet cipher
            self._key = Fernet(key)
        except Exception as e:
            self._logger.error(f"Error generating encryption key: {e}")
            raise
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        try:
            # Check if config file exists
            if os.path.exists(self._config_file):
                # Load config
                with open(self._config_file, "r") as f:
                    self._config = json.load(f)
            else:
                # Create empty config
                self._config = {}
                
                # Save config
                self._save_config()
        except Exception as e:
            self._logger.error(f"Error loading configuration: {e}")
            # Create empty config
            self._config = {}
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            # Save config
            with open(self._config_file, "w") as f:
                json.dump(self._config, f, indent=2)
        except Exception as e:
            self._logger.error(f"Error saving configuration: {e}")
            raise
    
    def _load_secrets(self) -> None:
        """Load secrets from file."""
        try:
            # Check if secrets file exists
            if os.path.exists(self._secrets_file):
                # Load secrets
                with open(self._secrets_file, "rb") as f:
                    encrypted_data = f.read()
                
                # Decrypt secrets
                decrypted_data = self._key.decrypt(encrypted_data)
                
                # Parse secrets
                self._secrets = json.loads(decrypted_data.decode())
            else:
                # Create empty secrets
                self._secrets = {}
                
                # Save secrets
                self._save_secrets()
        except Exception as e:
            self._logger.error(f"Error loading secrets: {e}")
            # Create empty secrets
            self._secrets = {}
    
    def _save_secrets(self) -> None:
        """Save secrets to file."""
        try:
            # Convert secrets to JSON
            data = json.dumps(self._secrets).encode()
            
            # Encrypt secrets
            encrypted_data = self._key.encrypt(data)
            
            # Save secrets
            with open(self._secrets_file, "wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            self._logger.error(f"Error saving secrets: {e}")
            raise
