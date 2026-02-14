"""
Logging Skill

Provides logging and audit trail functionality for agent actions.
All agent activities should be logged using this skill.
"""

from langchain.tools import tool
from typing import Optional
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

LOG_FILE = os.getenv("AGENT_LOG_FILE", "logs/agent_log.txt")
LOG_DIR = os.getenv("LOG_DIR", "logs")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)


@tool
def log_action(agent_name: str, action: str, details: Optional[str] = None) -> str:
    """
    Log an agent action to the audit trail.
    
    Args:
        agent_name: Name of the agent performing the action
        action: Description of the action being performed
        details: Optional additional details about the action
        
    Returns:
        Confirmation message with log entry ID
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Format log entry
        if details:
            log_entry = f"[{timestamp}] {agent_name}: {action} - {details}\n"
        else:
            log_entry = f"[{timestamp}] {agent_name}: {action}\n"
        
        # Write to log file
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        
        logger.info(f"Logged action by {agent_name}: {action}")
        return f"✓ Action logged: {action}"
        
    except Exception as e:
        logger.error(f"Failed to log action: {e}")
        raise


@tool
def log_error(agent_name: str, error_message: str, error_type: str = "ERROR") -> str:
    """
    Log an error to the audit trail and error log.
    
    Args:
        agent_name: Name of the agent encountering the error
        error_message: Description of the error
        error_type: Type of error (ERROR, WARNING, CRITICAL)
        
    Returns:
        Confirmation of error logging
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{error_type}] {agent_name}: {error_message}\n"
        
        # Write to log file
        with open(LOG_FILE, "a") as f:
            f.write(log_entry)
        
        logger.error(f"[{error_type}] {agent_name}: {error_message}")
        return f"✓ Error logged: {error_message}"
        
    except Exception as e:
        logger.error(f"Failed to log error: {e}")
        raise


@tool
def read_log(last_lines: int = 10) -> str:
    """
    Read recent entries from the agent log.
    
    Args:
        last_lines: Number of most recent log lines to return
        
    Returns:
        Recent log entries
    """
    try:
        if not os.path.exists(LOG_FILE):
            return "Log file not found"
        
        with open(LOG_FILE, "r") as f:
            all_lines = f.readlines()
        
        # Get last N lines
        recent_lines = all_lines[-last_lines:] if len(all_lines) > last_lines else all_lines
        
        return "".join(recent_lines)
        
    except Exception as e:
        logger.error(f"Failed to read log: {e}")
        raise


@tool
def clear_old_logs(days_to_keep: int = 30) -> str:
    """
    Clean up old log entries (keep only recent logs).
    
    Args:
        days_to_keep: Keep logs from the last N days
        
    Returns:
        Confirmation of cleanup
    """
    try:
        from datetime import datetime, timedelta
        
        if not os.path.exists(LOG_FILE):
            return "No log file to clean"
        
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
        
        # Filter lines newer than cutoff
        new_lines = []
        for line in lines:
            try:
                # Parse timestamp from log entry
                date_str = line[1:20]  # Extract "[YYYY-MM-DD HH:MM:SS]"
                entry_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                if entry_date >= cutoff_date:
                    new_lines.append(line)
            except (ValueError, IndexError):
                # Keep lines that can't be parsed
                new_lines.append(line)
        
        # Write cleaned logs back
        with open(LOG_FILE, "w") as f:
            f.writelines(new_lines)
        
        logger.info(f"Cleaned logs - kept {len(new_lines)} entries")
        return f"✓ Logs cleaned: kept {len(new_lines)} recent entries"
        
    except Exception as e:
        logger.error(f"Failed to clean logs: {e}")
        raise


def get_skill_info():
    """Return metadata about the logging skill"""
    return {
        "name": "Logging Skill",
        "description": "Provides audit logging and activity tracking",
        "functions": {
            "log_action": "Log an agent action",
            "log_error": "Log an error",
            "read_log": "Read recent log entries",
            "clear_old_logs": "Clean up old logs",
        },
    }
