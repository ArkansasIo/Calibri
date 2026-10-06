"""Distributed runtime helpers for AetherForge large-model LLM plans.

These helpers configure process groups and validate the requested parallel topology.
They do not allocate a 100T model on a single device.
"""
from dataclasses import dataclass
import os
import torch
import torch.distributed as dist

@dataclass(frozen=True)
class ParallelPlan:
    data: int = 1
    tensor: int = 1
    pipeline: int = 1
    expert: int = 1

    @property
    def world_size(self):
        return self.data * self.tensor * self.pipeline * self.expert

def validate_parallel_plan(plan: ParallelPlan, world_size: int | None = None):
    if min(plan.data, plan.tensor, plan.pipeline, plan.expert) < 1:
        raise ValueError("parallel dimensions must be positive")
    expected = plan.world_size
    actual = world_size if world_size is not None else int(os.environ.get("WORLD_SIZE", "1"))
    if actual != expected:
        raise ValueError(f"parallel topology requires WORLD_SIZE={expected}, got {actual}")
    return True

def init_process_group(backend: str | None = None):
    if not dist.is_available():
        raise RuntimeError("torch.distributed is unavailable")
    if dist.is_initialized():
        return
    backend = backend or ("nccl" if torch.cuda.is_available() else "gloo")
    dist.init_process_group(backend=backend)

def build_parallel_plan(cfg):
    p = cfg.distributed
    return ParallelPlan(
        data=int(p.data_parallel),
        tensor=int(p.tensor_parallel),
        pipeline=int(p.pipeline_parallel),
        expert=int(p.expert_parallel),
    )
