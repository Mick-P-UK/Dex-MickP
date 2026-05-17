# setup_cedric_worker_task.ps1
# Creates a Windows Task Scheduler task to run the Cedric hourly worker.
# Run once as Administrator: Right-click PowerShell -> Run as Administrator
# Then: cd "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP" ; .\setup_cedric_worker_task.ps1

$taskName    = "Cedric Hourly Worker"
$description = "MCSB Phase 1.2 -- Processes inbox, cleans daily notes, commits to GitHub every hour"
$batFile     = "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\run_cedric_worker.bat"
$workDir     = "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"

# Remove existing task if present
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
    Write-Host "Removed existing task: $taskName"
}

# Create trigger: every 60 minutes, starting from next hour
$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 60) `
           -Once -At (Get-Date).Date.AddHours((Get-Date).Hour + 1)

# Action: run the bat file
$action = New-ScheduledTaskAction -Execute "cmd.exe" `
          -Argument "/c `"$batFile`"" `
          -WorkingDirectory $workDir

# Settings: run whether logged in or not, start if missed
$settings = New-ScheduledTaskSettingsSet `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable

# Principal: run as current user
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME `
             -LogonType S4U -RunLevel Highest

Register-ScheduledTask `
    -TaskName    $taskName `
    -Description $description `
    -Trigger     $trigger `
    -Action      $action `
    -Settings    $settings `
    -Principal   $principal `
    -Force

Write-Host ""
Write-Host "Task created: $taskName"
Write-Host "Runs every 60 minutes. Check Task Scheduler to confirm."
Write-Host ""
Write-Host "To test immediately: Start-ScheduledTask -TaskName '$taskName'"
