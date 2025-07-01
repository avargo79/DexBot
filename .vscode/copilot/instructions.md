---
applyTo: "**/*.py"
---
# DexBot - RazorEnhanced Python Bot Development Rules

You are working on DexBot, a high-performance modular bot system for Ultima Online using RazorEnhanced Python scripting environment.

## CRITICAL CONSTRAINTS
- **Runtime**: RazorEnhanced Python with .NET Framework integration (IronPython)
- **Threading**: Single-threaded execution model preferred
- **Memory**: Long-running sessions (12+ hours) require careful memory management
- **APIs**: Only RazorEnhanced APIs available (no requests, pandas, etc.)
- **Performance**: Optimize for minimal API calls and efficient resource usage

## ARCHITECTURE REQUIREMENTS
- Follow existing modular patterns in `src/systems/`
- Use ConfigManager for all configuration (`src/config/config_manager.py`)
- Use Logger from `src/core/logger.py` for all logging
- Implement 3-case testing pattern (pass/fail/edge)
- Include comprehensive error handling with specific exceptions

## CODE GENERATION REQUIREMENTS

### Always Include
1. **Comprehensive docstrings** with Args, Returns, Raises, Example sections
2. **Type hints** for better code clarity and IDE support
3. **Error handling** with specific exception types
4. **Logging statements** for debugging and monitoring
5. **Input validation** for all public methods
6. **Performance considerations** for long-running operations
7. **Temporary files in `tmp/` directory** for workspace organization
8. **Cleanup `tmp/` directory** when wrapping up work sessions

### RazorEnhanced API Patterns
```python
# Standard imports
from System.Collections.Generic import List
from System import Int32 as int
from ..core.logger import Logger

# Safe API call wrapper
def safe_api_call(self, operation: str, api_func, *args, **kwargs):
    try:
        result = api_func(*args, **kwargs)
        Logger.debug(f"{operation} successful")
        return result
    except Exception as e:
        Logger.error(f"{operation} failed: {e}")
        return None
```

### Configuration Pattern
```python
def __init__(self):
    self.config_manager = ConfigManager()
    self.config = self.config_manager.get_system_config('system_name')
    self._validate_config()
```

### Testing Pattern
```python
class TestSystemName:
    def test_method_pass_case(self):
        # Test with valid input and expected behavior
        pass
    
    def test_method_fail_case(self):
        # Test with invalid input and proper error handling
        with pytest.raises(SpecificError):
            pass
    
    def test_method_edge_case(self):
        # Test boundary conditions
        pass
```

## NAMING CONVENTIONS
- Use descriptive, searchable names that indicate purpose and context
- Classes: `LootingSystemItemEvaluator` not `ItemEval`
- Methods: `evaluate_corpse_item_for_looting_decision` not `eval_item`
- Variables: `available_combat_targets` not `targets`

## ERROR HANDLING REQUIREMENTS
- Catch specific exceptions, never bare `except:`
- Always log errors with context
- Provide graceful fallbacks where possible
- Use project-specific exception hierarchy

## PERFORMANCE REQUIREMENTS
- Cache expensive operations
- Use RazorEnhanced ignore lists for processed items
- Implement periodic cleanup to prevent memory buildup
- Minimize API calls through batching and caching

## INTEGRATION POINTS
- Auto Heal System: Resource management, timing, state tracking
- Combat System: Target detection, engagement logic, performance
- Looting System: Corpse processing, item evaluation, ignore lists
- UI/GUMP Systems: User interaction, real-time updates, state management

## ANTI-PATTERNS TO AVOID
- Magic numbers (use named constants)
- Long functions (break into smaller, focused methods)
- Deep nesting (use early returns and guard clauses)
- Mutable defaults in function parameters
- Generic error handling without context
- Premature optimization without profiling

## WORKSPACE MANAGEMENT
- Always create temporary files in the `tmp/` directory
- Use descriptive names: `TASK_NAME_COMPLETION.md`, `ANALYSIS_RESULTS.md`
- Clean up `tmp/` directory when wrapping up work sessions
- **Cleanup Rules**:
  - Remove old temporary files from previous sessions
  - Remove temporary directories created for testing/extraction
  - Always preserve `.gitkeep` file for git tracking
  - Keep final deliverables and summary documents
- **Never Delete**: `.gitkeep`, configuration files, or active project files

## FILE CONTEXT TEMPLATE
Always start new files with:
```python
"""
=== AI CONTEXT BLOCK ===
System: [System Name]
Purpose: [Brief description of functionality]
Dependencies: [Key dependencies and APIs used]
Performance: [Performance characteristics and constraints]
Error Handling: [Expected error scenarios]
Integration: [How this connects to other systems]
=== END AI CONTEXT ===
"""
```
