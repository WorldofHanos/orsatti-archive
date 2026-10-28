import json,urllib.request,urllib.parse,re
H={'User-Agent':'OrsattiArchive/1.0 (family archive)'}
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))
def norm(t): return re.sub(r'[^a-z0-9]','',t.lower().replace('&','and').replace('the ',''))
cr=json.load(open('credits.all.json'));cache=json.load(open('bo_cache.json')) if __import__('os').path.exists('bo_cache.json') else {}
for c in cr:
  if c['type']!='movie' or c.get('boxOfficeSource') or c.get('boxOffice'): continue
  k=f"{c['title']}|{c['year']}"
  if k not in cache:
    r={'gross':None,'wiki':None,'text':None}
    try:
      hits=get('https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srlimit=1&srsearch='+urllib.parse.quote(f"{c['title']} {c['year']} film"))['query']['search']
      if hits and norm(c['title']) in norm(hits[0]['title']):
        t=hits[0]['title'];w=get('https://en.wikipedia.org/w/api.php?action=parse&prop=wikitext&format=json&section=0&page='+urllib.parse.quote(t))['parse']['wikitext']['*']
        if str(c['year']) in w:
          r['wiki']='https://en.wikipedia.org/wiki/'+urllib.parse.quote(t.replace(' ','_'))
          m=re.search(r'\|\s*gross\s*=\s*([^\n]*)',w)
          if m:
            g=re.sub(r'<ref.*?(</ref>|/>)','',m.group(1));g=re.sub(r'\{\{[^|}]*\|?|\}\}|\[\[|\]\]|&nbsp;',' ',g).strip();r['text']=g
            n=re.search(r'\$\s*([\d.,]+)\s*(million|billion)?',g)
            if n and not re.search(r'rental|\(US\)|domestic|North America|US and Canada',g,re.I):
              r['gross']=int(float(n.group(1).replace(',',''))*{'million':1e6,'billion':1e9}.get(n.group(2),1))
    except Exception as e: print('ERR',k,e)
    cache[k]=r
  r=cache[k]; c['boxOffice']=r['gross'];c['boxOfficeText']=r['text'];c['boxOfficeSource']=r['wiki'] if r['gross'] else None
json.dump(cache,open('bo_cache.json','w'));json.dump(cr,open('credits.all.json','w'),indent=1,ensure_ascii=False)
print('BO DONE',sum(1 for c in cr if c.get('boxOffice')),flush=True)
