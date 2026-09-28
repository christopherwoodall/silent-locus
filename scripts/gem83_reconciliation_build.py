#!/usr/bin/env python3
"""Lane E — 83-gem June-18 reconciliation build.

Reconstructs the 83-gem June-18 segment:
  81 gems by June-family grammar match against the JFrog inventory
      (data/gemstuffer-jfrog-2026-09-27.csv), plus
  2 random-suffix names cited in the thecolony.ai incident wiki
      (ultimate4834, method2088) — grammar-invisible.

Cross-references each name against:
  - JFrog inventory (versions, Xray ID)
  - Diffend corpus metadata (data/osv/diffend_sweep_results*.jsonl)
  - Wayback June metadata (data/gem-june18-wayback.jsonl)
  - collusion.wiki gem bridge (data/wiki_gem_bridge.json)

Outputs into data/gem83-reconciliation/:
  gem83-names.json, gem83-reconciliation.csv/.jsonl, pattern-sweep.txt,
  PROVENANCE.md
"""
import csv, json, os, re, hashlib
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = BASE + "/data"
OUT = DATA + "/gem83-reconciliation"
os.makedirs(OUT, exist_ok=True)

FAMS = {
    'proxy-4dash':   re.compile(r'^[a-z]----00proxy\d+$'),
    'prx-4dash':     re.compile(r'^[a-z]----00prx\d+$'),
    'cfjson-2dash':  re.compile(r'^[a-z]--00cfjson\d+$'),
    'cfmapjson-2dash': re.compile(r'^[a-z]--00cfmapjson\d+$'),
    'cfproxy-2dash': re.compile(r'^[a-z]--00cfproxy\d+$'),
    'cfproxy-4dash': re.compile(r'^[a-z]----00cfproxy\d+$'),
    'proxy-3dash':   re.compile(r'^[a-z]---00proxy\d+$'),
    'cfshape-3dash': re.compile(r'^[a-z]---00cfshape(s)?\d+$'),
    'amd-api':       re.compile(r'^amdapi\d+$'),
    'amd-var':       re.compile(r'^amdvar\d+$'),
    'amd-more':      re.compile(r'^amdmore\d+$'),
    'amd-hub':       re.compile(r'^amdwc\d+$'),
    'amd-bare':      re.compile(r'^amd\d+$'),
    'adep':          re.compile(r'^adep\d+$'),
    'mapanchor':     re.compile(r'^mapanchor[a-z0-9]+$'),
    'wctest':        re.compile(r'^wctest\d+$'),
}

# --- JFrog inventory -------------------------------------------------------
jfrog = {}
with open(DATA + "/gemstuffer-jfrog-2026-09-27.csv") as f:
    for r in csv.DictReader(f):
        jfrog[r['Package']] = {'versions': r['Versions'], 'xray_id': r['Xray ID']}

june, source = [], {}
for n in jfrog:
    for fam, pat in FAMS.items():
        if pat.match(n):
            june.append(n); source[n] = f"grammar:family={fam}"
            break
for n in ['ultimate4834', 'method2088']:
    assert n in jfrog, n
    june.append(n); source[n] = "incident-wiki-citation:random-suffix"
june = sorted(set(june))
assert len(june) == 83, f"expected 83, got {len(june)}"

# --- Diffend corpus ---------------------------------------------------------
diffend_names = set()
for fn in ['diffend_sweep_results.jsonl', 'diffend_sweep_results_retry.jsonl']:
    try:
        with open(DATA + "/osv/" + fn) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                d = json.loads(line)
                if d.get('name'):
                    diffend_names.add(d['name'])
    except FileNotFoundError:
        pass

# --- Wayback June metadata ---------------------------------------------------
wayback = {}
with open(DATA + "/gem-june18-wayback.jsonl") as f:
    for line in f:
        line = line.strip()
        if line:
            d = json.loads(line)
            wayback[d['gem']] = d

# --- collusion.wiki gem bridge -----------------------------------------------
bridge = {}
try:
    b = json.load(open(DATA + "/wiki_gem_bridge.json"))
    for rec in b.get('gem_metadata_records', []):
        bridge[rec['gem']] = rec.get('meta', {})
except FileNotFoundError:
    pass

# --- rows ---------------------------------------------------------------------
rows = []
for n in june:
    fam = next(f for f, p in FAMS.items() if p.match(n)) if source[n].startswith('grammar') else 'random-suffix'
    meta = bridge.get(n, {})
    rows.append({
        'gem': n,
        'name_family': fam,
        'identification_source': source[n],
        'in_jfrog': True,
        'jfrog_versions': jfrog[n]['versions'],
        'jfrog_xray_id': jfrog[n]['xray_id'],
        'in_diffend_corpus': n in diffend_names,
        'in_wayback_june_metadata': n in wayback,
        'wayback_recovery_status': wayback.get(n, {}).get('recovery_status'),
        'in_wiki_gem_bridge': n in bridge,
        'wiki_bridge_homepage_uri': meta.get('homepage_uri'),
        'wiki_bridge_info': meta.get('info'),
        'wave_inference': 'june-18',
    })

# --- outputs ------------------------------------------------------------------
with open(OUT + "/gem83-names.json", "w") as f:
    json.dump([{'gem': n, 'source': source[n]} for n in june], f, indent=1)

with open(OUT + "/gem83-reconciliation.jsonl", "w") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")

