#!/usr/bin/env python3
"""
Git Repository Setup Script for Dex Customizations
This script initializes git and creates the initial commit.
"""

import subprocess
import os
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a git command and handle errors"""
    print(f"  {description}...", end=" ", flush=True)
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        if result.returncode == 0:
            print("✓")
            if result.stdout.strip():
                print(f"    {result.stdout.strip()}")
            return True
        else:
            print("✗")
            if result.stderr.strip():
                print(f"    Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"✗ (Exception: {e})")
        return False

def main():
    """Main setup function"""
    print("=" * 60)
    print("Git Repository Setup for Dex Customizations")
    print("=" * 60)
    print()
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print(f"Working directory: {script_dir}")
    print()
    
    # Check if git is available
    print("Checking git installation...", end=" ", flush=True)
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓")
            print(f"  {result.stdout.strip()}")
        else:
            print("✗")
            print("  Git is not installed or not in PATH.")
            print("  Please install Git from https://git-scm.com/")
            return 1
    except FileNotFoundError:
        print("✗")
        print("  Git is not installed or not in PATH.")
        print("  Please install Git from https://git-scm.com/")
        return 1
    
    print()
    
    # Check if .git already exists
    git_dir = script_dir / ".git"
    if git_dir.exists():
        print("⚠ Git repository already exists")
        response = input("  Continue anyway? (y/n): ").strip().lower()
        if response != 'y':
            print("  Aborted.")
            return 0
        print()
    
    # Initialize git repository
    if not run_command("git init", "Initializing git repository"):
        return 1
    
    print()
    
    # Stage all files
    if not run_command("git add .", "Staging files"):
        return 1
    
    print()
    
    # Create initial commit
    commit_message = """Initial commit: Dex setup with custom file naming convention

- Initial Dex system setup completed
- Custom file naming: YYYY.MM.DD-Filename.md format
- Code updated to dynamically find latest dated files
- Custom changes log created (CUSTOM_CHANGES.md)

Files renamed:
- DEX_Setup.md -> 2026.02.07-DEX_Setup.md
- Tasks.md -> 2026.02.07-Tasks.md
- Week_Priorities.md -> 2026.02.07-Week_Priorities.md

Code changes:
- Python: work_server.py, career_server.py (added find_latest_dated_file helper)
- TypeScript: data-layer.ts, index.ts, context/task.ts (added findLatestDatedFile helper)
- All code now automatically finds most recent dated file or falls back to original name"""
    
    print("Creating initial commit...", end=" ", flush=True)
    try:
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            capture_output=True,
            text=True,
            cwd=script_dir
        )
        if result.returncode == 0:
            print("✓")
            print(f"  {result.stdout.strip()}")
        else:
            print("✗")
            if "nothing to commit" in result.stdout:
                print("  Nothing to commit (all files may be ignored by .gitignore)")
            else:
                print(f"  Error: {result.stderr.strip()}")
            return 1
    except Exception as e:
        print(f"✗ (Exception: {e})")
        return 1
    
    print()
    print("=" * 60)
    print("✓ Git repository setup complete!")
    print("=" * 60)
    print()
    print("Useful commands:")
    print("  git status     - Check repository status")
    print("  git log        - View commit history")
    print("  git diff       - See what changed")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
