"""Preference optimization primitives (DPO-style objective)."""
import torch

def dpo_loss(policy_chosen,policy_rejected,ref_chosen,ref_rejected,beta=0.1):
    policy_delta=policy_chosen-policy_rejected
    ref_delta=ref_chosen-ref_rejected
    return -torch.nn.functional.logsigmoid(beta*(policy_delta-ref_delta)).mean()
