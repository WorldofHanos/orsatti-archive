"""Static SEO layer: per-person pages, crawlable index summary, JSON-LD, sitemap, robots.
Uses only existing text from data.json. Called at the end of assemble.py."""
import json, re, html, datetime, os
SITE = 'https://orsattifilmarchive.com'
D = json.load(open('data.json'))
e = lambda s: html.escape(s or '', quote=True)
short = lambda n: n.split(' (')[0]
def slug(n): return re.sub(r'[^a-z0-9]+', '-', short(n).lower()).strip('-')
TITLE = 'Orsatti Family Film Archive | A Hollywood Family Since 1923'
DESC = ("The Orsattis, a Hollywood family since 1923: stunt work by Ernie, Frank H., Ernie F., Noon and "
        f"Rowbie Orsatti, Ken Orsatti of SAG, and {len(D['films'])} films and series.")
IMG = SITE + '/og.png'
today = datetime.date.today().isoformat()

def credits_for(p):
    out = []
    if p.get('films'):  # Inez: own filmography list
        for f in p['films']:
            out.append((f.get('year'), f.get('title'), f.get('role'), f.get('imdb'), 'movie'))
    s = short(p['name'])
    for f in D['films']:
        for c in f.get('credits', []):
            if c['person'].startswith(s):
                out.append((f.get('year'), f['title'], c.get('role'), f.get('imdb'), f.get('type')))
    seen, res = set(), []
    for r in sorted(out, key=lambda r: (r[0] or 0, r[1] or '')):
        k = (r[0], r[1], r[2])
        if k not in seen: seen.add(k); res.append(r)
    return res

def milestones_for(p):
    s = short(p['name'])
    return [m for m in D['milestones'] if s in m.get('title', '') or s in m.get('text', '')]

def link(u):
    if isinstance(u, dict): u = u.get('url') or u.get('source') or ''
    if isinstance(u, str) and u.startswith('http'):
        return f'<a href="{e(u)}" rel="noopener">{e(re.sub(r"^https?://(www\.)?", "", u).split("/")[0])}</a>'
    return e(u if isinstance(u, str) else '')

def person_ld(p):
    ld = {'@type': 'Person', 'name': short(p['name']), 'url': f"{SITE}/people/{slug(p['name'])}.html"}
    if p.get('birthName'): ld['alternateName'] = p['birthName']
    if p.get('relation'): ld['description'] = p['relation']
    if p.get('photo'): ld['image'] = SITE + '/' + p['photo']
    if p.get('imdb'): ld['sameAs'] = [p['imdb']]
    return ld

def head(title, desc, url, img, ld, prefix=''):
    return (f'<title>{e(title)}</title><meta name="description" content="{e(desc)}">'
            f'<link rel="canonical" href="{e(url)}">'
            f'<meta property="og:site_name" content="The Orsatti Film Archive"><meta property="og:type" content="website">'
            f'<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">'
            f'<meta property="og:url" content="{e(url)}"><meta property="og:image" content="{e(img)}">'
            f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}">'
            f'<meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{e(img)}">'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

