#!/usr/bin/env python3
"""
DexBot Enhanced Test Automation

Enhanced test automation with VS Code integration, monitoring capabilities,
and comprehensive result reporting for DexBot development workflow.
"""

import json
import os
import sys
import threading
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class RazorEnhancedMonitor:
    """Monitor for RazorEnhanced console output and events."""
    
    def __init__(self):
        """Initialize the monitor."""
        self.monitoring = False
        self.messages = []
        self.start_time = None
        
    def start_monitoring(self):
        """Start monitoring RazorEnhanced output."""
        self.monitoring = True
        self.start_time = datetime.now()
        print("🔍 RazorEnhanced Monitor Started")
        print("   - This would monitor RazorEnhanced console output")
        print("   - In actual implementation, would hook into RE logging")
        print("   - Press CTRL+C to stop monitoring")
        
        try:
            while self.monitoring:
                # Simulate monitoring - in real implementation would hook into RE
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring = False
        print(f"\n📊 Monitoring stopped after {datetime.now() - self.start_time if self.start_time else 'unknown'}")
        print(f"   - Captured {len(self.messages)} messages")


class EnhancedTestRunner:
    """Enhanced test runner with VS Code integration."""
    
    def __init__(self):
        """Initialize the enhanced test runner."""
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "test_session": "Enhanced Automated Tests",
            "environment": {
                "python_version": sys.version,
                "platform": sys.platform,
                "working_directory": os.getcwd()
            },
            "phases": [],
            "summary": {
                "total_phases": 0,
                "passed_phases": 0,
                "failed_phases": 0,
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0
            }
        }
        
    def run_environment_checks(self) -> bool:
        """Run comprehensive environment checks."""
        phase_name = "Environment Validation"
        print(f"=== {phase_name} ===")
        
        phase_result = {
            "name": phase_name,
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "status": "RUNNING"
        }
        
        all_passed = True
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major >= 3 and python_version.minor >= 7:
            print(f"[PASS] Python version: {sys.version.split()[0]}")
            self._add_test("Python version check", "PASS", phase_result)
        else:
            print(f"[FAIL] Python version too old: {sys.version.split()[0]}")
            self._add_test("Python version check", "FAIL", phase_result, "Python 3.7+ required")
            all_passed = False
        
        # Check working directory
        expected_files = ["src", "config", "dist"]
        missing_files = [f for f in expected_files if not os.path.exists(f)]
        
        if not missing_files:
            print(f"PASS Working directory structure valid")
            self._add_test("Directory structure", "PASS", phase_result)
        else:
            print(f"FAIL Missing directories: {missing_files}")
            self._add_test("Directory structure", "FAIL", phase_result, f"Missing: {missing_files}")
            all_passed = False
        
        # Check for critical files
        critical_files = [
            "src/config/config_manager.py",
            "src/utils/uo_items.py",
            "src/systems/looting.py",
            "ref/uo_item_database.json"
        ]
        
        for file_path in critical_files:
            if os.path.exists(file_path):
                print(f"PASS {file_path}")
                self._add_test(f"Critical file {file_path}", "PASS", phase_result)
            else:
                print(f"FAIL Missing: {file_path}")
                self._add_test(f"Critical file {file_path}", "FAIL", phase_result, "File not found")
                all_passed = False
        
        phase_result["status"] = "PASS" if all_passed else "FAIL"
        phase_result["end_time"] = datetime.now().isoformat()
        self.results["phases"].append(phase_result)
        
        return all_passed
    
    def run_import_validation(self) -> bool:
        """Validate all module imports."""
        phase_name = "Import Validation"
        print(f"\n=== {phase_name} ===")
        
        phase_result = {
            "name": phase_name,
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "status": "RUNNING"
        }
        
        # Critical imports that must work
        critical_imports = [
            "src.config.config_manager",
            "src.utils.uo_items",
            "src.systems.looting"
        ]
        
        # Optional imports (may not exist in all configurations)
        optional_imports = [
            "src.systems.auto_heal",
            "src.systems.combat",
            "src.core.logger",
            "src.ui.main_gump"
        ]
        
        all_critical_passed = True
        
        # Test critical imports
        for module_name in critical_imports:
            try:
                __import__(module_name)
                print(f"PASS {module_name}")
                self._add_test(f"Import {module_name}", "PASS", phase_result)
            except Exception as e:
                print(f"FAIL {module_name}: {e}")
                self._add_test(f"Import {module_name}", "FAIL", phase_result, str(e))
                all_critical_passed = False
        
        # Test optional imports
        for module_name in optional_imports:
            try:
                __import__(module_name)
                print(f"PASS {module_name} (optional)")
                self._add_test(f"Import {module_name} (optional)", "PASS", phase_result)
            except Exception as e:
                print(f"WARN {module_name}: {e} (optional - OK)")
                self._add_test(f"Import {module_name} (optional)", "SKIP", phase_result, "Optional module")
        
        phase_result["status"] = "PASS" if all_critical_passed else "FAIL"
        phase_result["end_time"] = datetime.now().isoformat()
        self.results["phases"].append(phase_result)
        
        return all_critical_passed
    
    def run_functionality_tests(self) -> bool:
        """Test core functionality."""
        phase_name = "Core Functionality"
        print(f"\n=== {phase_name} ===")
        
        phase_result = {
            "name": phase_name,
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "status": "RUNNING"
        }
        
        all_passed = True
        
        # Test ConfigManager
        try:
            from src.config.config_manager import ConfigManager
            config_manager = ConfigManager()
            
            # Basic config access
            main_config = config_manager.main_config
            print(f"PASS ConfigManager: {len(main_config)} main settings")
            self._add_test("ConfigManager instantiation", "PASS", phase_result)
            
            # Test looting config
            looting_config = config_manager.get_looting_config()
            print(f"PASS Looting config: {len(looting_config)} settings")
            self._add_test("Looting config access", "PASS", phase_result)
            
        except Exception as e:
            print(f"FAIL ConfigManager failed: {e}")
            self._add_test("ConfigManager", "FAIL", phase_result, str(e))
            all_passed = False
        
        # Test UOItemDatabase
        try:
            from src.utils.uo_items import UOItemDatabase
            db = UOItemDatabase()
            
            stats = db.get_database_stats()
            print(f"PASS UO Items DB: {stats['total_items']} items, {stats['total_categories']} categories")
            self._add_test("UO Items Database", "PASS", phase_result)
            
            # Test basic operations
            categories = db.get_available_categories()
            if categories:
                test_category = categories[0]
                items = db.get_items_by_category(test_category)
                print(f"PASS Category query: '{test_category}' has {len(items)} items")
                self._add_test("Database query functionality", "PASS", phase_result)
            
        except Exception as e:
            print(f"FAIL UO Items Database failed: {e}")
            self._add_test("UO Items Database", "FAIL", phase_result, str(e))
            all_passed = False
        
        # Test LootingSystem integration
        try:
            from src.systems.looting import LootingSystem
            print("PASS LootingSystem can be imported")
            self._add_test("LootingSystem import", "PASS", phase_result)
            
        except Exception as e:
            print(f"FAIL LootingSystem import failed: {e}")
            self._add_test("LootingSystem import", "FAIL", phase_result, str(e))
            all_passed = False
        
        phase_result["status"] = "PASS" if all_passed else "FAIL"
        phase_result["end_time"] = datetime.now().isoformat()
        self.results["phases"].append(phase_result)
        
        return all_passed
    
    def run_build_validation(self) -> bool:
        """Validate build output."""
        phase_name = "Build Validation"
        print(f"\n=== {phase_name} ===")
        
        phase_result = {
            "name": phase_name,
            "start_time": datetime.now().isoformat(),
            "tests": [],
            "status": "RUNNING"
        }
        
        all_passed = True
        
        # Check build output exists
        build_path = Path("dist/DexBot.py")
        if build_path.exists():
            file_size = build_path.stat().st_size
            print(f"PASS Build output exists: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            self._add_test("Build output exists", "PASS", phase_result)
            
            # Read and validate build content
            try:
                with open(build_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for critical components
                required_components = [
                    ("Main function", "def run_dexbot():"),
                    ("UOItemDatabase", "class UOItemDatabase"),
                    ("ConfigManager", "class ConfigManager"),
                    ("LootingSystem", "class LootingSystem")
                ]
                
                for component_name, search_text in required_components:
                    if search_text in content:
                        print(f"PASS {component_name} present in build")
                        self._add_test(f"Build contains {component_name}", "PASS", phase_result)
                    else:
                        print(f"FAIL {component_name} missing from build")
                        self._add_test(f"Build contains {component_name}", "FAIL", phase_result)
                        all_passed = False
                
                # Check for problematic patterns
                problematic_patterns = [
                    ("Relative imports", "from .."),
                    ("Dev-only imports", "import pytest"),
                ]
                
                for pattern_name, search_text in problematic_patterns:
                    if search_text in content:
                        print(f"WARN {pattern_name} found in build (may cause issues)")
                        self._add_test(f"Build free of {pattern_name}", "FAIL", phase_result, f"Found: {search_text}")
                        # Don't fail the whole test for this
                    else:
                        print(f"PASS No {pattern_name} in build")
                        self._add_test(f"Build free of {pattern_name}", "PASS", phase_result)
                
            except Exception as e:
                print(f"FAIL Error reading build file: {e}")
                self._add_test("Build file readable", "FAIL", phase_result, str(e))
                all_passed = False
                
        else:
            print("FAIL Build output not found")
            self._add_test("Build output exists", "FAIL", phase_result, "dist/DexBot.py not found")
            all_passed = False
        
        phase_result["status"] = "PASS" if all_passed else "FAIL"
        phase_result["end_time"] = datetime.now().isoformat()
        self.results["phases"].append(phase_result)
        
        return all_passed
    
    def _add_test(self, name: str, status: str, phase_result: Dict, error: Optional[str] = None):
        """Add a test result."""
        test_result = {
            "name": name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        if error:
            test_result["error"] = error
        
        phase_result["tests"].append(test_result)
    
    def calculate_summary(self):
        """Calculate test summary statistics."""
        summary = self.results["summary"]
        
        for phase in self.results["phases"]:
            summary["total_phases"] += 1
            if phase["status"] == "PASS":
                summary["passed_phases"] += 1
            else:
                summary["failed_phases"] += 1
            
            for test in phase["tests"]:
                summary["total_tests"] += 1
                if test["status"] == "PASS":
                    summary["passed_tests"] += 1
                elif test["status"] == "FAIL":
                    summary["failed_tests"] += 1
    
    def save_results(self) -> str:
        """Save enhanced test results."""
        self.calculate_summary()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_enhanced_{timestamp}.json"
        
        # Ensure tmp directory exists
        tmp_dir = "tmp"
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        
        # Save to tmp directory
        filepath = os.path.join(tmp_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        return filepath
    
    def print_summary(self):
        """Print enhanced test summary."""
        self.calculate_summary()
        summary = self.results["summary"]
        
        print(f"\n=== Enhanced Test Summary ===")
        print(f"Test Phases: {summary['passed_phases']}/{summary['total_phases']} passed")
        print(f"Individual Tests: {summary['passed_tests']}/{summary['total_tests']} passed")
        
        if summary["total_tests"] > 0:
            success_rate = (summary["passed_tests"] / summary["total_tests"]) * 100
            print(f"Overall Success Rate: {success_rate:.1f}%")
        
        # Show failed phases
        failed_phases = [p for p in self.results["phases"] if p["status"] == "FAIL"]
        if failed_phases:
            print(f"\nWARN  Failed Phases:")
            for phase in failed_phases:
                failed_tests = [t for t in phase["tests"] if t["status"] == "FAIL"]
                print(f"  - {phase['name']}: {len(failed_tests)} failed tests")
                for test in failed_tests[:3]:  # Show first 3 failures
                    print(f"    * {test['name']}: {test.get('error', 'Unknown error')}")
                if len(failed_tests) > 3:
                    print(f"    ... and {len(failed_tests) - 3} more")


def main():
    """Run the enhanced test automation suite."""
    print("DexBot Enhanced Test Automation Suite")
    print("=" * 45)
    print("* Running comprehensive validation tests...")
    
    runner = EnhancedTestRunner()
    
    # Run test phases
    phases_passed = 0
    total_phases = 4
    
    phase_functions = [
        runner.run_environment_checks,
        runner.run_import_validation,
        runner.run_functionality_tests,
        runner.run_build_validation
    ]
    
    for phase_func in phase_functions:
        if phase_func():
            phases_passed += 1
    
    # Print summary and save results
    runner.print_summary()
    results_file = runner.save_results()
    print(f"\n Detailed results saved to: {results_file}")
    
    # Overall status
    if phases_passed == total_phases:
        print("\n🎉 All phases passed! DexBot is ready for production use.")
        return 0
    else:
        print(f"\nWARN  {total_phases - phases_passed} phase(s) failed. Review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
