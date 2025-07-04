"""
Development tasks for DexBot - Python equivalent of npm scripts
Run with: python -m invoke <task_name>
"""

from invoke import task
import os
import shutil
import json
import subprocess
import glob
import time
import sys
from pprint import pformat
from pathlib import Path
from datetime import datetime

def get_version_info():
    """Read version information from version.txt file"""
    version_file = Path('version.txt')
    if not version_file.exists():
        return "UNKNOWN", "Development Version", "UNKNOWN"
    
    try:
        with open(version_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if line.startswith('#') or not line:
                    continue
                # Parse version line: VERSION|VERSION_NAME|BUILD_DATE
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        return parts[0].strip(), parts[1].strip(), parts[2].strip()
    except Exception as e:
        print(f"Warning: Could not read version.txt: {e}")
    
    return "UNKNOWN", "Development Version", "UNKNOWN"

def get_branch_info():
    """Get current git branch name for development context"""
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return "unknown-branch"

# Configuration
SRC_DIR = "src"
DIST_DIR = "dist"
MAIN_FILE = "DexBot.py"
BUNDLED_FILE = f"{DIST_DIR}/{MAIN_FILE}"
DEFAULT_MAIN_CONFIG_PATH = "src/config/default_main_config.json"
DEFAULT_AUTO_HEAL_CONFIG_PATH = "src/config/default_auto_heal_config.json"
DEFAULT_LOOTING_CONFIG_PATH = "src/config/default_looting_config.json"

# AI Validation Integration
def get_validation_integration():
    """Get AI validation integration if available."""
    try:
        # Import dynamically to avoid issues if validation not available
        sys.path.insert(0, os.path.abspath('.'))
        from src.utils.ai_integration import ValidationIntegration
        return ValidationIntegration()
    except ImportError:
        return None
    except Exception as e:
        print(f"Warning: AI validation not available: {e}")
        return None

def validate_task_context(task_name: str) -> bool:
    """Validate task execution context using AI validation system."""
    validation = get_validation_integration()
    if not validation:
        return True  # Proceed if validation not available
    
    print(f"[VALIDATION] Checking context for task '{task_name}'...")
    try:
        from src.utils.ai_integration import validate_invoke_context
        return validate_invoke_context()
    except Exception as e:
        print(f"[VALIDATION] Warning: {e}")
        return True  # Proceed on validation errors

@task
def clean(c):
    """Clean build artifacts and temporary files"""
    print("[CLEAN] Cleaning build artifacts...")
    
    # Remove dist directory
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
        print(f"   Removed {DIST_DIR}/ directory")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk("."):
        for dir_name in dirs[:]:  # Use slice to avoid modifying list during iteration
            if dir_name == "__pycache__":
                cache_path = os.path.join(root, dir_name)
                shutil.rmtree(cache_path)
                print(f"   Removed {cache_path}")
                dirs.remove(dir_name)
    
    # Clean runtime generated files in logs/ and reports/
    cleaned_count = 0
    for directory in ["logs", "reports"]:
        if os.path.exists(directory):
            print(f"[CLEAN] Cleaning {directory}/ directory...")
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                
                # Skip README.md files
                if filename == "README.md":
                    continue
                
                # Clean runtime generated files
                if filename.endswith(('.log', '.json', '.md', '.txt')):
                    try:
                        os.remove(file_path)
                        print(f"   Removed {file_path}")
                        cleaned_count += 1
                    except OSError as e:
                        print(f"   Warning: Could not remove {file_path}: {e}")
    
    if cleaned_count > 0:
        print(f"   Cleaned {cleaned_count} runtime files from logs/ and reports/")
    
    print("[SUCCESS] Clean completed")


@task
def deep_clean(c):
    """Deep clean including all runtime files and workspace organization"""
    print("[DEEP-CLEAN] Deep cleaning build artifacts, ALL runtime files, and organizing workspace...")
    
    # First run workspace organization
    organize(c)
    
    # Then run regular clean
    clean(c)
    
    # Deep clean logs/ and reports/ directories entirely
    cleaned_count = 0
    for directory in ["logs", "reports"]:
        if os.path.exists(directory):
            print(f"[CLEAN] Deep cleaning ALL files in {directory}/ directory...")
            
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                
                # Skip README.md files
                if filename == "README.md":
                    continue
                
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"   Removed {file_path}")
                        cleaned_count += 1
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"   Removed {file_path}/")
                        cleaned_count += 1
                except OSError as e:
                    print(f"   Warning: Could not remove {file_path}: {e}")
            
    if cleaned_count > 0:
        print(f"   Deep cleaned {cleaned_count} files from runtime directories")
    else:
        print(f"   No files found to clean in runtime directories")
    
    print("[SUCCESS] Deep clean completed")


