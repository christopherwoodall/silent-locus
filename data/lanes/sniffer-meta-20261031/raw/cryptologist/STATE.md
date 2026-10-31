# Cryptologist lane — state

Task: sniffer-sweep meta fleet, cryptologist lane. Operator:
BigSexyWarlock69. Work date: 2026-10-31.

## What was done

1. da.gd decode from saved rows only. All 30 saved rows in
   `uq-odd-dagd-domain.json` were read. All 13 base64 rows were
   decoded. Method: percent-unquote the `final_path` segment,
   then standard base64 decode. Decoded output was described by
   shape only (tag sequence, byte length, START presence and
   offset). No decoded payload text, locator, or script target
   was copied into any output file.
2. GH7 file `q06-i-am-ai-agent.json`: all 10 items classified
   by marker test (checkbox template, bare disclosure, fill-in
   template, delegation grammar, commit-hash shape, wallet-field
   shape, numbered-agent shape). Bodies were read in redacted
   form during analysis. Output files carry shapes only.
3. GH6 file `q05-collab-spawn.json`: all 10 items tested for
   dotted, flat, envelope, and concatenated spawn forms, plus
   wild-instance markers (all absent).
4. zz mystery: full scan of all 30 saved rows in
   `uq-odd-zz-param-agent-conj.json`, plus control scans of the
   zz-only and oai-tag files. Flagged row found at saved row 26.
5. Village beacon: issue, comments JSON, and comments text
   file all read. Record-level scan of all other staged sweep
   evidence files for the same post-then-fetch-back shape.
   Three loose HN matches and one Reddit match were checked
   and rejected as false friends, with reasons in FINDINGS.md.

## What was NOT done

- No new endpoint fetch, no POST, no login, no session.
- No commit and no push. The coordinator owns commit and push.
- No Factum write. Note on house rules: the repository guide
  defaults new structured evidence to Factum, but this task
  brief states stage only, no Factum writes, no commit. This
  lane followed the brief, as the earlier cryptologist review
  did. Any Factum ingest is the coordinator's call.
- No ANEC-01 material was touched.
- No Shodan, no package repos, no Docker Hub.
- No fetched capture exists, so no `.PROVENANCE.txt` or
  `.sha256` sidecar was created for this lane. Sources used are
  the sweep's own staged files, which carry their own provenance
  and hash sidecars in the sweep lane.

## Corrections to the earlier review

- Title truncation does not block decode. The `final_path`
  copy decodes fully for all three segments. The earlier
  "full decode fails" claim is corrected in FINDINGS.md.
- The zz flagged row is not missing. It is saved row 26. It
  is, however, unverifiable from saved bytes, because no saved
  field contains the flagged string.
- The GH7 wallet-shape item is item 9 (registration form),
  not item 6. Item 6's long tokens are commit hashes.
- The Codex grammar has a fourth form: concatenated
  (namespace and tool joined with no separator), in items 6
  and 9 of the GH6 file.

## Open questions (for the parent, not this lane)

- Live re-check of da.gd echo pages: not needed for decode.
- Full-URL lookup for the zz flagged row (row 26).
- Reading of the Village verification-evidence locator.
- No staged evidence shows an agent ticking the GH7 checkbox
  templates (items 0 and 4).

## Files written by this lane

- `data/lanes/sniffer-meta-20261031/raw/cryptologist/FINDINGS.md`
- `data/lanes/sniffer-meta-20261031/raw/cryptologist/STATE.md`
