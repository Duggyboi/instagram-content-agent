# Agentic Infrastructure Framework - Skill Template

This file shows you how to create new skills for agents to use.

## What is a Skill?

A skill is a reusable, modular capability that one or more agents can utilize. Skills:
- Encapsulate specific functionality
- Can be shared across multiple agents
- Are defined in the `skills/` directory
- Are registered in `skills.json`
- Follow a consistent interface

## Quick Start Skill Template

```python
# skills/my_skill.py
"""
My Custom Skill

A skill for doing something specific.
"""

from langchain.tools import tool
from typing import Any
import logging

logger = logging.getLogger(__name__)

@tool
def my_skill(input_data: str) -> str:
    """
    Useful for [describe what this skill does].
    
    Args:
        input_data: Description of input
        
    Returns:
        Description of output
    """
    try:
        logger.info(f"Executing my_skill with input: {input_data}")
        
        # Your skill implementation here
        result = process_input(input_data)
        
        logger.info(f"my_skill completed successfully: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in my_skill: {e}")
        raise

def process_input(data: str) -> str:
    """Helper function for skill logic"""
    # Implementation
    return f"Processed: {data}"
```

## Skill Structure

Create skills as Python files in the `skills/` directory:

```
skills/
├── __init__.py
├── code_generation_skill.py
├── logging_skill.py
├── repo_management_skill.py
└── [your_skill_name].py
```

## Naming Convention

- **File name**: `lowercase_with_underscores_skill.py`
- **Function name**: `snake_case` (use `@tool` decorator)
- **Skill ID**: `lowercase_with_underscores` (in skills.json)

Examples:
- `code_generation_skill.py` → `code_generation` skill
- `repo_management_skill.py` → `repo_management` skill
- `web_scraping_skill.py` → `web_scraping` skill

## Full Skill Template with Best Practices

```python
"""
[Skill Name] Skill

[Detailed description of what this skill does]

Usage:
    from skills.your_skill import your_skill
    
    result = your_skill("your input")
"""

from langchain.tools import tool
from typing import Any, Optional, List, Dict
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# Configuration
SKILL_NAME = "your_skill_name"
SKILL_VERSION = "1.0.0"
TIMEOUT = int(os.getenv("SKILL_TIMEOUT", "30"))

@tool
def your_skill(input_data: str, optional_param: Optional[str] = None) -> str:
    """
    Brief description of what the skill does.
    
    This is a more detailed description explaining the skill's purpose,
    behavior, and limitations.
    
    Args:
        input_data (str): The primary input to the skill
        optional_param (str, optional): Optional configuration parameter
        
    Returns:
        str: Description of the return value
        
    Raises:
        ValueError: If input validation fails
        TimeoutError: If execution exceeds timeout
        
    Examples:
        >>> result = your_skill("example input")
        >>> print(result)
        "example output"
    """
    
    # Validation
    if not input_data:
        raise ValueError("input_data cannot be empty")
    
    try:
        # Logging entry point
        logger.debug(f"[{SKILL_NAME}] Starting execution")
        logger.debug(f"[{SKILL_NAME}] Input: {input_data}")
        
        # Extract skill parameters
        config = {
            "timeout": TIMEOUT,
            "param": optional_param or "default_value",
        }
        
        # Execute core logic
        result = _execute_skill_logic(input_data, config)
        
        # Validate result
        if not result:
            logger.warning(f"[{SKILL_NAME}] Returned empty result")
        
        # Log success
        logger.info(f"[{SKILL_NAME}] Execution successful")
        logger.debug(f"[{SKILL_NAME}] Output: {result}")
        
        return result
        
    except TimeoutError as e:
        logger.error(f"[{SKILL_NAME}] Timeout: {e}")
        raise
    except Exception as e:
        logger.error(f"[{SKILL_NAME}] Error: {e}", exc_info=True)
        raise

def _execute_skill_logic(input_data: str, config: Dict) -> str:
    """
    Core implementation of the skill.
    
    Args:
        input_data: The input to process
        config: Configuration dictionary
        
    Returns:
        Processed result
    """
    # Your implementation here
    processed = input_data.upper()  # Example
    
    return processed

def validate_input(input_data: Any) -> bool:
    """Validate input data format and content"""
    if not isinstance(input_data, str):
        return False
    if len(input_data) == 0:
        return False
    return True

def get_skill_info() -> Dict[str, Any]:
    """Return metadata about this skill"""
    return {
        "name": SKILL_NAME,
        "version": SKILL_VERSION,
        "description": "Skill description",
        "capabilities": ["capability1", "capability2"],
        "dependencies": [],  # External dependencies
        "required_env_vars": [],  # Environment variables needed
    }

# Self-test capability
if __name__ == "__main__":
    test_input = "test input"
    try:
        result = your_skill(test_input)
        print(f"✓ Skill test passed: {result}")
        print(f"✓ Skill metadata: {get_skill_info()}")
    except Exception as e:
        print(f"✗ Skill test failed: {e}")
```

