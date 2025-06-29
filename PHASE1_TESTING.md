# Phase 1 Testing - Quick Start Guide

## 🚀 **Ready to Test!**

### **Files Created:**
- ✅ **Test Plan**: `docs/Looting_System_Phase1_Test_Plan.md` (Complete 9-test case plan)
- ✅ **Build Script**: Updated `tasks.py` (includes looting system)  
- ✅ **Bundled Script**: `dist/DexBot.py` (165KB, syntax validated)

---

## 🎯 **Quick Testing Steps:**

### **1. Deploy to RazorEnhanced**
```powershell
# Copy the built script
copy dist\DexBot.py "C:\Program Files (x86)\Ultima Online Unchained\Data\Plugins\RazorEnhanced\Scripts\"
```

### **2. Essential Tests to Run**
1. **Start DexBot** - Look for "Looting system: disabled" message
2. **Main GUMP** - Verify LOOTING section appears with toggle/settings buttons
3. **Toggle Test** - Click looting toggle (Button 60), watch for enable/disable messages
4. **Settings GUMP** - Click settings button (Button 61), verify Looting Settings opens
5. **Configuration** - Check that `config/looting_config.json` is created

### **3. Optional Advanced Tests**
- Enable debug mode in `main_config.json` for detailed logging
- Kill a creature nearby to test corpse detection (should see "Found X corpses" messages)
- Test all toggle buttons in Looting Settings GUMP

---

## ✅ **Success Criteria:**
- No crashes or errors during startup
- GUMP interface shows looting section correctly
- Toggle buttons work and show console messages
- Configuration files are created and updated
- System integrates cleanly with existing healing/combat

---

## 📊 **Expected Console Output:**
```
[DexBot] Starting DexBot v2.2.0...
[DexBot] Auto heal system: [status]
[DexBot] Combat system: [status]  
[DexBot] Looting system: disabled    ← Look for this!
[DexBot] Bot is now active
[DexBot] Status GUMP created - use buttons to control bot

# When toggling:
[DexBot] Looting system enabled via GUMP    ← Should see this
[DexBot] Looting system disabled via GUMP   ← And this
```

---

## 🐛 **If Issues Found:**
1. Check console for error messages
2. Verify file permissions for config directory
3. Ensure RazorEnhanced client is connected
4. Restart RazorEnhanced if GUMP doesn't appear
5. Report issues with specific error messages and steps to reproduce

---

**Phase 1 Status**: ✅ Ready for In-Game Testing  
**Next Phase**: Phase 2 - Detailed Looting Logic (after Phase 1 validation)
