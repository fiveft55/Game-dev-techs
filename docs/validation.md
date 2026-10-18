# Validation evidence

Checked 19 October 2026 (Australia/Sydney) in the onboarding workspace.

| Check | Result |
|---|---|
| `python3 tools/validate.py` | 58 tests passed under Python 3.12.14: 50 individual mechanics, 4 composition tests, and 4 coverage/link checks |
| `python3 tools/build_indexes.py --check` | Generated genre coverage and mechanics index match their JSON source data |
| Genre coverage | All 22 documented genre families mapped exactly once; all 50 catalog entries mapped to a genre or cross-cutting tools |
| C movement, C11, warnings treated as errors | Compiled and diagonal normalization assertion passed |
| C++ movement, C++17, warnings treated as errors | Compiled and diagonal normalization assertion passed |
| Node.js movement | Diagonal normalization assertion passed |
| C#, Lua, PHP, Rust movement | Not executed: corresponding runtimes were not installed |
| Source registry links | Seven GitHub links returned HTTP 200; 18 external documentation links were blocked by the network proxy with 403 |
| Production engine, real network session, encryption handshake, CAD kernel | Not implemented or validated in this edition |

C, C++, Node.js and source-link outcomes above are retained evidence from the first edition; those unchanged ports and remote links were not rechecked for this expansion.

The small language smoke checks cover diagonal normalization, not full equivalence or every invalid input. Python tests cover representative behavior, not exhaustive correctness, security, or performance. See `source-link-check.json` for individual HTTP outcomes. Network denials are not evidence that the linked sites are unavailable generally.

## Second-edition behavior checked

The 32 added mechanics exercise successful actions and edge/rejection paths: consumed jump buffers, diagonal occlusion, projectile tunneling, duplicate attack hits, reward claims, dialogue flags, resource shortages, stale clocks, lap order, match intersections and gravity, rhythm misses, negative chunks, hidden entities, ties, empty decks, save versions, cooldown refill, exact loot-weight boundaries, rollback correction and malformed movement commands.

Composition tests verify fog with line-of-sight walls, firing cooldown plus projectile contact and damage, crafting plus save roundtripping, and corrected deterministic input replay. The coverage tests verify taxonomy alignment, implementation/test presence, generated index freshness and local documentation links. No real network transport, encryption handshake, engine rendering, or performance benchmark was executed.
