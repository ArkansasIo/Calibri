"""MiMoCode integration for Calibri.

MiMoCode remains an external CLI dependency. This bridge discovers the installed
mimo command, runs it in the Calibri repository, and never stores API keys.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def executable() -> str | None:
    return shutil.which("mimo")


def status() -> dict[str, object]:
    exe = executable()
    return {"installed": exe is not None, "executable": exe, "repository": str(ROOT)}


def install_hint() -> str:
    return (
        'Windows PowerShell: powershell -ep Bypass -c '
        '"irm https://mimo.xiaomi.com/install.ps1 | iex"\n'
        'npm: npm install -g @mimo-ai/cli'
    )


def run(args: list[str] | None = None) -> int:
    exe = executable()
    if not exe:
        print("MiMoCode is not installed.")
        print(install_hint())
        return 1
    try:
        return subprocess.run([exe, *(args or [])], cwd=ROOT).returncode
    except KeyboardInterrupt:
        return 130


def interactive() -> int:
    return run([])


def one_shot(prompt: str) -> int:
    return run([prompt])


if __name__ == "__main__":
    sys.exit(interactive())
