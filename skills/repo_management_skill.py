"""
Repository Management Skill

Provides Git and repository management capabilities for agents
to handle version control operations.
"""

from langchain.tools import tool
from typing import List, Optional
import logging
import subprocess
import os

logger = logging.getLogger(__name__)


def _run_git_command(command: List[str]) -> tuple[int, str, str]:
    """
    Run a git command and return exit code, stdout, stderr.
    
    Args:
        command: Git command as list of strings
        
    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Git command timed out"
    except Exception as e:
        return 1, "", str(e)


@tool
def git_status(repo_path: str = ".") -> str:
    """
    Get the current git status of the repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        Git status output
    """
    try:
        code, stdout, stderr = _run_git_command(["git", "-C", repo_path, "status"])
        
        if code != 0:
            logger.error(f"Git status failed: {stderr}")
            return f"Error: {stderr}"
        
        logger.info("Retrieved git status")
        return stdout
        
    except Exception as e:
        logger.error(f"Failed to get git status: {e}")
        raise


@tool
def git_commit(repo_path: str, message: str) -> str:
    """
    Commit changes to the repository.
    
    Args:
        repo_path: Path to the repository
        message: Commit message
        
    Returns:
        Commit confirmation message
    """
    try:
        # Stage all changes
        code, _, stderr = _run_git_command(["git", "-C", repo_path, "add", "."])
        if code != 0:
            return f"Error staging changes: {stderr}"
        
        # Commit
        code, stdout, stderr = _run_git_command(
            ["git", "-C", repo_path, "commit", "-m", message]
        )
        
        if code != 0:
            return f"Error committing: {stderr}"
        
        logger.info(f"Committed: {message}")
        return f"✓ Committed: {message}"
        
    except Exception as e:
        logger.error(f"Failed to commit: {e}")
        raise


@tool
def git_push(repo_path: str = ".", branch: str = "main") -> str:
    """
    Push commits to the remote repository.
    
    Args:
        repo_path: Path to the repository
        branch: Branch to push to
        
    Returns:
        Push confirmation message
    """
    try:
        code, stdout, stderr = _run_git_command(
            ["git", "-C", repo_path, "push", "origin", branch]
        )
        
        if code != 0:
            logger.error(f"Git push failed: {stderr}")
            return f"Error: {stderr}"
        
        logger.info(f"Pushed to {branch}")
        return f"✓ Pushed to {branch}"
        
    except Exception as e:
        logger.error(f"Failed to push: {e}")
        raise


@tool
def git_branch(repo_path: str = ".", branch_name: Optional[str] = None) -> str:
    """
    Create and switch to a new branch, or list branches.
    
    Args:
        repo_path: Path to the repository
        branch_name: Name of branch to create and switch to (None to list)
        
    Returns:
        Branch information or confirmation
    """
    try:
        if branch_name:
            # Create and switch to branch
            code, stdout, stderr = _run_git_command(
                ["git", "-C", repo_path, "checkout", "-b", branch_name]
            )
            
            if code != 0:
                return f"Error creating branch: {stderr}"
            
            logger.info(f"Created and switched to branch: {branch_name}")
            return f"✓ Created branch: {branch_name}"
        else:
            # List branches
            code, stdout, stderr = _run_git_command(
                ["git", "-C", repo_path, "branch", "-a"]
            )
            
            if code != 0:
                return f"Error listing branches: {stderr}"
            
            return stdout
            
    except Exception as e:
        logger.error(f"Failed to manage branch: {e}")
        raise


@tool
def git_pull(repo_path: str = ".") -> str:
    """
    Pull latest changes from the remote repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        Pull confirmation message
    """
    try:
        code, stdout, stderr = _run_git_command(
            ["git", "-C", repo_path, "pull"]
        )
        
        if code != 0:
            logger.error(f"Git pull failed: {stderr}")
            return f"Error: {stderr}"
        
        logger.info("Pulled latest changes")
        return f"✓ Pulled latest changes\n{stdout}"
        
    except Exception as e:
        logger.error(f"Failed to pull: {e}")
        raise


def get_skill_info():
    """Return metadata about the repository management skill"""
    return {
        "name": "Repository Management Skill",
        "description": "Git and version control operations",
        "functions": {
            "git_status": "Get repository status",
            "git_commit": "Commit changes",
            "git_push": "Push to remote",
            "git_branch": "Manage branches",
            "git_pull": "Pull from remote",
        },
    }
