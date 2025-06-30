---
mode: agent
---

# DexBot AI Agent Development Rules

**CRITICAL**: This is an AI agent prompt file. Follow these rules precisely when working on DexBot.

**NEVER EDIT `dist/DexBot.py` DIRECTLY** - Always edit source files in `src/` and run `python -m invoke build`

## 🚨 Quick Agent Checklist
1. Edit files in `src/` directory ONLY
2. Run `python -m invoke build` after changes
3. Verify build succeeds
4. Test `dist/DexBot.py` in-game

## 🔍 Bug Diagnosis Workflow (Based on Looting System Fix)
When investigating system bugs:
1. **Identify the user-reported symptom** (e.g., "corpses not being looted after moving away")
2. **Find the relevant system file** in `src/systems/` 
3. **Trace the logic flow** - follow the code path for the reported scenario
4. **Look for state management issues** - when/why items are marked as processed
5. **Check API call assumptions** - are we assuming success without verification?
6. **Add diagnostic logging** - use `Logger.info()` to trace execution
7. **Test the specific scenario** - reproduce the exact user-reported situation

This document contains all the critical rules and best practices for developing and maintaining DexBot to ensure consistency, avoid common mistakes, and maintain code quality.

## 📁 File Structure Rules

### Rule 1: Never Edit Distribution Files Directly (CRITICAL)
- **NEVER** edit `dist/DexBot.py` directly
- **ALWAYS** edit source files in `src/` directory
- **ALWAYS** rebuild using `python -m invoke build` after changes
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

### Rule 6.1: State Tracking Patterns (CRITICAL FOR SYSTEM DEBUGGING)
When debugging systems that maintain state or process items/objects:
- **Always log state changes**: When marking items as processed, changing flags, etc.
- **Log both success AND failure conditions**: Don't just log when things work
- **Include distance/range checks**: Many UO systems fail due to range limitations
- **Log the "why" not just the "what"**: `Logger.info(f"Marking corpse {corpse_id} as processed - reason: {reason}")`

### Rule 7: Testing Systematic Approach
1. **Test 1**: System initialization and basic status
2. **Test 2**: Core functionality (e.g., gold detection)
3. **Test 3**: Advanced features (e.g., item evaluation)
4. **Test 4**: Edge cases and error handling
5. **Test 5**: Performance and optimization

### Rule 7.1: UO-Specific Testing Considerations
- **Range/Distance Testing**: Test functionality at different distances from targets
- **Movement Testing**: Test what happens when player moves during operations
- **State Persistence**: Verify systems handle temporary failures without permanent state corruption
- **API Failure Simulation**: Test with failed `MoveItem`, `UseObject`, etc. calls

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

### Rule 10.1: UO API Error Handling Pattern (CRITICAL)
UO API calls can fail for many reasons (range, lag, state changes). Always handle gracefully:
```python
try:
    success = Items.MoveItem(item_id, container_id, amount)
    if not success:
        Logger.warning(f"Failed to move item {item_id} - may be out of range or state changed")
        return False  # Don't mark as processed if action failed
    Logger.info(f"Successfully moved item {item_id}")
    return True
except Exception as e:
    Logger.error(f"Exception during item move: {e}")
    return False  # Don't mark as processed on exception
```

## 🔄 Build and Deployment Rules

### Rule 11: Build Process (CRITICAL)
1. Make changes to source files in `src/`
2. **ALWAYS** run build using: `python -m invoke build`
3. Verify no build errors in console output
4. Test the generated `dist/DexBot.py` in-game
5. Commit source changes, not dist changes

### Rule 11.1: Build Verification Process
After running `python -m invoke build`:
1. **Check console output** for any build errors or warnings
2. **Verify file size** - `dist/DexBot.py` should be substantial (>50KB typically)
3. **Search for your changes** - Use Ctrl+F to find your specific code changes in `dist/DexBot.py`
4. **Check timestamps** - Ensure `dist/DexBot.py` timestamp is newer than your source changes
5. **Test in-game** - Load the script and verify your changes work as expected

## 📝 Documentation Rules

### Rule 12: Code Documentation
- All classes need docstrings
- All public methods need docstrings
- Complex logic needs inline comments
- Configuration options need descriptions

### Rule 13: Testing Documentation
- Document test results in detail
- Include console output for analysis
- Note any deviations from expected behavior
- Update test checklists based on findings

