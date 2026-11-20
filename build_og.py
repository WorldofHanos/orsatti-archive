"""Render og.png (1200x630 share image) from data.json so its numbers never go stale.
Called by assemble.py. Re-renders only when the numbers change (og-stats.json). Needs Playwright;
if it is not installed the build continues and the existing og.png is kept."""
import json, os, datetime, base64, pathlib
HERE = pathlib.Path(__file__).parent
D = json.load(open(HERE / 'data.json'))
S = D['boxOfficeSummary']
stats = {'years': datetime.date.today().year - 1923,
         'credits': sum(len(f['credits']) for f in D['films']),
         'films': S['films'] + S['tvShows'],
         'box': '$%.1fB' % (S['total'] / 1e9)}
sf = HERE / 'og-stats.json'
if (HERE / 'og.png').exists() and sf.exists() and json.load(open(sf)) == stats and not os.environ.get('OG_FORCE'):
    print('og.png: up to date', stats)
else:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print('og.png: Playwright not installed, kept existing image (run with /workspace/.pwvenv/bin/python to refresh)')
    else:
        logo = base64.b64encode((HERE / 'logo.png').read_bytes()).decode()
        cells = ''.join(f'<div><b>{n}</b><span>{l}</span></div>' for n, l in [
            (stats['years'], 'Years in Hollywood'), (stats['credits'], 'Credits archived'),
            (stats['films'], 'Films &amp; series'), (stats['box'], 'Worldwide box office*')])
        html = f'''<html><head><style>
html,body{{margin:0;width:1200px;height:630px;background:#000;color:#f3eee4;font-family:'Playfair Display',serif;text-align:center;overflow:hidden}}
img{{height:140px;margin-top:50px;filter:drop-shadow(0 0 18px rgba(255,255,255,.18))}}
h1{{font-weight:400;font-size:80px;letter-spacing:1px;margin:22px 0 0;text-shadow:0 0 24px rgba(255,255,255,.18)}}
.rule{{margin:26px auto 0;width:210px;height:1px;background:linear-gradient(90deg,transparent,#c9a45c 30%,#c9a45c 70%,transparent);position:relative}}
.rule:after{{content:'';position:absolute;left:101px;top:-3px;width:7px;height:7px;background:#c9a45c;transform:rotate(45deg)}}
.tag{{color:#c9a45c;font-style:italic;font-size:21px;margin-top:22px}}
.st{{display:flex;justify-content:center;gap:0;margin-top:46px}}
.st div{{width:220px}}.st b{{display:block;font-weight:400;font-size:38px}}
.st span{{display:block;font-family:Inter,sans-serif;font-size:10.5px;letter-spacing:2.2px;text-transform:uppercase;color:#c9a45c;margin-top:8px}}
</style></head><body><img src="data:image/png;base64,{logo}"><h1>The Orsatti Film Archive</h1><div class="rule"></div>
<div class="tag">A Hollywood Family Since 1923</div><div class="st">{cells}</div></body></html>'''
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1200, 'height': 630})
            pg.set_content(html); pg.wait_for_timeout(300)
            pg.screenshot(path=str(HERE / 'og.png')); b.close()
        json.dump(stats, open(sf, 'w'))
        print('og.png: rendered', stats)
