from dataclasses import dataclass,field

@dataclass
class Message:
    role: str
    content: str

@dataclass
class Conversation:
    messages: list[Message]=field(default_factory=list)
    def add(self,role,content):
        if role not in {"system","user","assistant","tool"}: raise ValueError("invalid role")
        self.messages.append(Message(role,content))
    def render(self):
        return "\n".join(f"{m.role}: {m.content}" for m in self.messages)
    def clear(self): self.messages.clear()
