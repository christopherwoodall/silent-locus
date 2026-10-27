# Verifier report: broad agent-egress hunt

## Terms used here

- **PASS:** the raw capture or the live re-fetch supports the claim.
- **FAIL:** the evidence contradicts the claim.
- **UNVERIFIED:** the check could not run. A blocked check is not a pass.
- **SECONDARY:** evidence from a third party, not first-hand capture.
- **Raw capture:** a file saved from a source during the lane run.
- **On-disk:** checked against the saved file in this repo.
- **Live:** checked again from the source on 2026-10-27.

## Method

- Read-only work only. No POST. No login. No commit. No push.
- No Factum write. No file under `data/records/` or `data/.local/` was touched.
- No raw capture was changed.
- The urlscan detail gate was not bypassed. Detail files hold only the login warning, as the lane states.
- GitHub live checks used unauthenticated GET. The shared egress IP hit rate limits on some calls. Those calls are UNVERIFIED live, not failed.

## Final verdict: SHIP-WITH-FIXES

Ship after fix F1 below. Fix F1 is one count correction in one lane note.
No blocker was found. No citation was contradicted by its raw capture.
The three live-UNVERIFIED GitHub items are PASS on-disk, so they do not block shipment. The coordinator can retry the live check later.

## Fixes required before shipment

- **F1 (urlscan lane, candidate 2):** change "6 scans" to "5 distinct scans".
  The lane lists 5 scan URLs and 5 page names. The raw search files hold 5 distinct scan IDs. The count 6 comes from one scan (`recon.html`) that appears in two search files. So the true count is 5 distinct scans, in 6 search rows.
- **F2 (optional, not a blocker):** add one line to the GitHub-issues lane that ranked headings paraphrase the issue titles. The raw titles differ in words but match in substance. See the table below.
- **F3 (optional, not a blocker):** the linguist raw dir has no per-file hash files for its two provenance files. Its `SHA256SUMS` covers only the two JSON files. Other lanes hash provenance files too. This is a completeness gap, not a content failure.

## SHA256SUMS results, per raw dir

All dirs pass. Zero failures in any dir.

| Raw dir | Files hashed | Result |
|---|---|---|
| `cryptologist/` | 4 | PASS |
| `github-code/` | 16 | PASS |
| `github-issues/` | 12 | PASS |
| `huggingface/` | 948 | PASS |
| `linguist/` | 2 | PASS, but see F3 |
| `urlquery/` | 162 | PASS |
| `urlscan-wayback-crtsh/` | 54 | PASS |

Command used in each dir: `sha256sum -c SHA256SUMS`.

## Signed-URL rule grep result

- Searched all 7 lane notes for `Signature=`, `OSSAccessKeyId=`, and `Expires=` with a value after the `=` sign.
- Result: no value match. PASS.
- Parameter names alone appear in `cryptologist-notes.md` and `linguist-notes.md`. Names alone are allowed. No signed query string, signature, token, or credential-shaped value appears in any lane note.

## GitHub-issues lane: 11 ranked items

All 11 items exist in the raw search captures. All 11 dates match the lane note. All 11 states match the lane note (only item 1 is closed). All 11 key body terms were found in the raw bodies. Lane headings paraphrase the raw titles; the substance matches.

