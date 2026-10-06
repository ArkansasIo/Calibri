# AetherForge AI Architecture

## Layers

### 1. Local inference

Backends include llama.cpp, Ollama, and the native development LLM.

### 2. AI orchestration

Specialist agents provide planning, research, architecture, training, evaluation, optimization, and diagnostics.

### 3. Development integration

Project detection and language registries connect AI context to source trees, IDEs, build systems, and game engines.

### 4. Game engines

Unreal Engine 5 has an initial C++ module and Editor Python bridge. Other engines are represented by an extensible registry and adapter architecture.

### 5. Research

The original diffusion calibration system uses PyTorch, Diffusers, Accelerate, CMA-ES, and reward models.

### 6. Mathematics

Local mathematics can be combined with an optional Wolfram|Alpha API integration.

## Local-first boundary

The preferred architecture is:

    IDE / Game Editor
           |
           v
    AetherForge Bridge
           |
           v
    Local AI Runtime
           |
       +---+---+
       |       |
      LLM    Agents
       |       |
       +---+---+
           |
    project analysis
    code generation
    diagnostics
    mathematics
    build/test orchestration

Cloud APIs are optional integrations, not requirements for the local AI path.