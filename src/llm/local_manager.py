"""Local model manager and persistent memory for Calibri."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "models"
MEMORY_FILE = ROOT / ".calibri" / "memory.json"

RECOMMENDED = [
    {"id": "qwen3.5-0.8b", "backend": "llama.cpp", "source": "ggml-org/Qwen3.5-0.8B-GGUF"},
    {"id": "gemma-3-1b", "backend": "llama.cpp", "source": "ggml-org/gemma-3-1b-it-GGUF"},
]


def list_models() -> list[dict[str, str]]:
    MODEL_DIR.mkdir(exist_ok=True)
    return [{"file": p.name, "path": str(p), "size_mb": f"{p.stat().st_size / 1048576:.1f}"}
            for p in MODEL_DIR.rglob("*.gguf") if p.is_file()]


def recommended() -> list[dict[str, str]]:
    return RECOMMENDED.copy()


def load_memory() -> list[dict[str, str]]:
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []


def remember(text: str, tags: list[str] | None = None) -> dict[str, object]:
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = load_memory()
    item = {"text": text, "tags": tags or []}
    data.append(item)
    MEMORY_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return item


def search_memory(query: str, limit: int = 8) -> list[dict[str, str]]:
    terms = {x.lower() for x in query.split() if len(x) > 2}
    scored = []
    for item in load_memory():
        haystack = (item.get("text", "") + " " + " ".join(item.get("tags", []))).lower()
        score = sum(term in haystack for term in terms)
        if score:
            scored.append((score, item))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:limit]]


def runtime_status() -> dict[str, object]:
    return {
        "llama": shutil.which("llama") or shutil.which("llama-cli"),
        "llama_server": shutil.which("llama-server"),
        "ollama": shutil.which("ollama"),
        "models": list_models(),
        "memory_entries": len(load_memory()),
        "model_directory": str(MODEL_DIR),
    }


if __name__ == "__main__":
    print(json.dumps(runtime_status(), indent=2))
