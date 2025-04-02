"""
Logging utilities for the Cerebritron system.

This module provides functionality for setting up logging across all components
of the Cerebritron system.
"""

import logging
import logging.handlers
import os
import colorlog

def setup_logging(name):
    """Configures Cerebritron logger with hourly rotation and color formatting"""
    
    # Create a directory for logs if it doesn't exist
    log_dir='logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Format for file (without colors)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Format for console (with colors)
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    
    # Handler for file with hourly rotation
    file_handler = logging.handlers.TimedRotatingFileHandler(
        filename=os.path.join(log_dir, f'{name}.log'),
        when='H',
        interval=1,
        backupCount=168,  # Store logs from the last 7 days (24*7=168 hours)
        encoding='utf-8',
        delay=True  # Delay file creation until the first write
    )
    file_handler.setFormatter(file_formatter)
    
    # Handler for console with colors
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
