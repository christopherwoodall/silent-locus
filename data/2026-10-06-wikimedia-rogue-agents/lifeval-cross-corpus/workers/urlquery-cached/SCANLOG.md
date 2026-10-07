# urlquery-cached worker — scan log (2026-10-06)

Corpus root: ~/workspace/silent-locus/data/
Excluded: .git, 2026-10-06-wikimedia-rogue-agents/ (the lane itself)
File scope: *.json *.jsonl *.csv *.txt (3,678 candidate files)
Method: rg -i (ripgrep 14.1.0), exact-string patterns, per-file counts
Grades: OBSERVED / INFERENCE / UPSTREAM / NOISE

Patterns:
- p1 "Lifeval temporary technical sandbox initialization"
- p2 "Lifeval API temp-account test"
- p3 "Lifeval" (standalone; expect Tokyo Gas sponsor noise -> killed-by-noise appendix)
- p4 "Temporary technical sandbox initialization" (p1 is a strict subset of p4's hit set)
- p5 "sandbox test link" | "testing external link" | "Sandbox link test" | "Temporary technical sandbox"

## scans
- [ ] p1 single-pass (running as proc_6c764abf4a05)
- [ ] combined pass p2/p3/p4/p5 (single rg pass, -c per file)
- [ ] context extraction + grading per surviving file
- [ ] provenance cache of real hits into lifeval-cross-corpus/raw/ (bytes + source path + retrieval time + sha256)
- [ ] FINDINGS.md

## 2026-10-06 19:05 CDT — finisher note (account-profiler finisher session)
The two rg scans launched ~18:32 CDT were still running at 19:05 with no output.
SUPERSEDED: the disk-corpora worker completed an equivalent-or-broader sweep
(2026-10-06 ~18:16-18:25 CDT, `~/workspace/silent-locus/data/` + muse-home/projects,
FINDINGS.md written, one real survivor cached). These urlquery-cached scans cover a
subset of that scope (excludes the wikimedia-rogue-agents lane, no muse-home).
When they finish, record the verdict line here; do not re-grade survivors already
covered by disk-corpora/FINDINGS.md.

## 2026-10-06 19:15 CDT — scans reaped, output lost
Both rg processes (pids 1909/1910) exited by 19:15; their stdout was attached to the
pre-drain session and is unrecoverable. No verdict line can be recorded. This worker's
scope is fully covered by disk-corpora/FINDINGS.md (broader sweep, completed,
verdicts written). CLOSING urlquery-cached as superseded-redundant; no further work.