@task
def lint(c):
    """Run basic syntax checks"""
    print("[SEARCH] Running syntax checks...")

    # Basic syntax check for main file (try bundled version first, then original)
    main_file_checked = False
    if os.path.exists(BUNDLED_FILE):
        try:
            c.run(f"python -m py_compile {BUNDLED_FILE}", hide=True)
            print(f"[SUCCESS] {BUNDLED_FILE} syntax check passed")
            main_file_checked = True
        except Exception as e:
            print(f"[ERROR] {BUNDLED_FILE} syntax check failed: {e}")
            return False
    elif os.path.exists(MAIN_FILE):
        try:
            c.run(f"python -m py_compile {MAIN_FILE}", hide=True)
            print(f"[SUCCESS] {MAIN_FILE} syntax check passed")
            main_file_checked = True
        except Exception as e:
            print(f"[ERROR] {MAIN_FILE} syntax check failed: {e}")
            return False
    
    if not main_file_checked:
        print(f"[WARNING]  Warning: Neither {BUNDLED_FILE} nor {MAIN_FILE} found for syntax check")

    # Check all Python files in src/
    if os.path.exists(SRC_DIR):
        for root, dirs, files in os.walk(SRC_DIR):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        c.run(f"python -m py_compile {file_path}", hide=True)
                        print(f"[SUCCESS] {file_path} syntax check passed")
                    except Exception as e:
                        print(f"[ERROR] {file_path} syntax check failed: {e}")
                        return False

    print("[SUCCESS] All syntax checks passed")
    return True

@task
def test(c):
    """Run core tests (unit tests with pytest)"""
    print("[EXPERIMENT] Running core tests...")
    
    # Check if we have pytest and unit tests
    has_pytest = False
    try:
        import pytest
        has_pytest = True
    except ImportError:
        pass
    
    # Run unit tests if available
    unit_tests = ["test_uo_items.py", "test_looting_system.py", "test_uo_item_database.py"]
    test_passed = True
    
    if has_pytest:
        for test_file in unit_tests:
            test_path = f"tests/{test_file}"
            if os.path.exists(test_path):
                try:
                    result = c.run(f"python -m pytest {test_path} -v", warn=True)
                    if result.ok:
                        print(f"[SUCCESS] {test_file} passed")
                    else:
                        print(f"[ERROR] {test_file} failed")
                        test_passed = False
                except Exception as e:
                    print(f"[ERROR] {test_file} execution failed: {e}")
                    test_passed = False
    else:
        print("ℹ️  pytest not available - running simple validation")
        # Simple validation that files exist
        for test_file in unit_tests:
            test_path = f"tests/{test_file}"
            if os.path.exists(test_path):
                print(f"[SUCCESS] {test_file} exists")
            else:
                print(f"[ERROR] {test_file} missing")
                test_passed = False
    
    if test_passed:
        print("[SUCCESS] Core tests completed successfully")
    else:
        print("[ERROR] Some core tests failed")
    
    return test_passed

@task
def bundle(c):
    """Bundle all source files into a single distribution file"""
    print("[PACKAGE] Bundling source files...")
    
    # Create dist directory
    os.makedirs(DIST_DIR, exist_ok=True)
    
    if os.path.exists(SRC_DIR):
        print("[TOOL] Bundling modular source files...")
        
        # Source files in dependency order
        source_files = [
            "src/config/config_manager.py",
            "src/core/bot_config.py", 
            "src/core/logger.py",
            "src/utils/helpers.py",
            "src/utils/uo_items.py",
            "src/systems/auto_heal.py",
            "src/systems/combat.py",
            "src/systems/looting.py",
            "src/ui/gump_interface.py",
            "src/core/main_loop.py"
        ]
        
        try:
            # Get version information
            version, version_name, build_date = get_version_info()
            branch = get_branch_info()
            
            with open(BUNDLED_FILE, 'w', encoding='utf-8') as out_f:
                # Write header
                out_f.write('"""\n')
                out_f.write('DexBot.py - Bundled Distribution Version\n')
                out_f.write('A modular bot system with Auto Heal as the first component.\n')
                out_f.write('\n')
                out_f.write('This file was automatically generated from modular source files.\n')
                out_f.write('Author: RugRat79\n')
                out_f.write(f'Version: {version} - {version_name}\n')
                out_f.write(f'Build Date: {build_date}\n')
                out_f.write(f'Branch: {branch}\n')
                out_f.write('License: MIT\n')
                out_f.write('"""\n\n')
                
                # Write imports that need to be at the top
                out_f.write('from AutoComplete import *\n')
                out_f.write('from typing import Dict, List, Optional, Union, Tuple\n')
                out_f.write('import time\n')
                out_f.write('import json\n')
                out_f.write('import os\n\n')
                
                # Write embedded version constants for bundled script
                version, version_name, build_date = get_version_info()
                branch = get_branch_info()
                out_f.write('# Embedded version information for bundled script\n')
                out_f.write(f'_BUNDLED_VERSION = "{version}"\n')
                out_f.write(f'_BUNDLED_VERSION_NAME = "{version_name}"\n')
                out_f.write(f'_BUNDLED_BUILD_DATE = "{build_date}"\n')
                out_f.write(f'_BUNDLED_BRANCH = "{branch}"\n\n')
                
                # Write RazorEnhanced imports
                out_f.write('# RazorEnhanced API imports\n')
                out_f.write('import Player\n')
                out_f.write('import Items\n')
                out_f.write('import Timer\n')
                out_f.write('import Journal\n')
                out_f.write('import Target\n')
                out_f.write('import Misc\n')
                out_f.write('import Gumps\n')
                out_f.write('import Mobiles\n\n')
                
                # Prepend default configs
                try:
                    with open(DEFAULT_MAIN_CONFIG_PATH, 'r', encoding='utf-8') as f:
                        main_config_json = json.load(f)
                        main_config_content = pformat(main_config_json, indent=2)
                        out_f.write(f'DEFAULT_MAIN_CONFIG = {main_config_content}\n\n')
                    with open(DEFAULT_AUTO_HEAL_CONFIG_PATH, 'r', encoding='utf-8') as f:
                        auto_heal_config_json = json.load(f)
                        auto_heal_config_content = pformat(auto_heal_config_json, indent=2)
                        out_f.write(f'DEFAULT_AUTO_HEAL_CONFIG = {auto_heal_config_content}\n\n')
                    with open(DEFAULT_LOOTING_CONFIG_PATH, 'r', encoding='utf-8') as f:
                        looting_config_json = json.load(f)
                        looting_config_content = pformat(looting_config_json, indent=2)
                        out_f.write(f'DEFAULT_LOOTING_CONFIG = {looting_config_content}\n\n')
                    print("  [PACKAGE] Added default configurations (as Python dicts)")
                except Exception as e:
                    print(f"  [WARNING]  Warning: Could not prepend default configs: {e}")
                
                # Process each source file
                for src_file in source_files:
                    if os.path.exists(src_file):
                        print(f"  📄 Adding {src_file}")
                        
                        with open(src_file, 'r', encoding='utf-8') as src_f:
                            content = src_f.read()
                            
                            # Remove module docstring and relative imports, but keep everything else
                            lines = content.split('\n')
                            processed_lines = []
                            in_docstring = False
                            docstring_removed = False
                            
                            for line in lines:
                                # Skip only the first docstring at the beginning
                                if not docstring_removed and line.strip().startswith('"""') and not in_docstring:
                                    in_docstring = True
                                    continue
                                elif not docstring_removed and line.strip().endswith('"""') and in_docstring:
                                    in_docstring = False
                                    docstring_removed = True
                                    continue
                                elif in_docstring:
                                    continue
                                
                                # Remove relative imports only
                                if line.strip().startswith('from ..'):
                                    continue
                                
                                # Keep everything else
                                processed_lines.append(line)
                            
                            # Write the processed content
                            out_f.write(f'# ===========================================\n')
                            out_f.write(f'# {src_file.upper()}\n')
                            out_f.write(f'# ===========================================\n\n')
                            out_f.write('\n'.join(processed_lines))
                            out_f.write('\n\n')
                    else:
                        print(f"  [WARNING]  Warning: {src_file} not found")
                
                # Write entry point
                out_f.write('# ===========================================\n')
                out_f.write('# SCRIPT ENTRY POINT\n')
                out_f.write('# ===========================================\n\n')
                out_f.write('if __name__ == "__main__":\n')
                out_f.write('    run_dexbot()\n')
            
            print(f"[SUCCESS] Bundled to {BUNDLED_FILE}")
            print(f"   [STATS] Size: {os.path.getsize(BUNDLED_FILE)} bytes")
            
        except Exception as e:
            print(f"[ERROR] Bundling failed: {e}")
            # Fall back to copying main file
            shutil.copy(MAIN_FILE, BUNDLED_FILE)
            print(f"   📄 Fell back to copying {MAIN_FILE}")
    else:
        print("📄 Copying monolithic file (src/ not yet created)...")
        shutil.copy(MAIN_FILE, BUNDLED_FILE)
        print(f"[SUCCESS] Copied {MAIN_FILE} to {BUNDLED_FILE}")
    
    print("[SUCCESS] Bundle completed")

