import json,urllib.request,urllib.parse,os,re
H={'User-Agent':'Mozilla/5.0'}
V='https://en.wikipedia.org/wiki/Victor_Orsatti'
L=[(1956,'Flight to Hong Kong','Associate producer'),(1957,'Domino Kid','Producer'),(1957,'The Hired Gun','Producer'),(1957,'Ride Out for Revenge','Associate producer'),(1958,'Apache Territory','Producer'),(1963,'Face in the Rain','Executive producer')]
cr=json.load(open('credits.bo.json'));have={(c['title'],c['year']) for c in cr}
for y,t,r in L:
  if (t,y) in have: continue
  d=json.load(urllib.request.urlopen(urllib.request.Request('https://v3.sg.media-imdb.com/suggestion/x/'+urllib.parse.quote(f'{t} {y}'.lower())+'.json',headers=H)))['d']
  m=[x for x in d if x.get('id','').startswith('tt') and abs((x.get('y') or 0)-y)<=1]; e=m[0] if m else {}
  tid=e.get('id');img=(e.get('i') or {}).get('imageUrl');poster=None
  if img: poster=f'posters/{tid}.jpg'; os.system(f"curl -sL -m 30 -A Mozilla/5.0 -o {poster} '{img.replace('._V1_.','._V1_UX400_.')}'")
  cr.append(dict(year=y,title=t,person='Victor "Vic" Orsatti (1905–1984)',role=r,imdb=f'https://www.imdb.com/title/{tid}/' if tid else None,matchedTitle=e.get('l'),poster=poster,posterSource=img,source=V,boxOffice=None,boxOfficeText=None,boxOfficeSource=None))
  print(y,t,tid,e.get('l'),bool(poster))
json.dump(cr,open('credits.bo.json','w'),indent=1,ensure_ascii=False)
