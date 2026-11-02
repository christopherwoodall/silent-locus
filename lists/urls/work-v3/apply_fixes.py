"""FIX lane: apply LANG-COUNSEL-v3 (52) + ADVERSARIAL-v3 (D1-D8) + parent
judgment-call overrides to work-v3/final-v3-working.xlsx.

Reads:  final-v3-working.xlsx (working copy only)
Writes: final-v3-working.xlsx
Never touches: INTERNAL sheet, committed v3 file, evidence judgments.

Run: python3 apply_fixes.py
"""
import openpyxl, re, sys

PATH = "/home/hatch/workspace/silent-locus/lists/urls/work-v3/final-v3-working.xlsx"
wb = openpyxl.load_workbook(PATH)
poi = wb["Agent POIs"]
intel = wb["Intelligence and reporting URLs"]
notes = wb["Notes"]

PER_STAMP = "(per trajectory-domains.md, 2026-10-19)"
LEGACY_STAMP = "(legacy internal tally, pre-2026-10-19; re-tally pending)"

log = []
def sub(ws, r, c, old, new, tag):
    """Replace old->new in one cell; assert old present exactly once."""
    cell = ws.cell(r, c)
    v = cell.value or ""
    n = v.count(old)
    if n == 0:
        log.append(f"MISS [{tag}] {ws.title}!{cell.coordinate}: old text not found")
        return False
    if n > 1:
        log.append(f"MULTI [{tag}] {ws.title}!{cell.coordinate}: old text found {n}x, replacing all")
    cell.value = v.replace(old, new)
    log.append(f"OK   [{tag}] {ws.title}!{cell.coordinate}")
    return True

# ---------- D1: row 4 col F whole-cell replace ----------
c = poi.cell(4, 6)
log.append(f"D1 before: {c.value!r}")
c.value = "Submit URL \u2192 rendered scan and report | internal scan/state data paths"
log.append("OK   [D1] Agent POIs!F4")

# ---------- D3: row 14 col K add wiki.cgi URL (curl-verified HTTP 200) ----------
sub(poi, 14, 11,
    "https://wikiservice.at/dse",
    "https://wikiservice.at/dse; https://wikiservice.at/dse/wiki.cgi",
    "D3")

# ---------- D4: row 34 col R judgment-call disclosure (parent wording) ----------
sub(poi, 34, 18,
    "Role AGENT_COLONY is a judgment call (swarm treated as a collective \u2014 see Notes row 218)",
    "AGENT_COLONY is a judgment call: 'swarm' treated as a collective; see Notes.",
    "D4")

# ---------- Fix 5 (judgment call): row 94 -> ARTIFACT_REGISTRY ----------
sub(poi, 94, 9, "UNCONFIRMED", "ARTIFACT_REGISTRY", "fix5-role")
sub(poi, 94, 18,
    "Role UNCONFIRMED: no specific endpoint established (was TEMP_FILE_HOST)",
    "Role ARTIFACT_REGISTRY (was TEMP_FILE_HOST; no specific endpoint established)",
    "fix5-flag")
sub(notes, 218, 2,
    "Possible persistent storage/transfer channel \u2192 TEMP_FILE_HOST (could equally sit in ARTIFACT_REGISTRY).",
    "Possible persistent storage/transfer channel \u2192 ARTIFACT_REGISTRY (was TEMP_FILE_HOST; no specific endpoint established).",
    "fix5-notes218")

# ---------- Fix 16 override: keep 'surfacewatch', revert 'endpoint monitoring' ----------
for r in range(27, 34):
    for cc in (10, 12):  # J, L
        v = poi.cell(r, cc).value or ""
        if "endpoint monitoring" in v:
            sub(poi, r, cc, "endpoint monitoring", "surfacewatch", "fix16-surfacewatch")
# glossary entry (judgment call)
sub(notes, 117, 1,
    "Proper-name labels retained as-is: AIHW (case label in Transluce findings), 1F916 (service name).",
    "Proper-name labels retained as-is: AIHW (case label in Transluce findings), 1F916 (service name). "
    "surfacewatch = the internal endpoint-change monitoring method (used in Agent POIs rows 27\u201333 Sources/Seen).",
    "fix16-glossary")

