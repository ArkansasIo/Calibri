# AetherForge AI User Guide

## Windows quick start

    uv python install 3.11
    uv venv --python 3.11
    uv sync
    .\.venv\Scripts\Activate.ps1

Run the terminal control center:

    launch_terminal_ui.bat

## Free local AI

Run:

    setup_free_llm.bat

Then select LLM / Chat -> Free Local LLM.

AetherForge can use llama.cpp or Ollama locally. No paid API account is required.

## Local memory

    python scripts/local_ai.py remember "Important project decision"
    python scripts/local_ai.py memory "project decision"

Memory is stored locally under .calibri/memory.json.

## MiMoCode

    setup_mimocode.bat

Then launch the terminal UI and choose MiMoCode AI.

## Diffusion research

The original calibration workflow remains available through scripts/train.py and scripts/inference.py.

## Diagnostics

    python -m compileall gui scripts src configs
    python scripts/llm_preflight.py
    python scripts/local_ai.py status

## Desktop GUI

The compatibility launcher is launch_calibri_gui.bat. The visible application branding is AetherForge AI.