# DATA-AUDIT — repo hygiene for the main merge

**Repo:** `~/workspace/silent-locus` · **Branch:** `investigation-2026-10-05` @ `346d9406` (pushed to origin, in sync)
**Date:** 2026-10-06 · **Auditor:** DATA-AUDIT (coordinator) + 4 workers
**Worker reports:** `DATA-AUDIT-workers/{secret-sweep,size-audit,license-audit,dangling}.md`

## Verdict

**The pushed tree is clean and mergeable.** Zero live secrets, zero files over GitHub's 100MB hard limit, zero redistribution violations, zero broken symlinks. Push protection has already accepted everything tracked in HEAD.

**Blockers for the main merge (must fix first):** 2 dangling gitlinks (one is a regression), 1 committed `.pyc`. All fixable with non-destructive commands below — no history rewrite needed.

---

## Can-go-up / needs-allow-list / must-stay-local

### ✅ CAN GO UP (clean)

| Item | Notes |
|---|---|
| Entire pushed tree @ `346d9406` (6,342 files) | Already on origin; push protection accepted it |
| `docs/` onboarding READMEs (untracked, new) | `animation/README.md`, `data/.../README.md`, `german-french-swarm-hunt/README.md`, `studies/skill-egress-top1000/README.md` — intended for commit |
| Modified `README.md`, `collections/eval-questions/README.md`, `data/.../slug-hunt.py` | Post-push working-tree changes; commit normally |
| `DATA-AUDIT-workers/` | This audit's working files (or move to hidden_files/) |
| `why-these-sites/workers/index-hunter/FINDINGS.md` (42 KB, untracked) | Clean per secret-sweep (only `T00/B00/XXX` placeholders); **but see allow-list row** — it was flagged alongside the file below in the same blocked push |

### ⚠️ NEEDS ALLOW-LIST (push protection will block again)

| File | Flagged value | Why it's safe to allow |
|---|---|---|
| `data/2026-09-28-chinese-amap-fleet/studies/skill-egress-top1000/why-these-sites/workers/index-hunter/FINDINGS.md:128` | `hooks.slack.com/services/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` | Published IOC from the public `nodejs-backpack` npm-surveillance-malware writeup (Jul 2025), quoted as evidence. Not anyone's credential. |
| `data/2026-09-28-chinese-amap-fleet/village-join/our-urls-raw.txt:536569` | Same Slack URL | Same value, inside a 619k-line harvested-URL scratch dump. |

