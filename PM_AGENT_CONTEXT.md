# PM Agent Context & Enhancement Guide

This document analyzes what gives the PM Agent its "mind" and how to enhance it.

---

## Current PM Agent Setup (What It Has Now)

### 1. **Agent Definition** (`agents/pm_agent.py`)

**Current Mindset:**
```python
role = "Project Manager"

goal = (
    "Coordinate and manage the agentic framework project. "
    "Decompose complex tasks into manageable subtasks, "
    "delegate to appropriate agents, track progress, "
    "and escalate blockers or decisions that require human input."
)

backstory = (
    "You are an experienced project manager with expertise in "
    "coordinating autonomous agents. You excel at task decomposition, "
    "identifying dependencies, managing timelines, and making "
    "strategic decisions. You communicate clearly with team members "
    "and stakeholders, and you're not afraid to escalate issues "
    "when needed."
)
```

**Current Skillset (Default):**
- `log_action` - Log activities to audit trail
- `log_error` - Log errors and failures
- `git_status` - Check repository status

**Assessment**: ✅ Good foundation, but limited skills and context

---

## Context Files That Give the PM Agent Its "Mind"

### 1. **AGENT_GUIDE.md** ⭐ PRIMARY
The PM agent's **operating manual** that defines:
- **Responsibilities**: Task decomposition, delegate, track progress
- **Decision-making protocols**: When to auto-approve vs. escalate
- **Skills available**: 9 core skills the PM can use
- **Escalation procedures**: How to handle blockers
- **Communication channels**: PM_FEEDBACK.md, CONTEXT.md, etc.

**How it helps**: Gives PM agent the "rules of engagement"

### 2. **CONTEXT.md** ⭐ SECONDARY
The PM agent's **project knowledge base** containing:
- **Vision & goals**: What the project is trying to achieve
- **Architecture decisions**: Design patterns and choices made
- **Current state**: What's already done, in progress, not started
- **Milestones**: Project timeline and targets
- **Known limitations**: What we can't do yet

**How it helps**: Gives PM context for decision-making

### 3. **SKILL_GAPS.md** ⭐ SECONDARY
The PM agent's **awareness of limitations** showing:
- **Critical gaps**: Blocking issues to solve
- **Important gaps**: Nice-to-have improvements
- **Framework limitations**: Design constraints
- **Prioritization matrix**: What to work on first

**How it helps**: PM knows what we're lacking and can prioritize work

### 4. **tasks.yaml** ⭐ REFERENCE
The PM agent's **task catalog** defining:
- Available tasks (project_setup, agent_development, etc.)
- Subtasks for each
- Execution guidelines
- Workflows

**How it helps**: PM knows what work exists and how to structure it

### 5. **PM_FEEDBACK.md** ⭐ COMMUNICATION
The PM agent's **communication channel** for:
- Support requests from other agents
- Approval requests awaiting human decision
- Blockers that need escalation
- Questions about priorities

**How it helps**: PM knows where to request help and communicate needs

### 6. **TOOL_INVESTIGATION.md** & **SKILL_GAPS.md** ⭐ EVOLUTION
The PM agent's **improvement tracking** showing:
- Tools being evaluated
- Missing capabilities
- Enhancement priorities

**How it helps**: PM knows what the team wants to build next

### 7. **skills.json** ⭐ REFERENCE
The PM agent's **complete skills inventory** defining:
- All available skills (9 total)
- What each skill does
- Dependencies for each skill
- Status (active/experimental)

**How it helps**: PM knows what capabilities exist to delegate

---

## Context Flow Diagram

```
PM AGENT
   │
   ├─ MINDSET (agents/pm_agent.py)
   │   ├─ Role: Project Manager
   │   ├─ Goal: Coordinate agentic framework
   │   └─ Backstory: Experienced PM with agent coordination expertise
   │
   ├─ OPERATING PROCEDURES (AGENT_GUIDE.md)
   │   ├─ Task decomposition protocol
   │   ├─ Delegation rules
   │   ├─ Decision-making framework
   │   ├─ Escalation procedures
   │   └─ 9 available skills
   │
   ├─ PROJECT KNOWLEDGE (CONTEXT.md)
   │   ├─ Vision and goals
   │   ├─ Current state
   │   ├─ Milestones
   │   ├─ Architecture decisions
   │   └─ Known limitations
   │
   ├─ AWARENESS (SKILL_GAPS.md, TOOL_INVESTIGATION.md)
   │   ├─ Critical blockers
   │   ├─ Missing capabilities
   │   ├─ Tools being evaluated
   │   └─ Evolution priorities
   │
   ├─ COMMUNICATION (PM_FEEDBACK.md)
   │   ├─ Support requests
   │   ├─ Approval needs
   │   ├─ Escalations
   │   └─ Human decisions
   │
   └─ EXECUTION (skills.json, tasks.yaml)
       ├─ Available skills
       ├─ Available tasks
       └─ Workflows
```

