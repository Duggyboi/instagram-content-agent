"""
Ollama LLM Initialization

Creates configured LLM instances for CrewAI agents using Ollama.
"""

import os
from crewai import LLM


def get_ollama_llm():
    """
    Create an LLM instance configured for Ollama using CrewAI's LLM class.
    
    Returns:
        LLM: CrewAI LLM configured to use ollama provider
    """
    model = os.getenv("OLLAMA_MODEL", "mistral")
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    # LiteLLM format for Ollama: ollama/model-name
    return LLM(
        model=f"ollama/{model}",
        base_url=base_url,
    )

