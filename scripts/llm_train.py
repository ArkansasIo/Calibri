import argparse
import torch
from configs.llm import get_config
from src.llm.distributed import init_process_group, build_parallel_plan, validate_parallel_plan

def main():
    p=argparse.ArgumentParser(description="Calibri distributed LLM training launcher")
    p.add_argument("--backend", default=None)
    p.add_argument("--validate-only", action="store_true")
    a=p.parse_args()
    cfg=get_config()
    plan=build_parallel_plan(cfg)
    world=int(__import__("os").environ.get("WORLD_SIZE","1"))
    validate_parallel_plan(plan, world)
    if a.validate_only:
        print("distributed topology valid:", plan)
        return
    init_process_group(a.backend)
    rank=torch.distributed.get_rank()
    print(f"Calibri LLM distributed runtime initialized: rank={rank}, world={world}")
    if rank == 0:
        print("Model construction/training must be supplied with a distributed-safe checkpoint and optimizer.")
if __name__=="__main__":
    main()
