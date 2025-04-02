"""
Communication module for the Core functionality.

This module provides messaging and communication capabilities between
different components of the system.
"""

# Import the individual communication components
from .message_broker import MessageBroker
from .rest_client import RestClient
from .rest_server import RestServer

# Export the classes for backward compatibility
__all__ = ["MessageBroker", "RestClient", "RestServer"]
