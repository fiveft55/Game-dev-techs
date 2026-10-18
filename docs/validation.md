# Validation evidence

Checked 19 October 2026 (Australia/Sydney) in the cloud workspace. [Machine-readable native results](native-validation.json) record the toolchains, fixture counts, outcomes and a digest of the 408 native source files plus 51 C headers.

## Current edition

| Check | Result |
|---|---|
| `python3 tools/validate.py` | **79 tests passed** under Python 3.12.14: 51 individual mechanics, 13 focused grid-controller tests, 4 composition checks, 4 coverage/link checks and 7 portable-specification checks |
| `python3 tools/test_ports.py --languages all` | **163 fixtures passed in each of eight languages: 1,304 native fixture executions** across all 51 mechanics |
| JavaScript | Node.js v24.19.0: passed |
| TypeScript | 5.9.3 strict compilation, followed by execution in Node.js: passed |
| C | GCC 14.2.0, C11, warnings as errors and undefined-behavior sanitizer: passed |
| C integration | Public headers included together; all 51 separate translation units linked into one executable and invoked: passed |
| Lua | System Lua 5.4 library executed through the ctypes test launcher: passed |
| C# | .NET SDK 8.0.426 Roslyn compilation plus execution on .NET 8: passed |
| GDScript | Godot 4.6.3 headless script loading and execution: passed |
| Rust | Rust 1.90.0, edition 2021 compilation plus execution: passed |
| Go | Go 1.25.1, all 51 packages tested with fresh test execution and no fetched dependencies: passed |
| Generated source/contracts/fixtures | Checked against current generator/specifications: passed |
| Genre coverage | All 22 families mapped exactly once; every catalog entry mapped and all source/documentation links exist |
| Index freshness | Genre and mechanic indexes match catalog and coverage JSON |

The shared cases exercise successful actions, empty results, timing boundaries, duplicate events, invalid semantic requests, negative map coordinates, branching randomness, multi-flag dialogue, and other representative rules. Native fixtures are hand-authored; expected outputs are not produced by running the implementation being tested. C runs keep assertions enabled and use UBSan.

Additional Python reference tests compare portable math, collisions, pathfinding, line of sight and mesh output with existing Python modules over many inputs. Maze checks verify connectivity and closed borders. Composition tests exercise fog/line of sight, cooldown/projectile/damage, crafting/save roundtripping and deterministic correction/replay.

These checks validate the **documented portable contracts**, not full equivalence with every Python public method. See [language conventions](language-ports.md) for differences: event batching, minimal decoded save migration, explicit numeric IDs, binary64 arithmetic and reduced service APIs. Kernels assume correctly shaped finite input; they are not general hostile-input parsers.

## Platform notes

The .NET CLI's first-run NuGet migration failed on a named mutex. The runner uses the installed Roslyn compiler and net8 reference assemblies directly, then executes the resulting DLL. This compiles and runs real C#; it does not skip C# validation. `/usr/bin/go` was another program, so tests use the checksum-verified local Go 1.25.1 installation. See [toolchain instructions](toolchains.md).

No real network session, encryption handshake, engine rendering, production CAD kernel, concurrency load test or performance benchmark was run. Godot checks execute the pure GDScript kernels, not a playable scene. The original movement-only C++ smoke test remains prior-edition evidence; PHP and the earlier standalone movement snippets were not revalidated in this edition.

## Earlier research evidence

The first-edition source-link check recorded seven GitHub HTTP 200 responses and 18 documentation-site proxy denials. Those links were not re-fetched in this edition. See [source-link-check.json](source-link-check.json). A proxy denial does not establish that the site is unavailable generally, and an HTTP success does not establish substantive review or licensing suitability.

## Grid-movement addition

The new controller has 15 shared native fixtures and 13 focused Python tests plus a catalog-level behavioral test. Checks cover four directions, walls/map edges, partial and exact smooth landings, one-slot buffer replacement and expiry, release, repeated holds, explicit-state continuation, invalid requests, and equal results from long versus split updates. Instant-mode input cannot resume an unfinished smooth step. All eight native implementations executed the shared cases; no language was skipped. Drawing/input integration remains the caller's responsibility.
