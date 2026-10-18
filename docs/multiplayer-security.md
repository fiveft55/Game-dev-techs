# Multiplayer and data protection

## A useful architecture

Clients send input intentions to an authoritative server. The server authenticates the session, validates message schemas and rate limits, advances game rules, and sends only the state each client is permitted to know. The client predicts local movement and reconciles with server acknowledgements; remote entities usually render from a delayed snapshot buffer.

The included snapshot interpolation and replay-window modules demonstrate two isolated concepts. They are not a multiplayer engine or secure transport. A deployable multiplayer server and end-to-end transport test remain roadmap items.

## Encryption: use established transports

- For browser clients, use HTTPS and WSS through a maintained TLS implementation with normal certificate and hostname validation. TLS 1.3 is specified in RFC 8446.
- QUIC (RFC 9000) integrates a TLS-based handshake and can support independent streams. Select a mature implementation and a protocol suited to your latency needs.
- WebRTC data channels use DTLS/SCTP and require signaling plus ICE connectivity handling. Signaling also needs authentication and HTTPS/WSS.
- A raw UDP socket, encoded JSON, Base64, XOR, and a checksum do not encrypt or authenticate a game session.
- Do not implement your own cipher, handshake, key exchange, or nonce management. If application-layer encryption is actually needed, select a reviewed protocol/library and obtain a threat-model review.

## What encryption does not solve

An authenticated client can still cheat. Validate speed, inventory changes, fire rates, economy operations, and ownership on the server. Do not send secret enemy positions and assume encryption hides them from the receiving player. TLS does not stop replay of a valid application request by an authorized user; use session-bound sequence numbers and idempotency keys where appropriate.

The replay-window example must be called only AFTER successful authentication, or forged packets could advance its state and exclude real traffic. Bound packet size and sequence encodings before parsing. Reset sequence state for a fresh authenticated session; do not silently wrap counters or share windows across users.

## Persistence

Use parameterized queries and database transactions for inventory and economy updates. Store password hashes with a maintained password-hashing library, typically Argon2id according to current deployment guidance; do not store plaintext or reversible passwords. Keep keys in a secrets manager, enforce least privilege, encrypt backups, and test restoration. Encryption at rest complements access controls; it does not replace them.

## Production validation checklist

Test unauthorized joins, malformed messages, duplicate packets, out-of-order packets, disconnect/reconnect, packet loss, jitter, timeouts, overload, and concurrent writes. Add observability without logging tokens or sensitive player data. For a public service, plan abuse handling, denial-of-service protection, patching, and privacy obligations.

## Upstream code worth studying

See the source registry for ENet, GameNetworkingSockets, Nakama, Colyseus, and boardgame.io. These have different transport guarantees and scopes. A project's presence on this list is not an endorsement of every version or a statement that its code was imported or tested here.