# ---------- D2: per-stamp rows 27/28/29/30/33/36/37 counts (J and L) ----------
per_rows = {27: "25", 28: "24", 29: "36", 30: "37", 33: "17", 36: "20", 37: "16"}
for r, n in per_rows.items():
    sub(poi, r, 10, f"{n} Internal corpus hits |",
        f"{n} Internal corpus hits {PER_STAMP} |", f"D2-per-J{r}")
    sub(poi, r, 12, f"{n} Internal corpus hits;",
        f"{n} Internal corpus hits {PER_STAMP};", f"D2-per-L{r}")

# ---------- D2/D7: legacy stamp on every other unstamped count ----------
def legacy(ws, r, c, old, new, tag):
    return sub(ws, r, c, old, new, tag)

L = LEGACY_STAMP
legacy(poi, 5, 12, "13 Internal corpus hits;", f"13 Internal corpus hits {L};", "D7")
legacy(poi, 6, 10, "6 Internal corpus hits |", f"6 Internal corpus hits {L} |", "D7")
legacy(poi, 6, 12, "Internal corpus (6 hits). Malware sandbox",
       f"6 Internal corpus hits {L}. Malware sandbox", "D7+D8")
legacy(poi, 8, 12, "(3 Internal corpus hits)",
       f"(3 Internal corpus hits {L})", "D7")
legacy(poi, 15, 12, "2 Internal corpus hits.",
       f"2 Internal corpus hits {L}.", "D7")
legacy(poi, 26, 12, "15 Internal corpus hits.",
       f"15 Internal corpus hits {L}.", "D7")
legacy(poi, 38, 10, "813 Internal corpus hits |", f"813 Internal corpus hits {L} |", "D7")
legacy(poi, 38, 12, "813 Internal corpus hits;", f"813 Internal corpus hits {L};", "D7")
legacy(poi, 39, 10, "19 Internal corpus hits |", f"19 Internal corpus hits {L} |", "D7")
for r, n in [(40, "18"), (41, "16"), (42, "10"), (44, "6"), (45, "6"),
             (46, "5"), (48, "5"), (49, "4"), (50, "4"), (51, "3"),
             (52, "3"), (53, "3"), (54, "3"), (55, "3"), (56, "3")]:
    legacy(poi, r, 10, f"{n} Internal corpus hits |", f"{n} Internal corpus hits {L} |", "D7")
legacy(poi, 43, 10, "7 Internal corpus hits (Transluce #179) |",
       f"7 Internal corpus hits (Transluce #179; {L[1:]} |", "D7")
legacy(poi, 47, 10, "5 Internal corpus hits (Transluce #166/#167/#179) |",
       f"5 Internal corpus hits (Transluce #166/#167/#179; {L[1:]} |", "D7")
legacy(poi, 59, 12, "(489 Internal corpus hits)",
       f"(489 Internal corpus hits {L})", "D7")
legacy(poi, 60, 12, "(596 Internal corpus hits)",
       f"(596 Internal corpus hits {L})", "D7")
# D8 ', Internal corpus hits' variants + legacy stamp
legacy(poi, 65, 10, "4, Internal corpus hits paste collection |",
       f"4 Internal corpus hits {L}, paste collection |", "D8+D7")
legacy(poi, 69, 10, "25 Internal corpus hits |", f"25 Internal corpus hits {L} |", "D7")
legacy(poi, 70, 10, "10 Internal corpus hits |", f"10 Internal corpus hits {L} |", "D7")
legacy(poi, 71, 10, "6, Internal corpus hits paste collection |",
       f"6 Internal corpus hits {L}, paste collection |", "D8+D7")
legacy(poi, 72, 10, "5, Internal corpus hits paste collection |",
       f"5 Internal corpus hits {L}, paste collection |", "D8+D7")
