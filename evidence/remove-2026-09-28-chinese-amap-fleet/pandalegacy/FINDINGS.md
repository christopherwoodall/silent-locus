# CORRECTION (2026-10-05, parent review)

The verdict below ("our own probe marker") is **retracted**. Independent verification found:
- `uq.py` has only GET endpoints — our tooling cannot submit urlquery scans
- No agent was instructed to submit scans; no session evidence of submission via browser/curl/API
- The markers fit the operator's tag grammar; 2026-10-04 was the fleet's peak day (1,810 reports per the source article)
- 9-second-apart format variants match the operator's documented parallelism (cf. 8× uqcors.html in 2 min)

The `pandalegacy` / `mochou` / `customua` reports are **operator UA-evasion tests**, per the parent's original analysis:
systematic UA A/B testing (`taersi-mobile-ua`, `uqcustomua` + Googlebot spoof, bare `Mozilla/5.0`/`mobile`/`desktop`/`0`)
with self-documenting tags. The UA-anomaly detection method is validated; the attribution was not.

--- original (superseded) findings follow ---

# pandalegacy follow-up — Findings (2026-10-05)

## Verdict: `pandalegacy` is OUR OWN probe marker, not a new operator tag

The three UA=`"0"` reports that the parent agent found via UA anomaly are **our own
2026-10-04 custom-UA/tag experiments**, not a new operator testing the grammar.
The lead is closed as a self-footprint — with one genuine methodological win.

### Evidence

1. **Sibling documentation**: `farmable-surfaces/ua-inventory.md` (built by the
   farmable-surfaces agent from the same corpora) explicitly classifies these URLs as
   "our 2026-10-04 custom-UA experiments," listing `pandalegacy20261004` and
   `claude20261004mochou` among the probe markers alongside `customua-20261004`,
   `bazaar20261004a`, `research20261004a`, `uqcustomua20261004` (1,183 probe reports total).

2. **Pattern match**: our `raw/page_*.json` contains dozens of systematic
   `uqscan=<word>20261004<letter>` probe URLs from Oct 4 — `claude20261004target` (36),
   `target20261004a` (27), `research20261004` (23), `njxzgz20261004s/p` (24 each), etc.
   `pandalegacy20261004` and `claude20261004mochou` are two more tag-words in the same
   experiment batch. The "9 seconds apart, two tag formats" (`pandalegacy1791089321`
   vs `pandalegacy20261004`) is the experiment's epoch-vs-date format arm, not an
   unknown actor.

3. **UA=`"0"` explained**: the degenerate UA value was the experiment arm testing
   whether urlquery records arbitrary `settings.useragent` values verbatim (it does).
   UA=`"0"` appears on exactly these 3 unique reports across 5,899 scanned report
   records (deduped to 3) — no other submitter uses it.

4. **Nowhere else on Earth**: `pandalegacy` has zero agent-related hits on web search
   (only the unrelated Fortnite creator PandaLegacy), zero GitHub code hits (only
   expired-domain lists and creator-code CSVs), zero in Common Crawl's index for the
   queryable window (CC API timed out on wildcard queries — recorded as blocked, not
   negative), and zero in openai-agent-traces, swarmtraces-verification, or any other
   local corpus. `mochou` likewise absent from all other corpora.

5. **No new urlquery reports**: authenticated API still 429-throttled; htmx endpoint
   returns 0 for `pandalegacy`/`mochou` (recent-biased; the Oct-4 probes have aged out
   of its window). Nothing to re-fetch.

### Answers to the task's key question

> Is `pandalegacy` the operator testing new tag words, a copycat imitating the
> grammar, or a researcher probing?

**None of the above — it was us.** A prior agent in this hunt submitted these URLs to
urlquery on Oct 4 as controlled custom-UA/tag experiments. The parent agent's "UA
anomaly" discovery re-found our own footprints.

### Genuine win preserved

The UA-anomaly *method* is validated even though this instance was a self-hit: scanning
`settings.useragent` across 5,899 reports surfaced the only 3 non-conforming submissions
in the corpus. Applied to fresh data (not our own experiments), this is a working
distinct-submitter detector. The farmable-surfaces `ua-inventory.md` now documents the
organic-vs-probe split for all future analysis.

### Dataset hygiene

- `events.jsonl` (2,141 records): only 6 records (0.3%) match probe-marker patterns —
  the normalized dataset is essentially clean.
- `raw/page_*.json`: contains ~1,183 probe reports intermixed with organic fleet data.
  Any future mining of raw pages must exclude URLs matching the probe-marker set
  (`20261004` tag words, `customua`, `bazaar20261004`, `uqcustomua`) or use
  `farmable-surfaces/ua-inventory.md`'s organic/probe split.
- `ALL_LINKS.md` (2,673 URLs) includes probe-report URLs; noted, not rebuilt.

### Open (blocked, not skipped)

- Re-query `pandalegacy` / `mochou` on the authenticated urlquery API when the 429
  quota resets, to confirm no *organic* (non-probe) report has appeared since.
- Common Crawl wildcard queries time out; a targeted CDX pull for `amap.com` URLs
  containing `pandalegacy` remains untested.

Nothing pushed, per instructions.
