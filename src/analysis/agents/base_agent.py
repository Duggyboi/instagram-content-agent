"""
Base Agent class - all analysis agents inherit from this
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """Abstract base class for all analysis agents"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
    
    @abstractmethod
    def execute(self, input_data: str) -> str:
        """
        Execute the agent's analysis
        
        Args:
            input_data: Input data (usually file path or text)
            
        Returns:
            Analysis result as string
        """
        pass
    
    def _validate_input(self, input_data: str) -> bool:
        """Validate input data"""
        if not input_data:
            return False
        return True
