# PM Initialization Quick Start

**✅ Implementation Complete** | 5 Components Built | 3 Interactive Phases | Ready to Use

## TL;DR

Start your project definition in 3 commands:

```bash
# Phase 1: Define your project (scoping)
python pm_init.py

# Phase 2: Break it into objectives and milestones
python pm_decompose.py

# Phase 3: Design the technical solution
python pm_architect.py

# ✅ Your project is now fully defined!
```

## What Gets Created

After completing all phases, you'll have three markdown documents in `.project/`:

1. **project_brief.md** - Your project vision, goals, and success metrics
2. **project_decomposition.md** - Objectives, components, and timeline
3. **technical_proposal.md** - Tech stack and agent architecture

These become your project's blueprint.

## Getting Started (5 minutes)

### Step 1: Run Health Check + Phase 1
```bash
python pm_init.py
```
You'll see:
- Framework validation
- Welcome message
- Choice: "Do you have an idea (A) or existing brief (B)?"

### If you have an IDEA (Option A):
Agent asks you 5-6 discovery questions. You answer. Brief is created.

### If you have a BRIEF (Option B):
Paste your brief. Agent asks refinement questions. Brief is deepened.

### Step 2: Run Decomposition
```bash
python pm_decompose.py
```
Agent breaks your brief into:
- 3-5 core objectives
- Major components/phases
- Milestone timeline

You review and approve.

### Step 3: Run Architecture
```bash
python pm_architect.py
```
Agent proposes:
- Tech stack
- Agent architecture (PM, Dev, etc.)
- Required skills
- Implementation plan

✅ Done! Your project is ready.

## File Structure

```
pm_init.py                          ← Phase 1: Start here
pm_decompose.py                     ← Phase 2: Run next
pm_architect.py                     ← Phase 3: Run last
framework_health_check.py           ← Validates dependencies

agents/
  pm_business_architect.py          ← Phase 1 agent
  pm_decomposer.py                  ← Phase 2 agent
  pm_solution_architect.py          ← Phase 3 agent

.project/                           ← Created during init
  project_brief.md                  ← Phase 1 output
  project_decomposition.md          ← Phase 2 output
  technical_proposal.md             ← Phase 3 output
```

## Common Questions

**Q: Do I have to do all three phases?**
A: No. If you already have a brief, skip to `pm_decompose.py`. If you have both, jump to `pm_architect.py`.

**Q: Can I go back and edit?**
A: Absolutely. Edit any .project/X.md file and re-run the next phase to get new output.

**Q: What if health check fails?**
A: See `.framework/framework_checklist.md` for what's missing. Usually just needs: `pip install -r requirements.txt` and `.env` setup.

**Q: Can I skip a phase?**
A: Each phase needs the previous one's output. Skip Phase 1 only if you already have a brief.

**Q: How long does each phase take?**
A: 10-20 minutes each. Total: 30-60 minutes for full flow.

## Next: Full Documentation

For detailed explanations, see: [PM_INITIALIZATION_GUIDE.md](PM_INITIALIZATION_GUIDE.md)

For implementation details, see: [PM_INIT_IMPLEMENTATION_SUMMARY.md](PM_INIT_IMPLEMENTATION_SUMMARY.md)

---

🚀 **Ready?** Run: `python pm_init.py`
