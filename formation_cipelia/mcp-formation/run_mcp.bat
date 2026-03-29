@echo off
REM Wrapper script to run MCP Formation server
REM This ensures we run from the correct working directory

cd /d "C:\Users\avisia\Documents\Avisia\formation\formation_cipelia\mcp-formation"
"C:\Users\avisia\Documents\Avisia\formation\formation_cipelia\mcp-formation\venv\Scripts\python.exe" -m src.main
