"""
Health check module for Cerebritron services.

This module provides health check functionality for all Cerebritron services.
"""

import os
import time
import threading
import json
from typing import Dict, Any, Optional, List, Callable
import requests

from .logging import setup_logging


class HealthCheck:
    """Health check functionality for Cerebritron services."""
    
    def __init__(self, service_name: str, component_status_callback: Optional[Callable[[], Dict[str, bool]]] = None):
        """Initialize the health check.
        
        Args:
            service_name: Name of the service
            component_status_callback: Callback to get component status (optional)
        """
        self._service_name = service_name
        self._component_status_callback = component_status_callback
        self._dependencies = {}
        self._lock = threading.RLock()
        self._health_data = {
            "status": "initializing",
            "components": {},
            "dependencies": {},
            "timestamp": time.time()
        }
        self._logger = setup_logging(__name__)
    
    def add_dependency(self, name: str, url: str) -> None:
        """Add a dependency to check.
        
        Args:
            name: Name of the dependency
            url: URL to check
        """
        with self._lock:
            self._dependencies[name] = url
    
    def remove_dependency(self, name: str) -> None:
        """Remove a dependency.
        
        Args:
            name: Name of the dependency
        """
        with self._lock:
            if name in self._dependencies:
                del self._dependencies[name]
    
    def check_health(self) -> Dict[str, Any]:
        """Check health of the service and its dependencies.
        
        Returns:
            Health status data
        """
        with self._lock:
            # Get component status
            if self._component_status_callback:
                self._health_data["components"] = self._component_status_callback()
            
            # Check dependencies
            for name, url in self._dependencies.items():
                try:
                    # Make health check request
                    response = requests.get(f"{url}/health", timeout=5.0)
                    
                    # Parse response
                    if response.status_code == 200:
                        health_data = response.json()
                        
                        # Update dependency health data
                        self._health_data["dependencies"][name] = {
                            "status": health_data.get("status", "unknown"),
                            "timestamp": time.time()
                        }
                    else:
                        # Dependency is unhealthy
                        self._health_data["dependencies"][name] = {
                            "status": "unhealthy",
                            "error": f"Health check failed with status code {response.status_code}",
                            "timestamp": time.time()
                        }
                except Exception as e:
                    # Dependency is unreachable
                    self._health_data["dependencies"][name] = {
                        "status": "unreachable",
                        "error": str(e),
                        "timestamp": time.time()
                    }
            
            # Determine overall status
            if all(self._health_data["components"].values()) and all(
                dep.get("status") == "healthy" for dep in self._health_data["dependencies"].values()
            ):
                self._health_data["status"] = "healthy"
            else:
                self._health_data["status"] = "unhealthy"
            
            # Update timestamp
            self._health_data["timestamp"] = time.time()
            
            return self._health_data.copy()
    
    def get_health(self) -> Dict[str, Any]:
        """Get the current health status.
        
        Returns:
            Health status data
        """
        with self._lock:
            return self._health_data.copy()
    
    def set_status(self, status: str) -> None:
        """Set the overall status.
        
        Args:
            status: Status to set
        """
        with self._lock:
            self._health_data["status"] = status
            self._health_data["timestamp"] = time.time()
    
    def set_component_status(self, component: str, status: bool) -> None:
        """Set the status of a component.
        
        Args:
            component: Component name
            status: Component status
        """
        with self._lock:
            self._health_data["components"][component] = status
            self._health_data["timestamp"] = time.time()
