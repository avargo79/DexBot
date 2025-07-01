---
description: "Instructions for generating RazorEnhanced bot systems"
applyTo: "src/systems/**/*.py"
---

# RazorEnhanced System Development Instructions

When creating or modifying DexBot systems in `src/systems/`, follow these specific patterns:

## System Architecture Pattern
```python
from typing import Dict, Any, Optional
from ..core.logger import Logger
from ..config.config_manager import ConfigManager
from System.Collections.Generic import List
from System import Int32 as int

class NewBotSystem:
    """
    Brief system description.
    
    This system handles [specific functionality] for the DexBot automation.
    Integrates with [other systems] and uses [RazorEnhanced APIs].
    """
    
    def __init__(self):
        """Initialize the system with configuration and state."""
        self.config_manager = ConfigManager()
        self.config = self.config_manager.get_system_config('new_system')
        self.enabled = self.config.get('enabled', False)
        self.last_check_time = 0
        
    def update(self) -> bool:
        """
        Main system update method called by bot loop.
        
        Returns:
            bool: True if system performed an action, False otherwise
        """
        if not self.enabled:
            return False
            
        try:
            return self._perform_system_logic()
        except Exception as e:
            Logger.error(f"System update failed: {e}")
            return False
```

## Required Methods for All Systems
- `__init__()`: Initialize with configuration
- `update()`: Main logic, returns bool indicating action taken
- `is_enabled()`: Check if system is active
- `get_status()`: Return system status for monitoring

## RazorEnhanced API Safety
Always wrap API calls:
```python
def _safe_api_call(self, operation: str, api_func, *args, **kwargs):
    """Safely call RazorEnhanced API with error handling."""
    try:
        result = api_func(*args, **kwargs)
        if result is None:
            Logger.warning(f"{operation} returned None")
        return result
    except Exception as e:
        Logger.error(f"{operation} failed: {e}")
        return None
```

## Performance Requirements
- Minimize API calls in update loops
- Cache frequently accessed data
- Use efficient data structures
- Profile memory usage for long sessions
- Implement rate limiting for API calls

## Error Recovery
- Graceful degradation when APIs fail
- Automatic retry with backoff
- Clear error messages for troubleshooting
- System state recovery after errors
