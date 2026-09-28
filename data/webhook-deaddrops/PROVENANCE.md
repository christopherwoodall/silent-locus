# PROVENANCE — webhook-deaddrops (Lane K, 2026-09-27/28)

**Dataset:** `webhook-deaddrops` — marker sweep for the webhook dead-drop exfil
technique documented by JFrog GemStuffer report
(https://research.jfrog.com/post/gemstuffer-openai-rubygems/): `southpxdatapp6pi` —
zlib+base64 Southwark calendar chunks in `/api/v1/web_hooks` URLs shaped
`https://example.com/A000/<chunk>` … `ZZEND/<count>`.

**Retrieval date:** 2026-09-28 (UTC). Lane K sweep run 2026-09-28 ~03:30–04:00 UTC
(Sun 2026-09-27 22:21 CDT → ~22:45 CDT).

**Method:**
1. Local: `grep -rlE "southpxdatapp|web_hooks|webhook.site|oast.online|ZZEND|A000"`
   across all `data/` dirs (excluding this output dir), both
   `data/osv/diffend_sweep_results*.jsonl`, all 28 recovered `.gem` tarballs
   (byte-level scan of outer tar + inner data tar), chunk-label variant greps
   (`/A0[0-9]{2,4}/`, `A0000`, `web_hook` singular, `ZZEN[^D]`).
2. ES read-only: `collusion-wiki` index — 0 hits for every marker
   (southpxdatapp, ZZEND, web_hooks, webhook.site, oast.online, webhook, A000).
3. ES read-only: `rubygems-goimport-campaign` — slvhg151 present only as
   `jfrog_inventory` (XRAY-1023618); three `webhook-*` July-wave names found as
   JFrog-only records (XRAY-1079203/204/246).

**What landed** (`webhook-deaddrop-hits-2026-09-27.jsonl`, 8 docs):
- 2 confirmed dead-drop records (slvhg151, southpxdatapp6pi) — May-12 wave
- 3 webhook-named July-7 candidates (name-only evidence, low confidence)
- 2 ambiguous marker hits (paste-linuxiarz 24775389 redacted; thecolony-ai unattributed)
- 1 negative-sweep summary record

**Wave attribution:** may-12 for the dead-drop pair (Diffend publish timestamps);
july-7 for the webhook-named trio (epoch suffixes 1783405583/5247/6220 →
2026-07-07 ~06:2x–06:37 UTC).

**Quality bar:**
- No full recovered credentials, keys, or payload exfil chunks are reproduced
  (none were found locally; the dead-drop URL chunks themselves were not in our
  corpus — only the package names and the Diffend page-pattern hit).
- Exact duplicates collapsed; nothing claimed as verified without tool evidence.
- Agents/infrastructure only: no operator identity, registrant details, or
  person-focused attribution pursued.
- ES index `webhook-deaddrops` created under the shared canonical schema
  (notes/gems-es-mapping.json) with `event.dataset.keyword` multi-field at
  creation, plus `marker`/`evidence_level` keywords.

**Open:**
- slvhg151 payload bytes: Diffend page holds the diff but the sweep stored only
  mechanism_notes, not the matched literals or URL chunks. Re-fetch Diffend diff
  page for slvhg151/0.0.2 to recover the actual `/api/v1/web_hooks` URLs.
- southpxdatapp6pi reconstructed files in this checkout are 1-byte stubs; the
  bulk harvest JSON log may hold the real bytes.
- July-7 Diffend sweep for webhook-payload/fire/capture packages (new open lane
  per standing reconciliation targets).
- July-7 wave (215 pkgs / 333 releases) has zero bytes in our corpus.

## Closure 2026-09-28 (workstream D)

Bounded marker sweep complete: JFrog-documented dead-drop grammar swept
across all on-disk corpora, gem tarballs, and the collusion-wiki ES corpus.
N=8 docs (2 webhook_deaddrop + 3 webhook_deaddrop_candidate + 2
marker_ambiguous + 1 sweep_negative) is the full result set — the negative
summary doc records the sweep itself. ES `webhook-deaddrops` _count=8
verified. Nothing further to pull; the technique's footprint is May-12 +
July-7 only.

## Closure 2026-09-28 (workstream C)

Naturally small: bounded marker sweep for the JFrog-documented webhook
dead-drop technique (`southpxdatapp6pi`, `web_hooks`, `A000`/`ZZEND`) across the
local corpus, 28 recovered .gem tarballs, and 3 ES indices. N=8 docs (2
confirmed May-12 dead-drops, 3 July-7 name-only candidates, 2 ambiguous marker
hits, 1 negative-sweep summary) is the full hit set. ES `webhook-deaddrops`
_count=8 verified, schema-drift clean. July-7 wave deep work continues under
the separate `july7-wave` lane, not this dataset.
