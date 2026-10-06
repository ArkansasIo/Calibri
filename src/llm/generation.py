from dataclasses import dataclass
import torch


@dataclass(frozen=True)
class GenerateConfig:
    max_new_tokens: int = 128
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 0
    repetition_penalty: float = 1.0
    eos_token_id: int | None = 2
    do_sample: bool = True
    use_cache: bool = True
    max_context: int | None = None
    seed: int | None = None


def _filter_top_k_top_p(logits, top_k, top_p):
    if top_k > 0:
        k = min(top_k, logits.size(-1))
        threshold = torch.topk(logits, k, dim=-1).values[..., -1, None]
        logits = logits.masked_fill(logits < threshold, float("-inf"))
    if 0 < top_p < 1:
        sorted_logits, sorted_indices = torch.sort(logits, descending=True, dim=-1)
        probs = torch.softmax(sorted_logits, dim=-1)
        remove = torch.cumsum(probs, dim=-1) > top_p
        remove[..., 1:] = remove[..., :-1].clone()
        remove[..., 0] = False
        sorted_logits = sorted_logits.masked_fill(remove, float("-inf"))
        logits = torch.full_like(logits, float("-inf"))
        logits.scatter_(-1, sorted_indices, sorted_logits)
    return logits


@torch.no_grad()
def generate(model, input_ids, config=None, **kwargs):
    """Generate tokens with optional KV cache, sampling controls and EOS stop."""
    cfg = config or GenerateConfig(**kwargs)
    if cfg.max_new_tokens < 0:
        raise ValueError("max_new_tokens must be non-negative")
    if cfg.temperature <= 0:
        raise ValueError("temperature must be positive")
    if not 0 < cfg.top_p <= 1:
        raise ValueError("top_p must be in (0, 1]")
    if cfg.repetition_penalty < 1:
        raise ValueError("repetition_penalty must be >= 1")
    if cfg.seed is not None:
        torch.manual_seed(cfg.seed)
    model.eval()
    ids = input_ids.clone()
    past = None
    finished = torch.zeros(ids.size(0), dtype=torch.bool, device=ids.device)

    for _ in range(cfg.max_new_tokens):
        if past is None or not cfg.use_cache:
            model_input = ids
        else:
            model_input = ids[:, -1:]
        if cfg.max_context and model_input.size(1) > cfg.max_context:
            model_input = model_input[:, -cfg.max_context:]
            past = None
        out = model(model_input, past_key_values=past, use_cache=cfg.use_cache)
        logits = out["logits"][:, -1, :]
        if cfg.use_cache:
            past = out["past_key_values"]
        if cfg.repetition_penalty > 1:
            for b in range(ids.size(0)):
                seen = ids[b].unique()
                vals = logits[b, seen]
                logits[b, seen] = torch.where(vals < 0, vals * cfg.repetition_penalty, vals / cfg.repetition_penalty)
        if cfg.do_sample:
            logits = logits / cfg.temperature
            logits = _filter_top_k_top_p(logits, cfg.top_k, cfg.top_p)
            probs = torch.softmax(logits, dim=-1)
            next_token = torch.multinomial(probs, 1)
        else:
            next_token = logits.argmax(dim=-1, keepdim=True)
        if cfg.eos_token_id is not None:
            eos = torch.full_like(next_token, cfg.eos_token_id)
            next_token = torch.where(finished[:, None], eos, next_token)
            finished |= next_token.squeeze(-1).eq(cfg.eos_token_id)
        ids = torch.cat((ids, next_token), dim=-1)
        if cfg.eos_token_id is not None and bool(finished.all()):
            break
    return ids
