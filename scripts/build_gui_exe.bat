@echo off
setlocal
cd /d "%~dp0\.."
echo ==========================================
echo Calibri Windows GUI EXE Builder
echo ==========================================
where py >nul 2>nul
if errorlevel 1 (
  echo Python was not found.
  pause
  exit /b 1
)
if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=py -3.11"
)
%PY% -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error
if not exist "dist" mkdir dist
%PY% -m PyInstaller --noconfirm --clean --windowed --name Calibri --paths . gui\calibri_gui.py
if errorlevel 1 goto :error
echo.
echo Build complete: dist\Calibri\Calibri.exe
pause
exit /b 0
:error
echo.
echo EXE build failed.
pause
exit /b 1
