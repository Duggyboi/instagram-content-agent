# Agentic Infrastructure Framework

A comprehensive Python framework for building, orchestrating, and managing intelligent autonomous agents using CrewAI and LangChain.

## Overview

This framework provides a production-ready foundation for developing agentic applications with out-of-the-box support for:
- **Agent Creation & Management** - Define agents with roles, goals, and capabilities
- **Skill Management** - Organize reusable skills and tools
- **Orchestration** - Coordinate agent workflows and interactions
- **Configuration** - Centralized config management for different environments
- **Monitoring & Logging** - Track agent activities and performance

### 🚀 First Time Using This Framework?

**[→ Start with FIRST_TIME_USER_GUIDE.md](FIRST_TIME_USER_GUIDE.md)** - A comprehensive 30-45 minute guide covering:
- How agents, skills, and tasks work together
- Step-by-step setup from zero to running
- Your first working example with `my_first_task.py`
- Creating custom agents and skills
- Common workflows and best practices

### 📋 Ready to Define a New Project?

**[→ Use PM Initialization System](PM_INIT_QUICKSTART.md)** - Interactive 3-phase system:
1. **Phase 1**: Define your project scope (5-10 min)
2. **Phase 2**: Break it into objectives & milestones (5-10 min)
3. **Phase 3**: Design technical solution (10-20 min)

Quick start: Run `python pm_init.py` and follow the prompts.

See [PM_INITIALIZATION_GUIDE.md](PM_INITIALIZATION_GUIDE.md) for full details.

## Technology Stack

- **CrewAI** - Core agent framework
- **LangChain** - Agent orchestration and skill management
- **Python 3.10+** - Primary language

## Project Structure

```
agentic-infrastructure-framework/
├── agents/               # Agent implementations
│   ├── pm_agent.py       # Project Manager Agent
│   └── dev_agent.py      # Development Agent
├── skills/               # Reusable agent skills
│   ├── logging_skill.py  # Activity logging
│   ├── repo_management_skill.py  # Git operations
│   └── code_quality_skill.py     # Formatting & linting
├── templates/            # Agent & Skill creation templates
├── logs/                 # Agent activity logs
├── src/                  # Core framework source
├── tests/                # Test suite
├── docs/                 # User documentation
├── FIRST_TIME_USER_GUIDE.md    # Start here! 👈
├── my_first_task.py      # Working example script
├── skills.json           # Skill registry
├── tasks.yaml            # Workflow definitions
├── requirements.txt      # Python dependencies
├── setup.py             # Package setup
├── AGENT_GUIDE.md       # Agent operations guide
├── CONTEXT.md           # Project context & decisions
└── .env.example         # Environment variables template
```

## Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agentic-infrastructure-framework.git
cd agentic-infrastructure-framework
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and settings
```

### Basic Usage

Try the working example first:

```bash
# Run the included example
python my_first_task.py
```

This demonstrates PM and Dev agents working together on coordinated tasks.

For development, see examples in `agents/` and `skills/` directories:

```python
from crewai import Crew, Task
from agents.pm_agent import create_pm_agent
from agents.dev_agent import create_dev_agent

# Create agents
pm = create_pm_agent()
dev = create_dev_agent()

# Create tasks
task = Task(
    description="Your task description",
    agent=dev,
    expected_output="Expected result"
)

# Create crew and execute
crew = Crew(agents=[pm, dev], tasks=[task])
result = crew.kickoff()
```

## Configuration

Configuration is managed through:
- `src/config/settings.py` - Main settings
- `.env` file - Environment-specific secrets
- YAML files - Agent and skill definitions

## Development

### Running Tests

```bash
pytest tests/
```

### Creating a New Agent

1. Review the template: `templates/AGENT_TEMPLATE.md`
2. Create your agent in `agents/your_agent.py`
3. Add skills the agent can use
4. Test with a simple Task
5. See `agents/pm_agent.py` and `agents/dev_agent.py` for examples

### Creating a New Skill

1. Review the template: `templates/SKILL_TEMPLATE.md`
2. Create your skill in `skills/your_skill.py`
3. Register it in `skills.json`
4. Test the skill individually first
5. See existing skills in `skills/` for examples

For detailed walkthroughs, see [FIRST_TIME_USER_GUIDE.md](FIRST_TIME_USER_GUIDE.md)

## Documentation

**New to the framework?** Start here:
- [→ FIRST_TIME_USER_GUIDE.md](FIRST_TIME_USER_GUIDE.md) - Complete walkthrough (30-45 minutes)
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - One-page reference card

**For different needs, see:**
- [AGENT_GUIDE.md](AGENT_GUIDE.md) - How agents operate and communicate
- [CONTEXT.md](CONTEXT.md) - Project context, architecture decisions, roadmap
- [templates/AGENT_TEMPLATE.md](templates/AGENT_TEMPLATE.md) - Building custom agents
- [templates/SKILL_TEMPLATE.md](templates/SKILL_TEMPLATE.md) - Building custom skills
- [docs/architecture.md](docs/architecture.md) - System architecture overview
- [docs/agent-development.md](docs/agent-development.md) - Advanced agent patterns
- [docs/getting-started.md](docs/getting-started.md) - Additional setup help

**For tracking and improvement:**
- [PM_FEEDBACK.md](PM_FEEDBACK.md) - Support requests and approval tracking
- [TOOL_INVESTIGATION.md](TOOL_INVESTIGATION.md) - Tool evaluation log
- [SKILL_GAPS.md](SKILL_GAPS.md) - Missing capabilities tracker

## Environment Variables

```
# LLM Configuration
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4

# Logging
LOG_LEVEL=INFO

# Agent Settings
MAX_ITERATIONS=10
TIMEOUT=300
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please open a GitHub issue or contact the maintainers.
