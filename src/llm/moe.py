import torch
import torch.nn as nn
import torch.nn.functional as F

class TopKMoE(nn.Module):
    """Runnable sparse MoE layer for development-scale experiments.

    Expert count is configurable, but this implementation intentionally refuses
    to materialize an unsafe 100T configuration on one device.
    """
    def __init__(self, hidden_size, intermediate_size, num_experts=8, top_k=2):
        super().__init__()
        if num_experts < 1 or top_k < 1 or top_k > num_experts:
            raise ValueError("invalid MoE expert/top-k configuration")
        self.num_experts = num_experts
        self.top_k = top_k
        self.router = nn.Linear(hidden_size, num_experts, bias=False)
        self.experts = nn.ModuleList([
            nn.Sequential(nn.Linear(hidden_size, intermediate_size), nn.SiLU(),
                          nn.Linear(intermediate_size, hidden_size))
            for _ in range(num_experts)
        ])

    def forward(self, x):
        b, s, h = x.shape
        flat = x.reshape(-1, h)
        scores = F.softmax(self.router(flat), dim=-1)
        weights, indices = torch.topk(scores, self.top_k, dim=-1)
        weights = weights / weights.sum(dim=-1, keepdim=True).clamp_min(1e-8)
        out = torch.zeros_like(flat)
        for e, expert in enumerate(self.experts):
            token_idx, slot = torch.where(indices == e)
            if token_idx.numel():
                out.index_add_(0, token_idx, expert(flat[token_idx]) * weights[token_idx, slot].unsqueeze(-1))
        load = scores.mean(dim=0)
        balance_loss = self.num_experts * (load * load).sum()
        return out.reshape(b, s, h), balance_loss
