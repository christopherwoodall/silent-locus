# eventstreams-monitor — Wikimedia EventStreams ingest + monitor

**Status: BUILT, NOT RUNNING, NOT SCHEDULED.** Offline build only. No
connection to `stream.wikimedia.org` has ever been made from this directory;
no cron jobs, systemd units, or background processes exist for it. See
STATUS.md.

## What this is

A live monitor for agent-shaped activity on Wikimedia wikis, built for the
2026-10-06 rogue-agent hunt (WMF disclosure 2026-10-05): `~2026-*`
temp-account sandbox bursts, Web2Cit config tampering (the incident's
fetch-oracle primitive — community-editable templates at Meta-Wiki
`Web2Cit/data/` that cause `web2cit.toolforge.org` to fetch a target
server-side), temp-account fleet creation, and census probe-token grammars.

## Architecture (10 lines)

1. `ingester/ingest.sh` owns a persistent `curl -N` SSE connection per stream
   (Python HTTP stacks break on this VM's egress proxy; curl works).
2. Raw SSE bytes pipe into `ingester/process.py` (stdin only — provably
   network-free), which writes verbatim JSONL to
   `<out_dir>/raw/YYYY-MM-DD/HH.jsonl` (UTC hours, from each EVENT's timestamp).
3. `process.py` captures SSE `id:` lines and checkpoints them to
   `<out_dir>/state/<stream>.last_event_id`; `ingest.sh` sends the cursor back
   as `Last-Event-ID` on reconnect (DESIGN.md §7).
4. `ingest.sh` loops forever with exponential backoff (2s×2, cap 300s),
   resetting the ladder after any connection that survives ≥60s; SIGTERM/SIGINT
   drains curl and lets the processor flush the hour file.
5. `detector/detect.py` is a separate, offline batch process over closed hour
   files — a detector crash can never kill the ingester. The filesystem is the
   queue.
6. Detection rules live as data in `detector/rules.yaml` (6 rules), each with
   `provenance` (incident finding + source file + claim grade) that is copied
   into every alert it fires.
7. Rule 4 (`web2cit-nonbibliographic-target`, severity critical) compares each
   `Web2Cit/data/` edit's target domain — derived from the title's reversed-DNS
   path — against `allowlist_bibliographic_domains.txt` (562 census domains,
   2026-10-06; the incident's arcgis.com/geodata.hawaii.gov are NOT in it).
8. Alerts are JSONL on stdout: `{ts, rule, severity, wiki, user, title,
   evidence, provenance}`. Burst rules (`temp-account-burst`,
   `sandbox-edit-burst`) are stateful via `--state-file` (pruned sliding
   windows; alerts re-emit while a window is hot — consumers dedupe).
9. Everything is config-file driven (`ingester/config.example.yaml`); the
   system holds no credentials and must never gain any (read-only by
   construction).
10. Provenance of schema facts: `schema.wikimedia.org` + wikitech docs,
    fetched live 2026-10-06 (see DESIGN.md header). The builders then diverged
    from DESIGN.md in places (one stream per ingester instance, flat
    `raw/YYYY-MM-DD/HH.jsonl` layout, no `bin/` dir) — the code and READMEs are
    the authority; DESIGN.md §8's go-live command is stale.

## How it WILL run when the user says so (exact commands)

```sh
cd ~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/eventstreams-monitor

# 1. Configure (copy the example, edit: user_agent contact, wikis, thresholds).
cp ingester/config.example.yaml ingester/config.yaml

# 2. Validate the config — touches NO network (safe to run any time).
./ingester/ingest.sh --dry-run

# 3. Start the ingester (OPERATOR ONLY — never during the build).
#    One instance per stream; edit stream.url in config.yaml for
#    revision-create / page-delete.
./ingester/ingest.sh

# 4. Run the detector over closed hour files (batch; can also tail live).
python3 detector/detect.py --state-file detector/state.json \
  <out_dir>/raw/2026-10-06/13.jsonl >> alerts.jsonl
```

Acceptance test before leaving it alone (attended, ~5 min): raw hour file
grows; `state/<stream>.last_event_id` updates; kill curl once and confirm
backoff reconnect with resume (no unexplained gap); `detect.py` over a closed
hour writes alerts (possibly empty — empty is fine, missing is not).

## Never without the user's word

- Cron jobs, systemd units, or any autostart for the ingester.
- `notify: exec`-style off-host alerting (alerts stay local JSONL).
- Pointing the ingester at `stream-internal.wikimedia.org` (WMF-internal).
- Pushing from this directory (branch `wikipedia-edit-hunt-2026-10-06`;
  pushes are the lane coordinator's call).

## Layout

```
eventstreams-monitor/
  README.md            (this file)
  STATUS.md            (build/run/schedule status + component inventory)
  DESIGN.md            (architect's design doc; code+READMEs are authoritative
                        where they diverge — see §10 of this README)
  ingester/
    ingest.sh            curl -N reconnect loop, backoff, shutdown, resume
    process.py           stdin SSE parser -> per-hour JSONL, resume cursor
    config.example.yaml  all knobs, commented (copy to config.yaml at go-live)
    README.md            component doc
    tests/               offline fixtures + test_process.py (36 checks)
  detector/
    detect.py            rule engine (stdin/file -> alerts JSONL on stdout)
    rules.yaml           6 data-driven rules, each with provenance
    allowlist_bibliographic_domains.txt   562-domain census (2026-10-06)
    README.md            component doc
    tests/               fixtures + run_tests.py (16 checks)
```
