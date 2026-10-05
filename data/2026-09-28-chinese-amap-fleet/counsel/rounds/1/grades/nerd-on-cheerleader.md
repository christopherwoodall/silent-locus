# NERD PEER GRADES — on CHEERLEADER (round 1)

*Graded 2026-10-05 ~08:20 UTC. Method: re-pulled the urlquery recency index via `uq_htmx_curl.py` and grepped ~688k corpus events myself. Claims that didn't reproduce don't survive.*

**Adversary overlap:** none. The Adversary's five round-1 kills (letss.win httpbun, Tencent 62.234.187.97, jina-lookalikes, `?r=` nonce family, `/xss-osint-insert` double-submit) touch zero Cheerleader findings. The headline "campaign alive right now" is not pre-killed.

---

## F1 — Fresh 07:11Z probe: `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`, untagged, fresh POI

- **Novelty:** GENUINELY NEW. The report is real, and the POI is genuinely new to us.
- **Evidence:** OBSERVED — reproduced. Full report ID `c25ffacb-8450-47d8-8e20-e454ff3a88e3`, `date: 2026-10-05T07:11:00Z`, URL `amap-pc-ssr.amap.com/ssr/place/B000A7O1CU`, untagged. Corroborating byte: `B000A7O1CU` returns **zero hits** across `data/2026-09-28-chinese-amap-fleet/`, `openai-agent-traces/data/traces.jsonl` (589,972 events), and `data/2026-10-01-oai-tag-sweep/events.jsonl` (96,353 events) — first-ever appearance.
- **Actionability:** yes — (a) `c25ffacb` goes into seen.json at the next poll; (b) POI `B000A7O1CU` goes on the POI watchlist; (c) any follow-up probe with a tag referencing this POI = campaign continuity confirmed.
- **Verdict: KEEP.** The headline finding of the round, and it's load-bearing on real bytes. Attribution to the operator is INFERENCE (untagged single report) — the Cheerleader labels it honestly, and the burst context carries it.
- *Nit (non-killing):* the claim "operator slipped a probe through *between* our polls" assumes poll coverage semantics I can't verify from the index alone (Poll H4 found 0 new, H5 errored). The temporal fact — probe exists at 07:11Z, monitor missed it — holds regardless.

## F2 — `claude20261005*` stem census: 4 hits (a, mobile, mobile1, mobile2); b/c/d/e/f/mobile3 = zero; stem quiet since 01:26Z while the campaign continued under sibling tag families

