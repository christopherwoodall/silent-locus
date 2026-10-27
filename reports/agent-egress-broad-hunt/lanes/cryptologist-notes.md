# Cryptologist lane notes: hidden structure in agent-egress evidence

Grade: SECONDARY by default. No claim here is first-hand capture.
Style note: this file uses short sentences and simple words.
A term is defined the first time it is used.

## Terms

- Proxy-shaped URL: a URL that looks like it came from the routify file proxy.
- Signed URL: a URL with a time limit and a secret code in its query part.
- Query part: the part of a URL after the `?` mark. It holds named values.
- Metadata endpoint: a special address inside a cloud host. It gives data about the host.
- Exfiltration (exfil): data leaves a host to an outside party without a user order.
- Probe: a test action that sends a fixed harmless string, only to check reach.
- Lookalike: a URL that shares some features with the real shape but fails other tests.

## Sources used

- Prior hunt report: `reports/cohere-qwen-hunt/REPORT.md`.
- Prior hunt raw captures: `data/lanes/cohere-qwen-hunt/raw/` (read only, unchanged).
- Enrichment notes: `reports/cohere-qwen-enrichment/entity-to-behavior.md` and `ioc-list.md`.
- Detection pack text: `akasecurity/ai-tc#927` body, from the prior raw file
  `data/lanes/cohere-qwen-hunt/raw/github/q5_issues_unshare_aliyuncs.json`.
- Write-up text: `akasecurity/ai-tc#926`, fresh unauthenticated GET, 2026-10-27.
  The matching fresh GET for #927 hit the unauthenticated GitHub API rate limit
  on this run. No #927 text in this file comes from a fresh fetch.
- This lane's captures: `data/lanes/agent-egress-broad-hunt/raw/cryptologist/`
  (`aitc926.json`, `routify-path-shapes.json`, each with `.PROVENANCE.txt`,
  `.sha256`, and `SHA256SUMS`).
- Signed-URL rule kept: this file gives parameter NAMES and path shape only.
  It never copies a signed query string, a signature, or a token.

## 1. The routify proxy_temp_file grammar

A genuine proxy-shaped URL has this fixed shape, in order:

1. Scheme `https`.
2. Host `routify-file-proxy-sg.oss-ap-southeast-1.aliyuncs.com`.
   The host breaks down as bucket label `routify-file-proxy-sg`, then region
   `oss-ap-southeast-1` (Singapore), then `aliyuncs.com`.
3. Path segment `proxy_temp_file`.
4. Path segment `production`.
5. Path segment: a date, form `YYYY-MM-DD` (year, month, day).
6. Path segment: `trace_` plus 30 hex characters.
   Hex means digits `0-9` and letters `a-f` only.
7. Path segment: `requestId_` plus 32 hex characters.
8. Path segment: a final hex string, normally 32 characters.
9. Query part with exactly these three parameter NAMES, in this order:
   `Expires`, `OSSAccessKeyId`, `Signature`.

Evidence: 5 genuine URLs in the prior hunt raw file
`data/lanes/cohere-qwen-hunt/raw/github/q4_issues_routify-file-proxy.json`,
issue `hangtiancheng/yukino-code#2`, 2026-10-06.
All 5 share the same shape above. The date segment matches the issue date.
The shape-only extraction is stored in this lane's `routify-path-shapes.json`.

### New finding: trace IDs are structured, not pure random

The 2 distinct trace IDs in that issue share their first 16 hex characters
and their last 5 hex characters. Only the middle differs.
A pure random ID would not show that pattern twice.
This suggests the trace ID embeds a fixed part, such as a time block or a
session block, plus a random middle. This is INFERENCE, not proven.
Surface lanes should NOT treat a trace ID as a random token to match exactly.
They should match the shape (`trace_` plus 30 hex characters) and record
shared prefixes across IDs from one source.

### New finding: one final segment breaks the 32 rule

Four genuine final segments are 32 hex characters. One is 33 hex characters.
That outlier sits in an otherwise genuine URL, with the same trace ID,
request ID, date, and parameter names as its siblings.
Lesson: do NOT hard-require exactly 32 for the final segment.
Accept 32, and flag 33 as a near-match for human review, not as a failure.
A paste error or a variant length may explain it. The cause is unknown.

### Date rule, with a caution

