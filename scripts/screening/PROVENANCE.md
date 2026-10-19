# PROVENANCE — scripts/screening/

## Copied connector CLIs (2026-10-19)

The following files are copies of connector CLI tools. They are vendored
here so the screening directory is self-contained on clone. The canonical
source remains the connector directory. If the connector updates, re-copy.

| File | Source | Copied |
|------|--------|--------|
| `shodan.py` | `~/workspace/custom-connectors/custom.legacy-shodan/bin/shodan.py` | 2026-10-19 |
| `urlquery.py` | `~/workspace/custom-connectors/custom.legacy-urlquery/bin/uq.py` | 2026-10-19 |
| `urlquery-htmx.py` | `~/workspace/custom-connectors/custom.legacy-urlquery/bin/uq_htmx.py` | 2026-10-19 |
| `urlquery-htmx-curl.py` | `~/workspace/custom-connectors/custom.legacy-urlquery/bin/uq_htmx_curl.py` | 2026-10-19 |

Method: `cp` from the connector bin directories. No modifications.
Credential handling: these CLIs use the dynamic-credentials surrogate via
`PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin`. No secrets are
stored in these files.

## Symlinked in-repo scripts

All other `.py` files in this directory are symlinks to maintained scripts
elsewhere in this repo (scanners/, top-level scripts/). They resolve on
clone because their targets are in the same repository.
