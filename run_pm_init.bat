@echo off
REM PM Initialization System Launcher
REM This script runs the PM Agent Initialization System using the conda environment

cd /d "c:\Users\Keagan\projects\agentic-infrastructure-framework"

echo Launching PM Agent Initialization System...
echo.

"C:\Users\Keagan\anaconda3\envs\pm-agent\python.exe" pm_init.py

pause
