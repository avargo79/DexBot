# DexBot Phase 1 Test Automation Framework

This directory contains automated testing frameworks for validating DexBot Phase 1 (Looting System Core Infrastructure).

## 🧪 Testing Frameworks

### 1. Interactive Testing Framework (`test_automation.py`)
**Best for:** Step-by-step manual testing with guided assistance

**Features:**
- 9 comprehensive test cases covering all Phase 1 functionality
- Interactive guidance through each test step
- Automatic result collection and reporting
- JSON-based test result persistence
- Success rate analysis and Phase 2 readiness assessment

**Usage:**
```python
python test_automation.py
# Follow the interactive prompts
```

### 2. Enhanced Automated Framework (`test_automation_enhanced.py`)
**Best for:** Semi-automated testing with VS Code integration

**Features:**
- Advanced RazorEnhanced output monitoring
- Pattern matching for automated validation
- VS Code integration and reporting
- Three testing modes: Auto, Guided, Manual
- Real-time test result analysis
- Enhanced error handling and recovery testing

**Usage:**
```python
python test_automation_enhanced.py
# Choose from: 'auto', 'guided', or 'manual' mode
```

## 🎯 Test Coverage

### Phase 1 Test Cases
1. **System Startup and Integration** - Verify looting system initializes
2. **GUMP Interface Integration** - Validate main GUMP looting section  
3. **Looting System Toggle** - Test enable/disable functionality
4. **Looting Settings GUMP** - Verify dedicated settings interface
5. **Settings GUMP Controls** - Test all interactive controls
6. **Configuration File Management** - Validate config persistence
7. **Basic Corpse Detection** - Test detection-only functionality
8. **Error Handling and Recovery** - Verify graceful error handling
9. **Integration with Existing Systems** - Ensure no conflicts

### Success Criteria
- **80%+ Success Rate**: Ready for Phase 2 development
- **60-79% Success Rate**: Minor fixes needed
- **<60% Success Rate**: Major fixes required

## 🚀 Quick Start

### Prerequisites
- DexBot Phase 1 implementation completed
- `dist/DexBot.py` built and ready to deploy
- RazorEnhanced client with VS Code extension
- UO server connection established

### Running Tests
1. **Deploy Script**: Copy `dist/DexBot.py` to RazorEnhanced Scripts folder
2. **Choose Framework**: Interactive or Enhanced
3. **Execute Tests**: Follow framework-specific guidance
4. **Review Results**: Check generated JSON reports

### VS Code Integration
Use the provided VS Code tasks for enhanced workflow:
- `Ctrl+Shift+P` → "Tasks: Run Task"
- Select from available DexBot test tasks

## 📊 Test Results

Test results are automatically saved as JSON files:
- `test_results_phase1_[timestamp].json` (Interactive)
- `enhanced_test_report_phase1_[timestamp].json` (Enhanced)

### Result Structure
```json
{
  "phase": "Phase 1",
  "timestamp": 1234567890,
  "total_tests": 9,
  "summary": {
    "passed": 7,
    "failed": 1,
    "partial": 1,
    "skipped": 0,
    "success_rate": 83.3
  },
  "results": {
    "TEST_1": {
      "result": "pass",
      "notes": "All startup messages appeared",
      "timestamp": 1234567890
    }
  }
}
```

## 🔧 Advanced Usage

### Custom Test Patterns
Enhanced framework supports custom pattern matching:
```python
tester.monitor.set_expected_patterns([
    r"\[DexBot\] Custom message pattern",
    r"Expected output: \d+ items"
])
```

### RazorEnhanced Integration
The frameworks are designed to integrate with RazorEnhanced console output:
- Real-time message monitoring
- Pattern-based validation
- Automated result collection

### VS Code Extension Integration
When using the RazorEnhanced VS Code extension:
- Test results appear in VS Code output channels
- Integrated problem reporting
- Seamless workflow integration

## 📝 Best Practices

### Before Testing
1. ✅ Ensure Phase 1 implementation is complete
2. ✅ Build and validate `dist/DexBot.py`
3. ✅ Test in safe UO environment
4. ✅ Enable debug logging if available

### During Testing
1. 🎯 Follow test steps precisely
2. 👀 Monitor console output carefully
3. 📝 Document any unexpected behavior
4. 🔄 Retest failed cases when possible

### After Testing
1. 📊 Review success rates and detailed results
2. 🐛 Address any failed test cases
3. 📋 Update documentation if needed
4. ✅ Confirm readiness for Phase 2

## 🛠️ Troubleshooting

### Common Issues
- **No console output**: Verify RazorEnhanced connection
- **GUMP not appearing**: Check script deployment and execution
- **Config file issues**: Verify file permissions and JSON validity
- **Pattern matching fails**: Check exact message formats

### Debug Mode
Enable debug logging in `main_config.json`:
```json
{
  "debug_mode": true,
  "verbose_logging": true
}
```

## 🔄 Integration with Development Workflow

### Branch Strategy
- Test automation work: `feature/test-automation` (from main)
- Looting system work: `feature/looting-system` (from main)
- Keep test automation separate from feature implementation

### Continuous Testing
1. Run tests after each Phase 1 change
2. Validate before merging to main
3. Use results to guide Phase 2 development
4. Maintain test automation as features evolve

## 📈 Future Enhancements

### Planned Features
- Real-time RazorEnhanced log parsing
- Automated screenshot capture
- Web-based test dashboard
- Integration with CI/CD pipelines
- Phase 2 test case expansion

### Contributing
When adding new test cases:
1. Follow existing test case structure
2. Include clear pass/fail criteria
3. Add appropriate automation level
4. Update documentation

---

## 🏁 Ready to Test?

1. Choose your testing approach:
   - **Quick validation**: Interactive framework
   - **Comprehensive analysis**: Enhanced framework
   - **Custom testing**: Modify frameworks as needed

2. Execute tests systematically
3. Review results and fix issues
4. Proceed to Phase 2 when ready

**Success Rate Target: 80%+ for Phase 2 readiness**
