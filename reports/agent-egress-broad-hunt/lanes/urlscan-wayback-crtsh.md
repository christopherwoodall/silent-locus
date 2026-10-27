# Lane: urlscan, Wayback, crt.sh — broad agent-egress hunt

## Status

This lane is STAGED, not filed. No file here was committed or pushed.
No Factum write was made. No login was used. All fetches were
read-only GET requests. Raw files were never changed or redacted.

## Terms

- SECONDARY: evidence from a third party, not a first-hand capture.
- Behavior shape: a pattern of actions, not a host name string.
- Call-home: an agent sends data to an outside host without a user order.
- Confidence LOW: the match is thin, or only a string match.
- Confidence MEDIUM: the shape is clear, but the cause is not proven.
- UNCHECKABLE: the method failed, so zero cannot be claimed.
- Zero: the method ran clean and returned no rows.

## Method limits (read first)

- urlscan search is anonymous only. The search API itself limits
  results to the last 30 days. Every search response in this lane
  carries `search_date_limit_days: 30`. Totals below are 30-day totals.
- urlscan full scan detail needs a login. This lane did not log in.
  All 19 result-detail fetches returned the same login warning:
  "You're not logged in!" No request list, no page body, and no
  method (GET, PUT, POST) is visible for any candidate scan.
  Search metadata (task URL, page URL, date, IP, ASN) is all we have.
- urlscan capped totals at 10,000 for the big OSS family searches.
  Only the 100 newest rows were fetched for each such search.
- Wayback CDX ran on plain HTTP port 80. The backend failed twice
  with a "Temporarily Offline" page. Both queries were retried after
  60 seconds. The first attempts are kept as `.attempt1.json` files.
- Wayback prefix and domain methods are weak. A 1,000-row cap cut
  the aliyuncs domain set. Absence in a capped set is not proof.
- crt.sh is a certificate log search. A certificate is a public
  proof that a host owns a name. A 502 server error means
  UNCHECKABLE, never zero.

## What is NOT new (do not re-claim)

- Fleet B already found: routify urlscan zeros, sanmaohe crt.sh
  502 trouble, and Wayback routify limits. This lane does not
  re-claim those as new.
- The Cohere seed itself (Qwen, sanmaohe PUT probe, routify
  proxy) is context, not a hit.

## urlscan searches (all anonymous, last 30 days)

| Search | Total | Fetched | Note |
|---|---|---|---|
| `169.254.169.254` | 14 | 14 | Full set. See candidate 2. |
| `metadata.google.internal` | 2 | 2 | Full set. See candidate 2. |
| `100.100.100.200` | 4 | 4 | Full set. See candidate 2. |
| `sanmaohe` | 0 | 0 | UNRELIABLE zero, see warning below. |
| `routify-file-proxy` | 0 | 0 | Zero. Real, in this window. |
| `aliyuncs.com` | 10,000 (capped) | 100 newest | Same 100 rows as domain search. |
| `domain:aliyuncs.com` | 10,000 (capped) | 100 newest | Same 100 rows as plain search. |
| `proxy_temp_file` | 0 | 0 | Zero. Real, in this window. |
| `unshare` | 0 | 0 | Zero. Real, in this window. |
| `storage.googleapis.com` | 10,000 (capped) | 100 newest | No agent marker in fetched rows. |
| `blob.core.windows.net` | 10,000 (capped) | 100 newest | No agent marker in fetched rows. |
| `r2.dev` | 10,000 (capped) | 100 newest | No agent marker in fetched rows. |
| `PROBE_PAYLOAD` | 0 | 0 | Zero. Real, in this window. |
| `s3.amazonaws.com` | 10,000 (capped) | 100 newest | No agent marker in fetched rows. |
| `oss-cn-beijing.aliyuncs.com` | 668 | 100 newest | See candidate 1. |

Warning on the sanmaohe zero: the plain `sanmaohe` search returned
0, but the `oss-cn-beijing.aliyuncs.com` family search surfaced 4
sanmaohe rows in its 100 newest. The plain-search zero is therefore
NOT trusted. The family search is the true source for sanmaohe rows.
Do not cite the plain-search zero as absence.

## Ranked candidates

All candidates are grade SECONDARY by default. No candidate names
a model. No candidate proves live exfiltration. No candidate proves
an agent caused the traffic.

