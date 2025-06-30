"""
DexBot Phase 1 Test Launcher
Quick launcher for test automation frameworks
"""

import sys
import os
import json
import glob
from datetime import datetime


def show_menu():
    """Show the test launcher menu"""
    print("🧪 DexBot Phase 1 Test Automation Launcher")
    print("=" * 50)
    print("Choose your testing approach:")
    print()
    print("1. 📋 Interactive Testing")
    print("   - Step-by-step guided testing")
    print("   - Manual execution with assistance")
    print("   - Best for thorough validation")
    print()
    print("2. 🤖 Enhanced Automated Testing")
    print("   - Semi-automated with monitoring")
    print("   - VS Code integration") 
    print("   - Multiple testing modes")
    print()
    print("3. 📊 Review Test Results")
    print("   - View previous test results")
    print("   - Analyze success rates")
    print()
    print("4. 🔧 Setup Help")
    print("   - Pre-testing setup guide")
    print("   - Troubleshooting tips")
    print()
    print("5. ❌ Exit")
    print()


def launch_interactive():
    """Launch interactive testing framework"""
    print("🚀 Launching Interactive Testing Framework...")
    try:
        from test_automation import run_interactive_test
        tester = run_interactive_test()
        
        print("\n🎮 Interactive Testing Session Started!")
        print("Call tester.next_test() to begin Test 1")
        print("Example workflow:")
        print("  >>> tester.next_test()  # Start first test")
        print("  >>> tester.record_result('TEST_1', 'pass', 'All good!')  # Record result")
        print("  >>> # Repeat for all tests...")
        
        return tester
        
    except ImportError as e:
        print(f"❌ Error importing test_automation: {e}")
        print("Ensure test_automation.py is in the current directory")
        return None


def launch_enhanced():
    """Launch enhanced automated testing framework"""
    print("🚀 Launching Enhanced Automated Testing Framework...")
    try:
        from test_automation_enhanced import run_enhanced_interactive_test
        tester = run_enhanced_interactive_test()
        
        print("\n🎮 Enhanced Testing Session Started!")
        print("Choose a testing mode:")
        print("  >>> tester.set_testing_mode('guided')  # Guided with automation")
        print("  >>> tester.set_testing_mode('auto')    # Maximum automation")
        print("  >>> tester.set_testing_mode('manual')  # Traditional manual")
        
        return tester
        
    except ImportError as e:
        print(f"❌ Error importing test_automation_enhanced: {e}")
        print("Ensure test_automation_enhanced.py is in the current directory")
        return None


def review_results():
    """Review previous test results"""
    print("📊 Reviewing Test Results...")
    
    # Find all test result files
    result_files = glob.glob("*test_results*.json") + glob.glob("*test_report*.json")
    
    if not result_files:
        print("❌ No test result files found")
        print("Run some tests first to generate results")
        return
    
    print(f"Found {len(result_files)} test result file(s):")
    print()
    
    for i, file in enumerate(sorted(result_files, reverse=True), 1):
        try:
            with open(file, 'r') as f:
                data = json.load(f)
            
            # Extract key info
            timestamp = data.get('timestamp', 0)
            if timestamp:
                date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            else:
                date_str = "Unknown date"
            
            summary = data.get('summary', {})
            success_rate = summary.get('success_rate', 0)
            total_tests = summary.get('total', len(data.get('results', {})))
            passed = summary.get('passed', 0)
            
            print(f"{i}. {file}")
            print(f"   📅 Date: {date_str}")
            print(f"   📈 Success Rate: {success_rate:.1f}%")
            print(f"   ✅ Passed: {passed}/{total_tests}")
            print()
            
        except Exception as e:
            print(f"{i}. {file} (Error reading: {e})")
            print()
    
    # Ask if user wants to view details
    try:
        choice = input("Enter file number to view details (or press ENTER to skip): ").strip()
        if choice and choice.isdigit():
            file_idx = int(choice) - 1
            if 0 <= file_idx < len(result_files):
                show_detailed_results(sorted(result_files, reverse=True)[file_idx])
    except (ValueError, KeyboardInterrupt):
        pass