**Decision needed:** either (a) BigSexyWarlock69 approves the allow-list at the secret-scanning unblock URL and both files get committed, or (b) the FINDINGS.md gets committed after allow-list while `our-urls-raw.txt` stays local (recommended — it's 45.8 MB of intermediate scratch; gitignore it instead).

### 🔒 MUST STAY LOCAL (never push)

| Item | Size | Mechanism |
|---|---|---|
| `collections/eval-questions/mind2web/raw/` | 6.1 GB (incl. test.zip) | gitignored (`.gitignore:219`); test split excluded per author terms |
| `collections/eval-questions/swe-bench/raw/` | 115 MB | gitignored (`:220`) |
| `collections/eval-questions/anthropic-evals/raw/` | 94 MB | gitignored (`:221`) |
| `collections/eval-questions/sealqa/raw/` | 70 MB | gitignored (`:222`) |
| `collections/eval-questions/tau-bench/raw/` | 66 MB | gitignored (`:223`) |
| `data/.../village-join/our-urls-raw.txt` | 45.8 MB | **untracked AND unignored — add to .gitignore (see fix)** |
| `collections/re-hunt-patterns/data/hits.jsonl`, `openai-agent-traces/data/traces.jsonl` | >50 MB each | gitignored (`:212`–`:213`) |
| Nested repo `.../pastebin-plunderer/.../ref/run1/` contents | ~300 MB | gitlink (local-only per `a3e2e36f` intent); nested `.git` quarantined |
| AI Village 5.1 GB tables | gone from VM | never in repo; only derived join excerpts are tracked |

---

## Worker findings (summary counts)

| Worker | Result |
|---|---|
| SECRET-SWEEP | 52 unique non-bulk hits + 472 bulk scan-JSON entries. **0 live-suspicious.** 25 test-fixture · 22 published-IOC · 5 false-positive. 0 private keys. |
| SIZE-AUDIT | **3 tracked files >50 MB** (70.8 / 66.8 / 53.3 MiB — arquivo.pt timelines, oai-tag events). **0 files >100 MB.** No merge blocker. |
| LICENSE-AUDIT | All 20 eval dirs have license records in NOTES.md. **No repo LICENSE** (README says undecided). **0 redistribution violations** (mind2web test split excluded, xbench plaintext not banked, BrowseComp ciphertext only, AI Village data not in repo). |
| DANGLING | **2 gitlinks (must-fix)** · 0 broken symlinks · 1 committed `.pyc` (must-fix) · 14 scripts with hardcoded `/home/hatch` (recommended) · 0 junk dirs · 0 screenshot dumps |

---

## Must-fix before merge (exact commands)

```bash
cd ~/workspace/silent-locus

# 1. Remove the two dangling gitlinks from the index.
#    Files stay on disk; nested repos remain local-only. No history rewrite.
#    NOTE: ref/run1 is a REGRESSION — a3e2e36f deliberately removed it and
#    346d9406 re-added it. This restores the intended local-only status.
git rm --cached collections/eval-questions/openai-mle-bench/raw/mle-bench
git rm --cached data/2026-09-28-chinese-amap-fleet/personas/pastebin-plunderer/raw/deep-dive/lane3-colony-bullfincher/ref/run1

# 2. Drop the committed .pyc bytecode file
git rm data/2026-06-17-reverse-tunnels/raw/run-logs/htmx_search.cpython-312.pyc

# 3. Extend .gitignore (exists, 223 lines — append)
cat >> .gitignore <<'EOF'
*.pyc
__pycache__/
.DS_Store
data/2026-09-28-chinese-amap-fleet/village-join/our-urls-raw.txt
EOF

# 4. Decide on mle-bench: either track its files as regular blobs
#    (rm -rf collections/eval-questions/openai-mle-bench/raw/mle-bench/.git && git add <dir>)
#    or leave the dir untracked. Do NOT re-add as gitlink.

# 5. Commit + push (then the allow-list decision below determines whether the
#    2 flagged files join this commit or stay out)
git add -A
git commit -m "Repo hygiene: drop dangling gitlinks, remove committed .pyc, extend .gitignore"
git push origin investigation-2026-10-05
```

## Recommended, non-blocking

```bash
# De-hardcode the 14 scripts (onboarding portability). Pattern per script:
#   python: HERE = os.path.dirname(os.path.abspath(__file__))
#   bash:   DIR="$(cd "$(dirname "$0")" && pwd)"
#   skill path: "$HOME/workspace/skills/urlquery/bin/uq.py" instead of /home/hatch/...
# Files: collections/hunt-missed-surfaces/hot-leads/{cc_probe_batch,cc_probe_retry,cc_probe_retry2,urlscan_batch,urlscan_retry}.py
#   data/.../german-hunt/{priority_sweep,sweep}.py, data/.../slug-hunt.py
#   data/.../live-monitor/monitor_loop.sh, data/.../new-fleets/{collect_gapfill2,retry_loop}.sh
#   data/.../personas/cartographer/raw/redirector_sweep.py
#   data/.../personas/ghost-hunter/raw/egress_watcher.py
#   data/.../personas/metronome/{build_baseline,raw/cadence_profiler}.py

# Record AI Village terms in village-join/ (research/analysis only; no training w/o permission)
# Fix gaia NOTES.md license record: "unspecified" -> CC-BY-4.0 (0 questions banked; record hygiene only)
# Add one-line provenance headers to collections dirs lacking READMEs
#   (arquivo-pt, fake-org, sec-county-watch, urlscan-cc-feeds, re-hunt-*)
```

## Decisions needed from BigSexyWarlock69

1. **Allow-list the published Slack IOC?** (unblock URL from the blocked push) — determines whether `index-hunter/FINDINGS.md` + `our-urls-raw.txt` can be committed, or stay local.
2. **Repo license** — README says undecided; composite inherits most-restrictive (CC-BY-4.0 attribution). Needed before any public release beyond this push.
3. **`mle-bench` nested dir** — track as regular blobs or leave untracked (after gitlink removal).

## Merge-readiness checklist

- [x] Pushed tree: 0 live secrets · 0 files >100 MB · 0 redistribution violations · 0 broken symlinks
- [ ] Fix 2 gitlinks + 1 .pyc, extend .gitignore, push (commands above)
- [ ] Allow-list decision on the 2 flagged files
- [ ] Merge `investigation-2026-10-05` → `main` via PR (never push to main directly; no history rewrite)
- [ ] Post-merge: de-hardcode scripts, record AI Village terms, provenance headers (non-blocking)