SHELL = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
{head}<link rel="icon" href="{pre}favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}styles.css"><link rel="stylesheet" href="{pre}seo.css"></head><body class="sp">
<div class="grain"></div>
<header class="sp-top"><a href="{pre}"><img src="{pre}logo.png" alt="Orsatti family crest – comedy and tragedy masks"></a><a class="sp-home" href="{pre}">The Orsatti Film Archive</a></header>
<main class="sp-main">{body}</main>
<footer><div class="deco"><span></span>◆<span></span></div><p class="sp-foot"><a href="{pre}">Explore the full timeline ›</a> · <a href="{pre}people/">The family</a></p></footer>
</body></html>
'''

def paras(t): return ''.join(f'<p>{e(x)}</p>' for x in (t or '').split('\n') if x.strip())

pages = []
for p in D['people']:
    s = slug(p['name']); url = f'{SITE}/people/{s}.html'
    first = (p.get('note') or '').split('\n')[0]
    desc = first if len(first) <= 160 else first[:157].rsplit(' ', 1)[0] + '…'
    title = f"{p['name']}{', ' + p['years'] if p.get('years') else ''} | The Orsatti Film Archive"
    img = SITE + '/' + p['photo'] if p.get('photo') else IMG
    b = '<article class="sp-person">'
    if p.get('photo'):
        b += f'<img class="sp-portrait" src="../{e(p["photo"])}" alt="{e(p.get("photoCaption") or p["name"])}">'
    b += '<div class="k">Family Member</div>' + f'<h1>{e(p["name"])}</h1>'
    if p.get('birthName'): b += f'<div class="sp-meta">Born {e(p["birthName"])}</div>'
    if p.get('relation'): b += f'<div class="sp-meta">{e(p["relation"])}</div>'
    if p.get('years'): b += f'<div class="sp-meta">{e(p["years"])}</div>'
    b += f'<div class="sp-bio">{paras(p.get("note"))}</div>'
    if p.get('imdb'): b += f'<p><a class="btn" href="{e(p["imdb"])}" rel="noopener">View on IMDb</a></p>'
    cr = credits_for(p)
    if cr:
        b += f'<h2>Credits in the archive ({len(cr)})</h2><ul class="sp-list">'
        for y, t, role, imdb, typ in cr:
            tt = f'<a href="{e(imdb)}" rel="noopener">{e(t)}</a>' if imdb else e(t)
            tag = ' <i>TV</i>' if typ == 'tv' else ' <i>Music Video</i>' if typ == 'music_video' else ''
            b += f'<li><span class="fy">{e(str(y or ""))}</span> {tt}{tag}{" <span class=fr>" + e(role) + "</span>" if role else ""}</li>'
        b += '</ul>'
    ms = milestones_for(p)
    if ms:
        b += '<h2>On the timeline</h2>'
        for m in sorted(ms, key=lambda m: m.get('year') or 0):
            b += f'<section class="sp-ms"><div class="fy">{e(str(m.get("year") or ""))}</div><h3>{e(m["title"])}</h3>{paras(m.get("text"))}</section>'
    srcs = [x for x in ([p.get('photoSource')] + (p.get('noteSources') or []) + (p.get('nameSources') or [])) if x]
    srcs = [x for i, x in enumerate(srcs) if json.dumps(x) not in [json.dumps(y) for y in srcs[:i]]]
    if srcs: b += '<p class="src">Sources: ' + ' · '.join(link(x) for x in srcs) + '</p>'
    b += '</article>'
    ld = {'@context': 'https://schema.org', **person_ld(p)}
    open(f'people/{s}.html', 'w').write(SHELL.format(head=head(title, desc, url, img, ld), body=b, pre='../'))
    pages.append((p, s, desc))

# family hub page
hub = '<article class="sp-person"><div class="k">The Family</div><h1>The Orsatti Family</h1><ul class="sp-fam">'
for p, s, desc in pages:
    hub += f'<li><a href="{s}.html"><b>{e(p["name"])}</b></a>{" <span class=fy>" + e(p["years"]) + "</span>" if p.get("years") else ""}<br><span>{e(desc)}</span></li>'
hub += '</ul></article>'
hub_ld = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'The Orsatti Family', 'url': SITE + '/people/',
          'hasPart': [person_ld(p) for p, _, _ in pages]}
open('people/index.html', 'w').write(SHELL.format(head=head('The Orsatti Family | The Orsatti Film Archive', DESC, SITE + '/people/', IMG, hub_ld), body=hub, pre='../'))

# index.html: generated head block + noscript summary between markers
site_ld = {'@context': 'https://schema.org', '@graph': [
    {'@type': 'WebSite', 'name': 'The Orsatti Film Archive', 'url': SITE + '/', 'description': DESC},
    *[person_ld(p) for p, _, _ in pages]]}
H = '<!--SEO:HEAD-->' + head(TITLE, DESC, SITE + '/', IMG, site_ld) + '<link rel="stylesheet" href="seo.css"><!--/SEO:HEAD-->'
N = ('<!--SEO:BODY--><noscript><section class="sp-main"><h2>The Orsatti Family</h2><ul class="sp-fam">' +
     ''.join(f'<li><a href="people/{s}.html"><b>{e(p["name"])}</b></a>{" <span class=fy>" + e(p["years"]) + "</span>" if p.get("years") else ""}<br><span>{e(desc)}</span></li>' for p, s, desc in pages) +
     '</ul></section></noscript><!--/SEO:BODY-->')
ix = open('index.html').read()
if '<!--SEO:HEAD-->' not in ix:
    # first run: replace the hand-written title/description/og/twitter tags with the generated block
    ix = re.sub(r'<title>.*?</title>', '', ix, count=1, flags=re.S)
    ix = re.sub(r'<meta (name="description"|property="og:[^"]+"|name="twitter:[^"]+")[^>]*>', '', ix)
    ix = ix.replace('<link rel="icon"', H + '<link rel="icon"', 1)
    ix = ix.replace('<footer>', N + '\n<footer>', 1)
else:
    ix = re.sub(r'<!--SEO:HEAD-->.*?<!--/SEO:HEAD-->', lambda _: H, ix, flags=re.S)
    ix = re.sub(r'<!--SEO:BODY-->.*?<!--/SEO:BODY-->', lambda _: N, ix, flags=re.S)
open('index.html', 'w').write(ix)

urls = [SITE + '/', SITE + '/people/'] + [f'{SITE}/people/{s}.html' for _, s, _ in pages]
open('sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    ''.join(f'  <url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open('robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('seo pages:', len(pages) + 1)
