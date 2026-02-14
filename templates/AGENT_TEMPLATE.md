# Agentic Infrastructure Framework - Agent Template

This file shows you how to create a new agent using CrewAI and LangChain.

## Quick Start Agent Template

```python
from crewai import Agent, Task, Crew
from langchain.llms import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Define your agent
my_agent = Agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    backstory="You are an expert data analyst with years of experience",
    verbose=True,
    allow_delegation=False,
)

# Define a task for the agent
analyze_task = Task(
    description="Analyze the sales data for Q1 2026",
    agent=my_agent,
    expected_output="A detailed analysis report with key metrics and insights"
)

# Create a crew and execute
crew = Crew(
    agents=[my_agent],
    tasks=[analyze_task],
    verbose=True,
)

result = crew.kickoff()
print(result)
```

## Understanding the Components

### Agent
An autonomous entity that can execute tasks. Define:
- `role`: What the agent does
- `goal`: What it's trying to achieve
- `backstory`: Context about the agent's expertise
- `tools`: Optional - specific tools the agent can use
- `allow_delegation`: Whether agent can delegate to other agents

### Task
A specific work item for the agent. Include:
- `description`: What needs to be done
- `agent`: Which agent executes this
- `expected_output`: What the result should look like
- `tools`: Optional - specific tools for this task

### Crew
A collection of agents working together. Configure:
- `agents`: List of agents in the crew
- `tasks`: List of tasks to execute
- `manager_agent`: Optional - for hierarchical coordination
- `verbose`: Enable detailed logging

## Agent Naming Convention

When creating agents, use this naming pattern:

```
agents/[agent_name]_agent.py

Examples:
- agents/pm_agent.py
- agents/dev_agent.py
- agents/research_agent.py
```

## Agent Code Structure

```python
# 1. Imports
from crewai import Agent, Task, Crew
from langchain.llms import OpenAI
from dotenv import load_dotenv
import logging

# 2. Setup
load_dotenv()
logger = logging.getLogger(__name__)

# 3. Define agent tools (optional)
def custom_tool(input_data):
    """A custom tool the agent can use"""
    pass

# 4. Create the agent
my_agent = Agent(
    role="Agent Role",
    goal="Agent Goal",
    backstory="Agent backstory and context",
    verbose=True,
    allow_delegation=False,  # or True for multi-agent
    tools=[custom_tool],  # optional
)

# 5. Define tasks
task1 = Task(
    description="First task for the agent",
    agent=my_agent,
    expected_output="What this task should produce",
)

task2 = Task(
    description="Second task for the agent",
    agent=my_agent,
    expected_output="What this task should produce",
)

# 6. Create crew and execute
if __name__ == "__main__":
    crew = Crew(
        agents=[my_agent],
        tasks=[task1, task2],
        verbose=True,
    )
    
    result = crew.kickoff()
    logger.info(f"Agent execution complete: {result}")
```

## Key Best Practices

### 1. Logging
Always log agent activities:
```python
logger.info(f"Agent {agent.role} starting task: {task.description}")
```

### 2. Error Handling
Handle potential errors gracefully:
```python
try:
    result = crew.kickoff()
except Exception as e:
    logger.error(f"Error executing crew: {e}")
    # Handle recovery
```

### 3. Skill Integration
Use skills from the `skills/` directory:
```python
from skills.code_generation import CodeGeneratorSkill
from skills.logging_skill import LoggingSkill

my_agent = Agent(
    # ... other config ...
    tools=[CodeGeneratorSkill(), LoggingSkill()],
)
```

### 4. Documentation
Document your agent:
```python
"""
PM Agent - Project Manager Agent

Responsibilities:
- Task decomposition and delegation
- Progress tracking
- Escalation and decision-making

Skills Used:
- repo_management
- code_quality_assessment
- communication

Example Usage:
    python -m agents.pm_agent
"""
```

### 5. Configuration
Use environment variables:
```python
import os

AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "300"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
VERBOSE = os.getenv("AGENT_VERBOSE", "true").lower() == "true"
```

## Testing Your Agent

```python
# test_my_agent.py
import pytest
from agents.my_agent import my_agent

def test_agent_creation():
    assert my_agent.role == "Expected Role"
    assert my_agent.goal == "Expected Goal"

def test_agent_task_execution():
    # Create a simple test task
    from crewai import Task
    
    test_task = Task(
        description="Test description",
        agent=my_agent,
        expected_output="Test output"
    )
    
    # Execute and verify
    # Specific test logic depends on task
```

## Multi-Agent Example

```python
# Create multiple agents
pm_agent = Agent(
    role="Project Manager",
    goal="Coordinate the development team",
    backstory="Experienced project manager",
)

dev_agent = Agent(
    role="Developer",
    goal="Implement features",
    backstory="Senior software engineer",
    allow_delegation=False,
)

# Create tasks for each
planning_task = Task(
    description="Create project plan",
    agent=pm_agent,
)

implementation_task = Task(
    description="Implement features from plan",
    agent=dev_agent,
)

# Create crew with manager
crew = Crew(
    agents=[pm_agent, dev_agent],
    tasks=[planning_task, implementation_task],
    manager_agent=pm_agent,  # PM manages the flow
    verbose=True,
)

result = crew.kickoff()
```

## Using Skills

Skills are modular, reusable capabilities. Create them in `skills/` directory:

```python
# skills/my_skill.py
from langchain.tools import tool

@tool
def my_skill(input_data: str) -> str:
    """Useful for doing something specific"""
    # Implementation
    return result

# Use in agent
from skills.my_skill import my_skill

my_agent = Agent(
    # ...
    tools=[my_skill],
)
```

## Next Steps

1. Check existing agents in `agents/` directory
2. Review skill definitions in `skills/` directory
3. Read `AGENT_GUIDE.md` for operational guidelines
4. Examine example agents in documentation
5. Start building your own agents!

## Resources

- [Agent Development Guide](../docs/agent-development.md)
- [Agent Operations Guide](../AGENT_GUIDE.md)
- [Skills Registry](../skills.json)
- [CrewAI Documentation](https://github.com/joaomdmoura/crewai)
- [LangChain Documentation](https://python.langchain.com/)
