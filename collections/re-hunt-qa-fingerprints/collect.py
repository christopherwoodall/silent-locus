#!/usr/bin/env python3
"""
Lane 1 (re-hunt-qa-fingerprints): derive distinctive fingerprint strings from
the 900 DeepSearchQA questions, then sweep them across the frozen corpora
(case-insensitive fixed-string matching).

Outputs (under this lane dir):
  fingerprints.jsonl   one row per question: {"qid","fingerprints":[...],"skipped":bool,...}
  patterns.txt         working file: unique fingerprints, one per line
  data/hits.jsonl      annotated hits (capped per key; keep-all, staged, never merged)
  pattern-log.jsonl    every (qid, fingerprint, corpus) tried, with hit counts (zeros included)
  state.json           watermarks, counts, resume state

Idempotent: re-running resumes from state.json. Questions already fingerprinted
are skipped; corpora fully swept are skipped; a corpus interrupted mid-sweep has
its hits/pattern-log rows purged and is re-swept from scratch. Never duplicates
rows, never invents data. Corpora are opened read-only.

Stdlib only.
"""

import gzip
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

LANE_DIR = Path(__file__).resolve().parent
QUESTIONS_PATH = (LANE_DIR / ".." / "deepsearchqa" / "data" / "questions.jsonl").resolve()
EXPORTS_DIR = Path(os.path.expanduser(
    "~/workspace/muse-home/projects/swarmtraces-hf-corpus/elastic-exports"))
ARQUIVO_RAW = Path(os.path.expanduser(
    "~/workspace/silent-locus/data/2026-10-01-arquivo-pt/raw"))

FP_PATH = LANE_DIR / "fingerprints.jsonl"
PATTERNS_PATH = LANE_DIR / "patterns.txt"
HITS_PATH = LANE_DIR / "data" / "hits.jsonl"
PLOG_PATH = LANE_DIR / "pattern-log.jsonl"
STATE_PATH = LANE_DIR / "state.json"

HITS_CAP_PER_KEY = 25
EXCERPT_LEN = 400

# ----------------------------------------------------------------------------
# Fingerprint extraction
# ----------------------------------------------------------------------------

