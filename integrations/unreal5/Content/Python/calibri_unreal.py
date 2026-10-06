"""UE5 Editor-side Calibri bridge."""

try:
    import unreal
except ImportError:
    unreal = None

from pathlib import Path
import subprocess
import sys

def project_root():
    if unreal:
        return Path(unreal.Paths.project_dir())

def ask_calibri(prompt: str):
    root = project_root()
    if not root:
        raise RuntimeError("Run this script inside Unreal Editor.")
    calibri = root / "calibri_bridge_prompt.txt"
    calibri.write_text(prompt, encoding="utf-8")
    return str(calibri)

if __name__ == "__main__":
    print("Calibri UE5 bridge ready:", project_root())
