# Port toolchains and reproducible checks

The code itself has no third-party game/runtime libraries. Validation requires Python 3.10+ plus each selected native toolchain. The runner finds tools on PATH, then checks `GAME_DEV_TOOLS` (default `/workspace/.game-dev-tools`) for locally installed TypeScript, .NET, Rust and Go. Tool downloads and caches stay outside the tracked repository. Generated tests/results stay in `.build/ports/`.

## Versions actually used

| Language | Toolchain |
|---|---|
| JavaScript | Node.js available in the cloud image (exact version in validation report) |
| TypeScript | TypeScript 5.9.3, strict mode, ES2020, CommonJS output |
| C | System GCC, C11, `-Wall -Wextra -Werror`, undefined-behavior sanitizer |
| Lua | System Lua 5.4 shared library, through the small ctypes test launcher |
| C# | .NET SDK 8.0.426, installed net8.0 references and Roslyn compiler |
| GDScript | Godot 4.6.3, headless Godot 4 script execution |
| Rust | Rust 1.90.0, edition 2021, no external crates |
| Go | Go 1.25.1, standard library only, network package fetching disabled for tests |

A program named `/usr/bin/go` in this image is not the Go language toolchain. Check `go version`; the runner prefers the verified local Go toolchain when present.

## Installation notes

Use trusted official installers and keep TLS, checksum and signature verification enabled. No root-owned configuration or global PATH was changed during this work.

TypeScript was installed with:

```sh
mkdir -p /workspace/.game-dev-tools
npm install --prefix /workspace/.game-dev-tools --cache /workspace/.game-dev-tools/npm-cache --no-audit --no-fund typescript@5.9.3
```

.NET was installed from the official `https://dot.net/v1/dotnet-install.sh` installer into `/workspace/.game-dev-tools/dotnet`. For a pinned fresh install, pass `--version 8.0.426 --install-dir /workspace/.game-dev-tools/dotnet --no-path` after downloading the installer over verified HTTPS. The current instance was installed using the 8.0 channel and resolved that exact version.

The .NET CLI's first-run NuGet migration hit a platform named-mutex error in this container. The test runner therefore invokes the installed **Roslyn `csc.dll` directly with the installed net8 reference assemblies**, then executes the compiled DLL with the .NET host. This bypasses the unnecessary package-restore/first-run step; it does not bypass compilation or behavioral execution. No NuGet packages are needed. On a typical development machine, an ordinary net8.0 project can compile these classes.

Rust was installed using the official `https://sh.rustup.rs` installer, with `--profile minimal --default-toolchain 1.90.0 --no-modify-path`, setting `RUSTUP_HOME=/workspace/.game-dev-tools/rustup` and `CARGO_HOME=/workspace/.game-dev-tools/cargo`. The test runner supplies these variables for that local installation; no shell profile activation is required.

Go was downloaded from `https://dl.google.com/go/go1.25.1.linux-amd64.tar.gz`. The SHA-256 was verified against the matching official `https://go.dev/dl/?mode=json&include=all` release entry before extraction:

```text
7716a0d940a0f6ae8e1f3b3f4f36299dc53e31b16840dbd171254312c41ca12e
```

Extract a verified archive into `/workspace/.game-dev-tools` to obtain `go/bin/go`. Other architectures need the corresponding official archive and checksum, not this Linux x86_64 artifact.

Godot and GCC were already installed. Lua's shared library was already installed; `tools/run_lua.py` is a test launcher for that library, not an interpreter bundled into each port. On machines with `lua` or `lua5.4`, the runner uses the CLI directly. If neither is available, install Lua 5.4 through your trusted package manager.

## Commands

From the repository root:

```sh
python3 tools/test_ports.py --languages all
python3 tools/test_ports.py --mechanic player-movement --languages javascript,typescript,lua,csharp,gdscript,c,rust,go
```

The runner creates temporary language test projects with explicit fixtures. Go tests disable network dependency resolution; .NET uses only installed framework references. C tests additionally link all selected modules into one program to detect export collisions. To record a missing tool without failing the run, explicitly add `--allow-missing`; the report distinguishes missing from passed.
