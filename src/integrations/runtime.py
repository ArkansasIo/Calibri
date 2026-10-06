"""Unified local capability discovery for AetherForge AI."""
from __future__ import annotations
import importlib.util
import shutil
import sys
from pathlib import Path
from .engine_bridge import detect_engine
from .ide_bridge import installed_ides
from .library_registry import supported_libraries
from .language_registry import supported_languages

ROOT = Path(__file__).resolve().parents[2]


def system_status(project: str | Path | None = None):
    result = {
        "python": sys.version.split()[0],
        "python_executable": sys.executable,
        "torch": importlib.util.find_spec("torch") is not None,
        "cuda": False,
        "git": shutil.which("git"),
        "uv": shutil.which("uv"),
        "ollama": shutil.which("ollama"),
        "llama_cpp": shutil.which("llama-cli") or shutil.which("llama"),
        "ides": installed_ides(),
        "language_count": len(supported_languages()),
        "library_count": len(supported_libraries()),
    }
    if result["torch"]:
        try:
            import torch
            result["cuda"] = bool(torch.cuda.is_available())
            result["gpu_count"] = torch.cuda.device_count()
        except Exception as exc:
            result["torch_error"] = str(exc)
    if project is not None:
        result["project"] = detect_engine(project).__dict__
    return result