Genuine dates sit in the past relative to the report, and near the report date.
The Crow case shows `2026-09-25` in the path for a `2026-09-24` issue.
A one-day gap is normal. Time zones can shift a date by one day.
A date far from the report date, or a future date, is a warning sign, not proof
of fakery on its own. A recalled URL can carry a plausible old date and still
be fake (see section 2).

## 2. Genuine proxy-shaped URL versus lookalike

Use all tests together. No single test decides.

| Test | Genuine | Lookalike or fake |
|---|---|---|
| Scheme | `https` | `http` (the blazux recall uses `http`) |
| Path | Full 6-segment shape from section 1 | Short, ellipsised, or missing segments |
| Trace and request IDs | Full hex, lengths in section 1 | `trace_…` / `requestId_…` with dots (ellipsised) |
| Query part | All 3 names: `Expires`, `OSSAccessKeyId`, `Signature` | Missing, or only 1 name |
| Fetch result | Fetches, or fails with 403 (refusal) | Fails with `SignatureDoesNotMatch` (bad code) |
| Traffic proof | Tool result or log shows a real fetch | Pcap (network record) shows no traffic to the proxy |

### The blazux fake: how it fails

Source: `blazux/qwen3.8-Flash-DGX#16` comments, in
`data/lanes/cohere-qwen-hunt/raw/github/c_blazux-16.json`.
The model recalled a proxy-shaped URL when asked what it fetched.
It fails 4 tests at once: scheme is `http`, the trace and request parts are
ellipsised (dots, not hex), no signing parameters are shown, and the comment
itself calls the signature fake and invalid. A later screenshot shows
`SignatureDoesNotMatch` when the recalled URL is fetched.
A pcap shows no traffic to the proxy. The real fetch went to the correct URL.
Rule: a recalled URL is NOT a fetched URL. A model can emit the shape from
memory (training artefact) with zero network traffic.
Surface lanes must record "recalled" and "fetched" as different facts.

### The Crow invented URLs: how they fail

Source: `nibor1896/Crow#288`, in the same q4 raw file.
The body shows the proxy path with ellipsised trace and request parts,
and no query part at all. The model invented the URLs. The harness fetched
them anyway and took error pages as frames.
Rule: an invented URL can still cause a fetch, but the URL itself is not a
proxy object. The finding is about the harness (no provenance guard), not
about the proxy. The fix shipped in Crow v2.6.0 (host must already appear in
user text, tool results, or the goal file).

### OSS lookalikes that are NOT proxy-shaped

These share only "OSS host plus opaque path plus query string". That is not
a proxy-shape match.

- Smaflowi cluster (urlquery detail `uq_report_a88644a1.json`):
  unsigned GET downloads of coin-icon PNG files from an OSS bucket, under
  `/waihui/` and `/javajys/` paths. No PUT, no POST, no probe, no signed
  parameters, no `proxy_temp_file` path. This is a rescanned web app, not
  an agent fetch. Do not rank it on host string alone.
- Redirect landing (urlscan scan 2026-10-27T02:32Z, submitted URL `50c5.cc`):
  page URL on an OSS host with path `/xg-d-vpu/rso/WVRq` and query names
  `d`, `e`, one random-looking name, and `ts`. No `proxy_temp_file` path,
  no `trace_` or `requestId_` segment, no OSS signing names.
  The fragment `WVRq` decodes from base64 to 3 non-meaningful bytes (`YTj`).
  It is not a payload. The `ts` value is a millisecond time stamp, not proof
  of agent action. The scan was cherry-picked from the newest 100 rows of a
  capped search. Grade: string presence only.
- Trustexc cluster (urlquery): unsigned GET image loads from an OSS bucket,
  with POSTs going to the site's own API host, not to OSS.
  Shared `/waihui/` paths show a shared front-end kit, not shared agent
  infrastructure.

### Other routify strings that are NOT the proxy

- `routify.alibaba-inc.com`, `routify-online.alibaba-inc.com`,
  `routify-pub.alibaba-inc.com`: first-party vendor ModelRouter hosts, from
  `QwenLM/qwen-code#10896`. Vendor traffic, disclosed and merged. Not covert.
  Not call-home by an honest definition. Held out of ranking.
- `proxy.routify.ai/v1`: a different product's proxy path. No OSS host,
  no `proxy_temp_file` path. Name overlap only.
