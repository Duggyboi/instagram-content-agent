# PM Initialization System - Verification Checklist

Use this checklist to verify the PM initialization system is fully installed and working.

## ✅ Files Created

### Core Scripts (in root directory)
- [ ] `framework_health_check.py` - Health check module
- [ ] `pm_init.py` - Phase 1 entry point
- [ ] `pm_decompose.py` - Phase 2 script
- [ ] `pm_architect.py` - Phase 3 script

### Agents (in agents/ directory)
- [ ] `pm_business_architect.py` - Phase 1 agent
- [ ] `pm_decomposer.py` - Phase 2 agent
- [ ] `pm_solution_architect.py` - Phase 3 agent

### Documentation
- [ ] `PM_INITIALIZATION_GUIDE.md` - Full user guide
- [ ] `PM_INIT_IMPLEMENTATION_SUMMARY.md` - Implementation details
- [ ] `PM_INIT_QUICKSTART.md` - Quick reference
- [ ] `README.md` - Updated with PM system links

### Directories
- [ ] `.project/` - Project artifacts directory (created on first run)
- [ ] `.framework/` - Framework health check outputs (created if issues found)

## ✅ Health Check Tests

### Python Environment
- [ ] Python 3.10 or higher installed
- [ ] Virtual environment activated (if using one)

### Dependencies
```bash
# Verify these packages are installed:
pip list | grep -i crewai
pip list | grep -i langchain
pip list | grep -i pytest
pip list | grep -i black
pip list | grep -i flake8
```
- [ ] CrewAI installed
- [ ] LangChain installed
- [ ] pytest installed
- [ ] Black installed
- [ ] Flake8 installed

### Configuration
- [ ] `.env` file exists
- [ ] At least one API key configured in `.env`

### Repository
- [ ] Git initialized (`.git/` directory exists)

## ✅ Functional Tests

### Test 1: Health Check Runs Successfully
```bash
python framework_health_check.py
```
Expected: 
- [ ] All checks pass or
- [ ] Issues generate `framework_checklist.md`

### Test 2: PM Init Phase 1 Starts
```bash
python pm_init.py
```
Expected:
- [ ] Health check runs
- [ ] Welcome message appears
- [ ] User is prompted for Option A or B
- [ ] Can be interrupted with Ctrl+C

### Test 3: Phase 1 with Option A (Idea)
```bash
python pm_init.py
# Select Option A
# Provide test answers
```
Expected:
- [ ] Agent asks discovery questions
- [ ] Can answer multiple questions
- [ ] Brief is synthesized
- [ ] `.project/project_brief.md` created
- [ ] User is asked about next steps

### Test 4: Phase 1 with Option B (Brief)
```bash
python pm_init.py
# Select Option B
# Paste test brief
```
Expected:
- [ ] Can paste multi-line text
- [ ] Agent asks clarification questions
- [ ] Brief is refined
- [ ] `.project/project_brief.md` created
- [ ] User is asked about next steps

### Test 5: Phase 2 Decomposition
```bash
python pm_decompose.py
```
Expected:
- [ ] Checks for `.project/project_brief.md`
- [ ] Shows error if brief missing (good)
- [ ] If brief exists: Agent reads it
- [ ] Decomposes into objectives/components/milestones
- [ ] `.project/project_decomposition.md` created
- [ ] User is asked about next steps

### Test 6: Phase 3 Architecture
```bash
python pm_architect.py
```
Expected:
- [ ] Checks for `.project/project_decomposition.md`
- [ ] Shows error if decomposition missing (good)
- [ ] Reads decomposition and brief (if exists)
- [ ] Proposes technical solution
- [ ] `.project/technical_proposal.md` created
- [ ] "Ready for implementation" message shown

## ✅ Output Files Verification

After running Phase 1:
```bash
cat .project/project_brief.md
```
- [ ] File exists and is readable
- [ ] Contains: Problem Statement, Target Users, Outcomes, Success Metrics, Scope, Constraints, Dependencies, Risks

