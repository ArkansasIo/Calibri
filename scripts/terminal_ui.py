"""Calibri interactive terminal control center.

A dependency-light Windows-friendly TUI built with the Python standard library.
It provides menus, submenus, settings, agent chat, LLM controls, diagnostics,
calibration shortcuts, and safe project utilities.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = ROOT / ".calibri"
SETTINGS_FILE = CONFIG_DIR / "terminal_settings.json"
LOG_FILE = CONFIG_DIR / "terminal.log"

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}" if sys.stdout.isatty() else text


def pause() -> None:
    input("\nPress Enter to continue...")


def log(message: str) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(f"[{datetime.now().isoformat(timespec='seconds')}] {message}\n")


def load_settings() -> dict[str, Any]:
    defaults = {
        "theme": "dark",
        "show_timestamps": True,
        "agent_approval": True,
        "chat_device": "cpu",
        "max_new_tokens": 64,
        "default_agent": "planner",
        "safe_mode": True,
    }
    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
        defaults.update(data)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return defaults


def save_settings(settings: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(
        json.dumps(settings, indent=2) + "\n", encoding="utf-8"
    )


def header(title: str, settings: dict[str, Any]) -> None:
    clear()
    width = min(88, max(60, shutil_terminal_width()))
    line = "=" * width
    print(color(line, CYAN))
    print(color(" CALIBRI :: AI RESEARCH & AGENT CONTROL CENTER", BOLD + CYAN))
    print(color(f" {title}", BOLD + WHITE))
    print(color(line, CYAN))
    if settings.get("show_timestamps", True):
        print(color(datetime.now().strftime(" %Y-%m-%d %H:%M:%S"), DIM))
    print()


def shutil_terminal_width() -> int:
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


def menu(title: str, items: list[tuple[str, str]]) -> str:
    while True:
        print(color(title, BOLD + CYAN))
        for key, label in items:
            print(f"  {color(key, YELLOW)}  {label}")
        choice = input("\nSelect: ").strip().lower()
        if any(choice == key.lower() for key, _ in items):
            return choice
        print(color("Invalid selection.", RED))


def print_wrapped(value: Any) -> None:
    text = str(value)
    for line in text.splitlines() or [""]:
        print(textwrap.fill(line, width=max(50, shutil_terminal_width() - 4)))


def agent_chat(settings: dict[str, Any]) -> None:
    from src.agents import AgentOrchestrator

    selected = settings.get("default_agent", "planner")
    agents = [
        "planner", "researcher", "architect", "trainer",
        "evaluator", "optimizer", "diagnostics",
    ]

    while True:
        header("AGENT CHAT", settings)
        print(f" Active agent: {color(selected, GREEN)}")
        print(f" Approval: {color(str(settings['agent_approval']), GREEN)}")
        print("\nCommands: /agents  /clear  /back  /help")
        prompt = input(color("\nYou > ", CYAN)).strip()

        if not prompt:
            continue
        if prompt == "/back":
            return
        if prompt == "/clear":
            continue
        if prompt == "/help":
            print("Enter a task for the selected agent.")
            print("/agents switches the active specialist.")
            pause()
            continue
        if prompt == "/agents":
            header("SELECT AGENT", settings)
            for i, name in enumerate(agents, 1):
                print(f"  {i}. {name}")
            choice = input("\nAgent number: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(agents):
                selected = agents[int(choice) - 1]
                settings["default_agent"] = selected
                save_settings(settings)
            continue

        try:
            orchestrator = AgentOrchestrator(
                require_approval=bool(settings["agent_approval"])
            )
            if selected != "planner":
                result = orchestrator.registry.get(selected).handler({"task": prompt})
                result["routed_agent"] = selected
            else:
                result = orchestrator.run(prompt)
            log(f"agent={result.get('routed_agent', selected)} task={prompt!r}")
            print(color("\nCALIBRI >", GREEN))
            print_wrapped(json.dumps(result, indent=2, default=str))
        except Exception as exc:
            print(color(f"Agent error: {exc}", RED))
        input("\nPress Enter for another message...")


def settings_menu(settings: dict[str, Any]) -> None:
    while True:
        header("SETTINGS", settings)
        choice = menu("Configuration", [
            ("1", f"Theme: {settings['theme']}"),
            ("2", f"Show timestamps: {settings['show_timestamps']}"),
            ("3", f"Agent approval: {settings['agent_approval']}"),
            ("4", f"Safe mode: {settings['safe_mode']}"),
            ("5", f"Chat device: {settings['chat_device']}"),
            ("6", f"Max new tokens: {settings['max_new_tokens']}"),
            ("7", f"Default agent: {settings['default_agent']}"),
            ("8", "Reset settings"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            settings["theme"] = input("Theme (dark/light): ").strip() or "dark"
        elif choice in {"2", "3", "4"}:
            key = {"2": "show_timestamps", "3": "agent_approval", "4": "safe_mode"}[choice]
            settings[key] = not settings[key]
        elif choice == "5":
            value = input("Device (cpu/cuda): ").strip().lower()
            if value in {"cpu", "cuda"}:
                settings["chat_device"] = value
        elif choice == "6":
            try:
                value = int(input("Max new tokens: "))
                if 1 <= value <= 4096:
                    settings["max_new_tokens"] = value
            except ValueError:
                pass
        elif choice == "7":
            value = input("Agent: ").strip().lower()
            if value in {"planner", "researcher", "architect", "trainer", "evaluator", "optimizer", "diagnostics"}:
                settings["default_agent"] = value
        elif choice == "8":
            settings.clear()
            settings.update(load_settings_defaults())
        save_settings(settings)


def load_settings_defaults() -> dict[str, Any]:
    return {
        "theme": "dark", "show_timestamps": True, "agent_approval": True,
        "chat_device": "cpu", "max_new_tokens": 64, "default_agent": "planner",
        "safe_mode": True,
    }


def system_menu(settings: dict[str, Any]) -> None:
    while True:
        header("SYSTEM & DIAGNOSTICS", settings)
        choice = menu("Diagnostics", [
            ("1", "Python / platform information"),
            ("2", "PyTorch / CUDA status"),
            ("3", "LLM preflight"),
            ("4", "Compile-check project"),
            ("5", "View terminal log"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            print(f"Python: {sys.version}")
            print(f"Platform: {platform.platform()}")
            print(f"Root: {ROOT}")
        elif choice == "2":
            try:
                import torch
                print(f"PyTorch: {torch.__version__}")
                print(f"CUDA available: {torch.cuda.is_available()}")
                if torch.cuda.is_available():
                    print(f"GPU: {torch.cuda.get_device_name(0)}")
            except Exception as exc:
                print(color(f"PyTorch unavailable: {exc}", RED))
        elif choice == "3":
            run_known(["scripts/llm_preflight.py"])
        elif choice == "4":
            run_known(["-m", "compileall", "gui", "scripts", "src", "configs"])
        elif choice == "5":
            if LOG_FILE.exists():
                print_wrapped(LOG_FILE.read_text(encoding="utf-8")[-12000:])
            else:
                print("No log yet.")
        pause()


def run_known(args: list[str]) -> None:
    try:
        command = [sys.executable] + args
        result = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, timeout=300
        )
        print(result.stdout)
        if result.stderr:
            print(color(result.stderr, YELLOW))
        print(f"\nExit code: {result.returncode}")
    except Exception as exc:
        print(color(f"Command failed: {exc}", RED))


def llm_menu(settings: dict[str, Any]) -> None:
    while True:
        header("LLM CONTROL", settings)
        choice = menu("Language model", [
            ("1", "Interactive LLM chat"),
            ("2", "Single-prompt LLM"),
            ("3", "Create checkpoint"),
            ("4", "Show 100P configuration"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            run_known(["scripts/llm_chat.py", "--device", settings["chat_device"],
                       "--max-new-tokens", str(settings["max_new_tokens"])])
        elif choice == "2":
            prompt = input("Prompt: ").strip()
            if prompt:
                run_known(["scripts/llm.py", prompt])
        elif choice == "3":
            output = input("Checkpoint directory: ").strip()
            if output:
                run_known(["scripts/llm_checkpoint.py", "--output", output])
        elif choice == "4":
            from configs.llm import get_config
            print_wrapped(get_config())
        pause()


def agents_menu(settings: dict[str, Any]) -> None:
    while True:
        header("AGENT SYSTEM", settings)
        choice = menu("Multi-agent system", [
            ("1", "Agent chat"),
            ("2", "List registered agents"),
            ("3", "Route a task"),
            ("4", "Safety policy"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            agent_chat(settings)
        elif choice == "2":
            from src.agents import AgentOrchestrator
            registry = AgentOrchestrator().registry
            for name in registry.list():
                print(f"  {name}")
            pause()
        elif choice == "3":
            from src.agents import AgentOrchestrator
            task = input("Task: ").strip()
            if task:
                result = AgentOrchestrator().run(task)
                print_wrapped(json.dumps(result, indent=2))
            pause()
        elif choice == "4":
            print("Safe mode:", settings["safe_mode"])
            print("Agent approval:", settings["agent_approval"])
            print("Destructive/network/shell actions require explicit policy support.")
            pause()


def main_menu(settings: dict[str, Any]) -> None:
    while True:
        header("MAIN MENU", settings)
        choice = menu("Control Center", [
            ("1", "AI Agent System"),
            ("2", "LLM / Chat"),
            ("3", "Calibration / Research"),
            ("4", "System / Diagnostics"),
            ("5", "Project / Developer Tools"),
            ("6", "Settings"),
            ("7", "Help / About"),
            ("q", "Exit"),
        ])
        if choice == "q":
            return
        if choice == "1":
            agents_menu(settings)
        elif choice == "2":
            llm_menu(settings)
        elif choice == "3":
            research_menu(settings)
        elif choice == "4":
            system_menu(settings)
        elif choice == "5":
            developer_menu(settings)
        elif choice == "6":
            settings_menu(settings)
        elif choice == "7":
            header("HELP / ABOUT", settings)
            print("Calibri — diffusion calibration + LLM + multi-agent research environment.")
            print("This terminal UI uses only Python's standard library.")
            print("\nSafety: known project commands only; arbitrary shell execution is not exposed.")
            print("\nUseful shortcuts:")
            print("  AI Agent System -> Agent Chat")
            print("  LLM / Chat -> Interactive LLM Chat")
            print("  System -> Preflight / compile check")
            pause()


def research_menu(settings: dict[str, Any]) -> None:
    while True:
        header("CALIBRATION / RESEARCH", settings)
        choice = menu("Research operations", [
            ("1", "Show Calibri configuration"),
            ("2", "Run project compile check"),
            ("3", "Run LLM preflight"),
            ("4", "Open inference command guidance"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            try:
                from configs.calibri import cmaes_hpsv3_flux_gates
                print_wrapped(cmaes_hpsv3_flux_gates())
            except Exception as exc:
                print(color(f"Configuration error: {exc}", RED))
        elif choice == "2":
            run_known(["-m", "compileall", "gui", "scripts", "src", "configs"])
        elif choice == "3":
            run_known(["scripts/llm_preflight.py"])
        elif choice == "4":
            print("Use scripts/inference.py with the selected Calibri configuration.")
            print("GPU + model weights are required for diffusion inference.")
        pause()


def developer_menu(settings: dict[str, Any]) -> None:
    while True:
        header("PROJECT / DEVELOPER TOOLS", settings)
        choice = menu("Developer tools", [
            ("1", "Show repository root"),
            ("2", "Git status"),
            ("3", "Run compile check"),
            ("4", "Run Python module import check"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            print(ROOT)
        elif choice == "2":
            run_known(["-c", "import subprocess; print(subprocess.run(['git','status','--short'], cwd=r'" + str(ROOT).replace("\\", "\\\\") + "', text=True, capture_output=True).stdout)"])
        elif choice == "3":
            run_known(["-m", "compileall", "gui", "scripts", "src", "configs"])
        elif choice == "4":
            run_known(["-c", "import src.llm, src.agents, configs.llm; print('Imports OK')"])
        pause()


if __name__ == "__main__":
    settings = load_settings()
    save_settings(settings)
    try:
        main_menu(settings)
    except KeyboardInterrupt:
        print("\nExiting Calibri.")
