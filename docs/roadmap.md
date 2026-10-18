# Coverage and expansion roadmap

## Delivered

50 independent original Python mechanics with behavioral checks, mapped to all 22 genre families in [the coverage table](genre-coverage.md). Player movement additionally has C, C++, C#, Lua, JavaScript, PHP, and Rust ports. The latter four remain unrun in this workspace. Genre and technology histories, security/legal guidance, and machine-readable indexes are included. See [validation evidence](validation.md).

The second edition adds 32 implementations, including platform jump timing, swept projectiles, attack frames, line of sight, RPG progression, quests, dialogue, initiative, resource purchases, fog, waves, simulation events, racing checkpoints, ball bounce, match-three collapse, rhythm timing, crafting, chunks, interest filtering, safe zones, ballots, decks, learning reviews, offline production, save migration, cooldowns, weighted loot, rollback replay, server input checks, sprite timing, and grid construction.

## Coverage limits

These are representative reusable algorithms, not every mechanic from every game. The coverage table's remaining column is an explicit backlog, not completed code. All 50 have Python code; only movement has other language ports. No third-party game code or assets were scraped. No complete multiplayer transport, deployed server, game engine, or CAD kernel has been built. No unattended researcher or background worker is configured.

## Next coherent milestones

1. Compose a playable example per genre using the independent modules. Begin with an ASCII maze, platform controller, and turn-based encounter.
2. Complete the most useful remaining systems from the coverage table: moving-platform contacts, weapon/targeting policies, combo input grammar, status effects, puzzle solvability, and audio-clock integration.
3. Add a tested authoritative multiplayer demo using a maintained framework, with authentication, secure transport, bounded inputs, disconnect/reconnect, packet loss and operational tests. Existing validation and replication examples are not substitutes for that demo.
4. Port mechanics across requested languages with equivalent tests, recording actual language/runtime versions and distinguishing unrun ports.
5. Add practical Godot, Unity, Unreal, LÖVE, Bevy and browser adapters. Keep version-specific code separate and record SDK licensing.
6. Expand 3D and tooling: navigation meshes, rigid-body contacts/constraints, terrain/voxel meshing, skeletal animation, editor serialization and precision CAD-kernel integration.

## Definition of complete for an entry

A focused README, assumptions/units, independent source, legal provenance, working invocation, meaningful behavioral checks, stated limitations, and updated catalog plus genre mapping. Run `python3 tools/build_indexes.py` after editing the data. Validate with `python3 tools/validate.py` and `python3 tools/build_indexes.py --check`. Label absent ports and pending integrations honestly.
