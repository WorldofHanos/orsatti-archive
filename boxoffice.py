import json,urllib.request,urllib.parse,re
H={'User-Agent':'OrsattiArchive/1.0 (family archive)'}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H)))
cr=json.load(open('credits.tmp.json')); cache={}
for c in cr:
  k=(c['title'],c['year'])
  if k not in cache:
    r={'gross':None,'grossText':None,'wiki':None}
    try:
      q=urllib.parse.quote(f"{c['title']} {c['year']} film")
      hits=get(f'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json&srlimit=1')['query']['search']
      if hits:
        t=hits[0]['title']; r['wiki']='https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_'))
        w=get(f'https://en.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(t)}&prop=wikitext&format=json&section=0')['parse']['wikitext']['*']
        m=re.search(r'\|\s*gross\s*=\s*([^\n]*)',w)
        if m:
          g=re.sub(r'<ref.*?(</ref>|/>)','',m.group(1)); g=re.sub(r'\{\{[^|}]*\|?|\}\}|\[\[|\]\]','',g).strip(); r['grossText']=g
          n=re.search(r'\$\s*([\d.,]+)\s*(million|billion)?',g)
          if n:
            v=float(n.group(1).replace(',',''));mul={'million':1e6,'billion':1e9}.get(n.group(2),1); r['gross']=int(v*mul)
    except Exception as e: print('ERR',k,e)
    cache[k]=r; print(k,r['wiki'],r['grossText'],flush=True)
  c.update(boxOffice=cache[k]['gross'],boxOfficeText=cache[k]['grossText'],boxOfficeSource=cache[k]['wiki'])
json.dump(cr,open('credits.bo.json','w'),indent=1,ensure_ascii=False)
