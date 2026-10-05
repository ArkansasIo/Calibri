from ml_collections import ConfigDict

def get_config():
    cfg = ConfigDict()
    cfg.enabled = True
    cfg.directory = "checkpoints"
    cfg.format = "safetensors-sharded"
    cfg.shard_size_gb = 10
    cfg.save_every_steps = 1000
    cfg.keep_last = 5
    cfg.resume = True
    cfg.verify_checksums = True
    cfg.atomic_writes = True
    cfg.save_optimizer = True
    cfg.save_rng_state = True
    cfg.save_training_state = True
    return cfg
