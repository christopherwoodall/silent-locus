# APPWRITE-FOLLOWUP — wave-3 worker findings (2026-10-05)

Follow-up on tld-sweeper LEAD #1 ("Appwrite deployment burst", graded LEAD
moderate-weak). Characterized via 22 paged `uq_htmx_curl.py` keyword
queries (`appwrite`, offsets 0–1320), 60+ sec pacing, plus 1 `url.domain:`
query and local-corpus checks. Read-only/public OSINT only; no Appwrite
deployments were fetched or probed. Full observed values, no redaction;
OBSERVED vs INFERENCE separated below.

## 1. OBSERVED — the burst is 12+ hours, not 75 minutes

- 1,358 unique `appwrite`-matching reports pulled; **923 are
  `*.appwrite.network` submissions**, spanning **2026-10-05T03:21:00Z →
  2026-10-05T15:36:00Z** and still ongoing at last pull.
- 453 distinct minutes with ≥1 report; hourly counts: 03:30, 04:49, 05:53,
  06:63, 07:55, 08:98, 09:68, 10:69, 11:112, 12:65, 13:82, 14:113, 15:66.
  Sustained ~100/hr for 12 hours — the tld-sweeper's "14:15–15:28Z, 26
  hosts" was one window of a much larger all-day operation.
- 458 unique `*.appwrite.network` hosts. Re-scan counts are high:
  `branch-v2-0f34728.appwrite.network` ×38 (07:27Z→14:50Z, ~3–4 min
  intervals, one 59-min gap), `branch-armonia-corretta-1e1dda8` ×25
  (08:38Z→14:36Z), `branch-e2e-validation-f5afea6` ×16 (06:29Z→09:46Z),
  `branch-edutoks-producti-6f2ba05-1b62f52` ×14 (06:44Z→15:03Z),
  `6ac3323200137dee90fb.appwrite.network` ×14 (05:16Z→13:11Z),
  `hackhub.appwrite.network` ×9 (10:12Z→15:17Z).
- Branch-name grammar (`branch-<git-branch>-<hex>`), 303 reports / 95 unique
  deploys. Prefix census: main (87r/40h), feat (40/9), v (38/1),
  armonia (25/1), e (16/1, `e2e-validation`), edutoks (14/1), master (10/3),
  dev (7/3), fix (6/6), feature (6/3), develop (5/3), blog (5/2),
  android (5/1), ai (4/1), spec (3/2 — includes tld-sweeper's
  `branch-spec-92-u5-home-81df635-70e2d92`), claude (3/3), codex (3/1).
- 236 distinct hex-labeled prefixes (Appwrite Sites auto-IDs; lengths 20 and
  13 hex chars). Chronological first-seen vs numeric ordering: **165/235
  ascending-adjacent pairs (70.2%)** — new IDs appear in roughly increasing
  order through the day (e.g. `6ac317e7e002e0e6ffe2` at 03:25Z →
  `6ac3c32ecc63973264a3` at 15:34Z), i.e. new sites are being CREATED
  steadily and scanned as they appear. Matches new-fleets FINDING 4 (the
  `6ac31*` series, same day).
- Named hosts include `6ac3<SERIES>-routertest.stage.appwrite.network`
  (~26 distinct routertest.stage variants), plus QA-flavored names:
  `niwport-staging`, `ss-training`, `detour-1t7n`, `muschellecker`,
  `camwhisky-pdsy`, `peque-rutinas`, `pfpzone`, `radphrase`,
  `kanteva-app`/`kanteva-app-rc6c`/`kanteva-app-68fs`, `vb-qc`,
  `vb-qc-me7p`, `my-website-pi1b`/`my-website-e0o6`, `sha-kweyol`,
  `onze desk` (onze), `kincloud`, `lender-hub`, `hackhub`, `webpad`,
  `megaprofile`, `jingshi`, `alberti-dashboard`. 120 distinct hosts carry
  QA/dev keywords (routertest/e2e/validation/feat/staging/stage/test/
  deploy/preview).
