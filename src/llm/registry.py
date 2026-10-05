from dataclasses import dataclass

@dataclass
class ModelEntry:
    name: str
    factory: object
    metadata: dict

class ModelRegistry:
    def __init__(self): self._items={}
    def register(self,name,factory,metadata=None):
        if name in self._items: raise KeyError(f"model already registered: {name}")
        self._items[name]=ModelEntry(name,factory,metadata or {})
    def create(self,name,*args,**kwargs):
        return self._items[name].factory(*args,**kwargs)
    def list(self): return sorted(self._items)