| # | Item | On-disk | Live re-fetch |
|---|---|---|---|
| 1 | CorbanuTerminal#876, 2026-10-16, closed | PASS. Raw title: "Linux: deny new user namespaces to agent commands under Moderate and Aggressive (#826)". Body holds `unshare -Ur`, `tmpfs`, `EPERM`. | UNVERIFIED. Shared-IP rate limit on both tries. State and date rest on the capture. |
| 2 | LifeSciences#345, 2026-10-12, open | PASS. Body holds `metadata.google.internal`, `16`, `38.2`. | PASS. Title, state open, date 2026-10-12 match. |
| 3 | OpenSkynet#77, 2026-05-30, open | PASS. Body holds `web_extract`, `169.254.169.254`. | PASS. Title, state open, date 2026-05-30 match. |
| 4 | ms-agent#1020, 2026-10-19, open | PASS. Body holds `169.254.169.254`, `100.100.100.200`. | UNVERIFIED. Shared-IP rate limit on both tries. |
| 5 | guidance#1498, 2026-07-29, open | PASS. Body holds `168.63.129.16`, `100.100.100.200`. | PASS. Title, state open, date 2026-07-29 match. |
| 6 | kyvor#20, 2026-10-07, open | PASS. Body holds `unshare`, `umount`. | UNVERIFIED. Shared-IP rate limit on both tries. |
| 7 | Wingman#278, 2026-09-19, open | PASS. Body holds `metadata.google.internal`. | PASS. Title, state open, date 2026-09-19 match. |
| 8 | Grok-Bot-Clone#14, 2026-08-20, open | PASS. Body holds `curl -T`, `upload-file`. | PASS. Title, state open, date 2026-08-20 match. |
| 9 | hermes-agent#108236, 2026-09-11, open | PASS. Body holds `curl -o`. | PASS. Title, state open, date 2026-09-11 match. |
| 10 | Project-Bootstrap-Protocol#108, 2026-09-17, open | PASS. Body holds `curl -sSL -o /tmp/x.sh`. | PASS. Title, state open, date 2026-09-17 match. |
| 11 | bailey#19, 2026-09-16, open | PASS. Body holds `clone`, `unshare`. | PASS. Title, state open, date 2026-09-16 match. |

Query totals on-disk also match the lane table for all 12 queries (for example q01 57,107 with 100 items; q10 6,553 with 99 items; total fetched 1,199). PASS.

Honest-null claims on-disk: shape 3 has no ranked hit, shape 6 has no ranked hit, and no ranked item shows a credential actually read. The captures support these nulls within the screened page-1 sample. The lane states the sample limit plainly. PASS, with the stated limit.

Caveat not re-verifiable: the lane note says the shared core bucket showed 10 of 60 left at run start. No capture records that rate state. This is UNVERIFIED as history, not contradicted. It does not change any ranked item.

## GitHub-code lane: honest null and named repos

- Query totals on-disk match the lane table for all 16 queries (for example c06 1,280,000; c14 63; c15 73; 30 items each; 480 total). PASS.
- All 15 named repos in ranked items 1 to 5 appear in the raw fragments: `cdxiaodong/cain-agent`, `ASCIT31/Dark-Moon`, `awarexone/Agentic-Bug-Hunter`, `SnailSploit/Claude-Red`, `Zyrexnn/Cybermes`, `wtogami/qwen-block-proxy-artifacts`, `Enntity/sparkqwen`, `enncoded/pi-block-proxy-artifacts`, `javierbits/qwen38-prefill-repro`, `alextra-lab/personal_agent`, `bendyline/gezel`, `ai-job-search-dev/ai-job-search`, `different-ai/openwork`, `omnirush-ai/omnirush-gui`, `gadievron/raptor`. PASS on-disk.
- Key skill and guard paths appear in fragments: `skills/gcp-attack.md`, `conf/agents/gcp.md`, `sandbox-escape-techniques`, `TOOL-GUARD`, `security_guards.py`, `egress-indicators.ts`, `probes.py`. PASS.
- Live repo existence: 4 of 5 spot-checked repos return public repo records (`wtogami/qwen-block-proxy-artifacts`, `javierbits/qwen38-prefill-repro`, `SnailSploit/Claude-Red`, `ai-job-search-dev/ai-job-search`). PASS.
- Live repo existence for `cdxiaodong/cain-agent`: UNVERIFIED. Shared-IP rate limit. The repo is present on-disk in the c11 capture, so the on-disk claim stands.
- Honest-null claim (zero screened items show an agent doing a hunted shape): consistent with the fragment evidence and the lane's own classification of every ranked item as mention, doc, guard, or instruction artifact. PASS within the stated 30-per-query sample limit. Full-file reads were not done, and the lane says so.

## Hugging Face lane: honest zero

