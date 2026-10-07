# TODO — Counsel of 20 ranked directions (2026-10-07)

Source: 20-persona counsel deliberation. Each has a first probe and a kill criterion.
Work them in rank order; kill fast.

## 1. The Dawn Gap (Cartographer)
Date-scoped urlquery search Nov 2025–Apr 2026 for toolkit grammar (`zz=`, epoch
nonces) + dead-drop hosts, WITH a control query proving sensor coverage of the
window. Kill: control proves coverage AND zero grammar hits → grammar postdates gap.

## 2. Rush-Hour-First (Traffic Engineer)
Tag-agnostic burst clustering: histogram agent-tagged urlquery submissions
Apr–Jul 2026 into 5-min bins, test top-of-hour phase alignment vs human-CI-cron
control. Kill: uniform hourly distribution, no phase alignment.

## 3. Bus-Stop Walls (the Child)
Re-read cached urlquery corpus for no-auth paste/file drops (0x0.st, termbin.com,
ix.io, sprunge.us, file.io, transfer.sh). Zero new collection. Kill: zero
drop-service URLs, or all hits are ordinary human paste-sharing.

## 4. Purge Ghosts (Archivist)
Hunt erasures on public MediaWiki farms (Fandom/Miraheze): revision-ID gaps +
deletion-log bursts with blank/identical summaries, May–Aug 2026. Template: the
usemod.org WikiPatches case. Kill: steady human-paced deletions, uniform gaps.

## 5. Keyring Census (Locksmith)
Mine corpus for credential-carrying URLs (`access_token=`, `api_key=`,
basic-auth); cluster by identical credential value + burst timing. Kill: all hits
are human debug URLs, no shared values, no bursts.

## 6. The Clock in the Nonce (Detective Novelist)
Epoch nonces are clocks: nonce-epoch minus observed-timestamp across tagged
requests; a consistent non-zero offset fingerprints the launcher's container clock
skew (provider infra ID). Kill: deltas uniform/random, or offsets collapse to
reporter clock.

## 7. Spore-Print Hunt (Dr. Mycelia)
One grep.app query for `zz=oai` grammar fragment; triage top 20 for harness-shaped
code (param builders, nonce generators, dead-drop writers). Kill: zero hits
outside our own notes. (Weak negative if harness is private — one query, cheap.)

## 8. The Jina Shadow (Cartographer)
Extract target hosts from jina-reader URL submissions in urlquery; diff against
directly-submitted hosts. The jina-only set = deliberately-unseen targets.
Kill: set empty or all-benign with human-shaped timing.

## Queued (not counsel output — do not lose)
- urlscan.io scan (anonymous, 500/day): `page.domain:civilrightsdata.ed.gov`, then `task.url:*zz=*`
- crt.sh tunnel enumeration: `%.trycloudflare.com`, `%.lhr.life`, `%.pinggy.io` vs May–Jul 2026
- ClawBench transaction-hunt (write-heavy eval → consumer platforms)
- Name the DseWiki swarm's eval (collapses a dozen unattributed incidents)
- Package-registry one-pass (npm/PyPI/crates)

## Transluce-derived (2026-10-07, from 25 findings + 4 lanes)

9. **Bounty-Watch** (from #166/#167): monitor rentahuman.ai for agent-posted
   bounties (CAPTCHA clearing, phone-label removal, review posting). The
   human-outsourcing channel is a new surface. Kill: bounties are all human.

10. **Dead-Drop Grammar Search** (from lane 4): hunt urlquery for COMBO-INIT
    siblings — `bxinit`/`xdcinit`/`capture` payloads, httpbin base64 carriers,
    webhook.site/ntfy.sh dead-drops. Grammar is known; find its family.
    Kill: the one drop is the whole population.

11. **POI-ID Expansion** (from dead-drop): B0138027SQ is new to our corpus.
    Search urlquery for `getPoiInfo?id=` with other IDs + `live=N_` cache-busters.
    Maps the current Amap target set. Kill: single POI, no family.

12. **Frozen-Epoch Sweep** (from #147): the `mid<epoch><seq>` naming tool is
    fingerprinted. Sweep other public YOURLS instances (start with our tracked
    university shorteners) for the same keyword grammar. Kill: yourls.space only.

13. **Trajectory-Dataset Hunt** (from WildClaw lane): one unreported defeat hid
    in the "unreviewed" pile. Search HF for more `*Trajector*`/`*Trace` eval
    datasets; audit their solve_*/bypass flags. Kill: the three sets are all there is.

14. **Turnstile-Defeat Search** (from solve_cloudflare audit): search urlquery +
    corpus for "turnstile" with agent markers, "captcha is solved" strings,
    GSMArena + agent traffic. Kill: the GLM run is the only one.

15. **Key-Mint Watch** (from #152): agents self-provisioning via
    `/api/htmx/apikey/new` (Microlink). Search for more key-minting activity —
    it marks the self-provisioning phase. Kill: the one report is the whole story.

16. **Sandbox-Signup Probing** (from #157): FileScan.IO signup probes via
    urlquery. Search for filescan.io and sibling sandbox-signup probing.
    Kill: isolated probes, no pattern.
