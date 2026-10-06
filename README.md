# AetherForge AI

A local-first AI development and research platform for software, games, mathematics, and creative computing.

AetherForge AI is the new user-facing name for this repository. The Git repository remains ArkansasIo/Calibri so the original research implementation and history are preserved.

## Mission

AetherForge combines parameter-efficient diffusion calibration with a local AI development environment. It is designed to connect local language models, specialist agents, coding assistants, mathematics, game engines, IDEs, programming languages, and research tools.

Core goals:

- local-first AI inference;
- no paid API requirement for local inference;
- game-development assistance;
- multi-language software engineering;
- mathematics and scientific computing;
- diffusion-model research;
- safe agent orchestration;
- Windows desktop and terminal workflows;
- extensible integrations rather than vendor lock-in.

## Product identity

| Item | Value |
|---|---|
| Product | AetherForge AI |
| Repository | ArkansasIo/Calibri |
| License | MIT |
| Python | 3.10 through 3.12 |
| Local AI | llama.cpp, Ollama, native development LLM |
| Diffusion | PyTorch, Diffusers, Accelerate |
| Optimization | CMA-ES |
| Game development | Unreal Engine 5 and extensible engine adapters |

The historical name Calibri remains in research-specific code, configuration names, paper attribution, and compatibility paths where changing identifiers would break the original implementation.

## Platform architecture

    AETHERFORGE AI
           |
    +------+-------+----------------+
    |              |                |
  LOCAL AI       AGENTS          RESEARCH
    |              |                |
 llama.cpp     Planner          Diffusion
 Ollama        Researcher      CMA-ES
 Native LLM    Architect       Rewards
 GGUF          Trainer         FLUX
 Memory        Evaluator       SD3
               Optimizer       Qwen
               Diagnostics
    |              |                |
    +--------------+----------------+
                   |
          DEVELOPMENT BRIDGE
                   |
    +------+-------+-------+--------+
    |      |       |       |        |
   UE5   Unity   Godot   Bevy    Custom
    |      |       |       |        |
   C++   C#      GDScript Rust    Any
 Blueprint
 Python
                   |
             PROGRAMMING
                   |
 C/C++ C# Rust Java Python JS/TS Go Swift Kotlin
 Lua GDScript PHP Ruby Dart SQL HLSL GLSL Assembly
                   |
              MATHEMATICS
                   |
       Local math + Wolfram|Alpha

## Free local AI

AetherForge does not require a paid cloud API for its local AI path.

No subscription is required.
No paid API account is required.
No cloud inference is required.
No API usage billing is required.

LLMs still use internal tokens to represent text. No-token in the product description means no paid API-token billing system, not that the mathematical concept of tokens is removed from language models.

### Local backends

llama.cpp provides local GGUF inference on supported CPU/GPU hardware.

Ollama provides a convenient local model runtime and model manager.

The native AetherForge LLM provides a small development/reference transformer for testing the LLM infrastructure.

### Windows setup

    cd "C:\Users\Shadow\Music\New folder\Calibri"
    setup_free_llm.bat

Then:

    launch_terminal_ui.bat

Choose:

    LLM / Chat
      -> Free Local LLM

## Local model manager

Local GGUF models are discovered under:

    models/

The manager can list models, show recommended models, inspect runtime availability, and report model sizes.

Commands:

    python scripts/local_ai.py status
    python scripts/local_ai.py models
    python scripts/local_ai.py recommended

## Persistent local memory

AetherForge can store local development memories under:

    .calibri/memory.json

Examples:

    python scripts/local_ai.py remember "Use Unreal C++ for the combat server."
    python scripts/local_ai.py memory "combat server"

This memory is local project data. It is not automatically uploaded to a cloud AI service.

## Multi-agent system

The agent framework contains specialist roles:

- Planner
- Researcher
- Architect
- Trainer
- Evaluator
- Optimizer
- Diagnostics

The terminal control center supports agent selection, routing, interactive chat, approval settings, and safety controls.

The default interface does not expose unrestricted destructive shell execution.

## MiMoCode

AetherForge integrates MiMoCode as an external terminal-native coding assistant.

The integration deliberately keeps the external project separate from the AetherForge source tree.

Windows setup:

    setup_mimocode.bat

Then:

    launch_terminal_ui.bat

Choose:

    MiMoCode AI

## Unreal Engine 5

AetherForge includes an Unreal Engine 5 plugin foundation for development workflows.

Location:

    integrations/unreal5/

The adapter targets:

- C++;
- Blueprint;
- Unreal Editor Python;
- project inspection;
- future AI-assisted generation;
- compiler/build diagnostics.

The AI runtime should normally remain outside the packaged shipping game. The UE plugin is a development bridge, not an instruction to embed a large model into every game executable.

## Other game engines

The integration architecture is designed for:

| Engine | Languages |
|---|---|
| Unreal Engine 5 | C++, Blueprint, Python |
| Unity | C#, HLSL, ShaderLab |
| Godot | GDScript, C#, C++ |
| Bevy | Rust |
| Stride | C# |
| MonoGame | C# |
| libGDX | Java, Kotlin |
| Defold | Lua |
| GameMaker | GML |
| CryEngine | C++, C# |
| Custom engines | Project-defined |

The engine bridge is intended to inspect project structure, identify the engine and language, and provide the correct development context to the local AI.

## Programming languages

