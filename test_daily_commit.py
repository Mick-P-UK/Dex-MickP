#!/usr/bin/env python3
"""
Test script for daily git commit automation
Run this to verify the daily commit script works correctly.
"""

import subprocess
import sys
from pathlib import Path

def test_daily_commit():
    """Test the daily commit script"""
    script_dir = Path(__file__).parent.absolute()
    daily_script = script_dir / "daily_git_commit.py"
    
    print("=" * 60)
    print("Testing Daily Git Commit Script")
    print("=" * 60)
    print()
    print(f"Script location: {daily_script}")
    print()
    
    # Check if script exists
    if not daily_script.exists():
        print("✗ ERROR: daily_git_commit.py not found!")
        return 1
    
    # Check if git repository exists
    git_dir = script_dir / ".git"
    if not git_dir.exists():
        print("⚠ WARNING: Git repository not initialized")
        print("  Run setup_git.py first")
        print()
    
    # Run the script
    print("Running daily commit script...")
    print("-" * 60)
    print()
    
    try:
        result = subprocess.run(
            [sys.executable, str(daily_script)],
            cwd=str(script_dir),
            text=True
        )
        
        print()
        print("-" * 60)
        
        if result.returncode == 0:
            print("✓ Test completed successfully!")
            print()
            print("The script is working correctly.")
            print("You can now set up the scheduled tasks.")
            return 0
        else:
            print("✗ Test completed with errors")
            print("Check the output above for details.")
            return 1
            
    except Exception as e:
        print(f"✗ Error running script: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(test_daily_commit())
