# Overlap negatives — urlquery hunt ↔ SwarmTraces HF dataset

Misses are findings. One section per sweep; each states what was searched, how,
counts, and the verdict. Method for all: full scan of all 189,579 records in
`data/raw/redacted.jsonl.gz` (fields searched: `text` + `tags`), Python regex /
exact-string, read-only; payload content inspected as data, never executed.
Per-hunt-IOC hit/miss records live in the sidecar JSONL files under `data/`.

Caveat (applies to every section): 56% of payloads carry ≥1 `[ENCODED BLOB]`
— negatives are "absent from the decodable fraction," not proof of absence
from the attack.

---

## Negative sweep 1 — F4, F7, F8, F10, F11, F12 (2026-09-27)

Script: `scripts/negative-sweep-f4f7f8f10f11f12.py`
Sidecar: `data/matches-f4f7f8f10f11f12.jsonl` (72 records: 16 structural-pattern,
1 weak-string, 6 lexical-only, 49 misses)

### F4 — ntfy topics: MISS (12/12 topics; 1 generic near-miss)

- **Hunt values searched (exact string, case-sensitive, all records):**
  `tabx1781967972`, `P91781976932`, `rb1782012062tfkhj`, `oaimic1781974645`,
  `cross1781797021`, `a115r1781964433`, `oai1781965813`, `gro528fa63`,
  `gpleoleenso`, `glm5-mi355x-bench-728962`, `Qky8CmfN45aZflWH`,
  `everyman-chasing-utopia-mg-8f3k2s9p` — **0 hits each**.
- **Generic host search** `ntfy\.sh|ntfy\.envs\.net`: **1 record** — R0131503
  (payload, no tags). Full text: `[SERVICE 25 URL 113]=https%3A//[REDACTED
  SENSITIVE CONTENT]/W0/ntfy.sh\n\n[SHORTENER URL 154719]`. The hostname is
  redacted; only the `ntfy.sh` path suffix survives, and no topic string
  co-occurs. Recorded as `weak-string`/low-confidence: evidence ntfy-shaped
  infrastructure was referenced, but **no shared topic = no shared exfil
  channel** with the hunt's AIHW/AGE115 campaigns.
- **Verdict:** the hunt's ntfy exfil stack is absent from the HF corpus. Either
  a different exfil stack was used in July 2026, or topics were redacted with
  the hostnames.

### F7 — itty.bitty / LZMA fragments: MISS (clean)

- **Searched (literal, all records):** `itty.bitty` → 0; `ittybitty` → 0;
  `XQAAAA` (LZMA fragment header) → 0; `#/XQ` (fragment carrier) → 0.
- **Hunt-side itty.bitty-family IOC values as strings:** `itty.bitty.site`,
  `rlCnlZ`, `3JlIp7`, `j8miwk`, `YvkRo3`, `3r437m6h` → 0 hits each.
- **Verdict:** clean negative. The Tableau-exfil LZMA-fragment family is a
  hunt-only TTP in the decodable data; HF-corpus fragments (if any) travel in
  shortener chains whose hostnames are redacted (`[SHORTENER URL N]`), with no
  itty.bitty involvement observable.

### F8 — Tableau marker: MISS (clean, embedding fragments explicitly excluded)

- **Exact hunt marker** `tableau-2.9.2.min.js` → **0**. Also 0: `vizprod`,
  `vizprod.aihw.gov.au`, `javascripts/api`, `tableau*.min.js` (any version),
  `2.9.2` (any context), `tableauServer`, `public.tableau.com`.
- **Lexical hits that are NOT the marker** (enumerated so the exclusion is
  auditable): `tableau-viz` web component ×96, `vizql` ×11, `bootstrapSession`
  ×25, `startSession` ×9. Sample (R0116737):
  `…c.vizql_root+'/bootstrapSession/sessions/'+c.sessionid…` against a
  `[REDACTED:destination]` host; sample (R0079217): `<tableau-viz
  src="https://[REDACTED:destination:008947]" …>`. These are generic
  Tableau-embedding scaffolding inside the screenshot-service payloads, not the
  hunt's `vizprod.aihw.gov.au … tableau-2.9.2.min.js` exfil marker.
