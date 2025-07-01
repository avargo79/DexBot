# GitHub Copilot Instructions for DexBot

This file provides context and guidelines for GitHub Copilot when working on the DexBot modular bot system for Ultima Online with RazorEnhanced.

## Project Overview

**DexBot** is a high-performance, modular bot system for Ultima Online that uses the RazorEnhanced scripting environment. The project emphasizes clean architecture, comprehensive testing, and production-ready code quality.

### Key Characteristics
- **Target Environment**: RazorEnhanced Python scripting for Ultima Online
- **Architecture**: Modular system with clear separation of concerns
- **Code Quality**: 100+ line length, comprehensive documentation, extensive testing
- **Performance Focus**: Optimized for long-running bot sessions (12+ hours)
- **Production Ready**: All systems are battle-tested with performance metrics

## Architecture & Patterns

### Directory Structure
```
src/
├── config/         # Configuration management
├── core/           # Core bot logic and state management
├── systems/        # Main bot systems (auto_heal, combat, looting)
├── ui/             # GUMP interfaces and user interaction
└── utils/          # Utilities and helper functions

docs/
├── backlog/        # Product backlog and prioritized features
└── prds/           # Product Requirements Documents (detailed specs)

tests/              # Comprehensive test suite
config/             # Default configuration files
ref/                # API references and item databases
```

### Core Systems (Production Ready)
1. **Auto Heal System** (`src/systems/auto_heal.py`) - Intelligent healing with potions/bandages
2. **Combat System** (`src/systems/combat.py`) - High-performance target detection and engagement
3. **Looting System** (`src/systems/looting.py`) - Advanced corpse looting with ignore list optimization

## Coding Standards & Conventions

