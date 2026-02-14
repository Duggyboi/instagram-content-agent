"""
Agentic Infrastructure Framework
Main package initialization
"""

__version__ = "0.1.0"
__author__ = "DuggyBoi"

from src.config import load_config
from src.agents import create_agent

__all__ = [
    "load_config",
    "create_agent",
]
