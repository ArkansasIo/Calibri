import torch

def build_optimizer(model, lr=1e-5, weight_decay=0.1, betas=(0.9,0.95)):
    decay=[]; no_decay=[]
    for n,p in model.named_parameters():
        if not p.requires_grad: continue
        (no_decay if p.ndim < 2 or n.endswith("bias") else decay).append(p)
    return torch.optim.AdamW([
        {"params":decay,"weight_decay":weight_decay},
        {"params":no_decay,"weight_decay":0.0}], lr=lr, betas=betas)

def cosine_lr(step,total_steps,base_lr,warmup_steps=0,min_lr=0.0):
    if step < warmup_steps: return base_lr*step/max(1,warmup_steps)
    progress=min(1.0,(step-warmup_steps)/max(1,total_steps-warmup_steps))
    return min_lr+0.5*(base_lr-min_lr)*(1+__import__("math").cos(__import__("math").pi*progress))
