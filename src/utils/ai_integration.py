"""
AI Validation Integration Wrapper

Provides easy integration points for the AI validation system with development tools,
invoke tasks, and command line interfaces.

=== AI CONTEXT BLOCK ===
System: AI Validation Integration
Purpose: Easy integration wrapper for validation system
Dependencies: ai_validation.py, ConfigManager, subprocess
Performance: Lightweight wrapper with validation caching
Error Handling: Graceful fallback when validation unavailable
Integration: Used by invoke tasks, development scripts, AI assistants
=== END AI CONTEXT ===
"""

import os
import sys
import subprocess
from typing import Dict, List, Optional, Any
from functools import wraps

from src.core.logger import Logger
from src.config.config_manager import ConfigManager
from src.utils.ai_validation import CommandValidator, LearningEngine, AIValidationError


class ValidationIntegration:
    """
    Integration wrapper for AI validation system.
    
    Provides simple interfaces for common validation scenarios and integrates
    with existing development workflows.
    """
    
    def __init__(self):
        """Initialize the validation integration."""
        self.logger = Logger()
        self._validator = None
        self._learning_engine = None
        self._enabled = True
        
        try:
            config_manager = ConfigManager()
            self._validator = CommandValidator(config_manager)
            self._learning_engine = LearningEngine(config_manager)
        except Exception as e:
            self.logger.warning(f"AI validation not available: {e}")
            self._enabled = False
    
    def validate_command_safe(self, command: str, context: Optional[Dict] = None) -> bool:
        """
        Safely validate a command with fallback.
        
        Args:
            command: Command to validate
            context: Optional context information
            
        Returns:
            True if command is safe to execute, False otherwise
            
        Example:
            integration = ValidationIntegration()
            if integration.validate_command_safe("git push origin main"):
                execute_command()
        """
        if not self._enabled or not self._validator:
            return True  # Fail open if validation unavailable
        
        try:
            is_valid, error, suggestion = self._validator.validate_command(command, context)
            if not is_valid:
                self.logger.warning(f"Command validation failed: {command}")
                self.logger.warning(f"Error: {error}")
                if suggestion:
                    self.logger.info(f"Suggestion: {suggestion}")
            return is_valid
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return True  # Fail open on validation errors
    
    def enforce_workflow_check(self) -> Dict[str, Any]:
        """
        Perform workflow compliance check.
        
        Returns:
            Dictionary with compliance status and required actions
        """
        if not self._enabled or not self._validator:
            return {"compliant": True, "required_actions": [], "warnings": []}
        
        try:
            return self._validator.enforce_workflow_rules()
        except Exception as e:
            self.logger.error(f"Workflow check error: {e}")
            return {"compliant": False, "required_actions": [f"Fix validation error: {e}"]}
    
    def get_validation_suggestions(self, command: str) -> List[str]:
        """
        Get validation suggestions for a command.
        
        Args:
            command: Command to get suggestions for
            
        Returns:
            List of suggestions
        """
        if not self._enabled or not self._validator:
            return []
        
        try:
            return self._validator.get_suggested_corrections(command)
        except Exception as e:
            self.logger.error(f"Suggestion error: {e}")
            return []