---

## Current PM Agent Skill Set Analysis

### Has These Skills ✅
1. **log_action** - Record what it's doing
2. **log_error** - Record errors
3. **git_status** - Check project status

### Missing Skills ❌
1. **git_commit** - Can't commit decisions
2. **git_push** - Can't push changes
3. **read_log** - Can't review activity history
4. **run_flake8_lint** - Can't assess code quality
5. **run_black_format** - Can't suggest formatting
6. **Task analysis functions** - Custom analysis tools

---

## Enhancement Recommendations

### Level 1: Immediate (Easy)

**Enhancement 1.1: Expand Default Skillset**

Currently the PM agent gets 3 skills. We should add:
- `read_log` - Review recent activity and history
- `git_commit` - Commit decisions/plans to version control
- `git_branch` - Create branches for different work streams

**Why**: PM needs visibility into activity and ability to record decisions

### Level 2: Medium (Requires Thought)

**Enhancement 2.1: Context Awareness Function**

Create a new skill that lets PM agent:
- Read and summarize CONTEXT.md
- Read and summarize SKILL_GAPS.md
- Read and summarize PM_FEEDBACK.md
- Understand project state at a glance

**Why**: PM needs to understand project context before making decisions

**Enhancement 2.2: Enhanced Backstory**

Make the backstory more specific about:
- Knowledge of CrewAI and LangChain
- Understanding of autonomous agent patterns
- Awareness of project stakeholder needs
- Commitment to quality and testing

**Why**: Better backstory = better decisions and reasoning

### Level 3: Advanced (Requires Implementation)

**Enhancement 3.1: Task Analysis Tool**

Custom skill for PM to:
- Analyze complexity of incoming tasks
- Break down into subtasks automatically
- Estimate effort and dependencies
- Suggest agent delegation

**Why**: PM's core responsibility is task decomposition

**Enhancement 3.2: Decision Logger**

Custom skill for PM to:
- Formally log decision rationale
- Record approval/rejection reasons
- Create audit trail for decisions
- Suggest escalation when appropriate

**Why**: PM decisions are critical and need audit trails

**Enhancement 3.3: Progress Tracker**

Custom skill for PM to:
- Aggregate progress from other agents
- Identify blockers automatically
- Suggest course corrections
- Update CONTEXT.md with progress

**Why**: PM's responsibility includes progress tracking

---

## Proposed Enhanced PM Agent

Here's what an enhanced version could look like:

```python
def create_enhanced_pm_agent(name: str = "PM Agent") -> Agent:
    """Create an enhanced PM Agent with full context awareness"""
    
    from skills.logging_skill import log_action, log_error, read_log
    from skills.repo_management_skill import git_status, git_commit, git_branch
    from skills.context_awareness import (
        read_project_context,
        read_skill_gaps,
        read_feedback,
        summarize_project_state
    )
    from skills.decision_making import (
        analyze_task,
        decompose_task,
        log_decision,
        suggest_delegation
    )
    
    tools = [
        # Logging & Visibility
        log_action,
        log_error,
        read_log,
        
        # Repository Management
        git_status,
        git_commit,
        git_branch,
        
        # Context Awareness
        read_project_context,
        read_skill_gaps,
        read_feedback,
        summarize_project_state,
        
        # Decision Making
        analyze_task,
        decompose_task,
        log_decision,
        suggest_delegation,
    ]
    
    agent = Agent(
        role="Senior Project Manager (AI-Driven)",
        goal=(
            "Successfully coordinate and manage the agentic-infrastructure-framework project. "
            "Decompose complex work into clear subtasks, delegate to appropriate specialized agents, "
            "track progress transparently, maintain decision audit trails, escalate blockers promptly, "
            "and ensure continuous improvement toward the project vision."
        ),
        backstory=(
            "You are a senior project manager with 10+ years of experience managing technical projects "
            "and coordinating specialized teams. You have deep expertise in:\n"
            "- CrewAI and LangChain based agentic systems architecture\n"
            "- Autonomous agent coordination and delegation patterns\n"
            "- Complex technical project management and timeline estimation\n"
            "- Quality assurance and continuous improvement practices\n"
            "- Risk identification and mitigation strategies\n"
            "- Clear communication with technical teams and stakeholders\n\n"
            "Your approach: Start every task by understanding project context (vision, state, gaps). "
            "Decompose complexity into clear subtasks. Choose the right agent for each task. "
            "Track progress transparently. Make data-driven decisions. Escalate blockers immediately. "
            "Log all significant decisions with reasoning. Never assume - always verify. "
            "Prioritize quality and clarity over speed."
        ),
        verbose=True,
        allow_delegation=True,
        tools=tools,
    )
    
    return agent
```

