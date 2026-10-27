# Manifest: RubyGems July spike CSV review

Third-party dashboard export reviewed: operator-supplied CSV, 533 rows,
preserved at
`data/lanes/rubygems-goimport-campaign/raw/rubygems-july-2026-spike-operator-20261027.csv`
(sha256 `765ee2f24e6ec1a191c66faee030aaea8586cc4a0cdde1bee4c0668a0f0f3ce0`).
The CSV itself is UPSTREAM. This review stages findings only: no Factum
writes, no Transluce submissions, no Shodan, no account creation, no
logins, no POSTs. No push made; the parent pushes.

- ./REPORT.md — full review
- ./findings.json — 23 graded findings (F01–F23)
- ./adversarial-review.md — coordinator attack pass on the synthesis
- ./verifier-report.md — verifier lane report (written by the verifier lane)
- ./working/stats/ — schema census, script, tables
- ./working/linguist/ — naming grammar, summary census, reason classes
- ./working/cryptologist/ — payload inventory, scripts, tallies
- ./working/corroboration/ — overlap matrix, NEW-names lists, Factum sample, live-fetch script
- ./working/adversarial/ — lane adversarial review, likely-rows audit, prompt-v2 table, scripts
- ../data/lanes/rubygems-july-spike-review/raw/corroboration/ — live fetch captures, each with .PROVENANCE.txt + .sha256

SHA256SUMS in this directory covers the top-level deliverables; lane
working files carry their own hashes where the lane produced them.
