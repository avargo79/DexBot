"""
AI Adaptive Learning Real-Time Validation System

This module provides real-time command validation and error prevention for AI assistants
working on the DexBot project. It enforces workflow rules, validates commands, and 
learns from patterns to prevent common mistakes.

=== AI CONTEXT BLOCK ===
System: AI Validation and Learning
Purpose: Real-time error prevention and workflow enforcement
Dependencies: ConfigManager, Logger, git commands, invoke tasks
Performance: Lightweight validation with minimal overhead
Error Handling: Graceful degradation when validation fails
Integration: Used by development tools and AI assistance workflows
=== END AI CONTEXT ===
"""

import os
import re
import subprocess
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime, timedelta

from src.core.logger import Logger
from src.config.config_manager import ConfigManager


class AIValidationError(Exception):
    """
    Raised when AI validation detects a critical workflow violation.
    
    This exception is used to prevent harmful commands from executing
    and guide the AI toward correct patterns.
    """
    pass


class CommandValidator:
    """
    Real-time command validation system for AI assistants.
    
    Validates commands against known patterns, enforces workflow rules,
    and provides corrective guidance when violations are detected.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the command validator.
        
        Args:
            config_manager: ConfigManager instance for accessing validation rules
            
        Example:
            validator = CommandValidator(config_manager)
            if validator.validate_command("git push origin main"):
                execute_command()
        """
        self.config = config_manager
        self.logger = Logger()
        self.validation_rules = self._load_validation_rules()
        self.learning_data = self._load_learning_data()
        
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules from configuration."""
        return {
            "git_protection": {
                "blocked_commands": [
                    r"git push.*origin main",
                    r"git push.*main",
                    r"git commit.*--amend.*main"
                ],
                "required_workflow": [
                    "git fetch",
                    "git checkout main", 
                    "git pull origin main"
                ]
            },
            "invoke_validation": {
                "preferred_commands": [
                    r"python -m invoke validate",
                    r"python -m invoke test",
                    r"python -m invoke build"
                ],
                "discouraged_patterns": [
                    r"python -c.*import tasks",
                    r"python tasks\.py"
                ]
            },
            "workflow_enforcement": {
                "branch_requirements": {
                    "feature_prefix": ["feature/", "hotfix/", "bugfix/"],
                    "main_protection": True,
                    "pr_required": True
                }
            }
        }
    
    def _load_learning_data(self) -> Dict[str, Any]:
        """Load learning data from previous sessions."""
        return {
            "successful_patterns": [],
            "failed_patterns": [],
            "correction_history": [],
            "pattern_confidence": {}
        }
    
    def validate_command(self, command: str, context: Optional[Dict] = None) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate a command before execution.
        
        Args:
            command: The command string to validate
            context: Optional context information (current branch, file state, etc.)
            
        Returns:
            Tuple of (is_valid, error_message, suggested_correction)
            
        Raises:
            AIValidationError: When a critical workflow violation is detected
            
        Example:
            is_valid, error, correction = validator.validate_command("git push origin main")
            if not is_valid:
                print(f"Error: {error}")
                print(f"Suggestion: {correction}")
        """
        try:
            # Git protection validation
            git_result = self._validate_git_command(command, context)
            if not git_result[0]:
                return git_result
            
            # Invoke command validation
            invoke_result = self._validate_invoke_command(command)
            if not invoke_result[0]:
                return invoke_result
            
            # Workflow validation
            workflow_result = self._validate_workflow_compliance(command, context)
            if not workflow_result[0]:
                return workflow_result
            
            # Record successful pattern
            self._record_successful_pattern(command, context)
            
            return True, None, None
            
        except Exception as e:
            self.logger.error(f"Command validation error: {e}")
            return False, f"Validation error: {e}", None
    
    def _validate_git_command(self, command: str, context: Optional[Dict]) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate git commands against protection rules."""
        if not command.strip().lower().startswith("git"):
            return True, None, None
        
        # Check for direct push to main
        blocked_patterns = self.validation_rules["git_protection"]["blocked_commands"]
        for pattern in blocked_patterns:
            if re.search(pattern, command, re.IGNORECASE):
                error_msg = "CRITICAL: Cannot push directly to main branch"
                suggestion = "Create feature branch: git checkout -b feature/your-feature-name"
                self.logger.warning(f"Blocked command: {command}")
                return False, error_msg, suggestion
        
        # Check for proper workflow sequence
        if "git checkout -b" in command:
            if not self._check_main_is_current(context):
                error_msg = "WARNING: Should fetch/pull main before creating new branch"
                suggestion = "Run: git fetch && git checkout main && git pull origin main"
                return False, error_msg, suggestion
        
        return True, None, None
    
    def _validate_invoke_command(self, command: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate invoke command usage."""
        if "python -c" in command and "import tasks" in command:
            error_msg = "Use invoke tasks instead of direct import"
            suggestion = command.replace("python -c \"import tasks; tasks.", "python -m invoke ").replace("()\"", "")
            return False, error_msg, suggestion
        
        return True, None, None
    
    def _validate_workflow_compliance(self, command: str, context: Optional[Dict]) -> Tuple[bool, Optional[str], Optional[str]]:
        """Validate workflow compliance."""
        # Check if on main branch when trying to commit
        if "git commit" in command:
            current_branch = self._get_current_branch(context)
            if current_branch == "main":
                error_msg = "CRITICAL: Cannot commit directly to main branch"
                suggestion = "Create feature branch first: git checkout -b feature/your-feature-name"
                return False, error_msg, suggestion
        
        return True, None, None
    
    def _check_main_is_current(self, context: Optional[Dict]) -> bool:
        """Check if main branch is up to date."""
        try:
            # Check git status for "Your branch is up to date"
            result = subprocess.run(["git", "status"], capture_output=True, text=True)
            return "up to date" in result.stdout or "up-to-date" in result.stdout
        except Exception:
            return False
    
    def _get_current_branch(self, context: Optional[Dict]) -> str:
        """Get the current git branch."""
        try:
            if context and "current_branch" in context:
                return context["current_branch"]
            
            result = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
            return result.stdout.strip()
        except Exception:
            return "unknown"
    
    def _record_successful_pattern(self, command: str, context: Optional[Dict]):
        """Record a successful command pattern for learning."""
        pattern_data = {
            "command": command,
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
            "success": True
        }
        self.learning_data["successful_patterns"].append(pattern_data)
        
        # Update pattern confidence
        pattern_key = self._extract_pattern_key(command)
        if pattern_key not in self.learning_data["pattern_confidence"]:
            self.learning_data["pattern_confidence"][pattern_key] = 0.5
        else:
            # Increase confidence for successful patterns
            current_confidence = self.learning_data["pattern_confidence"][pattern_key]
            self.learning_data["pattern_confidence"][pattern_key] = min(1.0, current_confidence + 0.1)
    
    def _extract_pattern_key(self, command: str) -> str:
        """Extract a pattern key from a command for learning purposes."""
        # Normalize command to pattern
        if command.startswith("git"):
            return f"git_{command.split()[1]}" if len(command.split()) > 1 else "git_unknown"
        elif "python -m invoke" in command:
            return f"invoke_{command.split()[-1]}" if command.split() else "invoke_unknown"
        else:
            return command.split()[0] if command.split() else "unknown"
    
    def get_suggested_corrections(self, failed_command: str) -> List[str]:
        """
        Get suggested corrections for a failed command.
        
        Args:
            failed_command: The command that failed validation
            
        Returns:
            List of suggested corrections
            
        Example:
            corrections = validator.get_suggested_corrections("git push origin main")
            for correction in corrections:
                print(f"Try: {correction}")
        """
        corrections = []
        
        if "git push" in failed_command and "main" in failed_command:
            corrections.extend([
                "git checkout -b feature/your-feature-name",
                "# Make your changes and commit them",
                "git push origin feature/your-feature-name",
                "# Create PR to merge into main"
            ])
        
        if "python -c" in failed_command and "tasks" in failed_command:
            corrected = failed_command.replace("python -c \"import tasks; tasks.", "python -m invoke ")
            corrected = corrected.replace("()\"", "")
            corrections.append(corrected)
        
        return corrections
    
    def enforce_workflow_rules(self) -> Dict[str, Any]:
        """
        Enforce critical workflow rules and return status.
        
        Returns:
            Dict containing enforcement status and any required actions
            
        Example:
            status = validator.enforce_workflow_rules()
            if not status['compliant']:
                for action in status['required_actions']:
                    print(f"Required: {action}")
        """
        status = {
            "compliant": True,
            "required_actions": [],
            "warnings": [],
            "current_state": {}
        }
        
        try:
            # Check current branch
            current_branch = self._get_current_branch(None)
            status["current_state"]["branch"] = current_branch
            
            # Check if on main when we shouldn't be
            if current_branch == "main":
                # Check for uncommitted changes
                result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
                if result.stdout.strip():
                    status["compliant"] = False
                    status["required_actions"].append("Create feature branch before making changes")
                    status["required_actions"].append("git stash && git checkout -b feature/your-feature-name && git stash pop")
            
            # Check if main is up to date
            if not self._check_main_is_current(None):
                status["warnings"].append("Main branch may not be up to date")
                status["required_actions"].append("git fetch && git checkout main && git pull origin main")
            
        except Exception as e:
            self.logger.error(f"Workflow enforcement error: {e}")
            status["compliant"] = False
            status["required_actions"].append(f"Fix workflow enforcement error: {e}")
        
        return status


