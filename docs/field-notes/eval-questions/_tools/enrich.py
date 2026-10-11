#!/usr/bin/env python3
"""W3-ENRICHMENT for EVALHUNT: enrich banked eval questions.

Reads  questions.jsonl + raw/ for the 11 W2-banked evals (never modifies them)
and writes:
  <eval-slug>/questions-enriched.jsonl   per-eval enriched copy (provenance)
  all-questions.jsonl                    unified query-ready corpus

Enriched schema per line:
  {"eval","eval_org","question_id","question","topic",
   "expected_sources":[{"domain_or_url","why"}],
   "fingerprint_phrases":[...],"license","retrieved"}

why values: "metadata" | "named-in-question" | "prior" | "selfhosted"
            | "synthetic-policy-no-live-web" | "context-provided-no-web-needed"
            | "no-metadata-no-prior"
The last three are marker entries with domain_or_url == "" recording WHY the
source list is empty (tau-bench synthetic policy; facts-grounding ships its own
context doc; no mineable metadata and no justified prior).

stdlib only.
"""
import ast
import csv
import glob
import json
import os
import random
import re
import sys
from collections import Counter
from urllib.parse import urlparse

ROOT = os.path.expanduser('~/workspace/silent-locus/collections/eval-questions')
sys.path.insert(0, os.path.join(ROOT, '_tools'))

EVALS = ['openai-simpleqa', 'google-facts-grounding', 'google-frames',
         'assistantbench', 'mind2web', 'webvoyager', 'webarena', 'tau-bench',
         'sealqa', 'webwalkerqa', 'openai-mle-bench']

SOURCE_URL = {
    'openai-simpleqa': 'https://openaipublic.blob.core.windows.net/simple-evals/simple_qa_test_set.csv',
    'google-facts-grounding': 'https://huggingface.co/datasets/google/FACTS-grounding-public/resolve/main/examples.csv',
    'google-frames': 'https://huggingface.co/datasets/google/frames-benchmark/resolve/main/test.tsv',
    'assistantbench': 'https://huggingface.co/datasets/AssistantBench/AssistantBench/resolve/main/assistant_bench_v1.0_test.jsonl',
    'mind2web': 'https://huggingface.co/datasets/osunlp/Mind2Web/resolve/main/data/train/train_{0..10}.json',
    'webvoyager': 'https://raw.githubusercontent.com/MinorJerry/WebVoyager/main/data/WebVoyager_data.jsonl',
    'webarena': 'https://raw.githubusercontent.com/web-arena-x/webarena/main/config_files/test.raw.json',
    'tau-bench': 'https://github.com/sierra-research/tau-bench',
    'sealqa': 'https://huggingface.co/datasets/vtllms/sealqa',
    'webwalkerqa': 'https://huggingface.co/datasets/callanwu/WebWalkerQA/resolve/main/data/main-00000-of-00001.jsonl',
    'openai-mle-bench': 'https://github.com/openai/mle-bench',
}

# ---------------------------------------------------------------- metadata maps

