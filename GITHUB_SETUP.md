# GitHub Setup Instructions

This document provides step-by-step instructions for pushing your agentic-infrastructure-framework repository to GitHub.

## Prerequisites

1. **GitHub Account**: Ensure you have a GitHub account at https://github.com
2. **Git Installed**: Verify git is installed on your machine
   ```bash
   git --version
   ```
3. **Git Configured**: Set up git with your credentials
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@github.com"
   ```

## Option 1: Manual Setup (Recommended for First Time)

Follow these steps to create the repository on GitHub and push locally:

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Enter repository name: `agentic-infrastructure-framework`
3. Select **Private** (as per your requirements)
4. DO NOT initialize with README, .gitignore, or license (we already have these)
5. Click **Create repository**

### Step 2: Configure Local Repository

In your project directory, run these commands:

```bash
# Initialize git (if not already done)
git init

# Add all files to staging
git add .

# Create initial commit
git commit -m "Initial commit: Agentic Infrastructure Framework scaffolding

- Complete project structure with agents and skills modules
- Core documentation (README, AGENT_GUIDE, CONTEXT)
- Support tracking files (PM_FEEDBACK, TOOL_INVESTIGATION, SKILL_GAPS)
- Skill examples (logging, repo management, code quality)
- Agent templates (PM Agent, Dev Agent)
- Configuration files and requirements"

# Add the remote repository
git branch -M main
git remote add origin https://github.com/your-username/agentic-infrastructure-framework.git

# Push to GitHub
git push -u origin main
```

**Replace `your-username` with your actual GitHub username.**

### Step 3: Configure SSH (Optional but Recommended)

For future pushes without entering credentials, set up SSH:

```bash
# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your.email@github.com"

# Add SSH key to GitHub
# 1. Copy the public key from ~/.ssh/id_ed25519.pub
# 2. Go to GitHub Settings > SSH and GPG keys
# 3. Click "New SSH key" and paste the content
# 4. Then switch remote to SSH:
git remote set-url origin git@github.com:your-username/agentic-infrastructure-framework.git
```

### Step 4: Verify Setup

```bash
# Check remote URL
git remote -v

# Should show:
# origin  https://github.com/your-username/agentic-infrastructure-framework.git (fetch)
# origin  https://github.com/your-username/agentic-infrastructure-framework.git (push)
```

---

## Option 2: Using GitHub CLI (Faster)

If you have GitHub CLI installed:

```bash
# Install GitHub CLI if needed (https://cli.github.com/)

# Login to GitHub
gh auth login

# Create repository directly
gh repo create agentic-infrastructure-framework \
  --private \
  --source=. \
  --remote=origin \
  --push

# Verify
gh repo view
```

---

## Option 3: Using GitHub Desktop (GUI Alternative)

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Sign in with your GitHub account
3. File → New Repository
4. Set repository name and local path
5. Publish to GitHub as Private

---

## Security: Protecting Sensitive Files

### Important: Never Commit `.env` File

Before pushing, ensure:

1. **`.env` is in `.gitignore`** (already configured)
   ```bash
   # Verify
   cat .gitignore | grep "\.env"
   ```

2. **Only `.env.example` should be in the repo** (already the case)
   ```bash
   # Verify - should exist
   ls -la .env.example
   
   # Verify - should NOT exist in git
   git ls-files | grep "\.env"
   ```

3. **If you accidentally committed .env, remove it:**
   ```bash
   git rm --cached .env
   git commit -m "Remove sensitive .env file from git history"
   ```

### Adding to `.gitignore` (If Needed)

```bash
# Check current .gitignore
cat .gitignore

# Should include:
# .env
# .env.local
# *.pyc
# __pycache__/
# .venv/
# venv/
```

---

## GitHub Repository Settings

After pushing, configure your repository:

### Branch Protection (Optional)

1. Go to Settings → Branches
2. Click "Add rule"
3. Set branch name pattern: `main`
4. Enable "Require pull request reviews"
5. Enable "Require status checks to pass"

### Collaborators (When Needed)

1. Settings → Collaborators
2. Invite team members
3. Set appropriate permissions (Developer, Maintainer, etc.)

### Issues & Discussions

1. Settings → Features
2. Enable Issues for bug tracking
3. Enable Discussions for community

### GitHub Actions (For CI/CD Future)

When you're ready to set up automated testing:

1. Create `.github/workflows/tests.yml`
2. Configure pytest runs on push/PR
3. Add badge to README

---

## Verifying Your Setup

```bash
# Check current repository status
git status

# Check remote configuration
git remote -v

# View git log
git log --oneline

# Verify GitHub connection
git ls-remote origin
```

All should show your repository with 0 commits initial state, then your initial commit after push.

---

## Troubleshooting

### Error: "fatal: not a git repository"
```bash
# Initialize git
git init
git add .
git commit -m "Initial commit"
```

### Error: "remote origin already exists"
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/your-username/agentic-infrastructure-framework.git
```

### Error: "The branch 'main' is not fully merged"
```bash
# Reset branch
git branch -M main
git push -u origin main
```

### Error: "Authentication failed"
- Install [GitHub CLI](https://cli.github.com/) and run `gh auth login`
- Or [Generate Personal Access Token](https://github.com/settings/tokens) and use it as password

### Error: "Permission denied (publickey)"
- If using SSH, ensure your public key is added to GitHub
- Run `ssh -T git@github.com` to test SSH connection

---

## Next Steps After GitHub Setup

1. **Add collaborators** if working with a team
2. **Enable GitHub Actions** for CI/CD when ready
3. **Create GitHub Issues** for tasks and bugs
4. **Use GitHub Discussions** for design decisions
5. **Link to external docs** (deploy to GitHub Pages if needed)

---

## Useful Git Commands

```bash
# Check status
git status

# View branches
git branch -a

# Create a feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Descriptive commit message"

# Push to remote
git push origin feature/my-feature

# Create pull request on GitHub (via web interface)
# Merge PR, then sync locally:
git checkout main
git pull origin main

# Delete local feature branch
git branch -d feature/my-feature

# View git history
git log --oneline
git log --graph --all --oneline
```

---

## Resources

- [GitHub Docs - Creating a repository](https://docs.github.com/en/get-started/quickstart/create-a-repo)
- [GitHub Docs - Pushing commits to a remote repository](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository)
- [GitHub Docs - SSH Keys](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)

---

## Support

If you encounter issues:

1. **Check GitHub Status**: https://www.githubstatus.com/
2. **Review GitHub Docs**: https://docs.github.com/
3. **Log in PM_FEEDBACK.md**: If you need help from the PM agent
4. **GitHub Community**: https://github.community/

---

**Repository**: https://github.com/your-username/agentic-infrastructure-framework  
**Created**: 2026-02-10  
**Last Updated**: 2026-02-10