### Python Style Guidelines
Following [PEP 8](https://peps.python.org/pep-0008/) and modern Python best practices:

#### Code Quality Characteristics
- **Functionality**: Code works as expected and fulfills its intended purpose
- **Readability**: Easy for humans to understand with descriptive names
- **Documentation**: Clearly explains purpose and usage with comprehensive docstrings
- **Standards Compliance**: Adheres to PEP 8 and project conventions
- **Reusability**: Can be used in different contexts without modification
- **Maintainability**: Allows modifications without introducing bugs
- **Robustness**: Handles errors and unexpected inputs effectively
- **Testability**: Can be easily verified for correctness
- **Efficiency**: Optimizes time and resource usage
- **Scalability**: Handles increased loads without degradation
- **Security**: Protects against vulnerabilities and malicious inputs

#### Style Standards
- **Line Length**: 100 characters (configured in pyproject.toml)
- **Indentation**: 4 spaces (never tabs)
- **Naming Conventions**:
  - `snake_case` for functions, variables, and modules
  - `PascalCase` for classes and type variables
  - `UPPER_CASE` for constants
  - `_private_method` for internal use (single underscore)
  - `__dunder_method__` for special methods only
- **String Quotes**: Prefer double quotes `"string"` for consistency
- **Import Organization**:
  1. Standard library imports
  2. Third-party imports  
  3. Local application imports
  4. Separate groups with blank lines

#### Code Formatting Tools
- **Black**: Automated code formatting (`black --line-length 100`)
- **isort**: Import statement organization
- **Flake8/Ruff**: Linting and style checking
- **mypy**: Static type checking when type hints are used

#### Documentation Standards
```python
from typing import Any, Dict

def complex_method(self, param: str) -> Dict[str, Any]:
    """
    Brief description of what the method does.
    
    Args:
        param: Description of parameter and expected values
        
    Returns:
        Dict containing result data with keys: 'status', 'data', 'message'
        
    Raises:
        SpecificError: When specific condition occurs
        
    Example:
        result = self.complex_method("test_value")
        if result['status'] == 'success':
            process_data(result['data'])
    """
```

#### Error Handling Best Practices
```python
from typing import List, Optional
from ..core.logger import Logger

# Specific exception handling
try:
    result = risky_operation()
except SpecificError as e:
    Logger.error(f"Operation failed: {e}")
    return default_value
except Exception as e:
    Logger.error(f"Unexpected error: {e}")
    raise

# Input validation
def process_data(data: Optional[List[str]]) -> bool:
    if not data:
        raise ValueError("Data cannot be empty")
    
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    
    return True
```

### Type Hints and Static Analysis
```python
# Use type hints for better code clarity
from typing import Any, Dict, List, Optional, Union

def analyze_data(
    items: List[Dict[str, Any]], 
    threshold: float = 0.5
) -> Optional[Dict[str, Union[int, float]]]:
    """Analyze data with proper type annotations."""
    if not items:
        return None
    
    return {
        'count': len(items),
        'average': sum(item['value'] for item in items) / len(items)
    }
```

### Code Review Checklist
- [ ] **Functionality**: Does the code work as intended?
- [ ] **Readability**: Are names descriptive and code structure clear?
- [ ] **Testing**: Are there sufficient tests with good coverage?
- [ ] **Error Handling**: Are edge cases and errors handled properly?
- [ ] **Performance**: Is the code efficient for its use case?
- [ ] **Security**: Are there any security vulnerabilities?
- [ ] **Documentation**: Are docstrings and comments adequate?
- [ ] **Style Compliance**: Does code follow PEP 8 and project standards?

### Security Best Practices
- **Input Validation**: Always validate and sanitize external inputs
- **Avoid Dangerous Functions**: Don't use `eval()`, `exec()`, or `pickle.load()` on untrusted data
- **Secrets Management**: Never hardcode passwords, API keys, or sensitive data
- **SQL Injection Prevention**: Use parameterized queries
- **Path Traversal Prevention**: Validate file paths and use secure file operations

### RazorEnhanced API Usage
```python
# Standard RazorEnhanced imports pattern
from System.Collections.Generic import List
from System import Int32 as int

# Common RazorEnhanced APIs used in this project:
# - Player: Player.Name, Player.Hits, Player.HitsMax, Player.Mount, Player.Buffs
# - Items: Items.FindBySerial, Items.GetPropValue, Items.Filter
# - Mobiles: Mobiles.FindBySerial, Mobiles.Filter, Mobiles.Select
# - Misc: Misc.Pause, Misc.SendMessage, Misc.IgnoreObject, Misc.ClearIgnore
# - Journal: Journal.Search, Journal.Clear
# - Gumps: Gumps.SendAction, Gumps.CloseGump
# - Target: Target.SetLast, Target.Last
```

### Development Workflow Best Practices

#### Git and Version Control Standards
- **Commit Early and Often**: Make frequent, small commits with clear, descriptive messages
- **Never Commit Broken Builds**: Always validate code compiles and core tests pass before committing
  - Use `python -m invoke validate` to check system integrity before committing
  - Run `python -m invoke test` to ensure test suite passes
  - Use `python -m invoke build` to verify bundled output builds successfully
- **Atomic Commits**: Each commit should represent one logical change or feature
- **Descriptive Commit Messages**: Use conventional commit format when possible
  ```
  feat: add new looting system optimization
  fix: resolve bandage count display issue in GUMP
  docs: update development workflow guidelines
  test: add integration tests for UO Items database
  ```

#### Preferred Development Workflow Commands
Always use the unified invoke task system for development operations:

```bash
# Validation and Testing (use before committing)
python -m invoke validate    # Check system integrity and function presence
python -m invoke test       # Run comprehensive test suite
python -m invoke build      # Build and validate bundled DexBot.py

# Development Operations
python -m invoke status     # Check git status and workspace health
python -m invoke quick      # Fast build+test cycle for iterative development
python -m invoke watch      # Monitor file changes during development

# Information and Help
python -m invoke version    # Display version and build information
python -m invoke help       # Show all available tasks with descriptions
python -m invoke --list     # List all available invoke tasks
```

#### Pre-Commit Validation Checklist
Before any git commit, ensure:
- [ ] `python -m invoke validate` passes (checks for missing functions, proper imports)
- [ ] `python -m invoke test` shows high pass rates (96%+ expected)
- [ ] `python -m invoke build` completes successfully
- [ ] No syntax errors or import issues in modified files
- [ ] Version information is current in `version.txt` if version changed
- [ ] All new code follows project coding standards and includes proper documentation

#### Continuous Integration Mindset
- **Build Validation**: Every change should maintain build integrity
- **Test Coverage**: New features require corresponding tests using the 3-case pattern
- **Performance Awareness**: Consider long-running session impact (12+ hours)
- **Documentation Updates**: Keep docs current with code changes
- **Backward Compatibility**: Ensure config file migrations work properly

#### Emergency Procedures
If a broken commit is discovered:
1. **Immediate**: Use `git revert <commit-hash>` rather than force-push if already shared
2. **Assessment**: Run `python -m invoke validate` and `python -m invoke test` to identify issues
3. **Fix Forward**: Create fix commits rather than amending shared history
4. **Validation**: Ensure `python -m invoke build` produces working bundled output

### AI-Assisted Development Guidelines

#### Context Awareness for AI
When working with AI tools, always provide this essential context:

**Project Type**: RazorEnhanced Python bot for Ultima Online
**Python Version**: 3.x with .NET Framework integration via IronPython
**Unique Constraints**: 
- All code runs in RazorEnhanced scripting environment
- Uses .NET APIs through Python bindings
- Single-threaded execution model preferred
- Memory management crucial for long-running sessions
- No standard Python package imports (requests, pandas, etc.)

#### Required Context for Each AI Interaction
```python
"""
CONTEXT FOR AI:
- File Purpose: [Brief description of what this file does]
- System Integration: [Which systems this connects to - auto_heal, combat, looting, ui]
- Key Dependencies: [List main imports and dependencies]
- Performance Constraints: [Any specific performance requirements]
- Error Handling: [Expected error scenarios and handling patterns]
"""
```

#### AI Prompt Templates for Common Tasks

**For New System Development:**
```
Create a new [system_name] for DexBot that:
- Follows the existing architecture pattern (see src/systems/ examples)
- Uses ConfigManager for configuration (see src/config/config_manager.py)
- Implements proper logging with Logger from src/core/logger.py
- Includes comprehensive error handling
- Has 3-case testing pattern (pass/fail/edge)
- Optimizes for 12+ hour runtime sessions
- Uses RazorEnhanced APIs: [list specific APIs needed]
```

**For Bug Fixes:**
```
Fix this issue in DexBot:
- Current behavior: [describe what's happening]
- Expected behavior: [describe what should happen]
- System affected: [auto_heal/combat/looting/ui/core]
- Error logs: [paste any relevant error messages]
- Performance impact: [any performance considerations]
- Test scenario: [how to reproduce and verify fix]
```

**For Performance Optimization:**
```
Optimize this DexBot code for:
- Target: [specific performance metric - memory, speed, API calls]
- Current issue: [describe performance problem]
- Constraints: [RazorEnhanced limitations, memory limits, etc.]
- Measurement: [how performance is currently measured]
- Expected improvement: [specific goals - "reduce API calls by 50%"]
```

#### Code Generation Preferences
- **Always include docstrings** with Args, Returns, Raises, and Example sections
- **Prefer explicit over implicit** - be verbose for clarity
- **Include type hints** when beneficial for understanding
- **Add inline comments** for complex RazorEnhanced API usage
- **Consider edge cases** - null checks, empty collections, API failures
- **Plan for extensibility** - use patterns that can be easily modified
- **Create temporary files in `tmp/`** - keep workspace organized by using the tmp directory for all temporary files
- **Clean up `tmp/` directory** - remove temporary files when wrapping up work sessions

#### Workspace Management Guidelines
- **Temporary Files**: Always create temporary files in `tmp/` directory
- **File Naming**: Use descriptive names with context: `TASK_NAME_COMPLETION.md`, `FEATURE_ANALYSIS.md`
- **Preserve Important Files**: Never delete `.gitkeep`, configuration files, or active project files
- **Cleanup Rules**:
  - Remove old temporary analysis files (`.md` files older than current session)
  - Remove temporary directories created for testing/extraction
  - Keep `.gitkeep` file to maintain git tracking
  - Keep final summary documents for reference
- **Session Management**: At end of work session, clean up temporary files but preserve final deliverables

#### Testing-First Approach for AI
When generating new code, AI should:
1. **Generate test cases first** using the 3-case pattern
2. **Include mock setup** for RazorEnhanced APIs
3. **Provide test data examples** with realistic UO item IDs and values
4. **Consider integration scenarios** - how systems interact
5. **Include performance test suggestions** for long-running operations

#### AI-Friendly Naming Conventions
```python
# Use descriptive, searchable names that indicate purpose and context
class LootingSystemItemEvaluator:  # Not: ItemEval
    def evaluate_corpse_item_for_looting_decision(self, item):  # Not: eval_item
        """
        Evaluate whether a corpse item should be looted based on configuration.
        
        This method is called for each item found on a corpse and determines
        whether the item meets the criteria for being taken into inventory.
        """
        pass

# Include context in variable names
def process_combat_target_selection(self):
    available_combat_targets = self._find_hostile_mobiles()  # Not: targets
    closest_valid_combat_target = self._select_closest_target(available_combat_targets)
    current_combat_engagement_distance = self._calculate_distance(closest_valid_combat_target)
```

#### AI Context Documentation Pattern
```python
"""
=== AI CONTEXT BLOCK ===
System: Combat Target Selection
Purpose: Find and prioritize hostile targets for engagement
Dependencies: Mobiles API, distance calculations, combat configuration
Performance: Critical path - called every 100ms during combat
Error Handling: Must gracefully handle target disappearing, out of range
Integration: Used by CombatSystem.update_combat_state()
Last Modified: 2025-07-01 - Added priority scoring
=== END AI CONTEXT ===
"""

def select_optimal_combat_target(self, available_targets: List[Mobile]) -> Optional[Mobile]:
    """Select the best target based on distance, health, and threat level."""
    pass
```

#### Comprehensive Error Documentation
```python
class DexBotSystemError(Exception):
    """
    Base exception for DexBot system errors.
    
    AI Usage: Catch this for any DexBot-specific error handling.
    All DexBot exceptions inherit from this for consistent error handling.
    """
    pass

class RazorEnhancedAPIError(DexBotSystemError):
    """
    Raised when RazorEnhanced API calls fail.
    
    Common Causes:
    - API not available (Player not logged in)
    - Invalid parameters passed to API
    - Timing issues (API called too frequently)
    
    AI Usage: Wrap all RazorEnhanced API calls in try/except for this.
    """
    pass
```

## Key Development Workflow Reminders

Always include comprehensive docstrings with Args, Returns, Raises, and Example sections for DexBot code.
Use RazorEnhanced-specific imports: 'from System.Collections.Generic import List' and 'from System import Int32 as int'.
Wrap all RazorEnhanced API calls in try/except blocks with proper logging using Logger from src/core/logger.py.
Follow the 3-case testing pattern: pass/fail/edge cases for all new functionality.
Always create temporary files in the tmp/ directory to keep the workspace organized.
Clean up the tmp/ directory when wrapping up work sessions to maintain a tidy workspace.

**CRITICAL WORKFLOW PRACTICES:**
- **Never commit broken builds** - Always run `python -m invoke validate` and `python -m invoke test` before committing
- **Use invoke tasks** - Prefer `python -m invoke <task>` over direct commands for consistency and validation
- **Commit frequently** - Make small, atomic commits with descriptive messages using conventional commit format
- **Validate before commit** - Ensure build succeeds, tests pass (96%+ expected), and no syntax errors exist
