@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==================================================
echo AETHERFORGE AI - FREE LOCAL LLM SETUP
echo ==================================================
echo.
echo Local inference requires no paid API key or cloud
echo usage account. Models run on your own CPU/GPU.
echo.

set "PYTHON_CMD=python"
if exist ".venv\Scripts\python.exe" set "PYTHON_CMD=.venv\Scripts\python.exe"

echo [1/4] Checking Python...
%PYTHON_CMD% --version >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found.
  echo Run scripts\setup_windows.bat first.
  pause
  exit /b 1
)

echo [2/4] Checking local runtimes...
where ollama >nul 2>nul
if not errorlevel 1 (
  echo Ollama detected:
  ollama --version
  goto runtime_ready
)

where llama-cli >nul 2>nul
if not errorlevel 1 (
  echo llama.cpp detected:
  llama-cli --version
  goto runtime_ready
)

where llama >nul 2>nul
if not errorlevel 1 (
  echo llama.cpp runtime detected:
  llama --version
  goto runtime_ready
)

echo No local LLM runtime was detected.
echo.
echo [1] Install Ollama automatically
echo [2] Show llama.cpp instructions
echo [3] Continue without a runtime
echo [Q] Quit
choice /c 123Q /n /m "Selection: "
if errorlevel 4 exit /b 0
if errorlevel 3 goto runtime_ready
if errorlevel 2 goto llama_help
if errorlevel 1 goto install_ollama

:install_ollama
echo.
echo Installing Ollama using the official Windows installer command...
powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://ollama.com/install.ps1 | iex"
if errorlevel 1 (
  echo ERROR: Ollama installation failed.
  echo Manual installer: https://ollama.com/download/windows
  pause
  exit /b 1
)
set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Ollama"
where ollama >nul 2>nul
if errorlevel 1 (
  echo Reopen this terminal if the ollama command is not yet visible.
  pause
  exit /b 0
)
ollama --version
goto runtime_ready

:llama_help
echo.
echo llama.cpp releases:
echo https://github.com/ggml-org/llama.cpp/releases
echo Put llama-cli.exe on PATH, then reopen this terminal.
goto runtime_ready

:runtime_ready
echo.
echo [3/4] Checking AetherForge local LLM integration...
%PYTHON_CMD% scripts\free_llm.py --help
if errorlevel 1 echo WARNING: integration check returned a non-zero status.
echo.
echo [4/4] Setup complete.
echo.
echo Start: .\launch_terminal_ui.bat
echo Then choose LLM / Chat and Free Local LLM.
echo.
echo Direct examples:
echo   %PYTHON_CMD% scripts\free_llm.py --backend ollama
echo   %PYTHON_CMD% scripts\free_llm.py --backend llama_cpp
echo.
echo No paid API token is required.
pause
endlocal