"""Validation and planning helpers for very-large model configurations.

These helpers deliberately fail closed: a 100T target is treated as an architecture
plan unless an explicit distributed runtime is selected. They never allocate a
100-trillion-parameter dense tensor accidentally.
"""
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ScalePlan:
    target_parameters: int
    architecture: str
    distributed: bool
    estimated_bf16_weight_bytes: int
    estimated_fp32_weight_bytes: int


def build_scale_plan(cfg: Any) -> ScalePlan:
    scale = cfg.model.scale
    target = int(scale.target_parameters)
    distributed = bool(scale.distributed.enabled) if "distributed" in scale else True
    architecture = str(scale.architecture)
    return ScalePlan(
        target_parameters=target,
        architecture=architecture,
        distributed=distributed,
        estimated_bf16_weight_bytes=target * 2,
        estimated_fp32_weight_bytes=target * 4,
    )


def validate_scale_config(cfg: Any) -> Dict[str, Any]:
    plan = build_scale_plan(cfg)
    safety = cfg.model.scale.safety if "safety" in cfg.model.scale else {}
    max_single = int(safety.max_single_device_parameters) if "max_single_device_parameters" in safety else 100_000_000
    errors = []

    if plan.target_parameters <= 0:
        errors.append("target_parameters must be positive")
    if plan.target_parameters > max_single and not plan.distributed:
        errors.append("large-model target requires distributed execution")
    if plan.target_parameters >= 100_000_000_000_000 and not plan.distributed:
        errors.append("100T target cannot use the single-device runtime")
    if plan.architecture == "moe":
        experts = int(cfg.model.scale.experts)
        active = int(cfg.model.scale.active_experts_per_token)
        if active < 1 or active > experts:
            errors.append("active_experts_per_token must be between 1 and experts")

    return {
        "valid": not errors,
        "errors": errors,
        "target_parameters": plan.target_parameters,
        "architecture": plan.architecture,
        "distributed": plan.distributed,
        "estimated_bf16_weight_bytes": plan.estimated_bf16_weight_bytes,
        "estimated_fp32_weight_bytes": plan.estimated_fp32_weight_bytes,
    }