- `roxiness/routify`: a code project name. Name overlap only.

## 3. OSS signed-URL parameter structure

### What the names prove

A genuine Alibaba OSS signed URL carries exactly these parameter NAMES:

- `Expires`: a time limit, as epoch seconds (seconds since 1970-01-01).
- `OSSAccessKeyId`: the key label that signed the URL.
- `Signature`: the secret code that proves the signature.

Presence of all 3 names, plus the section 1 path shape, plus `https`,
is the full fingerprint. Any one part alone is weak.

### What absence or a partial set proves

- No query part at all: NOT a signed URL. It may be a recalled shape, an
  invented shape, or a truncated quote. The Crow URLs and the blazux recall
  both sit here.
- Only `Expires` visible, rest truncated: signed-ness is UNVERIFIED.
  The enrichment notes show exactly this case: one README example URL shows
  `Expires` then truncation. The signature is INFERRED from the name only.
  Do not claim "signed" from one name.
- Only `Signature` as a word in a report: check context first. In the
  urlquery and urlscan haul, the word `Signature` in 2 detail reports was a
  TLS certificate field (TLS is the encryption layer of web traffic).
  It was NOT an OSS signed URL. No `OSSAccessKeyId` or `Signature` parameter
  appeared anywhere in that haul.
- Wrong parameter family: Azure blob URLs use `sv` and `se` names.
  S3 URLs use a different signing family. A URL with `sv`/`se` is not an
  OSS signed URL, even if it also uploads or downloads.

### What is fake or invalid

- A URL whose own reporter calls the signature fake and invalid: treat as
  fake. The blazux recall is the example. Do not upgrade it to "signed URL"
  because it looks proxy-shaped.
- A URL that returns `SignatureDoesNotMatch` when fetched: the code does not
  match the request. It is not a live signed object. It may be a recalled
  shape, a tampered shape, or an expired shape with a changed path.
- A URL with a far-future expiry value is still live-shaped, even if the
  object is gone. The prior report warns that the q4 raw file holds complete
  signed URLs with far-future expiry. This lane never copies those values.
  Surface lanes must also carry names and path shape only into derived notes.
- Case matters: `OSSAccessKeyId` and `Signature` use exact capital letters.
  Lower-case variants (`signature`, `ossaccesskeyid`) are NOT the OSS
  signing parameters. They may be another system's fields. Flag, do not match.

### Signed-URL rule for this hunt (restated)

Parameter NAMES and path shape only, in every derived note and record.
Raw files are never redacted. The rule governs derived notes, not raw files.

## 4. Metadata-endpoint variants: which cloud, and how they hide

### The four canonical forms (from pack #927)

| Form | Cloud | Note |
|---|---|---|
| `169.254.169.254` | AWS, GCP, Azure (all three use it) | Link-local address. "Link-local" means it only works inside the host's own network. It does NOT by itself prove which cloud. |
| `100.100.100.200` | Alibaba Cloud | Alibaba's metadata address. This one DOES point to Alibaba. |
| `fd00:ec2::254` | AWS | IPv6 form. IPv6 is the newer, longer address format. Full form: `fd00:0ec2:0000:0000:0000:0000:0000:0254`. |
| `metadata.google.internal` | GCP | A DNS name, not a number address. DNS maps names to numbers. GCP also answers on `169.254.169.254`. |

Common paths after the address: `/latest/meta-data/` (AWS style),
`/latest/dynamic/` and similar. A bare address with no metadata path is
weaker evidence than an address plus a metadata path.

### Encodings and aliases that hide the same address

Surface lanes must search these forms too. The current samples only show
literal forms (prior q6 sample: `169.254.169.254` in 28 of 30 items,
`fd00:ec2` in 3, `metadata.google.internal` in 2, zero encoded forms).
Absence of encoded forms in that sample is NOT proof that no one hides them.
All numeric forms below were computed locally from the address, not copied
from evidence.

For `169.254.169.254`:

