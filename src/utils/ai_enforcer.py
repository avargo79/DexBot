"""
AI Command Enforcement Wrapper
Provides wrapper functions that AI assistants should use instead of direct commands.
"""

import subprocess
import sys
from typing import List, Optional, Tuple
from src.utils.ai_validation import CommandValidator
from src.utils.ai_integration import ValidationIntegration, safe_execute_command
from src.config.config_manager import ConfigManager

class AICommandEnforcer:
    """
    Wrapper class that enforces AI validation for all commands.
    AI assistants should use these methods instead of direct command execution.
    """
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.validator = CommandValidator(self.config_manager)
        self.integration = ValidationIntegration()
    
    def execute_git_command(self, git_args: List[str]) -> Tuple[bool, str, str]:
        """
        Execute a git command with mandatory validation.
        
        Args:
            git_args: List of git command arguments (e.g., ['status'], ['push', 'origin', 'main'])
            
        Returns:
            Tuple of (success, stdout, stderr)
            
        Example:
            success, output, error = enforcer.execute_git_command(['status'])
            success, output, error = enforcer.execute_git_command(['push', 'origin', 'feature/test'])
        """
        command = f"git {' '.join(git_args)}"
        
        # MANDATORY validation - no bypass allowed
        is_valid, error_msg, suggestion = self.validator.validate_command(command)
        
        if not is_valid:
            error_output = f"VALIDATION FAILED: {error_msg}"
            if suggestion:
                error_output += f"\nSUGGESTION: {suggestion}"
            return False, "", error_output
        
        # Execute if validation passes
        try:
            result = subprocess.run(
                ['git'] + git_args,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", f"Execution error: {e}"
    
    def execute_invoke_command(self, task_name: str, args: Optional[List[str]] = None) -> Tuple[bool, str, str]:
        """
        Execute an invoke command with validation.
        
        Args:
            task_name: Name of the invoke task
            args: Optional additional arguments
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        args = args or []
        command_parts = ['python', '-m', 'invoke', task_name] + args
        command = ' '.join(command_parts)
        
        # Validate the command pattern
        is_valid, error_msg, suggestion = self.validator.validate_command(command)
        
        if not is_valid:
            error_output = f"VALIDATION FAILED: {error_msg}"
            if suggestion:
                error_output += f"\nSUGGESTION: {suggestion}"
            return False, "", error_output
        
        # Execute if validation passes
        try:
            result = subprocess.run(
                command_parts,
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", f"Execution error: {e}"

# Global enforcer instance for AI assistants to use
AI_ENFORCER = AICommandEnforcer()

# Convenience functions that AI assistants should use
def ai_git(*args) -> Tuple[bool, str, str]:
    """
    MANDATORY wrapper for git commands. AI assistants must use this instead of direct git.
    
    Example:
        success, output, error = ai_git('status')
        success, output, error = ai_git('push', 'origin', 'feature/test')
    """
    return AI_ENFORCER.execute_git_command(list(args))

def ai_invoke(task: str, *args) -> Tuple[bool, str, str]:
    """
    MANDATORY wrapper for invoke commands. AI assistants must use this instead of direct invoke.
    
    Example:
        success, output, error = ai_invoke('test')
        success, output, error = ai_invoke('build')
    """
    return AI_ENFORCER.execute_invoke_command(task, list(args))

def ai_safe_command(command: str) -> Tuple[bool, str, str]:
    """
    MANDATORY wrapper for any command execution. Validates before executing.
    
    Args:
        command: Full command string to execute
        
    Returns:
        Tuple of (success, stdout, stderr)
    """
    return safe_execute_command(command)
