# PROVENANCE — university-shorteners-batch2 dataset

## Scope

Batch 2 (lane Q, 2026-09-28) sweeps NEW venues only — batch 1's
data/university-shorteners/ is untouched. Source of candidates: (1) a new
goto.unm.edu slug (`vbudg+`) surfaced via search-engine index of UNM's public
stats pages; (2) new university YOURLS candidates from web search
(`goto.ucr.edu`, `lnk.mcla.edu`); (3) referrer-surfaced community shorteners
from batch 1 (`da.gd`, `is.gd`, `2dd.pl`, `fooabc.com`); (4) two more
edu-domain candidates from a public URL-shortener blocklist
(`mlc-wels.edu`, `go.aim.edu`). Community YOURLS already swept by
brausepulver/collusion-wiki-link-shorteners (yourls.space, yourls.biz,
hko.nu, yourls.pro, ns3.dnscores.com, IP-nip.io hosts) are saturated ground
and were NOT re-swept.

## Method (read-only, passive)

- Direct GETs only to public read endpoints: per-link `+` stats pages and
  front pages.
- Never: shortening/action/API-write endpoints, logins, form submissions,
  counter increments, mass target fetching, challenge solving.
- Login-walled `+` stats (goto.ucr.edu, per instance policy) were recorded
  and not bypassed. 403/Cloudflare/DNS-dead hosts recorded as-is.
- Slug sources: search-engine-indexed `+` pages and UCR's own public ITS
  documentation (KB0011332). No slugs were guessed.

## Contents

- `goto-unm-edu/vbudg_stats_2026-09-28.txt` — the one verifiable hit
  (control page; 4 hits, no agent markers).
- `negative-probes/*.txt` — 8 documented negatives.
- `university-shorteners-batch2.jsonl` — 1 Elastic-ready doc (the vbudg hit).
- `SHA256SUMS` — checksums of every file above.
- `progress.log` — resumable run log.

## Elastic

Index `university-shorteners-batch2`, canonical shared schema
(notes/gems-es-mapping.json), `labels.shortener.scope` distinguishes
university vs community. Negatives are documented here and in the notes
report, not in Elastic (same convention as batch 1).

## Guards honored

Read-only research only. No submissions/uploads/accounts/logins/posts/
counter increments/payload execution. Agents/infrastructure traces only —
no operator identity, registrant details, or person-focused attribution.
No credentials reproduced. No absolute home-directory paths in logs/docs.
