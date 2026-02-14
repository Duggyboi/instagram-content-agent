"""
Tool integrations and utilities
"""

from typing import Callable, Optional, Dict, Any
from langchain.tools import Tool


def create_tool(
    name: str,
    description: str,
    func: Callable,
    **kwargs
) -> Tool:
    """
    Create a LangChain tool from a function

    Args:
        name: The name of the tool
        description: The description of what the tool does
        func: The callable function that implements the tool
        **kwargs: Additional arguments to pass to Tool

    Returns:
        Tool: A LangChain Tool instance
    """
    return Tool(
        name=name,
        description=description,
        func=func,
        **kwargs
    )


class ToolManager:
    """Manages tool registry"""

    def __init__(self):
        self.tools: Dict[str, Tool] = {}

    def register_tool(self, tool: Tool) -> None:
        """Register a new tool"""
        self.tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name"""
        return self.tools.get(name)

    def get_all_tools(self) -> list:
        """Get all registered tools"""
        return list(self.tools.values())

    def list_tools(self) -> list:
        """List all registered tool names"""
        return list(self.tools.keys())
