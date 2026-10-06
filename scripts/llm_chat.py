import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import torch
from src.llm import AetherForgeLLM, ModelConfig, SimpleTokenizer, generate


def main():
    p = argparse.ArgumentParser(description="AetherForge LLM interactive chat")
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    p.add_argument("--max-new-tokens", type=int, default=64)
    a = p.parse_args()
    tok = SimpleTokenizer()
    model = AetherForgeLLM(ModelConfig()).to(a.device).eval()
    print("AetherForge LLM chat. Type /quit to exit.")
    while True:
        prompt = input("You: ").strip()
        if prompt == "/quit":
            break
        ids = torch.tensor([tok.encode(prompt)], device=a.device)
        out = generate(model, ids, max_new_tokens=a.max_new_tokens)
        print("AI:", tok.decode(out[0].tolist()))


if __name__ == "__main__":
    main()
