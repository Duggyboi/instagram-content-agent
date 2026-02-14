"""
Agentic Infrastructure Framework - Skills Module

This module contains all reusable skills that agents can utilize.
Skills are modular, single-purpose tools that encapsulate specific
functionality and can be shared across multiple agents.

Structure:
    skills/
    ├── __init__.py
    ├── logging_skill.py
    ├── repo_management_skill.py
    ├── code_quality_skill.py
    └── [your_skill_name].py

To create a new skill:
    1. Copy templates/SKILL_TEMPLATE.md
    2. Implement in skills/[name]_skill.py
    3. Register in ../skills.json
    4. Import in agents that need it

See templates/SKILL_TEMPLATE.md for detailed guide.
"""

# Core skills available in this module
try:
    from .logging_skill import log_action, log_error
except ImportError:
    pass

try:
    from .repo_management_skill import git_status, git_commit
except ImportError:
    pass

try:
    from .code_quality_skill import (
        run_black_format,
        run_flake8_lint
    )
except ImportError:
    pass

__all__ = [
    "log_action",
    "log_error",
    "git_status",
    "git_commit",
    "run_black_format",
    "run_flake8_lint",
]

__version__ = "0.1.0"
