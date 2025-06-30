"""
Pre-Merge Validation Script for Test Automation Framework
Comprehensive testing before merging to main branch
"""

import sys
import os
import json
import traceback
from datetime import datetime


def test_basic_framework():
    """Test basic test automation framework"""
    print("🧪 Testing Basic Framework...")
    
    try:
        from test_automation import DexBotTester, run_interactive_test
        
        # Test instantiation
        tester = DexBotTester()
        assert len(tester.test_cases) == 9, f"Expected 9 test cases, got {len(tester.test_cases)}"
        
        # Test test case structure
        for i, test_case in enumerate(tester.test_cases):
            required_keys = ['id', 'name', 'description', 'steps', 'pass_criteria']
            for key in required_keys:
                assert key in test_case, f"Test case {i} missing required key: {key}"
        
        # Test result recording
        tester.record_result('TEST_1', 'pass', 'Mock test')
        assert 'TEST_1' in tester.test_results, "Result recording failed"
        assert tester.test_results['TEST_1']['result'] == 'pass', "Result not stored correctly"
        
        # Test run_interactive_test function
        test_tester = run_interactive_test()
        assert test_tester is not None, "run_interactive_test returned None"
        
        print("   ✅ Basic framework: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Basic framework: FAILED - {e}")
        traceback.print_exc()
        return False


def test_enhanced_framework():
    """Test enhanced automation framework"""
    print("🤖 Testing Enhanced Framework...")
    
    try:
        from test_automation_enhanced import EnhancedDexBotTester, run_enhanced_interactive_test
        
        # Test instantiation
        tester = EnhancedDexBotTester()
        assert len(tester.test_cases) == 9, f"Expected 9 test cases, got {len(tester.test_cases)}"
        
        # Test automation levels
        automation_levels = set()
        for test_case in tester.test_cases:
            if 'automation_level' in test_case:
                automation_levels.add(test_case['automation_level'])
        
        expected_levels = {'auto', 'manual', 'semi_auto'}
        assert automation_levels == expected_levels, f"Expected {expected_levels}, got {automation_levels}"
        
        # Test monitor components
        assert hasattr(tester, 'monitor'), "Monitor component missing"
        assert hasattr(tester, 'reporter'), "Reporter component missing"
        
        # Test run_enhanced_interactive_test function
        enhanced_tester = run_enhanced_interactive_test()
        assert enhanced_tester is not None, "run_enhanced_interactive_test returned None"
        
        print("   ✅ Enhanced framework: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Enhanced framework: FAILED - {e}")
        traceback.print_exc()
        return False


def test_launcher():
    """Test launcher functionality"""
    print("🚀 Testing Launcher...")
    
    try:
        import test_launcher
        
        # Test that main components exist
        assert hasattr(test_launcher, 'show_menu'), "show_menu function missing"
        assert hasattr(test_launcher, 'launch_interactive'), "launch_interactive function missing"
        assert hasattr(test_launcher, 'launch_enhanced'), "launch_enhanced function missing"
        assert hasattr(test_launcher, 'review_results'), "review_results function missing"
        assert hasattr(test_launcher, 'show_setup_help'), "show_setup_help function missing"
        assert hasattr(test_launcher, 'main'), "main function missing"
        
        print("   ✅ Launcher: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Launcher: FAILED - {e}")
        traceback.print_exc()
        return False


def test_vscode_integration():
    """Test VS Code integration"""
    print("💻 Testing VS Code Integration...")
    
    try:
        # Check tasks.json exists and is valid
        tasks_file = ".vscode/tasks.json"
        assert os.path.exists(tasks_file), "tasks.json file missing"
        
        with open(tasks_file, 'r') as f:
            tasks_data = json.load(f)
        
        assert 'tasks' in tasks_data, "tasks key missing in tasks.json"
        assert len(tasks_data['tasks']) >= 3, f"Expected at least 3 tasks, got {len(tasks_data['tasks'])}"
        
        # Check that tasks have required fields
        for task in tasks_data['tasks']:
            assert 'label' in task, "Task missing label"
            assert 'type' in task, "Task missing type"
            assert 'command' in task, "Task missing command"
        
        print("   ✅ VS Code integration: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ VS Code integration: FAILED - {e}")
        traceback.print_exc()
        return False


