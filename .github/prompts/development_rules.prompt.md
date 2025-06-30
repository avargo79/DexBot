---
mode: agent
---

# DexBot Development Rules and Best Practices

This document contains all the critical rules and best practices for developing and maintaining DexBot to ensure consistency, avoid common mistakes, and maintain code quality.

## 📁 File Structure Rules

### Rule 1: Never Edit Distribution Files Directly (CRITICAL)
- **NEVER** edit `dist/DexBot.py` directly
- **ALWAYS** edit source files in `src/` directory
- **ALWAYS** rebuild using `scripts/build.ps1` after changes
- The `dist/DexBot.py` file is auto-generated and will be overwritten

### Rule 2: Source File Organization
```
src/
├── config/          # Configuration management
├── core/           # Core bot functionality (config, logger, main loop)
├── systems/        # Individual bot systems (healing, combat, looting)
├── ui/             # User interface (GUMP system)
└── utils/          # Utility functions and imports
```

## 🔧 Configuration Management Rules

### Rule 3: Configuration Hierarchy
1. **Defaults in code** - Fallback values in `DEFAULT_*_CONFIG` constants
2. **JSON config files** - User-modifiable settings in `config/` directory
3. **Runtime settings** - Temporary changes during execution

### Rule 4: Configuration Loading Order
1. Load defaults from code constants
2. Merge with JSON file settings (if exists)
3. Create JSON file with defaults if missing
4. Apply runtime overrides

### Rule 5: Debug Mode Configuration
- Debug mode must be enabled in **both** places:
  1. `global_settings.debug_mode: true` in main config
  2. `logging.log_level: "debug"` in main config
- Always verify debug logging works before proceeding with debugging

## 🐛 Debugging and Testing Rules

### Rule 6: Debug Message Hierarchy (CRITICAL FOR TROUBLESHOOTING)
1. Use `Logger.info()` for critical tracking during development and troubleshooting
2. Use `Logger.debug()` only after confirming debug mode works properly
3. Use `Logger.error()` for error conditions
4. Use `Logger.warning()` for non-critical issues

**TROUBLESHOOTING INSIGHT**: During development and issue resolution:
- **Always** start with `Logger.info()` for important validation messages
- This ensures visibility even if debug mode configuration is problematic
- Switch back to `Logger.debug()` only after confirming the issue is resolved
- Example: `Logger.info("LOOTING: System called - checking for corpses")` instead of `Logger.debug()`

### Rule 7: Testing Systematic Approach
1. **Test 1**: System initialization and basic status
2. **Test 2**: Core functionality (e.g., gold detection)
3. **Test 3**: Advanced features (e.g., item evaluation)
4. **Test 4**: Edge cases and error handling
5. **Test 5**: Performance and optimization

## 🏗️ Code Architecture Rules

### Rule 8: System Enablement Pattern
Every system must implement:
```python
def is_enabled(self) -> bool:
    """Check if system is enabled"""
    config_enabled = self.config_manager.get_X_setting('enabled', False)
    result = self.enabled and config_enabled
    Logger.debug(f"System status - self.enabled: {self.enabled}, config_enabled: {config_enabled}, result: {result}")
    return result
```

### Rule 9: Main Loop Integration Pattern
```python
# System initialization (once)
system = SystemClass(config_manager)

# Main loop integration (every cycle)
if system.is_enabled():
    system.update()
```

### Rule 10: Error Handling Pattern
```python
try:
    # Main functionality
    pass
except Exception as e:
    Logger.error(f"System error: {e}")
    # Graceful degradation, not crash
```

## 🔄 Build and Deployment Rules

### Rule 11: Build Process (CRITICAL)
1. Make changes to source files in `src/`
2. **ALWAYS** run build using one of these methods:
   - From PowerShell: `powershell -ExecutionPolicy Bypass -File scripts\build.ps1`
   - From project root: `.\scripts\build.ps1` (if execution policy allows)
   - If execution issues: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` then `.\scripts\build.ps1`
3. Verify no build errors in console output
4. Test the generated `dist/DexBot.py` in-game
5. Commit source changes, not dist changes

### Rule 12: PowerShell Command Syntax (CRITICAL)
**NEVER use "&&" to combine PowerShell commands** - it's not supported in PowerShell!

**Wrong**:
```powershell
cd "path" && .\scripts\build.ps1  # This will FAIL
```

**Right**:
```powershell
# Method 1: Use semicolon and Set-Location
Set-Location "c:\Program Files (x86)\Ultima Online Unchained\Data\Plugins\RazorEnhanced\Scripts\DexBot"; .\scripts\build.ps1

# Method 2: Navigate first, then run
cd "c:\Program Files (x86)\Ultima Online Unchained\Data\Plugins\RazorEnhanced\Scripts\DexBot"
.\scripts\build.ps1

# Method 3: Use full path
powershell -ExecutionPolicy Bypass -File "c:\Program Files (x86)\Ultima Online Unchained\Data\Plugins\RazorEnhanced\Scripts\DexBot\scripts\build.ps1"
```

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Editing Distribution Files (CRITICAL)
- **Wrong**: Editing `dist/DexBot.py` directly
- **Right**: Edit `src/` files and rebuild

### Mistake 2: Debug Mode Issues
- **Wrong**: Assuming `Logger.debug()` works without verification
- **Right**: Test with `Logger.info()` first, then switch to debug

### Mistake 3: Configuration Sync Issues
- **Wrong**: Setting config in one place only
- **Right**: Ensure all config locations are synchronized

### Mistake 4: PowerShell Command Syntax
- **Wrong**: Using "&&" to combine PowerShell commands (`cd "path" && .\script.ps1`)
- **Right**: Use semicolon (`;`) or separate commands (`Set-Location "path"; .\script.ps1`)

### Mistake 5: Missing Error Handling
- **Wrong**: Assuming API calls always work
- **Right**: Wrap in try-catch with proper error logging

### Mistake 6: Incomplete Testing
- **Wrong**: Testing only happy path scenarios
- **Right**: Test edge cases, errors, and boundary conditions

## 📝 Documentation Rules

### Rule 13: Code Documentation
- All classes need docstrings
- All public methods need docstrings
- Complex logic needs inline comments
- Configuration options need descriptions

### Rule 14: Testing Documentation
- Document test results in detail
- Include console output for analysis
- Note any deviations from expected behavior
- Update test checklists based on findings

---

*DexBot Development Rules - Always edit source files, never dist files*
*Document Version: 2.0*
