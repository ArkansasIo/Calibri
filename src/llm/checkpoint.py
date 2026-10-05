"""Checkpoint utilities with shard metadata for distributed LLM training."""
from pathlib import Path
import json
import torch

def save_sharded_state_dict(state_dict, directory, max_tensors_per_shard=32):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    items = list(state_dict.items())
    shards = []
    for start in range(0, len(items), max_tensors_per_shard):
        shard = dict(items[start:start + max_tensors_per_shard])
        name = f"model-{len(shards):05d}.pt"
        torch.save(shard, directory / name)
        shards.append(name)
    index = {
        "format": "pytorch-sharded",
        "weight_map": {key: name for name, start in
                       ((name, i) for i, name in enumerate(shards))
                       for key in dict(items[start * max_tensors_per_shard:
                                            min((start + 1) * max_tensors_per_shard, len(items))])}
    }
    (directory / "model.index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    return index

def load_sharded_state_dict(directory, map_location="cpu"):
    directory = Path(directory)
    index = json.loads((directory / "model.index.json").read_text(encoding="utf-8"))
    out = {}
    for name in sorted(set(index["weight_map"].values())):
        out.update(torch.load(directory / name, map_location=map_location, weights_only=True))
    return out
