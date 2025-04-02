"""
REST Server module for the Core functionality.

This module provides a server for hosting REST API endpoints.
"""

import threading
import time
import json
from typing import Any, Dict, Optional, List

from fastapi import FastAPI, APIRouter, Request, Response
import uvicorn

from .logging import setup_logging


class RestServer:
    """Server for providing REST API endpoints."""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        """Initialize the REST server.
        
        Args:
            host: Host to bind to
            port: Port to bind to
        """
        self._host = host
        self._port = port
        self._app = FastAPI(title="Cerebritron API")
        self._server = None
        self._server_thread = None
        self._lock = threading.RLock()
        self._initialized = False
        self._logger = setup_logging(__name__)
    
    def initialize(self) -> bool:
        """Initialize the REST server.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        with self._lock:
            if self._initialized:
                return True
            
            try:
                self._logger.info("Initializing REST server")
                
                # Start server thread
                self._server_thread = threading.Thread(
                    target=self._run_server,
                    daemon=True,
                    name="rest-server"
                )
                self._server_thread.start()
                
                # Wait for server to start
                time.sleep(1.0)
                
                self._initialized = True
                self._logger.info(f"REST server initialized successfully at http://{self._host}:{self._port}")
                return True
            except Exception as e:
                self._logger.error(f"Error initializing REST server: {e}")
                return False
    
    def shutdown(self) -> bool:
        """Shutdown the REST server.
        
        Returns:
            True if shutdown was successful, False otherwise
        """
        with self._lock:
            if not self._initialized:
                return True
            
            try:
                self._logger.info("Shutting down REST server")
                
                # Stop server
                if self._server:
                    self._server.should_exit = True
                    self._server = None
                
                # Wait for server thread to stop
                if self._server_thread:
                    self._server_thread.join(timeout=5.0)
                    self._server_thread = None
                
                self._initialized = False
                self._logger.info("REST server shutdown successfully")
                return True
            except Exception as e:
                self._logger.error(f"Error shutting down REST server: {e}")
                return False
    
    def add_router(self, router: APIRouter, prefix: str = "") -> None:
        """Add a router to the server.
        
        Args:
            router: Router to add
            prefix: Prefix for router routes (optional)
        """
        self._app.include_router(router, prefix=prefix)
    
    def _run_server(self) -> None:
        """Run the server."""
        self._logger.info(f"Starting REST server on {self._host}:{self._port}")
        
        try:
            # Create and run server
            config = uvicorn.Config(
                app=self._app,
                host=self._host,
                port=self._port,
                log_level="error"
            )
            self._server = uvicorn.Server(config)
            self._server.run()
        except Exception as e:
            self._logger.error(f"Error running REST server: {e}")
