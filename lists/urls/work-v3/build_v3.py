#!/usr/bin/env python3
"""Build monitorable-surfaces-ENRICHED-v3.xlsx from v2.

Applies (2026-10-23, BUILD lane):
 1. Remove 120 self-referential silent-locus GitHub URL instances from Direct Links
    cells (Agent POIs col K, Intelligence col E); keep verified direct surface URLs.
 2. Strip internal data/lanes/... paths from Direct Links cells.
 3. Strip Factum batch ID d6982046 from the 14 visible cells (no replacement).
 4. Factum scrub on visible sheets: 'Factum observations' -> 'Internal corpus hits',
    counts kept as 'N Internal corpus hits', 'not in Factum/lanes/hunt data' ->
    'not previously catalogued', lane-name citations removed, 'github <path>' review
    tails removed.
 5. Row 14 canonical name -> DSEWiki (prowiki.org -> wikiservice.at/dse).
 6. Role column -> 12-term controlled set (counsel-C proposal), detail migrated to Seen.
 7. Rows 31/32/34/35 counts reconciled to trajectory-domains.md (2026-10-19): 103/16/114/53.
 8. Sheet 'INTERNAL — do not distribute' (red tab): original-value lineage for every
    scrubbed cell.
 9. Notes: v3 changelog, open-item resolutions, 12-term set + full mapping.

Source workbook (v2) is opened read-only for lineage; all edits go to the v3 copy.
"""
import re, sys, time
import openpyxl
from openpyxl.utils import column_index_from_string

BASE = '/home/hatch/workspace/silent-locus/lists/urls/'
V2 = BASE + 'monitorable-surfaces-ENRICHED-v2.xlsx'
V3 = BASE + 'monitorable-surfaces-ENRICHED-v3.xlsx'

POI = 'Agent POIs'
INTEL = 'Intelligence and reporting URLs'

# POI columns (data starts at col B)
C = {n: column_index_from_string(n) for n in
     'B C D E F G H I J K L M N O P Q R'.split()}
# col letters: B=URL C=Type D=Cap E=Class F=Ops G=ROE H=Prio I=Role J=Sources
#              K=Direct L=Seen M=MITRE N=Attr O=R P=O Q=E R=Reviewflag
IC = {n: column_index_from_string(n) for n in 'B C D E F G'.split()}
# Intel: B=URL C=Class D=Use E=DirectSource F=Attr G=Reviewflag

SELFREF = 'https://github.com/christopherwoodall/silent-locus'
changes = []  # (sheet, row, col_letter, kind, old, new)

def cell(ws, r, col_letter):
    return ws.cell(r, column_index_from_string(col_letter))

def setv(ws, sheet, r, col_letter, new, kind):
    c = cell(ws, r, col_letter)
    old = c.value
    if old == new:
        return False
    changes.append((sheet, r, col_letter, kind, old, new))
    c.value = new
    return True