def test_documentation():
    """Test documentation completeness"""
    print("📚 Testing Documentation...")
    
    try:
        readme_file = "TEST_AUTOMATION_README.md"
        assert os.path.exists(readme_file), "README file missing"
        
        with open(readme_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for key sections
        required_sections = [
            "# DexBot Phase 1 Test Automation Framework",
            "## 🧪 Testing Frameworks",
            "## 🎯 Test Coverage",
            "## 🚀 Quick Start",
            "## 📊 Test Results"
        ]
        
        for section in required_sections:
            assert section in content, f"Missing section: {section}"
        
        assert len(content) > 5000, "Documentation seems too short"
        
        print("   ✅ Documentation: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Documentation: FAILED - {e}")
        traceback.print_exc()
        return False


def test_file_structure():
    """Test that all required files exist"""
    print("📁 Testing File Structure...")
    
    try:
        required_files = [
            "test_automation.py",
            "test_automation_enhanced.py",
            "test_launcher.py",
            "TEST_AUTOMATION_README.md",
            "validate_test_framework.py",
            ".vscode/tasks.json"
        ]
        
        for file in required_files:
            assert os.path.exists(file), f"Required file missing: {file}"
        
        print("   ✅ File structure: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ File structure: FAILED - {e}")
        return False


def test_json_output():
    """Test JSON output functionality"""
    print("📄 Testing JSON Output...")
    
    try:
        from test_automation import DexBotTester
        
        tester = DexBotTester()
        tester.record_result('TEST_1', 'pass', 'Mock test')
        
        # Simulate final results
        results = tester._show_final_results()
        
        # Check that results have expected structure
        assert 'status' in results, "Results missing status"
        assert 'success_rate' in results, "Results missing success_rate"
        assert 'ready_for_phase2' in results, "Results missing ready_for_phase2"
        
        print("   ✅ JSON output: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ JSON output: FAILED - {e}")
        traceback.print_exc()
        return False


def run_pre_merge_validation():
    """Run all pre-merge validation tests"""
    print("🔍 DexBot Test Automation Framework - Pre-Merge Validation")
    print("=" * 70)
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    tests = [
        ("File Structure", test_file_structure),
        ("Basic Framework", test_basic_framework),
        ("Enhanced Framework", test_enhanced_framework), 
        ("Launcher", test_launcher),
        ("VS Code Integration", test_vscode_integration),
        ("Documentation", test_documentation),
        ("JSON Output", test_json_output)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name}: FAILED with exception - {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("=" * 70)
    print("📊 PRE-MERGE VALIDATION RESULTS")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    success_rate = (passed / total) * 100
    
    print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
    
    for test_name, result in results:
        status_icon = "✅" if result else "❌"
        print(f"   {status_icon} {test_name}")
    
    print()
    
    if success_rate == 100:
        print("🎉 ALL TESTS PASSED! Framework is ready for merge to main.")
        recommendation = "READY_FOR_MERGE"
    elif success_rate >= 80:
        print("⚠️  MOSTLY READY! Minor issues found, but likely safe to merge.")
        recommendation = "MOSTLY_READY"
    else:
        print("❌ NOT READY! Significant issues found. Fix before merging.")
        recommendation = "NOT_READY"
    
    # Save results
    validation_results = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total,
        "passed": passed,
        "success_rate": success_rate,
        "recommendation": recommendation,
        "test_results": [{"name": name, "passed": result} for name, result in results]
    }
    
    results_file = f"pre_merge_validation_{int(datetime.now().timestamp())}.json"
    with open(results_file, 'w') as f:
        json.dump(validation_results, f, indent=2)
    
    print(f"\n💾 Validation results saved to: {results_file}")
    
    return success_rate == 100


if __name__ == "__main__":
    success = run_pre_merge_validation()
    sys.exit(0 if success else 1)
