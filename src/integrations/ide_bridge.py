"""IDE detection and project-opening helpers without arbitrary shell execution."""
from __future__ import annotations
import shutil
from pathlib import Path

IDE_COMMANDS = {
    "code": "code",
    "visual_studio": "devenv",
    "rider": "rider64",
    "clion": "clion64",
    "pycharm": "pycharm64",
    "idea": "idea64",
    "nvim": "nvim",
    "vim": "vim",
}


def installed_ides():
    return {name: shutil.which(command) for name, command in IDE_COMMANDS.items() if shutil.which(command)}


def detect_project_editor(project: str | Path):
    root = Path(project)
    if (root / ".vscode").exists():
        return "VS Code"
    if (root / ".idea").exists():
        return "JetBrains"
    if list(root.glob("*.sln")) or list(root.glob("*.csproj")):
        return "Visual Studio / Rider"
    if (root / "CMakeLists.txt").exists():
        return "CMake-compatible IDE"
    return None