- API search files: 45. Total rows summed from the files: 1,109. Unique dataset IDs: 821. Both match the lane note. PASS.
- Shape-term dataset searches return 0, except `cloud_metadata` with 1 row (the wine-label false positive). Model `unshare` returns 18 rows. Spaces return 0 for all shape terms. All match the lane note. PASS.
- Card text fetched: 150 dataset READMEs, 30 model cards, 74 trace files, 12 tree listings. All match the lane note. PASS.
- README prose math checks: 150 minus 30 with no README minus 7 YAML stubs equals 113 with prose. The lane says 113. PASS.
- Grep outputs: README grep sections are empty. Trace grep holds only the 2 localhost `curl -o /dev/null` lines the lane triages out. Model-card grep holds only the 2 Qwen-AgentWorld logo lines the lane triages out. PASS.
- The zero-candidate verdict matches the raw evidence within the stated limits (top-150 READMEs, top-30 model cards, Parquet and zip files unsearched, gated sets unsearched). The lane states each limit. PASS.

## urlquery lane: totals, details, and Part B live re-check

- Fetch-file rows summed from the files: 1,083. Matches the lane note. PASS.
- Fetch totals match the lane table for every checked query, including aliyuncs 48,965, oss-cn 6,649, routify 79, metadata 223, PROBE_PAYLOAD 4, resolv.conf 95, and trace 230. PASS.
- Detail-checked rows: 11 detail files exist, matching the 11 rows in the lane table. PASS.
- Detail counts match exactly for all 11: trustxx 98 requests (79 GET, 10 POST, 9 OPTIONS; 32 bucket GETs); smaflowi 80 (61 GET, 10 OPTIONS, 9 POST; 30 bucket GETs); charlesg 66 (65 GET, 1 OPTIONS; zero routify requests); bare routify host 2 GETs; metadata page 218 (216 GET, 1 OPTIONS, 1 POST); unshare page 40; resolv page 16; oss-cn page 46 with zero bucket requests; probe docs page 29 GETs; S3 block page 5 GETs with 2 to the S3 host and title Blocked; S3 landing page 4 GETs with 1 to the S3 host. PASS.
- Part B on-disk probes match: routify full host 1, sanmaohe host 0, sanmaohe full host 0, proxy_temp_file 0, PROBE_PAYLOAD_ABC123 0, vendor routify hosts 0 each. PASS.
- Part B live re-check (read-only search, limit 1, run for this report): routify full host 1, and the one row is the same bare-host report `0bec7c6c` dated 2026-08-16. Sanmaohe full host 0. proxy_temp_file 0. PROBE_PAYLOAD_ABC123 0. PASS.
- The lane's parser caveats (flag-form totals are not nested sets; hyphen-form and `url.domain:` zeros are not absence; the 1 unreachable routify row) are consistent with the raw files. PASS.

## urlscan, Wayback, crt.sh lane

- Urlscan search totals on-disk match the lane table for all 15 searches, including metadata 14, metadata-google 2, metadata-100 4, oss-cn-beijing 668 with 100 fetched, aliyuncs 10,000 capped with 100 fetched, sanmaohe plain 0, routify-file-proxy 0, proxy_temp_file 0, unshare 0, PROBE_PAYLOAD 0. PASS.
- Sanmaohe candidate 1: all 4 scans exist in the oss-cn family file with the stated dates and paths: 2026-10-27T10:39Z apex, 2026-10-27T07:03Z `/upload/test.bin`, 2026-10-27T00:01Z apex, 2026-10-26T17:23Z `/upload/`. Scan IDs match the lane note. PASS.
- Sanmaohe candidate 1 live re-check: the apex scan `01a17cf1` dated 2026-10-27T10:39:49Z is present in a live anonymous urlscan search. PASS.
- Metadata rig candidate 2: FAIL on count only, PASS on substance. The lane says "6 scans" but lists 5 scan URLs and 5 page names (`recon.html`, `recon2.html`, `probe.html`, `navchk.html`, `go.html`). The raw files hold 5 distinct scan IDs, all on 2026-10-22, all sharing one path id across two Amazon hosts, all pointing at metadata paths. The 6th count comes from the `recon.html` scan appearing in two search files. Fix F1 corrects the count. The rig shape itself is confirmed.
- Metadata rig live re-check: a live anonymous search for `169.254.169.254` returns total 14 and includes all 5 rig scan IDs. PASS.
- Result detail files: all 19 hold the same login-warning bytes and no scan content. The lane's login-gate claim is confirmed, and the gate was not bypassed. PASS.
- Wayback on-disk: sanmaohe exact and prefix empty; routify-sg exact and prefix empty; proxy_temp_file empty on retry; aliyuncs domain 1,000 rows (cap hit); metadata-169 588 rows; metadata-google 9 rows, all 2022. All match the lane note. PASS.
- crt.sh on-disk: sanmaohe exact and wildcard empty; routify-sg exact and wildcard empty; vendor hosts empty. All match the lane note. PASS.
- The lane's warnings are honest: the plain `sanmaohe` urlscan zero is not trusted (the family search finds 4 rows); shape 5 is UNCHECKED in urlscan, not zero; IPv6 metadata form is UNCHECKED, not zero. PASS.

