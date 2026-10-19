# 7. Multiplayer, saves and persistent state

Sending less unnecessary data is often more useful than encoding the same unnecessary data slightly faster. Keep server authority and security while reducing work.

## Budget each stage

Track server tick time, per-client relevant entities, encoded/decoded bytes, messages per second, send queues, RTT, jitter, loss/retransmission, client interpolation delay and database latency. Tick rate, snapshot rate and render rate can differ. Raising all three increases work and bandwidth without guaranteeing a better experience.

A rough application-payload estimate is:

`bytes/sec = updates/sec × relevant_entities × bytes_per_entity`.

Illustration: 20 updates/sec × 100 entities × 24 bytes gives 48,000 bytes/sec per client **before** transport headers, acknowledgements, encryption overhead, retransmission and other messages. This is arithmetic, not a measured network budget.

## Interest, deltas and precision

The [interest filter](../../mechanics/interest-management/README.md) scans entities and applies an authorization predicate before distance filtering. It is not a spatially indexed replication server. An index can reduce candidate search, but authorization and field visibility must still be applied before serialization. Never send hidden enemy positions merely because they are nearby.

Delta updates send changes relative to a known baseline. You need an acknowledgement/baseline policy, recovery from missing state, creation/destruction messages and a full-resync route. Quantization reduces position/angle precision to save bits; set an error budget and test boundaries, overflow and gameplay fairness.

Compression can reduce bytes while increasing CPU, latency, buffering and memory. Small messages may become larger after framing. Measure full encode/send/decode cost, not just compression ratio. Avoid mixing secrets and attacker-controlled data in compressed messages without a security review. Compression, Base64 and checksums are not encryption. See [LZ4](research.md#r35) as an implementation to evaluate, not a bundled dependency.

## Smoothness versus simulation

[Snapshot interpolation](../../mechanics/snapshot-interpolation/README.md) smooths displayed remote motion by deliberately rendering behind current server time. Prediction/reconciliation can reduce local perceived delay but add simulation and correction work. [Rollback](../../mechanics/rollback-resimulation/README.md) may replay many updates after a correction; bound stored history and measure the worst replay burst, not only normal frames.

[Replay protection](../../mechanics/replay-window/README.md) rejects repeated sequence numbers after authentication. Do not delete it or weaken transport validation for a timing improvement. [Server input checks](../../mechanics/server-input-validation/README.md) are only a rule kernel: authentication, schema bounds, rate limiting and one-command-per-tick enforcement remain application duties.

## Persistence and saves

Use batch writes when consistency rules permit; batch size and deadlines affect latency. Critical economy changes need transactional/idempotent handling, not an unbounded fire-and-forget queue. Measure database waits separately from simulation CPU. Bound request size, connection counts, queued work and retries.

The Python [save migration](../../mechanics/save-migration/README.md) parses and validates a small JSON schema; native ports migrate an already decoded minimal record. Neither is a database or encrypted save service. Avoid serializing the entire world every render frame. Save changed regions or checkpoint at explicit safe times, preserving atomicity/recovery and schema-version compatibility.

The [offline progress](../../mechanics/offline-progress/README.md) equation does not prevent duplicate reward claims. A faster calculation without authoritative time and atomic claiming can still break the economy.

Read [state synchronization](research.md#r12), [QUIC](research.md#r33) and the existing [multiplayer security guide](../multiplayer-security.md). Next: [concurrency](08-concurrency.md).
