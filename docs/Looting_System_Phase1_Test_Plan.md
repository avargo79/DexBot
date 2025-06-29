# DexBot Looting System - Phase 1 Test Plan

**Version**: Phase 1 - Core Infrastructure  
**Date**: June 29, 2025  
**Build Target**: v1.0.0-phase1  
**Tester**: Manual Testing Required  

## 🎯 **Phase 1 Testing Scope**

### ✅ **What's Implemented in Phase 1:**
- Core LootingSystem class infrastructure
- GUMP interface integration (main GUMP + settings GUMP)
- Configuration system with JSON file management
- Basic corpse detection framework
- Toggle controls and settings persistence
- System integration with main bot loop

### ❌ **What's NOT Implemented (Future Phases):**
- Actual item looting from corpses
- Skinning knife usage and creature skinning
- Item evaluation and filtering logic
- Inventory weight/space management
- Advanced error recovery

---

## 🧪 **Test Plan**

### **Pre-Test Setup**

#### **Environment Requirements:**
- ✅ RazorEnhanced client connected to UO server
- ✅ Character in-game with basic gear
- ✅ Access to creatures for corpse generation testing
- ✅ Debug mode enabled (optional but recommended)

#### **Build Instructions:**
```powershell
# Navigate to DexBot directory
cd "C:\Program Files (x86)\Ultima Online Unchained\Data\Plugins\RazorEnhanced\Scripts\DexBot"

# Build the bundled script
python -m invoke bundle

# Copy to RazorEnhanced Scripts folder
copy dist\DexBot.py "C:\Program Files (x86)\Ultima Online Unchained\Data\Plugins\RazorEnhanced\Scripts\"
```

#### **Enable Debug Mode (Recommended):**
Edit `config/main_config.json`:
```json
{
    "debug_mode": true
}
```

---

## 📝 **Test Cases**

### **TEST 1: System Startup and Integration**

**Objective**: Verify looting system initializes and integrates properly

**Steps:**
1. Start DexBot script in RazorEnhanced
2. Observe console output during startup

**Expected Results:**
```
[DexBot] Starting DexBot v2.2.0...
[DexBot] Auto heal system: [enabled/disabled]
[DexBot] Combat system: [enabled/disabled]  
[DexBot] Looting system: disabled
[DexBot] Bot is now active
[DexBot] Status GUMP created - use buttons to control bot
```

**Pass Criteria:**
- ✅ No startup errors
- ✅ "Looting system: disabled" message appears
- ✅ GUMP appears with looting section

---

### **TEST 2: GUMP Interface - Main GUMP Integration**

**Objective**: Verify looting system appears in main GUMP with proper controls

**Steps:**
1. Ensure DexBot GUMP is visible
2. Locate the "LOOTING" section in the main GUMP
3. Verify toggle and settings buttons are present

**Expected Results:**
- ✅ LOOTING section visible in main GUMP
- ✅ Enable/disable toggle button (Button 60)
- ✅ Settings button (Button 61)
- ✅ Status shows "Disabled" initially
- ✅ Both buttons have proper tooltips on hover

**Visual Reference:**
```
[HEALING] [Toggle] [Settings] | Status: Active
[COMBAT]  [Toggle] [Settings] | Status: Disabled  
[LOOTING] [Toggle] [Settings] | Status: Disabled
```

---

### **TEST 3: Looting System Toggle (Main GUMP)**

**Objective**: Test enabling/disabling looting system from main GUMP

**Steps:**
1. Click the looting system toggle button (Button 60)
2. Observe console messages
3. Verify GUMP updates
4. Toggle again to disable

**Expected Results:**
```
# When enabling:
[DexBot] Looting system enabled via GUMP

# When disabling:  
[DexBot] Looting system disabled via GUMP
```

**Pass Criteria:**
- ✅ Console messages appear correctly
- ✅ GUMP status updates to "Active"/"Disabled"
- ✅ No errors in console
- ✅ Settings persist after toggle

