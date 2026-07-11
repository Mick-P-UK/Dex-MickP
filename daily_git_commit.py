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
import tempfile
from pathlib import Path
from datetime import datetime

def log_message(message):
    """Append a timestamped line to the daily commit log (_git-commit.log)."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_git-commit.log")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"Could not write to log: {e}")

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
        for f in config_files[:10]:
            message_parts.append(f"  - {f}")
        if len(config_files) > 10:
            message_parts.append(f"  ... and {len(config_files) - 10} more")
        message_parts.append("")
    
    if docs_files:
        message_parts.append("Documentation updates:")
        for f in docs_files[:10]:
            message_parts.append(f"  - {f}")
        if len(docs_files) > 10:
            message_parts.append(f"  ... and {len(docs_files) - 10} more")
        message_parts.append("")
    
    if other_files:
        message_parts.append("Other changes:")
        for f in other_files[:5]:
            message_parts.append(f"  - {f}")
        if len(other_files) > 5:
            message_parts.append(f"  ... and {len(other_files) - 5} more")
    
    return "\n".join(message_parts)

def count_unpushed():
    """Return the number of local commits not yet on the remote, or None if unknown."""
    result = run_command("git rev-list --count @{u}..HEAD", "Counting unpushed commits")
    if result and result.returncode == 0:
        try:
            return int(result.stdout.strip())
        except ValueError:
            return None
    return None

def push_to_remote():
    """Push to the remote and report the outcome. Returns True on success."""
    print("Pushing to GitHub...", end=" ", flush=True)
    push_result = run_command("git push", "Pushing to remote")
    if push_result and push_result.returncode == 0:
        print("Done")
        log_message("Push succeeded")
        return True
    print("Failed")
    err = push_result.stderr.strip() if push_result else "unknown error"
    print(f"  Error: {err}")
    print("[WARNING] Push to GitHub failed - check authentication or network")
    log_message(f"Push FAILED: {err}")
    return False

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
        unpushed = count_unpushed()
        if unpushed and unpushed > 0:
            print(f"However {unpushed} earlier commit(s) have not reached GitHub - pushing now...")
            log_message(f"No new changes; {unpushed} unpushed commit(s) found - attempting catch-up push")
            push_to_remote()
        else:
            log_message("No changes to commit; nothing to push")
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
    
    # Commit. Write the message to a temp file and use -F so a large file
    # list can never exceed the Windows ~8191-char command-line limit.
    print("Creating commit...", end=" ", flush=True)
    msg_file = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".gitmsg", delete=False,
                                         encoding="utf-8", newline="\n") as _mf:
            _mf.write(commit_message)
            msg_file = _mf.name
        result = run_command(
            f'git commit -F "{msg_file}"',
            "Creating commit"
        )
    finally:
        if msg_file and os.path.exists(msg_file):
            try:
                os.remove(msg_file)
            except OSError:
                pass
    
    if result and result.returncode == 0:
        print("Done")
        print(f"  {result.stdout.strip()}")
        print()
        log_message(f"Committed {len(changed_files)} change(s)")

        # Push to remote (GitHub) - this sends the new commit plus any earlier unpushed ones
        if push_to_remote():
            print("[SUCCESS] Daily commit and push completed successfully")
            return 0
        else:
            print("[WARNING] Commit created locally but push to GitHub failed")
            print("  It will be retried automatically on the next run.")
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
