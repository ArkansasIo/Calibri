@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" "gui\calibri_gui.py"
) else (
  py -3.11 "gui\calibri_gui.py"
)
if errorlevel 1 pause