CURATED = [
    # education
    (r'\bCRDC\b', 'CRDC'),
    (r'Civil Rights Data Collection', 'Civil Rights Data Collection'),
    (r'National Center for Education Statistics', 'National Center for Education Statistics'),
    (r'\bNCES\b', 'NCES'),
    (r'data\.nysed\.gov', 'data.nysed.gov'),
    (r'\bNYSED\b', 'NYSED'),
    (r'tea\.texas\.gov', 'tea.texas.gov'),
    (r'Klein ISD', 'Klein ISD'),
    (r'Toronto District School [Bb]oard', 'Toronto District School Board'),
    (r'Toronto District School Board', 'Toronto District School Board'),
    # justice
    (r'\bOJJDP\b', 'OJJDP'),
    (r'Office of Juvenile Justice', 'Office of Juvenile Justice'),
    (r'Bureau of Justice Statistics', 'Bureau of Justice Statistics'),
    (r'\bBJS\b', 'BJS'),
    (r'Uniform Crime Report', 'Uniform Crime Reports'),
    (r'\bUCR\b', 'UCR'),
    (r'National Crime Victimization Survey', 'National Crime Victimization Survey'),
    (r'\bNCVS\b', 'NCVS'),
    (r'FBI Crime Data Explorer', 'FBI Crime Data Explorer'),
    (r'cde\.ucr\.cjis\.gov', 'cde.ucr.cjis.gov'),
    (r'ojjdp\.ojp\.gov', 'ojjdp.ojp.gov'),
    # census / econ / labor
    (r'Census Bureau', 'Census Bureau'),
    (r'U\.S\. Census', 'U.S. Census'),
    (r'US Census Bureau', 'US Census Bureau'),
    (r'American Community Survey', 'American Community Survey'),
    (r'\bACS\b', 'ACS'),
    (r'decennial census', 'decennial census'),
    (r'data\.census\.gov', 'data.census.gov'),
    (r'census\.gov', 'census.gov'),
    (r'\bBEA\b', 'BEA'),
    (r'Bureau of Economic Analysis', 'Bureau of Economic Analysis'),
    (r'bea\.gov', 'bea.gov'),
    (r'\bBLS\b', 'BLS'),
    (r'Bureau of Labor Statistics', 'Bureau of Labor Statistics'),
    (r'bls\.gov', 'bls.gov'),
    (r'Current Population Survey', 'Current Population Survey'),
    (r'\bCPS\b', 'CPS'),
    (r'\bFRED\b', 'FRED'),
    (r'fred\.stlouisfed\.org', 'fred.stlouisfed.org'),
    (r'St\.? Louis Fed', 'St Louis Fed'),
    (r'\bNAICS\b', 'NAICS'),
    (r'North American Industry Classification', 'North American Industry Classification System'),
    (r'county\.json', 'county.json'),
    (r'\bEDGAR\b', 'EDGAR'),
    (r'\bIPUMS\b', 'IPUMS'),
    (r'\bNHGIS\b', 'NHGIS'),
    (r'\bDataUSA\b', 'DataUSA'),
    (r'datacommons', 'datacommons'),
    (r'\bOMB\b', 'OMB'),
    (r'MAX\.gov', 'MAX.gov'),
    (r'max\.gov', 'max.gov'),
    (r'\bSF-?133\b', 'SF133'),
    (r'\bFIPS\b', 'FIPS'),
    (r'\bFEC\b', 'FEC'),
    (r'Federal Election Commission', 'Federal Election Commission'),
    (r'Survey of Income and Program Participation', 'Survey of Income and Program Participation'),
    (r'\bSIPP\b', 'SIPP'),
    # health
    (r'CDC WONDER', 'CDC WONDER'),
    (r'\bWONDER\b', 'WONDER'),
    (r'wonder\.cdc\.gov', 'wonder.cdc.gov'),
    (r'\bCDC\b', 'CDC'),
    (r'\bNCHS\b', 'NCHS'),
    (r'National Center for Health Statistics', 'National Center for Health Statistics'),
    (r'National Health Interview Survey', 'National Health Interview Survey'),
    (r'\bNHIS\b', 'NHIS'),
    (r'\bBRFSS\b', 'BRFSS'),
    (r'\bMEPS\b', 'MEPS'),
    (r'Aotearoa Data Explorer', 'Aotearoa Data Explorer'),
    # well-known non-gov datasets / sources named in questions
    (r'Our World in Data', 'Our World in Data'),
    (r'Vision of Humanity', 'Vision of Humanity'),
    (r'World Happiness Report', 'World Happiness Report'),
    (r'World Population Review', 'World Population Review'),
    (r'Pew Research Center', 'Pew Research Center'),
    (r'National Weather Service', 'National Weather Service'),
    # energy / misc agencies often written lowercase in questions
    (r'(?i)\beia\b', 'EIA'),
    (r'(?i)\bfaostat\b', 'FAOSTAT'),
    (r'(?i)\beurostat\b', 'Eurostat'),
    (r'(?i)\bworld bank\b', 'World Bank'),
    (r'\bG7\b', 'G7'),
    # incident-adjacent surfaces (kept for completeness; rarely in questions)
    (r'civilrightsdata\.ed\.gov', 'civilrightsdata.ed.gov'),    (r'\bCAL-ACCESS\b', 'CAL-ACCESS'),
    (r'\bcalaccess\b', 'calaccess'),
    (r'kansasmemory', 'kansasmemory'),
    (r'\bIQuery\b', 'IQuery'),
    (r'collectionsearch', 'collectionsearch'),
    (r'history\.navy\.mil', 'history.navy.mil'),
    (r'dshs\.texas\.gov', 'dshs.texas.gov'),
    (r'nysenate\.gov', 'nysenate.gov'),
    (r'gov\.scot', 'gov.scot'),
    (r'data\.london\.gov\.uk', 'data.london.gov.uk'),
    (r'calderdale\.gov\.uk', 'calderdale.gov.uk'),
]

