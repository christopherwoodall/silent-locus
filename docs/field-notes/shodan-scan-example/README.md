# Shodan Scan Example: Hunting Exposed AI-Harness Panels

Date: 2026-10-19
Purpose: Reference example for the Shodan query pattern used in agent-infrastructure hunting.

## Background

The NorForge investigation (https://norforge.com/blog/inside_cairn) found
publicly exposed AI-driven penetration-testing control panels (Cairn, Strix,
Hermes). These are web UIs left open by operators. Shodan indexes them.

## Queries

| Query | Count (2026-10-19) | Note |
|-------|-------------------|------|
| `http.title:"Cairn"` | 223 | Good precision |
| `http.title:"Strix"` | 152 | Good precision |
| `http.title:"Hermes"` | 8,651 | Too broad — Hermes is a common product name |
| `http.html:"Cairn"` | 324 | Broader than title, catches non-titled panels |

The `http.html` variant catches panels where "Cairn" appears in the page
body but not the `<title>` tag.

## Refining Hermes

`http.title:"Hermes"` returns 8,651 — mostly false positives. To narrow:

- Combine with harness-specific markers: `http.title:"Hermes" http.html:"agent"`
- Try product/banner strings from a known-good panel
- Filter by port: many harnesses run on non-standard ports

## API Pattern

The script (`shodan_scan_example.py`) uses two endpoints:

1. **`/shodan/host/count`** — get total matches for a query. Fast, cheap.
   Use this first to gauge result size before pulling details.

2. **`/shodan/host/{ip}`** — get full details for one IP: org, ASN, ports,
   hostnames, banners, last scan time. Use this to triage each candidate.

Note: `/shodan/host/search` (paginated full results) returns empty on the
current API plan. The count + host-detail pattern works around this.

## Auth

The script uses the stored `custom.shodan` credential via the surrogate
exchange in `dynamic_credentials`. Set `PYTHONPATH` before running:

```bash
export PYTHONPATH=/opt/muse/skills/custom-connector-setup/bin:$PYTHONPATH
python3 shodan_scan_example.py
```

Never paste API keys. The credential never appears in code or logs.

## Hunt Workflow

1. **Count** — run each query through `/count` to see the landscape
2. **Refine** — narrow broad queries (especially Hermes) with additional filters
3. **Pull** — for each candidate IP, get host details via `/host/{ip}`
4. **Triage** — check org/ASN/port/hostname for harness indicators
5. **Profile** — for open HTTP panels, passive GET only (see `cairn-fetch-panels.py`
   in `scripts/screening/`). Never POST, never log in, never start sessions.
6. **Clear** — counsel reviews each host: MALICIOUS / BENIGN / UNDETERMINED
7. **Mine** — only on MALICIOUS hosts: extract session logs, targets, intents

## Output

```
=== Shodan query counts ===
  cairn_title        223  (http.title:"Cairn")
  strix_title        152  (http.title:"Strix")
  hermes_title      8651  (http.title:"Hermes")
  cairn_html         324  (http.html:"Cairn")
```

## Files

- `shodan_scan_example.py` — runnable example script
- `README.md` — this writeup
