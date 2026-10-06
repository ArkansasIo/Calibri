"""Programming-language, IDE, build-system and library registry."""

LANGUAGES = {
    "C": [".c"], "C++": [".cpp", ".cc", ".cxx", ".h", ".hpp"],
    "C#": [".cs"], "Rust": [".rs"], "Java": [".java"], "Kotlin": [".kt"],
    "Python": [".py"], "JavaScript": [".js", ".mjs", ".cjs"],
    "TypeScript": [".ts", ".tsx"], "Go": [".go"], "Swift": [".swift"],
    "Objective-C": [".m", ".mm"], "Lua": [".lua"], "GDScript": [".gd"],
    "PHP": [".php"], "Ruby": [".rb"], "Dart": [".dart"],
    "Haskell": [".hs"], "OCaml": [".ml"], "Scala": [".scala"],
    "R": [".r"], "Julia": [".jl"], "Fortran": [".f", ".f90"],
    "Assembly": [".asm", ".s"], "SQL": [".sql"], "HTML": [".html"],
    "CSS": [".css"], "GLSL": [".glsl"], "HLSL": [".hlsl"],
    "ShaderLab": [".shader"], "GML": [".gml"], "Solidity": [".sol"],
    "WASM": [".wat", ".wasm"],
}

IDEs = [
    "Visual Studio", "VS Code", "JetBrains", "CLion", "Rider", "IntelliJ IDEA",
    "PyCharm", "Android Studio", "Xcode", "Eclipse", "NetBeans", "Neovim",
    "Vim", "Emacs", "Sublime Text", "Code::Blocks", "Qt Creator"
]

def detect_language(path: str) -> str:
    import pathlib
    suffix = pathlib.Path(path).suffix.lower()
    for language, extensions in LANGUAGES.items():
        if suffix in extensions:
            return language
    return "Unknown"

def supported_languages() -> list[str]:
    return sorted(LANGUAGES)