---

### **TEST 4: Looting Settings GUMP**

**Objective**: Test dedicated looting settings interface

**Steps:**
1. Click the looting settings button (Button 61) from main GUMP
2. Verify Looting Settings GUMP opens
3. Check all sections and controls are present

**Expected Results:**
- ✅ Looting Settings GUMP opens (replaces main GUMP)
- ✅ Title: "LOOTING SETTINGS"
- ✅ Back button (top-left)
- ✅ Close button (top-right)
- ✅ "LOOTING SYSTEM" section with toggle
- ✅ "BEHAVIOR SETTINGS" section with current values
- ✅ "CURRENT STATUS" section with player info
- ✅ "LOOT CONFIGURATION" information section

**Visual Sections to Verify:**
```
LOOTING SETTINGS
├── LOOTING SYSTEM
│   ├── Looting System: [ENABLED/DISABLED]
│   └── Auto Skinning: [ENABLED/DISABLED]
├── BEHAVIOR SETTINGS  
│   ├── Looting Range: 2 tiles
│   └── Weight Limit: 80%
├── CURRENT STATUS
│   ├── System Status: [Active/Disabled]
│   ├── Weight: [current]/[max] ([%])
│   └── Looting Range: 2 tiles
└── LOOT CONFIGURATION
    ├── Loot lists are configured in looting_config.json
    ├── • Always Take: Gold, gems, rare items
    ├── • Take If Space: Weapons, armor, reagents  
    └── • Never Take: Junk items, tools, containers
```

---

### **TEST 5: Settings GUMP Controls**

**Objective**: Test all interactive controls in the Looting Settings GUMP

**Steps:**
1. Open Looting Settings GUMP
2. Click "Looting System" toggle (Button 71)
3. Click "Auto Skinning" toggle (Button 72)  
4. Click "Back" button (Button 70)
5. Verify all state changes persist

**Expected Results:**
```
# When toggling looting system:
[DexBot] Looting system [enabled/disabled] via Looting Settings

# When toggling auto skinning:
[DexBot] Auto skinning [enabled/disabled] via Looting Settings
```

**Pass Criteria:**
- ✅ Both toggles work and show console messages
- ✅ GUMP updates immediately to show new states
- ✅ Back button returns to main GUMP
- ✅ Settings are preserved when returning

---

### **TEST 6: Configuration File Management**

**Objective**: Verify configuration file creation and persistence

**Steps:**
1. Check if `config/looting_config.json` exists
2. Toggle looting system settings via GUMP
3. Check file contents update
4. Restart DexBot and verify settings persist

**Expected File Location:**
```
DexBot/config/looting_config.json
```

**Expected File Structure:**
```json
{
    "version": "1.0",
    "enabled": false,
    "timing": { ... },
    "behavior": { ... },
    "loot_lists": { ... }
}
```

**Pass Criteria:**
- ✅ File is created on first run
- ✅ File updates when settings change
- ✅ Settings persist after script restart
- ✅ File contains valid JSON

---

### **TEST 7: Basic Corpse Detection**

**Objective**: Test corpse scanning functionality (detection only, no looting)

**Prerequisites:**
- Looting system must be enabled via GUMP
- Debug mode recommended for detailed logging

**Steps:**
1. Enable looting system
2. Kill a creature within 2 tiles of character
3. Wait 1-2 seconds for corpse scan
4. Observe console output

**Expected Results:**
```
# With debug mode:
Found 1 corpses in range
Processing corpse: Unknown Creature at distance 1.4

# Without debug mode:
(May see minimal or no output - this is normal for Phase 1)
```

**Pass Criteria:**
- ✅ No errors when corpses are nearby
- ✅ Debug logging shows corpse detection (if enabled)
- ✅ System doesn't crash or interfere with other bot functions

---

### **TEST 8: Error Handling and Recovery**

