# Source registry and legal reuse

This library contains original educational code, including the 32 additional genre mechanics in the second edition. The links below are a curated reading list, not bundled dependencies. Upstream availability, current license terms, vulnerabilities, and compatibility must be checked at the exact revision before importing code. No commercial game code or extracted assets have been copied. Link checking is recorded separately and does not establish that every page was substantively reviewed.

## Algorithms and engine architecture

- https://gafferongames.com/post/fix_your_timestep/ — fixed simulation updates and interpolation.
- https://www.redblobgames.com/pathfinding/a-star/introduction.html — pathfinding visual explanations.
- https://lodev.org/cgtutor/raycasting.html — grid raycasting tutorial; examples have their own terms.
- https://gameprogrammingpatterns.com/ — architecture patterns; consult the book/site terms before reusing text or code.
- https://www.reynoldssteering.com/ — autonomous steering references.
- https://box2d.org/documentation/ — a real physics engine's concepts and limitations.
- https://docs.godotengine.org/en/stable/ — engine/editor, rendering, networking, and scripting documentation.
- https://docs.blender.org/manual/en/latest/ — modeling and content workflows.
- https://dev.opencascade.org/ — precise CAD geometry and topology ecosystem.

## Historical primary code and collections

- https://github.com/id-Software/DOOM — historical engine source; read the license in the chosen revision. Game data is a separate rights question.
- https://github.com/id-Software/Quake — historical polygonal engine source; inspect GPL obligations and separate asset rights.
- https://www.computerhistory.org/ — historical collections and exhibits.
- https://www.museumofplay.org/ — game-history collections and research.
- https://www.khronos.org/opengl/ — graphics API history and specification resources.
- https://www.w3.org/TR/webgpu/ — WebGPU specification.

## Multiplayer code to evaluate, not blindly vendor

- https://github.com/lsalzman/enet — reliable UDP networking; inspect LICENSE and note that reliability is not encryption.
- https://github.com/ValveSoftware/GameNetworkingSockets — transport library with connection/security facilities; inspect README and license.
- https://github.com/heroiclabs/nakama — online game backend; inspect server, client, and commercial-feature licensing separately.
- https://github.com/colyseus/colyseus — multiplayer framework; inspect package and server deployment requirements.
- https://github.com/boardgameio/boardgame.io — turn-based game framework; inspect current maintenance and package terms.

## Security standards and guidance

- https://www.rfc-editor.org/rfc/rfc8446 — TLS 1.3.
- https://www.rfc-editor.org/rfc/rfc9000 — QUIC.
- https://www.rfc-editor.org/rfc/rfc8831 — WebRTC data channels.
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html — password storage.
- https://cheatsheetseries.owasp.org/cheatsheets/WebSocket_Security_Cheat_Sheet.html — WebSocket security.

## Import policy

Record upstream URL, exact commit, file paths, license identifier, copyright notices, modifications, and execution/tests in a per-import provenance file. Preserve license and attribution text. Review copyleft obligations before mixing code into distributed products; some licenses require source distribution under defined conditions. Treat art, music, fonts, datasets, trademarks, and patents separately from source-code licensing.

Public visibility does not mean public domain. Private visibility does not grant reuse rights. Reverse engineering does not automatically legalize copying or distribution; laws and contracts vary. Prefer documented interfaces, permitted clean implementations, and explicitly licensed code. This policy is engineering guidance, not a legal opinion on a particular product.
