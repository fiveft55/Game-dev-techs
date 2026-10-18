# Coverage and expansion roadmap

## Delivered

18 independent original Python mechanics with behavioral checks; movement ports in C, C++, C#, Lua, JavaScript, PHP, and Rust; genre and technology histories; security and legal-reuse guidance; searchable JSON catalog. Validation evidence is in validation.md.

## Not yet delivered

This is not every known mechanic, every language, a complete engine, a playable multiplayer game, or a CAD package. Only movement currently has the additional language ports. Internet code has not been mirrored wholesale. No background worker or unattended research service is configured.

## Next coherent milestones

1. Add a playable ASCII maze that composes the existing modules while retaining their independence.
2. Add rendering, input binding, jump buffering/coyote time, animation state, sound, particles, and a save-format migration example.
3. Add a tested authoritative multiplayer demo using a maintained framework, with WSS/TLS deployment and loss/reconnect tests.
4. Port independently validated algorithms across requested languages, recording language/runtime versions and equivalent behavioral tests.
5. Add navmesh integration, behavior trees, GOAP, rigid-body contacts, constraints, terrain chunks, voxel meshing, skeletal animation, and editor serialization.
6. Add practical Godot, Unity, Unreal, LÖVE, Bevy, and web integrations in separate adapters; record engine-version compatibility and SDK licensing.
7. Evaluate CAD kernels for robust booleans and parametric constraints rather than expanding the toy extrusion into an unsupported precision tool.

## Definition of complete for an entry

A focused README, assumptions and units, independently reusable source, legal provenance, working invocation, meaningful checks, measured limitations, and an updated catalog. Label untested language ports and planned adapters honestly. Research and merge in bounded, reviewable commits.
