"""
Development Agent

The Development Agent is responsible for:
- Code generation and implementation
- Running tests and validation
- Code style enforcement
- Bug fixes and refactoring
- Technical decision-making

This agent handles all code-related tasks and can work independently
or collaborate with other agents.
"""

from crewai import Agent
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)

# Configuration
DEV_AGENT_VERBOSE = os.getenv("DEV_AGENT_VERBOSE", "true").lower() == "true"


def create_dev_agent(
    name: str = "Dev Agent",
    allow_delegation: bool = False,
    verbose: Optional[bool] = None,
    tools: Optional[list] = None,
) -> Agent:
    """
    Create a new Development Agent.
    
    Args:
        name: Name for this dev agent instance
        allow_delegation: Whether this agent can delegate to others
        verbose: Enable detailed logging (uses env var if not specified)
        tools: Skills/tools the agent has access to
        
    Returns:
        Configured CrewAI Agent ready for use
        
    Example:
        >>> dev = create_dev_agent()
        >>> # Use dev in a Crew to implement features
    """
    
    verbose = verbose if verbose is not None else DEV_AGENT_VERBOSE
    tools = tools or []
    
    try:
        # Import skills the Dev agent needs
        from skills.logging_skill import log_action, log_error
        from skills.repo_management_skill import git_commit, git_push, git_branch
        from skills.code_quality_skill import (
            run_black_format,
            run_flake8_lint,
            run_all_checks
        )
        
        # Add default tools if not provided
        if not tools:
            tools = [
                log_action,
                log_error,
                git_commit,
                git_push,
                git_branch,
                run_black_format,
                run_flake8_lint,
            ]
        
    except ImportError:
        logger.warning("Could not import default Dev agent skills")
    
    agent = Agent(
        role="Senior Developer",
        goal=(
            "Write clean, well-tested code that implements features "
            "according to specifications. Ensure code quality through "
            "testing, formatting, and best practices. Work efficiently "
            "and communicate progress clearly."
        ),
        backstory=(
            "You are a senior software engineer with deep expertise in "
            "Python and software architecture. You pride yourself on "
            "writing clean, maintainable code and have strong testing "
            "practices. You're proficient with version control, understand "
            "CI/CD principles, and can quickly adapt to new codebases and "
            "frameworks."
        ),
        verbose=verbose,
        allow_delegation=allow_delegation,
        tools=tools,
    )
    
    logger.info(f"Created Dev Agent: {name}")
    return agent


# Example usage and testing
if __name__ == "__main__":
    from crewai import Task, Crew
    
    # Create Dev agent
    dev = create_dev_agent()
    
    # Create a simple coding task
    task = Task(
        description=(
            "Review the code structure in the skills directory "
            "and ensure all files follow the project's coding standards. "
            "Run formatting and linting checks."
        ),
        agent=dev,
        expected_output="Code review report with any issues found and fixed",
    )
    
    # Create crew and run
    crew = Crew(
        agents=[dev],
        tasks=[task],
        verbose=True,
    )
    
    print("Starting Dev Agent...")
    result = crew.kickoff()
    print(f"\nResult:\n{result}")
