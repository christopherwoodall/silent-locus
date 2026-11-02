# DarkSwarm capture — STATUS

Lane: darkswarm-20261101
Source repo: https://github.com/SauersML/DarkSwarm
Branch: main
Cloned HEAD SHA: be21462916e9f94ee7ff2ad48eb6c82b92d1617e
HEAD commit date: 2026-11-01 07:36:15 -0800
HEAD subject: Figures: Toro's private Tor line, lynxshell's tool call spilling into IRC
Retrieval time (UTC): 2026-11-02T05:20:33Z
Method: git clone --depth 1 (read-only, no login, no POST, no credentials) + copy
Scratch clone: ~/workspace/scratch/darkswarm-20261101-src (outside the silent-locus repo)

## Captured files

- README.md: 1 (16,325 bytes)
- Images: 50, all PNG, all under images/ with repo relative paths preserved
- Total captured files: 51
- Total bytes captured: 16,630,399 (~15.9 MiB)
- Matches the expected count (1 README + 50 images). No forcing was needed.

## Sidecars

- .PROVENANCE.txt sidecars: 51 (one per captured file)
- .sha256 sidecars: 51 (one per captured file)
- Provenance sidecar content per file: source URL
  https://github.com/SauersML/DarkSwarm/blob/main/<relative-path>,
  branch main, HEAD SHA above, retrieval time UTC, method
  "git clone --depth 1 + copy".

## Verification

- sha256sum -c over all 51 sidecars: PASS, 51 OK, 0 failures.
- Copies confirmed byte-identical to the cloned source (diff of README.md
  and images/ shows no content differences; only the sidecars are extra).
- Source inventory check: the cloned tree holds exactly 1 .md file and
  50 .png files besides .git, so nothing was missed.

## Missing / unexpected files

- Missing: none.
- Unexpected: none. All 50 images are PNG; no other file types exist in
  the repo tree at this HEAD.

## Constraints honored

- No git add, commit, or push inside ~/workspace/silent-locus.
- The pre-existing staged set was not touched (read-only status check only).
- data/records/ and data/.local/factum.db were not touched.
- No branch switch; work stayed on main as checked out.
- No redaction, no deletion. Images captured as bytes only; no chart
  contents claimed beyond README text (chart reading is another lane).
- No human-operator research: capture only, from the public repo.