legacy(poi, 73, 10, "4, Internal corpus hits paste collection |",
       f"4 Internal corpus hits {L}, paste collection |", "D8+D7")
legacy(poi, 74, 10, "4, Internal corpus hits paste collection |",
       f"4 Internal corpus hits {L}, paste collection |", "D8+D7")
legacy(poi, 75, 10, "3 Internal corpus hits each |",
       f"3 Internal corpus hits each {L} |", "D7")
legacy(poi, 76, 10, "3 Internal corpus hits each |",
       f"3 Internal corpus hits each {L} |", "D7")
for r in (84, 85, 86, 87, 88, 89, 90):
    legacy(poi, r, 10, "3 Internal corpus hits |", f"3 Internal corpus hits {L} |", "D7")
# Intel counts
legacy(intel, 11, 6, "3 Internal corpus hits |", f"3 Internal corpus hits {L} |", "D7-intel")
legacy(intel, 15, 6, "(237 Internal corpus hits)",
       f"(237 Internal corpus hits {L})", "D7-intel")

# ---------- GitHub nit (adversarial S3): row 60 col K, curl-verified HTTP 200 ----------
sub(poi, 60, 11,
    "https://github.com; https://d3ncjnql1bmhe8.cloudfront.net/findings/137",
    "https://github.com; https://github.com/youdotcom-oss/minimax-m3-deepsearchqa-skill-eval; https://d3ncjnql1bmhe8.cloudfront.net/findings/137",
    "S3-github")

# ---------- fix 12 global pattern leftovers (visible sheets only) ----------
old12 = "link dead 2026-10-23 (HTTP 000 \u2014 empty reply from server)"
new12 = "Link dead 2026-10-23 (HTTP 000 \u2014 no response from server)"
sub(poi, 78, 18, old12, new12, "fix12")
for r in (23, 24, 25, 26):
    sub(intel, r, 7, old12, new12, "fix12-intel")

# ---------- fix 27 pattern on row 14 col J ----------
sub(poi, 14, 10,
    "(suffix moved from Priority column 2026-10-23)",
    "(moved from the Priority column 2026-10-23)",
    "fix27-r14")

# ---------- LEAD-3 leftover in row 14 Review flag ----------
sub(poi, 14, 18,
    "LEAD-3 live capture: wikiservice.at/dse",
    "live capture: wikiservice.at/dse",
    "LEAD-3")

# ---------- leftover 'wired' in row 38 Seen (not a quoted original) ----------
sub(poi, 38, 12,
    "wired to slot-0 baseline 2026-10-22",
    "configured to slot-0 baseline 2026-10-22",
    "wired-38")

# ---------- Notes B113: header typo now fixed, update the note ----------
sub(notes, 113, 2,
    "(URL / Calssification / Use / Direct source links / Attribution - sheet's own header spelling kept)",
    "(URL / Classification / Use / Direct source links / Attribution \u2014 header typo corrected 2026-10-23)",
    "fix36-note")

# ---------- Notes A104: v2 changelog BUILD lane ----------
sub(notes, 104, 1,
    "v2 changelog (2026-10-23) - BUILD lane",
    "v2 changelog (2026-10-23) \u2014 build record",
    "BUILD-lane")

# ---------- D2 changelog line on Notes B126 ----------
sub(notes, 126, 2,
    'Full per-cell lineage of every removed value is on the sheet "INTERNAL \u2014 do not distribute".',
    'Full per-cell lineage of every removed value is on the sheet "INTERNAL \u2014 do not distribute". '
    "Count provenance: rows stamped '(per trajectory-domains.md, 2026-10-19)' were reconciled to that source; "
    "remaining counts are legacy internal tallies awaiting a corpus-wide re-tally.",
    "D2-changelog")

# ---------- fix 51: Template stays hidden ----------
wb["Template"].sheet_state = "hidden"
log.append("OK   [fix51] Template sheet hidden")

wb.save(PATH)
print("\n".join(log))
misses = [l for l in log if l.startswith("MISS")]
print(f"\n{len([l for l in log if l.startswith('OK')])} applied, {len(misses)} misses")
