# --- Ken photo lead (link only)
for p in data['people']:
  if p['name'].startswith('Ken Orsatti'):
    p['photoLinks']=[l for l in p.get('photoLinks',[]) if 'copcomm' not in l['url']]+[dict(caption='Ken Orsatti with SAG President Patty Duke, c. 1987 (SAG-AFTRA magazine, Spring 2021, p. 71)',url='https://digital.copcomm.com/i/1367665-spring-2021/72')]
