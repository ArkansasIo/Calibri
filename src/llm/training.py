"""Safe development/distributed training utilities for AetherForge LLM."""
from dataclasses import dataclass
import torch
from torch.utils.data import DataLoader, Dataset

@dataclass
class TrainingState:
    step: int = 0
    epoch: int = 0
    best_loss: float = float("inf")

class TokenDataset(Dataset):
    def __init__(self, sequences):
        self.sequences = [torch.as_tensor(x, dtype=torch.long) for x in sequences]
    def __len__(self): return len(self.sequences)
    def __getitem__(self, i):
        x = self.sequences[i]
        return {"input_ids": x, "labels": x.clone()}

def collate_batch(batch):
    width = max(x["input_ids"].numel() for x in batch)
    ids = torch.zeros(len(batch), width, dtype=torch.long)
    labels = torch.full_like(ids, -100)
    for i, item in enumerate(batch):
        n = item["input_ids"].numel()
        ids[i, :n] = item["input_ids"]
        labels[i, :n] = item["labels"]
    return {"input_ids": ids, "labels": labels}

def build_loader(sequences, batch_size=1, shuffle=True):
    return DataLoader(TokenDataset(sequences), batch_size=batch_size,
                      shuffle=shuffle, collate_fn=collate_batch)

def train_step(model, batch, optimizer, scaler=None, grad_accumulation=1, aux_weight=0.01):
    device = next(model.parameters()).device
    ids, labels = batch["input_ids"].to(device), batch["labels"].to(device)
    with torch.autocast(device_type=device.type,
                        dtype=torch.bfloat16 if device.type == "cuda" else torch.float32,
                        enabled=device.type == "cuda"):
        out = model(ids, labels=labels)
        loss = out["loss"] + aux_weight * out.get("aux_loss", loss.new_zeros(()))
        loss = loss / grad_accumulation
    if scaler is not None and scaler.is_enabled():
        scaler.scale(loss).backward()
    else:
        loss.backward()
    return float(loss.detach().item() * grad_accumulation)

def optimizer_step(optimizer, model, grad_clip=1.0, scaler=None):
    if scaler is not None and scaler.is_enabled():
        scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
    if scaler is not None and scaler.is_enabled():
        scaler.step(optimizer)
        scaler.update()
    else:
        optimizer.step()
    optimizer.zero_grad(set_to_none=True)
