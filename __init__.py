"""
Core module for Cerebritron

This module provides shared functionality used by all layers of the Cerebritron system.
"""

from .config import ConfigurationManager
from .communication import MessageBroker, RestClient, RestServer
from .logging import setup_logging
from .security import SecureStorage

__all__ = [
    'ConfigurationManager',
    'MessageBroker',
    'RestClient',
    'RestServer',
    'setup_logging',
    'SecureStorage'
]
