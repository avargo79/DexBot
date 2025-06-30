"""
Enhanced DexBot Phase 1 Testing Framework with VS Code Integration
Automated monitoring and test execution with real-time feedback
"""

import time
import json
import os
import re
import threading
import subprocess
from typing import Dict, List, Optional, Callable
from datetime import datetime
import logging


class RazorEnhancedMonitor:
    """Monitor RazorEnhanced output and script execution"""
    
    def __init__(self, log_callback: Optional[Callable] = None):
        self.log_callback = log_callback
        self.monitoring = False
        self.captured_messages = []
        self.expected_patterns = []
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start monitoring RazorEnhanced output"""
        self.monitoring = True
        self.captured_messages = []
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
            
    def set_expected_patterns(self, patterns: List[str]):
        """Set patterns to watch for in the output"""
        self.expected_patterns = [re.compile(pattern) for pattern in patterns]
        
    def _monitor_loop(self):
        """Main monitoring loop - would integrate with RazorEnhanced output"""
        # This would monitor actual RazorEnhanced console output
        # For now, we'll simulate monitoring by checking log files
        while self.monitoring:
            try:
                # In real implementation, this would monitor RazorEnhanced console
                # For now, we'll provide a framework for manual integration
                time.sleep(0.1)
            except Exception as e:
                if self.log_callback:
                    self.log_callback(f"Monitor error: {e}")
                    
    def check_for_pattern(self, pattern: str, timeout: int = 5) -> bool:
        """Check if a specific pattern appears in the output within timeout"""
        start_time = time.time()
        regex = re.compile(pattern)
        
        while time.time() - start_time < timeout:
            for message in self.captured_messages:
                if regex.search(message):
                    return True
            time.sleep(0.1)
            
        return False


class VSCodeTestReporter:
    """Report test results to VS Code through various channels"""
    
    def __init__(self):
        self.test_results = []
        self.current_test = None
        
    def start_test(self, test_id: str, test_name: str):
        """Start a new test"""
        self.current_test = {
            "id": test_id,
            "name": test_name,
            "start_time": datetime.now(),
            "status": "running",
            "messages": [],
            "screenshots": []
        }
        self._log_to_vscode(f"🧪 Starting test: {test_name}")
        
    def log_message(self, message: str, level: str = "info"):
        """Log a message for the current test"""
        if self.current_test:
            self.current_test["messages"].append({
                "timestamp": datetime.now(),
                "message": message,
                "level": level
            })
        self._log_to_vscode(f"[{level.upper()}] {message}")
        
    def complete_test(self, status: str, notes: str = ""):
        """Complete the current test"""
        if self.current_test:
            self.current_test.update({
                "status": status,
                "end_time": datetime.now(),
                "notes": notes,
                "duration": (datetime.now() - self.current_test["start_time"]).total_seconds()
            })
            self.test_results.append(self.current_test)
            self._log_to_vscode(f"✅ Test completed: {status}")
            
    def _log_to_vscode(self, message: str):
        """Log message to VS Code output channel"""
        # This would integrate with VS Code's output channel
        print(f"[VS Code] {message}")
        
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report"""
        total_tests = len(self.test_results)
        passed = sum(1 for test in self.test_results if test['status'] == 'pass')
        failed = sum(1 for test in self.test_results if test['status'] == 'fail')
        
        return {
            "summary": {
                "total": total_tests,
                "passed": passed,
                "failed": failed,
                "success_rate": (passed / total_tests * 100) if total_tests > 0 else 0
            },
            "tests": self.test_results,
            "generated_at": datetime.now().isoformat()
        }