### 1. LOW-MEDIUM — sanmaohe bucket shows fresh upload-path scans

- Behavior shapes: (2) object-storage upload path, (3) named probe
  host from the Cohere write-up.
- What was seen: 4 scans in the family search, all with the bucket
  as the task host:
  - 2026-10-27T10:39Z, bucket apex scan.
    Scan: https://urlscan.io/result/01a17cf1-bd4b-724c-9ce2-27febcda0fd7/
  - 2026-10-27T07:03Z, `/upload/test.bin` path scan.
    Scan: https://urlscan.io/result/01a17c2a-fcc7-745b-9e50-fa8f675b5415/
  - 2026-10-27T00:01Z, bucket apex scan.
    Scan: https://urlscan.io/result/01a17aa9-8860-75f2-8a0f-77e450fbbcaf/
  - 2026-10-26T17:23Z, `/upload/` path scan.
    Scan: https://urlscan.io/result/01a1793c-dc76-70ca-a6a8-4ac8d1e7ac7a/
- Why it ranks: the bucket is live and an `/upload/` path is being
  scanned days after the Cohere post. This is new activity in this
  lane's window. It is not in the Fleet B urlscan haul.
- Caveats: search metadata only. No request method is visible, so
  no PUT or POST is proven. The `/upload/test.bin` scan may be a
  researcher testing the bucket after the public post, not an agent.
  No model, no harness, and no payload are named in the metadata.
  Path shape only is given here. No signed query strings are copied.
- What it is not: this is not a repeat of the seed PUT probe. It
  is not proof of agent egress. It is a lead for the GitHub and
  urlquery lanes to check: who scans this bucket, and why.

### 2. LOW — metadata probe rig on two Amazon hosts, one shared path id

- Behavior shapes: (1) cloud-metadata reach, (6) recon-then-egress
  in URL shape only.
- What was seen: 6 scans on 2026-10-22 share one path id on two
  Amazon hosts. Page names are `recon.html`, `recon2.html`,
  `probe.html`, `navchk.html`, and `go.html`. Their query strings
  point at `169.254.169.254/latest/meta-data/` and at the
  `iam/security-credentials/` path under it. One page also names
  `metadata.google.internal`. Scans:
  - https://urlscan.io/result/01a16546-3e2c-76ca-a97e-af92aeaf1b6a/
  - https://urlscan.io/result/01a1653e-5e7f-736e-b595-4ed475a143ff/
  - https://urlscan.io/result/01a16538-d9bf-747a-b025-330e114fe2a1/
  - https://urlscan.io/result/01a164f6-74ba-71d9-9029-a278f24385f2/
  - https://urlscan.io/result/01a164f2-bdc9-75bc-b9ca-6de1ce1876a0/
- Why it ranks: the shared path id across two hosts and five page
  names looks like one deliberate test rig, not random hits. The
  rig tests exactly the metadata shape from the hunt brief.
- Caveats: search metadata only. No request list proves the rig
  reached a live metadata service. The rig may be human security
  research (SSRF testing), not an agent. No model is named. No
  agent marker appears in any task URL.
- Related rows, same shape, lower value: direct scans of
  `100.100.100.200/latest/meta-data/` on 2026-09-27 and 2026-10-13,
  and of the bare address on 2026-10-19, with no context at all;
  one httpbin redirect-to scan on 2026-10-21 pointing at the
  metadata credential path (a classic SSRF test shape); two
  httpbin base64 scans on 2026-10-18 encoding metadata-address
  pages (test payloads, not live reaches). All are string and
  shape matches only. None names an agent.

## Triaged out (do not rank)

- A page on `sprout.cautela.io` matched both metadata searches.
  It is most likely a write-up that lists endpoint addresses.
  No behavior is shown. String-only.
- Two webhook.site rows and one short-link row matched through
  page content. No behavior is shown in the metadata. String-only.
- Two vendor release hosts on `oss-cn-beijing` (a dev-platform kit
  and a CLI release) are ordinary vendor file hosting. Not agent
  behavior.
- One GCS bucket name holds the word for human sales staff in
  Spanish. That word is not proof of an agent harness. String-only.
- Azure, GCS, R2, and S3 newest-100 rows are ordinary hosting,
  phishing-style pages, and vendor buckets. No agent marker, no
  probe path, and no metadata string appears in their task URLs.
