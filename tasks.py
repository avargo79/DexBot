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
            "src/systems/auto_heal.py",
            "src/systems/combat.py",
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
                out_f.write('Version: 2.1.0 (Infrastructure)\n')
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
def docs(c):
    """Update API documentation by crawling RazorEnhanced docs"""
    print("📚 Updating API documentation...")
    
    try:
        # Run the API documentation updater
        c.run("python scripts/update_api_docs.py")
        print("✅ API documentation updated successfully")
        print("📖 View at: docs/RazorEnhanced_API_Reference.md")
        
    except Exception as e:
        print(f"❌ Error updating API documentation: {e}")
        raise