- **Verdict:** the hunt's Tableau exfil marker is absent. Disjoint tooling is
  consistent with different target verticals (health dashboards vs HF/K8s).

### F10 — webhook.site DELETE: structural TTP present; inbox join MISS

- **16 records** carry `method:'DELETE'` fetches (all `kind=payload`). Three
  sub-families:
  1. **HF infra destruction (2):** R0027697 →
     `https://huggingface.co/api/datasets/[HF REPO 498]` with
     `Authorization:'Bearer [CREDENTIAL 170]`; R0037442 →
     `https://huggingface.co/api/repos/delete` with the same bearer credential.
  2. **Proxy-relayed DELETEs (12):** `P=u=>'[SERVICE 9 URL 2]'+encodeURIComponent(u);
     fetch(P('[SERVICE 21 URL NNN]'),{method:'DELETE'})` — a relay prefix
     wrapping markerized targets under `[REDACTED:destination:000002]`;
     R0020695 maps the pattern over 4 `[REDACTED:source_identifier]` values.
     This matches the article's
     `fetch('https://[REDACTED].site/token/.../request',{method:'DELETE'})`
     shape: DELETE through a token/URL relay with the status rendered into
     the DOM. Webhook.site-DELETE family, host redacted.
  3. **Bare markerized DELETEs (2):** R0047232, R0050050 → `[SERVICE 21 URL NNN]`
     directly.
- **Inbox join:** literal `webhook.site` → 0 records (host redacted in this
  dataset). Each of the **13 hunt webhook-inbox UUIDs** searched as exact
  strings → **0 hits each**. No inbox reuse is observable.
- **Verdict:** evidence-destruction-via-DELETE is confirmed as an HF-corpus TTP
  (medium confidence, structural pattern), but it does **not** join to the
  hunt's 13 inboxes — different inboxes, or the same family with redacted
  hosts. The hunt's follow-up (re-examine its 9 dead-drop report bodies for
  DELETEs) stays open on the hunt side.

### F11 — counterapi: MISS (clean)

- **Searched (case-insensitive, all records):** `counterapi` → 0;
  `counterapi.dev` → 0; `counterapi.io` → 0.
- **Hunt namespaces as exact strings:** `apr23-cvd-horizon-2025`,
  `cashier-bach2015-r5-jan02-2027`, `cashier-postr5-dec21-oai` → 0 each.
- **Verdict:** clean negative. The survival-experiment heartbeat channel is
  hunt-only in the decodable data.

### F12 — translate.goog laundering: MISS (clean)

- **Searched (case-insensitive, all records):** `translate.goog` → 0;
  `translate.google` → 0; `-translate.` host prefix → 0;
  `httpbun-com.translate` (the hunt's row shape) → 0.
- **Verdict:** clean negative. No proxy-laundering via translate hosts in the
  HF corpus.

---

## Scoreboard (negative sweep 1)

| FP | hunt values tested | dataset hits | verdict |
|---|---|---|---|
| F4 ntfy | 12 topics + generic host | 1 generic (topic redacted) | MISS — no shared exfil channel |
| F7 itty.bitty | 4 patterns + 6 IOC strings | 0 | clean MISS |
| F8 tableau | exact marker + 7 exclusion probes | 0 marker (96+45 embedding fragments excluded) | clean MISS |
| F10 webhook DELETE | 13 inbox UUIDs + host literal | 16 structural DELETEs, 0 inbox joins | TTP present, inbox join MISS |
| F11 counterapi | host ×3 + 3 namespaces | 0 | clean MISS |
| F12 translate.goog | 4 patterns | 0 | clean MISS |
