@echo off
:: run_cedric_worker.bat
:: Launcher for Cedric hourly worker -- called by Windows Task Scheduler.
:: MCSB Phase 1.2
::
:: Schedule: hourly (every 60 minutes)
:: To set up Task Scheduler, run setup_cedric_worker_task.ps1 as Administrator.

cd /d "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"
python cedric_worker.py >> "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP\System\worker_console.log" 2>&1
