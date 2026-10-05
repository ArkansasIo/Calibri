<h1 align="center"> Calibri:<br>Enhancing Diffusion Transformers via Parameter-Efficient Calibration </h1>

<div align="center">
  <a href='https://arxiv.org/abs/2603.24800v1'><img src='https://img.shields.io/badge/ArXiv-red?logo=arxiv'></a>  &nbsp;
  <a href='https://v-gen-ai.github.io/Calibri-page/'><img src='https://img.shields.io/badge/Visualization-green?logo=github'></a> &nbsp;
  <a href='https://huggingface.co/collections/v-gen-ai/calibri-models'><img src='https://img.shields.io/badge/Model-blue?logo=huggingface'></a> &nbsp; 
  <!-- <a href='https://huggingface.co/spaces/jieliu/SD3.5-M-Flow-GRPO'><img src='https://img.shields.io/badge/Demo-blue?logo=huggingface'></a> &nbsp; -->
</div>

<br>

> **Calibri** is a parameter-efficient approach that optimally calibrates Diffusion Transformer (DiT) components to elevate generative quality. By framing DiT calibration as a black-box reward optimization problem solved using the CMA-ES evolutionary algorithm, Calibri modifies just **~100 parameters**. This lightweight calibration not only consistently improves generation quality across various models but also significantly reduces the required inference steps (NFE) while maintaining high-quality outputs.

# 📄 Changelog

 <details open>
<summary><strong>2026-04-13</strong></summary>


* Released **open calibration weights** for **FLUX.1-dev** and **Qwen-Image**.
* The calibrated checkpoints are now publicly available for inference at `weights/`.

</details>

<details open>
<summary><strong>2026-03-24</strong></summary>

* Official release of **Calibri** codebase! Code supports CMA-ES calibration for **FLUX**, **Stable Diffusion 3.5**, and **Qwen-Image**.

</details>


# 🤗 Supported Models & Rewards

Calibri optimizes text-to-image models by maximizing human-preference rewards. It currently supports the following DiT architectures and Reward Models:

