import json,re,urllib.request,time
H={'User-Agent':'Mozilla/5.0'}
import subprocess
g=lambda u:subprocess.run(['curl','-s','-A','Mozilla/5.0',u],capture_output=True,text=True,timeout=40).stdout
d=json.load(open('data.json'));out={}
TM={"It's Always Sunny in Philadelphia":'https://www.themoviedb.org/tv/2710-it-s-always-sunny-in-philadelphia','Entourage':'https://www.themoviedb.org/tv/1940-entourage','Carnivàle':'https://www.themoviedb.org/tv/185-carnivale','Moonlight':'https://www.themoviedb.org/tv/5690-moonlight','The Practice':'https://www.themoviedb.org/tv/3050-the-practice','The Magician':'https://www.themoviedb.org/tv/11745-the-magician'}
for f in d['films']:
  if f['title'] in TM and f['type']=='tv': f['tmdb']=TM[f['title']]
for f in d['films']:
  if f['type']!='tv' or not f.get('years') or not f.get('tmdb'): continue
  base=re.match(r'(https://www.themoviedb.org/tv/[^/?]+)',f['tmdb']).group(1)
  t=g(base+'/seasons?language=en-US')
  ss=sorted({int(n) for n in re.findall(r'/season/(\d+)\?',t)} - {0})
  S=[]
  for n in ss:
    p=g(f'{base}/season/{n}?language=en-US')
    ys=sorted({int(y) for y in re.findall(r'<span class="date">[A-Z][a-z]+ \d{1,2}, (\d{4})</span>',p)} or {int(y) for y in re.findall(r'"air_date"\s*:\s*"(\d{4})',p)} or {int(y) for y in re.findall(r'(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}, (\d{4})',p)})
    S.append(dict(season=n,years=ys));time.sleep(.2)
  out[f['title']]=S;print(f['title'],S,flush=True)
json.dump(out,open('tv_seasons.json','w'),indent=1)
