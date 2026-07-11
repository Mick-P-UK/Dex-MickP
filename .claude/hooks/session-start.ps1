# Claude Code SessionStart Hook (PowerShell)
# Injects strategic hierarchy and tactical context
# For Dex personal knowledge system

# Verify CLAUDE_PROJECT_DIR is set
if (-not $env:CLAUDE_PROJECT_DIR) {
    Write-Host "=== Dex Session Context ==="
    Write-Host ""
    Write-Host "⚠️  ERROR: CLAUDE_PROJECT_DIR environment variable not set"
    Write-Host "Session log cannot be loaded. Please check hook configuration."
    Write-Host ""
    exit 1
}

$CLAUDE_DIR = $env:CLAUDE_PROJECT_DIR
$PILLARS_FILE = Join-Path $CLAUDE_DIR "System\pillars.yaml"
$QUARTER_GOALS = Join-Path $CLAUDE_DIR "01-Quarter_Goals\Quarter_Goals.md"
$WEEK_PRIORITIES = Join-Path $CLAUDE_DIR "00-Inbox\Weekly_Plans.md"
$TASKS_FILE = Join-Path $CLAUDE_DIR "03-Tasks\Tasks.md"
$LEARNINGS_DIR = Join-Path $CLAUDE_DIR "06-Resources\Learnings"
$MISTAKES_FILE = Join-Path $LEARNINGS_DIR "Mistake_Patterns.md"
$PREFERENCES_FILE = Join-Path $LEARNINGS_DIR "Working_Preferences.md"
$ONBOARDING_MARKER = Join-Path $CLAUDE_DIR "System\.onboarding-complete"
$SESSION_LOG = Join-Path $CLAUDE_DIR "System\session_log.md"

Write-Host "=== Dex Session Context ==="
Write-Host ""

# Session Log (Resume Context) - CRITICAL: Always output something
if (Test-Path $SESSION_LOG) {
    Write-Host "--- 📍 Where We Left Off ---"
    try {
        Get-Content $SESSION_LOG -ErrorAction Stop | Write-Host
        Write-Host "---"
        Write-Host ""
    } catch {
        Write-Host "⚠️  ERROR: Could not read session log file: $SESSION_LOG"
        Write-Host "File exists but cannot be read. Check permissions."
        Write-Host "---"
        Write-Host ""
    }
} else {
    # File doesn't exist - output diagnostic message
    Write-Host "--- 📍 Where We Left Off ---"
    Write-Host "ℹ️  Session log not found at: $SESSION_LOG"
    Write-Host "This is normal for first-time setup or if session log was cleared."
    Write-Host "---"
    Write-Host ""
}

# Skip background checks during onboarding - nothing to check yet!
if (-not (Test-Path $ONBOARDING_MARKER)) {
    Write-Host "⏩ Onboarding in progress - background checks disabled"
    Write-Host ""
}

# SELF-LEARNING: Run background checks inline (fallback if Launch Agents not installed)
# These are fast checks with interval throttling - only run when needed
if (Test-Path $ONBOARDING_MARKER) {
    # Check for Claude Code updates (if 24+ hours since last check)
    $changelogScript = Join-Path $CLAUDE_DIR ".scripts\check-anthropic-changelog.cjs"
    if (Test-Path $changelogScript) {
        Start-Process -FilePath "node" -ArgumentList "`"$changelogScript`"" -WindowStyle Hidden -ErrorAction SilentlyContinue | Out-Null
    }

    # Check for pending learnings (if not checked today)
    $learningScript = Join-Path $CLAUDE_DIR ".scripts\learning-review-prompt.sh"
    if (Test-Path $learningScript) {
        $LAST_LEARNING_CHECK = Join-Path $CLAUDE_DIR "System\.last-learning-check"
        $TODAY = Get-Date -Format "yyyy-MM-dd"
        
        $shouldRun = $false
        if (-not (Test-Path $LAST_LEARNING_CHECK)) {
            $shouldRun = $true
        } else {
            $lastCheck = Get-Content $LAST_LEARNING_CHECK -ErrorAction SilentlyContinue
            if ($lastCheck -ne $TODAY) {
                $shouldRun = $true
            }
        }
        
        if ($shouldRun) {
            # Try bash first (Git Bash), fallback to PowerShell if needed
            $bashPath = Get-Command bash -ErrorAction SilentlyContinue
            if ($bashPath) {
                Start-Process -FilePath "bash" -ArgumentList "`"$learningScript`"" -WindowStyle Hidden -ErrorAction SilentlyContinue | Out-Null
            }
            $TODAY | Out-File -FilePath $LAST_LEARNING_CHECK -Encoding utf8 -ErrorAction SilentlyContinue
        }
    }

    # Wait briefly for checks to complete (but don't block session start)
    Start-Sleep -Milliseconds 100
}

