@echo off
REM ---------------------------------------------------------------------------
REM run_cedric_server.bat -- MCSB Phase 1.3
REM Launches the Cedric Server (FastAPI) in dev/foreground mode.
REM Default bind: 127.0.0.1:8765 (override with CEDRIC_SERVER_HOST / _PORT).
REM ---------------------------------------------------------------------------

cd /d "C:\Vaults\Mick's-Dex-2nd-Brain\Dex-MickP"

echo.
echo Starting Cedric Server (foreground)...
echo Health check: http://127.0.0.1:8765/health
echo Press Ctrl+C to stop.
echo.

python cedric_server.py
