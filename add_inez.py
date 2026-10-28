import json,urllib.request,urllib.parse
P='Inez Gorman (1912–1986)';A='https://catalog.afi.com/Person/72676-Inez-Gorman'
ex=[e for e in json.load(open('extra_credits.json')) if e['person']!=P]
for t,y,r in json.load(open('inez_list.json')):
  c=dict(person=P,source=A,boxOffice=None,boxOfficeSource=None,title=t,year=y,type='movie',role=r)
  q=urllib.parse.quote(t.lower())
  d=json.load(urllib.request.urlopen(f"https://v2.sg.media-imdb.com/suggestion/{q[0]}/{q}.json",timeout=15))['d']
  m=[e for e in d if e.get('id','').startswith('tt') and e.get('l','').lower()==t.lower() and abs((e.get('y') or 0)-y)<=1]
  if m:
    e=m[0];c['imdb']='https://www.imdb.com/title/%s/'%e['id']
    if e.get('i'):
      p='posters/%s.jpg'%e['id'];urllib.request.urlretrieve(e['i']['imageUrl'].replace('._V1_.','._V1_SX400.'),p);c['poster']=p
  print(t,c.get('imdb'),c.get('poster'));ex.append(c)
json.dump(ex,open('extra_credits.json','w'),indent=1,ensure_ascii=False)