- Known-operator markers in ALL 923 appwrite.network URLs: `zz=` 0,
  `uqscan` 0, `httpbun` 0, `webhook` 0, `oai` 0, `epoch` 0, `nonce` 0,
  `?task` 0, `batch=` 0, `eval` 0, `harness` 0.
- Content spot-checks (public report pages, read-only): `hackhub`
  = Next.js student directory app (benign; confirmed by tld-sweeper);
  `megaprofile.appwrite.network` = React/Next.js marketing-ish site
  (benign); `6ac322920efad6c117ac.appwrite.network` = page shell loading
  cloud.appwrite.io + Stripe JS + plausible.io (a Stripe-integrated test
  site; no credential-drop/phish markers visible in the host summary).
  (NOTE: the `zz.png` in that report is urlquery's unknown-country flag
  image, not a `zz=` marker.)

## 2. OBSERVED — local corpora

- Burst hostnames appear in `new-fleets/raw/window{3,4,5,6,7,10,12,15,16,17,18,19}.json`
  and `window_gapfill.json` — same-day (2026-10-05) urlquery collection
  windows, same operation (e.g. `6ac372404b613-routertest.stage` 09:50Z,
  `hackhub` 10:31Z/11:42Z/13:24Z/13:44Z, `radphrase`, `pfpzone`). These are
  INDEPENDENT confirmation of the all-day cadence (collection by a
  different worker, earlier today).
- new-fleets FINDINGS.md FINDING 4 already characterized the `6ac31*`
  Appwrite site series as bulk site creation (phishing-kit-farm hypothesis
  for the CREATION side; scanning = triage). The ascending-ID pattern found
  here is consistent with that.
- No prior sightings of these hostnames/branch names in any earlier corpus
  (pre-2026-10-05); all matches are today's material plus the tld-sweeper's
  own files.
- ExploitGym Appwrite comparison: per the 2026-09-28 marker sweep, the 134
  July `exploitgym` hits were **100% Appwrite console/Vibes preview
  deployments that are sign-in/password-protected pages (Jul 27–31)** —
  i.e. agents probing locked console previews. Today's operation targets
  PUBLIC preview deployments of Sites with real git-branch names and an
  e2e/QA flavor. Different shape; no match.

## 3. The discriminator

| Signal | Agent harness (ExploitGym shape) | CI deploy-verification | Observed | Fits |
|---|---|---|---|---|
| Targets locked console/Vibes previews | yes | no | public site previews | CI/QA |
| One scan per deployment (verify then done) | mixed | yes | same deploy re-scanned ×38 at 3–4 min intervals over 7h | neither — continuous polling |
| Branch names | harness/task IDs | real git branches (main/dev/feat/fix/claude/codex) | main, feat, fix, claude, codex, e2e-validation, armonia-corretta, spec-92-u5-home | CI/QA (agentic coding: `claude`/`codex` branches = agents DOING the deploys, not a swarm attacking) |
| New targets appear in ID order | no | no | 70% ascending hex-ID first-seen | creator scanning own deploys, OR platform-side abuse/triage sweep, OR threat-intel harvesting |
| Known operator grammar/markers | yes (historical) | no | zero markers in 923 URLs | CI/QA |
| Content | exploit attempts | benign | benign (Next.js apps, Stripe test site) | CI/QA |

Decisive points:
- **Re-polling every 3–4 minutes for 7+ hours kills "deploy verification"**
  (verify-once), but so does it kill a swarm-scan reading (a scanner moves
  on). The loop is a monitoring loop: uptime watcher, security re-scan
  service, or an agent's own deploy-health loop.
- **70%-ascending hex IDs** means the actor discovers new sites in creation
  order — exactly what (a) Appwrite-side abuse/malware screening, (b) a
  threat-intel vendor harvesting new Appwrite Sites, or (c) the site
  creator verifying their own churn would produce. (a)/(b) explain the
  re-polling of stable hosts (re-checking known sites); (c) explains
  same-day creation. All three are legitimate automation, not a swarm.
