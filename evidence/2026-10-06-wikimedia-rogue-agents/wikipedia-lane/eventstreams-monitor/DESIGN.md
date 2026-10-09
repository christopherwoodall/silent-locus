# EventStreams ingest + monitor — design (OFFLINE BUILD, NOT RUNNING)

Status: **BUILD ONLY — never executed, no network connection made to
`stream.wikimedia.org` in this task.** See §8 for the go-live procedure and
what stays gated.

Purpose: live monitor for agent-shaped activity on Wikimedia wikis, built for
the 2026-10-06 rogue-agent hunt (WMF disclosure 2026-10-05): `~2026-*` temp-account
sandbox bursts, Web2Cit config tampering (Meta-Wiki `Web2Cit/data/`
namespace), Etherpad-related note traffic, temp-account fleet creation.

Provenance of this doc's schema facts: fetched live 2026-10-06 ~13:50 CDT from
`schema.wikimedia.org` (verified live docs, not training memory):

- `mediawiki/recentchange/1.0.1` — https://schema.wikimedia.org/repositories/primary/jsonschema/mediawiki/recentchange/latest.yaml
- `mediawiki/revision/create/2.0.0` — https://schema.wikimedia.org/repositories/primary/jsonschema/mediawiki/revision/create/latest.yaml
- `mediawiki/page/delete/1.0.0` — https://schema.wikimedia.org/repositories/primary/jsonschema/mediawiki/page/delete/latest.yaml
- `Event Platform/EventStreams HTTP Service` (redirect target of
  `Event Platform/EventStreams`) — https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams_HTTP_Service
- Stream endpoint pattern (docs): `https://stream.wikimedia.org/v2/stream/<name>`

---

## 0. TRANSPORT REALITY (read first)

On this build VM, **Python HTTP stacks break on the egress proxy** (httpx
chokes on the IPv6 `NO_PROXY` entries; unproxied egress fails SSL). **`curl`
works.** Therefore:

- The ingester MUST be **curl-based** (`curl -N` for SSE chunked streams),
  with parsing done by piping curl's stdout into `jq` / a small local
  reader (python reading stdin is fine — only its HTTP stack is broken).
- Alternatively the ingester may run on a host with a healthy HTTP stack;
  that decision is a deployment parameter (see `config.yaml` example in §6).
- This constraint is load-bearing: any implementation that reaches for
  `requests`/`httpx`/`urllib` over the network on THIS VM will silently fail.
  Document and test accordingly at go-live (the acceptance test is:
  `curl -N` emits SSE `data:` lines; nothing else establishes connectivity).

The reference implementation is a POSIX shell ingester:

```sh
curl -N --retry 0 --max-time "$MAX_CONN_SECONDS" \
     -H "User-Agent: $UA" \
     -H "Last-Event-ID: $LAST_ID" \
     "https://stream.wikimedia.org/v2/stream/$STREAM" \
| ./sse_to_jsonl.py >> "$RAW_DIR/$STREAM/$(utc_hour).jsonl"
```

`curl -N` = no buffering (SSE). `Last-Event-ID` = SSE resume (see §7).

---

## 1. WHICH STREAMS TO CONSUME, AND WHY