@task(pre=[clean, lint, test])
def pipeline(c):
    """Full development pipeline: clean, lint, test, and build"""
    print("[BUILD]  Running full development pipeline...")
    bundle(c)
    print("🎉 Pipeline completed successfully!")
    print("[PACKAGE] Bundled script: dist/DexBot.py")

@task
def build(c):
    """Build the bundled DexBot.py file (without running tests)"""
    print("🔨 Building DexBot.py...")
    bundle(c)
    print("[SUCCESS] Build completed")
    print("[PACKAGE] Output: dist/DexBot.py")

@task
def dev(c):
    """Development mode - run tests and bundle for quick iteration"""
    print("[LAUNCH] Development mode...")
    if test(c) and lint(c):
        bundle(c)
        print("[SUCCESS] Development build ready")
    else:
        print("[ERROR] Development build failed")

@task
def info(c):
    """Show project information and structure"""
    print("[STATS] DexBot Project Information")
    print("=" * 50)
    
    # File sizes
    if os.path.exists(MAIN_FILE):
        size = os.path.getsize(MAIN_FILE)
        print(f"Main file: {MAIN_FILE} ({size:,} bytes)")
    
    if os.path.exists(BUNDLED_FILE):
        size = os.path.getsize(BUNDLED_FILE)
        print(f"Bundled file: {BUNDLED_FILE} ({size:,} bytes)")
    
    # Directory structure
    print("\nProject Structure:")
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        level = root.replace('.', '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            # Skip certain file types
            if not file.startswith('.') and not file.endswith('.pyc'):
                print(f"{subindent}{file}")

@task
def help(c):
    """Show all available development tasks and their descriptions"""
    print("🛠️  DexBot Development Tasks")
    print("=" * 50)
    
    tasks = [
        ("clean", "Clean build artifacts and runtime files"),
        ("deep_clean", "Deep clean including ALL runtime files and workspace organization"),
        ("organize", "Organize workspace by moving files to their proper directories (tests/, scripts/, reports/)"),
        ("lint", "Run basic syntax checks"),
        ("test", "Run all unit tests using pytest"),
        ("test-interactive", "Run Phase 1 interactive tests"),
        ("test-enhanced", "Run enhanced automated tests with comprehensive reporting"),
        ("test-monitor", "Start RazorEnhanced output monitoring for testing"),
        ("test-results", "List and display available test result files"),
        ("test-all", "Run all test suites (unit, interactive, enhanced)"),
        ("build", "Build the bundled DexBot.py file"),
        ("dev", "Run development version (source files)"),
        ("run", "Run the bundled DexBot.py file"),
        ("run-with-logging", "Run DexBot with comprehensive output logging to file"),
        ("validate", "Validate bundled script functionality"),
        ("deploy", "Deploy bundled script to RazorEnhanced directory"),
        ("pipeline", "Run complete development pipeline (clean, lint, test, build)"),
        ("quick", "Quick development cycle (lint, test, build - skip clean)"),
        ("watch", "Watch for file changes and auto-rebuild"),
        ("version", "Show current version information"),
        ("status", "Show development environment status"),
        ("release", "Prepare a release with version bump and validation"),
        ("info", "Show project information and structure"),
        ("extract-api-data", "Extract API data using Python script (TECH-001)"),
        ("analyze-journal-logs", "Analyze UO journal logs for DexBot activity and debugging"),
        ("help", "Show this help message")
    ]
    
    for task_name, description in tasks:
        print(f"  {task_name:<20} {description}")
    
    print("\n💡 Usage Examples:")
    print("  python -m invoke status        # Check development environment")
    print("  python -m invoke organize      # Clean up workspace organization")
    print("  python -m invoke quick         # Fast development cycle")
    print("  python -m invoke test-all      # Run all tests")
    print("  python -m invoke pipeline      # Full pipeline with tests")
    print("  python -m invoke run-with-logging  # Run with log file capture")
    print("  python -m invoke deploy        # Deploy to RazorEnhanced")
    print("  python -m invoke watch         # Auto-rebuild on changes")
    print("\n📄 Log Files:")
    print("  All log files are saved to logs/ directory with timestamps")
    print("  Example: logs/dexbot_run_20250101_120000.log")
    print("\n[DOCS] For more details, see docs/DEVELOPMENT_WORKFLOW.md")

@task
def generate_api_reference(c, format="all", input_path=None, output_path=None):
    """
    Generate API reference documentation in multiple formats (TECH-001)
    
    Args:
        format: Output format(s) - "all", "html", "markdown", "json", or comma-separated list
        input_path: Path to AutoComplete.json (default: ./config/AutoComplete.json)
        output_path: Output directory (default: ./ref/)
    """
    print("[TOOL] Generating API reference documentation (TECH-001)...")
    
    # Parse format argument
    if format == "all":
        formats = ["html", "markdown", "json"]
    else:
        formats = [f.strip() for f in format.split(",")]
    
    # Set default paths
    if input_path is None:
        input_path = "./config/AutoComplete.json"
    if output_path is None:
        output_path = "./ref/"
    
    # Build command
    cmd = [
        "python", "src/utils/autodoc.py",
        "--mode", "generate",
        "--input", input_path,
        "--output", output_path,
        "--formats"
    ] + formats
    
    print(f"  Input: {input_path}")
    print(f"  Output: {output_path}")
    print(f"  Formats: {', '.join(formats)}")
    
    result = c.run(" ".join(cmd), warn=True)
    
    if result.ok:
        print("[SUCCESS] API reference generation completed successfully")
    else:
        print("[ERROR] API reference generation failed")
        print(f"Error: {result.stderr}")

@task
def consolidate_api_references(c, output_path=None):
    """
    Consolidate existing API reference files (TECH-001)
    
    Args:
        output_path: Output directory (default: ./ref/)
    """
    print("[TOOL] Consolidating existing API references (TECH-001)...")
    
    if output_path is None:
        output_path = "./ref/"
    
    cmd = [
        "python", "src/utils/autodoc.py",
        "--mode", "consolidate",
        "--output", output_path
    ]
    
    print(f"  Output: {output_path}")
    
    result = c.run(" ".join(cmd), warn=True)
    
    if result.ok:
        print("[SUCCESS] API reference consolidation completed successfully")
        print("📄 Check ./ref/consolidated/ for consolidation report")
    else:
        print("[ERROR] API reference consolidation failed")
        print(f"Error: {result.stderr}")

@task
def validate_api_reference(c, input_path=None):
    """
    Validate API reference system integrity (TECH-001)
    
    Args:
        input_path: Path to AutoComplete.json (default: ./config/AutoComplete.json)
    """
    print("[TOOL] Validating API reference system (TECH-001)...")
    
    if input_path is None:
        input_path = "./config/AutoComplete.json"
    
    cmd = [
        "python", "src/utils/autodoc.py",
        "--mode", "validate",
        "--input", input_path
    ]
    
    print(f"  Input: {input_path}")
    
    result = c.run(" ".join(cmd), warn=True)
    
    if result.ok:
        print("[SUCCESS] API reference validation completed successfully")
    else:
        print("[ERROR] API reference validation failed")
        print(f"Error: {result.stderr}")

@task
def api_reference_workflow(c):
    """
    Complete API reference optimization workflow (TECH-001)
    
    This task runs the full workflow:
    1. Consolidate existing references
    2. Generate new documentation
    3. Validate the system
    """
    print("[LAUNCH] Starting complete API reference optimization workflow (TECH-001)...")
    
    # Step 1: Consolidate existing references
    print("\n[LIST] Step 1: Consolidating existing API references...")
    consolidate_api_references(c)
    
    # Step 2: Generate new documentation
    print("\n[DOCS] Step 2: Generating new API documentation...")
    generate_api_reference(c)
    
    # Step 3: Validate the system
    print("\n[SUCCESS] Step 3: Validating API reference system...")
    validate_api_reference(c)
    
    print("\n🎉 API reference optimization workflow completed!")
    print("📁 Check ./ref/ directory for generated documentation")

@task
def fetch_razor_api_data(c, razor_path=None, output_path=None):
    """
    Fetch AutoComplete.json from RazorEnhanced installation (TECH-001)
    
    This is a helper task to copy the AutoComplete.json file from a RazorEnhanced
    installation to the DexBot project for processing.
    
    Args:
        razor_path: Path to RazorEnhanced installation (default: auto-detect)
        output_path: Where to save AutoComplete.json (default: ./config/)
    """
    print("[TOOL] Fetching RazorEnhanced API data (TECH-001)...")
    
    import os
    from pathlib import Path
    
    # Auto-detect RazorEnhanced path if not provided
    if razor_path is None:
        common_paths = [
            "C:/Program Files (x86)/Ultima Online Unchained/Data/Plugins/RazorEnhanced/Config/",
            "C:/Program Files/Ultima Online Unchained/Data/Plugins/RazorEnhanced/Config/",
            "./Config/"  # Local development
        ]
        
        for path in common_paths:
            test_path = Path(path) / "AutoComplete.json"
            if test_path.exists():
                razor_path = path
                print(f"  Found RazorEnhanced at: {razor_path}")
                break
        
        if razor_path is None:
            print("[ERROR] Could not auto-detect RazorEnhanced installation")
            print("   Please specify --razor-path manually")
            return
    
    if output_path is None:
        output_path = "./config/"
    
    # Ensure output directory exists
    Path(output_path).mkdir(parents=True, exist_ok=True)
    
    # Copy the file
    source_file = Path(razor_path) / "AutoComplete.json"
    dest_file = Path(output_path) / "AutoComplete.json"
    
    if not source_file.exists():
        print(f"[ERROR] AutoComplete.json not found at: {source_file}")
        return
    
    try:
        import shutil
        shutil.copy2(source_file, dest_file)
        print(f"[SUCCESS] Copied AutoComplete.json to: {dest_file}")
        print(f"   File size: {dest_file.stat().st_size} bytes")
    except Exception as e:
        print(f"[ERROR] Failed to copy file: {str(e)}")

@task
def extract_api_data(c, input_path=None, output_path=None, verbose=False):
    """
    Extract API data using the Python extraction script (TECH-001)
    
    Args:
        input_path: Path to AutoComplete.json (default: auto-detect)
        output_path: Output directory (default: ./reports/api_extraction/)
        verbose: Enable verbose output
    """
    print("[TOOL] Extracting API data using Python script (TECH-001)...")
    
    # Build command
    cmd = ["python", "scripts/extract_razor_api_data.py"]
    
    if input_path:
        cmd.extend(["--input", input_path])
    if output_path:
        cmd.extend(["--output", output_path])
    if verbose:
        cmd.append("--verbose")
    
    print(f"  Command: {' '.join(cmd)}")
    
    result = c.run(" ".join(cmd), warn=True)
    
    if result.ok:
        print("[SUCCESS] API data extraction completed successfully")
        print("📄 Check the output directory for exported files")
    else:
        print("[ERROR] API data extraction failed")
        print(f"Error: {result.stderr}")

@task
def test_interactive(c):
    """Run Phase 1 interactive tests for DexBot core systems"""
    print("[EXPERIMENT] Running Phase 1 Interactive Tests...")
    
    result = c.run("python tests/test_automation.py", warn=True)
    
    if result.ok:
        print("[SUCCESS] Interactive tests completed successfully")
        # Check for test results file
        result_files = glob.glob("reports/*test_results*.json")
        if result_files:
            latest_result = max(result_files, key=os.path.getmtime)
            print(f"[STATS] Test results saved to: {latest_result}")
    else:
        print("[ERROR] Interactive tests failed")
        print(f"Error: {result.stderr}")

@task
def test_enhanced(c):
    """Run enhanced automated tests with comprehensive reporting"""
    print("[LAUNCH] Running Enhanced Automated Tests...")
    
    result = c.run("python tests/test_automation_enhanced.py", warn=True)
    
    if result.ok:
        print("[SUCCESS] Enhanced tests completed successfully")
        # Check for test results file
        result_files = glob.glob("reports/*test_results*.json")
        if result_files:
            latest_result = max(result_files, key=os.path.getmtime)
            print(f"[STATS] Test results saved to: {latest_result}")
    else:
        print("[ERROR] Enhanced tests failed")
        print(f"Error: {result.stderr}")

@task
def test_monitor(c):
    """Start RazorEnhanced output monitoring for testing"""
    print("[SEARCH] Starting RazorEnhanced Monitor...")
    print("   Press CTRL+C to stop monitoring")
    
    cmd = 'python -c "from tests.test_automation_enhanced import RazorEnhancedMonitor; monitor = RazorEnhancedMonitor(); monitor.start_monitoring()"'
    c.run(cmd, warn=True)

@task
def test_results(c):
    """List and display available test result files"""
    print("[LIST] Available Test Result Files:")
    
    result_files = glob.glob("reports/*test_results*.json")
    
    if not result_files:
        print("   No test result files found in reports/")
        return
    
    # Sort by modification time (newest first)
    result_files.sort(key=os.path.getmtime, reverse=True)
    
    for i, file_path in enumerate(result_files):
        file_stat = os.stat(file_path)
        file_time = file_stat.st_mtime
        file_size = file_stat.st_size
        
        print(f"   {i+1}. {os.path.basename(file_path)}")
        print(f"      Modified: {datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"      Size: {file_size} bytes")
        
        # Try to read summary from the most recent file
        if i == 0:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    if 'summary' in data:
                        summary = data['summary']
                        print(f"      Summary: {summary.get('passed', 0)}/{summary.get('total', 0)} tests passed")
            except Exception as e:
                print(f"      (Could not read summary: {e})")
        print()
    
    print(f"💡 Use VS Code to open and review the most recent results file: {os.path.basename(result_files[0])}")

@task
def test_all(c):
    """Run all test suites: unit tests, interactive tests, and enhanced tests"""
    print("[TARGET] Running Complete Test Suite...")
    
    success_count = 0
    total_tests = 3
    
    # Run unit tests
    print("\n1️⃣ Running Unit Tests...")
    result = c.run("python -m pytest tests/ -v", warn=True)
    if result.ok:
        print("[SUCCESS] Unit tests passed")
        success_count += 1
    else:
        print("[ERROR] Unit tests failed")
    
    # Run interactive tests
    print("\n2️⃣ Running Interactive Tests...")
    result = c.run("python tests/test_automation.py", warn=True)
    if result.ok:
        print("[SUCCESS] Interactive tests passed")
        success_count += 1
    else:
        print("[ERROR] Interactive tests failed")
    
    # Run enhanced tests
    print("\n3️⃣ Running Enhanced Tests...")
    result = c.run("python tests/test_automation_enhanced.py", warn=True)
    if result.ok:
        print("[SUCCESS] Enhanced tests passed")
        success_count += 1
    else:
        print("[ERROR] Enhanced tests failed")
    
    # Summary
    print(f"\n[STATS] Test Suite Summary: {success_count}/{total_tests} test suites passed")
    
    if success_count == total_tests:
        print("🎉 All test suites passed!")
        return True
    else:
        print("[WARNING]  Some test suites failed - check output above")
        return False

@task
def validate(c):
    """Validate bundled script functionality and integration"""
    print("[SEARCH] Validating bundled DexBot.py...")
    
    if not os.path.exists(BUNDLED_FILE):
        print("[ERROR] Bundled file not found. Run 'build' task first.")
        return False
    
    # Check for required components
    with open(BUNDLED_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_components = [
        'run_dexbot',
        'ConfigManager',
        'UOItemDatabase',
        'LootingSystem',
        'process_healing_journal'
    ]
    
    missing_components = []
    for component in required_components:
        if component not in content:
            missing_components.append(component)
    
    if missing_components:
        print(f"[ERROR] Missing components: {missing_components}")
        return False
    
    print("[SUCCESS] All required components present")
    print(f"[STATS] File size: {os.path.getsize(BUNDLED_FILE):,} bytes")
    return True

@task
def run(c):
    """Run the bundled DexBot.py file (for testing outside RazorEnhanced)"""
    print("[LAUNCH] Running bundled DexBot.py...")
    
    if not os.path.exists(BUNDLED_FILE):
        print("[ERROR] Bundled file not found. Run 'build' task first.")
        return False
    
    print("[WARNING]  Note: This will fail outside RazorEnhanced environment")
    result = c.run(f"python {BUNDLED_FILE}", warn=True)
    
    if result.ok:
        print("[SUCCESS] Script executed without syntax errors")
    else:
        print("[ERROR] Script execution failed (expected outside RazorEnhanced)")
    
    return result.ok

@task
def deploy(c, target_path=None):
    """Deploy bundled script to RazorEnhanced Scripts directory"""
    print("[LAUNCH] Deploying DexBot.py to RazorEnhanced...")
    
    if not os.path.exists(BUNDLED_FILE):
        print("[ERROR] Bundled file not found. Run 'build' task first.")
        return False
    
    # Auto-detect RazorEnhanced path if not provided
    if target_path is None:
        common_paths = [
            "C:/Program Files (x86)/Ultima Online Unchained/Data/Plugins/RazorEnhanced/Scripts/",
            "C:/Program Files/Ultima Online Unchained/Data/Plugins/RazorEnhanced/Scripts/",
            "../"  # If running from within Scripts directory
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                target_path = path
                break
        
        if target_path is None:
            print("[ERROR] Could not auto-detect RazorEnhanced Scripts directory")
            print("   Please specify --target-path manually")
            return False
    
    target_file = os.path.join(target_path, "DexBot.py")
    
    try:
        shutil.copy2(BUNDLED_FILE, target_file)
        print(f"[SUCCESS] Deployed to: {target_file}")
        print(f"   File size: {os.path.getsize(target_file):,} bytes")
        return True
    except Exception as e:
        print(f"[ERROR] Deployment failed: {e}")
        return False

@task
def version(c):
    """Show current version information"""
    version, version_name, build_date = get_version_info()
    branch = get_branch_info()
    
    print("[INFO] DexBot Version Information")
    print("=" * 40)
    print(f"Version: {version}")
    print(f"Name: {version_name}")
    print(f"Build Date: {build_date}")
    print(f"Branch: {branch}")

@task
def fix_unicode(c):
    """Fix Unicode emoji characters in task output for better compatibility"""
    print("[TOOL] Running Unicode fix utility...")
    
    # Check if the fix_unicode.py script exists
    script_path = os.path.join("tmp", "fix_unicode.py")
    if not os.path.exists(script_path):
        print("[ERROR] fix_unicode.py script not found. Run from system temp directory.")
        return False
    
    # Run the script
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    
    # Print output
    print(result.stdout)
    if result.stderr:
        print(f"[WARNING] Errors encountered: {result.stderr}")
    
    print("[SUCCESS] Unicode fix completed")
    return result.returncode == 0
    
    if os.path.exists(BUNDLED_FILE):
        size = os.path.getsize(BUNDLED_FILE)
        print(f"Bundled Size: {size:,} bytes ({size/1024:.1f} KB)")

@task
def status(c):
    """Show development environment status"""
    print("[STATS] DexBot Development Status")
    print("=" * 40)
    
    # Version info
    version, version_name, build_date = get_version_info()
    print(f"Version: {version} - {version_name}")
    
    # File status
    files_status = [
        ("Source directory", SRC_DIR, os.path.exists(SRC_DIR)),
        ("Bundled script", BUNDLED_FILE, os.path.exists(BUNDLED_FILE)),
        ("Version file", "version.txt", os.path.exists("version.txt")),
        ("Config directory", "config", os.path.exists("config")),
        ("Tests directory", "tests", os.path.exists("tests")),
    ]
    
    print("\nFile Status:")
    for name, path, exists in files_status:
        status_icon = "[SUCCESS]" if exists else "[ERROR]"
        print(f"  {status_icon} {name}: {path}")
    
    # Git status
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            print(f"\n[WARNING]  Git: {len(result.stdout.strip().split())} uncommitted changes")
        else:
            print("\n[SUCCESS] Git: Working directory clean")
    except:
        print("\n❓ Git: Status unknown")

@task
def quick(c):
    """Quick development cycle: lint, test, build (skip clean)"""
    print("⚡ Quick development cycle...")
    
    if not lint(c):
        print("[ERROR] Quick cycle failed at lint stage")
        return False
    
    if not test(c):
        print("[ERROR] Quick cycle failed at test stage") 
        return False
    
    bundle(c)
    print("[SUCCESS] Quick cycle completed successfully!")
    return True

@task
def watch(c):
    """Watch for file changes and auto-rebuild (requires watchdog)"""
    print("👀 Starting file watcher...")
    print("   Install watchdog: pip install watchdog")
    
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
    except ImportError:
        print("[ERROR] watchdog package not installed")
        print("   Run: pip install watchdog")
        return False
    
    class ChangeHandler(FileSystemEventHandler):
        def on_modified(self, event):
            if event.is_directory:
                return
            if event.src_path.endswith('.py'):
                print(f"[NOTE] File changed: {event.src_path}")
                print("[REFRESH] Auto-rebuilding...")
                quick(c)
    
    observer = Observer()
    observer.schedule(ChangeHandler(), SRC_DIR, recursive=True)
    observer.start()
    
    try:
        print("👀 Watching for changes... Press Ctrl+C to stop")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[SUCCESS] File watcher stopped")
    
    observer.join()

@task  
def release(c, version_bump="patch"):
    """Prepare a release: update version, build, validate, and tag"""
    print(f"[LAUNCH] Preparing release with {version_bump} version bump...")
    
    # This is a placeholder - you'd need to implement version bumping logic
    print("[WARNING]  Version bumping not yet implemented")
    print("   Manually update version.txt file")
    
    # Run full pipeline
    if not pipeline(c):
        print("[ERROR] Release preparation failed")
        return False
    
    # Validate
    if not validate(c):
        print("[ERROR] Release validation failed")
        return False
    
    print("[SUCCESS] Release preparation completed!")
    print("[LIST] Next steps:")
    print("   1. Review the bundled output")
    print("   2. Test in RazorEnhanced")
    print("   3. Commit and tag the release")
    print("   4. Deploy to production")

@task
def run_with_logging(c):
    """Run DexBot with comprehensive logging to file"""
    import datetime
    
    if not os.path.exists(BUNDLED_FILE):
        print(f"[ERROR] Bundled file not found: {BUNDLED_FILE}")
        print("Run 'python -m invoke build' first")
        return
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/dexbot_run_{timestamp}.log"
    
    # Ensure tmp directory exists
    os.makedirs("tmp", exist_ok=True)
    
    print("[LAUNCH] Running DexBot with Comprehensive Logging")
    print("=" * 50)
    print(f"📁 DexBot Script: {BUNDLED_FILE}")
    print(f"📄 Log Output: {log_file}")
    print(f"🕒 Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("💡 This will show output in console AND save to log file")
    print("   Press Ctrl+C to stop DexBot when testing is complete")
    print()
    
    try:
        # PowerShell command with Tee-Object for simultaneous console and file output
        cmd = f'python {BUNDLED_FILE} | Tee-Object -FilePath "{log_file}"'
        c.run(cmd)
    except KeyboardInterrupt:
        print("\n⏸️  DexBot execution stopped by user")
    except Exception as e:
        print(f"\n[ERROR] Error running DexBot: {e}")
    finally:
        if os.path.exists(log_file):
            file_size = os.path.getsize(log_file)
            print(f"\n[SUCCESS] Log file saved: {log_file}")
            print(f"[STATS] Log file size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            print(f"🕒 Completed: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"\n[WARNING]  Log file not created: {log_file}")

@task
def analyze_journal_logs(c):
    """Analyze Ultima Online journal logs for DexBot activity"""
    print("[SEARCH] Analyzing UO Journal Logs for DexBot Activity")
    print("=" * 50)
    
    # Check if the analyzer script exists
    analyzer_script = "reports/journal_log_analyzer.py"
    if not os.path.exists(analyzer_script):
        print(f"[ERROR] Journal log analyzer script not found: {analyzer_script}")
        print("   Run this task again to create the analyzer script")
        return
    
    try:
        # Run the journal log analyzer
        print("📂 Searching for journal logs in standard UO location...")
        c.run(f"python {analyzer_script}")
        
        print("\n💡 Analysis complete!")
        print("   Check logs/ and reports/ directories for generated reports and extracts")
        
    except Exception as e:
        print(f"[ERROR] Error running journal log analyzer: {e}")
        print("\n[TOOL] Manual usage:")
        print(f"   python {analyzer_script}")

@task
def organize(c):
    """Organize workspace by moving files to their proper directories"""
    print("[ORGANIZE] Organizing workspace structure...")
    
    moved_files = 0
    
    # Move test files from root to tests/
    test_files_to_move = []
    for filename in os.listdir("."):
        if filename.startswith("test_") and filename.endswith(".py"):
            test_files_to_move.append(filename)
    
    if test_files_to_move:
        os.makedirs("tests", exist_ok=True)
        for filename in test_files_to_move:
            target_path = os.path.join("tests", filename)
            if not os.path.exists(target_path):
                shutil.move(filename, target_path)
                print(f"   Moved {filename} -> tests/{filename}")
                moved_files += 1
            else:
                # Check if files are identical
                try:
                    with open(filename, 'r', encoding='utf-8') as f1:
                        content1 = f1.read()
                    with open(target_path, 'r', encoding='utf-8') as f2:
                        content2 = f2.read()
                    
                    if content1 == content2:
                        os.remove(filename)
                        print(f"   Removed duplicate {filename} (identical to tests/{filename})")
                        moved_files += 1
                    else:
                        print(f"   [WARNING] {filename} differs from tests/{filename} - manual review needed")
                except Exception as e:
                    print(f"   [ERROR] Could not compare {filename}: {e}")
    
    # Move development scripts to scripts/
    script_files_to_move = []
    for filename in os.listdir("."):
        # Development and preparation scripts should go to scripts/
        should_move = (
            filename.startswith("prepare_") or
            filename.startswith("setup_") or 
            filename.startswith("deploy_") or
            (filename.endswith((".bat", ".ps1", ".sh")) and not filename.startswith("."))
        )
        if should_move and os.path.isfile(filename):
            script_files_to_move.append(filename)
    
    if script_files_to_move:
        os.makedirs("scripts", exist_ok=True)
        for filename in script_files_to_move:
            target_path = os.path.join("scripts", filename)
            if not os.path.exists(target_path):
                shutil.move(filename, target_path)
                print(f"   Moved {filename} -> scripts/{filename}")
                moved_files += 1

    # Move analysis scripts and reports to reports/ directory or remove if obsolete
    files_to_move = []
    for filename in os.listdir("."):
        # Analysis scripts should go to reports/ if still useful, otherwise skip (will be cleaned)
        should_move = (
            (filename.startswith("analyze_") or filename.startswith("compare_")) and filename.endswith(".py") and
            not filename.startswith("analyze_uo_items_performance")  # This one is already in tools/
        )
        if should_move:
            files_to_move.append(filename)
    
    if files_to_move:
        os.makedirs("reports", exist_ok=True)
        for filename in files_to_move:
            target_path = os.path.join("reports", filename)
            if not os.path.exists(target_path):
                shutil.move(filename, target_path)
                print(f"   Moved {filename} -> reports/{filename}")
                moved_files += 1
    
    # Report results
    if moved_files > 0:
        print(f"[SUCCESS] Organized {moved_files} files")
    else:
        print("[SUCCESS] Workspace is already organized")
    
    # Show current structure
    print("\n📁 Current workspace structure:")
    for root_item in sorted(os.listdir(".")):
        if os.path.isdir(root_item) and not root_item.startswith('.'):
            print(f"   📁 {root_item}/")
        elif root_item.endswith('.py') and root_item not in ['tasks.py']:
            print(f"   📄 {root_item}")

    print(f"[ORGANIZE] Organization complete. Moved {moved_files} files to their proper locations.")


@task
def ai_validate(c):
    """Run AI validation checks on current development context"""
    print("[AI-VALIDATE] Running AI validation checks...")
    
    validation = get_validation_integration()
    if not validation:
        print("   AI validation system not available")
        return
    
    try:
        from src.utils.ai_integration import check_workflow_compliance
        compliant = check_workflow_compliance()
        
        if compliant:
            print("✅ [AI-VALIDATE] All validation checks passed")
        else:
            print("❌ [AI-VALIDATE] Validation issues detected")
            
    except Exception as e:
        print(f"❌ [AI-VALIDATE] Validation error: {e}")


@task
def ai_check_command(c, command):
    """Check if a command is safe to execute using AI validation"""
    print(f"[AI-CHECK] Validating command: {command}")
    
    validation = get_validation_integration()
    if not validation:
        print("   AI validation system not available")
        return
    
    if validation.validate_command_safe(command):
        print("✅ Command is safe to execute")
    else:
        print("❌ Command validation failed")
        suggestions = validation.get_validation_suggestions(command)
        if suggestions:
            print("Suggestions:")
            for suggestion in suggestions:
                print(f"   • {suggestion}")


