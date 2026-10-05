import torch

def apply_repetition_penalty(logits, input_ids, penalty=1.0):
    if penalty <= 0: raise ValueError("penalty must be positive")
    if penalty == 1.0: return logits
    out = logits.clone()
    for b in range(out.size(0)):
        ids = torch.unique(input_ids[b])
        vals = out[b, ids]
        out[b, ids] = torch.where(vals < 0, vals * penalty, vals / penalty)
    return out

def sample_next_token(logits, temperature=1.0, top_k=0, top_p=1.0):
    if temperature <= 0: return logits.argmax(dim=-1, keepdim=True)
    logits = logits / temperature
    if top_k > 0:
        k=min(top_k, logits.size(-1))
        threshold=torch.topk(logits,k,dim=-1).values[..., -1,None]
        logits=logits.masked_fill(logits < threshold, float("-inf"))
    if top_p < 1.0:
        vals, idx=torch.sort(logits,descending=True,dim=-1)
        probs=torch.softmax(vals,dim=-1)
        mask=torch.cumsum(probs,dim=-1)-probs > top_p
        vals=vals.masked_fill(mask,float("-inf"))
        logits=torch.full_like(logits,float("-inf")).scatter(-1,idx,vals)
    return torch.multinomial(torch.softmax(logits,dim=-1),1)
