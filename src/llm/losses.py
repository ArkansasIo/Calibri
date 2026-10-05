import torch
import torch.nn.functional as F

def causal_lm_loss(logits, labels, ignore_index=-100):
    return F.cross_entropy(logits[:, :-1].reshape(-1, logits.size(-1)),
                           labels[:, 1:].reshape(-1), ignore_index=ignore_index)

def label_smoothed_loss(logits, labels, smoothing=0.0, ignore_index=-100):
    if smoothing <= 0: return causal_lm_loss(logits,labels,ignore_index)
    logp=F.log_softmax(logits[:, :-1],dim=-1)
    target=labels[:,1:]
    mask=target.ne(ignore_index)
    safe=target.clamp_min(0)
    nll=-logp.gather(-1,safe.unsqueeze(-1)).squeeze(-1)
    smooth=-logp.mean(dim=-1)
    return ((1-smoothing)*nll+smoothing*smooth)[mask].mean()
