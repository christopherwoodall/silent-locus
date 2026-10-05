# HF hygiene scan — 2026-09-29 (worker 3/5)

Read-only scan of `~/workspace/silent-locus` on branch `local` (12 unpushed commits at scan time).
No commits made. Working tree had 5 modified-but-unstaged files under `hidden_files/` (lane12 logs, `watch_heartbeat.txt`) from other live workers — left untouched. One untracked file present: `scripts/gen_dataset_card_table.py`.

Scope: 3,465 tracked files. Working tree (excl. `.git`): 283 MB. `.git`: 662 MB (full merged history).

## 1. Secrets — CLEAN

- `git grep` for `ghp_`, `github_pat_`, `AKIA[0-9A-Z]{16}`, `-----BEGIN ... PRIVATE KEY-----`: **zero hits** in tracked files.
- `git log -S 'ghp_' --oneline --all` and `git log -S 'github_pat_' --oneline --all`: **zero commits** — the PAT never appears anywhere in history.
- `.git/config` is **not tracked** (`git ls-files | grep -x '.git/config'` returns nothing). It contains 1 match for the PAT pattern (verified by count only, value never read) — lives locally only, never committed.
- No tracked `.env`, `credentials*`, `*secret*` files, `id_rsa`, `*.pem`, `token.json`.
- `kibana-exports/` + `elk/`: no password/key hits.
- No `https://user:pass@host` credential URLs (hits were test-proxy strings, wiki-spam bodies, and JSON-LD `"@type"` schema.org strings — false positives).

Secret-*looking* values that are **dataset content, not our credentials** (flagged for awareness, not removal — the keep-all + annotate policy covers them):
- DPLA API key `910de961922b85c6e95ee1311938ece6` — agent-posted wiki spam URLs in `data/2026-05-17-collusion-wiki/raw/revisions.jsonl` (lines 928–930, 1736, 1986–1989, 2008, 9704) and derived `data/aggregates/2026-09-29-overlap-analysis/raw/wiki_ioc_pivots.jsonl` (lines 1707, 6215). Public DPLA demo key, part of the evidence.
- `controller_api_key=<redacted>` / `DEFAULT_API_KEY=<redacted>` in `data/2022-08-09-github-forensics/raw/fix-commit-e4123d04.diff` — already redacted at capture.
- `apiKey: '6cedc0f0f25c226daa9a9451645297c05efbc80a'` in `data/processed/gems/southnews-payload1-35329-0.0.2/payload.rb:71` — reconstructed malicious gem payload (campaign artifact).
- `ELASTIC_PASSWORD=<redacted>` etc. in `docker-compose.yml` — already redacted.
- `new.appwrite.io/reset?userId=…&secret=…` URLs in `data/2025-12-04-urlquery-marker-sweep/raw/` — captured IOC data, not ours.
- `data/2026-02-14-md-succ-ai/raw/repo/src/proxy-pool.mjs:122` — proxy-parsing code, no real secret.
- `data/2026-03-12-paste-archive-gap/raw/bodies/anna.fyi/56d1f0ea.txt:121` — paste content referencing `$MYSQLUSERPASS` env var, not a real secret.

## 2. Absolute home paths (`/home/hatch`) — 5 files, 6 hits

Real offender (functional code):
- `scripts/extract_f1f2.py:10` — hardcoded `HUNT = "/home/hatch/workspace/muse-home/projects/urlquery-api-hunt"`. Should be relativized or env-var-driven before publish.

Minor / self-referential (mention the path only in prose about the scrub rule or as history):
- `notes/cascade-synthesis-2026-09-28.md:131` — the grep pattern quoted in prose.
- `notes/hygiene-2026-09-28.md:53,57,60` — same, rule described in prose.
- `data/2026-05-05-gomod-hunt/raw/chunk.py:13` — comment: `was /home/hatch/workspace/tmp-gomod; relocated 2026-09-28`.
- `temp/build_w4.py:6` — usage docstring `/home/hatch/workspace/silent-locus` (in migration-scratch `temp/`, see clutter).

`/home/muse` hits: only the same two notes, self-referential. No `C:\Users` / `/Users/` style paths found.

## 3. PII — no private-individual data found