def validate_command(command: str, context: Optional[Dict] = None):
    """
    Decorator for command validation.
    
    Args:
        command: Command pattern to validate
        context: Optional context for validation
        
    Example:
        @validate_command("git push origin {branch}")
        def push_to_branch(branch):
            subprocess.run(["git", "push", "origin", branch])
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            integration = ValidationIntegration()
            
            # Build actual command from pattern
            actual_command = command
            if "{" in command:
                # Simple parameter substitution
                for i, arg in enumerate(args):
                    actual_command = actual_command.replace(f"{{{i}}}", str(arg))
                for key, value in kwargs.items():
                    actual_command = actual_command.replace(f"{{{key}}}", str(value))
            
            if not integration.validate_command_safe(actual_command, context):
                suggestions = integration.get_validation_suggestions(actual_command)
                error_msg = f"Command validation failed: {actual_command}"
                if suggestions:
                    error_msg += f"\nSuggestions: {', '.join(suggestions)}"
                raise AIValidationError(error_msg)
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_workflow_compliance():
    """
    Check workflow compliance and print results.
    
    This function can be called from invoke tasks or development scripts
    to ensure proper workflow compliance.
    
    Example:
        # In invoke task
        from src.utils.ai_integration import check_workflow_compliance
        check_workflow_compliance()
    """
    integration = ValidationIntegration()
    status = integration.enforce_workflow_check()
    
    if status["compliant"]:
        print("✅ Workflow compliance: PASSED")
    else:
        print("❌ Workflow compliance: FAILED")
        
    if status["required_actions"]:
        print("\nRequired Actions:")
        for action in status["required_actions"]:
            print(f"  • {action}")
    
    if status["warnings"]:
        print("\nWarnings:")
        for warning in status["warnings"]:
            print(f"  ⚠️  {warning}")
    
    return status["compliant"]


def validate_git_operation(operation: str, target: str = "") -> bool:
    """
    Validate git operations before execution.
    
    Args:
        operation: Git operation (push, commit, checkout, etc.)
        target: Target branch or remote
        
    Returns:
        True if operation is safe, False otherwise
        
    Example:
        if validate_git_operation("push", "origin main"):
            # Safe to push
            subprocess.run(["git", "push", "origin", "main"])
    """
    integration = ValidationIntegration()
    command = f"git {operation}"
    if target:
        command += f" {target}"
    
    return integration.validate_command_safe(command, {
        "operation": operation,
        "target": target,
        "timestamp": None
    })


def safe_execute_command(command: List[str], check_validation: bool = True) -> subprocess.CompletedProcess:
    """
    Safely execute a command with optional validation.
    
    Args:
        command: Command as list of strings
        check_validation: Whether to perform validation check
        
    Returns:
        CompletedProcess result
        
    Raises:
        AIValidationError: If validation fails
        
    Example:
        result = safe_execute_command(["git", "status"])
        result = safe_execute_command(["git", "push", "origin", "main"])  # Will validate
    """
    command_str = " ".join(command)
    
    if check_validation:
        integration = ValidationIntegration()
        if not integration.validate_command_safe(command_str):
            suggestions = integration.get_validation_suggestions(command_str)
            error_msg = f"Command validation failed: {command_str}"
            if suggestions:
                error_msg += f"\nSuggestions:\n" + "\n".join(f"  • {s}" for s in suggestions)
            raise AIValidationError(error_msg)
    
    return subprocess.run(command, capture_output=True, text=True)


# Integration functions for invoke tasks
def validate_invoke_context():
    """
    Validate the current invoke context for compliance.
    
    This should be called at the beginning of critical invoke tasks
    to ensure proper development environment setup.
    
    Returns:
        True if context is valid, False otherwise
    """
    integration = ValidationIntegration()
    status = integration.enforce_workflow_check()
    
    # Print status for invoke task output
    if not status["compliant"]:
        print("⚠️  Workflow compliance issues detected:")
        for action in status["required_actions"]:
            print(f"   • {action}")
        return False
    
    if status["warnings"]:
        print("⚠️  Workflow warnings:")
        for warning in status["warnings"]:
            print(f"   • {warning}")
    
    return True


def learn_from_invoke_success(task_name: str, command: str, outcome: str):
    """
    Record successful invoke task execution for learning.
    
    Args:
        task_name: Name of the invoke task
        command: Command that was executed
        outcome: Description of successful outcome
    """
    integration = ValidationIntegration()
    if integration._enabled and integration._learning_engine:
        context = {
            "task_name": task_name,
            "execution_context": "invoke_task",
            "timestamp": None
        }
        integration._learning_engine.learn_from_success(command, context, outcome)


def learn_from_invoke_failure(task_name: str, command: str, error: str, correction: str = ""):
    """
    Record failed invoke task execution for learning.
    
    Args:
        task_name: Name of the invoke task
        command: Command that failed
        error: Error message
        correction: Correction that should be applied
    """
    integration = ValidationIntegration()
    if integration._enabled and integration._learning_engine:
        context = {
            "task_name": task_name,
            "execution_context": "invoke_task",
            "timestamp": None
        }
        integration._learning_engine.learn_from_failure(command, context, error, correction)


# Command-line interface for validation
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ai_integration.py <command>")
        print("       python ai_integration.py --check-workflow")
        sys.exit(1)
    
    if sys.argv[1] == "--check-workflow":
        compliant = check_workflow_compliance()
        sys.exit(0 if compliant else 1)
    else:
        command = " ".join(sys.argv[1:])
        integration = ValidationIntegration()
        
        if integration.validate_command_safe(command):
            print(f"✅ Command validated: {command}")
            sys.exit(0)
        else:
            print(f"❌ Command validation failed: {command}")
            suggestions = integration.get_validation_suggestions(command)
            if suggestions:
                print("Suggestions:")
                for suggestion in suggestions:
                    print(f"  • {suggestion}")
            sys.exit(1)