- One opaque-path OSS row carries query parameters. Parameter
  values are not copied here, per the signed-URL rule. The row
  shows no agent marker and is not ranked.

## Wayback CDX checks

| Check | Rows | Note |
|---|---|---|
| sanmaohe exact host | 0 | Empty. Method ran clean. |
| sanmaohe prefix | 0 | Empty. Method ran clean. |
| routify-sg exact host | 0 | Empty. Method ran clean. |
| routify-sg prefix | 0 | Empty. Method ran clean. |
| `aliyuncs.com/proxy_temp_file` prefix | 0 | Empty on retry 2. Attempt 1 was Temporarily Offline. |
| aliyuncs domain, collapsed, cap 1,000 | 1,000 rows, 2013 to 2026-10-16 | Cap hit. Zero sanmaohe, routify, or proxy_temp rows inside the capped set. Weak: rows past the cap were never seen. |
| `169.254.169.254` prefix | 588 captures, 2018 to 2024 | All old. Zero rows in 2025 or 2026. Most are 404 errors. This is old SSRF write-up noise, not new behavior. |
| `metadata.google.internal` prefix | 9 captures, all 2022 | All old. No new behavior. |

## crt.sh checks

| Check | Rows | Verdict |
|---|---|---|
| sanmaohe exact host | 0 | Zero. Checkable this run (Fleet B saw a 502; this run returned clean empty JSON). |
| sanmaohe wildcard | 0 | Zero. Checkable this run. |
| routify-sg exact host | 0 | Zero. Checkable. |
| routify-sg wildcard | 0 | Zero. Checkable. |
| routify vendor hosts, exact (3 hosts) | 0 each | Zero. Checkable. |
| `%.oss-cn-beijing.aliyuncs.com` | 84 | Vendor wildcard certificate only. All rows name the Alibaba region host, not one bucket. No per-bucket cert. Not a finding. |
| `%.aliyuncs.com` | 502 page | UNCHECKABLE. Server error, never zero. |
| `routify-%` family pattern | empty JSON | UNPROVEN, not zero. The response does not show whether the pattern was applied. Do not cite as zero. |

No fresh (90-day) certificate exists on any checkable named host.
No issuer or subject pattern exists, because the named-host sets
are empty.

## Zeros that are real (this lane, this window)

- urlscan, last 30 days: `routify-file-proxy` 0, `proxy_temp_file`
  0, `unshare` 0, `PROBE_PAYLOAD` 0. No namespace-escape shape and
  no probe-string shape appeared in urlscan at all.
- No download-then-execute shape (shape 5) was testable in urlscan
  search metadata, because methods and bodies are login-gated.
  Shape 5 is UNCHECKED here, not zero.
- No fd00:ec2 IPv6 metadata shape was searched on urlscan: the
  search API treats the string poorly, and no separate IPv6 search
  ran. Shape 1 IPv6 form is UNCHECKED here, not zero.

## Open questions for the coordinator

1. Who scans the sanmaohe `/upload/` path, and with what method?
   urlscan detail is login-gated. The GitHub or urlquery lane may
   hold the answer.
2. Is the 2026-10-22 metadata rig one researcher's SSRF test set?
   The shared path id suggests one rig. No attribution is made
   here: agents and infra only, no human identity work.
3. Why does plain `sanmaohe` urlscan search return 0 while the
   family search finds 4 sanmaohe rows? The plain-search zero
   must not be cited until this gap is understood.

## Evidence index

All raw files live under:

`data/lanes/agent-egress-broad-hunt/raw/urlscan-wayback-crtsh/`

- 15 urlscan search files, each with `.PROVENANCE.txt` (source URL,
  retrieval time, method) and `.sha256`.
- 19 urlscan result files. All 19 hold the same login warning
  bytes. They prove the detail gate; they hold no scan content.
- 8 Wayback files, plus 2 `.attempt1.json` Temporarily Offline
  pages, each with provenance and hash.
- 10 crt.sh files, each with provenance and hash.
- `SHA256SUMS` for the directory, and the fetch scripts
  (`run_urlscan.sh`, `run_wayback_crtsh.sh`, `fetch_results.sh`).
- This lane summary:
  `reports/agent-egress-broad-hunt/lanes/urlscan-wayback-crtsh.md`
