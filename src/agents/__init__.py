"""
Agent creation and management utilities
"""

from typing import Optional, List
from crewai import Agent


def create_agent(
    name: str,
    role: str,
    goal: str,
    backstory: Optional[str] = None,
    tools: Optional[List] = None,
    verbose: bool = True,
) -> Agent:
    """
    Create a new agent with the specified configuration

    Args:
        name: The name of the agent
        role: The role/title of the agent
        goal: The goal the agent is trying to achieve
        backstory: Optional backstory/context for the agent
        tools: Optional list of tools the agent can use
        verbose: Whether to enable verbose output

    Returns:
        Agent: A configured CrewAI Agent instance
    """
    if backstory is None:
        backstory = f"An expert {role} dedicated to achieving the goal: {goal}"

    if tools is None:
        tools = []

    agent = Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        tools=tools,
        verbose=verbose,
    )

    return agent