def load_simpleqa_urls():
    out = []
    with open(f'{ROOT}/openai-simpleqa/raw/simple_qa_test_set.csv', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            md = ast.literal_eval(row['metadata'])
            out.append(md.get('urls') or [])
    return out

def load_frames_links():
    out = []
    with open(f'{ROOT}/google-frames/raw/test.tsv', encoding='utf-8') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            try:
                out.append(ast.literal_eval(row['wiki_links']))
            except Exception:
                out.append([])
    return out

def load_mind2web_websites():
    pat = re.compile(r'\{"website": "([^"]+)", "domain": "[^"]*", '
                     r'"subdomain": "[^"]*", "annotation_id": "([^"]+)"')
    m = {}
    for fp in sorted(glob.glob(f'{ROOT}/mind2web/raw/train_*.json')):
        with open(fp, encoding='utf-8') as f:
            for w, aid in pat.findall(f.read()):
                m[aid] = w
    return m

def load_webvoyager_webs():
    m = {}
    with open(f'{ROOT}/webvoyager/raw/WebVoyager_data.jsonl', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            m[d['id']] = d['web']
    return m

def load_webwalkerqa_meta():
    out = []
    with open(f'{ROOT}/webwalkerqa/raw/main-00000-of-00001.jsonl', encoding='utf-8') as f:
        for line in f:
            d = json.loads(line)
            out.append((d.get('root_url', ''), d.get('info') or {}))
    return out

def load_sealqa_urls():
    from pqdec import decode_column
    out = {}
    for split, fn in [('seal-0', 'seal-0.parquet'),
                      ('seal-hard', 'seal-hard.parquet'),
                      ('longseal', 'longseal.parquet')]:
        rows = decode_column(f'{ROOT}/sealqa/raw/{fn}', ('urls', 'list', 'element'))
        out[split] = [[b.decode('utf-8', 'replace') for b in r] for r in rows]
    return out

# ---------------------------------------------------------------- topics

SIMPLEQA_TOPIC = {'Science and technology': 'science', 'Geography': 'geography',
                  'Sports': 'sports', 'Art': 'entertainment', 'Politics': 'politics',
                  'Other': 'other', 'TV shows': 'entertainment', 'Music': 'entertainment',
                  'History': 'history', 'Video games': 'entertainment'}
SEALQA_TOPIC = {'Entertainment': 'entertainment', 'Sports': 'sports',
                'Science & Technology': 'science', 'Others': 'other',
                'Politics': 'politics', 'History & Geography': 'history'}
MIND2WEB_TOPIC = {'Restaurant': 'food', 'Car rental': 'travel', 'Department': 'shopping',
                  'Airlines': 'travel', 'Fashion': 'shopping', 'Movie': 'entertainment',
                  'Other': 'other', 'Ground': 'travel', 'General': 'other', 'Auto': 'other',
                  'Music': 'entertainment', 'Event': 'entertainment', 'Speciality': 'shopping',
                  'Digital': 'tech', 'Game': 'entertainment', 'Hotel': 'travel', 'Sports': 'sports'}
WWQ_DOMAIN = {'education': 'education', 'game': 'entertainment',
               'conference': 'other', 'organization': 'other'}

KW_RULES = [
    ('politics', [r'\bpresident\b', r'\belection\b', r'\bsenator\b', r'\bcongress\b',
                  r'\bparliament\b', r'\bprime minister\b', r'\bcampaign\b', r'\bdemocra(ts|cy|tic)\b',
                  r'\brepublicans?\b', r'\bwhite house\b', r'\bgovernor\b', r'\bmayor\b',
                  r'\breferendum\b', r'\bballot\b', r'\bimpeach', r'\bcoup\b', r'\bdictator\w*\b']),
    ('gov-policy', [r'\blegislation\b', r'\bamendment\b', r'\bconstitution\w*\b',
                    r'\bsupreme court\b', r'\bregulation\b', r'\bgovernment\b', r'\btariff\b',
                    r'\bsanction\b', r'\bimmigration\b', r'\bcourt\b', r'\bfcc\b', r'\bepa\b']),
    ('health', [r'\bdisease\b', r'\bcancer\b', r'\bcovid\b', r'\bvaccine\b', r'\bdoctor\b',
                r'\bhospital\b', r'\bfda\b', r'\bhealth\b', r'\bsymptom\w*\b', r'\btreatment\b',
                r'\bsurgery\b', r'\bvirus\b', r'\bpandemic\b', r'\bmental health\b', r'\bdiabetes\b',
                r'\bdementia\b', r'\brisk factor\w*\b', r'\balzheimer\w*\b', r'\bdepress\w*\b',
                r'\bobes\w*\b', r'\bsmok\w*\b', r'\bcholesterol\b', r'\bblood pressure\b',
                r'\bpsycholog\w*\b', r'\btherap\w*\b']),
    ('finance', [r'\bstock\b', r'\bmarket cap\b', r'\brevenue\b', r'\bceo\b', r'\bipo\b',
                 r'\bbitcoin\b', r'\bcrypto\w*\b', r'\binvestment\b', r'\bbillion\b',
                 r'\btrillion\b', r'\bfortune 500\b', r'\bnasdaq\b', r'\bhedge fund\b',
                 r'\bacquisition\b', r'\bbankrupt\w*\b', r'\bshares\b']),
    ('science', [r'\bspecies\b', r'\bmolecule\w*\b', r'\bprotein\b', r'\bquantum\b', r'\bdna\b',
                 r'\bgenome\b', r'\bnasa\b', r'\bexperiment\b', r'\bplanet\b', r'\bgalaxy\b',
                 r'\bphysics\b', r'\bchemistry\b', r'\bbiology\b', r'\bfossil\b', r'\bdinosaur\b',
                 r'\btelescope\b', r'\bparticle\b', r'\bevolution\b', r'\bclimate\b',
                 r'\batom\w*\b', r'\bneuron\w*\b', r'\bscientist\b']),
    ('history', [r'\bworld war\b', r'\bempire\b', r'\bancient\b', r'\bmedieval\b',
                 r'\brevolution\b', r'\btreaty\b', r'\bbattle\b', r'\bcivil war\b', r'\bcentury\b',
                 r'\bdynasty\b', r'\bcolony\b', r'\bindependence\b', r'\bpharaoh\b']),
    ('geography', [r'\bcountry\b', r'\bcapital\b', r'\briver\b', r'\bmountain\b', r'\bisland\b',
                   r'\bpopulation\b', r'\bborder\b', r'\bcontinent\b', r'\bocean\b',
                   r'\blake\b', r'\bdesert\b', r'\blatitude\b', r'\blongitude\b',
                   r'\bcit(y|ies)\b', r'\beurope\b', r'\basia\b', r'\bafrica\b']),
    ('sports', [r'\bnfl\b', r'\bnba\b', r'\bmlb\b', r'\bnhl\b', r'\bfifa\b', r'\bolympic\w*\b',
                r'\bsuper bowl\b', r'\bworld cup\b', r'\bpremier league\b', r'\bchampions league\b',
                r'\bwimbledon\b', r'\bgrand slam\b', r'\bnascar\b', r'\bformula 1\b',
                r'\btennis\b', r'\bsoccer\b', r'\bquarterback\b', r'\bplayoff\w*\b',
                r'\bchampionship\b', r'\btournament\b', r'\bmedal\b', r'\bbasketball\b',
                r'\bbaseball\b', r'\brugby\b', r'\bcricket\b', r'\bsport\b']),
    ('entertainment', [r'\bmovies?\b', r'\bfilms?\b', r'\bactor\b', r'\bactress\b', r'\boscar\w*\b',
                       r'\bgrammy\w*\b', r'\balbums?\b', r'\bsongs?\b', r'\bnetflix\b',
                       r'\bepisodes?\b', r'\btv series\b', r'\btv shows?\b', r'\bband\b',
                       r'\bconcert\b', r'\bvideo games?\b', r'\bgaming\b', r'\bhollywood\b',
                       r'\bcelebrity\b', r'\bnovels?\b', r'\bauthor\b', r'\bpodcasts?\b',
                       r'\bnintendo\b', r'\bplaystation\b', r'\bxbox\b', r'\binstagram\b',
                       r'\btiktok\b', r'\byoutube\b', r'\btwitter\b', r'\bcomics?\b',
                       r'\banime\b']),
    ('tech', [r'\bsoftware\b', r'\bartificial intelligence\b', r'\bcomputer\b', r'\biphone\b',
               r'\bandroid\b', r'\bmicrosoft\b', r'\bstartup\b', r'\balgorithm\b',
               r'\binternet\b', r'\bprogrammer\b', r'\bopenai\b', r'\brobot\w*\b',
               r'\bsemiconductor\b', r'\bdata center\b', r'\bmachine learning\b',
               r'\bsocial media\b', r'\bsmartphone\b']),
    ('food', [r'\brecipe\b', r'\brestaurant\b', r'\bmenu\b', r'\bcuisine\b', r'\bcooking\b',
               r'\bbaking\b', r'\bdish\b', r'\bingredient\b', r'\bchef\b']),
    ('travel', [r'\bflight\b', r'\bhotel\b', r'\bairline\b', r'\bairport\b',
                r'\bvacation\b', r'\bitinerary\b', r'\bcruise\b', r'\brental car\b']),
    ('shopping', [r'\bprice\b', r'\bproduct\b', r'\bcart\b', r'\bcheckout\b', r'\bdiscount\b',
                   r'\bdelivery\b', r'\bwarranty\b', r'\bshopping\b']),
]
KW_COMPILED = [(lab, [re.compile(p, re.I) for p in pats]) for lab, pats in KW_RULES]

# CJK keyword rules (substring match; checked first when CJK chars present).
# 433 webwalkerqa + 2 simpleqa questions are Chinese.
CJK_RULES = [
    ('politics', ['总统', '选举', '投票', '政府', '国会', '议会', '市长', '公投']),
    ('gov-policy', ['法律', '法规', '法院', '政策', '税收', '宪法']),
    ('health', ['健康', '疾病', '癌症', '疫苗', '医院', '医生', '药物', '新冠', '心理']),
    ('finance', ['股票', '投资', '银行', '经济', '收入', '利润']),
    ('science', ['科学', '生物', '物理', '化学', '基因', '实验', '气候', '恐龙', '化石']),
    ('history', ['历史', '朝代', '战争', '古代', '帝国', '革命']),
    ('geography', ['地理', '国家', '首都', '城市', '河流', '山脉', '岛屿', '人口', '欧洲', '亚洲']),
    ('sports', ['体育', '足球', '篮球', '奥运', '网球', '比赛', '冠军']),
    ('entertainment', ['电影', '音乐', '游戏', '电视剧', '演员', '歌手', '小说']),
    ('tech', ['软件', '计算机', '人工智能', '互联网', '手机', '算法']),
    ('food', ['菜谱', '餐厅', '美食', '烹饪']),
    ('travel', ['旅游', '航班', '酒店', '旅行', '签证']),
    ('shopping', ['价格', '购物', '产品', '商店']),
    ('education', ['大学', '学院', '学校', '教育', '培训', '讲座', '学者']),
]

def classify_topic(text):
    if CJK_RE.search(text):
        for label, kws in CJK_RULES:
            for kw in kws:
                if kw in text:
                    return label
    tl = text.lower()
    for label, pats in KW_COMPILED:
        for p in pats:
            if p.search(tl):
                return label
    return 'other'

# ---------------------------------------------------------------- expected sources

URL_RE = re.compile(r'https?://[^\s)\]"\'>]+')
BARE_RE = re.compile(
    r'\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+'
    r'(?:com|org|net|gov|edu|io|ai|co|uk|de|fr|info|biz|us|tv|me|app|dev|fm|int|mil|ca|au|in|jp|cn)\b',
    re.I)

def extract_from_text(text):
    urls = [m.group(0).rstrip('.,;:!?') for m in URL_RE.finditer(text)]
    tmp = URL_RE.sub(' ', text)
    doms = [m.group(0).lower() for m in BARE_RE.finditer(tmp)]
    # drop bare hits that are email addresses
    doms = [d for d in doms
            if not re.search(r'@' + re.escape(d) + r'\b', tmp, re.I)]
    return urls, doms

def domain_of(s):
    s = (s or '').strip()
    if not s or s.startswith('selfhosted:'):
        return s
    if '://' in s:
        try:
            net = urlparse(s).netloc.lower()
        except Exception:
            net = ''
        if net.startswith('www.'):
            net = net[4:]
        return net or s
    return s.lower()

BRANDS = [
    ('apple', 'apple.com'), ('tesla', 'tesla.com'), ('amazon', 'amazon.com'),
    ('google', 'google.com'), ('microsoft', 'microsoft.com'), ('netflix', 'netflix.com'),
    ('spotify', 'spotify.com'), ('nfl', 'nfl.com'), ('nba', 'nba.com'), ('mlb', 'mlb.com'),
    ('nhl', 'nhl.com'), ('fifa', 'fifa.com'), ('nasa', 'nasa.gov'), ('cdc', 'cdc.gov'),
    ('fda', 'fda.gov'), ('white house', 'whitehouse.gov'),
    ('supreme court', 'supremecourt.gov'), ('united nations', 'un.org'),
    ('imdb', 'imdb.com'), ('github', 'github.com'), ('wikipedia', 'en.wikipedia.org'),
]
QA_EVALS = {'openai-simpleqa', 'sealqa', 'google-frames', 'webwalkerqa',
            'google-facts-grounding', 'assistantbench'}
WH_RE = re.compile(r'^(who|whom|whose|what|which|when|where|how many|how much|'
                   r'how long|how old|how far|name|list|identify)\b', re.I)

M2W_SPECIAL = {'nyc': 'nyc.gov'}
KNOWN_TLDS = {'com', 'org', 'net', 'gov', 'edu', 'io', 'ai', 'co', 'uk', 'de', 'fr',
              'info', 'biz', 'us', 'tv', 'me', 'app', 'dev', 'fm', 'int', 'mil', 'ca',
              'au', 'in', 'jp', 'cn', 'nz', 'ie', 'nl', 'se', 'es', 'it', 'ch', 'at',
              'be', 'br', 'mx', 'kr', 'za', 'sg', 'hk', 'tw', 'pt', 'pl', 'no', 'dk', 'fi'}

def m2w_domain(w):
    w = w.strip().lower()
    if w in M2W_SPECIAL:
        return M2W_SPECIAL[w]
    if '.' not in w:
        return w + '.com'
    if w.rsplit('.', 1)[1] not in KNOWN_TLDS:
        return w + '.com'
    return w

def assemble_sources(eval_slug, meta_urls, question):
    """Return list of {domain_or_url, why}, 2-5 entries or a single why-marker."""
    entries, seen_dom, seen_url = [], set(), set()

    def add(val, why):
        if not val or len(entries) >= 5:
            return
        d = domain_of(val)
        if not d:
            return
        if why == 'metadata':
            # keep distinct article URLs even on one domain (trace gold)
            if val in seen_url:
                return
            seen_url.add(val)
            seen_dom.add(d)
        else:
            if d in seen_dom:
                return
            seen_dom.add(d)
        entries.append({'domain_or_url': val, 'why': why})

    for u in meta_urls or []:          # metadata first, deduped by domain
        if len(entries) >= 3:
            break
        add(u, 'metadata')
    text_urls, text_doms = extract_from_text(question)
    for u in text_urls:
        add(u, 'named-in-question')
    if eval_slug in QA_EVALS:
        for bd in text_doms:
            add(bd, 'named-in-question')
        ql = question.lower()
        for phrase, dom in BRANDS:
            if len(entries) >= 5:
                break
            if re.search(r'\b' + re.escape(phrase) + r'\b', ql):
                add(dom, 'prior')
        if not entries and WH_RE.match(question.strip()):
            add('en.wikipedia.org', 'prior')
    if eval_slug == 'openai-mle-bench' and 'kaggle.com' not in seen_dom:
        add('kaggle.com', 'prior')
    if not entries:
        if eval_slug == 'tau-bench':
            entries = [{'domain_or_url': '', 'why': 'synthetic-policy-no-live-web'}]
        elif eval_slug == 'google-facts-grounding':
            entries = [{'domain_or_url': '', 'why': 'context-provided-no-web-needed'}]
        elif eval_slug == 'webarena':
            entries = [{'domain_or_url': '', 'why': 'selfhosted-unknown'}]
        else:
            entries = [{'domain_or_url': '', 'why': 'no-metadata-no-prior'}]
    return entries

# ---------------------------------------------------------------- fingerprints

STOPWORDS = set("""a an the of in on to is are was were be been being will would
could should shall may might must can do does did done has have had having it its
this that these those they them their he she his her him we our you your i me my
us as at by for for from with about into over under between through during
before after above below up down out off again once here there where when why
how what which who whom whose whether while nor or and not no if then than so
such very just only also even ever never always often much many more most other
some any all both each few own same too s t ll re ve don isn aren wasn weren
doesn didn hasn haven hadn couldn wouldn shouldn won won't can't cannot per via
vs etc eg ie within without across toward towards among per""".split())

TOK_RE = re.compile(r'[a-z0-9]+|[\u4e00-\u9fff]')
CJK_RE = re.compile(r'[\u4e00-\u9fff]')
YEAR_RE = re.compile(r'^\d{4}$')

def tokenize(text):
    return TOK_RE.findall(text.lower())

def _is_weak(t):
    # CJK chars carry meaning individually -> content, never weak
    if CJK_RE.fullmatch(t):
        return False
    return t in STOPWORDS or len(t) <= 2

def _is_content(t):
    if CJK_RE.fullmatch(t):
        return True
    return len(t) >= 4 and t not in STOPWORDS

def ngram_ok(ng):
    if ng[0] in STOPWORDS:
        return False
    weak = 0
    content = 0
    for t in ng:
        if 'http' in t or 'www' in t or '_' in t:
            return False
        if any(c.isdigit() for c in t):
            if not (YEAR_RE.match(t) and 1800 <= int(t) <= 2099):
                return False
        if _is_weak(t):
            weak += 1
        if _is_content(t):
            content += 1
    if weak > len(ng) / 2:
        return False
    if content < 1:
        return False
    if len(ng) >= 6 and content < 2:
        return False
    return True

def build_df(all_tokens):
    df = Counter()
    for toks in all_tokens:
        seen = set()
        L = len(toks)
        for n in range(4, 9):
            for i in range(L - n + 1):
                seen.add(' '.join(toks[i:i + n]))
        df.update(seen)
    return df

def detok(tokens):
    """Rejoin tokens for verbatim search: no spaces inside CJK runs."""
    out = []
    for t in tokens:
        if out and not CJK_RE.fullmatch(t) and not CJK_RE.fullmatch(out[-1]):
            out.append(' ')
        out.append(t)
    return ''.join(out)

def pick_fingerprints(tokens, df, want=3):
    cands = []
    L = len(tokens)
    for n in range(4, 9):
        for i in range(L - n + 1):
            ng = tokens[i:i + n]
            if not ngram_ok(ng):
                continue
            key = ' '.join(ng)
            cands.append((df.get(key, 1), -n, i, key))
    cands.sort()
    picked, used = [], [False] * L
    for _, negn, i, key in cands:
        n = -negn
        if any(used[i:i + n]):
            continue
        picked.append(detok(tokens[i:i + n]))
        for j in range(i, i + n):
            used[j] = True
        if len(picked) >= want:
            break
    if len(picked) < 2:  # relax overlap to reach 2
        seen_ph = set(picked)
        for _, negn, i, key in cands:
            n = -negn
            ph = detok(tokens[i:i + n])
            if ph not in seen_ph:
                picked.append(ph)
                seen_ph.add(ph)
            if len(picked) >= 2:
                break
    if not picked and L:  # last resort
        picked = [detok(tokens[:min(8, L)])]
    return picked[:4]

# ---------------------------------------------------------------- main

def main():
    print('loading banked questions...', flush=True)
    banked = {}
    for ev in EVALS:
        recs = []
        with open(f'{ROOT}/{ev}/questions.jsonl', encoding='utf-8') as f:
            for line in f:
                recs.append(json.loads(line))
        banked[ev] = recs
        print(f'  {ev}: {len(recs)}', flush=True)

    print('loading metadata lookups...', flush=True)
    simpleqa_urls = load_simpleqa_urls();      print('  simpleqa urls ok', flush=True)
    frames_links = load_frames_links();        print('  frames links ok', flush=True)
    m2w_sites = load_mind2web_websites();      print(f'  mind2web sites ok ({len(m2w_sites)})', flush=True)
    voy_webs = load_webvoyager_webs();         print('  webvoyager webs ok', flush=True)
    wwq_meta = load_webwalkerqa_meta();        print('  webwalkerqa meta ok', flush=True)
    sealqa_urls = load_sealqa_urls();          print('  sealqa urls ok', flush=True)

    # ---- corpus-wide n-gram document frequency
    # (URLs stripped before tokenizing: chopped URL tokens make bad verbatim phrases)
    print('tokenizing corpus...', flush=True)
    order = [(ev, i, rec) for ev in EVALS for i, rec in enumerate(banked[ev])]
    all_tokens = [tokenize(URL_RE.sub(' ', rec['question'])) for _, _, rec in order]
    print('building n-gram df (4..8)...', flush=True)
    df = build_df(all_tokens)
    print(f'  unique n-grams: {len(df)}', flush=True)

    enriched = {ev: [] for ev in EVALS}
    for (ev, i, rec), toks in zip(order, all_tokens):
        q = rec['question']
        # topic
        if ev == 'openai-simpleqa':
            topic = SIMPLEQA_TOPIC.get(rec['topic'], 'other')
        elif ev == 'sealqa':
            topic = SEALQA_TOPIC.get(rec['topic'], 'other')
        elif ev == 'mind2web':
            topic = MIND2WEB_TOPIC.get(rec['topic'], 'other')
            if topic == 'other':  # metadata 'Other'/'General' -> keyword fallback
                topic = classify_topic(q)
        elif ev == 'tau-bench':
            topic = rec['topic']
        elif ev == 'webvoyager':
            topic = rec['topic']
        elif ev == 'webwalkerqa':
            topic = classify_topic(q)
            if topic == 'other':
                topic = WWQ_DOMAIN.get(wwq_meta[i][1].get('domain', ''), 'other')
        elif ev == 'openai-mle-bench':
            # classify on the competition slug (descriptions are long + boilerplate-heavy)
            topic = classify_topic(rec['question_id'].replace('-', ' '))
            if topic == 'other':
                topic = 'tech'
        else:
            topic = classify_topic(q)
        # expected sources
        if ev == 'openai-simpleqa':
            meta_urls = simpleqa_urls[i]
        elif ev == 'google-frames':
            meta_urls = frames_links[i]
        elif ev == 'mind2web':
            w = m2w_sites.get(rec['question_id'], '')
            meta_urls = [m2w_domain(w)] if w else []
        elif ev == 'webvoyager':
            meta_urls = [voy_webs.get(rec['question_id'], '')]
        elif ev == 'webwalkerqa':
            root_url, info = wwq_meta[i]
            meta_urls = ([root_url] if root_url else []) + (info.get('source_website') or [])
        elif ev == 'sealqa':
            split, idx = rec['question_id'].rsplit('-', 1)
            meta_urls = sealqa_urls[split][int(idx)]
        elif ev == 'webarena':
            sites = [s.strip() for s in rec['topic'].split(',') if s.strip()]
            entries = [{'domain_or_url': f'selfhosted:{s}', 'why': 'selfhosted'}
                       for s in sites[:5]]
            if not entries:
                entries = [{'domain_or_url': '', 'why': 'selfhosted-unknown'}]
            meta_urls = None  # handled below
        elif ev == 'tau-bench':
            meta_urls = None  # marker path
        else:
            meta_urls = []
        if ev == 'webarena':
            sources = entries
        elif ev == 'tau-bench':
            sources = [{'domain_or_url': '', 'why': 'synthetic-policy-no-live-web'}]
        else:
            sources = assemble_sources(ev, meta_urls, q)
        # fingerprints
        fps = pick_fingerprints(toks, df)
        enriched[ev].append({
            'eval': rec['eval'], 'eval_org': rec['eval_org'],
            'question_id': rec['question_id'], 'question': q, 'topic': topic,
            'expected_sources': sources, 'fingerprint_phrases': fps,
            'license': rec['license'], 'retrieved': rec['retrieved'],
        })

    # ---- schema validation
    print('validating...', flush=True)
    total = 0
    marker_counts = Counter()
    for ev in EVALS:
        for r in enriched[ev]:
            total += 1
            assert set(r) == {'eval', 'eval_org', 'question_id', 'question', 'topic',
                              'expected_sources', 'fingerprint_phrases', 'license',
                              'retrieved'}, r['question_id']
            assert r['question'] and r['question'].strip(), r['question_id']
            assert len(r['fingerprint_phrases']) >= 1, r['question_id']
            assert isinstance(r['expected_sources'], list)
            for s in r['expected_sources']:
                assert set(s) == {'domain_or_url', 'why'}, r['question_id']
                if s['domain_or_url'] == '':
                    marker_counts[(ev, s['why'])] += 1
    assert total == 10201, total
    print(f'  total records: {total} (expected 10201)', flush=True)
    print(f'  marker entries: {dict(marker_counts)}', flush=True)

    # ---- write per-eval enriched + unified
    print('writing outputs...', flush=True)
    with open(f'{ROOT}/all-questions.jsonl', 'w', encoding='utf-8') as out:
        for ev in EVALS:
            ep = f'{ROOT}/{ev}/questions-enriched.jsonl'
            with open(ep, 'w', encoding='utf-8') as f:
                for r in enriched[ev]:
                    line = json.dumps(r, ensure_ascii=False)
                    f.write(line + '\n')
                    out.write(line + '\n')
            print(f'  {ev}/questions-enriched.jsonl: {len(enriched[ev])}', flush=True)
    print('  all-questions.jsonl written', flush=True)

    # ---- spot-check 20 random records for eyeballing
    random.seed(20261005)
    flat = [r for ev in EVALS for r in enriched[ev]]
    print('\n--- SPOT CHECK (20 random records) ---', flush=True)
    for r in random.sample(flat, 20):
        print(f"[{r['eval']}/{r['question_id']}] topic={r['topic']}", flush=True)
        print(f"  Q: {r['question'][:160]}", flush=True)
        print(f"  SRC: {r['expected_sources']}", flush=True)
        print(f"  FP: {r['fingerprint_phrases']}", flush=True)

if __name__ == '__main__':
    main()
