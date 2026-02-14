# First-Time User Guide: End-to-End Walkthrough

This guide explains **how the agentic-infrastructure-framework works** and walks you through using it from start to finish.

**Target Audience**: Developers new to this framework  
**Time to Complete**: 30-45 minutes  
**Prerequisites**: Python 3.10+, basic command line knowledge

---

## Part 1: How the Framework Works (Concepts)

### The Big Picture

The agentic-infrastructure-framework is built around three core concepts:

```
┌─────────────────────────────────────────────────────────┐
│                     YOUR PROJECT                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐         ┌──────────────────────┐    │
│  │   AGENTS     │         │      SKILLS          │    │
│  │              │         │                      │    │
│  │ • PM Agent   │────────>│ • Logging            │    │
│  │ • Dev Agent  │         │ • Repo Management    │    │
│  │ • Custom     │         │ • Code Quality       │    │
│  │   Agents     │         │ • Custom Skills      │    │
│  └──────────────┘         └──────────────────────┘    │
│         │                                               │
│         └────────────────────┬───────────────────────   │
│                              │                          │
│                      ┌───────▼────────┐               │
│                      │     TASKS      │               │
│                      │                │               │
│                      │ Executable     │               │
│                      │ Work Units     │               │
│                      └────────────────┘               │
│                                                        │
│                    Powered by CrewAI                  │
│                    Orchestrated by LangChain          │
│                    Logged & Tracked                   │
│                                                        │
└─────────────────────────────────────────────────────────┘
```

### 1. **AGENTS** - Autonomous Workers
An Agent is an autonomous entity that performs work. Think of it as a specialized team member:

**Example Agents:**
- **PM Agent**: Coordinates work, makes decisions, delegates tasks
- **Dev Agent**: Writes code, runs tests, handles technical work
- **Your Custom Agent**: Anything you define!

**Key Properties:**
- `role`: What the agent does ("Senior Developer")
- `goal`: What they're trying to achieve
- `backstory`: Context about their expertise
- `tools` (skills): What they can do
- `allow_delegation`: Can they ask other agents for help?

### 2. **SKILLS** - Reusable Tools
A Skill is a specific capability that agents can use. Think of it as a tool in a toolbox:

**Example Skills:**
- `log_action`: Record what an agent did
- `git_commit`: Make a git commit
- `run_flake8_lint`: Check code style

**Key Points:**
- One skill does ONE thing well
- Can be reused by multiple agents
- Registered in `skills.json`
- Implemented in `skills/` directory

### 3. **TASKS** - Work to Be Done
A Task is a specific piece of work that an agent performs. It's the instruction given to an agent:

**Example Task:**
```python
task = Task(
    description="Analyze the sales data and create a report",
    agent=my_agent,
    expected_output="A detailed analysis report"
)
```

### 4. **CREW** - Coordinated Execution
A Crew is a group of agents working together on a set of tasks:

```python
crew = Crew(
    agents=[pm_agent, dev_agent],        # Who's involved
    tasks=[planning_task, dev_task],     # What to do
    manager_agent=pm_agent,              # Who coordinates
    verbose=True,                        # Show details
)

result = crew.kickoff()  # Execute!
```

---

## Part 2: Framework Architecture

### Directory Structure (What Goes Where)

```
agentic-infrastructure-framework/
│
├── agents/                    # Agent implementations
│   ├── pm_agent.py           # ← PM Agent definition
│   ├── dev_agent.py          # ← Dev Agent definition
│   └── your_custom_agent.py  # ← Add your agents here
│
├── skills/                    # Skill implementations
│   ├── logging_skill.py       # ← Logging (audit trail)
│   ├── repo_management_skill.py  # ← Git operations
│   ├── code_quality_skill.py  # ← Formatting & linting
│   └── your_custom_skill.py   # ← Add your skills here
│
├── templates/                 # Creation templates
│   ├── AGENT_TEMPLATE.md      # ← How to build agents
│   └── SKILL_TEMPLATE.md      # ← How to build skills
│
├── logs/                      # Activity tracking
│   └── agent_log.txt          # ← Audit trail of all actions
│
├── skills.json                # ← Registry of all skills
├── tasks.yaml                 # ← Workflow definitions
├── requirements.txt           # ← Python dependencies
└── .env.example               # ← Configuration template
```

### Data Flow (How It Works)

```
1. Define Agents
   ↓
2. Define Skills (agents use these)
   ↓
3. Create Tasks (tell agents what to do)
   ↓
4. Create a Crew (coordinate agents)
   ↓
5. Run crew.kickoff()
   ↓
6. Agent executes task using skills
   ↓
7. Results logged to logs/agent_log.txt
   ↓
8. Get results back
```

---

## Part 3: Step-by-Step Setup

