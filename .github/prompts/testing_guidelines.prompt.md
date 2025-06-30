---
mode: agent
---

# DexBot Testing Guidelines and Protocols

## 🎯 Current Testing Status: Phase 2 - Looting System Core Logic

### ✅ Completed Tests
- **Test 1 (Basic System Check)**: PASSED - All systems properly enabled and initialized

### 🔄 Current Test: Test 2 (Gold Detection and Processing)
**Status**: System running but not processing corpses - investigating enablement logic

### 📊 Latest Test Results
**System Integration**: ✅ WORKING
- Looting system initializes correctly
- Main loop calls `looting_system.update()` successfully
- No system crashes or errors

**Current Issue**: System calls `update()` but exits early
- Need to verify `is_enabled()` logic
- Need to verify corpse detection
- Need detailed execution tracing

## 🧪 Testing Protocol

### Pre-Test Checklist
1. **Build first**: Run `powershell -ExecutionPolicy Bypass -File scripts\build.ps1`
2. **Verify build success**: Check for "Build completed successfully"
3. **Load script**: Use the updated `dist/DexBot.py` 
4. **Check initialization**: Verify "Looting System initialized" appears
5. **Verify status**: Look for "[DexBot] Looting system: enabled"

### Test Execution Steps
1. **Kill 2-3 mobs** to create corpses with potential gold
2. **Stay near corpses** (within 2 tiles)
3. **Watch console output** for specific logging patterns
4. **Document exact console output**
5. **Note any unexpected behavior**

### Expected Logging Patterns

**System Initialization**:
```
Looting System initialized
[DexBot] Looting system: enabled
```

**Main Loop Integration**:
```
MAIN LOOP: About to call looting_system.update()
LOOTING: update() called
MAIN LOOP: looting_system.update() completed successfully
```

**Corpse Processing** (when working):
```
LOOTING: self.enabled=True, config_enabled=True, is_enabled()=True
LOOTING: System is ENABLED - proceeding with update
LOOTING: About to scan for corpses
LOOTING: Found [X] corpses in range
LOOTING: Processing corpse...
```

## 🔍 Diagnostic Logging Levels

### Current Focus: Enhanced Enablement Diagnostics
Added detailed logging to trace execution path:
- System enablement status breakdown
- Step-by-step update cycle progress
- Corpse queue size tracking
- Cache and timing information

### Key Diagnostic Questions
1. **Is `self.enabled` True?**
2. **Is config `enabled` True?** 
3. **Does `is_enabled()` return True?**
4. **Are corpses being detected?**
5. **Is the corpse queue being populated?**

## 📝 Test Documentation Format

### Required Information
- **Build timestamp**: When was `dist/DexBot.py` last rebuilt?
- **Test environment**: Mob types killed, approximate gold amounts
- **Console output**: Full logging from script start to test completion
- **Expected vs Actual**: What should have happened vs what did happen
- **Follow-up actions**: Next steps based on results

### Issue Classification
- **System Integration**: Problems with main loop or system initialization
- **Configuration**: Problems with enabled states or config loading
- **Detection Logic**: Problems finding corpses or items
- **Processing Logic**: Problems with looting actions or item evaluation
- **Performance**: Problems with timing, delays, or resource usage

---

*Testing Guidelines Version: 1.0*
*Last Updated: 2025-01-27*
*Current Phase: Phase 2 - Core Logic Validation*
