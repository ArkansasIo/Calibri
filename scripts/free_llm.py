"""Interactive free/local LLM console for Calibri."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.llm.free_local import llama_chat, ollama_chat, status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=("llama_cpp", "ollama"), default="llama_cpp")
    parser.add_argument("--model", default=None)
    parser.add_argument("prompt", nargs="*")
    args = parser.parse_args()

    if args.prompt:
        prompt = " ".join(args.prompt)
        if args.backend == "ollama":
            print(ollama_chat(prompt, args.model or "qwen3:0.6b"))
        else:
            print(llama_chat(prompt, args.model or "ggml-org/Qwen3.5-0.8B-GGUF"))
        return

    print("Calibri Free Local LLM Console")
    print("No paid API key or cloud usage account is required.")
    print("Commands: /status /backend /quit")
    backend = args.backend
    while True:
        try:
            prompt = input(f"[{backend}] You > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not prompt:
            continue
        if prompt == "/quit":
            return
        if prompt == "/status":
            print(status())
            continue
        if prompt == "/backend":
            backend = "ollama" if backend == "llama_cpp" else "llama_cpp"
            continue
        try:
            if backend == "ollama":
                answer = ollama_chat(prompt, args.model or "qwen3:0.6b")
            else:
                answer = llama_chat(prompt, args.model or "ggml-org/Qwen3.5-0.8B-GGUF")
            print("AI >", answer)
        except Exception as exc:
            print("ERROR >", exc)


if __name__ == "__main__":
    main()