- **Novelty:** GENUINELY NEW for the census table. The stem itself was already observed (OURS); the namespace exhaustion mapping is new.
- **Evidence:** OBSERVED — spot-verified. My re-pulls: `claude20261005b/c/d/e/f/mobile3` = 0 hits each (exact-token queries, consistent with the Cheerleader's htmx-index tokenization note). The 4 positive rows carry report IDs + timestamps and match the recency index. The sibling-family timestamps (`nested20261005a/b` 01:46–01:47Z, `qdnewapi*`/`qdoldditu*` 04:11Z, epoch nonces 03:43Z) all reproduced in my pull.
- **Actionability:** yes — a `claude20261005b`-or-higher / `mobile3`-or-higher tag appearing = instant anomaly for the monitor; same for any new stem on the `20261005` date.
- **Verdict: KEEP.** The census is real; the "harness burns through a tag taxonomy" tell is INFERENCE and labeled as such. It's a reasonable read, not a proven one — but the evidence table underneath it is solid.

## F3 — Date-stem suffix census `20261005<a–f>`: exhausted at `c`; `d/e/f` zero; tianshanzoo/navy971 already in mimic's drift report (OURS)

- **Novelty:** OURS-extension. The suffixes themselves were already logged (mimic's drift report; ALL_LINKS.md); the exhaustion boundary is the new bit.
- **Evidence:** OBSERVED. `anhui-famous-20261005a/b` (00:31/00:36Z) and the `c`-suffix `navy971-20261005c` are consistent with the index; the zero-claims on `d/e/f` are cheap to reproduce and consistent with F2's verified zeros.
- **Actionability:** yes, weak — same anomaly-trigger as F2 (a `d`-suffix = new signal). Mostly a monitoring convenience.
- **Verdict: KEEP, low priority.** It's a ledger entry, not a discovery — but the counsel needs the ledger, and the Cheerleader correctly flags which parts are hers and which are mimic's. Good provenance hygiene again.

## F4 — Cadence shape: hourly waves 01:25–04:11Z, ~3h gap, then 07:11Z single probe — "operator-shift or task-batch rhythm"

- **Novelty:** INFERENCE-graded synthesis over OURS observations. Not a new fact; a new read.
- **Evidence:** INFERENCE on OBSERVED bursts — the wave timestamps check out against the index (01:25–01:47, 02:09–02:33, 03:16–03:43, 04:11, 07:11). The rhythm read is the Cheerleader's interpretation, labeled as INFERENCE. Fair under the charter.
- **Actionability:** yes, soft — compute the inter-arrival distribution and compare against the Oct-4 session window (codebreaker's 15:01–17:00Z marker epochs) before the Conspiracist leans on it. The timestamps are all there; the binning is a 10-line job.
- **Verdict: WOUNDED → leaning KEEP as a working hypothesis.** It survives because the burst timestamps are real and the Conspiracist can test it. It does NOT survive as a conclusion — "operator-shift" is a story laid over 5 data points.
- **Nerd correction (byte-level, from my own pull):** the 02:09–02:33 wave is NOT "untagged + henanmuseum" only. The recency index shows *tagged* variants the Cheerleader didn't enumerate: `uqm=1/2/3` (`m.amap.com/detail/index/poiid=B03DF05V64?uqm=1`, 02:30Z) and `uqattempt=0/1` (`www.amap.com/place/B03DF05V64?uqattempt=0`, 02:13Z). These are **new tag grammar shapes** (`uqm`, `uqattempt`) not in the Cheerleader's tag census. The campaign was still tagging at 02:13–02:30 — the "labels ran dry" narrative in F2/F4 is premature. Log these two grammars; they're as much a census item as the epoch nonces.

## F5 — Tooling win: `uq_htmx_curl.py` (landed 05:16Z) returns `url.domain:amap.com` in ~10s where `uq_htmx.py` times out at 120s; recommendation to switch the live-monitor's domain queries

- **Novelty:** GENUINELY NEW to the Counsel. The tool landed this morning; the recommendation is a first.
- **Evidence:** OBSERVED — I used the curl variant for this grading session and it returned clean in ~10s, including the 07:11Z find. (I did not reproduce the `uq_htmx.py` 120s timeout myself, so the "twice timed out" half rests on the Cheerleader's session + the monitor's failed polls.)
- **Actionability:** yes — concrete, one-line: switch the live-monitor's domain queries to `uq_htmx_curl.py`. This is the most immediately actionable item in either file.
- **Verdict: KEEP.** A tool claim that survives contact with the tool. Rare. Treasure it.

## HONEST NULLS

- **N1 — "11 live webhook.site inboxes" UNRECONCILED:** KEEP. This is the correct move: codebreaker's 4 alive (newest request 03:05Z) vs an un-reproducible "11" — refusing to cheer a number you can't reproduce is the whole job. Actionable: Chair/Adversary must reconcile before anyone repeats the figure.
- **N2 — `anhui-famous` killed by ALL_LINKS.md:2683–84 + grammarian's E-hyph catalog:** KEEP. Self-killing a finding with the bytes is discipline, not failure. OURS, correctly filed.
- **N3 — "No new tag variants beyond the known set":** WOUNDED. The claim as stated is **wrong at the bytes level** — `uqm=1/2/3` and `uqattempt=0/1` (02:13–02:30Z) are tag variants the Cheerleader's census doesn't enumerate, and they're visible in the same recency pull. Downgrade to "no new variants *in the families I censused*; two additional grammar shapes (`uqm`, `uqattempt`) found on re-pull, unclassified." The spirit (only time is moving) is fine; the letter is falsified.

---

## Nerd's summary

The headline (F1) is the real thing: a genuinely new untagged probe on a genuinely new POI, 50 minutes before the sweep, on bytes I reproduced independently. F2/F3 are solid census work with honest provenance splits. F5 is the round's most actionable recommendation. Deductions: F4's "untagged" wave framing and N3's "no new tag variants" both miss `uqm`/`uqattempt` grammars that are sitting in the same index pull — the campaign was still tagging at 02:30Z, so the "labels ran dry" narrative is overstated. Nothing here is adversary-killed. Overall grade: **KEEP the file, WOUNDED on F4/N3 pending the `uqm`/`uqattempt` grammar classification.**
