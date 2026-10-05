from dataclasses import dataclass

@dataclass
class SafetyGuard:
    require_approval: bool = True
    allow_network: bool = False
    allow_shell: bool = False
    allow_destructive: bool = False

    def check(self, action: str) -> None:
        destructive = {"delete", "overwrite", "publish", "deploy"}
        if action in destructive and not self.allow_destructive:
            raise PermissionError(f"Action '{action}' requires explicit approval")
        if action == "network" and not self.allow_network:
            raise PermissionError("Network access is disabled")
        if action == "shell" and not self.allow_shell:
            raise PermissionError("Shell access is disabled")
