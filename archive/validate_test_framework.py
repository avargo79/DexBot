"""
DexBot Test Automation Framework Validation
Quick validation script to ensure all test components are working
"""

import sys
import os
import importlib
from pathlib import Path


def validate_test_framework():
    """Validate that the test automation framework is properly set up"""
    print("🔍 DexBot Test Automation Framework Validation")
    print("=" * 55)
    
    validation_results = []
    
    # Check 1: Test automation files exist
    print("📁 Checking test automation files...")
    required_files = [
        "test_automation.py",
        "test_automation_enhanced.py", 
        "test_launcher.py",
        "TEST_AUTOMATION_README.md"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
            validation_results.append(("file_" + file.replace(".", "_"), True))
        else:
            print(f"   ❌ {file} - MISSING")
            validation_results.append(("file_" + file.replace(".", "_"), False))
    
    # Check 2: Python imports work
    print("\n🐍 Checking Python imports...")
    try:
        import test_automation
        print("   ✅ test_automation.py imports successfully")
        validation_results.append(("import_basic", True))
    except Exception as e:
        print(f"   ❌ test_automation.py import failed: {e}")
        validation_results.append(("import_basic", False))
    
    try:
        import test_automation_enhanced
        print("   ✅ test_automation_enhanced.py imports successfully")
        validation_results.append(("import_enhanced", True))
    except Exception as e:
        print(f"   ❌ test_automation_enhanced.py import failed: {e}")
        validation_results.append(("import_enhanced", False))
    
    # Check 3: Test case definitions
    print("\n🧪 Checking test case definitions...")
    try:
        from test_automation import DexBotTester
        tester = DexBotTester()
        test_count = len(tester.test_cases)
        print(f"   ✅ Basic framework: {test_count} test cases defined")
        validation_results.append(("basic_tests", test_count == 9))
        
        # Validate test case structure
        required_keys = ['id', 'name', 'description', 'steps', 'pass_criteria']
        all_valid = True
        for test in tester.test_cases:
            for key in required_keys:
                if key not in test:
                    print(f"   ⚠️  Test {test.get('id', 'UNKNOWN')} missing '{key}'")
                    all_valid = False
        
        if all_valid:
            print("   ✅ All test cases have required structure")
            validation_results.append(("test_structure", True))
        else:
            validation_results.append(("test_structure", False))
            
    except Exception as e:
        print(f"   ❌ Test case validation failed: {e}")
        validation_results.append(("basic_tests", False))
        validation_results.append(("test_structure", False))
    
    # Check 4: Enhanced framework
    print("\n🤖 Checking enhanced framework...")
    try:
        from test_automation_enhanced import EnhancedDexBotTester
        enhanced_tester = EnhancedDexBotTester()
        enhanced_count = len(enhanced_tester.test_cases)
        print(f"   ✅ Enhanced framework: {enhanced_count} test cases defined")
        validation_results.append(("enhanced_tests", enhanced_count == 9))
        
        # Check for automation levels
        automation_levels = set()
        for test in enhanced_tester.test_cases:
            if 'automation_level' in test:
                automation_levels.add(test['automation_level'])
        
        print(f"   ✅ Automation levels: {', '.join(sorted(automation_levels))}")
        validation_results.append(("automation_levels", len(automation_levels) >= 2))
        
    except Exception as e:
        print(f"   ❌ Enhanced framework validation failed: {e}")
        validation_results.append(("enhanced_tests", False))
        validation_results.append(("automation_levels", False))
    
    # Check 5: VS Code integration
    print("\n💻 Checking VS Code integration...")
    vscode_dir = Path(".vscode")
    if vscode_dir.exists():
        tasks_file = vscode_dir / "tasks.json"
        if tasks_file.exists():
            print("   ✅ VS Code tasks.json exists")
            validation_results.append(("vscode_tasks", True))
            
            try:
                import json
                with open(tasks_file, 'r') as f:
                    tasks = json.load(f)
                
                task_count = len(tasks.get('tasks', []))
                print(f"   ✅ Found {task_count} VS Code tasks defined")
                validation_results.append(("task_count", task_count >= 3))
                
            except Exception as e:
                print(f"   ⚠️  Could not parse tasks.json: {e}")
                validation_results.append(("task_count", False))
        else:
            print("   ❌ VS Code tasks.json missing")
            validation_results.append(("vscode_tasks", False))
            validation_results.append(("task_count", False))
    else:
        print("   ❌ .vscode directory missing")
        validation_results.append(("vscode_tasks", False))
        validation_results.append(("task_count", False))
    
    # Check 6: Documentation
    print("\n📚 Checking documentation...")
    readme_exists = os.path.exists("TEST_AUTOMATION_README.md")
    if readme_exists:
        print("   ✅ TEST_AUTOMATION_README.md exists")
        
        # Check if README has reasonable content
        try:
            with open("TEST_AUTOMATION_README.md", 'r', encoding='utf-8') as f:
                content = f.read()
            
            if len(content) > 1000:  # Reasonable size check
                print("   ✅ README has substantial content")
                validation_results.append(("readme_content", True))
            else:
                print("   ⚠️  README seems too short")
                validation_results.append(("readme_content", False))
                
        except Exception as e:
            print(f"   ⚠️  Could not read README: {e}")
            validation_results.append(("readme_content", False))
    else:
        print("   ❌ TEST_AUTOMATION_README.md missing")
        validation_results.append(("readme_content", False))
    
    # Final Results
    print("\n" + "=" * 55)
    print("📊 VALIDATION RESULTS")
    print("=" * 55)
    
    passed = sum(1 for _, result in validation_results if result)
    total = len(validation_results)
    success_rate = (passed / total) * 100
    
    print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT! Test automation framework is ready to use!")
        status = "excellent"
    elif success_rate >= 75:
        print("✅ GOOD! Test automation framework is mostly ready")
        status = "good"
    elif success_rate >= 50:
        print("⚠️  NEEDS WORK! Some issues found")
        status = "needs_work"
    else:
        print("❌ MAJOR ISSUES! Framework needs significant fixes")
        status = "major_issues"
    
    # Show failed validations
    failed = [(name, result) for name, result in validation_results if not result]
    if failed:
        print(f"\n❌ Failed validations:")
        for name, _ in failed:
            print(f"   • {name}")
    
    print(f"\n🎯 RECOMMENDATION:")
    if status == "excellent":
        print("   Framework is ready for Phase 1 testing!")
        print("   Run 'python test_launcher.py' to start testing")
    elif status == "good":
        print("   Framework is usable but consider fixing minor issues")
        print("   Can proceed with testing")
    else:
        print("   Fix the failed validations before using the framework")
        print("   Review setup instructions and ensure all files are present")
    
    return {
        "success_rate": success_rate,
        "status": status,
        "passed": passed,
        "total": total,
        "failed_checks": failed
    }


def main():
    """Main validation function"""
    print("Starting DexBot test automation framework validation...\n")
    
    try:
        results = validate_test_framework()
        
        # Save validation results
        import json
        import time
        
        validation_file = f"validation_results_{int(time.time())}.json"
        with open(validation_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Validation results saved to: {validation_file}")
        
        return results
        
    except Exception as e:
        print(f"❌ Validation failed with error: {e}")
        return {"success_rate": 0, "status": "error", "error": str(e)}


if __name__ == "__main__":
    results = main()
    
    # Exit with appropriate code
    if results.get("success_rate", 0) >= 75:
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Issues found
