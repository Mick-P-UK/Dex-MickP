# PowerShell Script to Check Task Scheduler Status
# Verifies if Dex Git Commit scheduled tasks exist and reports their status

$ErrorActionPreference = "Continue"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Dex Git Commit - Task Scheduler Status Check" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$startupTaskName = "Dex Git Commit - Startup"
$dailyTaskName = "Dex Git Commit - Daily 9PM"

$tasksFound = 0
$tasksMissing = 0

# Check Startup Task
Write-Host "Checking for: $startupTaskName" -ForegroundColor Yellow
try {
    $startupTask = Get-ScheduledTask -TaskName $startupTaskName -ErrorAction Stop
    $tasksFound++
    
    Write-Host "  [FOUND]" -ForegroundColor Green -NoNewline
    Write-Host " - State: $($startupTask.State)" -ForegroundColor White
    
    # Get task info
    $startupInfo = Get-ScheduledTaskInfo -TaskName $startupTaskName -ErrorAction SilentlyContinue
    if ($startupInfo) {
        if ($startupInfo.LastRunTime) {
            Write-Host "  Last Run: $($startupInfo.LastRunTime)" -ForegroundColor Gray
            Write-Host "  Last Result: $($startupInfo.LastTaskResult)" -ForegroundColor Gray
        } else {
            Write-Host "  Last Run: Never" -ForegroundColor Gray
        }
        if ($startupInfo.NextRunTime) {
            Write-Host "  Next Run: $($startupInfo.NextRunTime)" -ForegroundColor Gray
        }
    }
    
    # Check if task is enabled
    if ($startupTask.State -eq "Disabled") {
        Write-Host "  WARNING: Task is DISABLED" -ForegroundColor Yellow
    }
    
} catch {
    $tasksMissing++
    Write-Host "  [NOT FOUND]" -ForegroundColor Red
    Write-Host "  Task does not exist in Task Scheduler" -ForegroundColor Gray
}

Write-Host ""

# Check Daily 9PM Task
Write-Host "Checking for: $dailyTaskName" -ForegroundColor Yellow
try {
    $dailyTask = Get-ScheduledTask -TaskName $dailyTaskName -ErrorAction Stop
    $tasksFound++
    
    Write-Host "  [FOUND]" -ForegroundColor Green -NoNewline
    Write-Host " - State: $($dailyTask.State)" -ForegroundColor White
    
    # Get task info
    $dailyInfo = Get-ScheduledTaskInfo -TaskName $dailyTaskName -ErrorAction SilentlyContinue
    if ($dailyInfo) {
        if ($dailyInfo.LastRunTime) {
            Write-Host "  Last Run: $($dailyInfo.LastRunTime)" -ForegroundColor Gray
            Write-Host "  Last Result: $($dailyInfo.LastTaskResult)" -ForegroundColor Gray
        } else {
            Write-Host "  Last Run: Never" -ForegroundColor Gray
        }
        if ($dailyInfo.NextRunTime) {
            Write-Host "  Next Run: $($dailyInfo.NextRunTime)" -ForegroundColor Gray
        }
    }
    
    # Check if task is enabled
    if ($dailyTask.State -eq "Disabled") {
        Write-Host "  WARNING: Task is DISABLED" -ForegroundColor Yellow
    }
    
} catch {
    $tasksMissing++
    Write-Host "  [NOT FOUND]" -ForegroundColor Red
    Write-Host "  Task does not exist in Task Scheduler" -ForegroundColor Gray
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Summary" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

if ($tasksFound -eq 2) {
    Write-Host "[SUCCESS] Both tasks are configured!" -ForegroundColor Green
    Write-Host ""
    Write-Host "To verify tasks are working:" -ForegroundColor Cyan
    Write-Host "  1. Open Task Scheduler (taskschd.msc)" -ForegroundColor White
    Write-Host "  2. Find tasks starting with 'Dex Git Commit'" -ForegroundColor White
    Write-Host "  3. Right-click a task → Run (to test manually)" -ForegroundColor White
    Write-Host "  4. Check 'Last Run Result' column (0x0 = success)" -ForegroundColor White
} elseif ($tasksFound -eq 1) {
    Write-Host "[PARTIAL] One task is missing!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To complete setup:" -ForegroundColor Cyan
    Write-Host "  Run: setup-automation.bat" -ForegroundColor White
} else {
    Write-Host "[NOT SET UP] No tasks found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "To set up automation:" -ForegroundColor Cyan
    Write-Host "  1. Double-click: setup-automation.bat" -ForegroundColor White
    Write-Host "  2. Click 'Yes' when UAC prompt appears" -ForegroundColor White
    Write-Host "  3. Press any key to continue" -ForegroundColor White
}

Write-Host ""
