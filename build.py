import sys,functools
print=functools.partial(print,flush=True)
import json,urllib.request,urllib.parse,os,re
U={'ef':'https://www.imdb.com/name/nm0650683/','e':'https://www.imdb.com/name/nm1108143/','n':'https://www.imdb.com/name/nm0650687/','r':'https://www.imdb.com/name/nm1769066/','fs':'https://www.imdb.com/name/nm0650685/','fa':'https://www.imdb.com/name/nm0650684/','afi':'https://catalog.afi.com/Person/289861-Noon-Orsatti'}
P={'e':'Ernie Orsatti (1902–1968)','ef':'Ernie F. Orsatti (1940–2020)','n':'Noon Orsatti','r':'Rowbie Orsatti','fs':'Frank H. Orsatti (stuntman, 1942–2004)','fa':'Frank Orsatti (agent)'}
C=[('e',1923,'Our Hospitality','Stunt coordinator (uncredited)'),('e',1924,'Sherlock Jr.','Assistant property master & stunts (uncredited)'),('e',1928,'The Cameraman','Assistant property master (uncredited)'),
('e',1934,'Death on the Diamond','Bit part: a Cardinals player shot while running the bases'),('ef',1972,'The Poseidon Adventure','Stunts – the famous fall through the glass skylight'),('ef',1974,'The Towering Inferno','Stunts – firefighter hanging from the scenic elevator'),('fa',1935,'The Irish in Us','Writer (story)'),
('ef',1978,'The Swarm','Duty Officer'),('ef',1977,'Viva Knievel!','Norman Clark'),('ef',1980,'Defiance','2nd Cop'),('ef',1982,'Dead Men Don\'t Wear Plaid','Stunts'),('ef',1995,'Tall Tale','Second unit director'),('ef',1995,'Theodore Rex','Second unit director'),('ef',1996,'Larger Than Life','Second unit director'),('ef',1997,'City of Industry','Second unit director'),('ef',1998,'Fallen','Stunts'),('ef',1998,'Doctor Dolittle','Second unit director'),('ef',1998,'Mafia!','Second unit director'),('ef',2000,'Men of Honor','Second unit director'),('ef',2001,'Black Knight','Second unit director'),('ef',2004,'Club Dread','Second unit director'),('ef',2005,'Yours, Mine & Ours','Stunt coordinator'),('ef',2006,'The Pink Panther','Second unit director: stunt unit (uncredited)'),('ef',2008,'Made of Honor','Stunt coordinator'),('ef',2008,'Strange Wilderness','Stunt coordinator'),('ef',2009,'The Pink Panther 2','Stunt coordinator'),('ef',2010,'Furry Vengeance','Stunt coordinator'),('ef',2006,"It's Always Sunny in Philadelphia",'Stunt coordinator (18 eps, 2006–2008)'),('ef',2004,'Entourage','Stunt coordinator (5 eps, 2004–2007)'),('ef',2003,'Carnivàle','Stunt coordinator (24 eps, 2003–2005)'),('ef',2009,'Big Love','Stunt director/coordinator (9 eps)'),
('fs',1974,'Black Samson',"Nappa's Gang"),('fs',1984,'The Terminator','Stunts – doubled Arnold Schwarzenegger (uncredited)'),('fs',1989,'Star Trek V: The Final Frontier','Stunts'),('fs',1991,'Highlander II: The Quickening','Stunts'),('fs',1993,'Hard Target','Stunts'),('fs',1994,'Maverick','Unshaven Man'),('fs',1995,'Nine Months','Stunts'),('fs',1997,'Con Air','Stunts'),('fs',1997,'Nothing to Lose','Stunts'),
('n',1986,'Back to School','Stunts'),('n',1986,'The Golden Child','Stunt player (as E. Noon Orsatti)'),('n',1988,'Beetlejuice','Stunt player'),('n',1988,'A Nightmare on Elm Street 4: The Dream Master','Stunt player'),('n',1996,'Tremors 2: Aftershocks','Stunt coordinator'),('n',1997,'Alien Resurrection','Stunts'),('n',2001,'Stop at Nothing','Second unit director'),('n',2007,'Moonlight','Second unit director (12 eps)'),('n',2008,'Rambo','Stunts'),('n',2010,'The Expendables','Stunts'),('n',2012,'Stolen','Second unit director'),('n',2019,'Gemini Man','Stunts'),('n',2019,'Avengers: Endgame','Stunts'),('n',2023,'Extraction II','Lead stunt coordinator (Taurus World Stunt Award)'),('n',2024,'Borderlands','Second unit director'),('n',2025,"You're Cordially Invited",'Second unit director'),('n',2025,'Bride Hard','Second unit director & stunt coordinator'),('n',2025,'Thunderbolts*','Stunts'),
('r',2012,'Project X','Stunts'),('r',2021,'Hawkeye','Stunts (5 eps)'),('r',2023,'Extraction II','Stunts'),('r',2024,'Fly Me to the Moon','Stunts'),('r',2024,'Agatha All Along','Stunt double: Joe Locke (9 eps)'),('r',2025,'Thunderbolts*','Stunts'),('r',2025,"You're Cordially Invited",'Stunts'),('r',2025,'Bride Hard','Stunts'),('r',2025,'Stranger Things','Stunt performer (2 eps)')]
out=[];os.makedirs('posters',exist_ok=True)
for k,y,t,role in C:
  q=urllib.parse.quote(f'{t} {y}'.lower()); e={}
  try:
    d=json.load(urllib.request.urlopen(urllib.request.Request(f'https://v3.sg.media-imdb.com/suggestion/x/{q}.json',headers={'User-Agent':'Mozilla/5.0'})))['d']
    m=[x for x in d if x.get('id','').startswith('tt') and abs((x.get('y') or 0)-y)<=1] or [x for x in d if x.get('id','').startswith('tt')]
    e=m[0] if m else {}
  except Exception as ex: print('ERR',t,ex)
  tid=e.get('id'); poster=None; img=(e.get('i') or {}).get('imageUrl')
  if img:
    fn=f'posters/{tid}.jpg'
    if not os.path.exists(fn):
      try: urllib.request.urlretrieve(img.replace('._V1_.','._V1_UX400_.') if '._V1_.' in img else img,fn)
      except Exception as ex: print('IMG',t,ex)
    poster=fn
  out.append(dict(year=y,title=t,person=P[k],role=role,imdb=f'https://www.imdb.com/title/{tid}/' if tid else None,matchedTitle=e.get('l'),poster=poster,posterSource=img,source=({'Death on the Diamond':'https://www.baseballamore.com/orsattie/','The Poseidon Adventure':'https://en.wikipedia.org/wiki/Ernie_Orsatti','The Towering Inferno':'https://en.wikipedia.org/wiki/Ernie_Orsatti'}.get(t) or U['afi'] if (k=='n' and y<1990) else ('https://www.ihorrordb.com/people/116575/noon-orsatti' if t in ('Tremors 2: Aftershocks','Alien Resurrection') else U[k]))))
  print(y,t,'->',tid,e.get('l'),e.get('y'))
json.dump(out,open('credits.tmp.json','w'),indent=1,ensure_ascii=False)
