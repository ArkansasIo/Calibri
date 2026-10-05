import math
import torch

@torch.no_grad()
def perplexity(model, batches, device=None):
    model.eval(); total_loss=0.0; total_tokens=0
    device=device or next(model.parameters()).device
    for batch in batches:
        out=model(batch["input_ids"].to(device),labels=batch["labels"].to(device))
        labels=batch["labels"].to(device)
        count=labels[:,1:].ne(-100).sum().item()
        if count:
            total_loss += float(out["loss"])*count; total_tokens += count
    return math.exp(total_loss/max(1,total_tokens)) if total_tokens else float("inf")
