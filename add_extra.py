import json,urllib.request,urllib.parse,os
R='Rowbie Orsatti';S='https://www.imdb.com/name/nm1769066/'
X=[dict(title='Charlie Puth: Loser',year=2022,type='music_video',role='Stunt Coordinator',youtube='https://www.youtube.com/watch?v=Sp6BS-rSr98',imdb='https://www.imdb.com/title/tt22527742/',yt='Sp6BS-rSr98'),
dict(title='Ballard',year=2025,type='tv',role='Stunt double: John Lee Ames'),
dict(title='The Runarounds',year=2025,type='tv',role='Utility Stunts'),
dict(title='The Oval',year=2026,type='tv',role='Stunt Performer'),
dict(title='Beauty in Black',year=2026,type='tv',role='Utility Stunts'),
dict(title='The Middle',year=2024,type='movie',role='Stunt Coordinator (short)'),
dict(title='Bad Bodyguard',year=2023,type='movie',role='Stunt Coordinator (short)'),
dict(title='Fort Valor',year=2026,type='movie',role='Stunt Performer (short)')]
V='Victor "Vic" Orsatti';A='https://catalog.afi.com/Person/151138-Victor-M.-Orsatti'
VX=[('Flight to Hong Kong',1956,'movie','Associate Producer'),('Ride Out for Revenge',1957,'movie','Associate Producer'),('Domino Kid',1957,'movie','Producer'),('The Hired Gun',1957,'movie','Producer'),('Apache Territory',1958,'movie','Producer'),('The Texan',1958,'tv','Producer (Rorvic Productions)'),('A Face in the Rain',1963,'movie','Executive Producer'),('Spring Fever',1927,'movie','Script Clerk')]
X+= [dict(title=t,year=y,type=ty,role=r,person=V,source=A if t!='The Texan' else 'https://en.wikipedia.org/wiki/Rorvic_Productions') for t,y,ty,r in VX]
FH='Frank H. Orsatti (stuntman, 1942–2004)';VA='https://variety.com/2005/scene/people-news/frank-orsatti-1117915927/'
X+=[dict(title='B.S. I Love You',year=1971,type='movie',role='Stunts',person=FH,source='https://stuntsunlimited.com/frank-orsatti-honorary/'),
dict(title='Serpico',year=1973,type='movie',role='Stunt Coordinator',person=FH,source=VA),
dict(title='The Magician',year=1973,type='tv',role='Stunts',person=FH,source=VA),
dict(title='The Practice',year=1997,type='tv',role='Stunt Double',person='Noon Orsatti',source='https://app.productionbeast.com/12248-noon-orsatti')]
out=[]
for x in X:
  c=dict(person=x.get('person',R),source=x.get('source',S),boxOffice=None,boxOfficeSource=None,**{k:v for k,v in x.items() if k not in('yt','person','source')})
  if x.get('yt'):
    p=f"posters/yt-{x['yt']}.jpg";urllib.request.urlretrieve(f"https://i.ytimg.com/vi/{x['yt']}/hqdefault.jpg",p);c['poster']=p
  else:
    q=urllib.parse.quote(x['title'].lower())
    try:
      d=json.load(urllib.request.urlopen(f"https://v2.sg.media-imdb.com/suggestion/{q[0]}/{q}.json",timeout=15))['d']
      m=[e for e in d if e.get('id','').startswith('tt') and e.get('l','').lower()==x['title'].lower() and ((x['type']=='tv' and 'TV' in (e.get('q') or '')) or abs((e.get('y') or 0)-x['year'])<=1)]
      if m:
        e=m[0];c['imdb']=f"https://www.imdb.com/title/{e['id']}/"
        if e.get('i'):
          p=f"posters/{e['id']}.jpg";urllib.request.urlretrieve(e['i']['imageUrl'].replace('._V1_.','._V1_SX400.'),p);c['poster']=p
    except Exception as ex: print(x['title'],ex)
  print(c['title'],c.get('imdb'),c.get('poster'));out.append(c)
json.dump(out,open('extra_credits.json','w'),indent=1)
