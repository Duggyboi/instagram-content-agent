"""
Agentic Infrastructure Framework - Agents Module

This module contains all agent definitions for the framework.
Agents are autonomous entities that execute tasks using skills.

Structure:
    agents/
    ├── __init__.py
    ├── pm_agent.py
    ├── dev_agent.py
    └── [your_agent_name].py

To create a new agent:
    1. Copy templates/AGENT_TEMPLATE.md
    2. Implement in agents/[name]_agent.py
    3. Import in this __init__.py if it's a core agent
    4. Follow naming conventions and patterns

See templates/AGENT_TEMPLATE.md for detailed guide.
"""

import logging

logger = logging.getLogger(__name__)

# Try to import core agents
try:
    from .pm_agent import create_pm_agent
except ImportError as e:
    logger.warning(f"Could not import PM agent: {e}")

try:
    from .dev_agent import create_dev_agent
except ImportError as e:
    logger.warning(f"Could not import Dev agent: {e}")

__all__ = [
    "create_pm_agent",
    "create_dev_agent",
]

__version__ = "0.1.0"