COMMON_START = {
    'The', 'A', 'An', 'In', 'On', 'At', 'For', 'Of', 'And', 'By', 'From', 'With',
    'Which', 'What', 'When', 'Where', 'Who', 'Whose', 'Name', 'Identify', 'Consider',
    'List', 'Tell', 'Based', 'Using', 'According', 'Between', 'Among', 'Amongst',
    'During', 'These', 'Those', 'This', 'That', 'There', 'Out', 'Each', 'Overall',
    'How', 'If', 'As', 'To', 'Is', 'Are', 'Was', 'Were', 'Be', 'It', 'Its', 'His',
    'Her', 'Their', 'Your', 'Our', 'No', 'Not', 'All', 'Any', 'Both', 'Few', 'More',
    'Most', 'Other', 'Some', 'Such', 'Only', 'Own', 'Same', 'Than', 'Too', 'Very',
    'Can', 'Will', 'Just', 'Should', 'Now', 'Then', 'While', 'After', 'Before',
    'Since', 'Until', 'Unless', 'Although', 'Because', 'Through', 'Across', 'Within',
    'Without', 'About', 'Into', 'Over', 'Under', 'Above', 'Below', 'Up', 'Down',
    'Use', 'Find', 'Give', 'Describe', 'Explain', 'Include', 'Provide', 'Please',
}

ACRONYM_STOP = {
    'THE', 'AND', 'FOR', 'ARE', 'WAS', 'WERE', 'HAS', 'HAVE', 'HAD', 'WITH', 'FROM',
    'THAT', 'THIS', 'THESE', 'THOSE', 'WILL', 'WOULD', 'CAN', 'NOT', 'ALL', 'ANY',
    'EACH', 'SUCH', 'OVER', 'UNDER', 'BETWEEN', 'AMONG', 'ABOUT', 'INTO', 'THROUGH',
    'DURING', 'BEFORE', 'AFTER', 'SINCE', 'WHILE', 'WHEN', 'WHERE', 'WHICH', 'WHOSE',
    'THEIR', 'THERE', 'THEN', 'THAN', 'ALSO', 'JUST', 'ONLY', 'EVEN', 'EVER', 'NEVER',
    'EVERY', 'BOTH', 'FEW', 'MORE', 'MOST', 'OTHER', 'SOME', 'SAME', 'MAY', 'OUT',
    'OFF', 'NEW', 'OLD', 'OWN', 'PER',
    # common English words / fragments that show up all-caps in questions
    # (column headers, table labels) but are useless as fingerprints
    'REPORT', 'REPORTS', 'TITLE', 'TITLES', 'TIME', 'TIMES', 'CATEGORY',
    'CATEGORIES', 'ANSWER', 'ANSWERS', 'COUNTY', 'COUNTIES', 'WATER', 'QUALITY',
    'AUTHOR', 'AUTHORS', 'AWARDS', 'TOY', 'TOYS', 'VACANCY', 'SMALLER', 'SUPREME',
    'BUS', 'BUSES', 'PEN', 'PENS', 'RAP', 'SAR', 'CAD', 'DEF', 'ECO', 'JAN',
    'CAROL', 'BURKE', 'GOS', 'FEUS', 'POTS', 'PLC', 'ORR', 'DBA', 'WNA', 'SUV',
    'SQA', 'PCN', 'USA', 'USD', 'OPS', 'III', 'YYYY',
}

GENERIC_ENTITIES = {
    'United States', 'New York', 'United Kingdom', 'Los Angeles', 'New York City',
    'San Francisco', 'United Nations', 'European Union', 'South Korea', 'North Korea',
    'Saudi Arabia', 'South Africa', 'New Zealand', 'Sri Lanka', 'Costa Rica',
    'Puerto Rico', 'District of Columbia',
}

GOV_TAGS = {'gov-data', 'gov-census', 'gov-education', 'gov-education-ny',
            'gov-education-tx', 'gov-elections', 'gov-fbi', 'gov-bea', 'gov-cdc',
            'census-flavored'}

QUOTED_RE = re.compile(r'(?<![\w"\u201d])["\u201c]([^"\u201c\u201d]{4,90})["\u201c\u201d]')
PAREN_ACR_RE = re.compile(r'\(([A-Z][A-Z0-9&.\-]{1,9})\)')
DOMAIN_RE = re.compile(r'[\w.\-]*\.(?:gov|edu|org|com|net|io)(?:\.[\w]+)?(?:/[\w.\-/\[\]]*)?')
SINGLE_RE = re.compile(r"\b([A-Z][A-Za-z'\-]{3,})\b")