def show_detailed_results(filename):
    """Show detailed results from a specific file"""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        print(f"\n📄 Detailed Results: {filename}")
        print("=" * 60)
        
        # Show summary
        summary = data.get('summary', {})
        print(f"📊 Summary:")
        print(f"   Total Tests: {summary.get('total', 'Unknown')}")
        print(f"   Passed: {summary.get('passed', 0)}")
        print(f"   Failed: {summary.get('failed', 0)}")
        print(f"   Partial: {summary.get('partial', 0)}")
        print(f"   Skipped: {summary.get('skipped', 0)}")
        print(f"   Success Rate: {summary.get('success_rate', 0):.1f}%")
        print()
        
        # Show individual test results
        results = data.get('results', {})
        if results:
            print("📝 Individual Test Results:")
            for test_id, result in results.items():
                status = result.get('result', 'unknown')
                status_icon = {"pass": "✅", "fail": "❌", "partial": "⚠️", "skip": "⏭️"}.get(status, "❓")
                print(f"   {status_icon} {test_id}: {status.upper()}")
                
                notes = result.get('notes', '')
                if notes:
                    print(f"      Notes: {notes}")
            print()
        
        # Show recommendations
        success_rate = summary.get('success_rate', 0)
        if success_rate >= 80:
            print("🎉 RECOMMENDATION: Ready for Phase 2 development!")
        elif success_rate >= 60:
            print("⚠️  RECOMMENDATION: Address issues before Phase 2")
        else:
            print("🔧 RECOMMENDATION: Major fixes needed before continuing")
            
    except Exception as e:
        print(f"❌ Error reading results file: {e}")


def show_setup_help():
    """Show setup help and troubleshooting"""
    help_text = """
🔧 DexBot Phase 1 Testing Setup Help
=====================================

📋 PRE-TESTING CHECKLIST:
✅ Phase 1 Looting System implementation complete
✅ dist/DexBot.py built successfully  
✅ RazorEnhanced client running
✅ Connected to UO server
✅ Character in safe location
✅ VS Code with RazorEnhanced extension (optional)

🚀 DEPLOYMENT STEPS:
1. Copy dist/DexBot.py to your RazorEnhanced Scripts folder
2. Start RazorEnhanced and connect to UO
3. Run DexBot script in RazorEnhanced
4. Verify GUMP appears and no startup errors

🐛 COMMON ISSUES:

❌ "No module named 'test_automation'"
   Solution: Ensure you're in the correct directory with test files

❌ "GUMP not appearing"
   Solution: Check script deployment and RazorEnhanced connection

❌ "No console output"
   Solution: Verify RazorEnhanced client is active and connected

❌ "Config file errors"  
   Solution: Check file permissions and JSON validity

❌ "Pattern matching fails"
   Solution: Verify exact console message formats

🔧 DEBUG MODE:
Enable debug logging in main_config.json:
{
  "debug_mode": true,
  "verbose_logging": true
}

📞 NEED MORE HELP?
- Check TEST_AUTOMATION_README.md
- Review Phase 1 test plan documentation
- Verify all Phase 1 requirements met

Press ENTER to return to main menu...
    """
    print(help_text)
    input()


def main():
    """Main launcher function"""
    tester = None
    
    while True:
        try:
            show_menu()
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == '1':
                tester = launch_interactive()
                if tester:
                    # Keep the tester object available
                    print(f"\n💡 Tester object stored as 'tester' variable")
                    print("You can now call tester methods to run tests")
                    break
                    
            elif choice == '2':
                tester = launch_enhanced()
                if tester:
                    print(f"\n💡 Enhanced tester object stored as 'tester' variable")
                    print("You can now call tester methods to run tests")
                    break
                    
            elif choice == '3':
                review_results()
                input("\nPress ENTER to continue...")
                
            elif choice == '4':
                show_setup_help()
                
            elif choice == '5':
                print("👋 Goodbye! Happy testing!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                input("Press ENTER to continue...")
                
        except KeyboardInterrupt:
            print("\n\n👋 Testing session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            input("Press ENTER to continue...")
    
    return tester


if __name__ == "__main__":
    # Run the launcher
    tester = main()
    
    # If we have a tester object, make it available for interactive use
    if tester:
        print("\n🎮 Test automation framework is ready!")
        print("The 'tester' object is available for interactive use.")