## Registering Your Skill

After creating a skill, register it in `skills.json`:

```json
{
  "skills": [
    {
      "id": "your_skill",
      "name": "Your Skill Name",
      "description": "What this skill does",
      "category": "category_name",
      "status": "active",
      "capabilities": ["capability1", "capability2"],
      "dependencies": ["python_package_name"],
      "examples": [
        "Example usage 1",
        "Example usage 2"
      ]
    }
  ]
}
```

## Skill Categories

- **developer_tools**: Version control, file operations
- **development**: Code generation, refactoring
- **code_quality**: Linting, formatting, testing
- **monitoring**: Logging, observability
- **maintenance**: Rollback, recovery, updates
- **communication**: Messaging, escalation
- **research**: Investigation, evaluation
- **improvement**: Optimization, metrics

## Using Skills in Agents

```python
from crewai import Agent, Task, Crew
from skills.your_skill import your_skill

# Create agent with skill
my_agent = Agent(
    role="Your Agent Role",
    goal="Your goal",
    backstory="Your backstory",
    tools=[your_skill],  # Add the skill
    verbose=True,
)

# Use in task
task = Task(
    description="Use your_skill to process data",
    agent=my_agent,
    expected_output="Processed result",
)

# Execute
crew = Crew(agents=[my_agent], tasks=[task])
result = crew.kickoff()
```

## Testing Your Skill

```python
# test_your_skill.py
import pytest
from skills.your_skill import your_skill, validate_input

def test_skill_execution():
    """Test basic skill execution"""
    result = your_skill("test input")
    assert result is not None
    assert isinstance(result, str)

def test_input_validation():
    """Test input validation"""
    assert validate_input("valid") == True
    assert validate_input("") == False
    assert validate_input(None) == False

def test_skill_error_handling():
    """Test error handling"""
    with pytest.raises(ValueError):
        your_skill("")

def test_skill_with_optional_params():
    """Test with optional parameters"""
    result = your_skill("input", optional_param="value")
    assert result is not None
```

Run tests:
```bash
pytest skills/test_your_skill.py -v
```

## Skill Integration Checklist

Before using a new skill in production:

- [ ] Skill file created with proper naming
- [ ] Docstrings complete for all functions
- [ ] Error handling implemented
- [ ] Logging added for debugging
- [ ] Unit tests written and passing
- [ ] Registered in `skills.json`
- [ ] Usage example provided
- [ ] Reviewed by team (if applicable)
- [ ] Environment variables documented
- [ ] Added to AGENT_GUIDE.md if needed

## Common Skill Patterns

### Pattern 1: File Processing Skill
```python
@tool
def process_file(filepath: str) -> str:
    """Process a file and return result"""
    with open(filepath, 'r') as f:
        content = f.read()
    # Process content
    return result
```

### Pattern 2: API Call Skill
```python
@tool
def call_api(endpoint: str, data: dict) -> str:
    """Call an API and return response"""
    import requests
    response = requests.post(endpoint, json=data)
    return response.json()
```

### Pattern 3: Data Transformation Skill
```python
@tool
def transform_data(input_data: str, format: str = "json") -> str:
    """Transform data to specified format"""
    # Parse input
    # Transform
    # Return in format
    return result
```

### Pattern 4: Validation Skill
```python
@tool
def validate(data: str, rules: dict) -> str:
    """Validate data against rules"""
    # Check against rules
    # Return validation result
    return "valid" or "invalid: reason"
```

## Advanced: Async Skills

For long-running operations:

```python
from langchain.tools import tool
import asyncio

@tool
async def async_skill(input_data: str) -> str:
    """Async skill for long-running operations"""
    result = await some_async_operation(input_data)
    return result

async def some_async_operation(data: str) -> str:
    # Async implementation
    await asyncio.sleep(1)
    return f"Processed: {data}"
```

## Troubleshooting Skills

**Skill not found by agent**:
- Check `skills.json` registration
- Verify import statement
- Check file location in `skills/` directory

**Skill execution failing**:
- Check error logs
- Verify input data format
- Check external dependencies installed

**Skill performance issues**:
- Add timing logs
- Consider async implementation
- Profile with cProfile

## Documentation Links

- [Agent Template](AGENT_TEMPLATE.md)
- [Agent Development Guide](../docs/agent-development.md)
- [Skills Registry](../skills.json)
- [Agent Guide](../AGENT_GUIDE.md)

## Next Steps

1. Review existing skills in `skills/` directory
2. Plan your skill capabilities
3. Implement following this template
4. Test thoroughly
5. Register in `skills.json`
6. Use in your agents!
