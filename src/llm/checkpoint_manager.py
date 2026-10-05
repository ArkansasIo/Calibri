"""Atomic checkpoint metadata and resume state."""
from pathlib import Path
import json, os, tempfile, torch

def save_training_state(directory,model,optimizer,scheduler,state):
    d=Path(directory); d.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=d,delete=False,suffix=".pt") as f:
        tmp=f.name
    torch.save({"model":model.state_dict(),"optimizer":optimizer.state_dict(),
                "scheduler":scheduler.state_dict() if scheduler else None,
                "state":state.__dict__ if hasattr(state,"__dict__") else state},tmp)
    os.replace(tmp,d/"training_state.pt")

def load_training_state(directory,model,optimizer=None,scheduler=None,map_location="cpu"):
    payload=torch.load(Path(directory)/"training_state.pt",map_location=map_location,weights_only=False)
    model.load_state_dict(payload["model"])
    if optimizer: optimizer.load_state_dict(payload["optimizer"])
    if scheduler and payload["scheduler"]: scheduler.load_state_dict(payload["scheduler"])
    return payload["state"]
