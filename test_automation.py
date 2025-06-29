"""
Automated DexBot Phase 1 Testing Framework
Interactive testing assistant that guides through test cases while monitoring output
"""

import time
import json
import os
from typing import Dict, List, Optional


class DexBotTester:
    """Interactive testing framework for DexBot Phase 1"""
    
    def __init__(self):
        self.current_test = 0
        self.test_results = {}
        self.start_time = time.time()
        
        # Define test cases
        self.test_cases = [
            {
                "id": "TEST_1",
                "name": "System Startup and Integration",
                "description": "Verify looting system initializes properly",
                "steps": [
                    "Start DexBot script in RazorEnhanced",
                    "Observe console output during startup"
                ],
                "expected_messages": [
                    "[DexBot] Starting DexBot",
                    "[DexBot] Looting system: disabled",
                    "[DexBot] Bot is now active",
                    "[DexBot] Status GUMP created"
                ],
                "pass_criteria": "No startup errors, looting system message appears, GUMP shows"
            },
            {
                "id": "TEST_2", 
                "name": "GUMP Interface - Main GUMP Integration",
                "description": "Verify looting section appears in main GUMP",
                "steps": [
                    "Ensure DexBot GUMP is visible",
                    "Locate LOOTING section in main GUMP",
                    "Verify toggle and settings buttons present"
                ],
                "expected_visual": "LOOTING section with toggle (Button 60) and settings (Button 61)",
                "pass_criteria": "LOOTING section visible with proper buttons and tooltips"
            },
            {
                "id": "TEST_3",
                "name": "Looting System Toggle (Main GUMP)",
                "description": "Test enable/disable from main GUMP",
                "steps": [
                    "Click looting system toggle button (Button 60)",
                    "Observe console messages",
                    "Verify GUMP updates",
                    "Toggle again to disable"
                ],
                "expected_messages": [
                    "[DexBot] Looting system enabled via GUMP",
                    "[DexBot] Looting system disabled via GUMP"
                ],
                "pass_criteria": "Console messages appear, GUMP updates, no errors"
            },
            {
                "id": "TEST_4",
                "name": "Looting Settings GUMP",
                "description": "Test dedicated looting settings interface",
                "steps": [
                    "Click looting settings button (Button 61)",
                    "Verify Looting Settings GUMP opens",
                    "Check all sections are present"
                ],
                "expected_sections": [
                    "LOOTING SETTINGS title",
                    "LOOTING SYSTEM section",
                    "BEHAVIOR SETTINGS section", 
                    "CURRENT STATUS section",
                    "LOOT CONFIGURATION section"
                ],
                "pass_criteria": "Settings GUMP opens with all sections visible"
            },
            {
                "id": "TEST_5",
                "name": "Settings GUMP Controls",
                "description": "Test interactive controls in settings",
                "steps": [
                    "Open Looting Settings GUMP",
                    "Click Looting System toggle (Button 71)",
                    "Click Auto Skinning toggle (Button 72)",
                    "Click Back button (Button 70)"
                ],
                "expected_messages": [
                    "[DexBot] Looting system enabled/disabled via Looting Settings",
                    "[DexBot] Auto skinning enabled/disabled via Looting Settings"
                ],
                "pass_criteria": "All toggles work, messages appear, back button works"
            },
            {
                "id": "TEST_6",
                "name": "Configuration File Management", 
                "description": "Verify config file creation and persistence",
                "steps": [
                    "Check for config/looting_config.json",
                    "Toggle settings via GUMP",
                    "Verify file updates",
                    "Restart script and check persistence"
                ],
                "expected_file": "config/looting_config.json with valid JSON",
                "pass_criteria": "File created, updates on changes, persists after restart"
            },
            {
                "id": "TEST_7",
                "name": "Basic Corpse Detection",
                "description": "Test corpse scanning (detection only)",
                "steps": [
                    "Enable looting system",
                    "Kill creature within 2 tiles",
                    "Wait 1-2 seconds",
                    "Observe console output"
                ],
                "expected_messages": [
                    "Found X corpses in range",
                    "Processing corpse: Unknown Creature"
                ],
                "pass_criteria": "No errors, debug shows corpse detection"
            },
            {
                "id": "TEST_8", 
                "name": "Error Handling and Recovery",
                "description": "Verify graceful error handling",
                "steps": [
                    "Test with no corpses nearby",
                    "Test rapid button clicking", 
                    "Test multiple quick toggles",
                    "Move away from corpses"
                ],
                "expected_behavior": "No crashes, system continues normally",
                "pass_criteria": "No exceptions, bot continues operating"
            },
            {
                "id": "TEST_9",
                "name": "Integration with Existing Systems",
                "description": "Verify no interference with other systems",
                "steps": [
                    "Enable looting system",
                    "Test auto-heal (take damage, use healing)",
                    "Test combat system if enabled",
                    "Verify all systems work together"
                ],
                "expected_behavior": "All systems work normally together",
                "pass_criteria": "No conflicts, all systems functional"
            }
        ]
    
    def start_testing(self):
        """Start the interactive testing process"""
        print("🧪 DexBot Phase 1 Interactive Testing Framework")
        print("=" * 60)
        print(f"📋 Total Test Cases: {len(self.test_cases)}")
        print(f"🎯 Goal: Validate Phase 1 core infrastructure")
        print("=" * 60)
        
        return self._show_initial_setup()
    
    def _show_initial_setup(self):
        """Show initial setup instructions"""
        setup_instructions = """
🚀 SETUP INSTRUCTIONS:

1. DEPLOY SCRIPT:
   Copy dist/DexBot.py to your RazorEnhanced Scripts folder
   
2. GAME SETUP:
   - Connect RazorEnhanced to UO server
   - Character should be in-game and safe location
   - Optional: Enable debug mode in main_config.json
   
3. READY TO START:
   - Have RazorEnhanced client visible
   - Console output visible
   - Ready to interact with GUMP interface

📝 I'll guide you through each test step-by-step and monitor the results.
🔍 I'll watch for expected console messages and guide troubleshooting.
✅ We'll validate each test case before moving to the next.

Press ENTER when ready to start Test 1...
        """
        print(setup_instructions)
        return "setup_complete"
    
    def next_test(self):
        """Move to the next test case"""
        if self.current_test >= len(self.test_cases):
            return self._show_final_results()
        
        test = self.test_cases[self.current_test]
        self.current_test += 1
        
        return self._execute_test(test)
    
    def _execute_test(self, test: Dict):
        """Execute a specific test case"""
        print(f"\n🧪 {test['id']}: {test['name']}")
        print("=" * 50)
        print(f"📝 Description: {test['description']}")
        print()
        
        print("📋 STEPS TO PERFORM:")
        for i, step in enumerate(test['steps'], 1):
            print(f"   {i}. {step}")
        print()
        
        if 'expected_messages' in test:
            print("👀 WATCH FOR THESE CONSOLE MESSAGES:")
            for msg in test['expected_messages']:
                print(f"   ✓ {msg}")
            print()
        
        if 'expected_visual' in test:
            print(f"👁️  VISUAL CHECK: {test['expected_visual']}")
            print()
        
        if 'expected_sections' in test:
            print("🔍 VERIFY THESE SECTIONS:")
            for section in test['expected_sections']:
                print(f"   ✓ {section}")
            print()
        
        print(f"✅ PASS CRITERIA: {test['pass_criteria']}")
        print()
        print("🎮 Perform the steps above, then report the results:")
        print("   Type 'pass' if test succeeded")
        print("   Type 'fail' if test failed") 
        print("   Type 'partial' if partially working")
        print("   Type 'skip' to skip this test")
        
        return {
            "test_id": test['id'],
            "test_name": test['name'],
            "status": "waiting_for_input"
        }
    
    def record_result(self, test_id: str, result: str, notes: str = ""):
        """Record the result of a test"""
        self.test_results[test_id] = {
            "result": result.lower(),
            "notes": notes,
            "timestamp": time.time()
        }
        
        if result.lower() == "pass":
            print("✅ Test PASSED - Moving to next test")
        elif result.lower() == "fail":
            print("❌ Test FAILED - Continuing with next test")
        elif result.lower() == "partial":
            print("⚠️  Test PARTIALLY PASSED - Continuing with next test")
        else:
            print("⏭️  Test SKIPPED - Moving to next test")
        
        return self.next_test()
    
    def _show_final_results(self):
        """Show final testing results"""
        total_tests = len(self.test_cases)
        passed = sum(1 for r in self.test_results.values() if r['result'] == 'pass')
        failed = sum(1 for r in self.test_results.values() if r['result'] == 'fail')
        partial = sum(1 for r in self.test_results.values() if r['result'] == 'partial')
        skipped = sum(1 for r in self.test_results.values() if r['result'] == 'skip')
        
        print("\n" + "=" * 60)
        print("🏁 PHASE 1 TESTING COMPLETE")
        print("=" * 60)
        print(f"📊 RESULTS SUMMARY:")
        print(f"   ✅ Passed: {passed}/{total_tests}")
        print(f"   ❌ Failed: {failed}/{total_tests}")
        print(f"   ⚠️  Partial: {partial}/{total_tests}")
        print(f"   ⏭️  Skipped: {skipped}/{total_tests}")
        print()
        
        success_rate = (passed + partial * 0.5) / total_tests * 100
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🎉 PHASE 1 READY FOR PHASE 2!")
            print("   Core infrastructure is solid - proceed to Phase 2 development")
        elif success_rate >= 60:
            print("⚠️  PHASE 1 NEEDS MINOR FIXES")
            print("   Some issues found - fix before Phase 2")
        else:
            print("🔧 PHASE 1 NEEDS MAJOR FIXES") 
            print("   Significant issues found - major fixes needed")
        
        print("\n📝 DETAILED RESULTS:")
        for test in self.test_cases:
            test_id = test['id']
            if test_id in self.test_results:
                result = self.test_results[test_id]
                status_icon = {"pass": "✅", "fail": "❌", "partial": "⚠️", "skip": "⏭️"}[result['result']]
                print(f"   {status_icon} {test_id}: {test['name']} - {result['result'].upper()}")
                if result['notes']:
                    print(f"      Notes: {result['notes']}")
        
        # Save results to file
        results_file = f"test_results_phase1_{int(time.time())}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "phase": "Phase 1",
                "timestamp": time.time(),
                "total_tests": total_tests,
                "results": self.test_results,
                "summary": {
                    "passed": passed,
                    "failed": failed, 
                    "partial": partial,
                    "skipped": skipped,
                    "success_rate": success_rate
                }
            }, f, indent=2)
        
        print(f"\n💾 Results saved to: {results_file}")
        
        return {
            "status": "complete",
            "success_rate": success_rate,
            "ready_for_phase2": success_rate >= 80
        }


# Interactive testing session manager
def run_interactive_test():
    """Run an interactive testing session"""
    tester = DexBotTester()
    
    print("Starting DexBot Phase 1 Interactive Testing...")
    current_state = tester.start_testing()
    
    return tester

if __name__ == "__main__":
    # Example usage
    tester = run_interactive_test()
    print("\nTester initialized. Call tester.next_test() to start testing.")
