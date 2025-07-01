#!/usr/bin/env python
"""
DexBot New Feature Preparation Script

This script automates the process of preparing your workspace for new feature development.
It performs the following tasks:
1. Updates the main branch
2. Cleans up merged branches
3. Cleans temporary files and build artifacts
4. Runs validation and tests to ensure a clean slate
5. Creates a new feature branch (if requested)

Usage:
    python prepare_feature.py [feature_name] [options]

Example:
    python prepare_feature.py buff-management-system
    python prepare_feature.py buff-management-system --non-interactive
    python prepare_feature.py --skip-git --skip-validation
"""

import os
import sys
import subprocess
import shutil
import glob
import time
import argparse
from datetime import datetime

def get_yes_no_input(prompt, default=True, non_interactive=False):
    """
    Get a yes/no input from the user with a default value.
    
    Args:
        prompt: The prompt to display to the user
        default: True for yes, False for no
        non_interactive: If True, returns the default without prompting
        
    Returns:
        bool: True for yes, False for no
    """
    if non_interactive:
        return default
    
    # Determine the display prompt based on default
    yes_no = "[Y/n]" if default else "[y/N]"
    response = input(f"{prompt} {yes_no}: ").lower().strip()
    
    # If empty, use default
    if not response:
        return default
    
    # Otherwise check first letter
    return response.startswith('y')

def run_command(command, description=None, non_interactive=False):
    """Run a shell command and print its output"""
    if description:
        print(f"\n{'-' * 80}\n{description}\n{'-' * 80}")
    
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
        if non_interactive:
            print("Exiting due to command failure in non-interactive mode.")
            sys.exit(result.returncode)
        elif not get_yes_no_input("Continue anyway?", default=False, non_interactive=non_interactive):
            sys.exit(result.returncode)
    
    return result.returncode == 0

def clean_temp_files(non_interactive=False):
    """Clean temporary files and directories"""
    print("\n=== Cleaning Temporary Files ===")
    
    # Create timestamp for backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Clean tmp directory but preserve .gitkeep
    tmp_dir = "tmp"
    if os.path.exists(tmp_dir):
        # Check if there are important files to back up
        important_files = glob.glob(os.path.join(tmp_dir, "*COMPLETE*.md"))
        important_files += glob.glob(os.path.join(tmp_dir, "*SUMMARY*.md"))
        
        backup_files = False
        if important_files:
            backup_files = get_yes_no_input("Back up important summary files?", default=True, non_interactive=non_interactive)
        
        if important_files and backup_files:
            backup_dir = os.path.join(tmp_dir, f"backup_{timestamp}")
            os.makedirs(backup_dir, exist_ok=True)
            for file in important_files:
                shutil.copy2(file, backup_dir)
            print(f"Backed up {len(important_files)} files to {backup_dir}")
        
        # Remove all files except .gitkeep
        for item in os.listdir(tmp_dir):
            item_path = os.path.join(tmp_dir, item)
            if item != ".gitkeep" and item != f"backup_{timestamp}":
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    print(f"Removed: {item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Removed directory: {item_path}")
    
    # Clean dist directory but preserve .gitkeep
    dist_dir = "dist"
    if os.path.exists(dist_dir):
        for item in os.listdir(dist_dir):
            item_path = os.path.join(dist_dir, item)
            if item != ".gitkeep":
                if os.path.isfile(item_path):
                    os.remove(item_path)
                    print(f"Removed: {item_path}")
    
    # Clean Python cache files
    for root, dirs, files in os.walk("."):
        # Remove __pycache__ directories
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"Removed: {pycache_path}")
        
        # Remove .pyc and .pyo files
        for file in files:
            if file.endswith((".pyc", ".pyo")):
                os.remove(os.path.join(root, file))
                print(f"Removed: {os.path.join(root, file)}")

def prepare_git_workspace(non_interactive=False):
    """Prepare Git repository for new feature development"""
    print("\n=== Preparing Git Workspace ===")
    
    # Step 1: Switch to main branch
    run_command("git checkout main", "Switching to main branch", non_interactive)
    
    # Step 2: Update main branch
    run_command("git fetch origin", "Fetching latest changes", non_interactive)
    run_command("git pull origin main", "Pulling latest main branch", non_interactive)
    
    # Step 3: List and clean merged branches
    run_command("git branch --merged main", "Listing merged branches", non_interactive)
    
    clean_branches = get_yes_no_input("Clean up merged branches?", default=True, non_interactive=non_interactive)
    
    if clean_branches:
        # On Windows PowerShell, we need a different approach
        result = subprocess.run("git branch --merged main", shell=True, capture_output=True, text=True)
        merged_branches = result.stdout.strip().split('\n')
        for branch in merged_branches:
            branch = branch.strip()
            # Skip current branch and main
            if branch and not branch.startswith('*') and branch != 'main':
                run_command(f"git branch -d {branch}", f"Deleting merged branch: {branch}", non_interactive)
    
    # Step 4: Prune remote tracking branches
    run_command("git remote prune origin", "Pruning remote tracking branches", non_interactive)
    
    # Step 5: List remaining branches
    run_command("git branch -a", "Listing all remaining branches", non_interactive)