with open(OUT + "/gem83-reconciliation.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# pattern sweep
lines = []
lines.append("LANE E — 83-gem June-18 name-grammar pattern sweep")
lines.append(f"Names analyzed: {len(june)}")
fc = Counter(r['name_family'] for r in rows)
lines.append("\nFamily counts:")
for fam, c in fc.most_common():
    lines.append(f"  {fam:16s} {c}")
lines.append("\n--- Grammar notes ---")
lines.append("- Dash padding varies by family: 4-dash (----) on proxy/prx/cfproxy,")
lines.append("  2-dash (--) on cfjson/cfmapjson, 3-dash (---) on proxy/cfshape.")
lines.append("- All numeric suffixes are short (2-6 digits): 726, 57431, 90485, 56692.")
lines.append("  NO epoch-style suffixes (10-digit 17xxxx/18xxxx) in this segment —")
lines.append("  unlike the May corpus (epoch_suffix grammar common there).")
lines.append("- The '00' infix is the fixed family token: 00proxy / 00prx / 00cfjson /")
lines.append("  00cfmapjson / 00cfproxy / 00cfshape. May corpus prx* names (prx1b49033905)")
lines.append("  lack the 00 infix and the dash padding — grammar distinguishes waves.")
lines.append("- Literal proxy names inside names: only the token 'proxy' itself.")
lines.append("- amdwc* (hub family) are the shortest machine names: amdwc51950, amdwc56692.")
lines.append("- The two random-suffix names (ultimate4834, method2088) are grammar-invisible;")
lines.append("  identified by direct citation in the incident wiki.")
lines.append("\nHub-and-spoke (as reported by thecolony.ai centaur post, NOT independently verified):")
lines.append("- Hub: amdwc56692 (present in JFrog inventory, XRAY-1077977, 0.0.1).")
lines.append("- Spokes per centaur: amdwc51950 v0.0.2 and wctest73410 declare a runtime")
lines.append("  dependency on amdwc56692.")
lines.append("- JFrog corroboration: amdwc51950 Versions='0.0.1;0.0.2' (only multi-version gem")
lines.append("  in the 83) — matches centaur's 'v0.0.2' claim exactly. wctest73410 present")
lines.append("  (XRAY-1079154). Dependency edges themselves have no tool evidence available:")
lines.append("  no gemspec contents for these gems in Diffend, JFrog CSV, or the wiki bridge.")
open(OUT + "/pattern-sweep.txt", "w").write("\n".join(lines) + "\n")

prov = """# PROVENANCE — gem83-reconciliation (Lane E)

Built 2026-09-27/28 (UTC) by subagent lane E. Reconstructs the 83-gem June-18
segment independently cross-referenced against three project sources.

## Inputs

1. `../gemstuffer-jfrog-2026-09-27.csv` — JFrog GemStuffer inventory
   (3,025 rows), saved 2026-09-27 from https://research.jfrog.com/gemstuffer.csv.
2. thecolony.ai incident wiki + centaur's "83 pointer-gems" post
   (`../thecolony-ai/`, see notes/thecolony-ai-ingest-2026-09-27.md):
   83 gems, account ulinkqy8py3mp, 2026-06-18 17:53-20:52 UTC, ~38.9k downloads,
   hub-and-spoke around amdwc56692 (amdwc51950 v0.0.2 and wctest73410 as spokes).
3. JFrog Security Research report: June 18 = 83 packages (full window table).
   https://research.jfrog.com/post/gemstuffer-openai-rubygems/
4. `../osv/diffend_sweep_results*.jsonl` — our Diffend corpus name list.
5. `../gem-june18-wayback.jsonl` — 16 June Wayback metadata records.
6. `../wiki_gem_bridge.json` — collusion.wiki explorer gem metadata (2026-09-28).

## Method

81 names = regex family-grammar match over the JFrog inventory (families from
centaur's post + incident wiki examples: `[a-z]----00proxyNNN`, `amdapi|amdvar|
amdmore|amdwc|amd`, `[a-z]--00cfjsonNNN`, `[a-z]--00cfmapjsonNNN`,
`[a-z]--/----00cfproxyNNN`, `[a-z]---00proxyNN`, `[a-z]---00cfshape(s)NNNNN`,
`[a-z]----00prxNNNNN`, `adepNNNNN`, `mapanchor*`, `wctest73410`).
2 names = direct incident-wiki citation (random-suffix: ultimate4834, method2088).
Exact duplicates were collapsed; no other de-dup. The June-18 date is
inferred from grammar + external reports — the JFrog CSV carries no per-row dates.

## Limitations

- This is a grammar reconstruction, not the owner-API manifest (that API now
  returns [] — all 83 yanked). The 83 count matches JFrog's published June-18
  count exactly.
- Dependency edges (hub-and-spoke) are centaur-reported; no gemspec content
  exists in any project source to verify them. Only corroborating fact:
  JFrog lists amdwc51950 with versions '0.0.1;0.0.2' — the sole multi-version
  gem in the 83 — matching centaur's 'v0.0.2' claim.
- Read-only; no package fetched, no code executed, no identity pursued.
"""
open(OUT + "/PROVENANCE.md", "w").write(prov)

# sha256 manifest
man = []
for fn in sorted(os.listdir(OUT)):
    if fn == "manifest.txt":
        continue
    h = hashlib.sha256(open(OUT + "/" + fn, "rb").read()).hexdigest()
    man.append(f"{h}  {fn}")
open(OUT + "/manifest.txt", "w").write("\n".join(man) + "\n")
print("built", len(june), "names;", OUT)