# single capitalized words that are too generic to be useful fingerprints
SINGLE_STOP = COMMON_START | {
    'House', 'Senate', 'Congress', 'States', 'State', 'Report', 'Reports', 'Table',
    'Tables', 'Service', 'Services', 'Data', 'Study', 'Studies', 'Survey', 'Surveys',
    'Index', 'Group', 'Groups', 'Company', 'Companies', 'Magazine', 'University',
    'College', 'School', 'Schools', 'Center', 'Centre', 'Department', 'Agency',
    'Office', 'Committee', 'Commission', 'Council', 'Board', 'Court', 'Courts',
    'Case', 'Cases', 'Country', 'Countries', 'City', 'Cities', 'County', 'Counties',
    'Region', 'Regions', 'District', 'Ward', 'Wards', 'Parliament', 'Assembly',
    'Ministry', 'Bureau', 'Administration', 'Institute', 'Foundation', 'Society',
    'Association', 'Program', 'Programs', 'Project', 'Projects', 'System', 'Systems',
    'Database', 'List', 'Order', 'Term', 'Year', 'Years', 'Month', 'Months', 'Week',
    'Day', 'Days', 'January', 'February', 'March', 'April', 'June', 'July',
    'August', 'September', 'October', 'November', 'December', 'Monday', 'Tuesday',
    'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'North', 'South',
    'East', 'West', 'Central', 'United', 'Great', 'First', 'Second', 'Third',
    'Total', 'Average', 'Median', 'General', 'Annual', 'National', 'Federal',
    'American', 'World', 'Global', 'International', 'European', 'African', 'Asian',
    'English', 'French', 'Spanish', 'Public', 'Private', 'Major', 'Minor', 'Official',
    'Highest', 'Lowest', 'Largest', 'Smallest', 'Best', 'Worst', 'Top', 'Bottom',
    'Revenues', 'Revenue', 'Sales', 'Prices', 'Price', 'Rates', 'Rate', 'Number',
    'Numbers', 'Percent', 'Share', 'Season', 'Game', 'Team', 'Teams', 'Player',
    'Players', 'Issue', 'Issues', 'Article', 'Articles', 'Page', 'Pages', 'Volume',
    'Version', 'Mode', 'Edition', 'Series', 'Episode', 'Season', 'Song', 'Songs',
    'Album', 'Film', 'Movie', 'Show', 'Book', 'Author', 'Director', 'President',
    'Senator', 'Representative', 'Governor', 'Mayor', 'Judge', 'Justice', 'Member',
    'Members', 'People', 'Person', 'Man', 'Woman', 'Child', 'Children', 'Family',
    'Women', 'Voters', 'Vote', 'Votes', 'Election', 'Elections', 'Bill', 'Bills',
    'Law', 'Laws', 'Act', 'Amendment', 'Resolution', 'Motion', 'Question',
    'Return', 'Returns', 'Americas', 'Nations', 'Nation', 'Area', 'Areas',
    'Period', 'Range', 'Kind', 'Type', 'Types', 'Title', 'Subject', 'Topic',
    'Field', 'Fields', 'Basis', 'Source', 'Sources', 'Figure', 'Figures',
    'Part', 'Parts', 'Form', 'Forms', 'Level', 'Levels', 'Degree', 'Amount',
    'Quantity', 'Names', 'Word', 'Words', 'Line', 'Lines', 'Row', 'Rows',
    'Column', 'Columns', 'Chart', 'Graph', 'Map', 'Image', 'Photo', 'Video',
    'Track', 'Tracks', 'Category', 'Categories', 'Answer', 'Answers',
    'Cohort', 'Cohorts',
}
ACRONYM_RE = re.compile(r'\b([A-Z]{3,8})\b')
CODE_RE = re.compile(r'\b(?=[A-Z0-9\-]*[0-9])(?=[A-Z0-9\-]*[A-Z])[A-Z0-9\-]{3,14}\b')
_IMPERATIVES = (r'List|Find|Name|Identify|Tell|Consider|Describe|Explain|Give|Use|'
                r'Include|Using|Based|According')