## Linguist lane: describing texts

- Zenity NEW-1: live page fetch returns HTTP 200. Title matches: "AgentCorruption: How A Single Prompt Collapsed The Entire Cloud Security Model". Page text holds the 2026-10-08 date and metadata-service content. The vendor-dispute framing in the lane note is consistent with the page. PASS.
- Field Effect NEW-2: live page fetch returns HTTP 200. Title matches. Page text holds "April 23, 2026, Field Effect MDR detected" and the `/tmp` file-grab chain. The lane date (incident detected 2026-04-23) matches. PASS.
- Bex NEW-3: live page fetch returns HTTP 200. Title matches the Cowork sandbox-escape topic. Page text holds `unshare`, `SharedRoot`, and the July 23 disclosure date. The lane grades this as a second-hand summary, not the primary report. That grade is honest and stands. PASS as a summary citation.
- NEW-4: the lane itself marks this as a candidate, not verified, with the primary source unfetched. No stronger claim is made. PASS as a lead only.
- The two akasecurity bodies in the linguist raw dir match issue numbers 926 and 927, both open, both dated 2026-10-26. PASS.
- Circular-downstream and known-prior-sighting exclusions are stated as method, not as new findings. No contradiction found. PASS.

## Cryptologist lane: hidden structure

- The shape-only extraction file lists 5 genuine proxy-shaped URLs, all with the stated host, path shape, and the 3 parameter names. PASS.
- Trace-ID structure claim, checked against the prior hunt raw file (`hangtiancheng/yukino-code#2`, 2026-10-06): 5 URLs found, 2 distinct trace IDs, both sharing the first 16 hex characters and the last 5 hex characters. PASS.
- Final-segment claim: 4 segments of 32 hex characters and 1 of 33. PASS.
- The lane states its INFERENCE limits plainly (structured trace ID is INFERENCE, not proven; the 33-length cause is unknown). PASS.
- The lane's signed-URL rule restatement matches the grep result above: names and path shape only. PASS.

## Counts

- Citations checked on-disk: 11 GitHub-issues items, 16 code queries, 45 HF search files, 28 urlquery fetch files plus 11 detail files, 15 urlscan searches plus 19 detail files, 8 Wayback checks, 10 crt.sh checks, 3 linguist describing texts, and the cryptologist grammar claims.
- On-disk: PASS on every citation except the urlscan rig count (FAIL on count only, see F1).
- Live: 8 of 11 GitHub-issues items PASS, 3 UNVERIFIED (rate limit); 4 of 5 code repos PASS, 1 UNVERIFIED (rate limit); Zenity PASS; Field Effect PASS; bex summary PASS; urlscan sanmaohe apex scan PASS; urlscan rig IDs PASS; urlquery Part B 4 of 4 PASS.
- FAIL count: 1 (the rig count, minor, fixable in one line).
- UNVERIFIED count: 5 live checks, all blocked by the shared-IP GitHub rate limit, none contradicted. The historical quota note in the issues lane is also UNVERIFIED as history.
- No citation was contradicted by its raw capture.

## What this report did not do

- No comment fetch for the 11 ranked GitHub items. The lane flags this as an open question. Comment text could add transcripts or model names. It was not checked here.
- No full-file read for GitHub-code fragments. Classification rests on fragments, as the lane states.
- No Parquet, zip, gated-set, or space-code read for Hugging Face. The lane states these limits.
- No urlscan detail read. Detail is login-gated. The gate was left in place.
- No live re-check of urlscan search totals beyond the metadata search and the sanmaohe apex scan. Totals for the capped family searches move with time and were verified on-disk only.