# OBSIDIAN SYNC DAEMON (if enabled) - Skip to avoid blocking
# Commented out for now to prevent hanging - can be re-enabled if needed
# $USER_PROFILE = Join-Path $CLAUDE_DIR "System\user-profile.yaml"
# if (Test-Path $USER_PROFILE) {
#     $content = Get-Content $USER_PROFILE -Raw -ErrorAction SilentlyContinue
#     $obsidianEnabled = $content -match "^\s*obsidian_mode:\s*true"
#     if ($obsidianEnabled) {
#         # Skip daemon check to avoid blocking
#     }
# }

Write-Host ""

# STRATEGIC HIERARCHY (Top-Down)

# 1. Strategic Pillars
if (Test-Path $PILLARS_FILE) {
    Write-Host "--- Strategic Pillars ---"
    # Extract pillar names and descriptions
    $content = Get-Content $PILLARS_FILE -Raw -ErrorAction SilentlyContinue
    if ($content) {
        $lines = $content -split "`n"
        $pillarCount = 0
        for ($i = 0; $i -lt $lines.Length - 2; $i++) {
            if ($lines[$i] -match '^\s+- id:') {
                $nameLine = $lines[$i + 1]
                $descLine = $lines[$i + 2]
                if ($nameLine -match '^\s+name:\s+"(.+)"') {
                    $name = $matches[1]
                    if ($descLine -match '^\s+description:\s+"(.+)"') {
                        $desc = $matches[1]
                        Write-Host "• $name — $desc"
                        $pillarCount++
                        if ($pillarCount -ge 5) { break }
                    }
                }
            }
        }
    }
    Write-Host "---"
    Write-Host ""
}

# 2. Quarterly Goals
if (Test-Path $QUARTER_GOALS) {
    # Check if goals are filled in (not template)
    $content = Get-Content $QUARTER_GOALS -Raw -ErrorAction SilentlyContinue
    if ($content -and $content -notmatch '\[Goal 1 Title\]') {
        Write-Host "--- Quarter Goals ---"
        $lines = Get-Content $QUARTER_GOALS -ErrorAction SilentlyContinue
        $inGoalSection = $false
        $outputCount = 0
        foreach ($line in $lines) {
            if ($line -match '^### [0-9]\.') {
                Write-Host $line
                $inGoalSection = $true
                $outputCount++
            } elseif ($inGoalSection -and $line -match '^\*\*Progress:\*\*') {
                Write-Host $line
                $outputCount++
            } elseif ($line -match '^---$') {
                $inGoalSection = $false
            }
            if ($outputCount -ge 10) { break }
        }
        Write-Host "---"
        Write-Host ""
    }
}

# 3. Weekly Priorities
if (Test-Path $WEEK_PRIORITIES) {
    # Extract current week's priorities section
    $lines = Get-Content $WEEK_PRIORITIES -ErrorAction SilentlyContinue
    $inWeekSection = $false
    $weekContent = @()
    foreach ($line in $lines) {
        if ($line -match '^## (🎯 )?This Week') {
            $inWeekSection = $true
        } elseif ($inWeekSection -and $line -match '^---$') {
            break
        } elseif ($inWeekSection -and $line.Trim() -ne '' -and $line -notmatch '^##') {
            $weekContent += $line
        }
    }
    if ($weekContent.Count -gt 0) {
        Write-Host "--- Weekly Priorities ---"
        $weekContent | Write-Host
        Write-Host "---"
        Write-Host ""
    }
}

# TACTICAL CONTEXT

# 4. Urgent Tasks
if (Test-Path $TASKS_FILE) {
    $lines = Get-Content $TASKS_FILE -ErrorAction SilentlyContinue
    $urgent = $lines | Where-Object {
        $_ -match '^- \[ \]' -and ($_ -match 'P0|urgent|today|overdue' -or $_ -match 'P0|urgent|today|overdue')
    } | Select-Object -First 3
    
    if ($urgent) {
        Write-Host "--- Urgent Tasks ---"
        $urgent | Write-Host
        Write-Host "---"
        Write-Host ""
    }
}