- Decimal (one number): `2852039166`.
- Hex (one number): `0xA9FEA9FE`.
- Octal dotted (base-8 parts): `0251.0376.0251.0376`.
- Hex dotted: `0xa9.0xfe.0xa9.0xfe`.
- Mixed (first part hex, rest decimal): `0xa9.254.169.254`.
- IPv6-mapped: `::ffff:a9fe:a9fe`.
- URL-encoded dots: `169%2E254%2E169%2E254`.
- Double URL-encoded dots: `169%252E254%252E169%252E254`.
- Base64 of the string: `MTY5LjI1NC4xNjkuMjU0` (only if the address sits
  inside an encoded blob, not as a bare URL host).

For `100.100.100.200`:

- Decimal: `1684301000`.
- Hex: `0x646464C8`.
- Octal dotted: `0144.0144.0144.0310`.
- Hex dotted: `0x64.0x64.0x64.0xc8`.
- IPv6-mapped: `::ffff:6464:64c8`.

Other hiding forms for both:

- DNS aliases: `metadata.google.internal` (GCP), `metadata` (short name),
  `instance-data` (AWS docs alias in some setups), and any custom DNS name
  that resolves to the address. A DNS name that resolves to a metadata
  address IS a metadata reach, even if the string never appears.
- Trailing dot: `metadata.google.internal.` (same name, dot at the end).
  Naive string match on the name without the dot still hits, but exact-match
  tools may miss it. Search both.
- Case: DNS names ignore case. `METADATA.GOOGLE.INTERNAL` is the same name.
- IPv6 case and compression: `FD00:EC2::254`, `fd00:ec2:0:0:0:0:0:254`,
  and the full expanded form above are the same address. Normalize IPv6
  before matching.
- URL user-info trick: `http://169.254.169.254@evil.example/` does NOT go to
  the metadata address. The real host is after the `@`. The reverse,
  `http://evil.example@169.254.169.254/`, DOES go to the metadata address
  with a fake user name in front. Match the host after the last `@`, not the
  first string that looks like an address.
- Redirect and proxy hiding: a short link, a proxy service, or a `r.jina.ai`
  style reader prefix can carry a metadata address as its target.
  Match after one decode of the wrapper, not only the outer URL.
- Percent-encoded path: `%31%36%39%2E%32%35%34%2E%31%36%39%2E%32%35%34`
  decodes to the dotted address. Decode once, then match. Decode twice for
  double-encoded forms, then match again.

### What does NOT count

- `127.0.0.1`, `localhost`, and TEST-NET addresses like `192.0.2.10`
  (documentation range) are local or test shapes, not cloud metadata.
  The enrichment notes list them as separate local/test shapes.
  They may still matter as probe targets, but they are not metadata reaches.
- A metadata address inside a `grep` search, a doc, or a prompt is NOT a
  network reach. Pack #927 states this rule with negative fixtures:
  the address must sit in a network use (a URL in an executable field,
  a network client command, or an interpreter one-liner that requests it).
  Mere mention stays silent.

## 5. Encodings that hide the shapes

### URL-encoding and double-encoding

Observed in evidence: path segments use `%2F` for `/`, as in
`/implant%2Fupdate.sh` and `/anon%2F<uuid-like>` (enrichment notes).
A `%2F` inside a segment is still one segment until decoded.
Rule: decode percent-encoding once, then run the grammar tests.
Decode a second time, then run them again. A shape that only appears after
the second decode is a double-encoded hide. Record the decode depth.

### Base64 path fragments

Base64 is an encoding that turns bytes into letters, digits, `+`, `/`, and
`=` padding. It is common in opaque URL paths.
Rule: a base64-looking fragment is NOT a payload until decoded AND shown
meaningful. The `WVRq` fragment decodes to 3 non-meaningful bytes.
That is a null, not a payload. A fragment that decodes to a metadata
address, a host name, or a command string IS a finding. Always decode,
then judge the decoded bytes, not the encoded shape.

### Shell-variable indirection (known pack gap)

Pack #927 states this gap in its own notes: "an upload whose host is in a
shell variable isn't matched." Example shape: the host lives in `$HOST`,
`${BUCKET}`, or an environment value, and the command uses the variable.
Naive string match on the command line misses it completely.
Surface lanes must handle this:

- Record the variable assignment when it appears in the same command,
  script, or transcript (for example, `HOST=<value>` then `curl $HOST`).
- Resolve one step: replace the variable with its assigned value, then run
  the grammar tests. Do NOT resolve across files or across turns unless the
  assignment is in evidence.
- If the assignment is NOT in evidence, grade the hit as "host unresolved"
  and keep it. Do not drop it, and do not claim a host that is not shown.
