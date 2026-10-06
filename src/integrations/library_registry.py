"""Common game/AI library registry and capability metadata."""
from __future__ import annotations

LIBRARIES = {
    "pytorch": {"languages": ["Python", "C++"], "domains": ["ml", "tensor", "cuda"]},
    "transformers": {"languages": ["Python"], "domains": ["llm", "nlp", "vision"]},
    "diffusers": {"languages": ["Python"], "domains": ["diffusion", "vision"]},
    "onnx": {"languages": ["Python", "C++", "C#", "Java"], "domains": ["inference", "interop"]},
    "onnxruntime": {"languages": ["Python", "C++", "C#", "Java"], "domains": ["inference"]},
    "numpy": {"languages": ["Python", "C"], "domains": ["math", "tensor"]},
    "three.js": {"languages": ["JavaScript", "TypeScript"], "domains": ["3d", "webgl", "games"]},
    "pygame": {"languages": ["Python"], "domains": ["games", "2d"]},
    "raylib": {"languages": ["C", "C++", "C#", "Python"], "domains": ["games"]},
    "sdl": {"languages": ["C", "C++", "C#", "Rust"], "domains": ["games", "windowing"]},
    "opengl": {"languages": ["C", "C++", "Python"], "domains": ["graphics", "3d"]},
    "vulkan": {"languages": ["C++", "Rust", "C#"], "domains": ["graphics", "gpu"]},
}


def supported_libraries():
    return sorted(LIBRARIES)


def capabilities(name: str):
    key = name.lower()
    if key not in LIBRARIES:
        raise KeyError(name)
    return dict(LIBRARIES[key])


def libraries_for_language(language: str):
    return [name for name, meta in LIBRARIES.items() if language in meta["languages"]]
