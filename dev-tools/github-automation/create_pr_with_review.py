#!/usr/bin/env python3
"""
GitHub PR Creation Helper with Automatic Review Requests
Automates PR creation with copilot review request for DexBot workflow
"""

import subprocess
import sys
import argparse
from pathlib import Path

def create_pr_with_review(title, body_file=None, reviewer="copilot", base="main"):
    """
    Create a PR with automatic review request.
    
    Args:
        title: PR title
        body_file: Path to PR body file (optional)
        reviewer: GitHub username to request review from
        base: Base branch (default: main)
    """
    
    # Build the gh pr create command
    cmd = [
        "gh", "pr", "create",
        "--title", title,
        "--base", base
    ]
    
    # Add body file if provided
    if body_file and Path(body_file).exists():
        cmd.extend(["--body-file", body_file])
    
    try:
        # Create the PR
        print(f"Creating PR: {title}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Extract PR URL from output
        pr_url = result.stdout.strip()
        print(f"✅ PR created: {pr_url}")
        
        # Extract PR number from URL
        pr_number = pr_url.split('/')[-1]
        
        # Request review from copilot
        print(f"Requesting review from {reviewer}...")
        review_cmd = ["gh", "pr", "edit", pr_number, "--add-reviewer", reviewer]
        
        review_result = subprocess.run(review_cmd, capture_output=True, text=True)
        
        if review_result.returncode == 0:
            print(f"✅ Review requested from {reviewer}")
        else:
            print(f"⚠️  Could not request review from {reviewer}: {review_result.stderr}")
            print("Note: Make sure the reviewer has access to the repository")
        
        return pr_url
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating PR: {e.stderr}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Create PR with automatic review request")
    parser.add_argument("title", help="PR title")
    parser.add_argument("--body-file", help="Path to PR body file")
    parser.add_argument("--reviewer", default="copilot", help="GitHub username for review request")
    parser.add_argument("--base", default="main", help="Base branch")
    
    args = parser.parse_args()
    
    create_pr_with_review(
        title=args.title,
        body_file=args.body_file,
        reviewer=args.reviewer,
        base=args.base
    )

if __name__ == "__main__":
    main()
