import argparse
import sys
from pathlib import Path

# Allow direct execution from VS Code, PowerShell, or cmd without installing
# Calibri as a site package.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import torch
from configs.llm import get_config


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--require-cuda", action="store_true")
    a = p.parse_args()

    c = get_config()
    print("AetherForge LLM preflight")
    print("torch:", torch.__version__, "cuda:", torch.cuda.is_available())
    print("target parameters:", c.parameter_target)
    print(
        "distributed product:",
        c.distributed.data_parallel
        * c.distributed.tensor_parallel
        * c.distributed.pipeline_parallel
        * c.distributed.expert_parallel,
    )
    if a.require_cuda and not torch.cuda.is_available():
        raise SystemExit("CUDA required")
    if (
        c.parameter_target >= 100_000_000_000_000
        and not c.safety.allow_single_device_100t
    ):
        print("100T single-device allocation: BLOCKED by safety policy")


if __name__ == "__main__":
    main()
