# Agentic Framework Architecture - Multi-Project Model

## Overview

The **agentic-infrastructure-framework** serves as a reusable template and core foundation for multiple projects. Projects are independent clones that can customize and extend the framework, with a feedback mechanism to promote improvements back to the core.

## Repository Structure

```
c:\Users\Keagan\projects\
│
├── agentic-infrastructure-framework/          [CORE TEMPLATE]
│   ├── agents/
│   ├── skills/                                (general, tested skills only)
│   ├── templates/
│   ├── PM_INIT_* (all PM documentation)
│   ├── README.md
│   └── VERSION: Core framework version
│
├── pricewize-prd-project/                     [PROJECT 1]
│   ├── agents/
│   ├── skills/                                (+ pricewize-specific skills)
│   ├── .project/                              (PM artifacts)
│   ├── README.md
│   └── FRAMEWORK_VERSION: 1.0.0 (tracks origin)
│
├── another-saas-app/                          [PROJECT 2]
│   ├── agents/
│   ├── skills/                                (+ app-specific skills)
│   ├── .project/
│   └── FRAMEWORK_VERSION: 1.0.0
│
└── internal-tool/                             [PROJECT 3]
    ├── agents/
    ├── skills/                                (+ tool-specific skills)
    └── .project/
```

## Workflow

### Creating a New Project

```bash
# Step 1: Clone framework as template
cd c:\Users\Keagan\projects\
cp -r agentic-infrastructure-framework my-new-project
cd my-new-project

# Step 2: Initialize as independent repo
git init
git remote add origin https://github.com/YourOrg/my-new-project.git
git branch -M main
git add .
git commit -m "Initial commit: Agentic framework template v1.0.0"
git push -u origin main

# Step 3: Document the origin
echo "FRAMEWORK_VERSION=1.0.0" > .frameworkrc
```

### Project Development

**In your project:**
1. Use PM initialization system to design your feature
2. Implement project-specific agents and skills
3. Add skills to `skills/` directory
4. Document in project README

**Project structure stays clean:**
- Framework code unchanged
- Project customizations isolated in skills/
- PM artifacts track design decisions

### Promoting Skills Back to Framework

**When you discover a generally useful skill:**

#### Promotion Checklist:
- [ ] Skill solves a common problem (not project-specific)
- [ ] Well-tested in production
- [ ] Documented with docstrings
- [ ] No project-specific dependencies
- [ ] Works with multiple agent types
- [ ] Follows framework conventions

#### Promotion Process:

**1. In your project:**
```bash
# Ensure skill is polished
cd my-new-project/skills
# Review: skill_name.py
```

**2. Copy to framework:**
```bash
cp my-new-project/skills/general_skill.py \
   agentic-infrastructure-framework/skills/

# Update framework skills.json
# Add entry to agentic-infrastructure-framework/skills.json
```

**3. Update framework:**
```bash
cd agentic-infrastructure-framework

# Update documentation
echo "## New Skill: general_skill" >> SKILL_GAPS.md

# Commit
git add .
git commit -m "Add general_skill - promoted from my-new-project"
git tag v1.1.0
git push origin main
```

**4. Pull improvement into all projects:**
```bash
# In each project
cd my-other-project
git fetch upstream  # if configured
# Or manually copy new skills
```

## Version Management

### Framework Versioning
```
agentic-infrastructure-framework/
├── VERSION = 1.0.0 (tag: v1.0.0)
├── CHANGELOG.md
└── PROMOTED_SKILLS.md  (list of skills that came from projects)
```

### Project Tracking
```
my-new-project/
├── .frameworkrc = FRAMEWORK_VERSION=1.0.0
├── CUSTOM_SKILLS.md = List of project-specific skills
└── IMPROVEMENTS.md = Potential skills to promote
```

## Decision Tree: Keep or Promote?

```
Is this skill...
├─ Project-specific? (e.g., "pricewize_price_calculator")
│  └─ NO → Keep in project/skills/
│
├─ Solves general problem? (e.g., "generic_api_caller")
│  └─ YES → Consider promoting
│
├─ Tested and stable?
│  └─ YES → Can promote
│
├─ Well documented?
│  └─ YES → Ready to promote
│
└─ Should go to framework → Promote!
```

## Benefits of This Model

✅ **Separation of Concerns**
- Framework stays clean and focused
- Projects are independent

✅ **Continuous Improvement**
- Framework improves through real-world use
- All projects benefit from promoted skills

✅ **Risk Management**
- Experimental code stays in projects
- Only proven code reaches framework

✅ **Scalability**
- Easy to create new projects
- Each project can evolve independently

✅ **Knowledge Sharing**
- Good ideas spread across all projects
- Framework documents best practices

## Implementation Timeline

### Phase 1: Framework Ready ✓
- Core template built
- PM initialization system working
- Documentation complete

### Phase 2: First Project (pricewize-prd)
- Clone framework
- Define with PM system
- Build project-specific skills
- Document improvements

### Phase 3: Promotion Pipeline
- Identify reusable skills
- Create promotion process
- Update framework
- Sync other projects

### Phase 4: Scale
- Add more projects
- Continuous feedback loop
- Framework grows stronger

## Example: Skill Promotion Journey

```
Discovery Phase:
├─ You build "smart_caching_skill" for pricewize-prd
│  └─ Works great, speeds up all agents
│
├─ Think: "Other projects would benefit!"
│  └─ This is generally useful
│
└─ It's well-tested and stable

Promotion Phase:
├─ Copy to framework/skills/smart_caching_skill.py
├─ Add to framework/skills.json
├─ Update framework docs
└─ Commit as "Promote: smart_caching_skill from pricewize-prd"

Propagation Phase:
├─ All NEW projects get it automatically
├─ Existing projects can pull manually
└─ Framework improves for everyone
```

## Next Steps

1. **Keep agentic-infrastructure-framework pristine** - It's your template
2. **Create pricewize-prd-project** - First real project
3. **Use PM system** - Design it properly
4. **Build & discover** - Develop project-specific skills
5. **Promote** - When general skills emerge
6. **Repeat** - With each new project

---

**Your Vision in Action:**
- Framework = constantly improving foundation
- Projects = laboratories for innovation
- Skills = discoveries that benefit everyone
- Win-win for each project and the core system