CONNECTOR_RE = re.compile(
    r"\b(?!(?:" + _IMPERATIVES + r")\b)"
    r"([A-Z][A-Za-z'\-.]*"
    r"(?:\s+(?:and|of|for|in|the|on|&)\s+[A-Z][A-Za-z'\-.]*"
    r"(?:\s+[A-Z][A-Za-z'\-.]*)*){1,2})\b")
ENTITY_RE = re.compile(r"\b([A-Z][A-Za-z'\-.]*(?:\s+[A-Z][A-Za-z'\-.]*){1,4})\b")
_COMMON_WORDS_LOOKAHEAD = (
    r'In|The|A|An|On|At|For|Of|And|By|From|With|To|As|If|How|Each|Out|All|Any|Both|'
    r'Few|More|Most|Other|Some|Such|Only|Own|Same|Than|Too|Very|No|Not|Up|Down|Over|'
    r'Under|Above|Below|Between|Among|During|While|After|Before|Since|Until|Unless|'
    r'Although|Because|Through|Across|Within|Without|About|Into|Use|Find|Name|List|'
    r'Tell|Consider|Based|Using|According|Which|What|When|Where|Who|Whose')
DIGIT_ENTITY_RE = re.compile(
    r"\b(?!(?:" + _COMMON_WORDS_LOOKAHEAD + r")\b)"
    r"([A-Z][A-Za-z'\-.]*(?:\s+[A-Za-z0-9'\-.,]+){1,3})\b")
TOKEN_RE = re.compile(r'[a-z0-9]+')


def normalize(text):
    return (text.replace('\u2019', "'").replace('\u2018', "'")
                .replace('\u2013', '-').replace('\u2014', '-'))


def clean_entity(ent):
    ent = re.sub(r"'s$", "", ent).strip()
    # strip sentence-bleed: trailing ". <CommonWord>"
    if '. ' in ent:
        head, tail = ent.rsplit('. ', 1)
        if tail.split()[0].title() in COMMON_START:
            ent = head.strip()
    return ent


def possessive_variants(ent):
    """Original plus 's-stripped variant when 's precedes a proper noun."""
    variants = [ent]
    ent2 = re.sub(r"'s(?= [A-Z])", "", ent)
    if ent2 != ent and ent2 not in variants:
        variants.append(ent2)
    return variants


def strip_leading_common(ent):
    words = ent.split()
    while (len(words) > 1 and words[0].title() in COMMON_START
           and words[1][:1].isupper()):
        words.pop(0)
    return ' '.join(words)


