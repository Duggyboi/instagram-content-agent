"""
Configuration management for Streamlit application.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

CONFIG_DIR = Path.home() / ".instagram_agent"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class LLMConfig:
    """LLM configuration."""
    provider: str = "ollama"  # ollama, openai, anthropic
    model: str = "llama2:13b"
    temperature: float = 0.7
    max_tokens: int = 2000
    
    # Ollama specific
    ollama_host: str = "http://localhost:11434"
    
    # OpenAI specific
    openai_api_key: Optional[str] = None
    
    # Anthropic specific
    anthropic_api_key: Optional[str] = None


@dataclass
class StorageConfig:
    """Storage configuration."""
    results_dir: str = "results"
    logs_dir: str = "logs"
    temp_dir: str = "temp_uploads"
    max_result_age_days: int = 30
    auto_cleanup: bool = False


@dataclass
class AnalysisConfig:
    """Analysis pipeline configuration."""
    enable_transcription: bool = True
    enable_summary: bool = True
    enable_research: bool = True
    enable_categorization: bool = True
    enable_impact: bool = True
    
    # Transcription settings
    transcription_model: str = "base"  # base, small, medium, large
    
    # Summary settings
    summary_max_length: int = 200
    
    # Research settings
    max_research_links: int = 10
    
    # Parallel processing
    parallel_tasks: int = 2


@dataclass
class AppConfig:
    """Overall application configuration."""
    llm: LLMConfig
    storage: StorageConfig
    analysis: AnalysisConfig
    
    @classmethod
    def load(cls) -> "AppConfig":
        """Load configuration from disk or create defaults."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE) as f:
                    data = json.load(f)
                    return cls(
                        llm=LLMConfig(**data.get("llm", {})),
                        storage=StorageConfig(**data.get("storage", {})),
                        analysis=AnalysisConfig(**data.get("analysis", {}))
                    )
            except Exception as e:
                logger.warning(f"Failed to load config: {e}, using defaults")
        
        return cls(
            llm=LLMConfig(),
            storage=StorageConfig(),
            analysis=AnalysisConfig()
        )
    
    def save(self) -> None:
        """Save configuration to disk."""
        try:
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            
            data = {
                "llm": asdict(self.llm),
                "storage": asdict(self.storage),
                "analysis": asdict(self.analysis)
            }
            
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Configuration saved to {CONFIG_FILE}")
        
        except Exception as e:
            logger.error(f"Failed to save config: {e}")


# Global config instance
_config: Optional[AppConfig] = None


def get_config() -> AppConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = AppConfig.load()
    return _config


def load_config() -> AppConfig:
    """Load configuration from disk."""
    global _config
    _config = AppConfig.load()
    return _config


def save_config(config: AppConfig) -> None:
    """Save configuration to disk."""
    global _config
    _config = config
    config.save()
