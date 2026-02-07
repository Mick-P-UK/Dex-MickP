# PowerShell Script to Set Up Daily Git Commit Automation
# Creates two Windows Task Scheduler tasks:
# 1. Runs at system startup (catches up on missed commits)
# 2. Runs daily at 9:00 PM

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setting Up Daily Git Commit Automation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptPath "daily_git_commit.py"

# Check if daily_git_commit.py exists
if (-not (Test-Path $pythonScript)) {
    Write-Host "ERROR: daily_git_commit.py not found at: $pythonScript" -ForegroundColor Red
    exit 1
}

Write-Host "Script location: $pythonScript" -ForegroundColor Gray
Write-Host ""

# Find Python executable
$pythonExe = $null
$pythonCommands = @("python", "py", "python3")

foreach ($cmd in $pythonCommands) {
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonExe = $cmd
            Write-Host "Found Python: $cmd" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

if (-not $pythonExe) {
    Write-Host "ERROR: Python not found. Please install Python or add it to PATH." -ForegroundColor Red
    Write-Host "Tried: $($pythonCommands -join ', ')" -ForegroundColor Gray
    exit 1
}

# Get full path to Python
$pythonFullPath = (Get-Command $pythonExe).Source
Write-Host "Python path: $pythonFullPath" -ForegroundColor Gray
Write-Host ""

# Task names
$startupTaskName = "Dex Git Commit - Startup"
$dailyTaskName = "Dex Git Commit - Daily 9PM"

# Remove existing tasks if they exist
Write-Host "Checking for existing tasks..." -ForegroundColor Yellow
$existingStartup = Get-ScheduledTask -TaskName $startupTaskName -ErrorAction SilentlyContinue
$existingDaily = Get-ScheduledTask -TaskName $dailyTaskName -ErrorAction SilentlyContinue

if ($existingStartup) {
    Write-Host "  Removing existing startup task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $startupTaskName -Confirm:$false
}

if ($existingDaily) {
    Write-Host "  Removing existing daily task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $dailyTaskName -Confirm:$false
}

Write-Host ""

# Create startup task
Write-Host "Creating startup task..." -ForegroundColor Cyan
$startupAction = New-ScheduledTaskAction -Execute $pythonFullPath -Argument "`"$pythonScript`"" -WorkingDirectory $scriptPath
$startupTrigger = New-ScheduledTaskTrigger -AtStartup
$startupSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$startupPrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

try {
    Register-ScheduledTask -TaskName $startupTaskName -Action $startupAction -Trigger $startupTrigger -Settings $startupSettings -Principal $startupPrincipal -Description "Dex: Git commit at system startup (catches up on missed commits)" | Out-Null
    Write-Host "  ✓ Startup task created successfully" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to create startup task: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Create daily 9PM task
Write-Host "Creating daily 9PM task..." -ForegroundColor Cyan
$dailyAction = New-ScheduledTaskAction -Execute $pythonFullPath -Argument "`"$pythonScript`"" -WorkingDirectory $scriptPath
$dailyTrigger = New-ScheduledTaskTrigger -Daily -At "9:00PM"
$dailySettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$dailyPrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

try {
    Register-ScheduledTask -TaskName $dailyTaskName -Action $dailyAction -Trigger $dailyTrigger -Settings $dailySettings -Principal $dailyPrincipal -Description "Dex: Git commit daily at 9:00 PM" | Out-Null
    Write-Host "  ✓ Daily 9PM task created successfully" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Failed to create daily task: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "[SUCCESS] Automation Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Created tasks:" -ForegroundColor Cyan
Write-Host "  1. $startupTaskName" -ForegroundColor White
Write-Host "     - Runs when your computer starts" -ForegroundColor Gray
Write-Host "     - Catches up on any missed commits from previous day" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. $dailyTaskName" -ForegroundColor White
Write-Host "     - Runs daily at 9:00 PM" -ForegroundColor Gray
Write-Host "     - Commits any changes made during the day" -ForegroundColor Gray
Write-Host ""
Write-Host "To view/manage tasks:" -ForegroundColor Cyan
Write-Host "  - Open Task Scheduler (taskschd.msc)" -ForegroundColor White
Write-Host "  - Look for tasks starting with 'Dex Git Commit'" -ForegroundColor White
Write-Host ""
Write-Host "To test the script manually:" -ForegroundColor Cyan
Write-Host "  python $pythonScript" -ForegroundColor White
Write-Host ""
