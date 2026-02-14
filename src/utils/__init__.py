"""
Utility functions and helpers
"""

import logging
import json
from typing import Any, Dict
from datetime import datetime


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Setup logging configuration

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger("agentic_framework")
    logger.setLevel(getattr(logging, log_level))

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def log_json(data: Dict[str, Any], logger: logging.Logger) -> None:
    """
    Log data as JSON

    Args:
        data: Dictionary to log
        logger: Logger instance
    """
    logger.info(json.dumps(data, indent=2, default=str))


def get_timestamp() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now().isoformat()


def format_dict_for_display(data: Dict[str, Any]) -> str:
    """Format a dictionary for display in logs/output"""
    return json.dumps(data, indent=2, default=str)
