"""Free local LLM backends for AetherForge AI.

This module deliberately uses local inference only. No cloud API key, account,
subscription, or usage-token billing is required. The model still has an
internal context/token representation; "no token system" here means no paid
API-token system.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def find_command(*names: str) -> str | None:
    for name in names:
        path = shutil.which(name)
        if path:
            return path
    return None


def backends() -> dict[str, dict[str, object]]:
    return {
        "calibri": {
            "name": "Calibri Native 100P",
            "available": True,
            "command": None,
            "local": True,
        },
        "llama_cpp": {
            "name": "llama.cpp Local",
            "available": find_command("llama", "llama-cli", "llama-server") is not None,
            "command": find_command("llama", "llama-cli", "llama-server"),
            "local": True,
        },
        "ollama": {
            "name": "Ollama Local",
            "available": find_command("ollama") is not None,
            "command": find_command("ollama"),
            "local": True,
        },
    }


def llama_chat(prompt: str, model: str = "ggml-org/Qwen3.5-0.8B-GGUF") -> str:
    command = find_command("llama-cli", "llama")
    if not command:
        raise RuntimeError(
            "llama.cpp is not installed. Install llama-cli and put it on PATH."
        )
    result = subprocess.run(
        ([command, "-hf", model, "-p", prompt] if Path(command).stem.lower() == "llama-cli" else [command, "cli", "-hf", model, "-p", prompt]),
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "llama.cpp failed")
    return result.stdout


def ollama_chat(prompt: str, model: str = "qwen3:0.6b") -> str:
    command = find_command("ollama")
    if not command:
        raise RuntimeError("Ollama is not installed or is not on PATH.")
    result = subprocess.run(
        [command, "run", model, prompt],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "Ollama failed")
    return result.stdout


def local_health(url: str = "http://127.0.0.1:11434/api/tags") -> bool:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            return response.status == 200
    except (OSError, urllib.error.URLError):
        return False


def status() -> dict[str, object]:
    result = backends()
    result["ollama_server"] = local_health()
    result["paid_api_key_required"] = False
    result["network_required_for_inference"] = False
    return result


if __name__ == "__main__":
    print(json.dumps(status(), indent=2))
