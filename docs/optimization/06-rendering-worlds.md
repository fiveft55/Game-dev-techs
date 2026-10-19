# 6. Rendering, large worlds and streaming

Only drawing what matters can save much more than making one arithmetic operation slightly faster. First determine whether the limiting work is CPU submission, GPU geometry, shading, memory bandwidth or synchronization.

## Rendering decision table

| Technique | What it skips/reuses | Main tradeoff |
|---|---|---|
| Frustum culling | Objects outside the camera volume | Bounding-volume maintenance and tests. |
| Occlusion culling | Objects hidden by other geometry | Query/hierarchy costs, conservative visibility and latency. |
| Batching / instancing | Repeated submissions or repeated mesh setup | Larger batches can reduce culling flexibility and increase memory. |
| LOD | Unnecessary geometric/material detail at distance | Visible transitions, error tuning and asset complexity. |
| Reduced overdraw | Repeated shading of covered pixels | Sorting/composition restrictions, especially with transparency. |
| Texture/mesh streaming | Resources not needed yet | I/O, decompression, upload spikes, residency tracking and fallback quality. |

A lower draw-call count is not automatically faster. Combining a whole city into one mesh can make culling much worse. Instancing many repeated objects can help submission, yet still shade too many pixels. Transparent particles can be expensive even when their triangle count is low. A shader can be limited by texture traffic rather than its visible source-code length.

## Investigate with controlled changes

Lowering resolution can help diagnose pixel/shading pressure, but the rest of the frame also changes; confirm with GPU tools. Reducing visible object count can help diagnose submission/geometry work. Inspect GPU capture/timing and avoid comparing CPU submission time with asynchronous GPU completion time. Measure a representative camera path rather than one convenient view.

Use a sensible content budget for lights, shadow casters, texture resolution, particle coverage and expensive materials. Loading all assets “to avoid streaming” may replace hitches with memory exhaustion. Shader/pipeline preparation should be planned around the engine/platform; changing compilation policy blindly can shift stalls rather than remove them.

Read [Godot GPU guidance](research.md#r05), [RenderDoc](research.md#r19), [Nsight](research.md#r18) and [WebGPU](research.md#r36).

## Chunked worlds

[Chunk coordinates](../../mechanics/chunk-coordinates/README.md) only map positions into chunk/local coordinates. They do not load files or manage a streaming world. A real streaming layer needs states such as absent, requested, reading, decoded, prepared and resident, plus cancellation and ownership.

Prioritize nearby/soon-visible chunks, but use movement prediction and a bounded safety margin to reduce pop-in. Put limits on queued bytes, decoded memory and per-frame uploads. Moving disk reads off-thread does not make decompression, GPU upload or scene creation disappear. Cache carefully and unload resources no longer referenced.

Preserve negative-coordinate behavior when dividing the world. Test teleports, rapid direction changes, crossing chunk boundaries and returning to old areas. A stale background load must not install a chunk into a new world/session after cancellation.

## Procedural geometry, voxels and CAD

Generate mesh data separately from engine-object creation when the API allows. Rebuild dirty chunks/regions rather than the whole world, and avoid duplicate rebuild jobs. Shared edges, lighting and collision meshes can require neighboring updates. Background workers should produce owned data that the appropriate engine thread can safely install.

The [maze](../../mechanics/procedural-maze/README.md) and [extrusion](../../mechanics/cad-extrusion/README.md) examples do not implement streaming, voxel meshing or precision CAD booleans. Precision/tolerance requirements can dominate CAD decisions; visual simplification acceptable in a game may be unacceptable in an engineering model. Next: [networking and persistence](07-networking-persistence.md).
