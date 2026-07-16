"""
Logging Configuration
Provides a configured logger for the SafeX AI Assistant.
"""

import logging
import sys
from datetime import datetime


def setup_logger(name: str = "safex", level: str = "INFO") -> logging.Logger:
    """
    Set up and return a logger with the given name and level.
    
    Args:
        name: Logger name (default: 'safex')
        level: Logging level (default: 'INFO')
    
    Returns:
        Configured logger instance
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


# Default application logger
app_logger = setup_logger("safex")