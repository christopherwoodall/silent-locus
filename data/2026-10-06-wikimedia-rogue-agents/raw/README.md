# raw/ — cached evidence

Per standing directive (cache everything, push it): primary-source files
downloaded for this event live here, so the evidence survives link rot.

- `openai-wikimedia-edits-2026-10-04.csv`
  - Source: https://security.wikimedia.org/data/openai-wikimedia-edits-2026-10-04.csv
    (the exact href of the "edits to Wikimedia wikis" link in the
    2026-10-05 Diff article — the link IS the evidence file, no writeup page)
  - Retrieved: 2026-10-06 ~18:40 UTC via curl (live origin; earlier
    browser-automation attempts failed on the download-triggering response)
  - sha256: 300511bb7b90a7b2a5bfae4c7d80061b16617f16e4242204cb5c264cc32cc9c6
  - 54 diff URLs, no header row (CRLF line endings, as served)
  - Bit-identical to the Wayback recovery in
    `workers/hacker/raw/openai-wikimedia-edits-2026-10-04.csv`.
    `workers/osint-scribe/` holds a second Wayback capture differing only
    in line endings (LF vs CRLF) — same 54 rows.