### Step 1: Clone & Set Up Environment

```bash
# Navigate to project
cd C:\Users\Keagan\projects\agentic-infrastructure-framework

# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# Or (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

```bash
# Copy template to actual file
cp .env.example .env

# Edit .env with your settings
# (Add your OpenAI API key, etc.)
```

**What to add to .env:**
```
OPENAI_API_KEY=sk-your-actual-key-here
LOG_LEVEL=INFO
DEBUG_MODE=false
AGENT_TIMEOUT=300
```

### Step 3: Verify Installation

```bash
# Test imports work
python -c "import crewai; print('CrewAI installed!')"

# Test the PM Agent runs
python -m agents.pm_agent
```

---

## Part 4: Your First Agent Task (Hands-On)

Let's create your first script that uses the framework.

### Create: `my_first_task.py`

```python
"""
My First Agent Task

This script demonstrates how to use the agentic framework
to execute a simple coordinated task.
"""

from crewai import Crew, Task
from agents.pm_agent import create_pm_agent
from agents.dev_agent import create_dev_agent
from skills.logging_skill import log_action
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Step 1: Create agents
print("Creating agents...")
pm_agent = create_pm_agent(allow_delegation=True)
dev_agent = create_dev_agent(allow_delegation=False)

# Step 2: Create tasks
print("Creating tasks...")

planning_task = Task(
    description=(
        "Review the current project structure in the agentic-infrastructure-framework. "
        "Identify what we have, what's working well, and what gaps exist. "
        "Create a simple analysis."
    ),
    agent=pm_agent,
    expected_output="A project status analysis with findings and recommendations"
)

implementation_task = Task(
    description=(
        "Based on the PM's analysis, create a simple Python module that uses the skills "
        "we have available. It should demonstrate logging a custom action."
    ),
    agent=dev_agent,
    expected_output="Working Python code that is tested and error-free"
)

# Step 3: Create crew (coordinate agents)
print("Setting up crew...")
crew = Crew(
    agents=[pm_agent, dev_agent],
    tasks=[planning_task, implementation_task],
    manager_agent=pm_agent,  # PM coordinates
    verbose=True,            # Show all details
)

# Step 4: Execute!
print("\n" + "="*60)
print("EXECUTING CREW - Watch the agents work!")
print("="*60 + "\n")

try:
    result = crew.kickoff()
    
    print("\n" + "="*60)
    print("EXECUTION COMPLETE!")
    print("="*60)
    print(f"\nResult:\n{result}")
    
except Exception as e:
    logger.error(f"Error during execution: {e}", exc_info=True)
    print(f"\n❌ Error: {e}")
```

### Run It:

```bash
python my_first_task.py
```

**What You'll See:**
1. Agents analyzing the project
2. Detailed logs of what they're thinking
3. Results returned
4. Everything logged to `logs/agent_log.txt`

---

## Part 5: Creating Your First Custom Skill

Skills are how agents **do things**. Let's create a simple one.

### Create: `skills/web_search_skill.py`

```python
"""
Web Search Skill

A simple skill that demonstrates how to create custom skills.
(This is a mock implementation for demo purposes)
"""

from langchain.tools import tool
import logging

logger = logging.getLogger(__name__)

