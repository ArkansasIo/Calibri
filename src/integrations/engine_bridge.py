"""Portable game-engine integration protocol for Calibri local AI."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

@dataclass
class EngineProject:
    engine: str
    project_path: str
    language: str
    editor: str | None = None

SUPPORTED_ENGINES = {
    "unreal5": ["C++", "Blueprint", "Python"],
    "unity": ["C#", "ShaderLab", "HLSL", "Python"],
    "godot": ["GDScript", "C#", "C++"],
    "bevy": ["Rust"],
    "stride": ["C#"],
    "monogame": ["C#"],
    "libgdx": ["Java", "Kotlin"],
    "defold": ["Lua"],
    "gamemaker": ["GML"],
    "cryengine": ["C++", "C#"],
    "custom": ["Any"],
}

def detect_engine(project: str | Path) -> EngineProject:
    root = Path(project)
    if (root / "*.uproject").exists() or list(root.glob("*.uproject")):
        return EngineProject("unreal5", str(root), "C++")
    if (root / "ProjectSettings" / "ProjectVersion.txt").exists():
        return EngineProject("unity", str(root), "C#")
    if (root / "project.godot").exists():
        return EngineProject("godot", str(root), "GDScript")
    if (root / "Cargo.toml").exists():
        return EngineProject("bevy", str(root), "Rust")
    return EngineProject("custom", str(root), "Any")

def manifest(project: EngineProject) -> str:
    return json.dumps(asdict(project), indent=2)
