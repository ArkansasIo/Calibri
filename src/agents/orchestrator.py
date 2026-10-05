from typing import Any, Dict
from .builtin import planner, researcher, architect, trainer, evaluator, optimizer, diagnostics
from .registry import AgentRegistry
from .safety import SafetyGuard

class AgentOrchestrator:
    def __init__(self, require_approval=True):
        self.registry = AgentRegistry()
        self.safety = SafetyGuard(require_approval=require_approval)
        self._register_defaults()

    def _register_defaults(self):
        for name, role, fn in [
            ("planner", "task_planning", planner),
            ("researcher", "research", researcher),
            ("architect", "model_architecture", architect),
            ("trainer", "training", trainer),
            ("evaluator", "evaluation", evaluator),
            ("optimizer", "calibration_optimization", optimizer),
            ("diagnostics", "system_diagnostics", diagnostics),
        ]:
            self.registry.register(name, role, fn)

    def route(self, task: str) -> str:
        text = task.lower()
        if any(k in text for k in ("train", "fine-tune", "finetune")):
            return "trainer"
        if any(k in text for k in ("evaluate", "benchmark", "score")):
            return "evaluator"
        if any(k in text for k in ("optimize", "calibrate", "cma-es")):
            return "optimizer"
        if any(k in text for k in ("architecture", "100t", "parameter", "model design")):
            return "architect"
        if any(k in text for k in ("diagnose", "debug", "error", "health")):
            return "diagnostics"
        if any(k in text for k in ("research", "paper", "literature")):
            return "researcher"
        return "planner"

    def run(self, task: str) -> Dict[str, Any]:
        agent = self.route(task)
        result = self.registry.get(agent).handler({"task": task})
        result["routed_agent"] = agent
        return result