| Stream | Endpoint path | Verdict | Why |
|---|---|---|---|
| `recentchange` | `/v2/stream/recentchange` | **CONSUME (primary)** | The only stream carrying *everything*: edits (`type=edit`), page creations (`type=new`), log events (`type=log` incl. **new temp-account creations** via `log_type=newusers`, deletions via `log_type=delete`), plus `categorize`/`external`. One connection covers the whole attack surface. Verified as the canonical "most notable" stream in the wikitech doc. |
| `revision-create` | `/v2/stream/revision-create` | **CONSUME (secondary)** | Enriched per-edit record with full `performer` object (user_groups, user_edit_count, user_registration_dt — absent from recentchange's flat `user` string). Key for attributing a sandbox burst to a temp-account fleet: `performer.user_text` + `user_registration_dt` + `page_namespace`. Schema `mediawiki/revision/create/2.0.0`, verified live. |
| `page-delete` | `/v2/stream/page-delete` | **CONSUME (secondary, cheap)** | Dedicated deletion events. Directly relevant: the incident's Web2Cit config pages were deleted 2026-10-06 01:39:44–01:40:11Z by 'Pppery' — a future config-tampering response would arrive here, with `comment` and `performer`. Low volume, high signal. Schema `mediawiki/page/delete/1.0.0`, verified live. |

### Options considered and trade-offs

- **`page-create`** (`/v2/stream/page-create`): only page creations; redundant
  with `recentchange type=new` + `revision-create`. Skip unless a detector
  needs creation-only semantics without edit noise.
- **`page-move` / `page-restore` / `page-properties-change`**: not needed for
  this hunt's TTPs; add only if the fetch-oracle rule expands to
  config-page moves.
- **`recentchange` alone vs adding the two secondaries**: recentchange alone
  catches all *events*; it does NOT carry `performer` enrichment
  (registration date, edit count, groups) — that is what separates a
  brand-new `~2026-*` temp account from a renamed veteran account, so
  `revision-create` is justified for any account-attribution detector.
  `page-delete` is near-free (very low volume) and covers the config-deletion
  reflex seen in the incident.
- **Event volume note**: `recentchange` across ALL wikis is the hot firehose
  (see disk estimates §4). The `wikis` filter in config (§6) lets the
  operator narrow to `metawiki`/`enwiki`/`commonswiki`/etc. — filtering is
  **client-side** (docs explicitly: no server-side filtering), so narrowing
  the filter does not reduce bandwidth, only storage/processing.

**Assumed, not verified**: exact stream name spellings beyond the three above
(`page-create` exists per stream-config convention but was not fetched).
Verify against https://stream.wikimedia.org/?doc#/streams before adding.

---

## 2. EVENT SCHEMA NOTES (detector-keyed fields)

### 2a. `recentchange` — schema `mediawiki/recentchange/1.0.1` (verified)

Fields the detectors key on:

- `user` (string) — `rc_user_text`. **Detector key #1.** Temp accounts look
  like `~2026-28355-02` (match `/^~\d{4}-\d+/`). NOTE: this is a display
  string; temp accounts are unlinked, so the same human can hold many.
- `title` (string) — full prefixed page title. Match `/Sandbox/`,
  `/Web2Cit/`, `User talk:` prefixes.
- `namespace` (integer) — namespace id. Watchlist: `2` (User), `3`
  (User talk), `4` (Project, incl. Meta `Web2Cit` project-namespace pages —
  incident configs live at Meta `Web2Cit/data/...`), `-1` (Special, log-only).
- `wiki` (string) — wfWikiID, e.g. `metawiki`, `enwiki`, `commonswiki`,
  `testwiki`. **Docs: filter client-side.**
- `timestamp` (integer) — unix ts derived from rc_timestamp. Use for burst
  windowing, not `meta.dt` (see §7 clock skew).
- `comment` (string) + `parsedcomment` — edit summaries; carry TTP grammar
  (e.g. tool-generated summaries).
- `type` (string) — one of `edit`, `new`, `log`, `categorize`, `external`.
- `log_type` / `log_action` (string|null) — for `type=log`: `newusers`
  (temp-account creation; `log_action` distinguishes create/autocreate),
  `delete` (page deletions also land here as `log_type=delete`).
- `log_id` (integer|null), `id` (integer|null rcid) — dedup keys (see §7).
- `revision.new` / `revision.old` (int|null) — rc_this_oldid/rc_last_oldid.
- `length.new` / `length.old` (int|null) — byte deltas; a config-template
  edit that adds a fetch URL is a small positive delta — burst detectors
  should weight by delta, not just count.
- `bot`, `minor`, `patrolled`, `server_name`, `server_url` — filter/context.
- `meta.id` (string, unique event id), `meta.dt` (ISO-8601 receive time),
  `meta.stream`, `meta.domain` — **discard `meta.domain == "canary"`**
  (docs' own example does this; canary heartbeat events are not real edits).

### 2b. `revision-create` — schema `mediawiki/revision/create/2.0.0` (verified)

Enrichment per revision (edits only — no log events):

- `performer.user_text` — same account string as recentchange `user`; join key.
- `performer.user_id` (int, optional) — absent for anons; **temp accounts DO
  have user ids** (they are real accounts), so presence alone doesn't
  distinguish — combine with the `~` prefix match.
- `performer.user_registration_dt` (string, optional) — account birth;
  incident sandbox accounts were May/Jun 2026 vintage; a burst from accounts
  all registered within hours = fleet signal.
- `performer.user_edit_count` (int, optional) — low count + sandbox namespace
  = probe behavior.
- `performer.user_groups` (array) — empty for temp accounts; `sysop`/`bot`
  filters out legitimate tooling (e.g. Pppery's deletion was a sysop action).
- `performer.user_is_bot` (bool).
- `page_id`, `page_namespace`, `page_title`, `page_is_redirect`.
- `rev_id`, `rev_parent_id`, `rev_sha1`, `rev_len`, `rev_timestamp`
  (ISO-8601), `rev_minor_edit`, `rev_is_revert`, `rev_content_changed`,
  `comment`, `dt` (event time ISO-8601), `database` (wiki db name, e.g.
  `metawiki`).
- `meta.id` — dedup key.

### 2c. `page-delete` — schema `mediawiki/page/delete/1.0.0` (verified)

- `page_title`, `page_namespace`, `page_id`, `rev_id` (head rev at delete),
  `rev_count`, `page_is_redirect`.
- `comment` — deletion reason; an admin cleaning up agent configs leaves
  a reason string — alert on `Web2Cit` in title regardless of reason.
- `performer.*` — same shape as revision-create (who deleted).
- `database`, `meta.*` — same conventions.

### Join keys across streams

`recentchange.user` == `revision-create.performer.user_text` ==
`page-delete.performer.user_text`; `wiki` == `database`; timestamps within
seconds. Detectors join on (wiki, user_text) for fleet analysis.

---

## 3. COMPONENT DIAGRAM (ASCII)

```
                    https://stream.wikimedia.org/v2/stream/<name>  (SSE)
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
              ┌──────────┐    ┌──────────┐    ┌──────────┐
              │ ingester │    │ ingester │    │ ingester │   one curl -N
              │recentch. │    │revision- │    │page-     │   process per
              │          │    │create    │    │delete    │   stream (§0)
              └────┬─────┘    └────┬─────┘    └────┬─────┘
                   │               │               │
                   ▼               ▼               ▼
              raw/<stream>/YYYY-MM-DDTHH.jsonl   (rotated hourly, §4)
                   │               │               │
                   └───────────────┴───────────────┘
                                   │
                                   ▼
                            ┌────────────┐
                            │  detector  │  offline pass over JSONL
                            │  (batch)   │  rules in §5; reads raw,
                            └─────┬──────┘  writes alerts
                                  │
                                  ▼
                    alerts/YYYY-MM-DDTHH.alerts.jsonl
                                  │
                    ┌─────────────┴──────────────┐
                    ▼                            ▼
              ┌───────────┐               ┌─────────────┐
              │ reviewer  │               │  operator   │
              │ (human)   │               │  (notify)   │
              └───────────┘               └─────────────┘
```

Design decisions:

- **Ingester and detector are separate processes; the filesystem is the
  queue.** The ingester never interprets events — it appends raw JSONL.
  This keeps the network-facing component tiny (easier to harden, easier
  to reason about reconnect) and lets detectors re-run over history.
- **Detectors run as a batch over closed hour files** (or tail the current
  hour file), never inline in the SSE pipe. A detector crash must never
  kill the ingester.
- **Alerts are JSONL**, one object per alert: `{detector, rule_id,
  first_seen, last_seen, wiki, user_text, page_title, namespace,
  event_count, sample_event_ids[], severity, notes}`. Alerts are
  append-only; triage state lives OUTSIDE this system (hunt notes),
  never by mutating alert files.

---

## 4. STORAGE LAYOUT

```
eventstreams-monitor/
  DESIGN.md            (this file)
  config.yaml          (§6; created at go-live from the template)
  bin/
    ingest.sh          # curl -N loop with reconnect backoff (§7)
    sse_to_jsonl.py    # SSE frame parser: stdin -> JSONL lines on stdout
    detect.py          # batch detectors (§5)
    rotate.sh          # hourly rotation + retention sweep
  raw/
    recentchange/
      2026-10-06T13.jsonl
      2026-10-06T14.jsonl
      ...
    revision-create/
      ...
    page-delete/
      ...
  alerts/
    2026-10-06T13.alerts.jsonl
    ...
  state/
    recentchange.last_event_id      # SSE resume cursor (§7)
    revision-create.last_event_id
    page-delete.last_event_id
    gaps.log                        # gap-detection log (§7)
```

- **Naming**: `raw/<stream>/YYYY-MM-DDTHH.jsonl` (UTC hour, zero-padded,
  `.jsonl` = one JSON object per line, the SSE `data:` payload verbatim).
  Hour files make retention math and detector windowing trivial.
- **Rotation**: the ingester writes to the current hour file; `rotate.sh`
  (or the ingester itself on hour rollover) starts the new file. No
  mid-file truncation — files are append-only until the hour closes.
- **Retention guidance**: raw 7 days minimum (covers a disclosure-to-hunt
  lag like this one: 2026-10-05 disclosure, hunt started 2026-10-06).
  30 days if disk allows. Alerts kept 90 days. `state/*.last_event_id`
  never expires.
- **Disk estimates (ESTIMATES — measure at go-live, do not budget on these)**:
  Event counts on `recentchange` across all wikis average roughly
  10–20 events/sec at typical load (order-of-magnitude; verify from the
  first hour of capture). At ~15 ev/s × ~1.2 KB/event:
  - `recentchange`: ~65 MB/hour → **~1.6 GB/day** → ~11 GB/week.
  - `revision-create`: edits only, roughly 60–70% of recentchange volume
    → ~1 GB/day.
  - `page-delete`: negligible (tens of events/hour).
  - **Total ≈ 2.5–3 GB/day → ~20 GB/week.** Recommend ≥100 GB free before
    a 30-day retention target. The `wikis` config filter reduces
    *processing*, not bandwidth — full-stream storage cost is fixed
    regardless (see §1).
  - Mitigation if disk-bound: capture full `recentchange` but rotate at
    24 h retention, or run a filtered sidecar copy (`raw-filtered/`) with
    only matching wikis/namespaces kept long-term.

---

## 5. DETECTOR RULES (initial set, from incident TTPs)

All rules run over `raw/` hour files; all emit to `alerts/`. Thresholds are
config knobs (§6), defaults below are starting points, not doctrine.

1. **temp-account-fleet** — `type=log AND log_type=newusers` on recentchange.
   Alert when ≥N temp accounts (`user` matches `^~\d{4}-`) created within
   a W-minute window on the same wiki. (Incident: `~2026-*` sandbox
   accounts; fleet creation is the earliest observable.)
2. **sandbox-burst** — `type IN (edit,new) AND namespace IN (2,3)` and title
   contains `Sandbox` (case-insensitive). Alert on ≥N edits by distinct
   temp accounts within W minutes on one wiki. (Incident: May 10 / May 27 /
   Jun 25 bursts.)
3. **web2cit-config-touch** — any edit to titles matching
   `(?i)web2cit` on `metawiki` (namespace 4 / 828 per incident layout),
   OR any stream: alert on EVERY such edit (N=1 — this namespace is
   normally near-silent; any touch is worth a human look). This is the
   **fetch-oracle detection rule** from the hunt.
4. **config-delete-watch** — `page-delete` where `page_title` matches
   `(?i)web2cit`; alert immediately (N=1). (Incident: Pppery deletion
   2026-10-06 01:39–01:40Z — the cleanup reflex is itself signal.)
5. **probe-grammar** — comment/parsedcomment matching known agent grammars
   (`tok=expt\d+`, `zz=oai`, `task-oai-\d+`, `dsqa_`, `retry=`) — currently
   all scoring zero against incident texts (per join-analyst: DISJOINT),
   kept as a tripwire for grammar migration.
6. **low-edit-count-burst** — join recentchange→revision-create on
   (wiki, user_text): ≥N edits in W minutes from accounts with
   `performer.user_edit_count < E` and empty `user_groups`. Catches probe
   crews regardless of username shape.

Severity: rules 3–4 = `high`; 1–2 = `medium`; 5–6 = `low`. Reviewer triages
all `high` same-day; the rest in the weekly sweep.

---

## 6. CONFIG FORMAT (commented example — template only, not live)

```yaml
# eventstreams-monitor/config.yaml — TEMPLATE. Copy to config.yaml at go-live,
# fill in, and never commit secrets (there are none; this system needs no credentials).

ingest:
  # Streams to consume. Names must match https://stream.wikimedia.org/v2/stream/<name>.
  streams: [recentchange, revision-create, page-delete]
  # Base URL. Override only for testing against a replay fixture.
  base_url: "https://stream.wikimedia.org/v2/stream"
  # Transport: "curl" is the ONLY supported value on this VM (see DESIGN.md §0).
  # On a host with a healthy HTTP stack, "python-sseclient" is acceptable.
  transport: curl
  # curl path and flags. -N = no buffering (required for SSE).
  curl_bin: /usr/bin/curl
  curl_extra_flags: ["-N", "--retry", "0"]
  # Per-connection ceiling; curl exits and the backoff loop reconnects.
  # Forces periodic resume-cursor exercise even on a healthy stream.
  max_conn_seconds: 3600
  # User-Agent sent on every connection. Identify the project; WMF asks
  # consumers to use a descriptive UA.
  user_agent: "silent-locus-eventstreams-monitor/0.1 (research; contact: <fill in>)"

filter:
  # Client-side wiki filter (EventStreams has NO server-side filtering).
  # Empty list = all wikis. Narrow for processing/storage triage, NOT bandwidth.
  wikis: [metawiki, enwiki, commonswiki, testwiki]
  # Namespaces of interest per detector (MediaWiki canonical ids).
  watch_namespaces: [2, 3, 4, 828]
  # Title regexes (Python syntax) for high-value pages.
  watch_title_regex: ["(?i)sandbox", "(?i)web2cit"]
  # Drop canary heartbeat events (meta.domain == "canary"). Always true.
  drop_canary: true

storage:
  raw_dir: ./raw
  alerts_dir: ./alerts
  state_dir: ./state
  # Rotation granularity: "hour" only (day/week not supported — detectors assume hours).
  rotation: hour
  # Retention in days for raw hour files (alerts: 90, state: forever).
  raw_retention_days: 7

reconnect:
  # Backoff on unexpected disconnect: base * 2^attempt, capped, with jitter.
  backoff_base_seconds: 2
  backoff_max_seconds: 300
  backoff_jitter: true
  # Consecutive failures before paging the operator (alerts/gaps.log + stderr).
  alert_after_consecutive_failures: 10
  # On reconnect, send Last-Event-ID from state/<stream>.last_event_id (SSE resume).
  resume_with_last_event_id: true
  # If the cursor is older than this, do NOT attempt resume (gap too large;
  # log it in gaps.log and start live). Prevents replaying ancient history.
  max_resume_age_seconds: 7200

detectors:
  temp_account_fleet:      { enabled: true,  window_minutes: 60,  min_accounts: 5 }
  sandbox_burst:            { enabled: true,  window_minutes: 30,  min_edits: 10 }
  web2cit_config_touch:     { enabled: true,  min_edits: 1 }   # any touch alerts
  config_delete_watch:      { enabled: true,  min_edits: 1 }   # any delete alerts
  probe_grammar:            { enabled: true,
                              patterns: ["tok=expt\\d+", "zz=oai", "task-oai-\\d+",
                                         "dsqa_", "\\bretry="] }
  low_edit_count_burst:     { enabled: true,  window_minutes: 60,
                              min_edits: 15, max_edit_count: 20 }

operator:
  # Where detector summaries go. "log" = alerts/*.alerts.jsonl only.
  # "exec" runs notify_command with the alert file path as $1 — USE WITH CARE.
  notify: log
  notify_command: ""
```

---

## 7. FAILURE MODES

- **Reconnect / backoff**: `ingest.sh` loops forever: connect with
  `Last-Event-ID: <cursor>` → on EOF/error, sleep
  `min(base * 2^attempt, max) + jitter`, reconnect. Attempt counter resets
  on any successful event. After `alert_after_consecutive_failures`,
  write to `state/gaps.log` and stderr. **Never exit the loop on its own** —
  a silent exit is the worst failure (looks like "no activity").
- **Gap detection (knowing you missed events)**:
  1. `Last-Event-ID` resume: the docs' own pattern — pass the last seen
     SSE event id; the service replays missed events (bounded server-side
     buffer; hence `max_resume_age_seconds`).
  2. `meta.id` dedup on the detector side: keep a per-hour Bloom/set of
     seen `meta.id`; count replays vs genuinely new events. A jump in
     `recentchange.id` (rcid) or `timestamp` discontinuity larger than the
     backoff window = a gap; log `(stream, gap_start, gap_end)` to
     `state/gaps.log`.
  3. Canary events (`meta.domain == "canary"`) are heartbeats — their
     ABSENCE for >N minutes while connected = stalled stream, treat as a
     failure and reconnect even if the socket looks open.
- **Clock skew**: detectors window on the **event's own timestamp**
  (`recentchange.timestamp`, `revision-create.rev_timestamp`/`dt`), never
  on file mtime or wall clock. `meta.dt` is receive time, not event time —
  do not use it for ordering.
- **Duplicate delivery**: SSE resume replays the tail; expect duplicates.
  Detectors dedup on `meta.id` (globally unique per event) before rule
  evaluation. Alert objects carry `sample_event_ids[]` so a duplicate
  alert is recognizable at review.
- **Schema drift**: WMF versions schemas (`1.0.1`, `2.0.0` — recorded in
  §2). `ingest.sh` does not validate; `detect.py` must tolerate missing
  optional fields (`performer.user_registration_dt` is optional) and log
  (not crash on) unknown fields. Pin the schema versions above in
  detector comments; re-fetch the YAML if detectors start seeing
  unfamiliar shapes.
- **curl-specific**: `--retry 0` (the shell loop owns retry policy, not
  curl), `--max-time` per connection, and check curl's exit code —
  exit 0 with clean EOF is a normal server-side close, still triggers
  backoff reconnect. Proxy env (`https_proxy` etc.) must be correct on
  the run host; on THIS VM curl works through the egress proxy as-is.
- **Disk full**: `rotate.sh` enforces retention by deleting oldest closed
  hour files first; the ingester checks free space before opening a new
  hour file and refuses to start a stream if <5 GB free (fail LOUD, not
  silent truncation).
- **Partial writes**: the SSE parser writes only complete JSON objects
  (one per line); a torn final line on kill is discarded by the detector
  (JSON parse failure on the last line of the CURRENT hour file is
  expected and ignored).

---

## 8. NON-GOALS AND GO-LIVE

### Explicit non-goals

- NOT a real-time alerting pager: detectors run batch over hour files.
  Sub-hour latency is not a requirement (the hunt works on hours-to-days).
- NOT a wiki editor, voter, or patroller: this system is read-only by
  construction. It holds no credentials and must never gain any.
- NOT a replacement for the MediaWiki API: historical backfill (e.g.
  re-examining the May/Jun 2026 sandbox bursts) is an API job, not a
  stream job — EventStreams has no replay beyond the short resume buffer.
- NOT a cross-hunt correlator: joining stream alerts against urlquery /
  collusion.wiki / corpus data happens in the hunt notes, not here.
- NOT multi-tenant: one operator, one config, one deployment.

### "Not running" status

Nothing in this directory has been executed. No connection to
`stream.wikimedia.org` was made during the build (docs only, via
`schema.wikimedia.org` and `wikitech.wikimedia.org`). No cron jobs, no
systemd units, no background processes were created.

### When the user says go — one command

```sh
cd ~/workspace/silent-locus/data/2026-10-06-wikimedia-rogue-agents/wikipedia-lane/eventstreams-monitor \
  && cp config.yaml.example config.yaml   # after creating it from §6 template
  # edit config.yaml: user_agent contact, wikis, thresholds
  && ./bin/ingest.sh --config config.yaml
```

Acceptance test before leaving it alone (5 minutes, attended):

1. `raw/recentchange/<current-hour>.jsonl` grows (SSE `data:` lines arriving).
2. `state/recentchange.last_event_id` updates.
3. Kill `curl` once; confirm backoff reconnect and resume (no gap in
   `state/gaps.log` beyond the kill window).
4. Run `./bin/detect.py --hour <closed-hour>`; confirm an
   `alerts/<hour>.alerts.jsonl` file is written (possibly empty — empty is
   fine, missing is not).

### What must NEVER be done without the user's word

- Creating cron jobs, systemd units, or any autostart for the ingester.
- Widening `wikis: []` to full-firehose retention beyond the disk budget
  in §4 (bandwidth/storage cost is real).
- Adding any `notify: exec` command that sends data off-host (webhook,
  email, bot post) — alerts stay local JSONL until explicitly approved.
- Pointing the ingester at `stream-internal.wikimedia.org` (WMF-internal,
  not public; attempting it is out of scope and likely to fail).
- Committing or pushing anything from this directory without the lane
  coordinator's go-ahead (branch `wikipedia-edit-hunt-2026-10-06`; the
  coordinator owns pushing).

---

## 9. DELIBERATELY LEFT OUT (and why)

- **`bin/` implementation scripts**: this task is the design; the shell +
  parser + detector code is a follow-up build task. The design pins every
  interface the code must honor (file layout, cursor format, alert schema,
  config keys) so implementation is mechanical.
- **`page-create` stream**: redundant with `recentchange type=new`; add if
  a detector needs creation-only semantics.
- **Wikidata/Commons-specific streams** (`mediawiki/wikibase/...`): the
  incident's TTPs are edit/config-centric; the WDQS angle is a separate
  (already-closed) lane.
- **Backfill of May–Oct 2026**: streams don't replay history; that work
  belongs to the MediaWiki API lane (wiki-surgeon pattern), not this system.
- **Exact event-volume numbers**: §4 gives order-of-magnitude estimates
  only — the first captured hour is the calibration run; do not budget
  retention on estimates.
- **Authentication / private streams**: public EventStreams needs no
  credentials; the design keeps it that way permanently.
