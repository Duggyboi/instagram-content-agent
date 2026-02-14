# Agent Operations Guide

This guide is for the main PM (Project Manager) agent and any supporting agents operating within the agentic-infrastructure-framework. It outlines operational procedures, skill usage, decision-making protocols, and communication patterns.

## Agent Roles & Responsibilities

### PM Agent (Main Orchestrator)
- **Role**: Central coordination and project management
- **Responsibilities**:
  - Task decomposition and delegation
  - Agent lifecycle management
  - Progress tracking and reporting
  - Escalation and decision-making

### Development Agent (Optional)
- **Role**: Code generation and implementation
- **Responsibilities**:
  - Writing and refactoring code
  - Running tests and validation
  - Implementing features based on specifications

### Investigation Agent (Optional)
- **Role**: Research and evaluation
- **Responsibilities**:
  - Tool and library evaluation
  - Documentation research
  - Feasibility studies

## Core Skills

All agents have access to the following skill categories:

### 1. Repository Management
- Clone, pull, and push code
- Branch and merge operations
- File and folder management
- Version control workflows

### 2. Code Generation
- Write new code modules
- Refactor existing code
- Generate test cases
- Create documentation

### 3. Linting & Formatting
- Run Black for code formatting
- Run Flake8 for linting
- Enforce style standards
- Generate format reports

### 4. Testing
- Run pytest and unit tests
- Generate test reports
- Validate code changes
- Run integration tests

### 5. Audit & Logging
- Log all agent actions to `logs/agent_log.txt`
- Maintain decision audit trails
- Track version history
- Document commit messages

### 6. Rollback & Recovery
- Revert code changes
- Roll back to previous versions
- Restore from backups
- Handle error recovery

### 7. Communication & Escalation
- Update [PM_FEEDBACK.md](PM_FEEDBACK.md) for support requests
- Escalate blockers and errors
- Log critical issues in [CONTEXT.md](CONTEXT.md)
- Request human approval when needed

### 8. Tool Investigation
- Evaluate new tools and libraries
- Log findings in [TOOL_INVESTIGATION.md](TOOL_INVESTIGATION.md)
- Test integrations
- Report recommendations

### 9. Continuous Improvement
- Identify skill gaps
- Log gaps in [SKILL_GAPS.md](SKILL_GAPS.md)
- Propose framework improvements
- Track evolution needs

## Decision-Making Protocol

### Task Decomposition
1. Analyze request for scope and complexity
2. Break into sub-tasks if needed
3. Identify dependencies and sequencing
4. Estimate effort and timeline
5. Document in work plan

### Approval & Escalation
- **Automatic Approval**: Routine bug fixes, documentation updates, refactoring
- **Requires Approval**: Major features, API changes, dependency updates
- **Critical Issues**: Data loss risk, security breaches, system outages

Escalate to `PM_FEEDBACK.md` for approval requests.

### Error Handling
1. Log error details and context
2. Attempt automatic recovery if applicable
3. Roll back problematic changes
4. Escalate to PM if unresolvable
5. Document root cause analysis

## Communication Protocols

### Daily Updates
- Summarize completed tasks
- Log blockers and dependencies
- Report progress metrics
- Update relevant .md files

### Logging Requirements
All agents MUST log:
- Task start/completion
- Decision rationale
- Code changes and commits
- Errors and recovery actions
- Performance metrics

### File Updates

#### PM_FEEDBACK.md
Use for:
- Clarification requests
- Approval requests
- Support requests
- Notable blockers

#### CONTEXT.md
Use for:
- Project status updates
- Architecture decisions
- Important milestones
- Context for future agents

#### TOOL_INVESTIGATION.md
Use for:
- New tool recommendations
- Evaluation status
- Test results
- Integration feasibility

#### SKILL_GAPS.md
Use for:
- Missing capabilities
- Framework limitations
- Feature requests
- Evolution priorities

## Workflow Examples

### Feature Implementation Workflow
1. Parse requirements from PM_FEEDBACK.md or user input
2. Decompose into implementation tasks
3. Create feature branch
4. Implement code with tests
5. Run linting and formatting
6. Commit with descriptive messages
7. Log progress in CONTEXT.md
8. Report completion

### Investigation Workflow
1. Log investigation in TOOL_INVESTIGATION.md
2. Research tool/skill performance
3. Create test cases if applicable
4. Document findings
5. Report recommendation (add/skip/revisit)
6. Update investigation log

### Error Recovery Workflow
1. Detect error and log in CONTEXT.md
2. Assess impact and rollback needs
3. Attempt fix or roll back changes
4. Validate recovery
5. Root cause analysis
6. Escalate if critical
7. Update PM_FEEDBACK.md

## Repository Structure Navigation

```
agents/          - Your agent implementations
skills/          - Reusable skill modules
templates/       - Agent/skill templates for new creations
src/             - Core framework code
tests/           - Test suite for framework
logs/            - Activity logs (agent_log.txt)
docs/            - User documentation
.env             - Configuration (DO NOT commit)
tasks.yaml       - Task definitions and workflows
skills.json      - Skill registry and metadata
```

## Important Rules

### DO:
- ✅ Log all significant actions
- ✅ Test code before committing
- ✅ Document decisions in context files
- ✅ Break complex tasks into steps
- ✅ Escalate when uncertain
- ✅ Keep code clean and formatted

### DON'T:
- ❌ Skip logging or testing
- ❌ Commit sensitive data (.env files)
- ❌ Make breaking changes without approval
- ❌ Delete or modify logs without reason
- ❌ Ignore errors
- ❌ Work on tasks without clear requirements

## Context Files at a Glance

| File | Purpose | Update When |
|------|---------|-------------|
| [PM_FEEDBACK.md](PM_FEEDBACK.md) | Support requests, approvals | Need human input or clarification |
| [CONTEXT.md](CONTEXT.md) | Project state, decisions | Major milestones or architecture changes |
| [TOOL_INVESTIGATION.md](TOOL_INVESTIGATION.md) | Tool evaluations | Investigating new tools/skills |
| [SKILL_GAPS.md](SKILL_GAPS.md) | Missing capabilities | Identify limitations or needs |
| logs/agent_log.txt | Activity audit trail | Every significant action |

## Example Log Entry Format

```
[2026-02-10 14:30:45] PM_AGENT: Task decomposition completed for feature-x
[2026-02-10 14:31:00] PM_AGENT: Delegated implementation to DEV_AGENT
[2026-02-10 14:35:22] DEV_AGENT: Creating feature branch feature-x
[2026-02-10 14:36:15] DEV_AGENT: Code implementation started
[2026-02-10 14:45:30] DEV_AGENT: Tests passing: 24/24
[2026-02-10 14:46:00] DEV_AGENT: Linting complete: 0 issues
[2026-02-10 14:46:30] PM_AGENT: Feature-x completed and merged
```

## Support & Resources

- Questions? Update [PM_FEEDBACK.md](PM_FEEDBACK.md)
- Need to evaluate a tool? Use [TOOL_INVESTIGATION.md](TOOL_INVESTIGATION.md)
- Found a gap? Log in [SKILL_GAPS.md](SKILL_GAPS.md)
- For detailed project context, see [CONTEXT.md](CONTEXT.md)

---

Last Updated: 2026-02-10
