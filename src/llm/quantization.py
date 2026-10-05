"""Lightweight quantization utilities; production kernels can replace these implementations."""
import torch

def int8_symmetric(tensor):
    scale=tensor.detach().abs().max().clamp_min(1e-8)/127
    q=torch.clamp(torch.round(tensor/scale),-127,127).to(torch.int8)
    return q,scale

def dequantize_int8(q,scale,dtype=torch.float32):
    return (q.float()*scale).to(dtype)
