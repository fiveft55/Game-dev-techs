# How game development technology evolved

This overview separates common trends from universal rules: old and new techniques coexist. Release examples are landmarks, not claims that a company invented a technique. Coverage reaches the contemporary 2020s; it is not a live census of every 2026 release.

## Foundations and the 1980s: constrained machines

Earlier mainframe experiments, arcade electronics, and home computers established interactive simulation. During the 1980s, limited RAM, CPU time, storage, and display hardware shaped both mechanics and art. Assembly and C were important; BASIC supported learning and many smaller projects. Tile maps reused small images; sprites moved independently of backgrounds. Character and ASCII worlds represented maps cheaply. Palette tricks, scanline effects, fixed-point arithmetic, and hand-tuned data layouts extracted more from hardware.

A development loop often involved cross-assemblers, custom map tools, emulators or hardware kits, and physical media. Tight budgets made data design inseparable from gameplay. Reusable lessons: compact state, explicit coordinate systems, predictable update loops, and tools built for designers.

## The 1990s: software 3D, acceleration, and network play

Raycasting and other constrained 3D techniques enabled navigable spaces on modest CPUs. Doom used sector-based level geometry and BSP techniques; it was not simply a grid raycaster. Quake moved to a different fully polygonal 3D architecture. Dedicated graphics hardware and APIs such as OpenGL and Direct3D shifted triangle rendering toward GPUs.

C and C++ grew across engine code; level editors and scripting separated content from engine internals. CD-ROMs enabled larger audio and video assets. LAN and Internet games exposed latency, synchronization, and bandwidth as design constraints. Deterministic lockstep suited some strategy games; authoritative client/server approaches suited many action games. These approaches still coexist.

## The 2000s: programmable GPUs and production pipelines

Vertex and pixel shaders made materials and lighting programmable. Skeletal animation, terrain, physics middleware, navigation meshes, and asset import pipelines became common engine capabilities. HLSL and GLSL expressed GPU work; C++, C#, Lua, Java, and other languages served different engine and tooling roles. Managed runtimes improved iteration for many teams.

Multicore processors encouraged job scheduling and careful ownership of data. Engines became integrated authoring environments rather than just renderers. Source control, automated builds, and asset validation became critical as teams and content grew. Browser Flash and Java ecosystems supported different delivery models from consoles and desktop engines.

## The 2010s: accessible engines, mobile, web, and services

Widely available engines lowered entry costs. Physically based rendering standardized material workflows, while deferred and forward techniques continued to evolve. Data-oriented design and ECS approaches helped manage large simulations, but were never mandatory for every project.

Mobile imposed thermal, memory, battery, touch-input, and device-fragmentation constraints. HTML5, JavaScript, WebGL, and later WebAssembly expanded browser options. Online games added persistent backends, telemetry, matchmaking, deployment pipelines, and operational security. VR emphasized low latency, stereo rendering, tracking, and comfort. Procedural generation and streaming helped build larger worlds without loading everything at once.

## The 2020s: scale, hybrid rendering, and automation

Hardware ray tracing, temporal reconstruction, virtualized geometry, improved streaming, GPU compute, and increasingly sophisticated animation pipelines broaden visual possibilities. Rasterization remains central, often combined with ray-based techniques. WebGPU offers a modern browser GPU programming model. Rust is used in some engine and tool ecosystems, while C++, C#, Lua, and JavaScript remain important in their domains.

Machine learning assists some animation, content, and coding workflows; output still requires technical validation and rights review. Real-time engines increasingly serve visualization, virtual production, and engineering. CAD differs from game mesh editing: precise geometry, topology, tolerances, constraints, and robust operations require specialized kernels. A triangle extrusion demo is not a production CAD system.

## What to learn independent of tools

1. Linear algebra, geometry, numerical integration, and floating-point limits.
2. Input sampling, fixed updates, rendering interpolation, and clocks.
3. Data ownership, profiling, spatial indexing, and serialization.
4. Authoring tools, reproducible builds, source control, and asset licensing.
5. Server authority, secure transports, latency handling, and operations.

See [sources](sources.md) for original engine repositories, standards, and technical explanations. See [roadmap](roadmap.md) for areas this first edition does not implement.