class LearningEngine:
    """
    Adaptive learning engine for improving AI validation over time.
    
    Learns from successful patterns, failed attempts, and user corrections
    to continuously improve validation accuracy and suggestions.
    """
    
    def __init__(self, config_manager: ConfigManager):
        """
        Initialize the learning engine.
        
        Args:
            config_manager: ConfigManager instance for learning configuration
        """
        self.config = config_manager
        self.logger = Logger()
        self.pattern_database = {}
        self.confidence_scores = {}
        
    def learn_from_success(self, command: str, context: Dict, outcome: str):
        """
        Learn from successful command execution.
        
        Args:
            command: The successful command
            context: Context when command was executed
            outcome: Description of successful outcome
        """
        pattern_key = self._extract_learning_pattern(command)
        
        if pattern_key not in self.pattern_database:
            self.pattern_database[pattern_key] = {
                "successful_instances": [],
                "failed_instances": [],
                "confidence": 0.5
            }
        
        self.pattern_database[pattern_key]["successful_instances"].append({
            "command": command,
            "context": context,
            "outcome": outcome,
            "timestamp": datetime.now().isoformat()
        })
        
        # Increase confidence
        current_confidence = self.pattern_database[pattern_key]["confidence"]
        self.pattern_database[pattern_key]["confidence"] = min(1.0, current_confidence + 0.05)
        
        self.logger.debug(f"Learned successful pattern: {pattern_key}")
    
    def learn_from_failure(self, command: str, context: Dict, error: str, correction: str):
        """
        Learn from failed command attempts.
        
        Args:
            command: The failed command
            context: Context when command failed
            error: Error message or description
            correction: Successful correction that was applied
        """
        pattern_key = self._extract_learning_pattern(command)
        
        if pattern_key not in self.pattern_database:
            self.pattern_database[pattern_key] = {
                "successful_instances": [],
                "failed_instances": [],
                "confidence": 0.5
            }
        
        self.pattern_database[pattern_key]["failed_instances"].append({
            "command": command,
            "context": context,
            "error": error,
            "correction": correction,
            "timestamp": datetime.now().isoformat()
        })
        
        # Decrease confidence for failed patterns
        current_confidence = self.pattern_database[pattern_key]["confidence"]
        self.pattern_database[pattern_key]["confidence"] = max(0.0, current_confidence - 0.1)
        
        self.logger.debug(f"Learned failed pattern: {pattern_key}")
    
    def _extract_learning_pattern(self, command: str) -> str:
        """Extract a learning pattern key from a command."""
        # Create a pattern that captures the intent but abstracts specifics
        command_parts = command.split()
        if len(command_parts) == 0:
            return "empty_command"
        
        base_command = command_parts[0]
        
        if base_command == "git":
            if len(command_parts) > 1:
                git_action = command_parts[1]
                if git_action in ["push", "pull", "checkout", "commit", "add"]:
                    return f"git_{git_action}"
        elif base_command == "python":
            if "-m" in command_parts:
                return "python_module"
            elif "-c" in command_parts:
                return "python_script"
        
        return base_command
    
    def get_confidence_score(self, command: str) -> float:
        """
        Get confidence score for a command pattern.
        
        Args:
            command: Command to check confidence for
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        pattern_key = self._extract_learning_pattern(command)
        if pattern_key in self.pattern_database:
            return self.pattern_database[pattern_key]["confidence"]
        return 0.5  # Default neutral confidence
    
    def suggest_alternatives(self, failed_command: str) -> List[str]:
        """
        Suggest alternative commands based on learning data.
        
        Args:
            failed_command: Command that failed validation
            
        Returns:
            List of suggested alternative commands
        """
        suggestions = []
        pattern_key = self._extract_learning_pattern(failed_command)
        
        if pattern_key in self.pattern_database:
            # Look for successful instances of similar patterns
            successful_instances = self.pattern_database[pattern_key]["successful_instances"]
            for instance in successful_instances[-3:]:  # Last 3 successful instances
                if instance["command"] != failed_command:
                    suggestions.append(instance["command"])
        
        return suggestions
