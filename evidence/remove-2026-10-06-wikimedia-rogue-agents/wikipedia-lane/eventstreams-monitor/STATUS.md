# STATUS — eventstreams-monitor

**BUILT. NOT RUNNING. NOT SCHEDULED.**

Awaiting the user's word before anything here is executed against the live
stream, scheduled, or wired to any autostart mechanism.

## Component inventory (as built, review 2026-10-06)

| component | file(s) | verdict | tests |
|---|---|---|---|
| architect design | `DESIGN.md` | PASS (with noted drift — see below) | n/a (doc) |
| ingester entry point | `ingester/ingest.sh` | PASS (3 fixes applied) | `--dry-run` offline: config-valid OK / bad-config exits 2 |
| SSE processor | `ingester/process.py` | PASS (3 fixes applied) | `tests/test_process.py`: **36 checks, all pass** |
| ingester config template | `ingester/config.example.yaml` | PASS (1 fix: added `user_agent`) | validated via `--dry-run` |
| ingester docs | `ingester/README.md` | PASS (updated for accuracy) | n/a |
| detection engine | `detector/detect.py` | PASS (4 fixes applied) | `tests/run_tests.py`: **16 checks, all pass** |
| detection rules | `detector/rules.yaml` | PASS (2 fixes applied; provenance verified) | covered by run_tests.py |
| domain allowlist | `detector/allowlist_bibliographic_domains.txt` | PASS | 562 domains; incident domains absent (correct); spot checks pass |
| detector docs | `detector/README.md` | PASS (updated for accuracy) | n/a |

Total: **52 offline checks, 0 failures.** Plus an offline end-to-end smoke
test: fixture SSE → `process.py` CLI (hour rotation, resume cursor,
heartbeat) → `detect.py` (correct rules fire on raw EventStreams shapes).

## Fixes applied during review (kill-or-fix)

Ingester:
1. `ingest.sh` config-load failure was silent (`eval` of empty stdout →
   false "dry-run OK" / curl with empty URL). Now fails loud (exit 2).
2. SSE resume (`Last-Event-ID`) was designed (DESIGN.md §7) but unimplemented.
   Implemented: `process.py` captures `id:` lines → checkpoints
   `<out_dir>/state/<stream>.last_event_id`; `ingest.sh` sends it back on
   reconnect. Test-covered.
3. `process.py` derived wiki from `meta.domain` only — wrong for e.g.
   `www.wikidata.org` (→ `wwwiki`). Now prefers the canonical `database`
   field. Also fixed `page-delete` events being mistyped as
   `revision-create` (both carry `rev_id`; now disambiguated by
   `meta.stream`). Test-covered.
4. Backoff ladder never reset — one flaky hour would poison the next day's
   reconnect timing. Now resets after any connection surviving ≥60s (DESIGN §7).
5. No User-Agent was sent (DESIGN §6 requires one; WMF asks consumers to
   identify). Added `user_agent` to config example; `ingest.sh` sends `-A`.

Detector:
6. `normalize_event` ignored `performer.user_text` — raw `revision-create`
   events fed directly to `detect.py` failed with "missing required field:
   user", contradicting the README. Now normalizes `performer.user_text`,
   `database`/`meta.domain`→wiki, and guards `namespace: null`. Test-covered
   end to end.
7. Rules with missing `name` / unknown `type` crashed with a raw traceback
   (exit 1). Now clean exit 2 ("bad rules file"). Test-covered.
8. Removed dead `fire_once_per_window` params from `rules.yaml` (the engine
   ignores them; re-emit + consumer-dedupe is the documented behavior).
   Fixed provenance path `wikipedia-lane/revisions.tsv` →
   `wikipedia-lane/raw/revisions.tsv` (the file's actual location).

## Deliberately left as-is (documented, not broken)

- **No jitter on backoff** (DESIGN §7 wants it): the ingester README documents
  this as a deliberate choice. Left alone.
- **DESIGN.md drift**: one stream per ingester instance (not three in `bin/`),
  flat `raw/YYYY-MM-DD/HH.jsonl` layout (not `raw/<stream>/YYYY-MM-DDTHH`),
  no `rotate.sh` / `gaps.log` / canary-heartbeat watchdog, alert schema
  field names differ from DESIGN §3. The code + subdir READMEs are the
  authority; DESIGN §8's go-live command (`bin/ingest.sh`) is stale.
- **Not implemented from DESIGN §5**: `low-edit-count-burst` (needs a
  cross-stream recentchange→revision-create join — genuinely hard offline);
  `config-delete-watch` as a separate rule (subsumed: a `page-delete` on a
  `Web2Cit/data/` title trips `web2cit-config-edit` anyway).
- **Detector exit codes**: 0 = evaluated, 2 = malformed input / bad rules,
  3 = PyYAML missing.

## Constraint audit (2026-10-06)

- Python code: zero network usage (no socket/urllib/requests/httpx imports;
  `process.py` and `detect.py` read stdin/files only). `subprocess` appears
  only in the test runner to spawn `detect.py` locally.
- The ONLY network touchpoint is `curl -N` in `ingester/ingest.sh`, which
  never fires during `--dry-run` or tests (verified).
- No secrets, credentials, tokens, or private keys anywhere in the tree.
- No cron, systemd, or autostart artifacts created.

## What "go" requires

The user's explicit word, then the commands in README.md ("How it WILL run").
Before unattended operation: fill in the `user_agent` contact in
`ingester/config.yaml`, confirm ≥100 GB free for a 30-day retention target
(DESIGN.md §4 estimates ~2.5–3 GB/day — order-of-magnitude, calibrate from
the first captured hour), and run the 5-minute attended acceptance test.
