# Calibri Unreal Engine 5 Integration

This adapter is designed for UE5 projects using C++, Blueprint and Editor Python.
Unreal exposes C++ modules/plugins and an Editor Python API, so Calibri can act
as a local AI development assistant without becoming part of the shipping game.

Use:
1. Copy the adapter into a UE5 project's Plugins/CalibriAI directory.
2. Enable the plugin.
3. Point it at the Calibri repository/local AI runtime.
4. Use the editor tools to generate, inspect and validate C++/Blueprint/Python.

The bridge should keep AI inference outside the packaged game unless explicitly
requested by the developer.
