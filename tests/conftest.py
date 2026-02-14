"""
Test configuration and utilities
"""

import pytest
from src.config import load_config


@pytest.fixture
def config():
    """Fixture to provide configuration for tests"""
    return load_config()
