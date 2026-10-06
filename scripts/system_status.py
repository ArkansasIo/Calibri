"""AetherForge AI local capability and project diagnostics CLI."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from src.integrations.runtime import system_status
from src.integrations.engine_bridge import SUPPORTED_ENGINES
from src.integrations.language_registry import supported_languages
from src.integrations.library_registry import supported_libraries


def main():
    parser = argparse.ArgumentParser(description="AetherForge AI system diagnostics")
    parser.add_argument("--project", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    data = system_status(args.project)
    data["engines"] = sorted(SUPPORTED_ENGINES)
    data["languages"] = supported_languages()
    data["libraries"] = supported_libraries()
    if args.json:
        print(json.dumps(data, indent=2, default=str))
        return
    print("AetherForge AI system status")
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            print(f"{key}: {json.dumps(value, default=str)}")
        else:
            print(f"{key}: {value}")

if __name__ == "__main__":
    main()
