from ml_collections import ConfigDict

def get_config():
    cfg = ConfigDict()

    cfg.agent = ConfigDict()
    cfg.agent.enabled = True
    cfg.agent.name = "Calibri-Orchestrator"
    cfg.agent.mode = "orchestrator"
    cfg.agent.max_steps = 32
    cfg.agent.timeout_seconds = 300
    cfg.agent.max_tool_calls = 64
    cfg.agent.require_approval_for_destructive_actions = True
    cfg.agent.persist_state = True

    cfg.agents = ConfigDict()
    for name, role in {
        "planner": "task_planning",
        "researcher": "research",
        "architect": "model_architecture",
        "trainer": "training",
        "evaluator": "evaluation",
        "optimizer": "calibration_optimization",
        "data": "dataset_management",
        "safety": "safety_validation",
        "diagnostics": "system_diagnostics",
        "checkpoint": "checkpoint_management",
    }.items():
        cfg.agents[name] = ConfigDict()
        cfg.agents[name].enabled = True
        cfg.agents[name].role = role
        cfg.agents[name].max_steps = 16
        cfg.agents[name].temperature = 0.2

    cfg.router = ConfigDict()
    cfg.router.strategy = "capability"
    cfg.router.fallback = "planner"
    cfg.router.max_parallel_agents = 8
    cfg.router.require_specialist_for_training = True

    cfg.memory = ConfigDict()
    cfg.memory.enabled = True
    cfg.memory.backend = "json"
    cfg.memory.path = "logs/agent_memory.json"
    cfg.memory.max_entries = 10000
    cfg.memory.redact_secrets = True

    cfg.tools = ConfigDict()
    cfg.tools.filesystem = True
    cfg.tools.git = True
    cfg.tools.python = True
    cfg.tools.shell = False
    cfg.tools.network = False
    cfg.tools.model_registry = True

    cfg.approval = ConfigDict()
    cfg.approval.enabled = True
    cfg.approval.actions = ["delete", "overwrite", "publish", "deploy", "external_network"]

    cfg.observability = ConfigDict()
    cfg.observability.logging = True
    cfg.observability.metrics = True
    cfg.observability.tracing = False
    cfg.observability.tensorboard = True

    cfg.providers = ConfigDict()
    cfg.providers.default = "local"
    cfg.providers.fallback = []
    cfg.providers.local = ConfigDict()
    cfg.providers.local.enabled = True
    cfg.providers.local.endpoint = ""
    cfg.providers.local.model = ""

    return cfg
