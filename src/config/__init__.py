"""
Configuration management for the agentic framework
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

# Load .env file
load_dotenv()


class AgentConfig(BaseSettings):
    """Agent configuration settings"""

    max_iterations: int = Field(default=10, env="MAX_ITERATIONS")
    timeout: int = Field(default=300, env="TIMEOUT")
    verbose: bool = Field(default=True, env="VERBOSE")


class LLMConfig(BaseSettings):
    """LLM provider configuration"""

    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4", env="OPENAI_MODEL")


class LoggingConfig(BaseSettings):
    """Logging configuration"""

    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")


class ProjectConfig(BaseSettings):
    """Project-level configuration"""

    project_name: str = Field(default="agentic-infrastructure-framework", env="PROJECT_NAME")
    environment: str = Field(default="development", env="ENVIRONMENT")


class Settings(BaseSettings):
    """Main settings class combining all configurations"""

    agent: AgentConfig = AgentConfig()
    llm: LLMConfig = LLMConfig()
    logging: LoggingConfig = LoggingConfig()
    project: ProjectConfig = ProjectConfig()

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def load_config() -> Settings:
    """
    Load and return the application configuration

    Returns:
        Settings: The loaded configuration object
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def get_config() -> Settings:
    """
    Get the current configuration (alias for load_config)

    Returns:
        Settings: The current configuration object
    """
    return load_config()