- Emails in tracked files are all campaign/dataset artifacts: `openaixyz65947@gmail.com` (swarm gmail, cited in `notes/gem-hunt-openai-incident-2026-09-27.md:125` and `notes/gem-public-intel-2026-09-27.md:16,39` as incident evidence), `testing{lion,wolf,rhino}@apexblack.org` (gem author names), `*@mailinator.com` throwaways, `claude-code@iskogen.nu` (swarm agent email, in events.jsonl), `diffend@whitesourcesoftware.com` (Diffend snapshot metadata), `none@example.com` / `test@test.com` / `scanner@example.com` placeholders.
- No phone numbers in `notes/`, `scripts/`, `schema/`.
- Name mentions of "Christopher" in notes = the repo owner (Christopher Woodall); expected, his name is on the dataset per the HF repair directive.
- events.jsonl spot-check: 66 files; sampled 116 records (first lines) + label-key census over full files + email regex over first 200 lines of each. Top-level schema is the shared schema (`@timestamp`, `event`, `fingerprint`, `labels`, `record_kind`, `source_url`, …); labels are taxonomy keys (`gem.name`, `wiki`, `page`, `shortener.*`, `paste.id`, `venue`, …). **No operator/registrant/real-name/submitter fields.** Hunt scope (agents + infrastructure only, no person-focused attribution) confirmed intact.

## 4. Size — no HF limits tripped

- Working tree (excl. `.git`): 283 MB. Largest single files: 40 MB `data/2026-05-17-collusion-wiki/raw/revisions.jsonl`, 31 MB `data/2026-09-28-dockerhub-trojan-images/events.jsonl`, 21 MB `data/2026-05-17-collusion-wiki/raw/records.jsonl`, 17 MB `data/2026-05-05-gomod-hunt/events.jsonl`, 15 MB `data/raw/redacted.jsonl.gz`, 15 MB `data/aggregates/2026-09-29-overlap-analysis/events.jsonl`, 14 MB `data/2026-05-17-collusion-wiki/events.jsonl`, 12 MB `…/raw/wiki_ioc_pivots.jsonl`, 11 MB `…/raw/links.jsonl`, 7.6 MB `data/2025-03-04-rubygems-goimport-campaign/events.jsonl`, then 5.4/4.1/4.0/4.0/3.7/3.1/2.9/2.6/2.5/2.4/2.2 MB.
- **No file needs git-lfs** (max 40 MB; plain git on HF handles this fine). Total 283 MB working tree is well within HF dataset-repo norms.
- `.git` is 662 MB (merged 110-commit history + 12 unpushed). Only matters for clones of this repo, not for a fresh HF dataset push.

## 5. `.gitignore` — covers byte-code/logs, NOT `temp/` or `hidden_files/`

- Covers `__pycache__/`, `*.py[cod]`, `*.log`, `.env`, `elk/data/`. Does not cover `temp/`, `hidden_files/`, `kibana-exports/`.
- Tracked files that look like runtime junk (committed despite `*.log` in gitignore — the hunt's "captures to disk + git" provenance habit; needs a publish decision):
  - `data/2026-07-07-july7-gem-forensics/progress.log`
  - `data/2026-09-29-gem-temporal-pivot/raw/run-logs/diffend_temporal_sweep.stdout.log`
  - `data/2026-09-29-separate-eval-test/raw/run-logs/progress.log`
  - 78 tracked files under `hidden_files/` (lane queues, sweep logs, working JSON — internal bookkeeping the repo convention says "the user should not see")
  - 38 tracked files under `temp/` (one-shot migration scripts: `build_w4.py`, `backfill_w*.py`, `phase2_patch_*.py`, `rewrite_datasets_*.py`, `layout_sweep.py`, …)
  - 24 tracked files under `kibana-exports/` (dashboard ndjson exports — viz artifacts, not dataset data)
- Recommendation for HF publish: exclude `temp/`, `hidden_files/`, `kibana-exports/`; decide whether run `*.log` files under `data/` stay as provenance or move.

## 6. Leftover clutter — reported, not deleted

- On-disk but **untracked** (ignored, harmless, will not be committed): `hidden_files/lane1/__pycache__/` (4 `.pyc`), `data/2026-06-17-reverse-tunnels/raw/run-logs/htmx_search.cpython-312.pyc`. Zero `.pyc` files are tracked.
- No `__pycache__` tracked anywhere (`git ls-files | grep -c '__pycache__'` = 0).
- Odd filename (UTF-8 arrow in name, from gem reconstruction): `data/processed/gems/yard-controllerlambda-0.0.3/lib/{yard-lambdak.rb → yard-controllerlambda.rb}` — git/HF handle it, but flagged.

## Publish-readiness summary

Blockers: none on secrets/PII/size. Fix before publish: `scripts/extract_f1f2.py:10` absolute path. Decide before publish: exclude `temp/`, `hidden_files/`, `kibana-exports/` from the HF dataset; keep-or-move run `*.log` files under `data/`; the DPLA API key in wiki raw data is campaign evidence (keep, it's already public in the wiki corpus).
