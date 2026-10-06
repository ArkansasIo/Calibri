@echo off
setlocal
cd /d "%~dp0"

where npm >nul 2>nul
if errorlevel 1 (
  echo Node.js/npm was not found.
  echo Install Node.js, then run this script again.
  pause
  exit /b 1
)

echo Installing/updating MiMoCode CLI...
call npm install -g @mimo-ai/cli
if errorlevel 1 (
  echo MiMoCode installation failed.
  pause
  exit /b 1
)

echo.
echo MiMoCode is installed.
echo Start Calibri with:
echo   launch_terminal_ui.bat
echo Then select: MiMoCode AI
echo.
mimo --version
pause
endlocal
