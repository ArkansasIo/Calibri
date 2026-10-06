"""CLI for managing offline models and local memory."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.llm.local_manager import list_models, recommended, remember, runtime_status, search_memory


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("status", "models", "recommended", "remember", "memory"))
    p.add_argument("value", nargs="*")
    args = p.parse_args()
    if args.command == "status":
        print(json.dumps(runtime_status(), indent=2))
    elif args.command == "models":
        print(json.dumps(list_models(), indent=2))
    elif args.command == "recommended":
        print(json.dumps(recommended(), indent=2))
    elif args.command == "remember":
        print(json.dumps(remember(" ".join(args.value)), indent=2))
    elif args.command == "memory":
        print(json.dumps(search_memory(" ".join(args.value)), indent=2))


if __name__ == "__main__":
    main()