| Task | Model | NFE with Calibri |
| -------- | -------- | -------- |
| Text-to-Image | [FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) | **15** |
| Text-to-Image | [stable-diffusion-3.5-medium](https://huggingface.co/stabilityai/stable-diffusion-3.5-medium) | **30** |
| Text-to-Image | [stable-diffusion-3.5-large](https://huggingface.co/stabilityai/stable-diffusion-3.5-large) | **30** |
| Text-to-Image | [Qwen-Image](https://huggingface.co/Qwen/Qwen-Image) | **30** |


**Supported Reward Models:**
* **[HPSv3](https://github.com/tgxs002/HPSv3)**: Human Preference Score v3.
* **[Q-Align](https://github.com/Q-Future/Q-Align)**: MLLM-based visual quality scoring.
* **[PickScore](https://huggingface.co/yuvalkirstain/PickScore_v1)**: CLIP-based aesthetic scoring model.
* **[ImageReward](https://github.com/THUDM/ImageReward)**: General human preference reward.


# 🚀 Quick start

## Environment Set Up
The framework is built with [uv](https://github.com/astral-sh/uv) — an extremely fast Python package and project manager. Installation guide is at uv [docs](https://docs.astral.sh/uv/getting-started/installation/)

**1. Clone the repository**
```bash
git clone https://github.com/your-username/Calibri.git
cd Calibri
```

**2. Setup environment and install dependencies**
```bash
uv sync
source .venv/bin/activate
```

## Reward Preparation

To train using HPSv3 or Q-Align rewards you need to start the reward servers before running the main training script.

HPSv3 server:

```bash
uv run src/metrics/hpsv3_server.py --device cuda:0
```

Q-Align server:
```bash
uv run src/metrics/qalign_server.py --device cuda:1
```

## Start Training
You can easily start the calibration process using Accelerate. The algorithm utilizes the CMA-ES evolutionary strategy to find the optimal scaling parameters.

```bash
accelerate launch --num_processes 2 scripts/train.py --config configs/calibri.py:cmaes_hpsv3_flux_layer
```

### ⚙️ Hyperparameters & Granularity

Calibri is designed to be highly flexible. You can easily customize the target DiT backbone, reward models, and optimization hyperparameters directly via `configs/calibri.py`.

A core feature of our framework is the ability to define the **search space granularity**. As described in our paper, Calibri supports three distinct levels of granularity for internal-layer calibration, allowing you to balance parameter efficiency and generation quality:

* **Block Scaling**: Uniformly adjusts the outputs of Attention and MLP layers within the same block (~57 parameters).
* **Layer Scaling**: Adjusts individual layers within a block using distinct coefficients (~76 parameters).
* **Gate Scaling**: Specialized calibration for visual and textual tokens processed through distinct gates in MM-DiT architectures (~114 parameters).

### 📈 Monitoring
Track your calibration progress, reward metrics, and generated image samples in real-time with tensorboard:

```bash
tensorboard --logdir=<exp_logdir>
```

## Inference

We provide a script to easily run inference for custom prompts or evaluate the calibrated checkpoints across your validation datasets.

**1. Custom Prompt Generation**

For Flux:

```bash
accelerate launch scripts/inference.py \
    --config configs/calibri.py:cmaes_hpsv3_flux_gates \
    --checkpoint_path ./weights/flux_gates.json \
    --prompt "a futuristic city at sunset" \
    --save_dir ./outputs/custom_gens
```

For Qwen:
```bash
accelerate launch scripts/inference.py \
    --config configs/calibri.py:cmaes_qwen_clean_hpsv3_2models_cfg \
    --checkpoint_path ./weights/qwenimage.json \
    --prompt "a futuristic city at sunset" \
    --save_dir ./outputs/custom_gens
```

This mode generates an image for your specific text prompt. It bypasses metrics calculation and outputs the result directly to `--save_dir`. 

**2. Data Evaluation**
```bash
accelerate launch scripts/inference.py \
    --config configs/calibri.py:cmaes_hpsv3_flux_gates \
    --checkpoint_path ./weights/flux_gates.json \
    --save_dir ./outputs/val_evaluation
```
If `--prompt` is not provided, the script runs a full evaluation on the validation dataset specified in your config (`cfg.data.val_dataset`). Distributed across multiple GPUs via `accelerate`, it generates all images and computes the human-preference reward metrics.

# 🤗 Acknowledgements

This repository is based on [diffusers](https://github.com/huggingface/diffusers/), [accelerate](https://github.com/huggingface/accelerate) and [flow_grpo](https://github.com/yifan123/flow_grpo/tree/main).
We thank them for their contributions to the community!!!

# ⭐Citation
If you find Calibri useful for your research or projects, we would greatly appreciate it if you could cite the following paper:

```bibtex
@article{tokhchukov2026calibri,
  title={Calibri: Enhancing Diffusion Transformers via Parameter-Efficient Calibration}, 
  author={Tokhchukov, Danil and Mirzoeva, Aysel and Kuznetsov, Andrey and Sobolev, Konstantin},
  journal={arXiv preprint arXiv:2603.24800},
  year={2026},
}
```
\n## 🧰 Visual Studio Code\n\nCalibri can be developed and debugged directly in VS Code on Windows.\n\n1. Install Python 3.11 and the VS Code Python extension.\n2. Open the repository folder in VS Code.\n3. Create/sync the environment with `uv sync`.\n4. Select `.venv\\Scripts\\python.exe` as the Python interpreter.\n5. Open **Run and Debug** and select **Calibri GUI**.\n\nThe repository includes `.vscode/settings.json` and `.vscode/launch.json`.\nThe **Calibri Inference — FLUX** debug profile runs the inference module through Accelerate.\n\n### Diagnostics\n\nRun this from the VS Code terminal:\n\n```powershell\npython -m compileall gui scripts src configs\npython -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"CPU\")"\n```\n\n### Recommended Windows setup\n\n```powershell\nuv python install 3.11\nuv venv --python 3.11\nuv sync\n.\\.venv\\Scripts\\Activate.ps1\npython -m compileall gui scripts src configs\n```\n\nThe GUI uses the active `.venv` Python interpreter and invokes Accelerate through `python -m accelerate.commands.launch`, avoiding a separate global `accelerate.exe` PATH dependency.\n