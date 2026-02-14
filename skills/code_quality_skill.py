"""
Code Quality Skill

Provides code style checking and formatting capabilities
using Black and Flake8.
"""

from langchain.tools import tool
from typing import Optional, List
import logging
import subprocess
import os

logger = logging.getLogger(__name__)


def _run_command(command: List[str]) -> tuple[int, str, str]:
    """
    Run a shell command and return exit code, stdout, stderr.
    
    Args:
        command: Command as list of strings
        
    Returns:
        Tuple of (exit_code, stdout, stderr)
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return 1, "", "Command timed out"
    except Exception as e:
        return 1, "", str(e)


@tool
def run_black_format(file_paths: str = ".") -> str:
    """
    Format Python code with Black formatter.
    
    Args:
        file_paths: File or directory paths to format (space-separated)
        
    Returns:
        Formatting result message
    """
    try:
        paths = file_paths.split()
        command = ["black"] + paths + ["--line-length=100"]
        
        code, stdout, stderr = _run_command(command)
        
        if code != 0:
            logger.error(f"Black formatting failed: {stderr}")
            return f"Black error: {stderr}"
        
        logger.info(f"Formatted code with Black: {file_paths}")
        return f"✓ Code formatted\n{stdout}"
        
    except Exception as e:
        logger.error(f"Failed to run Black: {e}")
        raise


@tool
def run_flake8_lint(file_paths: str = "src/ agents/ skills/") -> str:
    """
    Check Python code style with Flake8.
    
    Args:
        file_paths: File or directory paths to lint (space-separated)
        
    Returns:
        Lint report
    """
    try:
        paths = file_paths.split()
        command = ["flake8"] + paths + ["--max-line-length=100", "--count"]
        
        code, stdout, stderr = _run_command(command)
        
        # Flake8 returns 1 if issues found, but that's not a run error
        if code not in [0, 1]:
            logger.error(f"Flake8 failed: {stderr}")
            return f"Flake8 error: {stderr}"
        
        logger.info(f"Ran Flake8 lint: {file_paths}")
        
        if not stdout:
            return "✓ No linting issues found!"
        else:
            return f"Linting issues found:\n{stdout}"
        
    except Exception as e:
        logger.error(f"Failed to run Flake8: {e}")
        raise


@tool
def run_isort(file_paths: str = ".") -> str:
    """
    Sort and organize Python imports with isort.
    
    Args:
        file_paths: File or directory paths to organize (space-separated)
        
    Returns:
        Organization result message
    """
    try:
        paths = file_paths.split()
        command = ["isort"] + paths + ["--profile=black"]
        
        code, stdout, stderr = _run_command(command)
        
        if code != 0:
            logger.error(f"isort failed: {stderr}")
            return f"isort error: {stderr}"
        
        logger.info(f"Organized imports: {file_paths}")
        return f"✓ Imports organized\n{stdout if stdout else 'No changes needed'}"
        
    except Exception as e:
        logger.error(f"Failed to run isort: {e}")
        raise


@tool
def run_mypy_typecheck(file_paths: str = ".") -> str:
    """
    Check Python type annotations with mypy.
    
    Args:
        file_paths: File or directory paths to check (space-separated)
        
    Returns:
        Type checking report
    """
    try:
        paths = file_paths.split()
        command = ["mypy"] + paths + ["--ignore-missing-imports"]
        
        code, stdout, stderr = _run_command(command)
        
        logger.info(f"Ran mypy type check: {file_paths}")
        
        if not stdout:
            return "✓ No type errors found!"
        else:
            return f"Type checking issues:\n{stdout}"
        
    except Exception as e:
        logger.error(f"Failed to run mypy: {e}")
        raise


@tool
def run_all_checks(file_paths: str = ".") -> str:
    """
    Run all code quality checks (Black, Flake8, isort).
    
    Args:
        file_paths: File or directory paths to check
        
    Returns:
        Complete quality report
    """
    try:
        results = {}
        
        # Run Black
        results["black"] = run_black_format(file_paths)
        
        # Run isort
        results["isort"] = run_isort(file_paths)
        
        # Run Flake8
        results["flake8"] = run_flake8_lint(file_paths)
        
        # Generate report
        report = "=== Code Quality Check Report ===\n"
        for tool_name, result in results.items():
            report += f"\n[{tool_name.upper()}]\n{result}\n"
        
        logger.info("Completed all code quality checks")
        return report
        
    except Exception as e:
        logger.error(f"Failed to run quality checks: {e}")
        raise


def get_skill_info():
    """Return metadata about the code quality skill"""
    return {
        "name": "Code Quality Skill",
        "description": "Code formatting and linting checks",
        "functions": {
            "run_black_format": "Format code with Black",
            "run_flake8_lint": "Lint code with Flake8",
            "run_isort": "Organize imports with isort",
            "run_mypy_typecheck": "Check types with mypy",
            "run_all_checks": "Run all checks",
        },
    }
