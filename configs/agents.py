from ml_collections import ConfigDict

def get_config():
    cfg = ConfigDict()
    cfg.enabled = True
    cfg.registry = "configs.ai_systems:get_config"
    cfg.default_agent = "orchestrator"
    cfg.max_concurrent = 8
    cfg.health_check_interval_seconds = 30
    cfg.retry_count = 3
    cfg.retry_backoff_seconds = 2
    cfg.audit_log = "logs/agents.jsonl"
    cfg.allow_network = False
    cfg.allow_shell = False
    cfg.require_human_approval = True
    return cfg
