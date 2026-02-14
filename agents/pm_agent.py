"""
PM Agent - Project Manager Agent

The PM (Project Manager) Agent is responsible for:
- Task decomposition and delegation
- Agent lifecycle management
- Progress tracking and reporting
- Decision-making and escalation
- Overall project coordination

This agent serves as the central coordinator for the agentic framework.
"""

from crewai import Agent
from typing import Optional
import logging
import os

logger = logging.getLogger(__name__)

# Configuration
PM_AGENT_VERBOSE = os.getenv("PM_AGENT_VERBOSE", "true").lower() == "true"
PM_AGENT_MEMORY = os.getenv("PM_AGENT_MEMORY", "full")  # full, summary, or none


def create_pm_agent(
    name: str = "PM Agent",
    allow_delegation: bool = True,
    verbose: Optional[bool] = None,
    tools: Optional[list] = None,
) -> Agent:
    """
    Create a new PM (Project Manager) Agent.
    
    Args:
        name: Name for this PM agent instance
        allow_delegation: Whether this PM can delegate to other agents
        verbose: Enable detailed logging (uses env var if not specified)
        tools: Skills/tools the agent has access to
        
    Returns:
        Configured CrewAI Agent ready for use
        
    Example:
        >>> pm = create_pm_agent()
        >>> # Use pm in a Crew with other agents
    """
    
    verbose = verbose if verbose is not None else PM_AGENT_VERBOSE
    tools = tools or []
    
    try:
        # Import skills the PM agent needs
        from skills.logging_skill import log_action, log_error
        from skills.repo_management_skill import git_status, git_commit, git_push
        
        # Add default tools if not provided
        if not tools:
            tools = [log_action, log_error, git_status]
        
    except ImportError:
        logger.warning("Could not import default PM agent skills")
    
    agent = Agent(
        role="Project Manager",
        goal=(
            "Coordinate and manage the agentic framework project. "
            "Decompose complex tasks into manageable subtasks, "
            "delegate to appropriate agents, track progress, "
            "and escalate blockers or decisions that require human input."
        ),
        backstory=(
            "You are an experienced project manager with expertise in "
            "coordinating autonomous agents. You excel at task decomposition, "
            "identifying dependencies, managing timelines, and making "
            "strategic decisions. You communicate clearly with team members "
            "and stakeholders, and you're not afraid to escalate issues "
            "when needed."
        ),
        verbose=verbose,
        allow_delegation=allow_delegation,
        tools=tools,
        # agent_executor_kwargs={"max_iterations": 10}  # Uncomment to limit iterations
    )
    
    logger.info(f"Created PM Agent: {name}")
    return agent


# Example usage and testing
if __name__ == "__main__":
    from crewai import Task, Crew
    
    # Create PM agent
    pm = create_pm_agent()
    
    # Create a simple task
    task = Task(
        description="Review project setup and log status",
        agent=pm,
        expected_output="Project status report",
    )
    
    # Create crew and run
    crew = Crew(
        agents=[pm],
        tasks=[task],
        verbose=True,
    )
    
    print("Starting PM Agent...")
    result = crew.kickoff()
    print(f"\nResult:\n{result}")
