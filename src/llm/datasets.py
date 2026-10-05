"""Streaming-friendly text dataset helpers."""
import json
from pathlib import Path
import torch
from torch.utils.data import IterableDataset

class JsonlTextDataset(IterableDataset):
    def __init__(self,path,tokenizer,max_tokens=4096):
        self.path=Path(path); self.tokenizer=tokenizer; self.max_tokens=max_tokens
    def __iter__(self):
        with self.path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                row=json.loads(line)
                text=row.get("text","")
                ids=self.tokenizer.encode(text)[:self.max_tokens]
                if len(ids)>1:
                    x=torch.tensor(ids,dtype=torch.long)
                    yield {"input_ids":x,"labels":x.clone()}
