from ml_collections import ConfigDict

def get_config():
    cfg = ConfigDict()
    cfg.enabled = True
    cfg.backend = "nccl"
    cfg.timeout_seconds = 1800
    cfg.rendezvous_backend = "c10d"
    cfg.master_addr = "127.0.0.1"
    cfg.master_port = 29500
    cfg.elastic = False
    cfg.gradient_as_bucket_view = True
    cfg.find_unused_parameters = False
    cfg.static_graph = True
    cfg.deterministic = False
    cfg.allow_tf32 = True
    cfg.nccl_debug = "WARN"
    cfg.network_interface = ""
    return cfg