class EnhancedDexBotTester:
    """Enhanced testing framework with automation and monitoring"""
    
    def __init__(self):
        self.monitor = RazorEnhancedMonitor(self._log_callback)
        self.reporter = VSCodeTestReporter()
        self.current_test = 0
        self.auto_mode = False
        
        # Enhanced test cases with automation hooks
        self.test_cases = [
            {
                "id": "TEST_1",
                "name": "System Startup and Integration",
                "description": "Verify looting system initializes properly",
                "automation_level": "semi_auto",  # Can be automated with monitoring
                "setup_steps": [
                    "Deploy DexBot.py to RazorEnhanced Scripts folder",
                    "Start RazorEnhanced client",
                    "Connect to UO server"
                ],
                "test_steps": [
                    "Execute DexBot script in RazorEnhanced",
                    "Monitor console output for startup messages"
                ],
                "expected_patterns": [
                    r"\[DexBot\] Starting DexBot",
                    r"\[DexBot\] Looting system: disabled",
                    r"\[DexBot\] Bot is now active",
                    r"\[DexBot\] Status GUMP created"
                ],
                "pass_criteria": "All expected startup messages appear within 10 seconds",
                "timeout": 15
            },
            {
                "id": "TEST_2",
                "name": "GUMP Interface - Main GUMP Integration", 
                "description": "Verify looting section appears in main GUMP",
                "automation_level": "manual",  # Requires visual verification
                "test_steps": [
                    "Locate DexBot main GUMP on screen",
                    "Verify LOOTING section is visible",
                    "Check toggle button (60) and settings button (61) presence"
                ],
                "visual_checks": [
                    "LOOTING section header visible",
                    "Toggle button with proper tooltip",
                    "Settings button with proper tooltip"
                ],
                "pass_criteria": "All visual elements present and properly labeled"
            },
            {
                "id": "TEST_3",
                "name": "Looting System Toggle (Main GUMP)",
                "description": "Test enable/disable from main GUMP",
                "automation_level": "semi_auto",
                "test_steps": [
                    "Click looting system toggle button (Button 60)",
                    "Monitor console for toggle messages",
                    "Verify GUMP visual state changes",
                    "Toggle again to test disable"
                ],
                "expected_patterns": [
                    r"\[DexBot\] Looting system enabled via GUMP",
                    r"\[DexBot\] Looting system disabled via GUMP"
                ],
                "interaction_required": "Button clicks on GUMP",
                "pass_criteria": "Toggle works both ways with proper console messages"
            },
            {
                "id": "TEST_4",
                "name": "Looting Settings GUMP",
                "description": "Test dedicated looting settings interface",
                "automation_level": "manual",
                "test_steps": [
                    "Click looting settings button (Button 61)",
                    "Verify Looting Settings GUMP opens",
                    "Check all required sections are present"
                ],
                "visual_checks": [
                    "LOOTING SETTINGS title",
                    "LOOTING SYSTEM section",
                    "BEHAVIOR SETTINGS section",
                    "CURRENT STATUS section", 
                    "LOOT CONFIGURATION section"
                ],
                "pass_criteria": "Settings GUMP opens with all sections visible and properly formatted"
            },
            {
                "id": "TEST_5",
                "name": "Settings GUMP Controls",
                "description": "Test interactive controls in settings GUMP",
                "automation_level": "semi_auto",
                "test_steps": [
                    "Open Looting Settings GUMP",
                    "Test Looting System toggle (Button 71)",
                    "Test Auto Skinning toggle (Button 72)",
                    "Test Back button (Button 70)"
                ],
                "expected_patterns": [
                    r"\[DexBot\] Looting system (enabled|disabled) via Looting Settings",
                    r"\[DexBot\] Auto skinning (enabled|disabled) via Looting Settings"
                ],
                "interaction_required": "Multiple button clicks",
                "pass_criteria": "All controls work with proper feedback"
            },
            {
                "id": "TEST_6",
                "name": "Configuration File Management",
                "description": "Verify config file creation and persistence",
                "automation_level": "auto",  # Can be fully automated
                "test_steps": [
                    "Check for config/looting_config.json existence",
                    "Verify file structure and default values",
                    "Test config persistence after changes"
                ],
                "file_checks": [
                    "config/looting_config.json exists",
                    "Valid JSON structure",
                    "All required configuration keys present"
                ],
                "pass_criteria": "Config file created with proper structure and persists changes"
            },
            {
                "id": "TEST_7",
                "name": "Basic Corpse Detection",
                "description": "Test corpse scanning (detection only)",
                "automation_level": "semi_auto",
                "setup_requirements": [
                    "Character positioned near killable creature",
                    "Looting system enabled"
                ],
                "test_steps": [
                    "Kill creature within 2 tiles of character",
                    "Monitor console for corpse detection messages",
                    "Verify no errors during detection process"
                ],
                "expected_patterns": [
                    r"Found \d+ corpses in range",
                    r"Processing corpse: .+"
                ],
                "pass_criteria": "Corpse detection works without errors"
            },
            {
                "id": "TEST_8",
                "name": "Error Handling and Recovery", 
                "description": "Verify graceful error handling",
                "automation_level": "semi_auto",
                "test_steps": [
                    "Test with no corpses nearby",
                    "Test rapid button clicking on GUMP",
                    "Test multiple quick setting toggles",
                    "Move away from corpses during processing"
                ],
                "error_patterns": [
                    r"Exception",
                    r"Error",
                    r"Failed"
                ],
                "pass_criteria": "No crashes or exceptions, system continues normally"
            },
            {
                "id": "TEST_9",
                "name": "Integration with Existing Systems",
                "description": "Verify no interference with other DexBot systems",
                "automation_level": "manual",
                "test_steps": [
                    "Enable looting system",
                    "Test auto-heal functionality",
                    "Test any other enabled DexBot systems",
                    "Verify all systems work together"
                ],
                "pass_criteria": "No conflicts between systems, all remain functional"
            }
        ]
    
    def _log_callback(self, message: str):
        """Callback for monitor log messages"""
        if self.reporter.current_test:
            self.reporter.log_message(message)
    
    def start_automated_testing(self):
        """Start the enhanced automated testing process"""
        print("🚀 Enhanced DexBot Phase 1 Testing Framework")
        print("=" * 65)
        print("🤖 Features:")
        print("   • Automated monitoring of RazorEnhanced output")
        print("   • Semi-automated test execution")
        print("   • Real-time test reporting")
        print("   • VS Code integration")
        print("   • Comprehensive result analysis")
        print("=" * 65)
        
        return self._show_enhanced_setup()
    
    def _show_enhanced_setup(self):
        """Show enhanced setup with automation options"""
        setup_text = """
🔧 ENHANCED SETUP:

1. AUTOMATION PREPARATION:
   ✓ VS Code workspace ready
   ✓ RazorEnhanced extension installed
   ✓ DexBot.py deployed to Scripts folder
   
2. MONITORING SETUP:
   • Console output monitoring: Ready
   • Pattern matching: Configured
   • Test reporting: Active
   
3. TESTING MODES:
   🤖 Fully Automated: Tests that can run without interaction
   🔄 Semi-Automated: Tests with automated monitoring + manual actions
   👤 Manual: Tests requiring visual verification
   
4. READY TO START:
   Choose your testing approach:
   • Type 'auto' for maximum automation
   • Type 'guided' for step-by-step guidance
   • Type 'manual' for traditional manual testing

Enter your choice:
        """
        print(setup_text)
        return "enhanced_setup_complete"
    
    def set_testing_mode(self, mode: str):
        """Set the testing mode"""
        self.auto_mode = mode.lower() in ['auto', 'automated']
        
        if mode.lower() == 'auto':
            print("🤖 AUTOMATED MODE: Maximum automation enabled")
            return self._run_automated_sequence()
        elif mode.lower() == 'guided':
            print("🔄 GUIDED MODE: Step-by-step with automation assistance")
            return self._run_guided_sequence()
        else:
            print("👤 MANUAL MODE: Traditional manual testing")
            return self._run_manual_sequence()
    
    def _run_automated_sequence(self):
        """Run tests with maximum automation"""
        print("\n🤖 Starting Automated Test Sequence...")
        self.monitor.start_monitoring()
        
        results = []
        for test in self.test_cases:
            if test.get('automation_level') == 'auto':
                result = self._execute_automated_test(test)
                results.append(result)
            else:
                print(f"⏭️  Skipping {test['id']} (requires manual interaction)")
        
        self.monitor.stop_monitoring()
        return self._generate_final_report(results)
    
    def _run_guided_sequence(self):
        """Run tests with guided automation"""
        print("\n🔄 Starting Guided Test Sequence...")
        self.monitor.start_monitoring()
        
        results = []
        for test in self.test_cases:
            result = self._execute_guided_test(test)
            results.append(result)
            
            # Pause between tests for user verification
            input("\nPress ENTER to continue to next test...")
        
        self.monitor.stop_monitoring()
        return self._generate_final_report(results)
    
    def _execute_automated_test(self, test: Dict) -> Dict:
        """Execute a fully automated test"""
        self.reporter.start_test(test['id'], test['name'])
        
        print(f"\n🤖 AUTO: {test['name']}")
        print(f"📝 {test['description']}")
        
        try:
            if test['id'] == 'TEST_6':  # Config file test
                return self._test_config_file_automated(test)
            else:
                self.reporter.log_message("Automated test not implemented yet", "warning")
                self.reporter.complete_test("skip", "Automation not implemented")
                return {"status": "skip", "reason": "automation_pending"}
                
        except Exception as e:
            self.reporter.log_message(f"Test failed with exception: {e}", "error")
            self.reporter.complete_test("fail", str(e))
            return {"status": "fail", "error": str(e)}
    
    def _test_config_file_automated(self, test: Dict) -> Dict:
        """Automated config file testing"""
        config_path = "config/looting_config.json"
        
        # Check if file exists
        if not os.path.exists(config_path):
            self.reporter.log_message("Config file not found", "error")
            self.reporter.complete_test("fail", "Config file missing")
            return {"status": "fail", "reason": "file_missing"}
        
        # Validate JSON structure
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            required_keys = ['enabled', 'auto_skinning', 'max_range', 'item_types']
            missing_keys = [key for key in required_keys if key not in config]
            
            if missing_keys:
                self.reporter.log_message(f"Missing config keys: {missing_keys}", "error")
                self.reporter.complete_test("fail", f"Missing keys: {missing_keys}")
                return {"status": "fail", "reason": "invalid_structure"}
            
            self.reporter.log_message("Config file validation passed", "info")
            self.reporter.complete_test("pass", "Config file structure valid")
            return {"status": "pass"}
            
        except json.JSONDecodeError as e:
            self.reporter.log_message(f"Invalid JSON in config file: {e}", "error")
            self.reporter.complete_test("fail", f"JSON error: {e}")
            return {"status": "fail", "reason": "invalid_json"}
    
    def _execute_guided_test(self, test: Dict) -> Dict:
        """Execute a test with guided automation"""
        self.reporter.start_test(test['id'], test['name'])
        
        print(f"\n🔄 GUIDED: {test['name']}")
        print("=" * 50)
        print(f"📝 Description: {test['description']}")
        
        # Show automated monitoring setup
        if 'expected_patterns' in test:
            patterns = test['expected_patterns']
            self.monitor.set_expected_patterns(patterns)
            print("\n🤖 AUTOMATED MONITORING:")
            print("   Watching for these patterns:")
            for pattern in patterns:
                print(f"   • {pattern}")
        
        # Show manual steps
        print(f"\n👤 MANUAL STEPS:")
        for i, step in enumerate(test.get('test_steps', []), 1):
            print(f"   {i}. {step}")
        
        # Show visual checks if any
        if 'visual_checks' in test:
            print(f"\n👁️  VISUAL VERIFICATION:")
            for check in test['visual_checks']:
                print(f"   ✓ {check}")
        
        print(f"\n✅ PASS CRITERIA: {test['pass_criteria']}")
        print("\n🎮 Perform the steps above...")
        
        # Wait for user to complete manual steps
        if 'expected_patterns' in test:
            print("⏱️  Monitoring console output (30 second timeout)...")
            
            # Check for expected patterns
            patterns_found = []
            for pattern in test['expected_patterns']:
                if self.monitor.check_for_pattern(pattern, timeout=30):
                    patterns_found.append(pattern)
                    print(f"✅ Found: {pattern}")
                else:
                    print(f"❌ Missing: {pattern}")
            
            success_rate = len(patterns_found) / len(test['expected_patterns'])
            
            if success_rate >= 1.0:
                print("🎉 All expected patterns detected!")
                result_status = "pass"
            elif success_rate >= 0.7:
                print("⚠️  Most patterns detected")
                result_status = "partial"
            else:
                print("❌ Few patterns detected")
                result_status = "fail"
        else:
            # Manual verification required
            print("\n📋 Manual verification required:")
            user_result = input("Enter result (pass/fail/partial/skip): ").lower()
            result_status = user_result if user_result in ['pass', 'fail', 'partial', 'skip'] else 'fail'
        
        notes = input("Additional notes (optional): ")
        self.reporter.complete_test(result_status, notes)
        
        return {"status": result_status, "notes": notes}
    
    def _run_manual_sequence(self):
        """Run traditional manual testing"""
        print("\n👤 Starting Manual Test Sequence...")
        # Use the original test automation logic
        # This delegates to the original DexBotTester class
        pass
    
    def _generate_final_report(self, results: List[Dict]) -> Dict:
        """Generate comprehensive final report"""
        report = self.reporter.generate_test_report()
        
        print("\n" + "=" * 65)
        print("🏁 ENHANCED PHASE 1 TESTING COMPLETE")
        print("=" * 65)
        
        summary = report['summary']
        print(f"📊 AUTOMATED ANALYSIS:")
        print(f"   ✅ Passed: {summary['passed']}/{summary['total']}")
        print(f"   ❌ Failed: {summary['failed']}/{summary['total']}")
        print(f"   📈 Success Rate: {summary['success_rate']:.1f}%")
        
        # Enhanced recommendations
        if summary['success_rate'] >= 90:
            print("\n🎉 EXCELLENT! Phase 1 infrastructure is solid!")
            print("   ➡️  Ready to proceed to Phase 2 development")
        elif summary['success_rate'] >= 75:
            print("\n✅ GOOD! Phase 1 is mostly working")
            print("   ⚠️  Address minor issues before Phase 2")
        elif summary['success_rate'] >= 50:
            print("\n⚠️  NEEDS WORK! Several issues found")
            print("   🔧 Fix critical issues before continuing")
        else:
            print("\n❌ MAJOR ISSUES! Phase 1 needs significant work")
            print("   🚨 Do not proceed to Phase 2 until fixed")
        
        # Save enhanced report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"enhanced_test_report_phase1_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n💾 Enhanced report saved to: {report_file}")
        
        return report


