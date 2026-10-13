#!/bin/bash
# Fetch full article (body_markdown) + comments for every article in list files
python3 - <<'PYEOF'
import json, os, time, urllib.request, urllib.error

def get(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (ilands-crawl research)'})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:
            print('  retry', attempt, url, e)
            time.sleep(5)
    return None

work = []
for u in ['oliver_ilands','omega_ilands','aces_tom','jin_ilands','sam_ilands','vera_agent','sakiholds','lioraopal','fray','lander_rooms','cael_ilands','david_ilands','juliancarries','umbrafrancis','renji-ilands','uru_ilands','hynoma','rhett_7','michael_lands']:
    d = json.load(open(f'list_{u}.json'))
    for a in d:
        work.append((u, a['id'], a['slug']))

print('total articles:', len(work))
done_fnames = set(f for f in os.listdir('.') if f.startswith('article_'))
for (u, aid, slug) in work:
    base = f'{u}_{slug}'
    if f'article_{base}.json' in done_fnames and f'comments_{base}.json' in done_fnames:
        print('skip (have)', base); continue
    print('fetch', u, aid, slug)
    art = get(f'https://dev.to/api/articles/{aid}')
    if art:
        json.dump(art, open(f'article_{base}.json','w'), indent=2, ensure_ascii=False)
        md = art.get('body_markdown','')
        fm = f"---\ntitle: {art.get('title')}\nurl: {art.get('url')}\npublished_at: {art.get('published_at')}\nedited_at: {art.get('edited_at')}\nauthor: {art.get('user',{}).get('username')}\ntags: {art.get('tag_list')}\nreactions: public={art.get('public_reactions_count')} positive={art.get('positive_reactions_count')} comments={art.get('comments_count')}\n---\n\n"
        open(f'{base}.md','w',encoding='utf-8').write(fm + md)
    comments = get(f'https://dev.to/api/comments?a_id={aid}')
    if comments is not None:
        json.dump(comments, open(f'comments_{base}.json','w'), indent=2, ensure_ascii=False)
        # rendered comments md
        lines = [f"# Comments for: {art.get('title') if art else base}"]
        def walk(cs, depth=0):
            for c in cs:
                u2 = c.get('user',{}) or {}
                body = c.get('body_html','') or ''
                lines.append(f"\n{'  '*depth}- **{u2.get('username','?')}** ({c.get('created_at','?')}) id={c.get('id_code')}")
                lines.append(f"{'  '*depth}  {body}")
                walk(c.get('children') or [], depth+1)
        walk(comments or [])
        open(f'comments_{base}.md','w',encoding='utf-8').write('\n'.join(lines))
    time.sleep(2)
print('DONE')
PYEOF
