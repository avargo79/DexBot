# DexBot Development Rules and Best Practices

This document contains all the critical rules and best practices for developing and maintaining DexBot to ensure consistency, avoid common mistakes, and maintain code quality.

## 📁 File Structure Rules

### Rule 1: Never Edit Distribution Files Directly
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

**Logging Pattern for New Systems**:
```python
# System entry
Logger.info(f"SYSTEM_NAME: Starting system check (enabled: {self.is_enabled()})")

# Key decision points  
Logger.info(f"SYSTEM_NAME: Found {count} items to process")

# System exit
Logger.info(f"SYSTEM_NAME: System check completed")
```

### Rule 7: Testing Systematic Approach
1. **Test 1**: System initialization and basic status
2. **Test 2**: Core functionality (e.g., gold detection)
3. **Test 3**: Advanced features (e.g., item evaluation)
4. **Test 4**: Edge cases and error handling
5. **Test 5**: Performance and optimization

### Rule 8: Add Debug Logging for New Features
When adding new systems:
- Add initialization logging
- Add main function entry/exit logging  
- Add status check logging
- Add error condition logging

## 🏗️ Code Architecture Rules

### Rule 9: System Enablement Pattern
Every system must implement:
```python
def is_enabled(self) -> bool:
    """Check if system is enabled"""
    config_enabled = self.config_manager.get_X_setting('enabled', False)
    result = self.enabled and config_enabled
    Logger.debug(f"System status - self.enabled: {self.enabled}, config_enabled: {config_enabled}, result: {result}")
    return result
```

### Rule 10: Main Loop Integration Pattern
```python
# System initialization (once)
system = SystemClass(config_manager)

# Main loop integration (every cycle)
if system.is_enabled():
    system.update()
```

### Rule 11: Error Handling Pattern
```python
try:
    # Main functionality
    pass
except Exception as e:
    Logger.error(f"System error: {e}")
    # Graceful degradation, not crash
```

## 📊 Looting System Specific Rules

### Rule 12: Looting System Architecture
1. **Corpse Detection** - Scan for corpses within range
2. **Item Evaluation** - Apply loot rules (always_take, take_if_space, never_take)
3. **Container Management** - Open corpses, handle timeouts
4. **Item Movement** - Take items with verification
5. **Inventory Management** - Check weight/space limits

### Rule 13: Looting Configuration Structure
```json
{
  "enabled": true,
  "loot_lists": {
    "always_take": [1712, "Gold", "Gem"],
    "take_if_space": ["Weapon", "Armor"],
    "never_take": ["Bottle", "Bone"]
  },
  "behavior": {
    "max_looting_range": 2,
    "inventory_weight_limit_percent": 80
  }
}
```

### Rule 14: Gold Detection Requirements
- Gold item ID `1712` must be in `always_take` list
- Gold detection should work regardless of item name
- Must have debug logging for gold detection/taking

## 🔄 Build and Deployment Rules

### Rule 15: Build Process (CRITICAL)
1. Make changes to source files in `src/`
2. **ALWAYS** run build using one of these methods:
   - From PowerShell: `powershell -ExecutionPolicy Bypass -File scripts\build.ps1`
   - From project root: `.\scripts\build.ps1` (if execution policy allows)
   - If execution issues: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` then `.\scripts\build.ps1`
3. Verify no build errors in console output
4. Test the generated `dist/DexBot.py` in-game
5. Commit source changes, not dist changes

**CRITICAL DISCOVERY**: The build script is essential and non-optional:
- Direct edits to `dist/DexBot.py` are lost and cause confusion
- The build script properly combines imports and maintains dependencies
- Changes to source files are NOT active until rebuilt
- **Always verify build completed successfully before testing**

**Build Command from Project Root**:
```powershell
# Recommended method (bypasses execution policy):
powershell -ExecutionPolicy Bypass -File scripts\build.ps1

