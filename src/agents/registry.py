from dataclasses import dataclass
from typing import Callable, Dict, Any

@dataclass
class AgentSpec:
    name: str
    role: str
    handler: Callable[[Dict[str, Any]], Dict[str, Any]]

class AgentRegistry:
    def __init__(self):
        self._agents: Dict[str, AgentSpec] = {}

    def register(self, name: str, role: str, handler: Callable[[Dict[str, Any]], Dict[str, Any]]):
        self._agents[name] = AgentSpec(name, role, handler)

    def get(self, name: str) -> AgentSpec:
        if name not in self._agents:
            raise KeyError(f"Unknown agent: {name}")
        return self._agents[name]

    def list(self):
        return [{"name": a.name, "role": a.role} for a in self._agents.values()]
