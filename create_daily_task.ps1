# Create the missing Daily 9PM task
$ErrorActionPreference = "Stop"

Write-Host "Creating Daily 9PM Git Commit task..." -ForegroundColor Cyan

# Find Python
$pythonExe = $null
$pythonCommands = @("python", "py", "python3")

foreach ($cmd in $pythonCommands) {
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonExe = $cmd
            break
        }
    } catch {
        continue
    }
}

if (-not $pythonExe) {
    Write-Host "ERROR: Python not found!" -ForegroundColor Red
    exit 1
}

$pythonFullPath = (Get-Command $pythonExe).Source
$scriptPath = "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
$pythonScript = Join-Path $scriptPath "daily_git_commit.py"

Write-Host "Python: $pythonFullPath" -ForegroundColor Gray
Write-Host "Script: $pythonScript" -ForegroundColor Gray

# Remove existing task if it exists
$existing = Get-ScheduledTask -TaskName "Dex Git Commit - Daily 9PM" -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName "Dex Git Commit - Daily 9PM" -Confirm:$false
}

# Create the task
$action = New-ScheduledTaskAction -Execute $pythonFullPath -Argument "`"$pythonScript`"" -WorkingDirectory $scriptPath
$trigger = New-ScheduledTaskTrigger -Daily -At "9:00PM"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -TaskName "Dex Git Commit - Daily 9PM" -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description "Dex: Git commit daily at 9:00 PM" -Force | Out-Null

Write-Host "SUCCESS: Daily 9PM task created!" -ForegroundColor Green