# Alternative if execution policy is already set:
.\scripts\build.ps1
```

### Rule 15a: PowerShell Command Syntax (CRITICAL)
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

**Common PowerShell Command Combining Patterns**:
- Use `;` (semicolon) to run commands sequentially
- Use `|` (pipe) to pass output between commands  
- Use `&&` only in Command Prompt (cmd), not PowerShell

**Build Verification**:
- Check console for "Build completed successfully" message
- Verify `dist/DexBot.py` file timestamp updated
- Test in-game immediately after successful build

### Rule 16: Version Control
- Commit source files (`src/`)
- Do NOT commit `dist/DexBot.py` (it's generated)
- Use meaningful commit messages
- Test before committing

## 🚀 Testing Protocol Rules

### Rule 17: Phase Testing Approach
- **Phase 1**: System initialization and config validation
- **Phase 2**: Core functionality validation (current: looting)
- **Phase 3**: Integration testing (looting + combat + healing)
- **Phase 4**: Performance and optimization testing

### Rule 18: In-Game Testing Checklist
Before each test:
1. **Build first**: Run `.\scripts\build.ps1`
2. **Apply test config**: Use `tmp/testing_config_guide.md` for step-by-step setup
3. **Reload the script** (stop and restart)
4. **Verify console** shows expected initialization messages
5. **Kill test mobs** and observe console output
6. **Report exact console output** for analysis
7. **Document any unexpected behavior**

**Testing Configuration Files**:
- `tmp/testing_configs.py` - Comprehensive testing configurations
- `tmp/testing_config_guide.md` - Step-by-step application guide

## ⚠️ Common Mistakes to Avoid

### Mistake 1: Editing Distribution Files
- **Wrong**: Editing `dist/DexBot.py` directly
- **Right**: Edit `src/` files and rebuild

### Mistake 2: Debug Mode Issues
- **Wrong**: Assuming `Logger.debug()` works without verification
- **Right**: Test with `Logger.info()` first, then switch to debug

### Mistake 3: Configuration Sync Issues
- **Wrong**: Setting config in one place only
- **Right**: Ensure all config locations are synchronized

### Mistake 4: Missing Error Handling
- **Wrong**: Assuming API calls always work
- **Right**: Wrap in try-catch with proper error logging

### Mistake 5: Incomplete Testing
- **Wrong**: Testing only happy path scenarios
- **Right**: Test edge cases, errors, and boundary conditions

### Mistake 6: PowerShell Command Syntax
- **Wrong**: Using "&&" to combine PowerShell commands (`cd "path" && .\script.ps1`)
- **Right**: Use semicolon (`;`) or separate commands (`Set-Location "path"; .\script.ps1`)

## 📝 Documentation Rules

### Rule 19: Code Documentation
- All classes need docstrings
- All public methods need docstrings
- Complex logic needs inline comments
- Configuration options need descriptions

### Rule 20: Testing Documentation
- Document test results in detail
- Include console output for analysis
- Note any deviations from expected behavior
- Update test checklists based on findings

---

## 🎯 Current Development Focus

**Phase 2: Looting System Core Logic Validation**

**COMPLETED**:
- ✅ Fixed config synchronization issue (looting always "disabled")
- ✅ Added gold item ID (1712) to always_take loot list
- ✅ Enhanced debug logging throughout looting system
- ✅ Discovered and documented critical build process requirement
- ✅ Successfully completed Test 1 (Basic System Check)
- ✅ Added comprehensive execution path logging to main loop and looting system

**CURRENT STATUS**: 
- Ready for Test 2 (Gold Detection) with enhanced logging
- All systems properly enabled and configured
- Build process established and documented

**Next Steps**: 
1. Rerun Test 2 (Gold Detection) in-game with new info-level logging
2. Analyze logging output to verify looting system execution path
3. Continue through remaining tests in phase 2 checklist
4. Address any issues found and proceed to Phase 3

**Key Files**:
- `src/systems/looting.py` - Core looting logic (DO NOT EDIT dist/DexBot.py)
- `src/core/main_loop.py` - Main bot loop (DO NOT EDIT dist/DexBot.py)
- `scripts/build.ps1` - Critical build script (ALWAYS RUN AFTER CHANGES)
- `dist/DexBot.py` - Generated distribution (DO NOT EDIT DIRECTLY)

**Critical Discovery**: 
- Editing `dist/DexBot.py` directly was causing confusion and lost changes
- The `scripts/build.ps1` script properly combines all `src/` files
- **ALWAYS** edit source files and rebuild - this is non-negotiable

---

*Last Updated: 2025-01-27*
*Document Version: 1.1*
*Status: Phase 2 - Ready for Test 2 Execution*