---

## Implementation Roadmap

### Phase 1: Now
- [x] Current PM agent is functional
- [x] Has operating guide (AGENT_GUIDE.md)
- [x] Quick start works (my_first_task.py)

### Phase 2: This Week
- [ ] Expand default skillset (Level 1.1)
- [ ] Enhance backstory with more specifics (Level 2.2)
- [ ] Test with more complex tasks

### Phase 3: Next Week
- [ ] Create context_awareness skill (Level 2.1)
- [ ] Test PM agent on real project scenarios
- [ ] Log findings in CONTEXT.md

### Phase 4: Future
- [ ] Build task_analysis skill (Level 3.1)
- [ ] Build decision_logger skill (Level 3.2)
- [ ] Build progress_tracker skill (Level 3.3)
- [ ] Evaluate and refine based on real usage

---

## Files the PM Agent Should Read/Understand

### Must Read
1. **agents/pm_agent.py** - Know itself
2. **AGENT_GUIDE.md** - Know its role and procedures
3. **CONTEXT.md** - Know the project
4. **SKILL_GAPS.md** - Know what's missing

### Should Read
5. **tasks.yaml** - Know available work
6. **PM_FEEDBACK.md** - Know pending requests
7. **TOOL_INVESTIGATION.md** - Know what's being evaluated

### Reference As Needed
8. **skills.json** - Know available skills
9. **logs/agent_log.txt** - Know activity history

---

## How to Give PM Agent More Context

### Option A: Prompt Engineering
Update the backstory and goal to be more specific:
- Add more detail about project vision
- Reference specific architecture decisions
- Include known constraints
- Mention team member expectations

### Option B: Context Injection
Create skills that load context files:
- Read CONTEXT.md on startup
- Understand SKILL_GAPS.md
- Be aware of PM_FEEDBACK.md pending items

### Option C: System Prompts
Add system-level instructions about:
- How to handle ambiguity
- When to ask for clarification
- Decision-making frameworks
- Escalation triggers

### Option D: Memory Management
Implement agent memory that:
- Remembers past decisions
- Tracks what's been tried
- Learns from previous tasks
- Adapts approach based on experience

---

## Verification Checklist

### Does PM Agent Have Right Mindset? ✅
- [x] Clear role (Project Manager)
- [x] Specific goal (Coordinate framework)
- [x] Good backstory (Experienced PM)
- [ ] **TODO**: Add more detail about CrewAI/LangChain knowledge
- [ ] **TODO**: Add more detail about quality expectations

### Does PM Agent Have Right Skills? ⚠️
- [x] Can log activities (log_action)
- [x] Can handle errors (log_error)
- [x] Can check status (git_status)
- [ ] **TODO**: Add read_log for history
- [ ] **TODO**: Add git_commit for recording decisions
- [ ] **TODO**: Add context awareness skills
- [ ] **TODO**: Add task analysis skills

### Does PM Agent Understand Context? ⚠️
- [x] Knowledge of role (AGENT_GUIDE.md)
- [x] Knowledge of project (CONTEXT.md)
- [ ] **TODO**: Direct ability to read context files
- [ ] **TODO**: Automated state summarization
- [ ] **TODO**: Awareness of pending feedback

---

## Next Steps for Enhancement

Pick one:

**Quick Win** (30 minutes):
- Enhance the backstory in agents/pm_agent.py
- Add 3 more skills: read_log, git_commit, git_branch
- Test with my_first_task.py

**Solid Improvement** (2-3 hours):
- Create context_awareness skill module
- Enhance backstory
- Test PM agent reading CONTEXT.md and SKILL_GAPS.md
- Document findings

**Major Upgrade** (1 day+):
- Create all 3 advanced skill modules
- Fully enhanced backstory
- Comprehensive testing
- Ready for production use

---

## Questions to Consider

1. **What context should PM agent have on startup?**
   - Should it read CONTEXT.md and understand project state?
   - Should it know about recent activity from logs?

2. **How should PM agent make decisions?**
   - Based only on task description?
   - Or with awareness of project state, skill gaps, pending feedback?

3. **What should PM agent escalate?**
   - Critical decisions? Hard problems? Conflicts?
   - When should it ask human for input?

4. **How should PM agent evolve?**
   - Should it learn from past tasks?
   - Should it adapt its approach based on what worked?

---

**Created**: 2026-02-14
**Purpose**: Guide PM Agent enhancement with proper context awareness