def extract_fingerprints(text):
    """Return up to 4 distinctive fingerprint strings for a question."""
    text = normalize(text)
    cands = []          # (priority, fingerprint)
    seen = set()

    def add(prio, fp):
        fp = re.sub(r'\s+', ' ', fp).strip().strip('.,;:!?').strip()
        if len(fp) < 3 or len(fp) > 90:
            return
        key = fp.casefold()
        if key in seen:
            return
        seen.add(key)
        cands.append((prio, fp))

    # 0. curated dataset / agency / domain fingerprints
    for rx, canon in CURATED:
        if re.search(rx, text):
            add(0, canon)

    # 1. quoted phrases (usually titles / exact terms)
    for m in QUOTED_RE.finditer(text):
        q = m.group(1).strip()
        toks = q.split()
        if len(toks) >= 2 or (len(toks) == 1 and toks[0][:1].isupper() and len(q) >= 6):
            add(1, q)

    # 2. parenthetical acronyms, domains, alphanumeric codes, bare acronyms
    for m in PAREN_ACR_RE.finditer(text):
        if m.group(1) not in ACRONYM_STOP:
            add(2, m.group(1))
    for m in DOMAIN_RE.finditer(text):
        add(2, m.group(0).rstrip('/'))
    for m in CODE_RE.finditer(text):
        code = m.group(0).strip('-')
        if len(code) >= 3 and not code.replace('-', '').isdigit():
            add(2, code)
    for m in ACRONYM_RE.finditer(text):
        acr = m.group(1)
        if acr not in ACRONYM_STOP:
            add(2, acr)

    # 3. multi-word entities with lowercase connectors ("Center for X Rankings")
    for m in CONNECTOR_RE.finditer(text):
        ent = clean_entity(m.group(1))
        if ent in GENERIC_ENTITIES or len(ent) < 8:
            continue
        add(3, ent)

    # 3. plain capitalized entities
    for m in ENTITY_RE.finditer(text):
        ent = clean_entity(m.group(1))
        ent = strip_leading_common(ent)
        words = ent.split()
        if not words or words[0].title() in COMMON_START:
            continue
        # a lone generic word left after stripping (e.g. "THAT COUNTY" -> "COUNTY")
        if len(words) == 1 and words[0].title() in SINGLE_STOP:
            continue
        if ent in GENERIC_ENTITIES or len(ent) < 6:
            continue
        if all(len(w) <= 3 for w in words):
            continue
        for v in possessive_variants(ent):
            add(3, v)

    # 4. digit-containing entities ("World's 50 Best")
    for m in DIGIT_ENTITY_RE.finditer(text):
        ent = clean_entity(m.group(1))
        ent = strip_leading_common(ent)
        words = ent.split()
        caps = [w for w in words if w[:1].isupper()]
        if len(caps) < 2:
            continue
        if not any(any(ch.isdigit() for ch in w) for w in words):
            continue
        if ent in GENERIC_ENTITIES or len(ent) < 6:
            continue
        for v in possessive_variants(ent):
            add(4, v)

    # 5. distinctive single-word proper nouns (lowest priority)
    added_words = set()
    for _, fp in cands:
        added_words.update(TOKEN_RE.findall(fp.casefold()))
    for m in SINGLE_RE.finditer(text):
        tok = re.sub(r"'s$", "", m.group(1))
        if len(tok) < 4:
            continue
        if tok.casefold() in added_words:
            continue
        tok_title = tok.title()
        # camelCase / interior caps are almost always proper nouns
        if not re.search(r'[a-z][A-Z]', tok) and tok_title in SINGLE_STOP:
            continue
        if tok_title in GENERIC_ENTITIES:
            continue
        add(5, tok)

    cands.sort(key=lambda x: (x[0], -len(x[1])))
    return [fp for _, fp in cands[:4]]


# ----------------------------------------------------------------------------
# State / IO helpers
# ----------------------------------------------------------------------------

def utcnow():
    return datetime.now(timezone.utc).isoformat()


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {
        "lane": "re-hunt-qa-fingerprints",
        "started_utc": utcnow(),
        "updated_utc": utcnow(),
        "questions_total": 900,
        "questions_fingerprinted": 0,
        "questions_skipped": 0,
        "fingerprints_total": 0,
        "unique_patterns": 0,
        "corpora_swept": [],
        "items_collected": 0,
        "status": "in-progress",
        "watermarks": [],
    }


def save_state(state):
    state["updated_utc"] = utcnow()
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n")


def load_fingerprints():
    rows = {}
    if FP_PATH.exists():
        for line in FP_PATH.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                rows[r["qid"]] = r
    return rows


def corpus_specs():
    specs = [
        ("urlquery-incidents",
         EXPORTS_DIR / "urlquery-incidents-20260928T022324Z.jsonl.gz", "es"),
        ("collusion-wiki",
         EXPORTS_DIR / "collusion-wiki-20260928T025051Z.jsonl.gz", "es"),
        ("rubygems-goimport",
         EXPORTS_DIR / "rubygems-goimport-campaign-20260928T022324Z.jsonl.gz", "es"),
    ]
    for p in sorted(ARQUIVO_RAW.glob("*.cdx.jsonl.gz")):
        specs.append((f"arquivo-pt/{p.name}", p, "cdx"))
    return specs


def purge_corpus_rows(label):
    """Remove hits + pattern-log rows for a corpus (used when re-sweeping)."""
    for path in (HITS_PATH, PLOG_PATH):
        if not path.exists():
            continue
        kept = [l for l in path.read_text().splitlines()
                if l.strip() and json.loads(l).get("corpus") != label]
        path.write_text("\n".join(kept) + ("\n" if kept else ""))


# ----------------------------------------------------------------------------
# Sweep
# ----------------------------------------------------------------------------

def build_automaton_index(patterns):
    """Token-inverted index: token -> set of pattern indices (prefilter)."""
    tok2pats = {}
    for i, p in enumerate(patterns):
        for tok in set(TOKEN_RE.findall(p)):
            tok2pats.setdefault(tok, set()).add(i)
    return tok2pats


