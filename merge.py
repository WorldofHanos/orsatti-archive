import json,re,os,subprocess,urllib.parse
def norm(t): return re.sub(r'[^a-z0-9]','',t.lower().replace('&','and').replace('the ',''))
def sh(*a): return subprocess.run(a,capture_output=True,text=True).stdout
base=json.load(open('credits.bo.json'));tm=json.load(open('tmdb_credits.json'));afi=json.load(open('afi_credits.json'))
for c in base: c.setdefault('type','tv' if c['title'] in('It\'s Always Sunny in Philadelphia','Entourage','Carnivàle','Big Love','Moonlight','Hawkeye','Agatha All Along','Stranger Things') else 'movie')
extra=[dict(person='Rowbie Orsatti',title='Let Me In',year=2010,role='Actor: Scottie Tate (also stunts, uncredited)',type='movie',source='https://www.imdb.com/name/nm1769066/'),
 dict(person='Rowbie Orsatti',title='Charmed',year=1998,role='First credit (per IMDb)',type='tv',imdb='https://www.imdb.com/title/tt0158552/',source='https://www.imdb.com/name/nm1769066/')]
base+= [e for e in extra if (e['person'],norm(e['title'])) not in {(c['person'],norm(c['title'])) for c in base}]
allc=list(base); pk={(c['person'],norm(c['title'])) for c in allc}
def titlekey(t,y): return norm(t)
tinfo={}
for c in allc: tinfo.setdefault(norm(c['title']),c)
for c in tm+afi:
  if not c.get('year'): continue
  k=(c['person'],norm(c['title']))
  if k in pk: continue
  pk.add(k); src=tinfo.get(norm(c['title']))
  if src and abs((src['year'] or 0)-c['year'])<=2:
    for f in('imdb','poster','posterSource','boxOffice','boxOfficeText','boxOfficeSource'): c.setdefault(f,src.get(f))
    c['year']=src['year'];c['title']=src['title']
  else: tinfo[norm(c['title'])]=c
  allc.append(c)
# posters for new titles
for c in allc:
  if c.get('poster') and os.path.exists(c['poster']): continue
  if not c.get('imdb') and c['type']=='movie':
    try:
      d=json.loads(sh('curl','-s','-m','20','-A','Mozilla/5.0','https://v3.sg.media-imdb.com/suggestion/x/'+urllib.parse.quote(f"{c['title']} {c['year']}".lower())+'.json')).get('d',[])
      m=[x for x in d if x.get('id','').startswith('tt') and abs((x.get('y') or 0)-c['year'])<=1]
      if m: c['imdb']=f"https://www.imdb.com/title/{m[0]['id']}/"; c['posterSource']=c.get('posterSource') or (m[0].get('i') or {}).get('imageUrl')
    except Exception as e: pass
  u=c.get('posterSource')
  if u:
    key=(c.get('imdb') or c.get('tmdb') or c['title']).rstrip('/').split('/')[-1]
    fn=f'posters/{re.sub(r"[^A-Za-z0-9-]","",key)}.jpg'
    if not os.path.exists(fn): sh('curl','-sL','-m','30','-A','Mozilla/5.0','-o',fn,u.replace('._V1_.','._V1_UX400_.'))
    if os.path.exists(fn) and os.path.getsize(fn)>2000: c['poster']=fn
json.dump(allc,open('credits.all.json','w'),indent=1,ensure_ascii=False)
import collections;print(len(allc),len({norm(c['title']) for c in allc}),collections.Counter(c['person'] for c in allc))
