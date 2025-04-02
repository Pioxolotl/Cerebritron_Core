"""
REST Client module for the Core functionality.

This module provides a client for making REST API requests.
"""

import threading
from typing import Any, Dict, Optional

import requests

from .logging import setup_logging


class RestClient:
    """Client for making REST API requests."""
    
    def __init__(self, base_url: Optional[str] = None):
        """Initialize the REST client.
        
        Args:
            base_url: Base URL for requests (optional)
        """
        self._base_url = base_url
        self._session = None
        self._lock = threading.RLock()
        self._initialized = False
        self._logger = setup_logging(__name__)
    
    def initialize(self) -> bool:
        """Initialize the REST client.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        with self._lock:
            if self._initialized:
                return True
            
            try:
                self._logger.info("Initializing REST client")
                
                # Create session
                self._session = requests.Session()
                
                self._initialized = True
                self._logger.info("REST client initialized successfully")
                return True
            except Exception as e:
                self._logger.error(f"Error initializing REST client: {e}")
                return False
    
    def shutdown(self) -> bool:
        """Shutdown the REST client.
        
        Returns:
            True if shutdown was successful, False otherwise
        """
        with self._lock:
            if not self._initialized:
                return True
            
            try:
                self._logger.info("Shutting down REST client")
                
                # Close session
                if self._session:
                    self._session.close()
                    self._session = None
                
                self._initialized = False
                self._logger.info("REST client shutdown successfully")
                return True
            except Exception as e:
                self._logger.error(f"Error shutting down REST client: {e}")
                return False
    
    def get(self, url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make a GET request.
        
        Args:
            url: URL to request
            params: Query parameters (optional)
            headers: Request headers (optional)
            
        Returns:
            Response data
        """
        if not self._initialized:
            self._logger.error("REST client not initialized")
            return {"error": "REST client not initialized"}
        
        try:
            # Build URL
            full_url = url
            if self._base_url and not url.startswith(("http://", "https://")):
                full_url = f"{self._base_url.rstrip('/')}/{url.lstrip('/')}"
            
            # Make request
            response = self._session.get(full_url, params=params, headers=headers)
            
            # Check if response is JSON
            if response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            else:
                return {"text": response.text, "status_code": response.status_code}
        except Exception as e:
            self._logger.error(f"Error making GET request: {e}")
            return {"error": str(e)}
    
    def post(self, url: str, data: Optional[Dict[str, Any]] = None, json_data: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Make a POST request.
        
        Args:
            url: URL to request
            data: Form data (optional)
            json_data: JSON data (optional)
            headers: Request headers (optional)
            
        Returns:
            Response data
        """
        if not self._initialized:
            self._logger.error("REST client not initialized")
            return {"error": "REST client not initialized"}
        
        try:
            # Build URL
            full_url = url
            if self._base_url and not url.startswith(("http://", "https://")):
                full_url = f"{self._base_url.rstrip('/')}/{url.lstrip('/')}"
            
            # Make request
            response = self._session.post(full_url, data=data, json=json_data, headers=headers)
            
            # Check if response is JSON
            if response.headers.get("Content-Type", "").startswith("application/json"):
                return response.json()
            else:
                return {"text": response.text, "status_code": response.status_code}
        except Exception as e:
            self._logger.error(f"Error making POST request: {e}")
            return {"error": str(e)}
