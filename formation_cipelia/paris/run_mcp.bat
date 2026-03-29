@echo off
REM Paris MCP Server Launcher for Windows
REM Activate virtual environment and run the server

setlocal enabledelayedexpansion

REM Get the directory of this script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Check if venv exists
if not exist "venv" (
    echo Virtual environment not found. Creating venv...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\pip.exe install -r requirements.txt
)

REM Activate venv and run the server
call venv\Scripts\activate.bat
python -m src.main

pause