def validate_environment(non_interactive=False):
    """Run validation and tests to ensure clean environment"""
    print("\n=== Validating Environment ===")
    
    # Step 1: Run validation
    run_command("python -m invoke validate", "Running validation", non_interactive)
    
    # Step 2: Run tests
    run_tests = get_yes_no_input("Run test suite? (may take several minutes)", default=True, non_interactive=non_interactive)
    
    if run_tests:
        run_command("python -m invoke test", "Running tests", non_interactive)
    
    # Step 3: Verify build process
    verify_build = get_yes_no_input("Verify build process?", default=True, non_interactive=non_interactive)
    
    if verify_build:
        run_command("python -m invoke build", "Building bundle", non_interactive)

def create_feature_branch(feature_name, non_interactive=False):
    """Create and switch to a new feature branch"""
    if not feature_name:
        print("\nNo feature name provided. Skipping branch creation.")
        return
    
    branch_name = f"feature/{feature_name}"
    
    # Check if branch already exists
    result = subprocess.run(f"git branch --list {branch_name}", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print(f"\nBranch {branch_name} already exists.")
        
        switch_to_branch = get_yes_no_input(f"Switch to existing {branch_name}?", default=True, non_interactive=non_interactive)
        
        if switch_to_branch:
            run_command(f"git checkout {branch_name}", f"Switching to {branch_name}", non_interactive)
        return
    
    # Create new branch
    print(f"\n=== Creating New Feature Branch: {branch_name} ===")
    success = run_command(f"git checkout -b {branch_name}", f"Creating and switching to {branch_name}", non_interactive)
    
    if success:
        print(f"\nSuccessfully created and switched to {branch_name}")
        
        # Create feature planning document
        planning_doc = os.path.join("tmp", f"{feature_name.upper()}_PLANNING.md")
        
        create_planning_doc = get_yes_no_input(f"Create planning document at {planning_doc}?", default=True, non_interactive=non_interactive)
        
        if create_planning_doc:
            os.makedirs("tmp", exist_ok=True)
            with open(planning_doc, "w") as f:
                f.write(f"# {feature_name.replace('-', ' ').title()} Implementation Plan\n\n")
                f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d')}\n\n")
                f.write("## Requirements\n\n- \n\n")
                f.write("## Architecture\n\n- \n\n")
                f.write("## Implementation Steps\n\n1. \n\n")
                f.write("## Testing Strategy\n\n- \n\n")
                f.write("## Integration Points\n\n- \n\n")
            print(f"Created planning document: {planning_doc}")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="DexBot New Feature Preparation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python prepare_feature.py buff-management-system
  python prepare_feature.py buff-management-system --non-interactive
  python prepare_feature.py --skip-git --skip-validation
        """
    )
    
    parser.add_argument(
        "feature_name",
        nargs="?",
        default=None,
        help="Name of the feature to create (will create feature/[feature-name] branch)"
    )
    
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Run without any prompts or user interaction"
    )
    
    parser.add_argument(
        "--skip-git",
        action="store_true",
        help="Skip updating Git repository and branch management"
    )
    
    parser.add_argument(
        "--skip-cleanup",
        action="store_true",
        help="Skip cleaning temporary files and build artifacts"
    )
    
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip running validation and tests"
    )
    
    return parser.parse_args()

def main():
    """Main function to prepare for new feature development"""
    # Parse arguments
    args = parse_arguments()
    
    feature_name = args.feature_name
    non_interactive = args.non_interactive
    
    # If not provided in non-interactive mode, prompt for feature name
    if feature_name is None and not non_interactive:
        feature_name = input("Enter new feature name (or leave blank to skip branch creation): ").strip()
        # Convert spaces to hyphens and lowercase
        if feature_name:
            feature_name = feature_name.replace(" ", "-").lower()
    
    # Only confirm actions in interactive mode
    if not non_interactive:
        print("\nThe following actions will be performed:")
        if not args.skip_git:
            print("1. Update main branch from remote")
            print("2. Clean up merged branches")
        if not args.skip_cleanup:
            print("3. Clean temporary files and build artifacts")
        if not args.skip_validation:
            print("4. Run validation and tests")
        if feature_name:
            print(f"5. Create new feature branch: feature/{feature_name}")
        
        if not get_yes_no_input("\nContinue?", default=True, non_interactive=non_interactive):
            print("Aborted.")
            return
    
    # Start timer
    start_time = time.time()
    
    try:
        # Run preparation steps based on flags
        if not args.skip_git:
            prepare_git_workspace(non_interactive)
        
        if not args.skip_cleanup:
            clean_temp_files(non_interactive)
        
        if not args.skip_validation:
            validate_environment(non_interactive)
        
        if feature_name:
            create_feature_branch(feature_name, non_interactive)
        
        # Print summary
        elapsed_time = time.time() - start_time
        print(f"\n=== Preparation Complete ===")
        print(f"Total time: {elapsed_time:.1f} seconds")
        
        if feature_name:
            print(f"\nYou are now on branch: feature/{feature_name}")
            print("Next steps:")
            print("1. Review the PRD for this feature")
            print("2. Create default configuration")
            print("3. Implement the feature following DexBot coding standards")
            print("4. Run tests frequently")
        else:
            print("\nWorkspace prepared. Create a feature branch when ready.")
        
        print("\nHappy coding!")
    
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Workspace preparation incomplete.")
        sys.exit(1)

if __name__ == "__main__":
    main()
