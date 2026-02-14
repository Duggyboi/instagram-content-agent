"""
Basic tests for configuration loading
"""

from src.config import load_config, get_config, Settings


def test_load_config():
    """Test that configuration loads successfully"""
    config = load_config()
    assert isinstance(config, Settings)


def test_get_config():
    """Test that get_config returns the same instance as load_config"""
    config1 = load_config()
    config2 = get_config()
    assert config1 is config2


def test_agent_config(config):
    """Test agent configuration settings"""
    assert config.agent.max_iterations == 10
    assert config.agent.timeout == 300


def test_llm_config(config):
    """Test LLM configuration"""
    assert config.llm.openai_model == "gpt-4"


def test_logging_config(config):
    """Test logging configuration"""
    assert config.logging.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
