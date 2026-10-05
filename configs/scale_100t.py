from ml_collections import ConfigDict

def get_config():
    cfg = ConfigDict()
    cfg.enabled = True
    cfg.name = "100T-MoE"
    cfg.target_parameter_count = 100_000_000_000_000
    cfg.architecture = "sparse_moe_transformer"
    cfg.experts = 1024
    cfg.active_experts_per_token = 8
    cfg.hidden_size = 32768
    cfg.num_layers = 256
    cfg.attention_heads = 256
    cfg.kv_heads = 64
    cfg.mlp_multiplier = 4
    cfg.context_length = 32768
    cfg.vocab_size = 131072
    cfg.activation = "silu"
    cfg.normalization = "rmsnorm"
    cfg.positional_encoding = "rope"
    cfg.weight_dtype = "bf16"
    cfg.compute_dtype = "bf16"
    cfg.quantization = "none"

    cfg.parallelism = ConfigDict()
    cfg.parallelism.data = 8
    cfg.parallelism.tensor = 16
    cfg.parallelism.pipeline = 16
    cfg.parallelism.expert = 32
    cfg.parallelism.sequence = True

    cfg.memory = ConfigDict()
    cfg.memory.activation_checkpointing = True
    cfg.memory.cpu_offload = False
    cfg.memory.zero_stage = 3
    cfg.memory.fsdp = True
    cfg.memory.gradient_accumulation_steps = 16
    cfg.memory.micro_batch_size = 1

    cfg.cluster = ConfigDict()
    cfg.cluster.nodes = 64
    cfg.cluster.gpus_per_node = 8
    cfg.cluster.require_distributed = True
    cfg.cluster.checkpoint_sharding = True
    cfg.cluster.checkpoint_format = "safetensors-sharded"

    cfg.router = ConfigDict()
    cfg.router.type = "top_k"
    cfg.router.k = 8
    cfg.router.capacity_factor = 1.25
    cfg.router.load_balance_loss = 0.01
    cfg.router.router_jitter = 0.0

    cfg.safety = ConfigDict()
    cfg.safety.allow_single_device_allocation = False
    cfg.safety.max_single_device_parameters = 100_000_000
    cfg.safety.require_explicit_100t_enable = True
    return cfg
