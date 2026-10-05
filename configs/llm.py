from ml_collections import ConfigDict


def get_config():
    """Return the default 100-parameter LLM smoke-test configuration.

    Larger research configurations are kept as explicit opt-in profiles; the
    default is intentionally tiny so imports, training, generation and tests
    can run safely on a CPU without allocating a large model.
    """
    cfg = ConfigDict()
    cfg.enabled = True
    cfg.name = "Calibri-LLM-100P"
    cfg.architecture = "decoder_transformer"
    cfg.parameter_target = 100
    cfg.vocab_size = 11
    cfg.hidden_size = 2
    cfg.num_layers = 1
    cfg.num_attention_heads = 1
    cfg.num_key_value_heads = 1
    cfg.intermediate_size = 9
    cfg.max_position_embeddings = 64
    cfg.activation = "silu"
    cfg.normalization = "rmsnorm"
    cfg.position_encoding = "rope"
    cfg.rope_theta = 10000.0
    cfg.tie_word_embeddings = False
    cfg.dtype = "float32"

    cfg.moe = ConfigDict()
    cfg.moe.enabled = False
    cfg.moe.num_experts = 1
    cfg.moe.top_k = 1
    cfg.moe.capacity_factor = 1.0
    cfg.moe.load_balance_loss = 0.0

    cfg.generation = ConfigDict()
    cfg.generation.max_new_tokens = 32
    cfg.generation.temperature = 0.7
    cfg.generation.top_p = 0.9
    cfg.generation.top_k = 0
    cfg.generation.repetition_penalty = 1.0
    cfg.generation.do_sample = True

    cfg.training = ConfigDict()
    cfg.training.sequence_length = 32
    cfg.training.micro_batch_size = 1
    cfg.training.gradient_accumulation_steps = 1
    cfg.training.learning_rate = 1e-3
    cfg.training.warmup_steps = 10
    cfg.training.weight_decay = 0.0
    cfg.training.gradient_checkpointing = False
    cfg.training.bf16 = False

    cfg.distributed = ConfigDict()
    cfg.distributed.data_parallel = 1
    cfg.distributed.tensor_parallel = 1
    cfg.distributed.pipeline_parallel = 1
    cfg.distributed.expert_parallel = 1
    cfg.distributed.sequence_parallel = False
    cfg.distributed.zero_stage = 0
    cfg.distributed.fsdp = False

    cfg.cluster = ConfigDict()
    cfg.cluster.nodes = 1
    cfg.cluster.gpus_per_node = 0
    cfg.cluster.world_size = 1

    cfg.safety = ConfigDict()
    cfg.safety.require_distributed_for_100t = True
    cfg.safety.allow_single_device_100t = False
    return cfg
