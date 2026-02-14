# PM Agent Initialization System

A comprehensive project scoping workflow that guides you from idea to ready-for-development in three phases.

## Overview

The PM initialization system provides an interactive, guided process for defining your project scope before development begins. It's designed for project owners, product managers, and team leads who need to clearly define what they're building.

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  Health Check → Greeting → Phase 1 → Phase 2 → Phase 3 → Ready   │
│  (Validate)   (Welcome)   (Scoping) (Decompose) (Architecture)     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## The Four Stages

### Stage 0: Health Check
**What:** Validates that your environment has all required dependencies
**Output:** 
- ✅ All good → Proceed to Stage 1
- ❌ Issues found → `.framework/framework_checklist.md` with remediation steps

### Stage 1: Project Scoping (Business Architect Mode)
**What:** Interactive discovery session to define your project vision
**Who:** Business Architect Agent
**Input Options:**
- **Option A:** You have just an idea (agent asks discovery questions)
- **Option B:** You have an initial brief (agent refines and deepens it)
**Output:** `.project/project_brief.md` with:
- Problem statement
- Target users/stakeholders
- Desired outcomes
- Success metrics
- Scope & features
- Constraints
- Dependencies
- Risks & mitigation

### Stage 2: Project Decomposition (Decomposer Mode)
**What:** Breaks your project into structured components and timeline
**Who:** Project Decomposer Agent
**Input:** Reads your project brief
**Output:** `.project/project_decomposition.md` with:
- 3-5 core objectives
- Major components/phases
- Milestone timeline with deliverables
- Dependency analysis
- Risk factors

### Stage 3: Technical Solution Proposal (Solution Architect Mode)
**What:** Designs the technical architecture to execute your project
**Who:** Solution Architect Agent
**Input:** Reads your decomposition (and brief for context)
**Output:** `.project/technical_proposal.md` with:
- Tech stack recommendations
- Agent architecture (PM, Dev, QA, etc.)
- Skills required for each agent
- Implementation phases
- Risk mitigation strategies

## Getting Started

### Quick Start: Run the Full Flow

```bash
# Start the PM initialization journey
python pm_init.py

# This will:
# 1. Run health check
# 2. Show greeting
# 3. Start Phase 1 (Business Scoping)
# 4. Ask if you want to continue to Phase 2
```

### Phase Progression

```bash
# Phase 1: Start scoping
python pm_init.py

# Phase 2: Decompose the project  
python pm_decompose.py

# Phase 3: Design technical solution
python pm_architect.py
```

## Understanding Each Phase

### Phase 1: Business Scoping

The Business Architect Agent helps you think through your project systematically.

**If you're starting with an IDEA (Option A):**
```
Agent asks:
  "What's the core problem you're solving?"
  "Who are the main users?"
  "What should be different after this project?"
  "How will you measure success?"
  → Creates a detailed project brief
  → Asks for your approval
  → Saves to .project/project_brief.md
```

**If you're starting with a BRIEF (Option B):**
```
Agent reads your brief and asks:
  "What do you mean by...?"
  "Who are all the users/stakeholders?"
  "What are the constraints?"
  "How will you measure success?"
  → Deepens and refines your brief
  → Organizes into structured document
  → Asks for your approval
  → Saves to .project/project_brief.md
```

### Phase 2: Decomposition

The Decomposer Agent structures your project for execution.

**Breaks your vision into:**
- **Objectives** - The 3-5 things you're trying to achieve
- **Components** - The major parts/phases of the solution
- **Milestones** - Timeline with deliverables and checkpoints

**Then:**
- Identifies dependencies (what must happen first)
- Flags risks
- Proposes realistic timeline
- Asks for your approval before moving to Phase 3

### Phase 3: Technical Solution

The Solution Architect designs how to build it.

**Proposes:**
- **Tech Stack** - Languages, frameworks, tools
- **Agent Architecture** - What agents (PM, Dev, QA, etc.) and their roles
- **Skills** - What capabilities each agent needs
- **Implementation Plan** - How to build in phases

**Result:**
- Comprehensive technical proposal
- Ready for development team to start building

## Output Files

Your `.project/` directory will contain:

1. **project_brief.md**
   - What you're building and why
   - Who it's for and what success looks like
   - Constraints and dependencies