The language registry covers major ecosystems including:

C, C++, C#, Rust, Java, Kotlin, Python, JavaScript, TypeScript, Go, Swift, Objective-C, Lua, GDScript, PHP, Ruby, Dart, Haskell, OCaml, Scala, R, Julia, Fortran, Assembly, SQL, HTML, CSS, GLSL, HLSL, ShaderLab, GML, Solidity, and WebAssembly.

The registry is extensible. AetherForge does not attempt to replace the compiler, linker, debugger, package manager, or official IDE for each language.

## IDE support

The integration layer recognizes common development environments including:

Visual Studio, VS Code, JetBrains IDEs, CLion, Rider, IntelliJ IDEA, PyCharm, Android Studio, Xcode, Eclipse, NetBeans, Neovim, Vim, Emacs, Sublime Text, Code::Blocks, and Qt Creator.

The intended workflow is:

    IDE
      |
      v
    AetherForge AI
      |
      +--> local LLM
      +--> agents
      +--> project analysis
      +--> compiler/build diagnostics
      +--> mathematics
      +--> game-engine bridge

## Mathematics and Wolfram|Alpha

AetherForge includes a Wolfram|Alpha integration boundary for advanced mathematical queries.

Configure credentials outside source control:

    WOLFRAM_APP_ID=your-app-id

Never commit an App ID or other secret.

The intended workflow is:

    Natural-language problem
             |
             v
      AetherForge reasoning
             |
       +-----+------+
       |            |
    Local math   Wolfram|Alpha
       |            |
       +-----+------+
             |
     explanation / equation /
     algorithm / source code

This makes mathematical reasoning useful for programming and game-development tasks.

## Original diffusion research

The repository retains the original parameter-efficient diffusion research implementation.

Supported model families include:

- FLUX.1-dev
- Stable Diffusion 3.5 Medium
- Stable Diffusion 3.5 Large
- Qwen-Image

The original calibration approach uses CMA-ES to optimize a small calibration parameter set rather than retraining an entire diffusion model.

### Environment

Recommended Python version:

    Python 3.11

Windows:

    uv python install 3.11
    uv venv --python 3.11
    uv sync
    .\.venv\Scripts\Activate.ps1

Compile check:

    python -m compileall gui scripts src configs

### Training

Example:

    accelerate launch --num_processes 2 scripts/train.py --config configs/calibri.py:cmaes_hpsv3_flux_layer

### FLUX inference

    accelerate launch scripts/inference.py ^
      --config configs/calibri.py:cmaes_hpsv3_flux_gates ^
      --checkpoint_path .\weights\flux_gates.json ^
      --prompt "a futuristic city at sunset" ^
      --save_dir .\outputs\custom_gens

### Qwen-Image inference

    accelerate launch scripts/inference.py ^
      --config configs/calibri.py:cmaes_qwen_clean_hpsv3_2models_cfg ^
      --checkpoint_path .\weights\qwenimage.json ^
      --prompt "a futuristic city at sunset" ^
      --save_dir .\outputs\custom_gens

## Windows GUI

The existing compatibility launcher is:

    launch_calibri_gui.bat

The product identity shown to users is being migrated to AetherForge AI while the historical launcher remains available.

The GUI provides:

- environment diagnostics;
- setup and repair;
- local AI controls;
- diffusion inference;
- process control;
- output management;
- Windows executable build support.

## Terminal Control Center

Launch:

    launch_terminal_ui.bat

Main sections:

    1  AI Agent System
    2  LLM / Chat
    3  MiMoCode AI
    4  Calibration / Research
    5  System / Diagnostics
    6  Project / Developer Tools
    7  Settings
    8  Help / About
    q  Exit

## Safety

AetherForge is local-first and designed to keep credentials out of source code.

Never commit:

- API keys;
- Wolfram App IDs;
- cloud credentials;
- database passwords;
- SSH keys;
- private certificates;
- provider secrets.

Local model inference can remain offline after the runtime and model files have been obtained.

## Large-model configurations

The repository contains experimental distributed configurations for very large sparse models.

The 100T configuration is an architecture and distributed-training planning specification. It does not allocate a 100-trillion-parameter model on a normal desktop.

Real deployment requires suitable distributed hardware, memory, networking, checkpoint sharding, and parallelism.

## Project layout

    configs/              Configuration
    gui/                  Desktop GUI
    integrations/         Game-engine and external integrations
    scripts/              CLI tools
    src/agents/           Multi-agent framework
    src/integrations/     Engine, language and mathematics bridges
    src/llm/              Local LLM subsystem
    src/metrics/          Reward systems
    src/models/           Diffusion models
    src/optim/            Calibration algorithms
    weights/              Calibration checkpoints
    models/               Local GGUF model storage
    .calibri/             Local settings and memory
    tests/                Tests

## Development checks

Run:

    python -m compileall gui scripts src configs
    python scripts/llm_preflight.py
    python scripts/local_ai.py status

CUDA diagnostic:

    python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"

## Naming and compatibility

AetherForge AI is the new product name.

The repository path, historical research identifiers, configuration names, and compatibility launchers may still contain Calibri. These are retained deliberately to avoid breaking the original research implementation and existing workflows.

## License

MIT License. See LICENSE.

## Attribution

The original diffusion-calibration research and paper attribution remain preserved in the repository.

AetherForge AI is the broader development-platform identity built around that research foundation.
