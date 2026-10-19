# 10. A reproducible benchmark recipe

A benchmark is a controlled question, not a trophy number. This handbook adds no new measured game-performance result; the following is a procedure for producing one.

## Example question: is a spatial index worthwhile?

Compare a direct point-radius scan with an indexed query using exactly the same points, query centers and radius. For the current Python spatial-hash module, use a cell size at least the query radius, ask `nearby` for candidates, and apply the **same exact distance test** to those candidates. Candidate lists alone are not the same answer as exact hits.

Include:

1. Uniformly spread points, dense clusters, negative coordinates and boundary cases.
2. Small, medium and large populations; state their exact sizes.
3. Several query counts per rebuild. One query can favor a scan; many queries can amortize an index build.
4. A moving-world variant that includes rebuilding or maintaining the index.
5. The exact same stable identifiers and result comparison; ignore order only if order is not part of the contract.

Before timing, verify every optimized result against the direct reference on the selected workload. If results differ, investigate before reporting speedups. Inspect the current [spatial-hash limits](../../mechanics/spatial-hash/README.md): a nine-cell query is not a general arbitrary-radius shape query.

## Timing rules

Use a monotonic high-resolution clock such as Python's `time.perf_counter_ns()`. Measure complete useful batches, not one timer call around a few instructions. Pre-generate inputs outside the measured region unless input generation is part of the workload being studied. Consume results so a compiler cannot simply eliminate unused work.

Separate and report build, query and total cost. Run multiple trials and alternate/randomize baseline/candidate order when order could bias cache or thermal state. Record warm-up policy for JITs, caches and shader pipelines. Include a cold-start measurement separately when relevant.

Do not disable GC and then present the result as normal managed-game performance. If you run a special no-GC experiment, label it as such and still measure the normal configuration. Subtracting an empty-loop timing is not universally reliable: compiler and runtime behavior can change the work itself.

Report median and a tail statistic with sample count, workload and percentile method. For very short batches, choose sufficiently large batches/trial counts; do not publish unstable “nanoseconds per entity” precision unsupported by the experiment. Avoid choosing only the best trial. Repeated independent runs help distinguish noise from a real improvement.

## Amortization arithmetic

Let `B` be index-build time, `Q_i` total indexed-query time and `Q_s` total scan-query time. The indexed approach wins for that workload only if `B + Q_i < Q_s` when a rebuild is required. For reuse across frames, include updates, invalidation and retained-memory costs as well.

Illustration only: if building costs 2 ms and each indexed query saves 0.01 ms, roughly 200 such queries are needed just to break even on that build, assuming other costs are equal. These numbers are invented to explain the equation; they are not library timings.

## Result record template

```text
Question and hypothesis:
Baseline commit / candidate commit:
Hardware, OS, compiler/runtime/engine, build flags:
Resolution/settings/power/thermal conditions:
Input generator, seed, dataset sizes and distributions:
Correctness oracle and result:
Warm-up policy, trial count and run order:
What is included/excluded in each timed region:
Build / update / query / end-to-end times:
Median / p95 / p99 with sample counts and method:
Memory peak, allocations, relevant work counters:
Observed improvement and uncertainty/noise:
Regressions, break-even point and worst case:
Decision: keep, revise, or reject:
```

Save the harness and raw results with the write-up. Do not compare two runs that quietly used different maps, physics rules, compiler checking, visibility policy or network payloads. A microbenchmark can guide an implementation choice; follow it with a game-level replay on the target device. [Measurement](01-measurement.md) explains why.
