# Mathematics and Wolfram|Alpha

AetherForge can connect natural-language mathematics to programming and game-development work.

## Local mathematics

Use the local AI and application code for deterministic calculations, symbolic routines, numerical methods, equations, statistics, and simulation where appropriate.

## Wolfram|Alpha

The integration boundary is src/integrations/wolfram.py.

Configure WOLFRAM_APP_ID outside source control.

Do not commit credentials.

## Example workflows

- derive a gameplay formula;
- solve an equation;
- calculate probability;
- analyze a physics relationship;
- convert a formula into C++;
- convert an algorithm into Rust;
- generate a shader from a mathematical model;
- validate a numerical result.

For safety and correctness, numerical results should be independently tested when used in production game logic or scientific software.