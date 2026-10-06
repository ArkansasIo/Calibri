import argparse
from configs.llm import get_config
from src.llm.distributed import build_parallel_plan, validate_parallel_plan

def main():
    p=argparse.ArgumentParser(description="Validate AetherForge LLM distributed topology")
    p.add_argument("--world-size", type=int, default=None)
    a=p.parse_args()
    cfg=get_config()
    plan=build_parallel_plan(cfg)
    validate_parallel_plan(plan, a.world_size)
    print(f"parallel plan: {plan}")
    print(f"world size: {plan.world_size}")

if __name__=="__main__":
    main()
