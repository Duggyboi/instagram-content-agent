"""
LLM Configuration Module

Provides LLM initialization based on environment configuration.
Supports both OpenAI and Ollama (local models).
"""

import os
from typing import Optional


def get_llm_config():
    """
    Get LLM configuration based on environment variables.
    
    Checks for:
    1. OLLAMA_MODEL and OLLAMA_BASE_URL (for local models)
    2. OPENAI_API_KEY and OPENAI_MODEL (for OpenAI API)
    
    Returns:
        dict: Configuration for creating an LLM instance via CrewAI
    """
    
    # Check for Ollama configuration
    ollama_model = os.getenv("OLLAMA_MODEL")
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    if ollama_model:
        return {
            "provider": "ollama",
            "model": ollama_model,
            "base_url": ollama_url,
        }
    
    # Fall back to OpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    if openai_key and openai_key != "sk-your-api-key-here":
        return {
            "provider": "openai",
            "model": openai_model,
            "api_key": openai_key,
        }
    
    # No valid config found
    raise ValueError(
        "No valid LLM configuration found!\n"
        "Please configure either:\n"
        "  - OLLAMA_MODEL (for local models)\n"
        "  - OPENAI_API_KEY (for OpenAI API)\n"
        "in your .env file"
    )


def print_llm_config():
    """Print the current LLM configuration for debugging."""
    try:
        config = get_llm_config()
        print(f"\n✓ LLM Configuration:")
        print(f"  Provider: {config['provider']}")
        print(f"  Model: {config['model']}")
        if config['provider'] == 'ollama':
            print(f"  Base URL: {config['base_url']}")
        print()
    except ValueError as e:
        print(f"\n❌ {e}")
