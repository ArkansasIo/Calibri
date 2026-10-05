import argparse
from configs.scale_100t import get_config
from src.models.scale_runtime import build_scale_plan, validate_scale_config

def main():
    p=argparse.ArgumentParser(description="Validate the 100T LLM architecture plan")
    p.add_argument("--allow-100t", action="store_true")
    a=p.parse_args()
    cfg=get_config()
    cfg.model.scale.safety.allow_100t_allocation=a.allow_100t
    plan=build_scale_plan(cfg)
    validate_scale_config(cfg)
    print(plan)
    print("LLM 100T configuration validation: OK")

if __name__=="__main__":
    main()
