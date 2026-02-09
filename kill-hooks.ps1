# PowerShell script to kill hanging hook processes
Write-Host "Killing any hanging hook processes..."

# Kill node processes with session-start in command line
Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*session-start*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

# Kill PowerShell processes with session-start in command line  
Get-Process -Name "powershell" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*session-start*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

# Kill cmd processes with session-start in command line
Get-Process -Name "cmd" -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*session-start*"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Done. Try starting Claude Code again."
