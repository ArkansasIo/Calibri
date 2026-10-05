from dataclasses import dataclass
import torch
import torch.nn as nn
import torch.nn.functional as F

@dataclass
class ModelConfig:
    vocab_size: int = 131072
    hidden_size: int = 1024
    num_layers: int = 12
    num_attention_heads: int = 16
    num_key_value_heads: int = 4
    intermediate_size: int = 4096
    max_position_embeddings: int = 4096

class DecoderBlock(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.norm1 = nn.RMSNorm(cfg.hidden_size)
        self.attn = nn.MultiheadAttention(cfg.hidden_size, cfg.num_attention_heads, batch_first=True)
        self.norm2 = nn.RMSNorm(cfg.hidden_size)
        self.mlp = nn.Sequential(
            nn.Linear(cfg.hidden_size, cfg.intermediate_size),
            nn.SiLU(),
            nn.Linear(cfg.intermediate_size, cfg.hidden_size),
        )

    def forward(self, x):
        n = x.size(1)
        mask = torch.full((n, n), float("-inf"), device=x.device)
        mask = torch.triu(mask, diagonal=1)
        x = x + self.attn(self.norm1(x), self.norm1(x), self.norm1(x), attn_mask=mask, need_weights=False)[0]
        x = x + self.mlp(self.norm2(x))
        return x

class CalibriLLM(nn.Module):
    """Reference decoder LLM.

    The class is intentionally a runnable reference model. It does not instantiate
    the 100T configuration by default; the distributed/MoE runtime must be selected
    explicitly for that scale.
    """
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.config = cfg
        self.embed = nn.Embedding(cfg.vocab_size, cfg.hidden_size)
        self.blocks = nn.ModuleList([DecoderBlock(cfg) for _ in range(cfg.num_layers)])
        self.norm = nn.RMSNorm(cfg.hidden_size)
        self.lm_head = nn.Linear(cfg.hidden_size, cfg.vocab_size, bias=False)

    def forward(self, input_ids, labels=None):
        x = self.embed(input_ids)
        for block in self.blocks:
            x = block(x)
        logits = self.lm_head(self.norm(x))
        loss = None
        if labels is not None:
            loss = F.cross_entropy(logits[:, :-1].contiguous().view(-1, logits.size(-1)),
                                   labels[:, 1:].contiguous().view(-1))
        return {"logits": logits, "loss": loss}