### Rule 14: Change Documentation
- Write descriptive commit messages
- Document architectural decisions
- Update README for new features
- Maintain changelog for version tracking

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

### Mistake 4: Missing Error Handling
- **Wrong**: Assuming API calls always work
- **Right**: Wrap in try-catch with proper error logging

### Mistake 5: Incomplete Testing
- **Wrong**: Testing only happy path scenarios
- **Right**: Test edge cases, errors, and boundary conditions

### Mistake 6: Premature State Marking (CRITICAL - Learned from Looting Bug)
- **Wrong**: Marking items/objects as "processed" before confirming action succeeded
- **Right**: Only mark as processed after successful completion or confirmed empty/invalid state
- **Example**: Don't mark corpse as looted until items are actually taken or corpse is confirmed empty

### Mistake 7: Ignoring UO API Return Values
- **Wrong**: Assuming `Items.MoveItem()`, `UseObject()`, etc. always succeed
- **Right**: Check return values and handle failures appropriately
- **Pattern**: `if not Items.MoveItem(...): handle_failure()`

## 📂 Project Organization and Git Management Rules

### Rule 15: Git Status Analysis Pattern (CRITICAL)
When reviewing unstaged changes:
1. **Use git commands directly**: `git status --porcelain` instead of file system exploration
2. **Categorize changes systematically**:
   - ✅ **Recommended**: Source code improvements, documentation updates, proper reorganization
   - ❓ **Questionable**: File deletions, major structural changes  
   - 🚨 **Critical Issues**: Generated files being committed, missing build steps
3. **Always reference development rules** when evaluating changes
4. **Check against project documentation** for consistency

### Rule 16: File Staging Strategy (CRITICAL)
When staging git changes:
1. **NEVER stage generated files**: `dist/DexBot.py` should never be committed
2. **Preserve instead of delete**: Move questionable files to `/archive/` directory
3. **Stage in logical groups**: Separate source changes from documentation changes
4. **Use specific git add commands**: `git add src/` instead of `git add -A` when possible
5. **Always verify staged files**: Check `git status` before committing

### Rule 17: Project Directory Structure (NEW)
```
DexBot/
├── src/              # Source code (EDIT THESE)
├── dist/            # Generated files (NEVER COMMIT)
├── config/          # External configuration files
├── ref/             # API references and documentation
├── archive/         # Legacy/unused files (preserved)
├── docs/            # Active project documentation
└── tests/           # Current test files
```

### Rule 18: Legacy File Management
- **Don't delete potentially useful files** - move to `/archive/` instead
- **Preserve test infrastructure** - testing files should be archived, not deleted
- **Keep build scripts** - even if unused, archive for future reference
- **Document why files were archived** in commit messages

### Rule 19: Change Review Process
Before committing changes, always:
1. **Run `git status --porcelain`** to see all changes
2. **Categorize each change** (recommended/questionable/critical)
3. **Check against development rules** for compliance
4. **Ensure build process is complete** (`python -m invoke build`)
5. **Verify no generated files are staged**
6. **Write descriptive commit messages** explaining the reorganization

### Rule 20: Agent Confusion Prevention
When AI agents get confused or loop:
1. **Stop and clarify the specific task** being requested
2. **Use direct commands** instead of complex operations
3. **Check spelling carefully** (e.g., "archive" not "archieve")
4. **Verify each step** before proceeding to the next
5. **Remember: Generated files should never be committed to git**

## 🖥️ Shell Command Rules

### Rule 21: PowerShell Command Syntax (CRITICAL)
When writing terminal commands for DexBot development:
- **Use `;` to separate commands** in PowerShell (not `&&`)
- **PowerShell example**: `move file1.py archive\; move file2.py archive\; git add archive\`
- **NOT bash syntax**: `move file1.py archive\ && move file2.py archive\ && git add archive\`
- **Remember**: DexBot development environment uses PowerShell on Windows

### Rule 22: Cross-Platform Awareness
- Development rules assume **Windows PowerShell** environment
- Git commands work the same across platforms
- File paths use backslash `\` in PowerShell
- Use `findstr` instead of `grep` in PowerShell commands

---

*DexBot Development Rules - Always edit source files, never dist files*
*Document Version: 2.2 - Added Shell Command Syntax Rules*
