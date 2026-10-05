@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0.."

echo ==========================================
echo Calibri Windows Setup / Repair
echo ==========================================
echo.

set "ROOT=%CD%"
set "PY="
set "UV="

where uv >nul 2>nul
if not errorlevel 1 set "UV=uv"

if exist ".venv\Scripts\python.exe" (
    set "PY=.venv\Scripts\python.exe"
) else (
    where py >nul 2>nul
    if not errorlevel 1 set "PY=py -3.11"
)

if not defined UV (
    echo [ERROR] uv was not found.
    echo Install uv from https://docs.astral.sh/uv/getting-started/installation/
    echo Then run this setup again.
    goto :error
)

if not defined PY (
    echo [INFO] Python 3.11 was not found. uv will create the project environment.
)

echo [1/7] Checking repository files...
for %%F in (
    "pyproject.toml"
    "README.md"
    "configs\calibri.py"
    "scripts\inference.py"
    "scripts\train.py"
    "weights\flux_gates.json"
    "weights\qwenimage.json"
) do (
    if not exist "%%~F" (
        echo [ERROR] Missing required file: %%~F
        goto :error
    )
)

echo [2/7] Ensuring Python 3.11 is available...
uv python install 3.11
if errorlevel 1 goto :error

echo [3/7] Creating or repairing .venv...
uv venv --python 3.11
if errorlevel 1 goto :error

echo [4/7] Synchronizing dependencies...
uv sync
if errorlevel 1 goto :error

set "PY=.venv\Scripts\python.exe"

echo [5/7] Running syntax validation...
"%PY%" -m compileall gui scripts src configs
if errorlevel 1 goto :error

echo [6/7] Checking core imports...
"%PY%" -c "import torch, diffusers, transformers, accelerate, cma, ml_collections; print('Core imports: OK')"
if errorlevel 1 goto :error

echo [7/7] Checking PyTorch CUDA...
"%PY%" -c "import torch; print('PyTorch:', torch.__version__); print('CUDA available:', torch.cuda.is_available()); print('CUDA build:', torch.version.cuda); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU / CUDA unavailable')"

echo.
echo ==========================================
echo Setup / repair completed successfully.
echo ==========================================
echo.
echo Environment: %ROOT%\.venv
echo.
echo To launch the GUI:
echo   "%PY%" gui\calibri_gui.py
echo.
echo To build the GUI EXE:
echo   scripts\build_gui_exe.bat
echo.
pause
exit /b 0

:error
echo.
echo ==========================================
echo Setup / repair FAILED
echo ==========================================
echo Review the error above, then run this script again after fixing it.
pause
exit /b 1
