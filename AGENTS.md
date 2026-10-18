# Repository maintenance

Use the existing checkout; cloud tasks are already isolated. Do not create worktrees unless requested.

Read README.md, catalog.json, docs/roadmap.md, and docs/sources.md before extending coverage. Each mechanic belongs under mechanics/<descriptive-id>/<language>/. Keep unrelated mechanics separate; explain units, assumptions, limitations, execution commands, and source provenance in its README. Prefer original code; retain third-party license notices if importing authorized code. Do not portray missing ports, sketches, or unrun checks as complete.

Run python3 tools/validate.py for the Python library. Compile/run affected language examples where toolchains exist and report unrun languages. Do not introduce custom cryptography, secrets, copyrighted game assets, or unverifiable historical claims. Update catalog.json and docs/mechanics-index.md when adding implementations. Commit coherent increments; push only when authorized by the user. Never claim autonomous work continues after the active session ends.

Maintain genre-coverage.json whenever adding mechanics. Regenerate indexes with python3 tools/build_indexes.py. Run python3 tools/validate.py and python3 tools/build_indexes.py --check before committing. The validation suite checks that all documented genre families are mapped and every catalog entry has tested Python code.

Native ports: all 51 mechanics have numeric kernels in Lua, C#, GDScript, TypeScript, JavaScript, C, Rust and Go. Preserve API/scope differences documented in PORTS.md. Edit tools/ports/specs.py and explanations.py, then run tools/ports/generate.py and tools/ports/document.py. Regenerate indexes and test affected native languages with tools/test_ports.py; missing tools must not count as passed. Include plain-English purpose/steps and comments explaining every helper function. C entry points must remain unique and all linked units must share the same PORT_CAPACITY.
