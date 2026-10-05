from ml_collections import ConfigDict

def get_config():
    cfg = ConfigDict()
    cfg.enabled = True
    cfg.name = "Calibri-LLM"
    cfg.architecture = "decoder_transformer"
    cfg.parameter_target = 100_000_000_000_000
    cfg.vocab_size = 131072
    cfg.hidden_size = 32768
    cfg.num_layers = 256
    cfg.num_attention_heads = 256
    cfg.num_key_value_heads = 64
    cfg.intermediate_size = 131072
    cfg.max_position_embeddings = 32768
    cfg.activation = "silu"
    cfg.normalization = "rmsnorm"
    cfg.position_encoding = "rope"
    cfg.rope_theta = 500000.0
    cfg.tie_word_embeddings = False
    cfg.dtype = "bf16"

    cfg.moe = ConfigDict()
    cfg.moe.enabled = True
    cfg.moe.num_experts = 1024
    cfg.moe.top_k = 8
    cfg.moe.capacity_factor = 1.25
    cfg.moe.load_balance_loss = 0.01

    cfg.generation = ConfigDict()
    cfg.generation.max_new_tokens = 512
    cfg.generation.temperature = 0.7
    cfg.generation.top_p = 0.9
    cfg.generation.top_k = 50
    cfg.generation.repetition_penalty = 1.05
    cfg.generation.do_sample = True

    cfg.training = ConfigDict()
    cfg.training.sequence_length = 32768
    cfg.training.micro_batch_size = 1
    cfg.training.gradient_accumulation_steps = 16
    cfg.training.learning_rate = 1e-5
    cfg.training.warmup_steps = 1000
    cfg.training.weight_decay = 0.1
    cfg.training.gradient_checkpointing = True
    cfg.training.bf16 = True

    cfg.distributed = ConfigDict()
    cfg.distributed.data_parallel = 8
    cfg.distributed.tensor_parallel = 16
    cfg.distributed.pipeline_parallel = 16
    cfg.distributed.expert_parallel = 32
    cfg.distributed.sequence_parallel = True
    cfg.distributed.zero_stage = 3
    cfg.distributed.fsdp = True

    cfg.safety = ConfigDict()
    cfg.safety.require_distributed_for_100t = True
    cfg.safety.allow_single_device_100t = False
    return cfg
