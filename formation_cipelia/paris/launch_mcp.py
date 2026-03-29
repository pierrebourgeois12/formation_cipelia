#!/usr/bin/env python3
"""
Paris MCP Launcher
Lance le serveur MCP depuis le bon répertoire
"""
import subprocess
import sys
import os

# Change to the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_dir)

# Get the Python executable from venv
venv_python = os.path.join(project_dir, "venv", "Scripts", "python.exe")

# Run the server
subprocess.run([venv_python, "-m", "src.main"], check=False)
