# Getting Started Guide

## Prerequisites

- Python 3.10 or higher
- pip or conda package manager
- OpenAI API key (for LLM functionality)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/agentic-infrastructure-framework.git
cd agentic-infrastructure-framework
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy the example configuration:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4
LOG_LEVEL=INFO
```

### 5. Verify Installation

Run the tests:
```bash
pytest tests/
```

## Quick Start

Run the example agent:
```bash
python example_agent.py
```

## Next Steps

- Read [Architecture Overview](architecture.md)
- Explore [Agent Development Guide](agent-development.md)
- Check out examples in the repository
