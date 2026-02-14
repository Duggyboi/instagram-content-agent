"""
Tests for agent creation and management
"""

from src.agents import create_agent


def test_create_agent():
    """Test creating a basic agent"""
    agent = create_agent(
        name="Test Agent",
        role="Test Role",
        goal="Test Goal"
    )
    assert agent is not None
    assert agent.role == "Test Role"
    assert agent.goal == "Test Goal"


def test_create_agent_with_backstory():
    """Test creating an agent with custom backstory"""
    backstory = "Custom backstory"
    agent = create_agent(
        name="Test Agent",
        role="Test Role",
        goal="Test Goal",
        backstory=backstory
    )
    assert agent.backstory == backstory