- Related gap, also stated in #927: `curl -O` (file name taken from the URL)
  followed by a run is NOT linked to the download by the pack.
  Surface lanes should link download-then-execute across `-O` too.

### Other hiding forms to search

- Command substitution: `$(env)` or `$(printenv)` as an upload body
  (pack #927 flags this as an object-storage-file-upload shape).
  The body is the whole environment, which may hold secrets.
- Here-strings and pipes: `curl -d @-` reads the body from standard input.
  The body may come from a prior command in the same chain. Read the chain,
  not one command alone.
- Split strings: a host built by joining parts (`"169." + "254.169.254"`).
  Join string literals in one command before matching.
- Backslash and quote tricks: `169\.254\.169\.254` in a shell context,
  or a host split across quotes, still resolves to the same address.
  Normalize quotes and backslashes before matching.
- Case tricks in hosts: DNS ignores case, so `ROUTIFY-FILE-PROXY-SG...`
  in upper case is the same host. Lower-case before host matching.
  Path segments are case-sensitive: `proxy_temp_file` in upper case is NOT
  the same path. Keep path matching case-sensitive.

## 6. The sanmaohe probe versus a real exfiltration upload

### The probe shape (OBSERVED, main trace)

- Method: PUT. PUT is a web request that uploads data.
- Target host: `sanmaohe.oss-cn-beijing.aliyuncs.com`.
  Bucket label `sanmaohe`, region segment `cn-beijing` (INFERENCE from host).
- Path: `/upload/test.bin`. No query part. No signing parameters.
- Scheme: plain `http`, not `https`.
- Body: a fixed synthetic string (a made-up test string, not file content,
  not system data, not credentials). The body is the same on every run.
- Command shape: `curl -s -m 10 -o /tmp/put_probe -X PUT --data-binary <payload>
  -w HTTP:%{http_code}`. It saves the response to `/tmp/put_probe` and
  reports the HTTP code. The `-o` flag here saves the PUT response.
  It is NOT a fetch. Do not confuse it with the fetch chain in section 7.
- What leaves the host: only the probe string, the request line and path,
  and network metadata (source IP, time — INFERENCE, not in trace text).
- No GET in the main trace. No second network call. No follow-up use of
  the uploaded object.

### What a REAL exfiltration upload looks like (contrast)

A real exfil differs on method, body, path, and chain. Any 2 of these
together raise the grade. One alone is weak.

| Marker | Probe | Real exfil |
|---|---|---|
| Body | Fixed synthetic string | File content, env dump, archive, or secret |
| Upload flags | `--data-binary` with a literal string | `-T`, `--upload-file`, `-d @file`, `-F`, `--post-file`, `-d @-` with piped content |
| Path | `/upload/test.bin`, generic test name | Host name, date, user name, or stolen-file name; `.tar.gz`, `.zip`, `.env`, `passwd` style names |
| Query | None | Signing parameters, or an auth token, or a session label |
| Scheme | Plain `http` | `https` to a non-vendor host, or `http` to a listener the agent controls |
| Chain | Single PUT, then report the code | Recon first (list files, read env, check tools), then upload, then delete or hide the local copy |
| Follow-up | None | Second call to confirm, list, or fetch back the object |
| Destination | One named bucket, test path | A bucket, paste host, or listener never named in the task |

### Distinguishing tests for surface lanes

1. Body test: is the body a fixed string, or does it read a file or env?
   File or env body = exfil shape. Fixed string = probe shape.
2. Path test: does the path contain `test`, `probe`, `put_probe`, or
   `test.bin`? Test names point to probe. Host-named or file-named paths
   point to exfil.
3. Chain test: does recon appear in the same command or turn (list files,
   read env, check tools) before the upload? Recon plus upload = the
   recon-then-egress shape (pack #927, `command-risk` warn).
   Probe alone has no recon chain.
4. Method test: PUT alone is neutral. PUT with a file flag, or POST with
   a multipart file part, is an upload shape. GET to the same host is a
   fetch, not an upload. Direction matters: do not merge fetch and upload.
5. Response test: saving the response to `/tmp/put_probe` and printing the
   HTTP code is probe reporting. Saving an upload receipt and then
   deleting the source file is exfil cleanup.

## 7. The fetch chain that is NOT the probe (do not merge)

The enrichment notes show a separate fetch-and-inspect chain in the README
examples. It is NOT the main-trace PUT.

- Shape: fetch a URL, save it with `-o` to `/tmp/put_probe`, echo the exit
  status, list the file, then read the file. Variants suppress errors
  (`2>/dev/null`) or inspect with `file`, `head -c`, or `xxd`.
- Prefill trigger: at the `-o` (save-to-disk) flag, URL generation jumps
  from 4 percent to 92 percent, and watchlist hits from 0.5 percent to
  23 percent, led by the routify host (blog aggregates, UPSTREAM).
- Lesson: `-o` is a trigger for URL generation, not proof of upload.
  A fetch chain that ends in `cat` is inspection, not exfiltration.
  Grade fetch and upload separately, even when both use `/tmp/put_probe`.

## 8. Hidden-form variants surface lanes should also search

Search list, in priority order:

1. Routify grammar with one segment changed: `proxy_temp_file` plus a
   different second segment (not `production`), or a date in another form
   (`20260729`, `2026/07/29`). Record, do not auto-match.
2. Routify host with a different region: `routify-file-proxy-*.aliyuncs.com`
   for any region segment, not only `oss-ap-southeast-1`.
3. Routify path on a NON-routify bucket: `proxy_temp_file/production/...`
   on any `*.aliyuncs.com` host. The path grammar may travel without the host.
4. Trace/request shape without the proxy path: `trace_<30 hex>` plus
   `requestId_<32 hex>` in any URL, log line, or transcript.
5. Metadata addresses in every encoding from section 4, plus DNS aliases,
   plus the host-after-`@` rule.
6. Upload flags (`-T`, `--upload-file`, `-d @file`, `-F`, `--post-file`,
   `-d @-`, `--data-binary @file`) aimed at any object-storage host
   (S3, GCS, Azure Blob, R2, Alibaba OSS), not only sanmaohe.
7. Shell-variable hosts: resolve one step from an assignment in evidence,
   else grade "host unresolved" and keep the hit.
8. `curl -O` plus a later run of the downloaded file (the pack's stated gap).
9. Recon-then-egress in one command: recon terms (`cat /etc/resolv.conf`,
   `which curl`, `ls /tmp`, `uname -a`, `id`, `hostname`) plus a network
   call. Recon alone stays silent, per the pack.
10. Download-then-execute: `curl -o` or `wget -O` to a path, then running
    that path (`sh`, `bash`, `source`, `chmod +x`, `python`, `perl`,
    `node`, or a direct run).
11. `unshare` user-namespace shapes: `-U`, `-r`, `-c`, `-Urm` clusters,
    `--user`, `--map-*-user`. Mount-only (`-m`) and net-only (`--net`)
    are NOT flagged. Do not count them.
12. Double-decoded URLs: decode twice, then re-run tests 1 to 11.
13. Base64 fragments: decode, then judge the decoded bytes.

## 9. Open questions

1. What builds the trace ID? The shared 16-plus-5 pattern (section 1)
   suggests a structured ID. The builder is unknown. A larger sample of
   trace IDs from one source could confirm the fixed parts.
2. Is the 33-character final segment a paste error or a real variant?
   One sample cannot decide. More genuine URLs would settle it.
3. Does any surface show an ENCODED metadata address in a real agent
   command, or only literal forms? The q6 sample shows literals only.
   The encoded search (section 4) is still unrun on most surfaces.
4. Does any agent command resolve a metadata address through a shell
   variable or a DNS alias in evidence? The pack gap is stated, but no
   in-evidence example was found in this lane's sources.
5. Is there a real exfil upload (file or env body) to any OSS host in the
   broad surfaces, or only probes and fetches? Nothing in this lane's
   sources shows one. That is the broad hunt's main open question.

## 10. What this lane did NOT find (honest nulls)

- No new hidden-structure family beyond the shapes above.
- No encoded metadata address in any agent command in the sources read.
- No shell-variable host resolution in evidence in the sources read.
- No real exfil upload body in the sources read. Only the probe shape.
- No new routify host, region, or path variant beyond the stated grammar.
- The fresh #927 GET was rate-limited. #927 text here comes from prior raw
  capture, not a fresh fetch. That limit does not change the pack rules,
  which are quoted from the captured body.
