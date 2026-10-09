# FINDINGS — FILESHARE FARMER

Last updated: 2026-10-05T07:35Z. Sweep 1 complete. All URLs LOGGED with metadata; no file contents fetched (opsec).

## Method
Public listings + search-engine-indexed share pages + urlquery/urlscan pivots for agent-marker grammars
(`zz=oai<digits>`, `uqscan=<word><date><letter>`, 13-digit epoch nonces, `retry={epoch}-{N}`,
webhook.site URLs, httpbun staging, jina.ai laundering). LOG URLs, don't fetch contents (opsec).

## Verdict
No confirmed agent dead drop on a file-share service. One genuinely new machine-shaped lead (pixeldrain re-scan loop),
one in-corpus validation that catbox.moe's temp service carried agent nonce grammar, and clean honest negatives
across five major share domains on urlquery.

## 1. GENUINELY NEW lead: pixeldrain re-scan loop (agent-shaped, unconfirmed)
- **What:** `https://pixeldrain.com/api/file/UNcsXkRT` submitted to urlscan.io **6 times on 2026-10-02**
  between 09:34 and 16:39 UTC. Gaps: 3.8, 28.9, 23.3, 27.5, then 341.5 min.
- **Why it matters:** the middle three gaps (~23–29 min) read as a ~25-minute polling loop with jitter —
  machine re-submission, not human browsing. Someone (or something) is re-scanning the same file on a loop.
- **Caveats:** file contents unknown (not fetched, per opsec); could be a researcher monitoring a file.
  urlscan result API needs login for filenames — not retrieved.
- **Not in our corpora** (checked all three events.jsonl + codebreaker inventory): not OURS, not KNOWN-documented.
- **Grade:** LEAD — agent-shaped but unconfirmed. Follow-up: watch for recurrence of the same file ID or
  the same ~25-min cadence on other pixeldrain file URLs.

## 2. OURS: litter.catbox.moe carried epoch-nonce grammar (in-corpus validation)
- **What:** oai-tag-sweep corpus record (event_time 2026-05-10T08:12:57Z, indicator `epoch_nonce`):
  `litter.catbox.moe/hdcf0x.html?x=1778400745.7904322` — catbox's temp-file service (litterbox) with an
  epoch-with-decimals nonce parameter.
- **Why it matters:** validates catbox.moe/litterbox as an agent-used staging surface. The farmer's
  catbox lane is justified — keep farming it.
- **Grade:** OURS (in-corpus, previously recorded). Not a new find; a direction confirmation.

## 3. Nulls and negatives (honest)
- **urlquery htmx sweep (8 domains):** `gofile.io` 0 reports, `catbox.moe` 0, `filebin.net` 0, `temp.sh` 0,
  `mirrorace.com` 0, `pixeldrain.com` 12 (routine homepage + 2 file URLs, no markers),
  `1fichier.com` 11 (routine; one double-submit `?o9pqk9vjjcdk773zseps` 1 min apart — likely human re-scan),
  `mediafire.com` 12 (consumer files: mod APKs, invoice JPEG — one double-submit pair, no markers).
  Raw: `raw/urlquery_domains.json`.
- **Web search for marker co-occurrence** (`uqscan`/`zz=oai` × gofile/catbox/pixeldrain/filebin): zero hits.
  `gofile.io "webhook.site"`: zero agent-relevant hits.
- **filebin.net urlscan (6 results):** `ddos.zip`, `videl.zip`, `file.exe` — human malware distribution,
  not agent-shaped. Logged as negative context.

## 4. Logged, not finds
- **rubyhack.ai** — documents the RubyGems `oai`-author packages (lambQ4345, oaiztestxyz123, …).
  KNOWN per 2026-09-27 correction; useful source, not a find. https://rubyhack.ai/
- **pastebin.com/7Z30DxWA** — 10.58 KB base64 blob paste, crawled ~11 days ago. No agent marker visible
  in snippet; LEAD handed to numbers-station lane for structural analysis. Not fetched.
- **darkxyn-gpt.pages.dev** — urlscan hit embedding catbox.moe resources (2026-10-04). GPT-named
  pages.dev site; weak lead, no marker. Logged only.
- **groupda.com** (user seed): NOT a file share — WhatsApp group-invite directory. Has a
  `Hacking_Web_Learning` category; logged as a coordination surface, out of scope here.
- **sharesome.com** (user seed): browser fetch blocked by policy — logged, not retried.
- **mediafire cors-laundering hits** (2 records in oai-tag-sweep): OURS but treat as FALSE-POSITIVE
  per global-south-scout correction — the linkage came from hunter wrapper filenames, not submitter content.
- TikTok share URL containing coincidental `ZzOai` inside TikTok's own encoded params — noise, logged.

## 5. Service inventory status
`services.txt`: 16 services seeded. Status notes: oshi.at dead; bashupload status unchecked;
anonfiles dead (successors unknown — open thread). pixeldrain and 1fichier/mediafire have
search-visible file URLs; gofile/catbox/filebin/temp.sh have no public listing surface found yet.

## Open threads
1. pixeldrain UNcsXkRT recurrence watch — same file or same ~25-min cadence on other file IDs.
2. catbox.moe deeper farm — litterbox temp URLs are the validated agent surface; find listing/indexing angles.
3. gofile.io share-page indexing — search engines index some; try `site:gofile.io` dork variants.
4. anonfiles successors — identify and add to services.txt.
5. urlscan result API needs login for filenames — note as tooling gap; search-level metadata sufficed here.

## Evidence log
- `raw/urlquery_domains.json` — 8-domain urlquery htmx sweep (2026-10-05)
- `raw/urlscan_pixeldrain.json` — 132-result pixeldrain urlscan search (2026-10-05)
- `sweep.log` — timestamped lane log
- `services.txt` — service inventory
