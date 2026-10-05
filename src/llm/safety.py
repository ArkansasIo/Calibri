from dataclasses import dataclass

@dataclass
class SafetyPolicy:
    max_prompt_tokens: int = 32768
    max_new_tokens: int = 4096
    allow_tools: bool = False
    allow_network: bool = False
    require_confirmation_for_actions: bool = True

def validate_generation(request, policy=SafetyPolicy()):
    if len(request.get("input_ids", [])) > policy.max_prompt_tokens:
        raise ValueError("prompt exceeds safety context limit")
    n=int(request.get("max_new_tokens",128))
    if n < 1 or n > policy.max_new_tokens: raise ValueError("invalid max_new_tokens")
    if request.get("tool_call") and not policy.allow_tools:
        raise PermissionError("tool calls disabled by policy")
    return True
