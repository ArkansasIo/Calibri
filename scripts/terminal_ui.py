"""Calibri interactive terminal control center."""
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CONFIG_DIR = ROOT / ".calibri"
SETTINGS_FILE = CONFIG_DIR / "terminal_settings.json"
LOG_FILE = CONFIG_DIR / "terminal.log"

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
WHITE = "\033[97m"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def color(text: str, code: str) -> str:
    return f"{code}{text}{RESET}" if sys.stdout.isatty() else text


def pause():
    input("\nPress Enter to continue...")


def log(message: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {message}\n")


def defaults():
    return {
        "theme": "dark",
        "show_timestamps": True,
        "agent_approval": True,
        "chat_device": "cpu",
        "max_new_tokens": 64,
        "default_agent": "planner",
        "safe_mode": True,
        "local_llm_backend": "llama_cpp",
    }


def load_settings():
    data = defaults()
    try:
        data.update(json.loads(SETTINGS_FILE.read_text(encoding="utf-8")))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return data


def save_settings(settings):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")


def width():
    try:
        return max(60, min(100, os.get_terminal_size().columns))
    except OSError:
        return 80


def header(title, settings):
    clear()
    line = "=" * width()
    print(color(line, CYAN))
    print(color(" CALIBRI :: AI RESEARCH & AGENT CONTROL CENTER", BOLD + CYAN))
    print(color(f" {title}", BOLD + WHITE))
    print(color(line, CYAN))
    if settings.get("show_timestamps", True):
        print(color(datetime.now().strftime(" %Y-%m-%d %H:%M:%S"), DIM))
    print()


def menu(title, items):
    print(color(title, BOLD + CYAN))
    for key, label in items:
        print(f"  {color(key, YELLOW)}  {label}")
    while True:
        choice = input("\nSelect: ").strip().lower()
        if any(choice == key.lower() for key, _ in items):
            return choice
        print(color("Invalid selection.", RED))


def wrapped(value):
    for line in str(value).splitlines() or [""]:
        print(textwrap.fill(line, width=max(50, width() - 4)))


def run_known(args):
    try:
        result = subprocess.run(
            [sys.executable, *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            timeout=300,
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(color(result.stderr, YELLOW))
        print(f"\nExit code: {result.returncode}")
    except Exception as exc:
        print(color(f"Command failed: {exc}", RED))


def agent_chat(settings):
    from src.agents import AgentOrchestrator

    agents = ["planner", "researcher", "architect", "trainer",
              "evaluator", "optimizer", "diagnostics"]
    selected = settings.get("default_agent", "planner")

    while True:
        header("AGENT CHAT", settings)
        print(f" Active agent: {color(selected, GREEN)}")
        print(f" Approval: {color(str(settings['agent_approval']), GREEN)}")
        print("\nCommands: /agents  /back  /help")
        prompt = input(color("\nYou > ", CYAN)).strip()
        if not prompt:
            continue
        if prompt == "/back":
            return
        if prompt == "/help":
            print("Enter a task for the selected specialist.")
            print("/agents switches agents.")
            pause()
            continue
        if prompt == "/agents":
            choice = menu("Agents", [(str(i), n) for i, n in enumerate(agents, 1)])
            selected = agents[int(choice) - 1]
            settings["default_agent"] = selected
            save_settings(settings)
            continue
        try:
            orchestrator = AgentOrchestrator(
                require_approval=bool(settings["agent_approval"])
            )
            result = orchestrator.run(prompt)
            if selected != "planner":
                result = orchestrator.registry.get(selected).handler({"task": prompt})
                result["routed_agent"] = selected
            log(f"agent={selected} task={prompt!r}")
            print(color("\nCALIBRI >", GREEN))
            wrapped(json.dumps(result, indent=2, default=str))
        except Exception as exc:
            print(color(f"Agent error: {exc}", RED))
        pause()


def agents_menu(settings):
    while True:
        header("AI AGENT SYSTEM", settings)
        choice = menu("Multi-agent system", [
            ("1", "Interactive agent chat"),
            ("2", "List registered agents"),
            ("3", "Route a task automatically"),
            ("4", "Agent safety policy"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        from src.agents import AgentOrchestrator
        if choice == "1":
            agent_chat(settings)
        elif choice == "2":
            for spec in AgentOrchestrator().registry.list():
                print(f"  {spec['name']:<14} {spec['role']}")
            pause()
        elif choice == "3":
            task = input("Task: ").strip()
            if task:
                print(json.dumps(AgentOrchestrator().run(task), indent=2))
            pause()
        elif choice == "4":
            print("Safe mode:", settings["safe_mode"])
            print("Approval required:", settings["agent_approval"])
            print("Arbitrary shell/network/destructive actions are not exposed by this UI.")
            pause()


def mimo_menu(settings):
    while True:
        header("MIMOCODE AI", settings)
        choice = menu("MiMoCode integration", [
            ("1", "Launch MiMoCode in Calibri"),
            ("2", "Ask MiMoCode a one-shot question"),
            ("3", "Check MiMoCode installation"),
            ("4", "Installation instructions"),
            ("5", "MiMoCode capabilities"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        from scripts.mimo_code import install_hint, one_shot, interactive, status
        if choice == "1":
            print("Starting MiMoCode in:", ROOT)
            interactive()
        elif choice == "2":
            prompt = input("MiMoCode prompt: ").strip()
            if prompt:
                one_shot(prompt)
        elif choice == "3":
            info = status()
            print("Installed:", info["installed"])
            print("Executable:", info["executable"] or "not found")
            print("Project:", info["repository"])
        elif choice == "4":
            print(install_hint())
        elif choice == "5":
            print("MiMoCode is a terminal-native AI coding assistant.")
            print("It can work with project files, coding tasks, Git, agents, memory,")
            print("and provider/model configuration through its own TUI.")
        pause()


def free_llm_menu(settings):
    while True:
        header("FREE LOCAL LLM", settings)
        choice = menu("No-paid-API local AI", [
            ("1", "Free local LLM chat"),
            ("2", "Switch llama.cpp / Ollama backend"),
            ("3", "Check local LLM runtimes"),
            ("4", "Local AI architecture"),
            ("5", "Privacy / billing status"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            backend = settings.get("local_llm_backend", "llama_cpp")
            run_known(["scripts/free_llm.py", "--backend", backend])
        elif choice == "2":
            current = settings.get("local_llm_backend", "llama_cpp")
            settings["local_llm_backend"] = "ollama" if current == "llama_cpp" else "llama_cpp"
            save_settings(settings)
            print("Backend:", settings["local_llm_backend"])
        elif choice == "3":
            run_known(["-c", "from src.llm.free_local import status; import pprint; pprint.pp(status())"])
        elif choice == "4":
            print("Calibri Native 100P: built-in CPU smoke-test model.")
            print("llama.cpp: local GGUF inference on CPU/GPU.")
            print("Ollama: local model runtime and model manager.")
            print("No paid cloud inference is required for these backends.")
        elif choice == "5":
            print("Paid API key required: NO")
            print("Subscription required: NO")
            print("Cloud inference required: NO")
            print("Internet is only needed to install/download a model.")
            print("Once the model is local, inference can run offline.")
        pause()


def llm_menu(settings):
    while True:
        header("LLM CONTROL", settings)
        choice = menu("Language model", [
            ("1", "Interactive Calibri LLM chat"),
            ("2", "Free Local LLM (no paid API)"),
            ("3", "Single-prompt Calibri LLM"),
            ("4", "Create checkpoint"),
            ("5", "Show default 100P configuration"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            run_known(["scripts/llm_chat.py", "--device", settings["chat_device"],
                       "--max-new-tokens", str(settings["max_new_tokens"])])
        elif choice == "2":
            free_llm_menu(settings)
        elif choice == "3":
            prompt = input("Prompt: ").strip()
            if prompt:
                run_known(["scripts/llm.py", *prompt.split()])
        elif choice == "4":
            output = input("Checkpoint directory: ").strip()
            if output:
                run_known(["scripts/llm_checkpoint.py", "--output", output])
        elif choice == "5":
            from configs.llm import get_config
            wrapped(get_config())
        pause()

def settings_menu(settings):
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
            value = input("Theme (dark/light): ").strip().lower()
            if value in {"dark", "light"}:
                settings["theme"] = value
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
                print("Invalid number.")
        elif choice == "7":
            value = input("Agent: ").strip().lower()
            if value in {"planner", "researcher", "architect", "trainer", "evaluator", "optimizer", "diagnostics"}:
                settings["default_agent"] = value
        elif choice == "8":
            settings.clear()
            settings.update(defaults())
        save_settings(settings)


def system_menu(settings):
    while True:
        header("SYSTEM & DIAGNOSTICS", settings)
        choice = menu("Diagnostics", [
            ("1", "Python / platform"),
            ("2", "PyTorch / CUDA / GPU"),
            ("3", "LLM preflight"),
            ("4", "Compile check"),
            ("5", "Terminal log"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            print("Python:", sys.version)
            print("Platform:", platform.platform())
            print("Repository:", ROOT)
        elif choice == "2":
            try:
                import torch
                print("PyTorch:", torch.__version__)
                print("CUDA:", torch.cuda.is_available())
                if torch.cuda.is_available():
                    print("GPU:", torch.cuda.get_device_name(0))
            except Exception as exc:
                print(color(f"PyTorch unavailable: {exc}", RED))
        elif choice == "3":
            run_known(["scripts/llm_preflight.py"])
        elif choice == "4":
            run_known(["-m", "compileall", "gui", "scripts", "src", "configs"])
        elif choice == "5":
            print(LOG_FILE.read_text(encoding="utf-8")[-12000:] if LOG_FILE.exists() else "No log.")
        pause()


def research_menu(settings):
    while True:
        header("CALIBRATION / RESEARCH", settings)
        choice = menu("Research operations", [
            ("1", "Show Calibri configuration"),
            ("2", "Compile project"),
            ("3", "LLM preflight"),
            ("4", "Inference guidance"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            try:
                from configs.calibri import cmaes_hpsv3_flux_gates
                wrapped(cmaes_hpsv3_flux_gates())
            except Exception as exc:
                print(color(f"Configuration error: {exc}", RED))
        elif choice == "2":
            run_known(["-m", "compileall", "gui", "scripts", "src", "configs"])
        elif choice == "3":
            run_known(["scripts/llm_preflight.py"])
        elif choice == "4":
            print("Run scripts/inference.py with a supported Calibri configuration.")
            print("Diffusion inference requires the appropriate model weights and GPU environment.")
        pause()


def developer_menu(settings):
    while True:
        header("PROJECT / DEVELOPER TOOLS", settings)
        choice = menu("Developer tools", [
            ("1", "Repository root"),
            ("2", "Git status"),
            ("3", "Compile check"),
            ("4", "Import check"),
            ("b", "Back"),
        ])
        if choice == "b":
            return
        if choice == "1":
            print(ROOT)
        elif choice == "2":
            result = subprocess.run(["git", "status", "--short"], cwd=ROOT, text=True, capture_output=True)
            print(result.stdout or "Working tree clean.")
        elif choice == "3":
            run_known(["-m", "compileall", "gui", "scripts", "src", "configs"])
        elif choice == "4":
            run_known(["-c", "import src.llm, src.agents, configs.llm; print('Imports OK')"])
        pause()


def main_menu(settings):
    while True:
        header("MAIN MENU", settings)
        choice = menu("Control Center", [
            ("1", "AI Agent System"),
            ("2", "LLM / Chat"),
            ("3", "MiMoCode AI"),
            ("4", "Calibration / Research"),
            ("5", "System / Diagnostics"),
            ("6", "Project / Developer Tools"),
            ("7", "Settings"),
            ("8", "Help / About"),
            ("q", "Exit"),
        ])
        if choice == "q":
            return
        if choice == "1":
            agents_menu(settings)
        elif choice == "2":
            llm_menu(settings)
        elif choice == "3":
            mimo_menu(settings)
        elif choice == "4":
            research_menu(settings)
        elif choice == "5":
            system_menu(settings)
        elif choice == "6":
            developer_menu(settings)
        elif choice == "7":
            settings_menu(settings)
        elif choice == "8":
            header("HELP / ABOUT", settings)
            print("Calibri — diffusion calibration, LLM, and multi-agent research environment.")
            print("Standard-library terminal control center with safe project operations.")
            pause()


if __name__ == "__main__":
    settings = load_settings()
    save_settings(settings)
    try:
        main_menu(settings)
    except KeyboardInterrupt:
        print("\nExiting Calibri.")
