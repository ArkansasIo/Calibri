from dataclasses import dataclass
import torch
import torch.nn as nn
import torch.nn.functional as F
from .attention import GQAAttention
from .moe import TopKMoE

@dataclass
class ModelConfig:
    vocab_size: int = 11
    hidden_size: int = 2
    num_layers: int = 1
    num_attention_heads: int = 1
    num_key_value_heads: int = 1
    intermediate_size: int = 9
    max_position_embeddings: int = 64
    rope_theta: float = 10000.0
    moe_enabled: bool = False
    num_experts: int = 8
    moe_top_k: int = 2

class DecoderBlock(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.norm1 = nn.RMSNorm(cfg.hidden_size)
        self.attn = GQAAttention(cfg.hidden_size, cfg.num_attention_heads,
                                 cfg.num_key_value_heads, cfg.rope_theta)
        self.norm2 = nn.RMSNorm(cfg.hidden_size)
        self.moe = TopKMoE(cfg.hidden_size, cfg.intermediate_size,
                           cfg.num_experts, cfg.moe_top_k) if cfg.moe_enabled else None
        self.mlp = None if self.moe is not None else nn.Sequential(
            nn.Linear(cfg.hidden_size, cfg.intermediate_size),
            nn.SiLU(), nn.Linear(cfg.intermediate_size, cfg.hidden_size))

    def forward(self, x, past_key_value=None, use_cache=False):
        attn_out, present = self.attn(self.norm1(x), past_key_value, use_cache)
        x = x + attn_out
        aux_loss = x.new_zeros(())
        if self.moe is not None:
            ff, aux_loss = self.moe(self.norm2(x))
        else:
            ff = self.mlp(self.norm2(x))
        return x + ff, present, aux_loss

class AetherForgeLLM(nn.Module):
    """Development-scale decoder with GQA, RoPE, optional sparse MoE and KV cache."""
    def __init__(self, cfg: ModelConfig):
        super().__init__()
        self.config = cfg
        self.embed = nn.Embedding(cfg.vocab_size, cfg.hidden_size)
        self.blocks = nn.ModuleList([DecoderBlock(cfg) for _ in range(cfg.num_layers)])
        self.norm = nn.RMSNorm(cfg.hidden_size)
        self.lm_head = nn.Linear(cfg.hidden_size, cfg.vocab_size, bias=True)

    def forward(self, input_ids, labels=None, past_key_values=None, use_cache=False):
        if input_ids.ndim != 2:
            raise ValueError("input_ids must have shape [batch, sequence]")
        if input_ids.dtype != torch.long:
            input_ids = input_ids.long()
        x = self.embed(input_ids)
        presents = [] if use_cache else None
        aux_loss = x.new_zeros(())
        for i, block in enumerate(self.blocks):
            past = None if past_key_values is None else past_key_values[i]
            x, present, block_aux = block(x, past, use_cache)
            aux_loss = aux_loss + block_aux
            if use_cache:
                presents.append(present)
        logits = self.lm_head(self.norm(x))
        loss = None
        if labels is not None:
            loss = F.cross_entropy(
                logits[:, :-1].contiguous().view(-1, logits.size(-1)),
                labels[:, 1:].contiguous().view(-1),
                ignore_index=-100,
            )
        return {"logits": logits, "loss": loss, "aux_loss": aux_loss,
                "past_key_values": presents}

# Backward-compatible import name for existing Calibri integrations.
CalibriLLM = AetherForgeLLM