@tool
def web_search(query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: What to search for
        
    Returns:
        Search results as a string
    """
    try:
        logger.info(f"Searching for: {query}")
        
        # In a real implementation, you'd call a search API
        # For now, just return a mock result
        result = f"Search results for '{query}' (mock data)"
        
        logger.info(f"Search complete: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise

# Metadata about this skill
def get_skill_info():
    return {
        "name": "Web Search Skill",
        "description": "Search the web for information",
    }
```

### Register It: Update `skills.json`

Add to the skills array:
```json
{
  "id": "web_search",
  "name": "Web Search",
  "description": "Search the web for information",
  "category": "research",
  "status": "active",
  "capabilities": ["query_web"],
  "dependencies": [],
  "examples": [
    "Search for information about CrewAI",
    "Find documentation on LangChain"
  ]
}
```

### Use It in an Agent:

```python
from skills.web_search_skill import web_search
from agents.pm_agent import create_pm_agent

agent = create_pm_agent(tools=[web_search])
# Now this agent can use web_search!
```

---

## Part 6: Creating Your First Custom Agent

Let's create a specialized Research Agent.

### Create: `agents/research_agent.py`

```python
"""
Research Agent

Specialized in gathering and analyzing information.
"""

from crewai import Agent
from skills.web_search_skill import web_search
from skills.logging_skill import log_action
import logging

logger = logging.getLogger(__name__)

def create_research_agent(name: str = "Research Agent") -> Agent:
    """Create a Research Agent for information gathering"""
    
    agent = Agent(
        role="Research Analyst",
        goal="Gather accurate information and provide insightful analysis",
        backstory=(
            "You are an expert research analyst with years of experience "
            "finding and analyzing information. You're thorough, detail-oriented, "
            "and excellent at identifying patterns and insights."
        ),
        verbose=True,
        allow_delegation=False,
        tools=[web_search, log_action],  # Skills this agent can use
    )
    
    logger.info(f"Created Research Agent: {name}")
    return agent
```

### Use Your New Agent:

```python
from agents.research_agent import create_research_agent
from crewai import Task, Crew

# Create it
research_agent = create_research_agent()

# Create a task
research_task = Task(
    description="Research CrewAI framework capabilities and limitations",
    agent=research_agent,
    expected_output="Detailed research report with findings"
)

# Create crew
crew = Crew(
    agents=[research_agent],
    tasks=[research_task],
    verbose=True,
)

# Run it
result = crew.kickoff()
print(result)
```

---

## Part 7: Complete Workflow Example

Here's a realistic end-to-end scenario:

### Scenario: "Improve Code Quality"

```python
"""
Complete workflow: Improve code quality using multiple agents
"""

from crewai import Crew, Task
from agents.pm_agent import create_pm_agent
from agents.dev_agent import create_dev_agent
from skills.code_quality_skill import run_all_checks, run_black_format
from skills.logging_skill import log_action
from skills.repo_management_skill import git_commit, git_push

# 1. CREATE AGENTS
print("Step 1: Creating agents...")
pm = create_pm_agent()
dev = create_dev_agent()

# 2. CREATE TASKS
print("Step 2: Creating tasks...")

# Task 1: PM analyzes what needs to be done
analysis = Task(
    description=(
        "Analyze the code quality issues in the agents/ and skills/ directories. "
        "Identify the most critical issues to fix first."
    ),
    agent=pm,
    expected_output="Prioritized list of code quality improvements"
)

# Task 2: Dev fixes the issues
implementation = Task(
    description=(
        "Using the PM's analysis, run code formatting and linting. "
        "Fix the issues found. Then commit and push to git."
    ),
    agent=dev,
    expected_output="Fixed code, committed to git with summary of changes"
)

# 3. CREATE CREW
print("Step 3: Setting up crew...")
crew = Crew(
    agents=[pm, dev],
    tasks=[analysis, implementation],
    manager_agent=pm,
    verbose=True,
)

# 4. EXECUTE
print("\nStep 4: Executing workflow...\n")
result = crew.kickoff()

print(f"\n✓ Workflow complete!\n{result}")

# 5. CHECK RESULTS
print("Step 5: Verifying everything...")
from skills.logging_skill import read_log
recent_logs = read_log(20)
print(f"Recent activity:\n{recent_logs}")
```

---

## Part 8: Common Workflows

### Workflow 1: "Create a New Feature"

```
PM Agent (Planning)
    ↓
    ├─ Analyze requirements
    ├─ Break into tasks
    └─ Create implementation plan
    
        ↓ Delegate to
        
Dev Agent (Implementation)
    ↓
    ├─ Create feature branch
    ├─ Write code
    ├─ Run tests
    ├─ Format & lint
    └─ Commit & push
```

### Workflow 2: "Fix a Bug"

```
Research Agent (Investigation)
    ↓
    ├─ Search for bug reports
    ├─ Analyze logs
    └─ Reproduce issue
    
        ↓ Delegate to
        
Dev Agent (Implementation)
    ↓
    ├─ Write fix
    ├─ Test fix
    ├─ Verify no regressions
    └─ Commit & release
```

### Workflow 3: "Code Review"

```
Dev Agent (Code Review)
    ↓
    ├─ Run linting
    ├─ Run tests
    ├─ Check formatting
    └─ Analyze coverage
    
        ↓ Report to
        
PM Agent (Decision)
    ↓
    ├─ Approve or require changes
    └─ Merge to main
```

---

## Part 9: Troubleshooting

### Problem: "Python: command not found"
```bash
# Make sure Python is installed
python --version

# Use full path if needed
C:\Python311\python --version
```

### Problem: "ModuleNotFoundError: No module named 'crewai'"
```bash
# Reinstall requirements
pip install -r requirements.txt
```

### Problem: "OpenAI API error"
```bash
# Check .env has correct API key
cat .env | grep OPENAI_API_KEY

# If empty, add your key
OPENAI_API_KEY=sk-your-key-here
```

### Problem: "Agent seems stuck/slow"
```bash
# Check logs for details
tail logs/agent_log.txt

# Reduce verbosity in .env
LOG_LEVEL=WARNING

# Set shorter timeout
AGENT_TIMEOUT=60  # seconds
```

### Problem: "Git error when agent tries to commit"
```bash
# Make sure git is configured
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Check git is in PATH
git --version
```

---

## Part 10: Next Steps After This Guide

### ✅ What You Now Know
- How agents, skills, tasks work together
- How to set up the framework
- How to run existing agents
- How to create custom skills
- How to create custom agents
- Common workflow patterns

### 🎯 What to Do Next

1. **Run the examples** (most important!)
   - Try `my_first_task.py` from Part 4
   - Run existing agents
   - Experiment with tasks

2. **Create your first custom skill**
   - Follow the template in `templates/SKILL_TEMPLATE.md`
   - Register it in `skills.json`
   - Use it in an agent

3. **Create your first custom agent**
   - Follow the template in `templates/AGENT_TEMPLATE.md`
   - Give it specific skills
   - Test with a simple task

4. **Build a real workflow**
   - Combine multiple agents
   - Create meaningful tasks
   - Log and track results

5. **Keep improving**
   - Log gaps in `SKILL_GAPS.md`
   - Evaluate new tools in `TOOL_INVESTIGATION.md`
   - Update `CONTEXT.md` with learnings

---

## Part 11: Key Files Reference

| File | Purpose | When to Use |
|------|---------|------------|
| `agents/pm_agent.py` | PM Agent definition | Use as manager/coordinator |
| `agents/dev_agent.py` | Dev Agent definition | Use for code tasks |
| `agents/your_agent.py` | Your custom agent | Create new agents here |
| `skills/logging_skill.py` | Activity logging | All agents should log |
| `skills/repo_management_skill.py` | Git operations | Agents that modify code |
| `skills/code_quality_skill.py` | Formatting & linting | Before committing code |
| `templates/AGENT_TEMPLATE.md` | Agent guide | Creating new agents |
| `templates/SKILL_TEMPLATE.md` | Skill guide | Creating new skills |
| `skills.json` | Skill registry | Register each skill |
| `tasks.yaml` | Workflow definitions | Define workflows |
| `logs/agent_log.txt` | Activity audit trail | Check what happened |
| `AGENT_GUIDE.md` | Operations guide | Agent protocols |
| `CONTEXT.md` | Project context | Decisions & state |

---

## Part 12: Tips & Best Practices

### ✅ DO:
- ✅ Log all significant actions (`log_action` skill)
- ✅ Test skills individually before using in agents
- ✅ Give agents clear, specific goals and backstories
- ✅ Break complex tasks into subtasks
- ✅ Use `verbose=True` while developing, `False` in production
- ✅ Commit changes after each successful workflow
- ✅ Check logs to understand what agents are doing
- ✅ Reuse skills across multiple agents

### ❌ DON'T:
- ❌ Create skills that do multiple unrelated things
- ❌ Give agents conflicting goals
- ❌ Skip error handling in skills
- ❌ Forget to register skills in `skills.json`
- ❌ Leave `.env` file committed to git
- ❌ Ignore agent logs when debugging
- ❌ Create agents with all possible skills
- ❌ Skip testing before committing

---

## Quick Start Command Reference

```bash
# Setup
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API keys

# Run examples
python my_first_task.py
python -m agents.pm_agent
python -m agents.dev_agent

# Check logs
cat logs/agent_log.txt
tail -f logs/agent_log.txt  # Follow in real-time

# Git workflow
git status
git add .
git commit -m "Description"
git push origin main

# Testing your skill
python -c "from skills.your_skill import your_skill; print(your_skill('test'))"
```

---

## Summary: The 3-Minute Version

**The Framework is:**
- **Agents**: Autonomous workers with specialized roles
- **Skills**: Reusable tools agents can use
- **Tasks**: Work instructions for agents
- **Crews**: Coordinated groups of agents working together

**How to Use It:**
1. Create agents (from templates or existing ones)
2. Create skills agents will use
3. Define tasks for agents
4. Create a crew to coordinate them
5. Call `crew.kickoff()` to execute
6. Check `logs/agent_log.txt` for results

**To Extend It:**
- Add custom skills in `skills/`
- Add custom agents in `agents/`
- Register skills in `skills.json`
- Use in your crews

That's it! You're ready to build.

---

## Questions?

- **"How do I create a skill?"** → See `templates/SKILL_TEMPLATE.md`
- **"How do I create an agent?"** → See `templates/AGENT_TEMPLATE.md`
- **"Why did my agent fail?"** → Check `logs/agent_log.txt`
- **"Can agents work together?"** → Yes! Use a Crew with `manager_agent`
- **"How do I add a new skill to an agent?"** → Add to `tools` parameter
- **"How do I scale this?"** → See `SKILL_GAPS.md` for distributed execution options

---

**Happy building! 🚀**

Last Updated: 2026-02-10