def probe_record(kind, line, fp_lower):
    """Return (record_id, matched_field, excerpt) for a matching line."""
    rid, field, excerpt = None, "record", line[:EXCERPT_LEN]
    try:
        obj = json.loads(line)
    except Exception:
        obj = None
    if kind == "cdx" and isinstance(obj, dict):
        url = str(obj.get("url", ""))
        ts = str(obj.get("timestamp", ""))
        rid = f"{url}@{ts}" if url else f"line"
        if fp_lower in url.casefold():
            return rid, "url", url[:EXCERPT_LEN]
        return rid, "record", line[:EXCERPT_LEN]
    if isinstance(obj, dict):
        rid = obj.get("_id", "line")
        src = obj.get("_source", {}) if isinstance(obj.get("_source"), dict) else {}
        probes = []
        url = src.get("url")
        if isinstance(url, dict) and url.get("original"):
            probes.append(("url.original", str(url["original"])))
        labels = src.get("labels")
        if isinstance(labels, dict) and labels.get("label"):
            probes.append(("labels.label", str(labels["label"])))
        if src.get("download_url"):
            probes.append(("download_url", str(src["download_url"])))
        if src.get("gem"):
            probes.append(("gem", str(src["gem"])))
        for name, val in probes:
            if fp_lower in val.casefold():
                return rid, name, val[:EXCERPT_LEN]
    return rid, field, excerpt


def sweep_corpus(label, path, kind, patterns, fp_to_qids, fp_lower_list,
                 tok2pats, state):
    """Single-pass case-insensitive sweep of one corpus file. Returns counts."""
    per_fp_qid_counts = {}   # (qid, fp_idx) -> record count
    per_fp_qid_kept = {}     # (qid, fp_idx) -> rows kept
    hits_fh = HITS_PATH.open("a")
    lines = 0
    matched_lines = 0
    try:
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                lines += 1
                if not line.strip():
                    continue
                ll = line.casefold()
                # prefilter: candidate patterns sharing at least one token
                cand = set()
                for tok in set(TOKEN_RE.findall(ll)):
                    s = tok2pats.get(tok)
                    if s:
                        cand.update(s)
                if not cand:
                    continue
                matched = [i for i in cand if fp_lower_list[i] in ll]
                if not matched:
                    continue
                matched_lines += 1
                for i in matched:
                    fp = patterns[i]
                    for qid in fp_to_qids[i]:
                        key = (qid, i)
                        per_fp_qid_counts[key] = per_fp_qid_counts.get(key, 0) + 1
                        if per_fp_qid_kept.get(key, 0) < HITS_CAP_PER_KEY:
                            rid, field, excerpt = probe_record(kind, line, fp_lower_list[i])
                            hits_fh.write(json.dumps({
                                "qid": qid,
                                "fingerprint": fp,
                                "corpus": label,
                                "matched_field": field,
                                "excerpt": excerpt,
                                "record_id": rid,
                            }) + "\n")
                            per_fp_qid_kept[key] = per_fp_qid_kept.get(key, 0) + 1
    finally:
        hits_fh.close()

    # pattern-log rows for every (qid, fingerprint) tried against this corpus
    plog_fh = PLOG_PATH.open("a")
    try:
        for i, fp in enumerate(patterns):
            for qid in fp_to_qids[i]:
                plog_fh.write(json.dumps({
                    "qid": qid,
                    "fingerprint": fp,
                    "corpus": label,
                    "hits": per_fp_qid_counts.get((qid, i), 0),
                }) + "\n")
    finally:
        plog_fh.close()

    return lines, matched_lines, sum(per_fp_qid_kept.values())


