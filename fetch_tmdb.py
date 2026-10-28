import json,re,os,subprocess,time
from bs4 import BeautifulSoup
P={'1407364-noon-orsatti':'Noon Orsatti','112572-ernie-f-orsatti':'Ernie F. Orsatti (1940–2020)','1753329-rowbie-orsatti':'Rowbie Orsatti','166075-frank-orsatti':'Frank H. Orsatti (stuntman, 1942–2004)','1219264-frank-orsatti':'Frank H. Orsatti (stuntman, 1942–2004)','1050247-victor-m-orsatti':'Victor "Vic" Orsatti (1905–1984)','4194475-ernie-orsatti':'Ernie Orsatti (1902–1968)'}
def get(u):
  return subprocess.run(['curl','-s','-m','30','-A','Mozilla/5.0',u],capture_output=True,text=True).stdout
out=[];titles={}
for slug,person in P.items():
  url=f'https://www.themoviedb.org/person/{slug}?language=en-US'
  s=BeautifulSoup(get(url),'html.parser')
  for t in s.select('table.credit_group'):
    h=t.find_previous('h3');dept=h.get_text(strip=True) if h else ''
    for tr in t.select('tr'):
      a=tr.select_one('a.tooltip')
      if not a: continue
      y=tr.select_one('td.year').get_text(strip=True)
      g=tr.select_one('span.group');role=re.sub(r'\s+',' ',g.get_text(' ',strip=True)).lstrip('… ').strip() if g else dept
      role=re.sub(r'^as ','',role)
      href=a['href'].split('?')[0]
      out.append(dict(person=person,tmdb='https://www.themoviedb.org'+href,title=a.get_text(strip=True),year=int(y) if y.isdigit() else None,role=role or dept,dept=dept,type='tv' if href.startswith('/tv/') else 'movie',source=url))
      titles[href]=None
  print(slug,len(out),flush=True)
os.makedirs('posters',exist_ok=True)
meta=json.load(open('tmdb_meta.json')) if os.path.exists('tmdb_meta.json') else {}
for href in titles:
  if href in meta: continue
  h=get('https://www.themoviedb.org'+href+'?language=en-US')
  img=re.search(r'<meta property="og:image" content="([^"]+)"',h);imdb=re.search(r'imdb\.com/title/(tt\d+)',h)
  yrs=re.search(r'<span class="tag release_date">\(([^)]*)\)',h)
  meta[href]=dict(img=img.group(1) if img else None,imdb=imdb.group(1) if imdb else None,yr=yrs.group(1) if yrs else None)
  if len(meta)%25==0: json.dump(meta,open('tmdb_meta.json','w')); print('meta',len(meta),flush=True)
json.dump(meta,open('tmdb_meta.json','w'))
for c in out:
  m=meta.get(c['tmdb'].replace('https://www.themoviedb.org',''),{})
  c['imdb']=f"https://www.imdb.com/title/{m['imdb']}/" if m.get('imdb') else None; c['posterSource']=m.get('img')
  if c['year'] is None and m.get('yr') and m['yr'][:4].isdigit(): c['year']=int(m['yr'][:4])
json.dump(out,open('tmdb_credits.json','w'),indent=1,ensure_ascii=False)
print('DONE',len(out),len(titles),flush=True)