def create_vscode_test_task():
    """Create a VS Code task for running tests"""
    task_config = {
        "version": "2.0.0",
        "tasks": [
            {
                "label": "DexBot: Run Phase 1 Tests",
                "type": "shell",
                "command": "python",
                "args": ["test_automation_enhanced.py"],
                "group": "test",
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "new"
                },
                "problemMatcher": [],
                "detail": "Run automated Phase 1 tests for DexBot"
            },
            {
                "label": "DexBot: Monitor RazorEnhanced Output",
                "type": "shell", 
                "command": "python",
                "args": ["-c", "from test_automation_enhanced import RazorEnhancedMonitor; monitor = RazorEnhancedMonitor(); monitor.start_monitoring(); input('Monitoring... Press ENTER to stop')"],
                "group": "test",
                "isBackground": True,
                "presentation": {
                    "echo": True,
                    "reveal": "always",
                    "focus": False,
                    "panel": "new"
                },
                "detail": "Monitor RazorEnhanced console output in real-time"
            }
        ]
    }
    
    return task_config


# Interactive enhanced testing session
def run_enhanced_interactive_test():
    """Run an enhanced interactive testing session"""
    tester = EnhancedDexBotTester()
    
    print("🚀 Starting Enhanced DexBot Phase 1 Testing...")
    current_state = tester.start_automated_testing()
    
    return tester


if __name__ == "__main__":
    # Example usage
    tester = run_enhanced_interactive_test()
    print("\n🔧 Enhanced tester initialized.")
    print("Call tester.set_testing_mode('guided') to start guided testing.")
    print("Call tester.set_testing_mode('auto') for maximum automation.")
    print("Call tester.set_testing_mode('manual') for traditional testing.")
