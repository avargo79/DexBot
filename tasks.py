"""
Development tasks for DexBot - Python equivalent of npm scripts
Run with: python -m invoke <task_name>
"""

from invoke import task
import os
import shutil
import json
from pprint import pformat
from pathlib import Path

# Configuration
SRC_DIR = "src"
DIST_DIR = "dist"
MAIN_FILE = "DexBot.py"
BUNDLED_FILE = f"{DIST_DIR}/{MAIN_FILE}"
DEFAULT_MAIN_CONFIG_PATH = "src/config/default_main_config.json"
DEFAULT_AUTO_HEAL_CONFIG_PATH = "src/config/default_auto_heal_config.json"
DEFAULT_LOOTING_CONFIG_PATH = "src/config/default_looting_config.json"

@task
def clean(c):
    """Clean build artifacts and temporary files"""
    print("🧹 Cleaning build artifacts...")
    
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
    
    print("✅ Clean completed")

@task
def lint(c):
    """Run basic syntax checks"""
    print("🔍 Running syntax checks...")

    # Basic syntax check for main file (try bundled version first, then original)
    main_file_checked = False
    if os.path.exists(BUNDLED_FILE):
        try:
            c.run(f"python -m py_compile {BUNDLED_FILE}", hide=True)
            print(f"✅ {BUNDLED_FILE} syntax check passed")
            main_file_checked = True
        except Exception as e:
            print(f"❌ {BUNDLED_FILE} syntax check failed: {e}")
            return False
    elif os.path.exists(MAIN_FILE):
        try:
            c.run(f"python -m py_compile {MAIN_FILE}", hide=True)
            print(f"✅ {MAIN_FILE} syntax check passed")
            main_file_checked = True
        except Exception as e:
            print(f"❌ {MAIN_FILE} syntax check failed: {e}")
            return False
    
    if not main_file_checked:
        print(f"⚠️  Warning: Neither {BUNDLED_FILE} nor {MAIN_FILE} found for syntax check")

    # Check all Python files in src/
    if os.path.exists(SRC_DIR):
        for root, dirs, files in os.walk(SRC_DIR):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    try:
                        c.run(f"python -m py_compile {file_path}", hide=True)
                        print(f"✅ {file_path} syntax check passed")
                    except Exception as e:
                        print(f"❌ {file_path} syntax check failed: {e}")
                        return False

    print("✅ All syntax checks passed")
    return True

@task
def test(c):
    """Run tests"""
    print("🧪 Running tests...")
    
    # Run the main test file
    try:
        c.run("python test_dexbot.py", warn=True)
        print("✅ Main test file passed")
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False
    
    # Run tests in tests/ directory if it exists
    if os.path.exists("tests") and any(f.endswith(".py") for f in os.listdir("tests")):
        print("🧪 Running additional tests in tests/ directory...")
        for file in os.listdir("tests"):
            if file.endswith(".py") and file.startswith("test_"):
                try:
                    result = c.run(f"python tests/{file}", warn=True)
                    if result.ok:
                        print(f"✅ {file} passed")
                    else:
                        print(f"❌ {file} failed")
                        return False
                except Exception as e:
                    print(f"❌ {file} execution failed: {e}")
                    return False
    
    return True

@task
def bundle(c):
    """Bundle all source files into a single distribution file"""
    print("📦 Bundling source files...")
    
    # Create dist directory
    os.makedirs(DIST_DIR, exist_ok=True)
    
    if os.path.exists(SRC_DIR):
        print("🔧 Bundling modular source files...")
        
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
            with open(BUNDLED_FILE, 'w', encoding='utf-8') as out_f:
                # Write header
                out_f.write('"""\n')
                out_f.write('DexBot.py - Bundled Distribution Version\n')
                out_f.write('A modular bot system with Auto Heal as the first component.\n')
                out_f.write('\n')
                out_f.write('This file was automatically generated from modular source files.\n')
                out_f.write('Author: RugRat79\n')
                out_f.write('Version: 3.1.1 - Ignore List Optimization\n')
                out_f.write('License: MIT\n')
                out_f.write('"""\n\n')
                
                # Write imports that need to be at the top
                out_f.write('from AutoComplete import *\n')
                out_f.write('from typing import Dict, List, Optional, Union, Tuple\n')
                out_f.write('import time\n')
                out_f.write('import json\n')
                out_f.write('import os\n\n')
                
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
                    print("  📦 Added default configurations (as Python dicts)")
                except Exception as e:
                    print(f"  ⚠️  Warning: Could not prepend default configs: {e}")
                
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
                        print(f"  ⚠️  Warning: {src_file} not found")
                
                # Write entry point
                out_f.write('# ===========================================\n')
                out_f.write('# SCRIPT ENTRY POINT\n')
                out_f.write('# ===========================================\n\n')
                out_f.write('if __name__ == "__main__":\n')
                out_f.write('    run_dexbot()\n')
            
            print(f"✅ Bundled to {BUNDLED_FILE}")
            print(f"   📊 Size: {os.path.getsize(BUNDLED_FILE)} bytes")
            
        except Exception as e:
            print(f"❌ Bundling failed: {e}")
            # Fall back to copying main file
            shutil.copy(MAIN_FILE, BUNDLED_FILE)
            print(f"   📄 Fell back to copying {MAIN_FILE}")
    else:
        print("📄 Copying monolithic file (src/ not yet created)...")
        shutil.copy(MAIN_FILE, BUNDLED_FILE)
        print(f"✅ Copied {MAIN_FILE} to {BUNDLED_FILE}")
    
    print("✅ Bundle completed")