- **`branch-claude-*` / `branch-codex-*` names** indicate agentic coding
  tools (Claude Code / Codex-style) driving deploys — an agent loop doing
  dev work, with urlquery scans as part of a security-check step. That is
  "agent-shaped" only in the trivial sense (agents deploying their own
  apps); it is not a swarm, not our operator, and has zero known markers.
- ExploitGym shape does NOT match (locked console previews vs public site
  previews).

## 4. Verdict

**HONEST NEGATIVE (as an agent-swarm candidate).** Supersedes tld-sweeper's
LEAD (moderate-weak): the burst is real automation but it is a 12-hour
continuous polling/monitoring operation over Appwrite Sites preview
deployments with git-branch naming, QA/e2e flavor, zero known operator
markers, benign sampled content, and no match to the ExploitGym Appwrite
shape. Best-fit readings, in order: (1) a dev team/agentic-coding loop
(claude/codex branches) scanning its own preview deploys on a tight
re-poll; (2) platform-side abuse screening or a threat-intel service
harvesting newly created Appwrite sites (ascending-ID discovery); (3)
phishing-kit-farm triage — creation-side hypothesis only (new-fleets
FINDING 4), unsupported by content observed here (sampled pages benign).
None is a German/French agent swarm; none matches the known operator.

Kept as a watch item (not a tracked lead): the operation is live and
high-volume; a 24h re-pull distinguishes "persistent pipeline" (sustained
monitoring / kit-farm churn) from a one-day QA pass.

## 5. 24h re-pull spec (for coordinator)

- Query (via `uq_htmx_curl.py`, polite pacing ≥60s between queries):
  `python3 ~/workspace/skills/urlquery/bin/uq_htmx_curl.py search --query "appwrite" --limit 60 --offset <0,60,120,...> --delay 8`
  until date range reaches back past the previous run's earliest date.
  NOTE: `url.domain:appwrite.network` sorts differently (older first);
  plain keyword `appwrite` sorts newest-first — use keyword for freshness.
- Baseline captured this run: 923 unique `*.appwrite.network` reports,
  2026-10-05T03:21:00Z → 2026-10-05T15:36:00Z, 458 unique hosts, ~100/hr.
  Full report IDs + dates + URLs persisted in
  `burst_report_ids.jsonl` (923 rows, this directory). Raw pages in
  `uq_appwrite_kw_o{0..1320}.json` + `uq_appwrite_domain.json` (this
  directory).
- Tests for the re-pull:
  1. Is the scanning still running (reports newer than 2026-10-05T15:36Z)?
  2. Do the hex IDs continue ascending past `6ac3c32ecc63973264a3`
     (new site creation continuing)?
  3. Are `branch-v2-0f34728` / `branch-armonia-corretta-1e1dda8` still
     being re-polled (persistent monitoring), or abandoned (one-off QA)?
  4. Any new branch names with operator grammar (`zz=`, epoch nonces,
     task/batch params) — marker appearance would re-open this as a lead.
- Verdict rule: continued scanning at ≥50/hr with ascending hex IDs and no
  markers → persistent pipeline, stays a watch item (not a swarm lead).
  Appearance of agent grammar/markers → escalate back to LEAD.

## Files produced

- `FINDINGS.md` (this file)
- `burst_report_ids.jsonl` — 923 deduped reports (report_id, date, url),
  sorted chronologically — re-pull baseline
- `uq_appwrite_kw_o{0,60,...,1320}.json` + `uq_appwrite_domain.json` —
  raw htmx search pages (22 pages, offsets 0–1320)
- `analyze.py`, `analyze2.py`, `analyze3.py`, `repull.py`,
  `analysis.txt`, `analysis2.txt`, `analysis3.txt`, `stats.txt` — analysis
  scripts and outputs
- `uq_err*.log` — tool stderr logs
