import json,re
F={'218285-Ernie-Orsatti':'Ernie F. Orsatti (1940–2020)','53874-Frank-Orsatti':'Frank H. Orsatti (stuntman, 1942–2004)','289861-Noon-Orsatti':'Noon Orsatti'}
out=[]
for k,person in F.items():
  L=open(f'/tmp/afi-{k}.txt').read().split('\n')
  i=L.index('FILMOGRAPHY');sec=None;buf=[]
  for l in L[i+1:]:
    if l in('STAND INS','CAST','DIRECTOR','HISTORY'): sec=l;buf=[];continue
    if l in('TITLE','CREDITED AS','CREDIT','YEAR') or l.startswith('THESE TITLES') or l.startswith('CATALOG') or l.startswith('(1893'): buf=[];continue
    if l.startswith('AFI Life'): break
    if re.fullmatch(r'(18|19|20)\d\d',l):
      if buf:
        t=buf[0];role=buf[-1] if len(buf)>1 else ('Cast' if sec=='CAST' else 'Stunts')
        out.append(dict(person=person,title=t.title().replace("'S","'s"),year=int(l),role=role if sec!='CAST' else f'Actor: {role}' if len(buf)>1 else 'Actor',type='movie',source=f'https://catalog.afi.com/Person/{k}'))
      buf=[];continue
    buf.append(l)
json.dump(out,open('afi_credits.json','w'),indent=1,ensure_ascii=False)
import collections;print(collections.Counter(c['person'] for c in out))
