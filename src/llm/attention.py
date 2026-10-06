import math
import torch
import torch.nn as nn


def apply_rope(q, k, theta=500000.0, offset=0):
    """Apply rotary position embeddings to query/key tensors."""
    length = q.size(-2)
    dim = q.size(-1)
    half = dim // 2
    if half == 0:
        return q, k
    pos = torch.arange(offset, offset + length, device=q.device, dtype=torch.float32)
    inv = 1.0 / (theta ** (torch.arange(0, half, device=q.device, dtype=torch.float32) / half))
    angles = pos[:, None] * inv[None, :]
    cos, sin = angles.cos().to(q.dtype), angles.sin().to(q.dtype)

    def rotate(x):
        a, b = x[..., :half], x[..., half:2 * half]
        return torch.cat((a * cos - b * sin, a * sin + b * cos, x[..., 2 * half:]), dim=-1)

    return rotate(q), rotate(k)


class GQAAttention(nn.Module):
    """Grouped-query attention with RoPE and incremental KV caching."""
    def __init__(self, hidden_size, num_heads, num_kv_heads, rope_theta=500000.0):
        super().__init__()
        if hidden_size % num_heads:
            raise ValueError("hidden_size must divide evenly by num_heads")
        if num_heads % num_kv_heads:
            raise ValueError("num_heads must divide evenly by num_kv_heads")
        self.head_dim = hidden_size // num_heads
        self.num_heads = num_heads
        self.num_kv_heads = num_kv_heads
        self.rope_theta = rope_theta
        self.q_proj = nn.Linear(hidden_size, hidden_size, bias=False)
        self.k_proj = nn.Linear(hidden_size, num_kv_heads * self.head_dim, bias=False)
        self.v_proj = nn.Linear(hidden_size, num_kv_heads * self.head_dim, bias=False)
        self.o_proj = nn.Linear(hidden_size, hidden_size, bias=False)

    def forward(self, x, past_key_value=None, use_cache=False):
        b, s, _ = x.shape
        q = self.q_proj(x).view(b, s, self.num_heads, self.head_dim).transpose(1, 2)
        k = self.k_proj(x).view(b, s, self.num_kv_heads, self.head_dim).transpose(1, 2)
        v = self.v_proj(x).view(b, s, self.num_kv_heads, self.head_dim).transpose(1, 2)
        offset = 0 if past_key_value is None else past_key_value[0].size(-2)
        q, k = apply_rope(q, k, self.rope_theta, offset)
        if past_key_value is not None:
            k = torch.cat((past_key_value[0], k), dim=-2)
            v = torch.cat((past_key_value[1], v), dim=-2)
        repeat = self.num_heads // self.num_kv_heads
        k_attn = k.repeat_interleave(repeat, dim=1)
        v_attn = v.repeat_interleave(repeat, dim=1)
        # With cached keys, the query attends to all previous positions plus the
        # new token. A triangular causal mask over the enlarged K/V is incorrect.
        causal = past_key_value is None
        y = torch.nn.functional.scaled_dot_product_attention(
            q, k_attn, v_attn, is_causal=causal
        )
        y = y.transpose(1, 2).reshape(b, s, -1)
        return self.o_proj(y), ((k, v) if use_cache else None)
