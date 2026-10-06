from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SafetyPolicy:
    max_prompt_tokens: int = 32768
    max_new_tokens: int = 4096
    allow_tools: bool = False
    allow_network: bool = False
    require_confirmation_for_actions: bool = True


def _token_count(value: Any) -> int:
    if value is None:
        return 0
    if hasattr(value, "shape"):
        shape = tuple(value.shape)
        return int(shape[-1]) if shape else 0
    if isinstance(value, (str, bytes)):
        return len(value.split())
    return len(value)


def validate_generation(request, policy=SafetyPolicy()):
    count = _token_count(request.get("input_ids", []))
    if count > policy.max_prompt_tokens:
        raise ValueError("prompt exceeds safety context limit")
    n = int(request.get("max_new_tokens", 128))
    if n < 1 or n > policy.max_new_tokens:
        raise ValueError("invalid max_new_tokens")
    if request.get("tool_call") and not policy.allow_tools:
        raise PermissionError("tool calls disabled by policy")
    if request.get("network") and not policy.allow_network:
        raise PermissionError("network access disabled by policy")
    if request.get("destructive_action") and policy.require_confirmation_for_actions:
        if not request.get("confirmed"):
            raise PermissionError("explicit confirmation required for destructive action")
    return True