**Objective**: Verify system handles errors gracefully

**Steps:**
1. Test with no corpses nearby (normal operation)
2. Test rapid GUMP button clicking
3. Test toggling settings multiple times quickly
4. Move away from any corpses and observe behavior

**Expected Results:**
- ✅ No crashes or exceptions
- ✅ System continues operating normally
- ✅ Rate limiting prevents button spam
- ✅ Graceful handling of edge cases

**Pass Criteria:**
- ✅ No unhandled exceptions in console
- ✅ Bot continues normal operation
- ✅ All other systems (healing, combat) unaffected

---

### **TEST 9: Integration with Existing Systems**

**Objective**: Verify looting system doesn't interfere with other bot functions

**Steps:**
1. Enable looting system
2. Test auto-heal functionality (take damage, use bandages/potions)
3. Test combat system (if enabled)
4. Verify all systems work together

**Expected Results:**
- ✅ Auto-heal continues working normally
- ✅ Combat system unaffected
- ✅ GUMP updates correctly for all systems
- ✅ No conflicts or performance issues

---

## 📊 **Test Results Template**

### **Test Environment:**
- **Date**: ___________
- **Tester**: ___________
- **UO Shard**: ___________
- **RazorEnhanced Version**: ___________
- **DexBot Build**: v1.0.0-phase1

### **Results Summary:**
| Test Case | Status | Notes |
|-----------|---------|-------|
| System Startup | ⬜ Pass ⬜ Fail | |
| Main GUMP Integration | ⬜ Pass ⬜ Fail | |
| Looting Toggle | ⬜ Pass ⬜ Fail | |
| Settings GUMP | ⬜ Pass ⬜ Fail | |
| Settings Controls | ⬜ Pass ⬜ Fail | |
| Configuration Files | ⬜ Pass ⬜ Fail | |
| Corpse Detection | ⬜ Pass ⬜ Fail | |
| Error Handling | ⬜ Pass ⬜ Fail | |
| System Integration | ⬜ Pass ⬜ Fail | |

### **Overall Phase 1 Result:**
- ⬜ **PASS** - Ready for Phase 2 development
- ⬜ **FAIL** - Issues must be resolved before Phase 2

### **Issues Found:**
```
1. [Issue description]
   - Severity: [High/Medium/Low]  
   - Steps to reproduce: [steps]
   - Expected vs Actual: [description]

2. [Issue description]
   - Severity: [High/Medium/Low]
   - Steps to reproduce: [steps]  
   - Expected vs Actual: [description]
```

### **Notes and Observations:**
```
[Additional testing notes, performance observations, suggestions]
```

---

## 🔧 **Troubleshooting Common Issues**

### **Issue: GUMP doesn't show looting section**
- **Solution**: Verify script compilation successful, restart RazorEnhanced

### **Issue: Configuration file not created**
- **Solution**: Check directory permissions, verify script has write access

### **Issue: Toggle buttons don't work**
- **Solution**: Check console for errors, verify button IDs not conflicting

### **Issue: No corpse detection messages**
- **Solution**: Enable debug mode, ensure corpses are within 2 tiles, verify looting system enabled

---

## ✅ **Phase 1 Acceptance Criteria**

Phase 1 is considered **COMPLETE** and ready for Phase 2 when:

1. ✅ All 9 test cases pass without critical failures
2. ✅ GUMP interface fully functional with all controls working
3. ✅ Configuration system creates and manages files correctly
4. ✅ System integrates cleanly with existing bot functionality
5. ✅ No crashes, exceptions, or performance degradation
6. ✅ Basic corpse detection framework operational
7. ✅ Error handling prevents system failures

**Next Phase**: Upon successful Phase 1 completion, proceed to Phase 2 - Detailed Looting Logic Implementation.

---

**Test Plan Version**: 1.0  
**Last Updated**: June 29, 2025  
**Status**: Ready for Testing