@task(pre=[clean, lint, test])
def build(c):
    """Full build pipeline: clean, lint, test, and bundle"""
    print("🏗️  Running full build pipeline...")
    bundle(c)
    print("🎉 Build completed successfully!")
    print("📦 Bundled script: dist/DexBot.py")

@task
def dev(c):
    """Development mode - run tests and bundle for quick iteration"""
    print("🚀 Development mode...")
    if test(c) and lint(c):
        bundle(c)
        print("✅ Development build ready")
    else:
        print("❌ Development build failed")

@task
def info(c):
    """Show project information and structure"""
    print("📊 DexBot Project Information")
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
    """Show available tasks and their descriptions"""
    print("🚀 DexBot Development Tasks")
    print("=" * 50)
    print("clean    - Clean build artifacts and temporary files")
    print("lint     - Run basic syntax checks")
    print("test     - Run tests")
    print("bundle   - Bundle source files into single distribution file")
    print("build    - Full build pipeline (clean + lint + test + bundle)")
    print("dev      - Development mode (test + lint + bundle)")
    print("info     - Show project information and structure")
    print("help     - Show this help message")
    print("\nUsage: python -m invoke <task_name>")
    print("Example: python -m invoke build")

@task
def generate_api_reference(c, format="all", input_path=None, output_path=None):
    """
    Generate API reference documentation in multiple formats (TECH-001)
    
    Args:
        format: Output format(s) - "all", "html", "markdown", "json", or comma-separated list
        input_path: Path to AutoComplete.json (default: ./config/AutoComplete.json)
        output_path: Output directory (default: ./ref/)
    """
    print("🔧 Generating API reference documentation (TECH-001)...")
    
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
        print("✅ API reference generation completed successfully")
    else:
        print("❌ API reference generation failed")
        print(f"Error: {result.stderr}")

@task
def consolidate_api_references(c, output_path=None):
    """
    Consolidate existing API reference files (TECH-001)
    
    Args:
        output_path: Output directory (default: ./ref/)
    """
    print("🔧 Consolidating existing API references (TECH-001)...")
    
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
        print("✅ API reference consolidation completed successfully")
        print("📄 Check ./ref/consolidated/ for consolidation report")
    else:
        print("❌ API reference consolidation failed")
        print(f"Error: {result.stderr}")

@task
def validate_api_reference(c, input_path=None):
    """
    Validate API reference system integrity (TECH-001)
    
    Args:
        input_path: Path to AutoComplete.json (default: ./config/AutoComplete.json)
    """
    print("🔧 Validating API reference system (TECH-001)...")
    
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
        print("✅ API reference validation completed successfully")
    else:
        print("❌ API reference validation failed")
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
    print("🚀 Starting complete API reference optimization workflow (TECH-001)...")
    
    # Step 1: Consolidate existing references
    print("\n📋 Step 1: Consolidating existing API references...")
    consolidate_api_references(c)
    
    # Step 2: Generate new documentation
    print("\n📚 Step 2: Generating new API documentation...")
    generate_api_reference(c)
    
    # Step 3: Validate the system
    print("\n✅ Step 3: Validating API reference system...")
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
    print("🔧 Fetching RazorEnhanced API data (TECH-001)...")
    
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
            print("❌ Could not auto-detect RazorEnhanced installation")
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
        print(f"❌ AutoComplete.json not found at: {source_file}")
        return
    
    try:
        import shutil
        shutil.copy2(source_file, dest_file)
        print(f"✅ Copied AutoComplete.json to: {dest_file}")
        print(f"   File size: {dest_file.stat().st_size} bytes")
    except Exception as e:
        print(f"❌ Failed to copy file: {str(e)}")

@task
def extract_api_data(c, input_path=None, output_path=None, verbose=False):
    """
    Extract API data using the Python extraction script (TECH-001)
    
    Args:
        input_path: Path to AutoComplete.json (default: auto-detect)
        output_path: Output directory (default: ./tmp/api_extraction/)
        verbose: Enable verbose output
    """
    print("🔧 Extracting API data using Python script (TECH-001)...")
    
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
        print("✅ API data extraction completed successfully")
        print("📄 Check the output directory for exported files")
    else:
        print("❌ API data extraction failed")
        print(f"Error: {result.stderr}")


