import argparse
from pathlib import Path
import torch
from src.llm import CalibriLLM, ModelConfig
from src.llm.checkpoint import save_sharded_state_dict

def main():
    p=argparse.ArgumentParser(description="Create a sharded Calibri LLM checkpoint")
    p.add_argument("--output", required=True)
    a=p.parse_args()
    model=CalibriLLM(ModelConfig())
    index=save_sharded_state_dict(model.state_dict(), Path(a.output))
    print(f"wrote {len(set(index['weight_map'].values()))} shards to {a.output}")
if __name__=="__main__": main()