2. **project_decomposition.md**
   - Objectives, components, and timeline
   - Risk analysis
   - Milestone checkpoints

3. **technical_proposal.md**
   - Tech stack and architecture
   - Agent and skill definitions
   - Implementation strategy

**These become your project's blueprint.**

## User Interaction Model

Each phase is interactive with approval gates:

```
Phase 1 (Scoping):
  Agent: "Here's your project brief. Does this capture your vision?"
  You: "Yes, but change X to Y"
  Agent: Adjusts brief
  You: "Perfect!"
  ✓ Approved, move to Phase 2

Phase 2 (Decomposition):
  Agent: "Here's how I'd break this into components..."
  You: "Looks good, but can we combine A and B?"
  Agent: Restructures based on feedback
  You: "That's better!"
  ✓ Approved, move to Phase 3

Phase 3 (Architecture):
  Agent: "Here's the tech stack and architecture..."
  You: Review and approve
  ✓ Approved, project ready for implementation
```

## Common Workflows

### I have a vague idea
```bash
python pm_init.py
# Choose Option A at prompt
# Agent asks discovery questions
# You end up with a clear brief
```

### I have a written brief but want to refine it
```bash
python pm_init.py
# Choose Option B at prompt
# Paste your brief when prompted
# Agent asks clarifying questions
# You end up with a more detailed brief
```

### I want to skip to a specific phase
```bash
# Already have a brief? Start decomposition
python pm_decompose.py

# Already have both? Start architecture
python pm_architect.py
```

### I want to iterate on phase outputs
```bash
# Edit .project/project_brief.md
# Run Phase 2 again
python pm_decompose.py

# Or edit .project/project_decomposition.md
# Run Phase 3 again
python pm_architect.py
```

## Troubleshooting

### Health check fails
```
→ Check .framework/framework_checklist.md
→ Install missing packages: pip install -r requirements.txt
→ Setup .env file: cp .env.example .env (add your API keys)
→ Run pm_init.py again
```

### Agent seems stuck
```
→ Press Ctrl+C to interrupt
→ Check logs/agent_log.txt for context
→ Edit the .project/[file].md manually
→ Run the next phase script to continue
```

### I want to restart a phase
```
→ Delete the .project/project_brief.md (or relevant file)
→ Run python pm_init.py (or relevant script) again
```

### .project/ directory missing
```
→ Create it: mkdir .project
→ Run python pm_init.py to start over
```

## For Development Teams

Once you have all three files created:

1. **Share the brief** with stakeholders for consensus
2. **Share the decomposition** with the dev team to plan sprints
3. **Use the technical proposal** to guide implementation
4. **Create CrewAI tasks** for each component
5. **Monitor progress** using the PM Agent
6. **Iterate** based on team feedback

## Advanced Usage

### Custom Agent Modes
You can modify the agent backstories in `agents/pm_*.py` to customize how they approach your project.

### Skipping Phases
If you already have a brief and decomposition, jump straight to architecture:
```bash
python pm_architect.py
```

### Batch Processing
Run all phases non-interactively:
```bash
python pm_init.py          # Answer prompts
python pm_decompose.py     # Proceed (no interactive prompt)
python pm_architect.py     # Proceed
```

### Extending the Framework
Add more phases or agents to the workflow by creating new scripts in `agents/pm_*.py`.

## Key Concepts

**Phase Gates:** Each phase has an approval point before proceeding. This ensures quality and team consensus.

**Flexibility:** The system adapts to whether you're starting with an idea or a brief.

**Artifacts:** All outputs are markdown files for easy review, editing, and sharing.

**Iterative:** You can go back, edit any file, and re-run the next phase to get new outputs.

## Next Steps After Completing All Phases

Once you have all three documents:

1. **Team Review** - Get feedback from development team
2. **Task Creation** - Create tasks in your PM system
3. **Start Development** - Use Dev Agent to implement components
4. **Monitor Progress** - Track via PM Agent
5. **Iterate** - Adjust as you learn

---

**Questions?** Refer to [FIRST_TIME_USER_GUIDE.md](FIRST_TIME_USER_GUIDE.md) for framework concepts, or check [AGENT_GUIDE.md](AGENT_GUIDE.md) for agent operation details.
