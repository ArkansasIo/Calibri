@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" "scripts\terminal_ui.py"
) else (
  python "scripts\terminal_ui.py"
)
if errorlevel 1 pause
endlocal
