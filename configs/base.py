from ml_collections import ConfigDict

def get_config():
    cfg = ConfigDict()
    cfg.device = "cuda"

    cfg.experiment = ConfigDict()
    cfg.experiment.name = "flux_autoguidance_cmaes"
    cfg.experiment.seed = 42
    cfg.experiment.log_dir = "logs"
    cfg.experiment.save_eval_imgs = False
    cfg.experiment.save_json = True
    cfg.experiment.eval_orig_model = True

    cfg.model = ConfigDict()
    cfg.model.model_name = "black-forest-labs/FLUX.1-dev"
    cfg.model.dtype = "bf16"
    # Target architecture budget. This is metadata/configuration only; it does not
    # allocate 100 trillion parameters in memory. See README for feasibility notes.
    cfg.model.target_parameter_count = 100_000_000_000_000
    cfg.model.scale = ConfigDict()
    cfg.model.scale.enabled = True
    cfg.model.scale.preset = "100T"
    cfg.model.scale.target_parameters = 100_000_000_000_000
    cfg.model.scale.parameter_count_tolerance = 0.01
    cfg.model.scale.architecture = "moe"
    cfg.model.scale.experts = 1024
    cfg.model.scale.active_experts_per_token = 8
    cfg.model.scale.hidden_size = 32768
    cfg.model.scale.num_layers = 256
    cfg.model.scale.attention_heads = 256
    cfg.model.scale.kv_heads = 64
    cfg.model.scale.mlp_multiplier = 4
    cfg.model.scale.context_length = 32768
    cfg.model.scale.activation = "silu"
    cfg.model.scale.normalization = "rmsnorm"
    cfg.model.scale.positional_encoding = "rope"
    cfg.model.scale.weight_dtype = "bf16"
    cfg.model.scale.compute_dtype = "bf16"
    cfg.model.scale.quantization = "none"
    cfg.model.scale.distributed = ConfigDict()
    cfg.model.scale.distributed.enabled = True
    cfg.model.scale.distributed.data_parallel = 8
    cfg.model.scale.distributed.tensor_parallel = 16
    cfg.model.scale.distributed.pipeline_parallel = 16
    cfg.model.scale.distributed.expert_parallel = 32
    cfg.model.scale.distributed.sequence_parallel = True
    cfg.model.scale.distributed.zero_stage = 3
    cfg.model.scale.distributed.activation_checkpointing = True
    cfg.model.scale.distributed.cpu_offload = False
    cfg.model.scale.distributed.fsdp = True
    cfg.model.scale.distributed.checkpoint_sharding = True
    cfg.model.scale.distributed.nodes = 64
    cfg.model.scale.distributed.gpus_per_node = 8
    cfg.model.scale.safety = ConfigDict()
    cfg.model.scale.safety.require_distributed = True
    cfg.model.scale.safety.max_single_device_parameters = 100_000_000
    cfg.model.scale.safety.allow_100t_allocation = False

    cfg.gen = ConfigDict()
    cfg.gen.num_inference_steps = 15
    cfg.gen.num_inference_steps_val = 15
    cfg.gen.guidance_scale = 3.5
    cfg.gen.image_size = 512

    cfg.scaleguidance = ConfigDict()
    cfg.scaleguidance.num_models = 1
    cfg.scaleguidance.use_cfg = False
    cfg.scaleguidance.negative_prompt = ""

    cfg.optimize = ConfigDict()
    cfg.optimize.initial_sigma = 0.25
    cfg.optimize.max_generations = -1
    cfg.optimize.population_size = None
    cfg.optimize.val_every_steps = 10
    cfg.optimize.blocks_bound_low = -1.0
    cfg.optimize.blocks_bound_high = 2.0
    cfg.optimize.models_bound_low = -10.0
    cfg.optimize.models_bound_high = 10.0
    cfg.optimize.bucket_size = 16

    cfg.reward_fn = {}
    cfg.reward_fn_eval = {}

    cfg.data = ConfigDict()
    cfg.data.train_dataset = "data/t2i_compbench_train.txt"
    cfg.data.val_dataset = "data/t2i_compbench_val_random_crop.txt"
    cfg.data.batch_size_train = 4
    cfg.data.batch_size_val = 4
    cfg.data.num_workers = 2
    cfg.data.shuffle = True
    cfg.data.drop_last = True
    cfg.data.limit_train = -1
    cfg.data.limit_val = -1
    cfg.data.val_cut_cnt = None

    return cfg
