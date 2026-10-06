# Programming Languages, IDEs, and Libraries

AetherForge is an AI coordination layer, not a replacement compiler or IDE.

## Languages

The registry includes C, C++, C#, Rust, Java, Kotlin, Python, JavaScript, TypeScript, Go, Swift, Objective-C, Lua, GDScript, PHP, Ruby, Dart, Haskell, OCaml, Scala, R, Julia, Fortran, Assembly, SQL, HTML, CSS, GLSL, HLSL, ShaderLab, GML, Solidity, and WebAssembly.

## IDEs

The registry recognizes Visual Studio, VS Code, JetBrains IDEs, CLion, Rider, IntelliJ IDEA, PyCharm, Android Studio, Xcode, Eclipse, NetBeans, Neovim, Vim, Emacs, Sublime Text, and Code::Blocks.

## Libraries and frameworks

The integration strategy is deliberately ecosystem-neutral. A project can retain its existing package manager and build system while AetherForge supplies analysis, code generation, debugging assistance, documentation, tests, and agent orchestration.

Examples include CMake, MSBuild, Cargo, Gradle, Maven, npm, pnpm, yarn, pip, uv, Poetry, Conan, vcpkg, NuGet, and engine-specific package systems.

## Recommended workflow

Detect project -> detect language -> detect build system -> inspect tests -> ask local AI -> propose changes -> require approval -> build/test -> report results.