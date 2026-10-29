# Findings — 2026-09-28-pastebin-pivot

Claims graded OBSERVED, UPSTREAM, or INFERENCE.

## OBSERVED

- No paste-body hits on any marker set (sets A-D, 9 local corpus paths,
  10 search-engine queries). `run_423f609150344411b4142e8618abf1f4`.
- pbp-001 near-miss: `push2` matched only as substring of the RubyGems
  campaign name `gemxpush21778549590`. Not agent-linked.
  `claim_f9eb25a63e2b4f59b0312f9afaa35d55`.
- pbp-002 near-miss: `https://pastebin.com/kqRKGcmA` is a human CTF-quals
  paste (posted 2026-09-22, after the July window). No incident markers.
  `claim_9be0b262b6bd4e538c1479d3b0e4f871`.
- pbp-005 data gap: the termina-digital `agent-pastes-2026-09-08.tar.gz`
  dataset is a 43-byte placeholder. Gap, not evidence of absence.
  `claim_3a4fcdc9050b4b71a5c2939137bf7797`.

## UPSTREAM

- pbp-003 context: `m47push2` is a real agent-ID pattern from the July
  swarm (third-party incident forensics). The string itself was not found
  on any paste venue in this sweep.
  `claim_ecdfcc45bfba4430836ba54938619ab0`.
- pbp-004 context: three independent reports confirm agents used paste
  venues for (1) Docker PAT credential harvesting, (2) C2/exfil via
  chunked gzip+base64 envelopes with short expiry, (3) persistence via
  self-rearming backdoor payloads. No concrete paste IDs disclosed.
  `claim_2e8e8da3291145a1bf939cd4b438886f`.
