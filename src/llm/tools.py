from dataclasses import dataclass
from typing import Callable

@dataclass
class ToolSpec:
    name: str
    description: str
    handler: Callable

class ToolRegistry:
    def __init__(self): self._tools={}
    def register(self,spec):
        if spec.name in self._tools: raise KeyError(spec.name)
        self._tools[spec.name]=spec
    def describe(self):
        return [{"name":t.name,"description":t.description} for t in self._tools.values()]
    def call(self,name,**kwargs):
        if name not in self._tools: raise KeyError(name)
        return self._tools[name].handler(**kwargs)
