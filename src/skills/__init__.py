"""
Skill management and definitions
"""

from typing import Callable, Optional, Any
from dataclasses import dataclass


@dataclass
class Skill:
    """Base skill class"""

    name: str
    description: str
    execute: Callable
    parameters: Optional[dict] = None

    def run(self, *args, **kwargs) -> Any:
        """Execute the skill"""
        return self.execute(*args, **kwargs)


class SkillManager:
    """Manages skills registry and execution"""

    def __init__(self):
        self.skills = {}

    def register_skill(self, skill: Skill) -> None:
        """Register a new skill"""
        self.skills[skill.name] = skill

    def get_skill(self, name: str) -> Optional[Skill]:
        """Retrieve a registered skill by name"""
        return self.skills.get(name)

    def execute_skill(self, skill_name: str, *args, **kwargs) -> Any:
        """Execute a registered skill"""
        skill = self.get_skill(skill_name)
        if skill is None:
            raise ValueError(f"Skill '{skill_name}' not found")
        return skill.run(*args, **kwargs)

    def list_skills(self) -> list:
        """List all registered skills"""
        return list(self.skills.keys())


# Global skill manager instance
_skill_manager: Optional[SkillManager] = None


def get_skill_manager() -> SkillManager:
    """Get or create the global skill manager"""
    global _skill_manager
    if _skill_manager is None:
        _skill_manager = SkillManager()
    return _skill_manager
