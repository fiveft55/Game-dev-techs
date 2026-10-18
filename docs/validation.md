# Validation evidence

Checked 19 October 2026 (Australia/Sydney) in the onboarding workspace.

| Check | Result |
|---|---|
| `python3 tools/validate.py` | 18 behavioral test methods passed; one per Python mechanic |
| C movement, C11, warnings treated as errors | Compiled and diagonal normalization assertion passed |
| C++ movement, C++17, warnings treated as errors | Compiled and diagonal normalization assertion passed |
| Node.js movement | Diagonal normalization assertion passed |
| C#, Lua, PHP, Rust movement | Not executed: corresponding runtimes were not installed |
| Source registry links | Seven GitHub links returned HTTP 200; 18 external documentation links were blocked by the network proxy with 403 |
| Production engine, real network session, encryption handshake, CAD kernel | Not implemented or validated in this edition |

The small language smoke checks cover diagonal normalization, not full equivalence or every invalid input. Python tests cover representative behavior, not exhaustive correctness, security, or performance. See `source-link-check.json` for individual HTTP outcomes. Network denials are not evidence that the linked sites are unavailable generally.
