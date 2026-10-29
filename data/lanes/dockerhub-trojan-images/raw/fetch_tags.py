import json, time, urllib.request, urllib.error, os, datetime, math

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
progress = open('progress.log','a')
def log(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).isoformat()} {msg}"
    print(line, flush=True); progress.write(line+"\n"); progress.flush()

def get(url, tries=8):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'research-fetch/1.0'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            wait = min(120, 5 * (2**i))
            log(f"HTTP {e.code} on {url.split('?')[0]} page — sleeping {wait}s (try {i+1}/{tries})")
            time.sleep(wait)
    raise RuntimeError(f"failed after {tries} tries: {url}")

def tag_count(org, repo):
    d = get(f"https://hub.docker.com/v2/repositories/{org}/{repo}/tags?page_size=1")
    return d['count']

for org in ['cybergym','n132']:
    repos = json.load(open(f'org-{org}-repos.json'))['results']
    for r in repos:
        repo = r['name']
        out = f'repo-{org}-{repo}.jsonl'
        total = tag_count(org, repo)
        have = sum(1 for _ in open(out)) if os.path.exists(out) else 0
        if have >= total and total > 0:
            log(f"SKIP {org}/{repo} complete ({have}/{total})")
            continue
        start_page = have // 100 + 1
        pages = math.ceil(total / 100)
        log(f"RESUME {org}/{repo}: have {have}/{total}, pages {start_page}..{pages}")
        with open(out,'a') as f:
            for page in range(start_page, pages+1):
                url = f"https://hub.docker.com/v2/repositories/{org}/{repo}/tags?page_size=100&page={page}"
                d = get(url)
                for t in d.get('results',[]):
                    img = t.get('images') or []
                    f.write(json.dumps({
                        'org':org,'repo':repo,'tag':t.get('name'),
                        'tag_last_pushed':t.get('tag_last_pushed'),
                        'tag_status':t.get('tag_status'),
                        'last_updated':t.get('last_updated'),
                        'digest':t.get('digest'),
                        'images_arch':sorted({i.get('architecture') for i in img}),
                        'retrieved':now,
                        'source':f"https://hub.docker.com/v2/repositories/{org}/{repo}/tags"
                    })+"\n")
                time.sleep(1.0)
        log(f"DONE {org}/{repo}: {total} tags")
progress.close()