After running Phase 2:
```bash
cat .project/project_decomposition.md
```
- [ ] File exists and is readable
- [ ] Contains: Objectives, Components, Milestones, Risk analysis

After running Phase 3:
```bash
cat .project/technical_proposal.md
```
- [ ] File exists and is readable
- [ ] Contains: Tech Stack, Agent Architecture, Skills, Implementation Plan

## ✅ Documentation Verification

#### README.md
```bash
grep -i "pm initialization" README.md
```
- [ ] Links to `PM_INIT_QUICKSTART.md`
- [ ] Links to `PM_INITIALIZATION_GUIDE.md`

#### Quick Start Guide
```bash
cat PM_INIT_QUICKSTART.md
```
- [ ] Readable and helpful
- [ ] Shows quick start commands
- [ ] Says "python pm_init.py" to start

#### Full Guide
```bash
cat PM_INITIALIZATION_GUIDE.md
```
- [ ] Comprehensive (200+ lines)
- [ ] Explains all 4 stages
- [ ] Shows workflows and use cases
- [ ] Includes troubleshooting

#### Implementation Summary
```bash
cat PM_INIT_IMPLEMENTATION_SUMMARY.md
```
- [ ] Lists all components built
- [ ] Shows file structure
- [ ] Explains key features
- [ ] Provides usage examples

## ✅ Error Handling Tests

### Test: Missing .env
```bash
# Temporarily rename .env
mv .env .env.bak
python pm_init.py
# Should either warn or show in health check
mv .env.bak .env
```
- [ ] Handles gracefully
- [ ] Provides helpful error message

### Test: Missing Directory
```bash
# Temporarily remove agents directory
mv agents agents.bak
python pm_init.py
# Should show in health check
mv agents.bak agents
```
- [ ] Health check catches it
- [ ] Generates checklist
- [ ] Explains what's needed

### Test: Interrupted Phase
```bash
python pm_init.py
# Press Ctrl+C during Phase 1
```
- [ ] Gracefully interrupts
- [ ] Shows "cancelled by user" message
- [ ] Can re-run safely

### Test: Missing Previous Phase
```bash
python pm_decompose.py
# Without running pm_init.py first
```
- [ ] Shows helpful error
- [ ] Tells user to run pm_init.py first
- [ ] Exits cleanly

## ✅ Integration Tests

### Test: Full Flow
```bash
python pm_init.py      # Phase 1
python pm_decompose.py # Phase 2
python pm_architect.py # Phase 3
```
- [ ] All phases run successfully
- [ ] Three output files created
- [ ] Can be run in sequence without errors

### Test: Skip to Middle
```bash
# Assuming brief exists
python pm_decompose.py
# Then skip back
python pm_architect.py
```
- [ ] Can start decomposition without pm_init.py
- [ ] Can start architecture without earlier phases

## ✅ Performance Checks

- [ ] pm_init.py runs (health check < 2 seconds)
- [ ] Agent initialization < 5 seconds
- [ ] Interaction prompts appear immediately
- [ ] No hanging or long delays

## ✅ Code Quality

### Style
```bash
black --check *.py agents/*.py
```
- [ ] Code is properly formatted

### Linting
```bash
flake8 *.py agents/*.py
```
- [ ] No major lint issues

### Type Checking (if enabled)
```bash
mypy *.py
```
- [ ] Type hints are valid

## Summary

**Total Checks:** ~50
**Completion Target:** 100%

Once all checks pass:
1. ✅ System is fully installed
2. ✅ All components working
3. ✅ Ready for production use
4. ✅ Can guide projects from idea to execution

---

**Need Help?**
- See [PM_INIT_QUICKSTART.md](PM_INIT_QUICKSTART.md) for quick answers
- See [PM_INITIALIZATION_GUIDE.md](PM_INITIALIZATION_GUIDE.md) for detailed docs
- See `logs/agent_log.txt` for detailed logs if issues occur
