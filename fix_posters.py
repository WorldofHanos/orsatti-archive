import json,re,subprocess,os,urllib.parse
def get(u): return subprocess.run(['curl','-s','-m','30','-A','Mozilla/5.0',u],capture_output=True,text=True).stdout
Q={'Cheaper by the Dozen|2003':('movie','Cheaper by the Dozen','2003'),'Mixed Nuts|1994':('movie','Mixed Nuts','1994'),'Stop at Nothing|2001':('movie','Stop at Nothing','2001'),'Big Love|None':('tv','Big Love',''),'Stranger Things|None':('tv','Stranger Things','')}
ov=json.load(open('poster_override.json')) if os.path.exists('poster_override.json') else {}
for k,(typ,t,y) in Q.items():
  h=get(f'https://www.themoviedb.org/search/{typ}?query='+urllib.parse.quote(t+(' y:'+y if y else ''))+'&language=en-US')
  m=re.search(r'href="/'+typ+r'/(\d+[^"?]*)',h)
  if not m: print('nomatch',k);continue
  href=f'/{typ}/{m.group(1)}';p=get('https://www.themoviedb.org'+href+'?language=en-US')
  img=re.search(r'<meta property="og:image" content="([^"]+)"',p)
  if img:
    fn='posters/'+re.sub(r'[^A-Za-z0-9-]','',m.group(1))+'.jpg';subprocess.run(['curl','-sL','-m','30','-o',fn,img.group(1)])
    ov[k]=dict(poster=fn,tmdb='https://www.themoviedb.org'+href,posterSource=img.group(1));print(k,fn,os.path.getsize(fn))
json.dump(ov,open('poster_override.json','w'),indent=1)