def count_hits_file():
    if not HITS_PATH.exists():
        return 0
    return sum(1 for l in HITS_PATH.read_text().splitlines() if l.strip())


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    (LANE_DIR / "data").mkdir(parents=True, exist_ok=True)
    state = load_state()
    fp_rows = load_fingerprints()

    # ---- Phase 1: fingerprints ----
    questions = [json.loads(l) for l in QUESTIONS_PATH.read_text().splitlines()
                 if l.strip()]
    assert len(questions) == 900, f"expected 900 questions, got {len(questions)}"
    qids = [q["qid"] for q in questions]
    assert len(set(qids)) == 900, "duplicate qids"

    new_rows = 0
    with FP_PATH.open("a") as fh:
        for q in questions:
            if q["qid"] in fp_rows:
                continue
            fps = extract_fingerprints(q["question_text"])
            gov_priority = bool(set(q.get("tags", [])) & GOV_TAGS)
            if len(fps) < 1:
                row = {"qid": q["qid"], "fingerprints": fps, "skipped": True,
                       "reason": ("no distinctive fingerprints: no quoted phrases, "
                                  "parenthetical acronyms, dataset/agency names, domains, "
                                  "codes, or named entities found"),
                       "gov_priority": gov_priority, "tags": q.get("tags", [])}
            else:
                row = {"qid": q["qid"], "fingerprints": fps, "skipped": False,
                       "gov_priority": gov_priority, "tags": q.get("tags", [])}
            fh.write(json.dumps(row) + "\n")
            fp_rows[q["qid"]] = row
            new_rows += 1
    if new_rows:
        print(f"fingerprinted {new_rows} new questions")

    fingerprinted = [r for r in fp_rows.values() if not r["skipped"]]
    skipped = [r for r in fp_rows.values() if r["skipped"]]
    state["questions_fingerprinted"] = len(fingerprinted)
    state["questions_skipped"] = len(skipped)
    state["fingerprints_total"] = sum(len(r["fingerprints"]) for r in fingerprinted)

    # ---- Phase 2: patterns ----
    fp_to_qids_idx = {}   # fingerprint (original case) -> [qids]
    for r in fingerprinted:
        for fp in r["fingerprints"]:
            fp_to_qids_idx.setdefault(fp, []).append(r["qid"])
    patterns = sorted(fp_to_qids_idx.keys(), key=str.casefold)
    state["unique_patterns"] = len(patterns)
    PATTERNS_PATH.write_text("\n".join(patterns) + "\n")
    fp_to_qids = [sorted(set(fp_to_qids_idx[p])) for p in patterns]
    fp_lower_list = [p.casefold() for p in patterns]
    tok2pats = build_automaton_index(fp_lower_list)

    swept_labels = {c["label"] for c in state["corpora_swept"] if c.get("completed")}
    total_hits = count_hits_file()

    # ---- Phase 3: sweep each corpus ----
    for label, path, kind in corpus_specs():
        if not path.exists():
            print(f"WARNING: corpus file missing: {path} (skipped)")
            continue
        entry = next((c for c in state["corpora_swept"] if c["label"] == label), None)
        if entry and entry.get("completed"):
            continue
        if entry and not entry.get("completed"):
            purge_corpus_rows(label)  # interrupted earlier: re-sweep cleanly
            state["corpora_swept"] = [c for c in state["corpora_swept"]
                                      if c["label"] != label]
        print(f"sweeping {label} ...", flush=True)
        lines, matched_lines, kept = sweep_corpus(
            label, path, kind, patterns, fp_to_qids, fp_lower_list, tok2pats, state)
        state["corpora_swept"].append({
            "label": label,
            "file": str(path),
            "lines_scanned": lines,
            "lines_matched": matched_lines,
            "hits_staged": kept,
            "completed": True,
        })
        total_hits = count_hits_file()
        state["items_collected"] = total_hits
        save_state(state)
        print(f"  {label}: {lines} lines, {matched_lines} matched, {kept} staged")

    state["items_collected"] = count_hits_file()
    state["watermarks"] = [
        f"questions_sha256:{hashlib.sha256(QUESTIONS_PATH.read_bytes()).hexdigest()[:16]}",
        f"patterns:{len(patterns)}",
        f"corpora:{len([c for c in state['corpora_swept'] if c.get('completed')])}",
    ]
    if len(fp_rows) == 900 and all(
            c.get("completed") for c in state["corpora_swept"]):
        state["status"] = "complete"
    save_state(state)
    print(f"done: {len(fingerprinted)}/900 fingerprinted, "
          f"{len(skipped)} skipped, {len(patterns)} unique patterns, "
          f"{state['items_collected']} hits staged, status={state['status']}")


if __name__ == "__main__":
    main()
