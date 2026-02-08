#!/usr/bin/env python3
"""
Daily Git Commit Automation for Dex Customizations
Automatically commits changes to Dex system files daily.

This script:
1. Checks for changes to tracked files
2. Stages any changes
3. Creates a commit with timestamp
4. Updates CUSTOM_CHANGES.md if modified

Run this daily via Windows Task Scheduler or cron.
"""

import subprocess
import os
import sys
from pathlib import Path
from datetime import datetime

def run_command(cmd, description, capture_output=True):
    """Run a git command and return result"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        return result
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def check_git_status():
    """Check if there are any changes to commit"""
    result = run_command("git status --porcelain", "Checking git status")
    if result and result.returncode == 0:
        return result.stdout.strip()
    return None

def get_changed_files():
    """Get list of changed files"""
    status_output = check_git_status()
    if not status_output:
        return []
    
    files = []
    for line in status_output.split('\n'):
        if line.strip():
            # Git status format: " M file.py" or "?? newfile.py"
            status = line[:2].strip()
            filename = line[3:].strip()
            if status and filename:
                files.append((status, filename))
    return files

def create_commit_message(changed_files):
    """Create a descriptive commit message"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not changed_files:
        return None
    
    # Categorize changes
    code_files = []
    config_files = []
    docs_files = []
    other_files = []
    
    for status, filename in changed_files:
        if any(filename.endswith(ext) for ext in ['.py', '.ts', '.js']):
            code_files.append(filename)
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            config_files.append(filename)
        elif filename.endswith('.md'):
            docs_files.append(filename)
        else:
            other_files.append(filename)
    
    message_parts = [f"Daily commit: {timestamp}"]
    message_parts.append("")
    
    if code_files:
        message_parts.append("Code changes:")
        for f in code_files[:10]:  # Limit to 10 files
            message_parts.append(f"  - {f}")
        if len(code_files) > 10:
            message_parts.append(f"  ... and {len(code_files) - 10} more")
        message_parts.append("")
    
    if config_files:
        message_parts.append("Configuration changes:")
        for f in config_files:
            message_parts.append(f"  - {f}")
        message_parts.append("")
    
    if docs_files:
        message_parts.append("Documentation updates:")
        for f in docs_files:
            message_parts.append(f"  - {f}")
        message_parts.append("")
    
    if other_files:
        message_parts.append("Other changes:")
        for f in other_files[:5]:
            message_parts.append(f"  - {f}")
        if len(other_files) > 5:
            message_parts.append(f"  ... and {len(other_files) - 5} more")
    
    return "\n".join(message_parts)

def main():
    """Main automation function"""
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Daily Git Commit Check")
    print(f"Working directory: {script_dir}")
    print()
    
    # Check if git repository exists
    if not (script_dir / ".git").exists():
        print("[WARNING] Git repository not initialized. Run setup_git.py first.")
        return 1

    # Check for changes
    changed_files = get_changed_files()

    if not changed_files:
        print("[OK] No changes to commit")
        return 0
    
    print(f"Found {len(changed_files)} changed file(s):")
    for status, filename in changed_files[:10]:
        print(f"  {status} {filename}")
    if len(changed_files) > 10:
        print(f"  ... and {len(changed_files) - 10} more")
    print()
    
    # Stage changes
    print("Staging changes...", end=" ", flush=True)
    result = run_command("git add .", "Staging files")
    if result and result.returncode == 0:
        print("Done")
    else:
        print("Failed")
        if result:
            print(f"  Error: {result.stderr.strip()}")
        return 1
    
    # Create commit message
    commit_message = create_commit_message(changed_files)
    
    # Commit
    print("Creating commit...", end=" ", flush=True)
    result = run_command(
        f'git commit -m "{commit_message}"',
        "Creating commit"
    )
    
    if result and result.returncode == 0:
        print("Done")
        print(f"  {result.stdout.strip()}")
        print()

        # Push to remote (GitHub)
        print("Pushing to GitHub...", end=" ", flush=True)
        push_result = run_command("git push", "Pushing to remote")

        if push_result and push_result.returncode == 0:
            print("Done")
            print(f"  {push_result.stdout.strip() if push_result.stdout.strip() else 'Everything up-to-date'}")
            print()
            print("[SUCCESS] Daily commit and push completed successfully")
            return 0
        else:
            print("Failed")
            if push_result:
                print(f"  Error: {push_result.stderr.strip()}")
                print()
                print("[WARNING] Commit created locally but push to GitHub failed")
                print("  You may need to check your GitHub authentication or network connection")
            return 1
    else:
        print("Failed")
        if result:
            if "nothing to commit" in result.stdout:
                print("  Nothing to commit (files may be ignored)")
            else:
                print(f"  Error: {result.stderr.strip()}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
