# DexBot Phase 1 Testing Guide

## 🎯 **GOAL**: Validate Phase 1 Looting System Implementation

### 📋 **QUICK START TESTING**

1. **Deploy Script**:
   - Copy `dist/DexBot.py` to your RazorEnhanced Scripts folder
   - Ensure RazorEnhanced is connected to UO server

2. **Run Test Framework**:
   ```python
   # In Python or VS Code terminal:
   from test_automation import DexBotTester
   
   tester = DexBotTester()
   
   # Start first test
   tester.next_test()
   
   # After performing test steps, record result:
   tester.record_result('TEST_1', 'pass', 'System started correctly')
   
   # Continue with next test
   tester.next_test()
   # ... repeat for all 9 tests
   ```

3. **Alternative: Use Enhanced Framework**:
   ```python
   from test_automation_enhanced import run_enhanced_interactive_test
   
   tester = run_enhanced_interactive_test()
   tester.set_testing_mode('guided')  # For step-by-step guidance
   ```

### 🧪 **THE 9 PHASE 1 TEST CASES**

1. **TEST_1: System Startup and Integration**
   - Start DexBot script in RazorEnhanced
   - Watch for: "[DexBot] Starting DexBot", "[DexBot] Looting system: disabled"
   - ✅ PASS if: No startup errors, GUMP appears

2. **TEST_2: GUMP Interface - Main GUMP Integration**
   - Verify LOOTING section appears in main GUMP
   - Check toggle button (60) and settings button (61)
   - ✅ PASS if: LOOTING section visible with proper buttons

3. **TEST_3: Looting System Toggle (Main GUMP)**
   - Click looting system toggle button (Button 60)
   - Watch console for toggle messages
   - ✅ PASS if: Console messages appear, GUMP updates

4. **TEST_4: Looting Settings GUMP**
   - Click looting settings button (Button 61)
   - Verify Looting Settings GUMP opens
   - ✅ PASS if: Settings GUMP opens with all sections

5. **TEST_5: Settings GUMP Controls**
   - Test all toggles in settings GUMP
   - Click Back button (Button 70)
   - ✅ PASS if: All controls work with feedback

6. **TEST_6: Configuration File Management**
   - Check for config/looting_config.json
   - Toggle settings and verify file updates
   - ✅ PASS if: File created and persists changes

7. **TEST_7: Basic Corpse Detection**
   - Enable looting system
   - Kill creature within 2 tiles
   - ✅ PASS if: No errors, debug shows corpse detection

8. **TEST_8: Error Handling and Recovery**
   - Test with no corpses nearby
   - Test rapid button clicking
   - ✅ PASS if: No crashes, system continues normally

9. **TEST_9: Integration with Existing Systems**
   - Enable looting system
   - Test auto-heal functionality
   - ✅ PASS if: All systems work together

### 📊 **SUCCESS CRITERIA**
- **80%+ Success Rate**: Ready for Phase 2 ✅
- **60-79% Success Rate**: Minor fixes needed ⚠️
- **<60% Success Rate**: Major fixes required ❌

### 🚀 **READY TO TEST?**

**Option 1 - Manual Testing:**
1. Deploy `dist/DexBot.py` to RazorEnhanced
2. Use the test framework to guide you through each test
3. Record results for analysis

**Option 2 - VS Code Integration:**
1. Press `Ctrl+Shift+P`
2. Type "Tasks: Run Task"
3. Select "DexBot: Run Phase 1 Interactive Tests"

**Option 3 - Direct Framework:**
```bash
python test_launcher.py
# Choose option 1 for Interactive Testing
```

Let's start testing! 🧪