# 5. Working Preferences
if (Test-Path $PREFERENCES_FILE) {
    $lines = Get-Content $PREFERENCES_FILE -ErrorAction SilentlyContinue
    $prefCount = ($lines | Where-Object { $_ -match '^### ' }).Count
    if ($prefCount -gt 0) {
        Write-Host "--- Working Preferences ---"
        $outputCount = 0
        foreach ($line in $lines) {
            if ($line -match '^### ') {
                Write-Host $line
                $outputCount++
            } elseif ($outputCount -gt 0 -and $line.Trim() -ne '' -and $line -notmatch '^### ') {
                Write-Host $line
                $outputCount++
            }
            if ($outputCount -ge 10) { break }
        }
        Write-Host "---"
        Write-Host ""
    }
}

# 6. Active Mistake Patterns
if (Test-Path $MISTAKES_FILE) {
    $lines = Get-Content $MISTAKES_FILE -ErrorAction SilentlyContinue
    $patternCount = ($lines | Where-Object { $_ -match '^### ' }).Count
    if ($patternCount -gt 0) {
        Write-Host "--- Active Mistake Patterns ($patternCount) ---"
        $inActiveSection = $false
        $outputCount = 0
        foreach ($line in $lines) {
            if ($line -match '^## Active Patterns') {
                $inActiveSection = $true
            } elseif ($inActiveSection -and $line -match '^## Resolved') {
                break
            } elseif ($inActiveSection -and $line -match '^### ') {
                Write-Host $line
                $outputCount++
            } elseif ($inActiveSection -and $outputCount -gt 0 -and $line.Trim() -ne '' -and $line -notmatch '^---$') {
                Write-Host $line
                $outputCount++
            }
            if ($outputCount -ge 15) { break }
        }
        Write-Host "---"
        Write-Host ""
    }
}

# 7. Recent Learnings
if (Test-Path $LEARNINGS_DIR -PathType Container) {
    $foundLearnings = $false
    $files = Get-ChildItem -Path $LEARNINGS_DIR -Filter "*.md" -ErrorAction SilentlyContinue
    foreach ($file in $files) {
        $lines = Get-Content $file.FullName -ErrorAction SilentlyContinue
        $recent = $lines | Where-Object { $_ -match '## .+ — 202[0-9]-[0-9]{2}-[0-9]{2}' } | Select-Object -Last 2
        
        if ($recent) {
            if (-not $foundLearnings) {
                Write-Host "--- Recent Learnings ---"
                $foundLearnings = $true
            }
            Write-Host "[$($file.BaseName)]"
            $recent | Write-Host
        }
    }
    if ($foundLearnings) {
        Write-Host "---"
        Write-Host ""
    }
}

# 8. Pending Claude Code Updates
$CHANGELOG_PENDING = Join-Path $CLAUDE_DIR "System\changelog-updates-pending.md"
if (Test-Path $CHANGELOG_PENDING) {
    Write-Host "--- 🆕 Claude Code Updates Detected ---"
    Write-Host "New features or capabilities available!"
    Write-Host "Run: /dex-whats-new"
    Write-Host "---"
    Write-Host ""
}

# 9. Pending Learning Reviews
$LEARNING_PENDING = Join-Path $CLAUDE_DIR "System\learning-review-pending.md"
if (Test-Path $LEARNING_PENDING) {
    # Extract count from the file
    $lines = Get-Content $LEARNING_PENDING -ErrorAction SilentlyContinue
    $countLine = $lines | Where-Object { $_ -match '^\*\*Count:\*\*' } | Select-Object -First 1
    if ($countLine -match '\*\*Count:\*\*\s*(\d+)') {
        $LEARNING_COUNT = $matches[1]
        Write-Host "--- 📚 Pending Learnings Review ($LEARNING_COUNT) ---"
        Write-Host "Session learnings ready for review"
        Write-Host "Run: /dex-whats-new --learnings"
        Write-Host "---"
        Write-Host ""
    }
}

# 10. New Vault Welcome (if < 7 days old and Phase 2 not completed)
if (Test-Path $ONBOARDING_MARKER) {
    # Check if marker is less than 7 days old
    $markerFile = Get-Item $ONBOARDING_MARKER -ErrorAction SilentlyContinue
    if ($markerFile) {
        $age = (Get-Date) - $markerFile.LastWriteTime
        if ($age.Days -lt 7) {
            # Check if phase2_completed is false
            $content = Get-Content $ONBOARDING_MARKER -Raw -ErrorAction SilentlyContinue
            if ($content -and $content -notmatch '"phase2_completed":\s*true') {
                Write-Host "--- 👋 Welcome! ---"
                Write-Host "You're probably wondering what to do next..."
                Write-Host "Try: /getting-started"
                Write-Host "---"
                Write-Host ""
            }
        }
    }
}

Write-Host "=== End Session Context ==="
