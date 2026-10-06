# Game Engine Integration

## Unreal Engine 5

The UE5 foundation is under integrations/unreal5.

Supported development contexts:

- C++;
- Blueprint;
- Editor Python;
- project metadata;
- future build and diagnostic automation.

The plugin is intended for development/editor workflows.

## Unity

The planned adapter targets C#, HLSL, ShaderLab, project settings, scenes, prefabs, and Unity build tooling.

## Godot

The planned adapter targets GDScript, C#, C++, project.godot, scenes, nodes, resources, and Godot tooling.

## Bevy

The planned adapter targets Rust, Cargo, ECS systems, assets, shaders, and project configuration.

## Other engines

The language/engine registry provides a common discovery layer for Stride, MonoGame, libGDX, Defold, GameMaker, CryEngine, and custom engines.

## Common contract

An engine adapter should expose:

1. project detection;
2. language detection;
3. source/resource discovery;
4. build command discovery;
5. test command discovery;
6. diagnostics parsing;
7. AI prompt context;
8. safe file-edit boundaries.

AetherForge should not silently modify or execute destructive game-project operations.