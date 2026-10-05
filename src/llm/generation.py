import torch

@torch.no_grad()
def generate(model, input_ids, max_new_tokens=128, temperature=0.7, top_p=0.9):
    model.eval()
    ids = input_ids
    for _ in range(max_new_tokens):
        logits = model(ids)["logits"][:, -1, :]
        logits = logits / max(temperature, 1e-5)
        probs = torch.softmax(logits, dim=-1)
        sorted_probs, sorted_idx = torch.sort(probs, descending=True)
        cumulative = torch.cumsum(sorted_probs, dim=-1)
        remove = cumulative > top_p
        remove[..., 1:] = remove[..., :-1].clone()
        remove[..., 0] = False
        sorted_probs[remove] = 0
        sorted_probs = sorted_probs / sorted_probs.sum(dim=-1, keepdim=True)
        next_token = sorted_idx.gather(-1, torch.multinomial(sorted_probs, 1))
        ids = torch.cat([ids, next_token], dim=-1)
    return ids
