# PM Feedback & Support Requests

This file is for logging questions, support requests, or feedback that the agents need from the project owner or human collaborators. Use this as a communication channel for approvals, clarifications, and escalations.

## How to Use
- Agents add entries when they need clarification, guidance, approval, or support
- Project owner responds directly in this file or schedules a review
- Reference this file regularly to stay aligned with agent needs
- Date entries for tracking response times

---

## Feedback Log

### Setup & Configuration [PENDING RESPONSE]

**[2026-02-10]** GitHub Repository Setup
- **From**: GitHub Copilot (Initial Setup)
- **Status**: Pending
- **Request**: The framework is ready to push to GitHub. Options:
  1. Manual push: You create a private repo on GitHub and we push locally
  2. Automatic: Provide GitHub personal access token for automated creation
- **Required Decision**: Which approach would you prefer? If automatic, provide token.
- **Impact**: Needed before first code push

### Configuration Questions [PENDING RESPONSE]

**[2026-02-10]** API Keys & Environment Setup
- **From**: Framework Setup
- **Status**: Pending
- **Question**: Which LLM providers should we configure? (OpenAI, Anthropic, etc.)
- **Action Item**: Update `.env.example` with API key placeholders
- **Target Resolution**: Before running agents

### Documentation Review [PENDING RESPONSE]

**[2026-02-10]** Guide Customizations
- **From**: GitHub Copilot
- **Status**: Pending
- **Issue**: Review the generated AGENT_GUIDE.md, CONTEXT.md, and SKILL_GAPS.md
- **Question**: Do these align with your project vision? Any adjustments needed?
- **Action Item**: Provide feedback on structure and content

---

## Common Escalation Types

### Approval Requests
Use format:
```
**[DATE]** Feature/Change Name
- **From**: AGENT_NAME
- **Status**: Pending Approval
- **Description**: What needs approval?
- **Options**: List alternatives if multiple paths
- **Recommended**: Which option makes most sense?
```

### Clarification Requests
Use format:
```
**[DATE]** Topic Name
- **From**: AGENT_NAME
- **Status**: Blocked - Needs Clarification
- **Question**: What are we unclear about?
- **Impact**: How does this block progress?
- **Timeline**: When do we need an answer?
```

### Support/Help Requests
Use format:
```
**[DATE]** Issue Description
- **From**: AGENT_NAME
- **Status**: Needs Support
- **Problem**: What's the issue?
- **Attempted Solutions**: What have we tried?
- **Help Needed**: What do you need from us?
```

---

## Response Guidelines

### Priority Levels
- **🔴 CRITICAL**: Respond ASAP (security issues, data loss, system down)
- **🟠 HIGH**: Respond within 24 hours (blockers, major features)
- **🟡 MEDIUM**: Respond within 3 days (improvements, questions)
- **🟢 LOW**: Respond when convenient (feedback, nice-to-haves)

### Response Format
When responding, use:
```
**[2026-02-10]** RESPONSE to [Original Issue Title]
- **Decision**: What's the decision?
- **Rationale**: Why this choice?
- **Action Items**: What are agents expected to do?
- **Timeline**: When should this be done?
```

---

## Historical Feedback (Resolved)
*Entries moved here after resolution*

---

## Next Steps for Project Owner

1. **Pull this file from GitHub** to see all pending requests
2. **Review each pending item** above
3. **Provide responses** in the format specified
4. **Set up a regular review cycle** (daily/weekly check-ins recommended)
5. **Update PM_FEEDBACK.md** with responses so agents continue forward

**For questions about entries**: Check the agent that logged them or review CONTEXT.md and AGENT_GUIDE.md for more context.

---

Last Updated: 2026-02-10
