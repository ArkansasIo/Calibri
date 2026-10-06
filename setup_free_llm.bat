@echo off
setlocal
cd /d "%~dp0"

echo ================================================
echo CALIBRI FREE LOCAL LLM SETUP
echo ================================================
echo.
echo This setup does not require a paid API key.
echo Local inference runs on your own CPU/GPU.
echo.

where llama >nul 2>nul
if not errorlevel 1 (
  echo llama.cpp is already available.
  llama --version
  goto done
)

where ollama >nul 2>nul
if not errorlevel 1 (
  echo Ollama is already available.
  ollama --version
  goto done
)

echo No local LLM runtime was detected.
echo.
echo Recommended options:
echo   1. llama.cpp - native local CPU/GPU inference
echo   2. Ollama    - simple local model management
echo.
echo Install either runtime, then reopen this terminal.
echo.
echo llama.cpp documentation:
echo https://github.com/ggml-org/llama.cpp
echo.
echo Ollama documentation:
echo https://ollama.com
echo.

:done
echo.
echo Start the Calibri terminal UI:
echo   launch_terminal_ui.bat
echo Then choose:
echo   LLM / Chat
echo   Free Local LLM
echo.
pause
endlocal