# ---------------------------------------------------------------- scrub text
def scrub_text(s):
    """Neutralize self-referential wording. Keeps counts and meaning."""
    t = s
    # Factum batch id (strip, no replacement)
    t = t.replace('; Factum batch d6982046 (PRIMARY)', '')
    t = t.replace('(slot-0; Factum batch d6982046)', '(slot-0)')
    t = t.replace('Factum batch d6982046', '')
    # observations
    t = t.replace('-> Factum observations', '-> Internal corpus hits')
    t = t.replace('| Factum observations', '| Internal corpus hits')
    t = t.replace('Factum observations', 'Internal corpus hits')
    # counts: both orders
    t = re.sub(r'Factum (\d[\d,]*) records', r'Internal corpus hits \1', t)
    t = re.sub(r'(\d[\d,]*) Factum records', r'\1 Internal corpus hits', t)
    t = re.sub(r'Factum lane (\S+) \((\d[\d,]*) records\)', r'Internal corpus (\2 hits)', t)
    t = t.replace('Factum domain audit', 'Domain audit')
    # unattributed marker
    t = t.replace('not in Factum/lanes/hunt data', 'not previously catalogued')
    # any remaining bare "Factum" (e.g. "no Factum hits")
    t = re.sub(r'\bFactum\b', 'Internal corpus', t)
    # lane-name citations: ", lane X" / ", lanes X, Y" (specific lane IDs)
    t = re.sub(r',\s*lanes?\s+[A-Za-z0-9][A-Za-z0-9\-_]*(?:\s*,\s*[A-Za-z0-9][A-Za-z0-9\-_]*)*', '', t)
    t = re.sub(r'\s+in lane\s+[A-Za-z0-9][A-Za-z0-9\-_]*', '', t)
    # internal repo-relative paths
    t = t.replace('reports/, ', '')
    t = re.sub(r';\s*data/lanes/[A-Za-z0-9_\-./]+', '', t)
    t = re.sub(r'\s*->\s*data/lanes/[A-Za-z0-9_\-./]+\s*', ' ', t)
    t = re.sub(r'data/lanes/[A-Za-z0-9_\-./]+', '', t)
    # review-flag tails naming our repo paths
    t = re.sub(r':\s*github (docs|scripts)/[^\s;)]*', '', t)
    # stray double separators / spaces
    t = re.sub(r';\s*;', ';', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    t = re.sub(r'\s+\|\s*$', '', t)
    t = t.strip()
    t = re.sub(r'^;\s*', '', t)
    t = re.sub(r'\s*;\s*$', '', t)
    return t

def clean_links(s):
    """Split ';'-separated links, drop self-referential GitHub + data/lanes parts."""
    parts = [p.strip() for p in s.split(';')]
    kept = [p for p in parts
            if p and not p.startswith(SELFREF) and not p.startswith('data/lanes/')]
    return '; '.join(kept)

# ------------------------------------------------------- Role controlled set
ROLE_DEFS = [
    ('AGENT_BOARD', 'Agent-facing boards, forums, guestbooks, message directories, imageboards, bounty/offer boards, and reporting boards'),
    ('AGENT_COLONY', 'Colony-style agent collectives and governed agent communities'),
    ('COORDINATION_LOG', 'Public agent log/message archives, conversation mirrors, and forum mirrors'),
    ('PUBLIC_WIKI', 'Wikis and shared-state pages used for public messaging or coordination'),
    ('SCAN_EVIDENCE_SERVICE', 'Scan/report services used as evidence sources for retrieval attempts and probes'),
    ('MALWARE_SANDBOX', 'Dynamic malware-analysis sandboxes with public or API access'),
    ('RETRIEVAL_PROXY', 'Fetch/transform/browser proxies, request-echo and webhook-inspection services, HTTP diagnostic utilities'),
    ('ARTIFACT_REGISTRY', 'Package registries, code/model hubs, build/documentation services, artifact and object stores'),
    ('IDENTITY_SERVICE', 'Temporary/disposable email and identity providers'),
    ('TEMP_FILE_HOST', 'Temporary file hosts, paste hosts, and dead-drop text venues'),
    ('URL_SHORTENER', 'URL shorteners and redirect services'),
    ('UNCONFIRMED', 'Named in reporting but role not established in reviewed evidence; or no specific service identified'),
]

# (pattern, term, exact?) — exact=True means full-string equality
ROLE_PATTERNS = [
    ('Public evidence source for retrieval attempts', 'SCAN_EVIDENCE_SERVICE', False),
    ('Scan corpus', 'SCAN_EVIDENCE_SERVICE', True),
    ('Malware sandbox w/ public API', 'MALWARE_SANDBOX', True),
    ('Indirect retrieval of remote content', 'RETRIEVAL_PROXY', False),
    ('Unknown', 'RETRIEVAL_PROXY', True),
    ('Remote content retrieval and transformation', 'RETRIEVAL_PROXY', False),
    ('Remote browser operation', 'RETRIEVAL_PROXY', False),
    ('HTTP testing or request-handling', 'RETRIEVAL_PROXY', False),
    ('Webhook and request-inspection service', 'RETRIEVAL_PROXY', True),
    ('exact role needs confirmation', 'UNCONFIRMED', False),
    ('general function is not established', 'UNCONFIRMED', False),
    ('canonical URL has not been confirmed', 'UNCONFIRMED', False),
    ('General candidate class', 'UNCONFIRMED', False),
    ('IP/ASN context', 'UNCONFIRMED', False),
    ('Public messages and coordination attributed', 'PUBLIC_WIKI', False),
    ('Test or early public-wiki', 'PUBLIC_WIKI', False),
    ('Wiki revision histories', 'PUBLIC_WIKI', False),
    ('Agent board + post office', 'AGENT_BOARD', False),
    ('Agent Commons', 'AGENT_BOARD', False),
    ('Public agent board (MCP, OpenAPI, skill file, Atom feeds)', 'AGENT_BOARD', False),
    ('Agent messaging network', 'AGENT_BOARD', False),
    ('Zero-trust agent message board', 'AGENT_BOARD', False),
    ('Agent guestboard', 'AGENT_BOARD', False),
    ('passphrase-private channels', 'AGENT_BOARD', False),
    ('Agent board (llms.txt)', 'AGENT_BOARD', True),
    ('Agent board', 'AGENT_BOARD', True),
    ('Agent forum', 'AGENT_BOARD', True),
    ('pollable channel', 'AGENT_BOARD', False),
    ('on-chain treasury', 'AGENT_BOARD', False),
    ('Agent imageboard', 'AGENT_BOARD', False),
    ('Agent relay', 'AGENT_BOARD', True),
    ('agents hiring humans', 'AGENT_BOARD', False),
    ('Agent board, public posts', 'AGENT_BOARD', True),
    ('Agent message directory', 'AGENT_BOARD', True),
    ('Agent /offers board', 'AGENT_BOARD', True),
    ('pulse-check posts', 'AGENT_BOARD', False),
    ('mcp.json (dead', 'AGENT_BOARD', False),
    ('Agent surface, skill.md', 'AGENT_BOARD', True),
    ('dark since 2026-10-21', 'AGENT_BOARD', False),
    ('llms.txt write door', 'AGENT_BOARD', False),
    ('REST/A2A/MCP', 'AGENT_BOARD', False),
    ('concern reports', 'AGENT_BOARD', False),
    ('skill.md canon', 'AGENT_BOARD', False),
    ('Agent social network', 'AGENT_BOARD', True),
    ('older records, nature to re-verify', 'AGENT_BOARD', False),
    ('Live Hermes Agent deployment', 'AGENT_BOARD', False),
    ('Public agent log archive', 'COORDINATION_LOG', False),
    ('cross-board conversation guides', 'COORDINATION_LOG', False),
    ('Public mirror of the 1F916', 'COORDINATION_LOG', False),
    ('heartbeat-verified', 'AGENT_COLONY', False),
    ('Agent colony', 'AGENT_COLONY', True),
    ('council-governed', 'AGENT_COLONY', False),
    ('Agent swarm surface', 'AGENT_COLONY', True),
    ('Large-scale publication allegations', 'ARTIFACT_REGISTRY', False),
    ('Independent reporting alleges misuse', 'ARTIFACT_REGISTRY', False),
    ("Relevant external platform in OpenAI's published incident report", 'ARTIFACT_REGISTRY', False),
    ('Public repository activity and token-exposure', 'ARTIFACT_REGISTRY', False),
    ('Candidate public artifact', 'ARTIFACT_REGISTRY', False),
    ('OpenAI reported using internal Artifactory', 'ARTIFACT_REGISTRY', False),
    ('Module proxy', 'ARTIFACT_REGISTRY', False),
    ('temporary-email service', 'IDENTITY_SERVICE', False),
    ('Disposable email provider', 'IDENTITY_SERVICE', True),
    ('/paste/ endpoint', 'TEMP_FILE_HOST', False),
    ('Temp file host', 'TEMP_FILE_HOST', True),
    ('Paste archive', 'TEMP_FILE_HOST', True),
    ('raw view', 'TEMP_FILE_HOST', False),
    ('cityb dead-drop venue', 'TEMP_FILE_HOST', False),
    ('Markdown paste host', 'TEMP_FILE_HOST', True),
    ('Byte-bin raw host', 'TEMP_FILE_HOST', True),
    ('Dead-drop venue paired', 'TEMP_FILE_HOST', False),
    ('Pastebin-like source flagged', 'TEMP_FILE_HOST', False),
    ('Possible persistent storage', 'TEMP_FILE_HOST', False),
    ('Possible short text-sharing', 'TEMP_FILE_HOST', False),
    ('Potential artifact-transfer path', 'TEMP_FILE_HOST', True),
    ('General URL shortener', 'URL_SHORTENER', False),
    ('no specific YOURLS instance', 'URL_SHORTENER', False),
]

def map_role(value):
    v = (value or '').strip()
    hits = []
    for pat, term, exact in ROLE_PATTERNS:
        if (v == pat) if exact else (pat in v):
            hits.append((pat, term))
    if len(hits) != 1:
        raise RuntimeError(f'Role mapping ambiguous/unmatched for {v!r}: {hits}')
    return hits[0]

def extract_details(old_role):
    """Parenthetical groups (one nesting level) + post-'|' fragments."""
    details = []
    if '|' in old_role:
        for p in old_role.split('|')[1:]:
            p = p.strip()
            if p:
                details.append(p)
    # stack-based paren matching
    stack = []
    groups = []
    for i, ch in enumerate(old_role):
        if ch == '(':
            stack.append(i)
        elif ch == ')' and stack:
            s = stack.pop()
            if not stack:
                groups.append(old_role[s:i+1])
    for g in groups:
        inner = g[1:-1]
        if not any(inner in d for d in details):
            details.append(g)
    # quoted names ("Agent Commons") are detail too
    for m in re.finditer(r'"([^"]+)"', old_role):
        q = m.group(0)
        if not any(q in d for d in details):
            details.append(q)
    return details

def detail_covered(detail, sources_text, seen_text):
    # strip the paren characters themselves but KEEP the inner text for matching
    sig = re.sub(r'[()]', ' ', detail)
    sig = re.sub(r'[^a-zA-Z ]', ' ', sig).lower()
    words = [w for w in sig.split() if len(w) >= 4]
    if not words:
        return True
    blob = ((sources_text or '') + ' ' + (seen_text or '')).lower()
    hit = sum(1 for w in words if w in blob)
    return hit / len(words) >= 0.6

def main():
    wb2 = openpyxl.load_workbook(V2, data_only=False)   # lineage source, read-only use
    wb = openpyxl.load_workbook(V3)
    ws = wb[POI]
    wi = wb[INTEL]
    wn = wb['Notes']

    # ---- 1. Direct Links: drop self-referential GitHub + data/lanes parts
    for r in range(4, 105):
        c = cell(ws, r, 'K')
        v = c.value
        if isinstance(v, str) and (SELFREF in v or 'data/lanes/' in v):
            new = clean_links(v)
            if not new:
                new = 'unattributed — no specific URL established'
            setv(ws, POI, r, 'K', new, 'substitute')
    for r in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28]:
        c = cell(wi, r, 'E')
        v = c.value
        if isinstance(v, str) and (SELFREF in v or 'data/lanes/' in v):
            if r == 7:
                setv(wi, INTEL, r, 'E',
                     'unattributed — internal wiki-investigation dataset, no public home',
                     'substitute')
            else:
                setv(wi, INTEL, r, 'E', clean_links(v), 'substitute')

    # ---- 2. Generic Factum scrub on visible-sheet text cells
    # POI: F (Ops), J (Sources), L (Seen), R (Review flag)
    for r in range(4, 105):
        for col in 'FJLR':
            c = cell(ws, r, col)
            v = c.value
            if isinstance(v, str):
                new = scrub_text(v)
                if new != v:
                    setv(ws, POI, r, col, new, 'scrub')
    # Intel: D (Use), E (Direct source), F (Attribution), G (Review flag)
    for r in [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,23,24,25,26,27,28]:
        for col in 'DEFG':
            c = cell(wi, r, col)
            v = c.value
            if isinstance(v, str):
                new = scrub_text(v)
                if new != v:
                    setv(wi, INTEL, r, col, new, 'scrub')

    # ---- 3. Special-case rewrites
    # R12 L: attribution marker -> neutral
    setv(ws, POI, 12, 'L',
         'Cloudflare Workers Playground (execution surface). No established agent-actor attribution in the data reviewed to date.',
         'special')
    # R40 L: lane-name form -> descriptive
    setv(ws, POI, 40, 'L', 'Seen in 2026-09-03 agent-surface captures', 'special')
    # Intel F9: drop internal scan-lane citation
    f9 = cell(wi, 9, 'F').value
    if isinstance(f9, str) and 'lab-intel-anthropic-scan' in f9:
        setv(wi, INTEL, 9, 'F', f9.replace(', ingested by the lab-intel-anthropic-scan', ''), 'special')
    # Intel F17: drop "(iocfeeds lane 14)"
    f17 = cell(wi, 17, 'F').value
    if isinstance(f17, str):
        setv(wi, INTEL, 17, 'F', f17.replace(' (iocfeeds lane 14)', ''), 'special')
    # POI L76/L89/L90: lane-ID form -> descriptive
    for r in (76, 89, 90):
        v = cell(ws, r, 'L').value
        if isinstance(v, str):
            setv(ws, POI, r, 'L',
                 v.replace('2026-09-28-chinese-amap-fleet lane context',
                           'Chinese Amap fleet context'), 'special')

    # ---- 4. Row 14 canonical name (DSEWiki vs ProWiki -> DSEWiki)
    setv(ws, POI, 14, 'B', 'DSEWiki (prowiki.org → wikiservice.at/dse)', 'row14')
    r14r = cell(ws, 14, 'R').value or ''
    r14r = r14r.replace(
        'canonical host should be verified from the incident source before use in a collector (moved from URL cell 2026-10-23)',
        'canonical host verified from the incident source 2026-10-23 (Transluce #42 evidence: prowiki.org/dse; LEAD-3 live capture: wikiservice.at/dse)')
    r14r = r14r.replace(
        'canonical name DSEWiki vs ProWiki unresolved — operator word needed',
        'canonical name resolved 2026-10-23: DSEWiki (incident-source host prowiki.org → current host wikiservice.at/dse); choice recorded in Notes')
    setv(ws, POI, 14, 'R', r14r, 'row14')
    r14l = cell(ws, 14, 'L').value or ''
    setv(ws, POI, 14, 'L',
         r14l.replace('Row notes canonical host must be verified before collector use.',
                      'Canonical name and host resolved 2026-10-23: DSEWiki (prowiki.org → wikiservice.at/dse); see Review flag.'),
         'row14')

    # ---- 5. Rows 31/32/34/35: reconcile counts to trajectory-domains.md (2026-10-19)
    rec = {31: 103, 32: 16, 34: 114, 35: 53}
    oldn = {31: 105, 32: 17, 34: 248, 35: 57}
    for r, n in rec.items():
        o = oldn[r]
        j = cell(ws, r, 'J').value
        setv(ws, POI, r, 'J',
             j.replace(f'trajectory-domains Tier 1; Internal corpus hits {o}',
                       f'trajectory-domains Tier 1; Internal corpus hits {n} (per trajectory-domains.md, 2026-10-19)'),
             'retally')
        lv = cell(ws, r, 'L').value
        setv(ws, POI, r, 'L',
             lv.replace(f'trajectory-domains Tier 1; {o} Internal corpus hits',
                        f'trajectory-domains Tier 1; {n} Internal corpus hits (per trajectory-domains.md, 2026-10-19)'),
             'retally')
        base = ('Reconciled 2026-10-23: count updated to the cited source value '
                '(trajectory-domains.md, 2026-10-19); a corpus-wide re-tally awaits '
                'the next regeneration of that source')
        if r == 34:
            tail = cell(ws, r, 'R').value or ''
            extra = ''
            if 'auth-gated 2026-10-23' in tail:
                extra = '; auth-gated 2026-10-23 (ID verified in local cache): cloudfront findings #171'
            setv(ws, POI, r, 'R',
                 base + ' — the workbook\'s 248 was an error (not reproducible under a consistent method)' + extra,
                 'retally')
        else:
            setv(ws, POI, r, 'R', base, 'retally')

    # ---- 6. Role column -> 12-term controlled set
    unmatched = []
    for r in range(4, 105):
        c = cell(ws, r, 'I')
        old = (c.value or '').strip()
        try:
            pat, term = map_role(old)
        except RuntimeError as e:
            unmatched.append((r, old))
            continue
        # migrate parenthetical / pipe detail to Seen when not already covered
        details = extract_details(old)
        for d in details:
            d_scrub = scrub_text(d)
            if not detail_covered(d_scrub, cell(ws, r, 'J').value, cell(ws, r, 'L').value):
                lv = cell(ws, r, 'L').value
                add = d_scrub if not (lv and lv.strip()) else (lv.rstrip() + '; ' + d_scrub)
                setv(ws, POI, r, 'L', add, 'role-detail')
        if old != term:
            setv(ws, POI, r, 'I', term, f'role:{pat}')
    if unmatched:
        raise RuntimeError(f'unmapped Role values: {unmatched}')
    # review-flag notes for the two judgment-call residuals
    r8r = cell(ws, 8, 'R').value
    if not r8r:
        setv(ws, POI, 8, 'R',
             "Role mapped Unknown → RETRIEVAL_PROXY (controlled set 2026-10-23; capability 'fetcher' established, incident role unconfirmed)",
             'role-note')
    r91r = cell(ws, 91, 'R').value or ''
    setv(ws, POI, 91, 'R',
         r91r + ('; ' if r91r else '') +
         'Role mapped to AGENT_BOARD (controlled set 2026-10-23; a harness endpoint is the set\'s worst fit — a 13th HARNESS_ENDPOINT term was proposed but not adopted)',
         'role-note')

    # ---- 7. Notes: R43C + R123A neutral wording
    c43 = cell(wn, 43, 'C').value
    if isinstance(c43, str) and 'GitHub' in c43:
        setv(wn, 'Notes', 43, 'C', c43.replace('GitHub', 'public code forges'), 'notes')
    c123 = cell(wn, 123, 'A').value
    if isinstance(c123, str) and 'Factum count deltas' in c123:
        setv(wn, 'Notes', 123, 'A', c123.replace(
            'Factum count deltas (rows 31/32/34/35) flagged for re-tally, not reconciled here.',
            'Internal corpus count deltas (rows 31/32/34/35) reconciled 2026-10-23 against their cited source trajectory-domains.md (2026-10-19): counts updated to 103 / 16 / 114 / 53; a corpus-wide re-tally awaits the next regeneration of that source.'), 'notes')

    # ---- 8. INTERNAL lineage sheet (exempt from the visible-sheet machine check)
    flag_rx = {
        'factum': re.compile(r'factum', re.I),
        'github': re.compile(r'github', re.I),
        'lanepath': re.compile(r'data/lanes/'),
        'batchid': re.compile(r'd6982046'),
        'lanename': re.compile(r'\blanes?\s+[a-z0-9][a-z0-9\-_/]*', re.I),
        'labscan': re.compile(r'lab-intel-[a-z\-]+', re.I),
        'lane-slug': re.compile(r'2026-09-03[ -]collusion-manifest|2026-09-28[ -]chinese-amap-fleet', re.I),
    }
    keep = {'https://github.com', 'https://gist.github.com',
            'github.com/youdotcom-oss/minimax-m3-deepsearchqa-skill-eval'}
    if 'INTERNAL — do not distribute' in wb.sheetnames:
        wb.remove(wb['INTERNAL — do not distribute'])
    wi2 = wb.create_sheet('INTERNAL — do not distribute', 2)
    wi2.sheet_properties.tabColor = 'FF0000'
    wi2.append(['Sheet', 'Row', 'Cell', 'Flag class', 'Original v2 value', 'v3 disposition'])
    for name in [POI, INTEL, 'Notes']:
        wsrc = wb2[name]
        for row in wsrc.iter_rows():
            for cc in row:
                v = cc.value
                if not isinstance(v, str):
                    continue
                hits = [k for k, p in flag_rx.items() if p.search(v)]
                if not hits:
                    continue
                disp = 'scrubbed/removed in v3'
                if any(k in v for k in keep) and SELFREF not in v and 'factum' not in v.lower():
                    disp = 'retained in v3 — third-party, not self-referential (operator rule)'
                if name == POI and cc.row in (60, 61) and cc.column_letter in ('B', 'K'):
                    disp = 'retained in v3 — third-party surface (operator rule)'
                wi2.append([name, cc.row, cc.column_letter, ','.join(hits), v, disp])
    for col, w in zip('ABCDEF', (32, 6, 6, 14, 60, 52)):
        wi2.column_dimensions[col].width = w

    # ---- 9. Notes additions
    rows_notes = []
    rows_notes.append(('v3 changelog (2026-10-23) — BUILD lane: self-referential source scrub',
        '120 self-referential silent-locus GitHub URL instances removed from Direct Links cells (Agent POIs col K, Intelligence col E); the verified direct surface URL stays in each cell. Internal data/lanes/... paths stripped from Direct Links cells (POI K19–K26, Intel E9/E27/E28) and from Ops/Seen text. Factum batch ID d6982046 stripped from 14 visible cells (POI J/L 19, 21–26) with no replacement. Visible-sheet wording: the word Factum is gone — counts stay as "N Internal corpus hits"; "not in Factum/lanes/hunt data" → "not previously catalogued". Three third-party GitHub instances stay per the operator rule: POI K60 (github.com), K61 (gist.github.com), and the L60 evidence note naming github.com/youdotcom-oss/minimax-m3-deepsearchqa-skill-eval. Full per-cell lineage of every removed value is on the sheet "INTERNAL — do not distribute".'))
    rows_notes.append(('v3 open-item resolutions (2026-10-23)',
        '(a) Row 14 canonical name: DSEWiki (prowiki.org → wikiservice.at/dse). Evidence: Transluce #42 incident-source link prowiki.org/dse/wiki.cgi; LEAD-3 live capture of the same DSE wiki ForumSeite at wikiservice.at/dse (2026-10-23); Nightingale Collective dump lists wikiservice.at/dse as the main surface. "ProWiki" was the incident-time host, not a separate venue. (b) Role column: 12-term controlled set applied (see below); the full 76-value mapping follows. (c) Rows 31/32/34/35 counts: reconciled to their cited source trajectory-domains.md (2026-10-19) — 103 / 16 / 114 / 53, each stamped with the source. The workbook\'s 248 (row 34) was an error and is not reproducible under a consistent method. A corpus-wide re-tally awaits the next regeneration of that source.'))
    rows_notes.append(('Role controlled set, v3 (Counsel-C proposal, applied 2026-10-23)', ''))
    for term, definition in ROLE_DEFS:
        rows_notes.append((f'  {term}', definition))
    rows_notes.append(('Role value → controlled term (all 76 v2 values; parenthetical detail moved to Seen where not already present)', ''))
    # rebuild mapping rows in a stable order
    seen_map = []
    for pat, term, exact in ROLE_PATTERNS:
        seen_map.append((pat, term, exact))
    for pat, term, exact in seen_map:
        tag = 'exact' if exact else 'prefix'
        rows_notes.append((f"  '{pat}' → {term}", f'match: {tag}'))
    rows_notes.append(('Judgment calls in the Role mapping (flagged for the operator)',
        'Agent swarm surface → AGENT_COLONY (swarm treated as a collective). Possible persistent storage/transfer channel → TEMP_FILE_HOST (could equally sit in ARTIFACT_REGISTRY). Live Hermes Agent deployment → AGENT_BOARD (worst fit in the set; a harness endpoint is not a board — a 13th HARNESS_ENDPOINT term was proposed but not adopted; noted in row 91 Review flag). s.jina.ai "Unknown" → RETRIEVAL_PROXY (capability "fetcher" is established; residual uncertainty noted in row 8 Review flag). "Public board (older records, nature to re-verify)" → AGENT_BOARD (value added after Counsel-C wrote its table).'))
    r = 126
    for a, b in rows_notes:
        cell(wn, r, 'A').value = a
        if b:
            cell(wn, r, 'B').value = b
        changes.append(('Notes', r, 'A', 'notes-add', None, a))
        r += 1

    # ---- save with EPERM retries
    for attempt in range(5):
        try:
            wb.save(V3)
            break
        except (PermissionError, OSError) as e:
            if attempt == 4:
                raise
            time.sleep(2 * (attempt + 1))
    print(f'OK: {len(changes)} cell changes applied; saved {V3}')

if __name__ == '__main__':
    main()
