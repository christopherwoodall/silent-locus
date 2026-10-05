# NOTE — `htmx_search.cpython-312.pyc` in this directory

**What this is:** the compiled bytecode of the `htmx_search.py` tool used in
the reverse-tunnels hunt lane (LANE C: read-only urlquery HTMX search for
reverse-tunnel hostnames).

**History:**
- The original `.pyc` (compiled 2026-09-28 23:29) was deleted on 2026-09-29
  after its embedded constants were verified against the surviving source.
  The source survives at `scripts/reverse_tunnels_htmx_search.py` (tracked).
- On 2026-09-29 the file was **re-added by recompiling** the original
  pre-normalization source
  (`data/reverse-tunnels/htmx_search.py` from the pre-move archive).
  Recursive structural comparison confirms the recompiled bytecode is
  identical to the source in all constants, names, docstrings, and query
  strings. It is **not byte-identical** to the deleted original — the `.pyc`
  header embeds the compile-time source mtime, which cannot be reproduced.

**Why it's tracked:** per operator direction, kept as a curated run artifact
of the hunt tooling. Exempted from the repo `*.py[cod]` gitignore rule (see
the `!` negation in `.gitignore`); checksummed in this collection's
`SHA256SUMS`.
