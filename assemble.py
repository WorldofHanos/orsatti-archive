import re
import json
cr=json.load(open('credits.all.json'))+json.load(open('extra_credits.json'))
AFIFIX={('Ernie F. Orsatti (1940–2020)',2003):'Cheaper by the Dozen',('Noon Orsatti',1994):'Mixed Nuts'}
for c in cr:
  if c['title'].startswith('Afi Catalog'): c['title']=AFIFIX.get((c['person'],c['year']),c['title'])
cr=[c for c in cr if not c['title'].startswith("L'Incroyable Hulk")]
for c in cr:
  if c['title']=='Extraction II': c['title']='Extraction 2'
for c in cr:
  if c['title']=="Jane Austen's Mafia!": c['title']='Mafia!'

import unicodedata
_R={'ii':'2','iii':'3','iv':'4','v':'5','vi':'6','vii':'7','viii':'8'}
def _norm(t):
  t=unicodedata.normalize('NFKD',t).encode('ascii','ignore').decode().lower().replace('&',' and ')
  t=re.sub(r"[^a-z0-9 ]"," ",t); w=[_R.get(x,x) for x in t.split()]
  w=[x for x in w if x not in ('the','a','part','chapter')]
  return ' '.join(w)
def _iid(c):
  m=re.search(r'tt\d+',c.get('imdb') or ''); return m.group(0) if m else None
_cl=[]
for c in cr:
  n,i=_norm(c['title']),_iid(c)
  for g in _cl:
    if (i and i in g['ids'] and (n.startswith(g['n']) or g['n'].startswith(n))) or (n==g['n'] and (c.get('type')=='tv' or g['tv'] or abs(c['year']-g['y'])<=1)):
      g['m'].append(c); i and g['ids'].add(i); break
  else: _cl.append(dict(n=n,y=c['year'],tv=c.get('type')=='tv',ids={i} if i else set(),m=[c]))
MERGED=[]
for g in _cl:
  ts={c['title'] for c in g['m']}
  if len(ts)>1 or len({c['year'] for c in g['m']})>1:
    best=max(g['m'],key=lambda c:(bool(c.get('poster')),bool(c.get('imdb')),c.get('boxOffice') is not None))
    y=min(c['year'] for c in g['m']); MERGED.append((sorted(ts),y))
    for c in g['m']:
      c['title']=best['title']; c['year']=y
      for k in ('poster','imdb','boxOffice','boxOfficeSource','tmdb'):
        if not c.get(k) and best.get(k): c[k]=best[k]
json.dump(MERGED,open('merged_report.json','w'),indent=1)
for c in cr:
  if c['person'].startswith('Victor "Vic" Orsatti'): c['person']='Vic Orsatti (1905–1984)'
_seen=set();cr=[c for c in cr if not ((c['person'],c['title'],c['year']) in _seen or _seen.add((c['person'],c['title'],c['year'])))]
OV=json.load(open('poster_override.json'))
FIX={'Cop & 1/2':dict(imdb='https://www.imdb.com/title/tt0106613/',poster='posters/tt0106613.jpg',boxOffice=40700000,boxOfficeSource='https://en.wikipedia.org/wiki/Cop_and_a_Half'),
'Big Love':dict(imdb='https://www.imdb.com/title/tt0421030/',poster=None,boxOffice=None,boxOfficeSource=None),
'Stranger Things':dict(imdb='https://www.imdb.com/title/tt4574334/',poster=None,boxOffice=None,boxOfficeSource=None),
'Stop at Nothing':dict(boxOffice=None,boxOfficeSource=None),'Moonlight':dict(boxOffice=None,boxOfficeSource=None),
'The Swarm':dict(boxOffice=None),'Highlander II: The Quickening':dict(boxOffice=None),
'Avengers: Endgame':dict(boxOffice=2799439100,boxOfficeSource='https://en.wikipedia.org/wiki/Avengers:_Endgame')}
for c in cr:
  c.update(FIX.get(c['title'],{}))
  if c['title']=='The Poseidon Adventure' and c['person'].startswith('Ernie F'): c['role']='Terry (actor) – performed the famous 32-ft skylight fall'
for c in cr:
  if c['title']=='Death on the Diamond': c['source']='https://www.baseballamore.com/orsattie/'
  if c['title'] in('The Poseidon Adventure','The Towering Inferno'): c['source']='https://en.wikipedia.org/wiki/Ernie_Orsatti'
W='https://en.wikipedia.org/wiki/Ernie_Orsatti'; S='https://sabr.org/bioproj/person/ernie-orsatti/'; V='https://en.wikipedia.org/wiki/Victor_Orsatti'
funfacts={
 'B.S. I Love You':[{'text':'Frank H. Orsatti jumped off the Golden Gate Bridge for this film.','source':'https://stuntsunlimited.com/frank-orsatti-honorary/'}],
 'Serpico':[{'text':'Frank H. Orsatti was the film\'s stunt coordinator.','source':'https://variety.com/2005/scene/people-news/frank-orsatti-1117915927/'}],
 'Highlander II: The Quickening':[{'text':'Frank H. Orsatti was the film\'s stunt coordinator.','source':'https://variety.com/2005/scene/people-news/frank-orsatti-1117915927/'}],
 'The Magician':[{'text':'Frank H. did stunts on this Bill Bixby series, then followed Bixby to The Incredible Hulk as his double and stunt coordinator.','source':'https://variety.com/2005/scene/people-news/frank-orsatti-1117915927/'}],
 'Planet of the Apes':[{'text':'Frank H. Orsatti\'s first stunt job (1968). Drafted by the Cardinals, an injury ended his baseball career; he spent ten years in the Merchant Marine before stunts.','source':'https://stuntsunlimited.com/frank-orsatti-honorary/'}],
 'The Practice':[{'text':'Noon Orsatti is credited as a stunt double on seasons 2 and 4.','source':'https://app.productionbeast.com/12248-noon-orsatti'}],
 'Agatha All Along':[{'text':'Rowbie doubled Joe Locke as Wiccan.','source':'family (Rowbie); https://www.imdb.com/name/nm1769066/'}],
 'American History X':[{'text':'Noon Orsatti and Ernie F. Orsatti created the film\'s infamous curb-stomp scene (family account). Both are credited as the film\'s stunt coordinators.','source':'family; https://www.themoviedb.org/person/1407364-noon-orsatti; https://www.hollywoodreporter.com/news/general-news/ernie-orsatti-stuntman-who-took-quite-the-fall-in-the-poseidon-adventure-dies-at-80-4063318/'}],
 'Stolen':[{'text':'Stuntman-actor Kevin Foster got his role through Noon, the film\'s stunt coordinator: "It all started with Noon." The same route landed him his part in the first Iron Man.','source':'https://mattjhorn.wordpress.com/2013/04/02/kevin-foster-stolen-2013/'}],
 'Hill Street Blues':[{'text':'Ernie F. Orsatti was thrown through a window in the 1981 pilot.','source':'https://www.hollywoodreporter.com/news/general-news/ernie-orsatti-stuntman-who-took-quite-the-fall-in-the-poseidon-adventure-dies-at-80-4063318/'}],
 'The Mechanic':[{'text':'Ernie F. appears as the "Chicken Lickin driver."','source':'https://catalog.afi.com/Person/218285-Ernie-Orsatti'}],
 'The Incredible Hulk':[{'text':'Frank H. Orsatti doubled both sides of the show: Bill Bixby as David Banner, and the Hulk himself. He was also the series\' stunt coordinator, directed twelve episodes, and hired Manny Perry to double Lou Ferrigno.','source':'Orsatti family; https://stuntsunlimited.com/frank-orsatti-honorary/'}],
 'Mafia!':[{'text':'Rowbie Orsatti was set to play the kid in the Forrest Gump parody scene, but, afraid of wearing the leg braces, told his grandfather (Ernie F. Orsatti, the film\'s second-unit director) he wasn\'t interested.','source':'family (Rowbie Orsatti)'}],
 'Project X':[{'text':'Rowbie Orsatti doubled lead actor Thomas Mann (per Rowbie; IMDb lists his stunt credit on the film).','source':'https://www.imdb.com/name/nm1769066/'}],
 'Sherlock Jr.':[{'text':'Ernie was hired as assistant prop man because Buster Keaton was a huge baseball fan who insisted on playing ball on the sets of all his films.','source':'https://www.imdb.com/name/nm1108143/'},{'text':'At 5\'7" and 150 lb, Ernie was a close physical match for Keaton (5\'6", 140 lb) and doubled him in a scene in this film; SABR notes Keaton otherwise did his own stunts.','source':'https://sabr.org/bioproj/person/ernie-orsatti/'}],
 'Our Hospitality':[{'text':'In the early 1920s Ernie doubled for Keaton and captained Keaton\'s amateur baseball team.','source':W}],
 'Death on the Diamond':[{'text':'The scene was filmed at Sportsman\'s Park on June 26, 1934, before a Cardinals–Giants game – in the middle of the Gashouse Gang\'s championship season.','source':'https://www.baseballamore.com/orsattie/'}],
 'The Poseidon Adventure':[{'text':'Ernie F. Orsatti is best known for his free fall into a skylight in this film.','source':W},{'text':'He was cast as Terry (Pamela Sue Martin\'s boyfriend), not as a stuntman, when asked to do the 32-ft fall. Gene Hackman came to watch: "We\'ve all come to watch you die." One take; it knocked him "colder than a cucumber."','source':'https://www.hollywoodreporter.com/news/general-news/ernie-orsatti-stuntman-who-took-quite-the-fall-in-the-poseidon-adventure-dies-at-80-4063318/'}],
 'Borderlands':[{'text':'Noon: "Chad Stahelski used to work for me, Dave Leitch used to work for me, and Sam Hargrave used to work for me."','source':'https://www.digitaltrends.com/movies/borderlands-interview-stunts-jimmy-odee-noon-orsatti/'}],
 'The Towering Inferno':[{'text':'Played a hero firefighter hanging on to the scenic elevator.','source':W}],
 'The Terminator':[{'text':'Frank H. Orsatti doubled for Arnold Schwarzenegger.','source':'https://www.imdb.com/name/nm0650685/'}],
 'Extraction 2':[{'text':'Noon drove Chris Hemsworth\'s SUV from a hidden rear seat in the forest chase – "the most dangerous work I\'ve ever had in my career."','source':'https://decider.com/2023/06/16/extraction-2-director-interview-21-minute-one-shot-take/'},{'text':'Noon\'s lead stunt coordination earned him a Taurus World Stunt Award (per his IMDb bio).','source':'https://www.imdb.com/name/nm0650687/'},{'text':'Two generations on one film: Noon and his son Rowbie both have stunt credits.','source':'https://www.imdb.com/name/nm1769066/'}],
 'A Nightmare on Elm Street 4: The Dream Master':[{'text':'Noon is credited as a stunt player (AFI Catalog). A claim that he doubled Freddy Krueger could NOT be verified – AFI lists him among general stunt players only.','source':'https://catalog.afi.com/Catalog/moviedetails/58990'}],
}
milestones=[
 dict(year=1925,kind='milestone',title='Vic quarterbacks USC',text='Vic Orsatti played quarterback (No. 5) for Howard Jones\'s 1925 and 1926 USC Trojans, and also played baseball and ran track at USC.',sources=['https://en.wikipedia.org/wiki/Victor_Orsatti']),
 dict(year=1970,kind='milestone',title='Stunts Unlimited',text='Frank H. Orsatti was one of the original members of Stunts Unlimited, the elite stunt association co-founded by Hal Needham, Ronnie Rondell and Glenn Wilder. In 2019 the group named him an honorary member. He started in stunts in 1968 on Planet of the Apes, jumped off the Golden Gate Bridge for B.S. I Love You, doubled Burt Reynolds for nine years, and directed twelve episodes of The Incredible Hulk.',sources=['https://stuntsunlimited.com/frank-orsatti-honorary/'],flag='Founding year 1970 per Stunts Unlimited history; Frank described as an original member'),
 dict(year=1978,kind='quote',title='"Frank Orsatti created a stunt legacy."',text='"…he gave so many second unit directors and stunt coordinators their first breaks as stunt performers, myself included." – Manny Perry, Stunts Unlimited, on being hired by Frank to double Lou Ferrigno on The Incredible Hulk.',sources=['https://stuntsunlimited.com/frank-orsatti-honorary/']),
 dict(year=1998,kind='milestone',title='Rowbie Orsatti\'s first credit: Charmed',text='Rowbie Orsatti\'s first screen credit came on Charmed in 1998, a show the family ran for years: his grandfather Ernie F. Orsatti was its stunt coordinator (37 episodes), and his father Noon Orsatti also worked on the series.',sources=['https://www.imdb.com/name/nm1769066/','https://www.themoviedb.org/person/112572-ernie-f-orsatti','family']),
 dict(year=2001,kind='milestone',title='Rowbie Orsatti joins SAG',text='Rowbie Orsatti becomes a member of the Screen Actors Guild – the union Ken Orsatti led as national executive director from 1981 to 2000.',sources=['family']),
 dict(year=1999,kind='milestone',title='The Orsatti TV years',text='Through the late 1990s and 2000s Ernie F. and Noon Orsatti coordinated stunts across a remarkable run of network and cable series – Charmed, Carnivàle, Entourage, It\'s Always Sunny in Philadelphia, Nip/Tuck, The Closer, Big Love and more. The family recalls a stretch when father and son were running more shows than anyone in town.',sources=['https://www.imdb.com/name/nm0650683/','https://www.imdb.com/name/nm0650687/','family']),
 dict(year=1928,kind='lore',title='Bootleggers to the studios',text='Family lore holds that the Orsatti brothers supplied Hollywood – and MGM in particular – during Prohibition. The documented pieces: author Tim Adler says Frank got into the movie business by supplying Louis B. Mayer with alcohol and women; Weaver et al. call Frank "a former bootlegger"; and father Morris was convicted (1922–25) of bribing a Prohibition agent.',sources=['https://en.wikipedia.org/wiki/Victor_Orsatti (citing Adler, Hollywood and the Mob)','Tom Weaver, David Schecter & Robert J. Kiss, Universal Terrors, 1951–1955 (McFarland, 2017)','https://hallapproved.com/us/cases/ca9/1925/6757913/'],flag='Lore, partly documented'),
 dict(year=1936,kind='lore',title='Vic\'s spaghetti parties',text='A period news photo shows Al and Victor Orsatti with Alice Faye, James Stewart, Rochelle Hudson and Shirley Ross at "one of Victor Orsatti\'s famous Hollywood spaghetti parties."',sources=['https://www.gettyimages.com.au/detail/news-photo/al-orsatti-rochelle-hudson-victor-orsatti-shirley-ross-news-photo/646310372'],flag='Photo caption; exact year unknown'),
 dict(year=1936,kind='business',title='Bringing Sonja Henie to Hollywood',text='Vic is credited with persuading three-time Olympic figure-skating champion Sonja Henie to move to Hollywood after the 1936 Winter Olympics; she became one of its highest-paid stars. In 1939 Louella Parsons reported their romance was "the talk of Hollywood."',sources=['https://en.wikipedia.org/wiki/Victor_Orsatti']),

 dict(year=1902,kind='milestone',title='Ernest Ralph Orsatti is born',text='Born Sept 8, 1902 in Los Angeles, sixth of seven children of Italian immigrants Maurizio and Maria (Manze) Orsatti – anglicized to Morris and Mary. Morris had been a tailor in Philadelphia; in Los Angeles he owned the International Steamship and Railroad Ticket Agency.',sources=['https://sabr.org/bioproj/person/ernie-orsatti/','https://en.wikipedia.org/wiki/Victor_Orsatti'],flag='Emigration date, ship and Italian hometown not found'),
 dict(year=1920,kind='keaton',title='Quitting school for the movies',text='"My interest, as a boy, was in motion pictures and not in baseball… In 1920, I decided to quit school and devote all my time to the picture business." He worked as a gofer, then a stuntman: wing-walking, cliff dives, car and boat stunts. From 1922 he was Keaton\'s prop man and bit player, and played first base and catcher on Keaton\'s team (1922–25).',sources=['https://sabr.org/bioproj/person/ernie-orsatti/ (citing The Sporting News, Feb 4, 1932)']),
 dict(year=1922,kind='mob',title='Morris Orsatti and the Prohibition agent',text='A federal indictment charged Morris Orsatti with promising and paying bribes to Prohibition agent Harold H. Dolley (from June 1922) to drop or reduce cases against arrested liquor-law violators. Convicted on all 21 counts; the Ninth Circuit affirmed in Orsatti v. United States, 3 F.2d 778 (Feb 2, 1925), and the Supreme Court denied review on May 4, 1925.',sources=['https://hallapproved.com/us/cases/ca9/1925/6757913/','https://www.govinfo.gov/content/pkg/USREPORTS-268/pdf/USREPORTS-268-BackMatter.pdf'],flag='Court record; identity with the patriarch is strongly implied (Los Angeles, same name) but not stated in the opinion'),
 dict(year=1923,kind='quote',title='Babe Ruth\'s bat',text='Ernie\'s brother Vic, named best all-around high-school athlete in Los Angeles, won the bat Babe Ruth used for the first home run at Yankee Stadium (April 18, 1923) in a Los Angeles Evening Herald home-run contest. It sold in 2004 for about $1.26 million.',sources=['https://en.wikipedia.org/wiki/Victor_Orsatti','https://sabr.org/bioproj/person/ernie-orsatti/']),
 dict(year=1926,kind='baseball',title='Climbing the Cardinals farm',text='Branch Rickey bought his contract after seeing him hit .347 at Cedar Rapids (1925). He hit .386 at Omaha in 1926 and .330 at Houston in 1927, then .381 with 15 HR at Minneapolis in 1928. On Aug 24, 1928 his first-inning homer beat the Phillies 1–0 and kept St. Louis in first place.',sources=['https://sabr.org/bioproj/person/ernie-orsatti/']),
 dict(year=1932,kind='baseball',title='Best season: .336 – and Rickey\'s phone trick',text='Ernie hit .336 (sixth in the NL). When he asked Branch Rickey for a raise over $4,500, Rickey took two "calls" from farm clubs asking for an outfielder; Ernie asked only for a pen to sign. Bill Veeck Sr. later said the calls were fake, rung by a foot pedal under Rickey\'s desk.',sources=['https://sabr.org/bioproj/person/ernie-orsatti/ (citing Toledo Blade, Apr 1, 1972)'],flag='Anecdote'),
 dict(year=1934,kind='quote',title='"Orsatti was a showman."',text='Teammate Jim Mooney recalled him catching a line drive and turning "two or three somersaults." In the 1934 World Series he played all seven games, hitting .318. Detroit fans were still bitter 25 years later: Frankie Frisch said a Detroit hotel clerk refused Ernie a room.',sources=['https://sabr.org/bioproj/person/ernie-orsatti/']),
 dict(year=1960,kind='business',title='Orsatti Bail Bonds',text='Ernie married Alice Joyce Ritchie in 1960 and ran Orsatti Bail Bonds in Van Nuys with her until his death on Sept 4, 1968. He is buried at San Fernando Mission Cemetery. His son Ernie F. remembered him as a great athlete and a talented chef who cooked Christmas Eve dinner for dozens of show-business and opera guests.',sources=['https://sabr.org/bioproj/person/ernie-orsatti/']),
 dict(year=1963,kind='baseball',title='Frank H. tries the family game',text='Ernie\'s son Frank played 12 games for the Cardinals\' affiliate Brunswick (Georgia-Florida League) in 1963 before an injury ended his career; he later spent ten years in the Merchant Marine before becoming a stuntman.',sources=['https://sabr.org/bioproj/person/ernie-orsatti/','https://www.imdb.com/name/nm0650685/']),

 dict(year=1923,kind='milestone',title='The Orsatti family begins in Hollywood',text='1923 is the founding year on the family\'s own crest (est. 1923); Noon Orsatti\'s IMDb bio also says the Orsatti name has been synonymous with film making since 1923.',sources=['family logo','https://www.imdb.com/name/nm0650687/'],flag='Per family logo; no independent record found'),
 dict(year=1925,kind='keaton',title='Fired… into pro baseball',text='Per Keaton biographer James Curtis, Ernie "was so good that one day in 1925 he arrived at work and found a new set of luggage and a check…and was told he was fired. Keaton handed him a contract to play for the Vernon Tigers."',sources=[W+' (citing Curtis, Buster Keaton: A Filmmaker\'s Life, 2022, p.280)']),
 dict(year=1927,kind='baseball',title='MLB debut – St. Louis Cardinals',text='Ernie debuts September 4, 1927. Career 1927–35: 701 games, .306 average, 663 hits, 10 HR, 237 RBI. Bats and throws left.',sources=[W,'https://www.baseball-reference.com/players/o/orsater01.shtml']),
 dict(year=1931,kind='baseball',title='World Series champion',text='Ernie played in four World Series (1928, 1930, 1931, 1934), winning in 1931 and 1934; .273 across 13 Series games.',sources=[W]),
 dict(year=1932,kind='quote',title='"The envy of most of the younger players"',text='"His flashy sweaters, golf hose, knickers and sports suits are Hollywood importations, and his wardrobe is the envy of most of the younger players." – The Sporting News, 1932. SABR: "Ernie\'s ensembles made him stand out like a peacock in the ranks of the Gashouse Gang."',sources=[S]),
 dict(year=1934,kind='baseball',title='Gashouse Gang – 1934 champions',text='Ernie was part of the famously scruffy 1934 "Gashouse Gang" Cardinals who won the World Series; he drove in both of his career Series RBIs that fall.',sources=[W,S]),
 dict(year=1930,kind='business',title='Frank Orsatti opens the Orsatti Agency',text='"In 1930, their son Frank, a former bootlegger, went into the agency business and brought in his brothers Al, Victor and Ernie. The Orsatti Agency represented actors, executives, producers, directors, writers and radio talent." The same book says father Morris Orsatti, a bank vice-president, had ties to organized crime and "spent time up the river in the 1920s."',sources=['Tom Weaver, David Schecter & Robert J. Kiss, Universal Terrors, 1951–1955 (McFarland, 2017), This Island Earth chapter'],flag='Single published source; father\'s prison term not independently verified'),
 dict(year=1949,kind='business',title='Victor takes charge',text='"By 1949 Frank and Al were dead of heart attacks (at 53 and 48, respectively) and Victor took charge."',sources=['Tom Weaver, David Schecter & Robert J. Kiss, Universal Terrors, 1951–1955 (McFarland, 2017), This Island Earth chapter']),
 dict(year=1935,kind='business',title='The Orsatti Talent Agency',text='After his last MLB game (Sept 28, 1935) Ernie joins brothers Frank, Vic and Al in the Orsatti Talent Agency. Clients included Judy Garland, Sonja Henie, Betty Grable, Edward G. Robinson, Margaret O\'Brien, Alice Faye, Frank Capra and George Stevens. His son called it the largest agency in Hollywood.',sources=[S,V],flag='Closing date not found'),
 dict(year=1937,kind='mob',title='Frank Orsatti & the Wizard of Oz',text='Agent Frank Orsatti told MGM producer Arthur Freed that Samuel Goldwyn held the rights to The Wizard of Oz – the film that made Orsatti client Judy Garland a legend. Vic Orsatti negotiated her Dorothy contract.',sources=['https://web.archive.org/web/20070907233032/http:/thewizardofoz.warnerbros.com/movie/cmp/timeline.html',V]),
 dict(year=1938,kind='mob',title='"Handling all of MGM\'s dirty work"',text='Author Tim Adler (Hollywood and the Mob, 2011) called Frank Orsatti "a bootlegger and gangster" who got into the movie business by supplying Louis B. Mayer with alcohol and women, with a reputation for "handling all of MGM\'s \'dirty work\'." Adler called Vic a "gangster-cum-agent." Allegations from one author, not court findings.',sources=[V],flag='Reputation/allegation'),
 dict(year=1939,kind='baseball',title='One last season',text='Ernie returns for 1939 with the Hollywood Stars (PCL) and Columbus. The New York Times said Orsatti, "now an actors\' agent, is expected to prove a strong drawing card in the film colony."',sources=[S]),
 dict(year=1943,kind='quote',title='"Husbands are much easier to find than good agents."',text='Actress Marie "The Body" McDonald (married to Vic Orsatti 1943–47, formerly Bugsy Siegel\'s girlfriend) kept him as her agent after the divorce.',sources=[V]),
 dict(year=1947,kind='mob',title='The Bugsy Siegel connection',text='Vic Orsatti\'s wife Marie McDonald had previously been Bugsy Siegel\'s girlfriend (Wikipedia, citing Tim Adler). A fan-history site further claims that during her 1947 Las Vegas divorce stay from Orsatti she rode the Flamingo Hotel float for Siegel – that detail is from a non-scholarly source.',sources=[V,'http://www.glamourgirlsofthesilverscreen.com/show/183/Marie++McDonald/'],flag='Second-hand / partly lore'),
 dict(year=1945,kind='business',title='Ernie Orsatti\'s Oddity Shop and Florist',text='In the mid-1940s Ernie opened an oddity shop and florist on Sunset Boulevard (with his brothers-in-law, per Wikipedia). Business cards: Cardinals redbirds perched on a bat. He also held a patent on a candy-vending machine, collecting royalties on candy sold in most Southern California theater lobbies.',sources=[S,W],flag='Year approximate ("mid-1940s")'),
 dict(year=1946,kind='business',title='"Third from the top"',text='The St. Louis Star and Times (Oct 1, 1946) said the Orsatti agency was "third from the top where movie actors\' agents get together."',sources=[W]),
 dict(year=1956,kind='business',title='Saber Productions & Rorvic Productions',text='Vic Orsatti\'s Saber Productions produced films incl. Flight to Hong Kong (1956); Rorvic Productions (with Rory Calhoun) made CBS\'s The Texan.',sources=[V]),
 dict(year=1981,kind='business',title='Ken Orsatti: SAG National Executive Director',text='Ken Orsatti (1932–2010), SAG national executive director 1981–2000, negotiated ~20 major contracts and helped found the SAG Foundation. Sources call him national executive director (the Guild\'s top staff executive and chief negotiator), not SAG president (an elected actor post). Born Alfred Kendall Orsatti; his father and two uncles ran the Orsatti Agency, so he was Ernie\'s nephew (most likely Al\'s son).',sources=['https://variety.com/2010/scene/people-news/former-sag-chief-orsatti-dies-1118023607/','https://www.latimes.com/local/obituaries/la-me-passings-20100902-story.html'],flag='Which brother was his father is inferred from his name (Alfred)'),
 dict(year=1961,kind='business',title='Ken Orsatti joins SAG',text='Ken Orsatti starts at the Screen Actors Guild as a theatrical business rep; Southwest regional director 1966; Hollywood exec director 1971–81.',sources=['https://variety.com/2010/scene/people-news/former-sag-chief-orsatti-dies-1118023607/','https://www.latimes.com/local/obituaries/la-me-passings-20100902-story.html'],),
 dict(year=2024,kind='milestone',title='Taurus World Stunt Award',text='Noon Orsatti wins the Taurus World Stunt Award for Best Stunt Coordinator and/or 2nd Unit Director for Extraction 2 – the third generation of the family in film.',sources=['https://en.wikipedia.org/wiki/Taurus_World_Stunt_Awards','https://www.imdb.com/name/nm0650687/']),
]
C="https://commons.wikimedia.org/wiki/Special:FilePath/"
PH={"Quitting school for the movies":[dict(src=C+"Buster_Keaton_with_writers_and_director_in_1923.jpg?width=900",caption="Buster Keaton (centre) with his writers and director, 1923 – the Keaton unit Ernie joined (Ernie not pictured)",source="https://commons.wikimedia.org/wiki/File:Buster_Keaton_with_writers_and_director_in_1923.jpg"),dict(src=C+"Buster_keaton_in_sherlock_jr,_1924.jpg?width=900",caption="Buster Keaton in Sherlock Jr. (1924), the film in which Ernie doubled him",source="https://commons.wikimedia.org/wiki/File:Buster_keaton_in_sherlock_jr,_1924.jpg")],"Fired… into pro baseball":[dict(src="photos/ernie-action.jpg",caption="Ernie Orsatti fielding, press photo (public domain, via DPLA)",source="https://commons.wikimedia.org/wiki/File:Ernest_Orsatti_-_DPLA_-_9bca1ab5bc3cc804eea874cbf130f097.jpg")],"MLB debut – St. Louis Cardinals":[dict(src="photos/ernie-goudey-1933-pd.jpg",caption="Ernie Orsatti, 1933 Goudey card #201 (public domain)",source="https://commons.wikimedia.org/wiki/File:ErnieOrsattiGoudeycard.jpg")],"World Series champion":[dict(src="photos/ernie-action.jpg",caption="Ernie Orsatti, Cardinals-era press photo (public domain, via DPLA)",source="https://commons.wikimedia.org/wiki/File:Ernest_Orsatti_-_DPLA_-_9bca1ab5bc3cc804eea874cbf130f097.jpg")],"Gashouse Gang – 1934 champions":[dict(src="photos/ernie-goudey-1933-pd.jpg",caption="Ernie Orsatti, 1933 Goudey card (public domain)",source="https://commons.wikimedia.org/wiki/File:ErnieOrsattiGoudeycard.jpg")]}
for _m in milestones:
  if _m["title"] in PH: _m["photos"]=PH[_m["title"]]
PH2={'Stunts Unlimited':[dict(src=C+'Bill_Bixby_Lou_Ferrigno_Incredible_Hulk_1977.jpg?width=900',caption="Bill Bixby and Lou Ferrigno in The Incredible Hulk (1977 publicity photo). Frank H. Orsatti doubled both Bixby's David Banner and the Hulk, and coordinated the show's stunts (Frank not pictured)",source='https://commons.wikimedia.org/wiki/File:Bill_Bixby_Lou_Ferrigno_Incredible_Hulk_1977.jpg')],'"Frank Orsatti created a stunt legacy."':[dict(src=C+'Lou_Ferrigno_Incredible_Hulk.jpg?width=900',caption='Lou Ferrigno as the Hulk (1977 publicity photo) – Manny Perry, hired by Frank, doubled him',source='https://commons.wikimedia.org/wiki/File:Lou_Ferrigno_Incredible_Hulk.jpg')],'Vic quarterbacks USC':[dict(src=C+"Howard_Jones'_Trojans_Prepare_for_Iowa_Eleven,_1925.jpg?width=900",caption="USC Trojans players preparing for Iowa, 1925 – Howard Jones's squad that Vic quarterbacked (Vic not identified in this photo)",source="https://commons.wikimedia.org/wiki/File:Howard_Jones'_Trojans_Prepare_for_Iowa_Eleven,_1925.jpg"),dict(src=C+'Howard_Jones_and_the_USC_football_team_at_the_Coliseum.jpg?width=900',caption='Coach Howard Jones and the USC football team at the Coliseum (Vic not identified)',source='https://commons.wikimedia.org/wiki/File:Howard_Jones_and_the_USC_football_team_at_the_Coliseum.jpg')],'Bringing Sonja Henie to Hollywood':[dict(src=C+'Sonja_Henie_1936.jpg?width=900',caption='Sonja Henie at the 1936 Winter Olympics – after which Vic persuaded her to try Hollywood',source='https://commons.wikimedia.org/wiki/File:Sonja_Henie_1936.jpg'),dict(src=C+'Sonja_Henie_on_Time_Magazine_1939.jpg?width=900',caption='Sonja Henie on the cover of Time, July 17, 1939 – by then a top 20th Century-Fox star',source='https://commons.wikimedia.org/wiki/File:Sonja_Henie_on_Time_Magazine_1939.jpg')],'The Bugsy Siegel connection':[dict(src=C+'Bugsy_Siegel.jpg?width=900',caption='Benjamin "Bugsy" Siegel, police mugshot, April 12, 1928 (public domain)',source='https://commons.wikimedia.org/wiki/File:Bugsy_Siegel.jpg')],'Quitting school for the movies':[dict(src=C+'Our_Hospitality_(1923)_Poster.jpg?width=900',caption="Poster for Buster Keaton's Our Hospitality (1923), from the era Ernie worked in Keaton's unit",source='https://commons.wikimedia.org/wiki/File:Our_Hospitality_(1923)_Poster.jpg')]}
for _m in milestones:
  if _m['title'] in PH2: _m['photos']=_m.get('photos',[])+PH2[_m['title']]

PH3={"Babe Ruth's bat":[dict(src=C+'Babe_Ruth,_at_opening_of_Yankee_Stadium_(baseball)_LCCN2014715919.jpg?width=900',caption='Babe Ruth at the opening of Yankee Stadium, April 18, 1923 – the day he hit the home run with the bat Vic later won (Library of Congress)',source='https://commons.wikimedia.org/wiki/File:Babe_Ruth,_at_opening_of_Yankee_Stadium_(baseball)_LCCN2014715919.jpg')],'Climbing the Cardinals farm':[dict(src=C+'Branch_Rickey_and_Bert_Shotten,_1924_photo_by_Underwood.jpg?width=900',caption='Branch Rickey (with Burt Shotton), 1924 – architect of the Cardinals farm system Ernie came up through',source='https://commons.wikimedia.org/wiki/File:Branch_Rickey_and_Bert_Shotten,_1924_photo_by_Underwood.jpg')],"Best season: .336 – and Rickey's phone trick":[dict(src=C+'Branch_Rickey_Cardinals.jpg?width=900',caption='Branch Rickey, St. Louis Cardinals team photo, c. 1941',source='https://commons.wikimedia.org/wiki/File:Branch_Rickey_Cardinals.jpg')],'"Husbands are much easier to find than good agents."':[dict(src=C+'Marie_McDonald.jpg?width=900',caption='Marie McDonald, Yank pin-up, Sept. 8, 1944 – married to Vic Orsatti 1943–47',source='https://commons.wikimedia.org/wiki/File:Marie_McDonald.jpg')],'The Bugsy Siegel connection':[dict(src=C+'Marie_McDonald.jpg?width=900',caption="Marie McDonald, 1944 – Vic's wife, later linked to Siegel",source='https://commons.wikimedia.org/wiki/File:Marie_McDonald.jpg'),dict(src=C+'John_Roselli_LA_mug_shot_(1948).jpg?width=900',caption="Johnny Roselli, Los Angeles mug shot, July 27, 1948 – later married June Lang, Vic's first wife",source='https://commons.wikimedia.org/wiki/File:John_Roselli_LA_mug_shot_(1948).jpg')],'Frank Orsatti & the Wizard of Oz':[dict(src=C+'Judy_Garland_Over_the_Rainbow_2.jpg?width=900',caption='Judy Garland singing "Over the Rainbow" in The Wizard of Oz (1939), from the 1940 trailer',source='https://commons.wikimedia.org/wiki/File:Judy_Garland_Over_the_Rainbow_2.jpg')],'The Orsatti Talent Agency':[dict(src=C+'1940_Mickey_Rooney_and_Judy_Garland_publicity_photo_for_Strike_up_the_Band,_1940.webp?width=900',caption='Mickey Rooney and Judy Garland, Strike Up the Band publicity photo, 1940 – Garland was an Orsatti client',source='https://commons.wikimedia.org/wiki/File:1940_Mickey_Rooney_and_Judy_Garland_publicity_photo_for_Strike_up_the_Band,_1940.webp')],'Saber Productions & Rorvic Productions':[dict(src=C+'Rory_Calhoun_by_Gene_Kornman,_1953.jpg?width=900',caption="Rory Calhoun by Gene Kornman, 1953 – Vic's partner in Rorvic Productions (Rory + Vic)",source='https://commons.wikimedia.org/wiki/File:Rory_Calhoun_by_Gene_Kornman,_1953.jpg')]}
for _m in milestones:
  if _m['title'] in PH3: _m['photos']=_m.get('photos',[])+PH3[_m['title']]

people=[
 dict(name='Al Orsatti',year=1935,relation='Brother of Ernie Orsatti',relationSource='SABR; Wikipedia',note='Agency partner with Frank, Vic and Ernie; his clients included actress Peggy O\'Neill. Died by 1949 of a heart attack, aged 48 (Weaver et al.). Likely father of SAG leader Ken (Alfred Kendall) Orsatti – inferred.'),
 dict(name='Vic Orsatti',birthName='Victor Manuel Orsatti',photos=[dict(src='https://commons.wikimedia.org/wiki/Special:FilePath/June_Lang_by_Otto_Dyar,_1930s.jpg?width=900',caption='June Lang, Vic Orsatti\'s first wife (m. 1937), portrait by Otto Dyar, 1930s',source='https://commons.wikimedia.org/wiki/File:June_Lang_by_Otto_Dyar,_1930s.jpg')],relation='Brother of Ernie Orsatti',relationSource='Wikipedia; SABR',years='1905–1984',year=1937,photo='photos/victor-orsatti.png',photoCaption='1923 high-school football photo (public domain)',photoSource='https://commons.wikimedia.org/wiki/File:Victor_Orsatti.png',note='Ernie\'s brother: USC quarterback, agent to Judy Garland and Sonja Henie, later a producer. Formed Sabre Productions on Sept 17, 1953, planning This Island Earth as its first film (the picture was made at Universal). Producer credits: Flight to Hong Kong (assoc., 1956), Ride Out for Revenge (assoc., 1957), Domino Kid and The Hired Gun (1957), Apache Territory (1958), A Face in the Rain (exec., 1963), plus the CBS western The Texan (1958–60) with Rory Calhoun. Earliest credit: script clerk on Spring Fever (1927). Born Victor Manuel Orsatti in Los Angeles, Nov 25, 1905; died Newport Beach, June 9, 1984; interred at Pacific View Memorial Park, Corona del Mar. Mob-adjacent orbit: his first wife June Lang (m. 1937) later married Outfit figure Johnny Roselli; second wife Marie "The Body" McDonald reportedly had an affair with Bugsy Siegel in Las Vegas while divorcing him (1947). Photos (link only): with RKO starlet Frances Neal at the Citizen Kane premiere, 1941 (Variety); at Victor Orsatti\'s spaghetti party with Al, Alice Faye and James Stewart (Getty).',photoLinks=[dict(caption='Vic Orsatti & Frances Neal, Citizen Kane premiere, 1941 (Variety)',url='https://variety.com/gallery/citizen-kane-premiere-anniversary-photos/'),dict(caption='Spaghetti party with Al Orsatti, Rochelle Hudson, Shirley Ross (Getty)',url='https://www.gettyimages.com.au/detail/news-photo/al-orsatti-rochelle-hudson-victor-orsatti-shirley-ross-news-photo/646310372')],noteSources=['https://catalog.afi.com/Person/151138-Victor-M.-Orsatti','https://en.wikipedia.org/wiki/Rorvic_Productions','https://www.findagrave.com/memorial/26911562/victor_m-orsatti','https://www.glamourgirlsofthesilverscreen.com/show/213/Vic+Orsatti/index.html (citing Crivello, Fallen Angels; Strait, Queen of Ice)','Weaver, Schecter & Kiss, Universal Terrors 1951–1955 (McFarland, 2017)']),
 dict(name='Ernie Orsatti',birthName='Ernest Ralph Orsatti',nameSources=['https://www.baseball-reference.com/players/o/orsater01.shtml','https://sabr.org/bioproj/person/ernie-orsatti/','https://en.wikipedia.org/wiki/Ernie_Orsatti'],year=1923,photo='photos/ernie-portrait.jpg',photoCaption='Ernie Orsatti, St. Louis Cardinals era press photo (public domain, via DPLA)',photoSource='https://commons.wikimedia.org/wiki/File:Ernest_Orsatti_-_DPLA_-_9bca1ab5bc3cc804eea874cbf130f097.jpg',photos=[dict(src='photos/ernie-goudey-1933-pd.jpg',caption='1933 Goudey card #201 (public domain)',source='https://commons.wikimedia.org/wiki/File:ErnieOrsattiGoudeycard.jpg')],years='1902–1968',imdb='https://www.imdb.com/name/nm1108143/',note='Keaton prop man/stuntman, Cardinals outfielder, agent.'),
 dict(name='Frank Orsatti (agent)',year=1930,relation='Brother of Ernie Orsatti',relationSource='Wikipedia; SABR',imdb='https://www.imdb.com/name/nm0650684/',note='Founded the Orsatti Agency in 1930 after a career described as bootlegging; reputed fixer for MGM\'s Louis B. Mayer; agent to Judy Garland. Died by 1949 of a heart attack, aged 53 (Weaver et al.). Not the same person as Frank H. Orsatti the stuntman.'),
 dict(name='Ernie F. Orsatti',relation='Son of Ernie Orsatti',relationSource='Family; IMDb and SABR',year=1972,photo='photos/ernie-f.jpg',photoSource='https://www.imdb.com/name/nm0650683/',years='1940–2020',imdb='https://www.imdb.com/name/nm0650683/',note='Born Beverly Hills Feb 13, 1940; died La Quinta Sept 12, 2020. Nicknamed "The Legend." Mother: opera singer Inez Gorman. A Foster Grant model and swimmer trained under Johnny Weissmuller; three Death Wish films, Hot Shots!, Alien: Resurrection, American History X, NYPD Blue, Charmed.',noteSources=['https://www.hollywoodreporter.com/news/general-news/ernie-orsatti-stuntman-who-took-quite-the-fall-in-the-poseidon-adventure-dies-at-80-4063318/']),
 dict(name='Frank H. Orsatti (stuntman)',relation='Son of Ernie Orsatti',relationSource='Family; IMDb and SABR',year=1974,years='1942–2004',imdb='https://www.imdb.com/name/nm0650685/',note='Frank Harry Orsatti, born LA Feb 26, 1942; died Sherman Oaks Dec 23, 2004. Doubled Arnold Schwarzenegger (The Terminator), Burt Reynolds (nine years) and Bill Bixby (The Magician, and David Banner on The Incredible Hulk), and doubled the Hulk himself; directed Hulk episodes; stunt coordinator on Serpico and Highlander II; original member of Stunts Unlimited.',noteSources=['https://variety.com/2005/scene/people-news/frank-orsatti-1117915927/','https://stuntsunlimited.com/frank-orsatti-honorary/']),
 dict(name='Noon Orsatti',relation='Son of Ernie F. Orsatti',year=1986,photo='photos/noon.jpg',photoSource='https://www.imdb.com/name/nm0650687/',imdb='https://www.imdb.com/name/nm0650687/',note='Son of Ernie F.; stunt coordinator / 2nd-unit director. Won the 2024 Taurus World Stunt Award (Extraction 2); in the SAG Awards stunt-ensemble nominees for The Falcon and the Winter Soldier (2022). Chad Stahelski recalls working for Ernie F. and Noon on NYPD Blue, The Pretender and Profiler – and that Noon sent him to the Matrix audition.',noteSources=['https://en.wikipedia.org/wiki/Taurus_World_Stunt_Awards','https://www.actorawards.org/node/12606','https://ew.com/movies/chad-stahelski-keanu-reeves-stunt-double-the-matrix-resurrections-interview/']),
 dict(name='Rowbie Orsatti',relation='Son of Noon Orsatti',relationSource='Family; also IMDb trivia (nm1769066)',year=2012,photo='photos/rowbie.jpg',photoSource='https://www.imdb.com/name/nm1769066/',years='b. 1991',imdb='https://www.imdb.com/name/nm1769066/',note='Son of Noon; stunt performer/coordinator.'),
 dict(name='Ken Orsatti (Alfred Kendall)',year=1961,years='1932–2010',note='Nephew of Ernie: his father and two uncles ran the Orsatti Agency (LA Times). Rorvic Productions assistant 1956; SAG national executive director 1981–2000.'),
]
PH5={'World Series champion':[dict(src='photos/fam-ruth-1934-ws.jpg',caption='Babe Ruth with Cardinals and Tigers players, 1934 World Series – From the Orsatti family collection',source='From the Orsatti family collection')],'Gashouse Gang – 1934 champions':[dict(src='photos/fam-ruth-1934-ws.jpg',caption='Babe Ruth (in suit) with Cardinals and Tigers players, 1934 World Series – From the Orsatti family collection',source='From the Orsatti family collection')],"Babe Ruth's bat":[dict(src='photos/fam-ruth-1934-ws.jpg',caption='Babe Ruth (in suit) with Cardinals and Tigers players, 1934 World Series – From the Orsatti family collection',source='From the Orsatti family collection')],'Quitting school for the movies':[dict(src='photos/fam-mgm-still-9396.jpg',caption='Buster Keaton holding the ball, MGM studio still (MGMP-9396), likely The Cameraman (1928) – From the Orsatti family collection',source='From the Orsatti family collection')],"Best season: .336 – and Rickey's phone trick":[dict(src='photos/fam-ernie-batting.jpg',caption='Ernie Orsatti in a batting pose, Cardinals spring training – From the Orsatti family collection',source='From the Orsatti family collection')],'Fired… into pro baseball':[dict(src='photos/fam-ernie-ballpark-friends.jpg',caption='Ernie Orsatti (in Cardinals uniform) with George Raft and Joe E. Brown – From the Orsatti family collection',source='From the Orsatti family collection')]}
for _m in milestones:
  if _m['title'] in PH5: _m['photos']=PH5[_m['title']]+_m.get('photos',[])
for _m in milestones:
  if _m['title'] in ('Gashouse Gang – 1934 champions','MLB debut – St. Louis Cardinals'): _m['photos']=_m.get('photos',[])+[dict(src='photos/fam-ernie-ballpark-friends.jpg',caption='Ernie Orsatti (in Cardinals uniform) with George Raft and Joe E. Brown – From the Orsatti family collection',source='From the Orsatti family collection')]
for _m in milestones:
  if 'June Lang' in _m.get('text','') or 'June Lang' in _m['title']: _m['photos']=[dict(src='photos/fam-vic-premiere.jpg',caption='Vic Orsatti and June Lang at their wedding, 1937 – From the Orsatti family collection',source='From the Orsatti family collection')]+_m.get('photos',[])
_TEAM=dict(src='photos/fam-cardinals-1934-team.jpg',caption='1934 St. Louis Cardinals — the Gashouse Gang, World Series champions. Ernie Orsatti is named in the team roster. – From the Orsatti family collection',source='From the Orsatti family collection')
for _m in milestones:
  if _m['title'] in ('Gashouse Gang – 1934 champions','World Series champion'): _m['photos']=[_TEAM]+_m.get('photos',[])
PP={'Ernie Orsatti':[_TEAM,dict(src='photos/fam-ernie-batting.jpg',caption='Ernie Orsatti batting pose, Cardinals spring training – From the Orsatti family collection',source='From the Orsatti family collection'),dict(src='photos/fam-ernie-ballpark-friends.jpg',caption='Ernie Orsatti with George Raft and Joe E. Brown – From the Orsatti family collection',source='From the Orsatti family collection'),dict(src='photos/fam-ernie-goudey-1933.jpg',caption='Ernie Orsatti, 1933 Goudey card – From the Orsatti family collection',source='From the Orsatti family collection')],'Ernie F. Orsatti':[dict(src='photos/fam-event-1970s.jpg',caption='Ernie F. Orsatti with Paul and Lynda Orsatti – From the Orsatti family collection',source='From the Orsatti family collection')],'Vic Orsatti':[dict(src='photos/fam-vic-premiere.jpg',caption='Vic Orsatti and June Lang at their wedding, 1937 – From the Orsatti family collection',source='From the Orsatti family collection')]}
for _p in people:
  _k=_p['name'].split(' (')[0]
  if _k in PP: _p['photos']=PP[_k]+_p.get('photos',[])

media={
 'Charlie Puth: Loser':[{'type':'youtube','title':'Charlie Puth – Loser (Official Music Video)','url':'https://www.youtube.com/watch?v=Sp6BS-rSr98','id':'Sp6BS-rSr98'}],
 'The Poseidon Adventure':[{'type':'link','title':'The Poseidon Adventure: Falling Up with Ernie (2006 featurette, Ernie F. recounts the fall)','url':'https://www.imdb.com/name/nm0650683/','note':'Listed on his IMDb; video not located online'},{'type':'youtube','title':'Poseidon Adventure (1972) making-of featurette','url':'https://www.youtube.com/watch?v=JpOU1hGm-xs','id':'JpOU1hGm-xs'},{'type':'article','title':'Hollywood Reporter obituary: the skylight fall','url':'https://www.hollywoodreporter.com/news/general-news/ernie-orsatti-stuntman-who-took-quite-the-fall-in-the-poseidon-adventure-dies-at-80-4063318/'}],
 'Extraction 2':[{'type':'article','title':'Decider: the car chase & Noon\'s rear-seat driving','url':'https://decider.com/2023/06/16/extraction-2-director-interview-21-minute-one-shot-take/'},{'type':'audio','title':'Philosophical Fall Guy podcast, Ep. 1: Noon Orsatti (2025)','url':'https://podbay.fm/p/philosophical-fall-guy/e/1741801177'}],
 'Borderlands':[{'type':'article','title':'Digital Trends interview with Noon Orsatti & Jimmy O\'Dee','url':'https://www.digitaltrends.com/movies/borderlands-interview-stunts-jimmy-odee-noon-orsatti/'}],
 'Sherlock Jr.':[{'type':'link','title':'LAPL photo: Ernie Orsatti Jr. (Ernie F.), Valley College outfielder, 1961','url':'https://calisphere.org/item/1b436e5952a6ff3776783e5fa5e461e0/'},{'type':'photo','src':'photos/ernie-1933-goudey.jpg','title':'Ernie Orsatti, 1933 Goudey card','url':'https://commons.wikimedia.org/wiki/File:Ernest_Orsatti_-_DPLA_-_9bca1ab5bc3cc804eea874cbf130f097.jpg'}],
}
PH4={'World Series champion':[dict(src=C+'1931_World_Series-_Philadelphia_Athletics_vs._St._Louis_Cardinals_(3533485459).jpg?width=900',caption="The 1931 World Series, Athletics vs. Cardinals – Ernie's Cardinals won in seven games (Ernie not identified)",source='https://commons.wikimedia.org/wiki/File:1931_World_Series-_Philadelphia_Athletics_vs._St._Louis_Cardinals_(3533485459).jpg')],'Gashouse Gang – 1934 champions':[dict(src=C+'Dizzy_Dean_Time.jpg?width=900',caption="Dizzy Dean on Time magazine, April 1935 – ace of Ernie's 1934 Gashouse Gang (copyright not renewed)",source='https://commons.wikimedia.org/wiki/File:Dizzy_Dean_Time.jpg'),dict(src=C+'Dizzy_Dean_1934_tiger.jpg?width=900',caption="Dizzy Dean in 1934, the Gashouse Gang's championship season",source='https://commons.wikimedia.org/wiki/File:Dizzy_Dean_1934_tiger.jpg')]}
for _m in milestones:
  if _m['title'] in PH4: _m['photos']=_m.get('photos',[])+PH4[_m['title']]
media.setdefault('The Towering Inferno',[]).append({'type':'link','title':'Towering Inferno behind-the-scenes featurettes, incl. interview with Ernie F. Orsatti (Internet Archive)','url':'https://archive.org/details/towering-inferno-bts'})
media.setdefault('Sherlock Jr.',[]).append({'type':'link','title':'Sherlock Jr. (1924) with commentary by film historian David Kalat (Internet Archive)','url':'https://archive.org/details/sherlock-jr-david-kalat'})

films={}
for c in cr:
  k=(c['title'],None if c.get('type')=='tv' else c['year']); f=films.setdefault(k,dict(title=('Mafia! (Jane Austen\'s Mafia!)' if c['title']=='Mafia!' else c['title']),year=c['year'],type=c.get('type','movie'),tmdb=c.get('tmdb'),imdb=c.get('imdb'),poster=c.get('poster'),boxOffice=c.get('boxOffice'),boxOfficeText=c.get('boxOfficeText'),boxOfficeSource=c.get('boxOfficeSource'),credits=[],funFacts=funfacts.get(c['title'],[]),media=media.get(c['title'],[])))
  f['year']=min(f['year'],c['year']); f['poster']=f['poster'] or c.get('poster'); f['imdb']=f['imdb'] or c.get('imdb')
  import re as _r; m=_r.match(r'(\d+ episodes?)\s*…?\s*(.*)',c['role'] or ''); c['role']=f"{m.group(2) or 'Crew'} · {m.group(1)}" if m else c['role']
  c['role']=(c['role'] or '').replace('(also stunts, uncredited)','· Stunts')
  c['role']=re.sub(r'\s*[(,]?\s*(also stunts, )?uncredited\s*\)?','',c['role'] or '',flags=re.I).replace('( ','(').replace('()','').strip(' ,·') or 'Crew'
  if c['title']=='Hot Shots! Part Deux' and c['person'].startswith('Ernie F.'): c['role']='Stunt Coordinator · Second Unit Director'
  if not any(x['person'].split(' (')[0]==c['person'].split(' (')[0] for x in f['credits']): f['credits'].append(dict(person=c['person'],role=c['role'],source=c['source']))
for f in films.values():
  o=OV.get(f"{f['title']}|{f['year'] if f['type']=='movie' else None}")
  if o and not (f['poster'] and __import__('os').path.exists(f['poster'])): f.update({k:v for k,v in o.items() if k in('poster','tmdb')})
fl=sorted(films.values(),key=lambda f:f['year'])
# multi-year TV: years the family worked on the show where known (IMDb/TMDB/family), else full run (Wikidata/TMDB)
TVSPAN={"It's Always Sunny in Philadelphia":(2006,2008),'Entourage':(2004,2007),'Carnivàle':(2003,2005),'Moonlight':(2007,2008),'The Practice':(1997,2000)}  # only credited work years (IMDb credit spans / credited seasons)
TVADDED=0
SEAS=json.load(open('tv_seasons.json'))
SEAS['Carnivàle']=[dict(season=1,years=[2003]),dict(season=2,years=[2005])]
ONLY={'The Practice':{2,4}}  # Noon credited as stunt double on seasons 2 and 4
def _yl(ys): return str(ys[0]) if len(ys)==1 else f"{ys[0]}–{str(ys[-1])[2:]}"
for f in fl:
  if f['type']=='tv' and f['title'] not in TVSPAN and SEAS.get(f['title']):
    S=[x for x in SEAS[f['title']] if f['year'] in x['years']]
    if S: f['seasonsByYear']={str(f['year']):' & '.join(f"Season {x['season']} · {_yl(x['years'])}" for x in S)}
  if f['type']=='tv' and f['title'] in TVSPAN and SEAS.get(f['title']):
    a,b=TVSPAN[f['title']]
    S=[x for x in SEAS[f['title']] if x['years'] and (f['title'] not in ONLY or x['season'] in ONLY[f['title']]) and any(a<=y<=b for y in x['years'])]
    yrs=sorted({y for x in S for y in x['years'] if a<=y<=b})
    if not yrs: continue
    f['years']=yrs;f['year']=yrs[0];TVADDED+=len(yrs)-1
    f['seasonsByYear']={str(y):' & '.join(f"Season {x['season']} · {_yl(x['years'])}" for x in S if y in x['years']) for y in yrs}
    f['seasonSource']='TMDB season/episode air dates'
print('TV year appearances added:',TVADDED)
known=[f for f in fl if f['boxOffice'] and f['type']=='movie']
data=dict(title='The Orsatti Film Archive',people=people,films=fl,milestones=milestones,boxOfficeSummary=dict(total=sum(f['boxOffice'] for f in known),withData=len(known),films=sum(1 for f in fl if f['type']=='movie'),tvShows=sum(1 for f in fl if f['type']=='tv'),note='Worldwide gross from each film\'s Wikipedia infobox; each film counted once; TV series excluded/null.'))
# --- Daredevil years (1920) + Keaton-years enrichment
data['milestones'].append(dict(year=1920,kind='keaton',title='Daredevil years',
 text='At seventeen, Ernie walked out of school and onto the studio lots of Los Angeles. He began as a gofer, then became a stuntman: walking the wings of airplanes in flight, diving off cliffs, and taking the car and boat gags the pictures of the day ate up. This was Hollywood\'s barnstorming moment, when war-surplus Curtiss Jennys and aerial daredevils like Ormer Locklear were turning wing-walking into screen spectacle. "I wanted to be an actor, a director, a cameraman, anything that would identify me with motion pictures," he said. Within two years the daredevil was on Buster Keaton\'s lot.',
 sources=['https://sabr.org/bioproj/person/ernie-orsatti/ (citing The Sporting News, Feb 4, 1932)'],
 photos=[dict(src=C+'WingWalk1.jpg?width=900',caption='Barnstormer Ormer Locklear wing-walking on a Curtiss JN-4D, c. 1919–20 – the stunt era Ernie entered (Ernie not pictured). Smithsonian NASM, public domain',source='https://commons.wikimedia.org/wiki/File:WingWalk1.jpg')]))
for m in data['milestones']:
  if m['title']=='Quitting school for the movies':
    m['text']=('"My interest, as a boy, was in motion pictures and not in baseball… In 1920, I decided to quit school and devote all my time to the picture business." '
     'In 1922 he joined Buster Keaton\'s studio as prop man and bit player – assistant property master on Sherlock Jr. (1924) and The Cameraman (1928), with stunt work on Our Hospitality (1923) and Sherlock Jr. '
     'At 5-foot-7 and 150 pounds he was nearly Keaton\'s double, and in Sherlock Jr.\'s famous motorcycle run he was exactly that. Keaton told the story in 1958: actor Ford West "couldn\'t fall off the motorcycle so I took my assistant prop man… and put my clothes on him to be on the handlebars," while Keaton himself, dressed as West, took the fall. '
     'Ernie also played first base and caught for Keaton\'s ball team (1922–25), until former big-leaguer Turkey Mike Donlin told Keaton the kid could earn more playing baseball than working in pictures.')
    m['sources']=['https://sabr.org/bioproj/person/ernie-orsatti/','https://www.imdb.com/name/nm1108143/','https://www.damfinoroads.com/buster-keaton (Keaton interview with Christopher Bishop, 1958)']
# --- second-generation stories (research round)
THR='https://www.hollywoodreporter.com/news/general-news/ernie-orsatti-stuntman-who-took-quite-the-fall-in-the-poseidon-adventure-dies-at-80-4063318/'
SU='https://stuntsunlimited.com/frank-orsatti-honorary/'
VAR='https://variety.com/2005/scene/people-news/frank-orsatti-1117915927/'
data['milestones']+= [
 dict(year=1968,kind='milestone',title='From freighters to Planet of the Apes',
  text='Frank H. Orsatti was drafted by his father\'s Cardinals, but an injury in training ended that dream. He shipped out with the Merchant Marines and spent ten years working freighters. Back in Los Angeles he took his first stunt job on Planet of the Apes (1968), then worked Rosemary\'s Baby and Bullitt the same year.',
  sources=[SU,'https://www.imdb.com/name/nm0650685/bio/']),
 dict(year=1971,kind='milestone',title='Off the Golden Gate Bridge',
  text='For B.S. I Love You, Frank H. Orsatti jumped off the Golden Gate Bridge. Stunts Unlimited lists it among the defining gags of a career that went on to The Poseidon Adventure, The Longest Yard, Lethal Weapon 2 and 3, Point Break and Con Air.',
  sources=[SU]),
 dict(year=1972,kind='milestone',title='"We\'ve all come to watch you die."',
  text='Ernie F. Orsatti was cast as an actor in The Poseidon Adventure, playing Terry, the boyfriend of Pamela Sue Martin\'s character. The day before the shoot, Irwin Allen told him he wanted him to do the fall. "I\'m not a stuntman," Ernie said. He did it anyway: hanging from an upside-down table, letting go, and dropping 32 feet onto his back through the ballroom skylight. Paul Stader\'s only advice: "Pick a point, look at it and let go." It knocked him "colder than a cucumber," and they got it in one take. Gene Hackman and Ernest Borgnine came in on their day off with their families. "We\'ve all come to watch you die," Hackman told him, and took pictures. Afterwards, Ernie said, nobody called him an actor again: "you\'re the guy who did the stunt in The Poseidon Adventure, you\'re a stuntman – I wish I\'d found that out years earlier because I\'d be richer."',
  sources=[THR,'https://www.imdb.com/name/nm0650683/bio/']),
 dict(year=1981,kind='milestone',title='Through the window on Hill Street Blues',
  text='Ernie F. Orsatti was thrown through a window in the Hill Street Blues pilot (1981), the start of three decades coordinating stunts – Hoosiers, Grumpy Old Men, Primal Fear, Fear and Loathing in Las Vegas, Pleasantville, Joe Dirt, Cheaper by the Dozen – and TV from L.A. Law and Picket Fences to Nip/Tuck and Big Love.',
  sources=[THR,'https://www.televisionacademy.com/bios/ernie-f-orsatti']),
]
for p in data['people']:
  if p['name'].startswith('Ernie F.'):
    p['note']=p['note'].rstrip('.')+'. Started in the film industry at sixteen; acted in The Green Berets (1968), The Mechanic (1972) and The Towering Inferno (1974, a firefighter in the glass-elevator rescue) before stunts took over.'
    p.setdefault('noteSources',[]).extend([THR,'https://www.televisionacademy.com/bios/ernie-f-orsatti'])
  if p['name'].startswith('Frank H.'):
    p['note']=p['note'].rstrip('.')+'. Ten years in the Merchant Marines before stunts; jumped off the Golden Gate Bridge for B.S. I Love You; second-unit director on Sherlock Holmes Returns, Stark and Strays.'
    p.setdefault('noteSources',[]).extend([SU,VAR])
# --- Inez Gorman
_inez=dict(name='Inez Gorman',films=[{'title': 'No Questions Asked', 'year': 1951, 'role': 'Minor role', 'imdb': 'https://www.imdb.com/title/tt0043861/'}, {'title': 'Strictly Dishonorable', 'year': 1951, 'role': 'Calpurnia, opera sequence', 'imdb': 'https://www.imdb.com/title/tt0044082/'}, {'title': "Singin' in the Rain", 'year': 1952, 'role': 'Mrs. Simpson', 'imdb': 'https://www.imdb.com/title/tt0045152/'}, {'title': 'Love Is Better Than Ever', 'year': 1952, 'role': 'Mrs. Sperson', 'imdb': 'https://www.imdb.com/title/tt0044852/'}, {'title': 'Dream Wife', 'year': 1953, 'role': 'Secretary', 'imdb': 'https://www.imdb.com/title/tt0045706/'}, {'title': 'Give a Girl a Break', 'year': 1953, 'role': 'Miss Leslie', 'imdb': 'https://www.imdb.com/title/tt0045822/'}],imdb='https://www.imdb.com/name/nm0331075/',birthName='Lillian Inez Gorman',relation='Wife of Ernie Orsatti; mother of Ernie F. and Frank H.',year=1934,years='1912–1986',

 note=('Born October 31, 1912 in Massachusetts, she was a soprano trained at Philadelphia\'s Curtis Institute of Music, where on April 13, 1933 she gave the first performance of Ezra Rachlin\'s Goethe song "Gefunden" in Casimir Hall. '
  'She married Ernie Orsatti in Beverly Hills in September 1934, the year he won the World Series, and they had two sons who became the family\'s stunt dynasty: Ernie F. and Frank H. '
  'Twentieth Century-Fox signed her around 1936 for glamour portraits by Gene Kornman; in January 1937 she was elected an active member of the American Guild of Musical Artists alongside Rose Bampton and John McCormack; and Hal Roach tested her for a vocalist part in Laurel and Hardy\'s Swiss Miss (1938). '
  'In 1945 she sang as Nelson Eddy\'s guest soprano on CBS radio\'s The Electric Hour (March 11, April 8 and June 17). At MGM in the early 1950s she sang Calpurnia in the opera sequence of Strictly Dishonorable opposite Ezio Pinza, and played Mrs. Simpson in Singin\' in the Rain. '
  'In 1936 she sang at the Metropolitan Opera in Wagner\'s Die Meistersinger. '
  'She and Ernie divorced in 1952; in 1953 she married Raymond Earl Pierson, her husband until her death in Glendale on December 6, 1986. Her son Ernie F. remembered the Christmas Eve parties at home, his father cooking for dozens of guests "from show business and the opera world."'),
 noteSources=['https://reed.dur.ac.uk/xtf/view?docId=ark%2F32150_s14x51hj07h.xml','https://sabr.org/bioproj/person/ernie-orsatti/','https://docslib.org/doc/10162088/agma-forum-will-he-held-on-tuesday-january-26-1937-in-room-414-551-fifth-avenue-new-york-city-at-2-30-p','https://catalog.afi.com/Film/6045-SWISS-MISS','https://radiogoldin.library.umkc.edu/ProgramMoreinfo/105785','https://www.radioechoes.com/?genre=OTR-Variety&page=series&series=Nelson+Eddy+The+Electric+Hour','https://catalog.afi.com/Person/72676-Inez-Gorman','https://www.imdb.com/name/nm0331075/ (bio and trivia; the Met appearance is from IMDb trivia and not found in the Met archives search)','https://www.allmovie.com/artist/inez-gorman-an1032206','https://www.imdb.com/name/nm0650683/bio/','https://leadinglightsautographs.com/products/inez-gorman-singer-and-starlet-autograph-and-vintage-photo (dealer listing; also says she sang at the Metropolitan Opera – not found in the Met archives)'],
 photo='photos/fam-inez-fox-1936.jpg',photoCaption='Inez Gorman, 20th Century-Fox publicity portrait, c. 1936. From the Orsatti family collection.',photoSource='From the Orsatti family collection')
_i=[k for k,p in enumerate(data['people']) if p['name']=='Ernie Orsatti'][0]
data['people']=[p for p in data['people'] if p['name']!='Inez Gorman'];data['people'].insert(_i+1,_inez)
# --- Ken photo lead (link only)
for p in data['people']:
  if p['name'].startswith('Ken Orsatti'):
    p['photoLinks']=[l for l in p.get('photoLinks',[]) if 'copcomm' not in l['url']]+[dict(caption='Ken Orsatti with SAG President Patty Duke, c. 1987 (SAG-AFTRA magazine, Spring 2021, p. 71)',url='https://digital.copcomm.com/i/1367665-spring-2021/72')]
# --- Hulk role (family)
for f in data['films']:
  if f['title']=='The Incredible Hulk':
    for c in f['credits']:
      if c['person'].startswith('Frank H.'):c['role']='Stunt double: David Banner (Bill Bixby) & the Hulk · Stunt Coordinator · Director';c['source']='https://stuntsunlimited.com/frank-orsatti-honorary/'
# --- Morris: Bank of Italy lore + Dolley
data['milestones']=[m for m in data['milestones'] if m['title']!='Morris and the Bank of Italy']
data['milestones'].append(dict(year=1913,kind='lore',title='Morris and the Bank of Italy',
 text='Family lore holds that Morris Orsatti, owner of the International Steamship and Railroad Ticket Agency, was close to A.P. Giannini, whose Bank of Italy came to Los Angeles in 1913 and later became Bank of America. Morris\'s agency served the same Italian immigrant families Giannini built his bank on, in the years the Bank of Italy opened its Plaza branch in LA\'s Little Italy.',
 sources=['Orsatti family (Noon Orsatti)','https://sabr.org/bioproj/person/ernie-orsatti/','https://pcad.lib.washington.edu/building/14111/','https://artsandculture.google.com/story/eAWBC2Udnlo3KQ','https://www.occ.gov/about/who-we-are/history/history-of-the-occ/1866-1913/1866-1913-bank-of-america.html']))
for m in data['milestones']:
  if m['title']=='Morris Orsatti and the Prohibition agent' and 'framing' not in m['text']:
    m['text']=m['text'].replace('A federal indictment charged Morris Orsatti','A federal indictment charged Morris Orsatti, the Los Angeles steamship and railroad ticket agent,',1)+' The case cut both ways: in 1923 Dolley, by then California\'s Prohibition chief, was himself accused of framing "Italian steamship agent Morris Orsatti", and was cleared.'
    m.pop('flag',None)
    m['sources']=m['sources']+['https://en.wikipedia.org/wiki/George_Hunter_White (citing Bakersfield Morning Echo, Nov 1, 1923, p. 5)']
# --- research round: 1980s-on
TA='https://www.televisionacademy.com/bios/noon-orsatti';DT='https://www.digitaltrends.com/movies/borderlands-interview-stunts-jimmy-odee-noon-orsatti/'
VO='https://variety.com/2020/film/obituaries-people-news/ernie-f-orsatti-dead-dies-stuntman-poseidon-adventure-1234775752/'
data['milestones']=[m for m in data['milestones'] if m['title'] not in('Two Emmy nominations for Hawkeye','"A land of the real"')]
data['milestones']+=[
 dict(year=2022,kind='milestone',title='Two Emmy nominations for Hawkeye',
  text='Noon Orsatti earned two Primetime Emmy nominations for Marvel\'s Hawkeye in 2022: Outstanding Stunt Coordination for a Comedy Series, shared with Heidi Moneymaker, and Outstanding Stunt Performance for the episode "Echoes." His son Rowbie worked the same series as a stunt performer.',
  sources=[TA,'https://www.televisionacademy.com/shows/hawkeye']),
 dict(year=2001,kind='milestone',title='A land of the real',
  text='Several stunt performers who worked for Noon Orsatti went on to direct: Chad Stahelski (John Wick), David Leitch (Deadpool 2) and Sam Hargrave (Extraction). Noon counts J.J. Perry among the stunt veterans who have made the same move behind the camera, and credits the group\'s attention to detail for the transition. His own approach stayed old school: practical action on the ground, with real cars, real people and real jumps.',
  sources=[DT])]
REXN='Rex Orsatti (Rex Pierson)';REXS='https://www.themoviedb.org/person/1720933-rex-pierson'
REX=[('Rocky III',1982,'tt0084602','Challenger'),('Beverly Hills Cop',1984,'tt0086960','Stunts'),('Road House',1989,'tt0098206','Stunts'),('Lock Up',1989,'tt0097770','Stunts'),('Darkman',1990,'tt0099365','Stunts'),('Another 48 Hrs.',1990,'tt0099044','Barroom fighter'),('The Perfect Weapon',1991,None,'Stunts'),('Necessary Roughness',1991,'tt0102510','Stunts'),('U.S. Marshals',1998,'tt0120873','Stunts'),('BASEketball',1998,'tt0131857','Stunts'),('The Incredible Hulk',None,None,'Stand-in')]
for t,y,tt,r in REX:
  f=next((f for f in data['films'] if f['title']==t),None)
  if not f:
    f=dict(title=t,year=y,type='movie',tmdb=None,imdb='https://www.imdb.com/title/%s/'%tt,poster='posters/%s.jpg'%tt,boxOffice=None,boxOfficeText=None,boxOfficeSource=None,credits=[],funFacts=[],media=[]);data['films'].append(f)
  if not any(c['person']==REXN for c in f['credits']):f['credits'].append(dict(person=REXN,role=r,source=REXS))
for f in data['films']:
  if f['title']=='The Expendables':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunt Coordinator (with Chad Stahelski)';c['source']='https://www.svenskfilmdatabas.se/en/item/?itemid=71940&type=film'
  if f['title']=='Highlander II: The Quickening':
    for c in f['credits']:
      if c['person'].startswith('Frank H.'):c['role']='Stunt Coordinator · Sword Master · Stunts';c['source']='https://catalog.afi.com/Person/53874-Frank-Orsatti'
  if f['title']=='Hawkeye':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunt Coordinator · 2 Emmy nominations (2022)';c['source']=TA
_rex=dict(name=REXN,relation='Half-brother of Ernie F. and Frank H. Orsatti',year=1982,years='',imdb=REXS,
 note='Credited on screen as Rex Pierson, Rex worked stunts through the 1980s and 1990s: Beverly Hills Cop, Road House and Lock Up (the last two alongside his brother Frank), Darkman, Necessary Roughness and U.S. Marshals. He fought Rocky as a "Challenger" in Rocky III, brawled in Another 48 Hrs., and stood in on The Incredible Hulk.',
 noteSources=[VO,'https://www.imdb.com/name/nm0650685/bio/',REXS,'https://www.metacritic.com/person/rex-pierson/','https://www.tvguide.com/celebrities/rex-pierson/credits/3000470832/'],photos=[])
data['people']=[p for p in data['people'] if p['name']!=REXN]
_i=[k for k,p in enumerate(data['people']) if p['name'].startswith('Frank H.')][0];data['people'].insert(_i+1,_rex)
for p in data['people']:
  n=p['name']
  if n.startswith('Ernie F.') and '140' not in p['note']:
    p['note']+=' Over his career he logged some 140 stunt credits, and closed out coordinating 18 episodes of It\'s Always Sunny in Philadelphia (2006–08), Big Love and Furry Vengeance (2010).';p['noteSources'].append(VO)
  if n.startswith('Frank H.') and 'sword master' not in p['note']:
    p['note']=p['note'].replace('stunt coordinator on Serpico and Highlander II','stunt coordinator on Serpico, Lock Up and Highlander II (also its sword master)')
  if n.startswith('Noon') and 'Emmy' not in p['note']:
    p['note']+=' Two 2022 Primetime Emmy nominations for Hawkeye (stunt coordination; stunt performance, "Echoes"). Co-coordinated The Expendables (2010) with Stahelski.';p.setdefault('noteSources',[]).extend([TA,'https://www.svenskfilmdatabas.se/en/item/?itemid=71940&type=film'])
  if n.startswith('Rowbie') and 'Thunderbolts' not in p['note']:
    p['note']='Son of Noon; stunt performer and coordinator. Started young on The Bernie Mac Show (2001); stunts on Hawkeye, Extraction II, Thunderbolts* and Stranger Things (2025); doubled Joe Locke on Agatha All Along and John Lee Ames on Ballard (2025); coordinated Charlie Puth\'s "Loser" music video (2022).';p.setdefault('noteSources',[]).append('https://www.imdb.com/name/nm1769066/')
# --- Towering Inferno: McQueen (family)
for f in data['films']:
  if f['title']=='The Towering Inferno':
    f['funFacts']=[dict(text='Ernie F. Orsatti played the hero firefighter hanging on to Steve McQueen outside the scenic glass elevator, high above San Francisco, in the film\'s famous elevator rescue.',source='Orsatti family; https://en.wikipedia.org/wiki/Ernie_Orsatti')]
    for c in f['credits']:
      if c['person'].startswith('Ernie F.'):c['role']='Stunts – firefighter hanging on to Steve McQueen outside the scenic elevator'
for p in data['people']:
  if p['name'].startswith('Ernie F.'):p['note']=p['note'].replace('(1974, a firefighter in the glass-elevator rescue)','(1974, the firefighter hanging on to Steve McQueen outside the scenic glass elevator)')
# --- Sky Riders: actor role
for f in data['films']:
  if f['title']=='Sky Riders':
    for c in f['credits']:
      if c['person'].startswith('Ernie F.'):c['role']='Actor (Joe) · Stunt Coordinator';c['source']='https://catalog.afi.com/Catalog/MovieDetailsPrintView/55219'
# --- Dead Men Don't Wear Plaid (family)
for f in data['films']:
  if f['title']=="Dead Men Don't Wear Plaid":
    for c in f['credits']:
      if c['person'].startswith('Ernie F.'):c['role']='Stunt Coordinator';c['source']='Orsatti family; https://www.imdb.com/name/nm0650683/'
    if not any(c['person'].startswith('Noon') for c in f['credits']):f['credits'].append(dict(person='Noon Orsatti',role='Stunts',source='Orsatti family'))
    f['funFacts']=[dict(text='Father and son on one set: Ernie F. coordinated the stunts on Steve Martin\'s noir spoof, and 19-year-old Noon worked them alongside him.',source='Orsatti family')]
# --- Winds of War: Noon's first project (family)
WW='https://en.wikipedia.org/wiki/The_Winds_of_War_(miniseries)'
data['films']=[f for f in data['films'] if f['title']!='The Winds of War']
data['films'].append(dict(title='The Winds of War',year=1980,years=[1980,1981],type='tv',tmdb='https://www.themoviedb.org/tv/42240-the-winds-of-war',imdb='https://www.imdb.com/title/tt0085111/',poster='posters/tt0085111.jpg',boxOffice=None,boxOfficeText=None,boxOfficeSource=WW,
 credits=[dict(person='Noon Orsatti',role='Stunts · first project',source='Orsatti family; '+WW)],
 funFacts=[dict(text='Noon Orsatti\'s first project. Shot from December 1980 to December 1981 at 404 locations, ABC\'s $40 million miniseries aired over seven nights in February 1983 and was seen by 140 million viewers.',source=WW)],media=[]))
for p in data['people']:
  if p['name']=='Noon Orsatti':
    p['year']=1980
    if 'Winds of War' not in p['note']:p['note']=p['note'].replace('Son of Ernie F.; ','Son of Ernie F. His career began on The Winds of War, the epic ABC miniseries shot 1980–81. Stunt coordinator and 2nd-unit director. ',1).replace('81. Stunt coordinator and 2nd-unit director. stunt coordinator / 2nd-unit director.','81. Stunt coordinator and 2nd-unit director.');p.setdefault('noteSources',[]).append(WW)
# --- Noon early years (family)
for f in data['films']:
  if f['title']=='The Winds of War':
    f['funFacts'][0]['text']=f['funFacts'][0]['text'].replace("Noon Orsatti's first project.","Noon Orsatti's first project, at 18.")
for p in data['people']:
  if p['name']=='Noon Orsatti' and 'Bruce Weber' not in p['note']:
    p['note']=p['note'].replace('the epic ABC miniseries shot 1980–81.','the epic ABC miniseries shot 1980–81, when he was 18. Early on he also booked a run of national commercials – McDonald\'s, Sara Lee, Polaroid and more.',1)
data['milestones']=[m for m in data['milestones'] if m['title']!='In front of Bruce Weber\'s camera']
data['milestones'].append(dict(year=1987,kind='milestone',title='In front of Bruce Weber\'s camera',
 text='Father and son, Ernie F. and Noon Orsatti sat together for a photo shoot with fashion photographer Bruce Weber. Noon also turns up in Weber\'s Oscar-nominated Chet Baker documentary Let\'s Get Lost (1988).',
 sources=['Orsatti family','https://catalog.afi.com/Film/58169-LET\'S-GET-LOST']))
# --- A Guide for the Married Man: Noon at 4 (family)
data['films']=[f for f in data['films'] if f['title']!='A Guide for the Married Man']
data['films'].append(dict(title='A Guide for the Married Man',year=1967,type='movie',tmdb=None,imdb='https://www.imdb.com/title/tt0061736/',poster='posters/tt0061736.jpg',boxOffice=None,boxOfficeText=None,boxOfficeSource='https://en.wikipedia.org/wiki/A_Guide_for_the_Married_Man',
 credits=[dict(person='Noon Orsatti',role='Child performer',source='Orsatti family')],funFacts=[dict(text="Noon's first time on set, age 4.",source='Orsatti family')],media=[]))
for p in data['people']:
  if p['name']=='Noon Orsatti' and 'Married Man' not in p['note']:
    p['note']=p['note'].replace('His career began on','He first stepped onto a set at four, in Gene Kelly\'s A Guide for the Married Man (1967); his career proper began on',1)
# --- Freddy (family)
EL='A Nightmare on Elm Street 4: The Dream Master'
for f in data['films']:
  if f['title']==EL:
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunt double: Freddy Krueger (Robert Englund)';c['source']='Orsatti family (Noon Orsatti); credited as stunt player, https://catalog.afi.com/Catalog/moviedetails/58990'
    f['funFacts']=[dict(text='Noon doubled Freddy Krueger – and Robert Englund trusted him with more than the stunts.',source='Orsatti family')]
data['milestones']=[m for m in data['milestones'] if m['title']!='"The only one that truly understands Freddy"']
data['milestones'].append(dict(year=1988,kind='milestone',title='"The only one that truly understands Freddy"',
 text='On A Nightmare on Elm Street 4: The Dream Master, Noon Orsatti doubled Freddy Krueger. Robert Englund told him, "You\'re the only one that truly understands Freddy" – and left Noon on set to deliver Freddy\'s dialogue and play the scenes on camera himself.',
 sources=['Orsatti family (Noon Orsatti)','https://catalog.afi.com/Catalog/moviedetails/58990 (Noon credited as stunt player; Kevin J. Redzinski is credited as Freddy stunt double/stand-in)']))
# --- Donor (family)
for f in data['films']:
  if f['title']=='Donor' and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Stunts',source='Orsatti family'))
# --- Point Break (family)
for f in data['films']:
  if f['title']=='Point Break':
    if not any(c['person'].startswith('Noon') for c in f['credits']):
      f['credits'].append(dict(person='Noon Orsatti',role='Stunt double: Keanu Reeves (gas station fight)',source='Orsatti family'))
    f['funFacts']=[dict(text='Noon doubled Keanu Reeves in the gas station fight with Patrick Swayze – with his uncle Frank H. also on the stunt crew.',source='Orsatti family')]
# --- Red Shoe Diaries (family)
for f in data['films']:
  if f['title']=='Red Shoe Diaries':
    f['years']=list(range(1992,1998))
    for c in f['credits']:
      if c['person'].startswith(('Noon','Ernie F.')):c['role']='Stunt Coordinator (entire series)';c['source']='Orsatti family'
# --- Sleepwalkers (family)
for f in data['films']:
  if f['title']=='Sleepwalkers':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunt double: Brian Krause';c['source']='Orsatti family; https://www.themoviedb.org/movie/11428-sleepwalkers'
    f['funFacts']=[dict(text="Noon Orsatti was in full prosthetics doubling Brian Krause when he was let off set early to race to the hospital for the birth of his son, Rowbie Orsatti – the family's fourth generation of stunt performers.",source='Orsatti family')]
# --- Benny & Joon, Grumpy Old Men (family)
for f in data['films']:
  if f['title']=='Benny & Joon':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunt Coordinator · Stunt double: Johnny Depp';c['source']='Orsatti family; https://catalog.afi.com/Person/289861-Noon-Orsatti'
    f['funFacts']=[dict(text="Noon Orsatti doubled Johnny Depp – and he's the one on screen in the famous diner juggling scene.",source='Orsatti family')]
  if f['title']=='Grumpy Old Men':
    for c in f['credits']:
      if c['person'].startswith('Ernie F.') and 'Second Unit' not in c['role']:c['role']=c['role']+' · Second Unit Director';c['source']='Orsatti family; '+c.get('source','')
# --- Hot Shots! Part Deux: Cryer (family)
for f in data['films']:
  if f['title']=='Hot Shots! Part Deux':
    for c in f['credits']:
      if c['person'].startswith('Noon') and 'Cryer' not in c['role']:c['role']='Stunts · Stunt double: Jon Cryer';c['source']='Orsatti family; '+c.get('source','')
# --- Surf Ninjas (family)
for f in data['films']:
  if f['title']=='Surf Ninjas':
    for c in f['credits']:
      if c['person'].startswith('Ernie F.'):c['role']='Stunt Coordinator';c['source']='Orsatti family; https://catalog.afi.com/Person/218285-Ernie-Orsatti'
# --- Tall Tale (family)
for f in data['films']:
  if f['title']=='Tall Tale':
    for c in f['credits']:
      if c['person'].startswith('Ernie F.'):c['role']='Stunt Coordinator · Second Unit Director';c['source']='Orsatti family; https://www.imdb.com/name/nm0650683/'
    if not any(c['person'].startswith('Noon') for c in f['credits']):f['credits'].append(dict(person='Noon Orsatti',role='Additional Stunt Coordinator',source='Orsatti family'))
# --- Larger Than Life (family)
for f in data['films']:
  if f['title']=='Larger Than Life' and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Stunt double: Matthew McConaughey',source='Orsatti family'))
# --- Bilko / Trial and Error / Love Bug (family)
for f in data['films']:
  r={'Sgt. Bilko':'Stunts','Trial and Error':'Stunts','The Love Bug':'Stunt driver (Herbie)'}.get(f['title'])
  if r and f['year'] in (1996,1997) and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role=r,source='Orsatti family'))
  if f['title']=='The Love Bug' and f['year']==1997:
    f['funFacts']=[dict(text='Noon Orsatti drove Herbie – with his father Ernie F. coordinating the stunts.',source='Orsatti family')]
# --- City of Industry (family)
for f in data['films']:
  if f['title']=='City of Industry' and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Additional Stunt Coordinator',source='Orsatti family'))
# --- Noon DGA card (family)
data['milestones']=[m for m in data['milestones'] if m['title']!='Noon earns his DGA card']
data['milestones'].append(dict(year=2001,kind='milestone',title='Noon earns his DGA card',
 text='Noon Orsatti earned his Directors Guild of America card as second unit director on Stop at Nothing (2001).',sources=['Orsatti family (Noon Orsatti)']))
for f in data['films']:
  if f['title']=='Stop at Nothing':
    f['funFacts']=[dict(text='Noon Orsatti earned his DGA card here, as second unit director.',source='Orsatti family (Noon Orsatti)')]
# --- Ernie F. & Frank H. DGA cards (family)
data['milestones']=[m for m in data['milestones'] if m['title'] not in ('Ernie F. earns his DGA card','Frank H. earns his DGA card')]
data['milestones'].append(dict(year=1981,kind='milestone',title='Ernie F. earns his DGA card',
 text='Ernie F. Orsatti earned his Directors Guild of America card on Underground Aces (1981).',sources=['Orsatti family']))
for f in data['films']:
  if f['title']=='Underground Aces':
    f['funFacts']=[dict(text='Ernie F. Orsatti earned his DGA card here.',source='Orsatti family')]
# --- Noon doubles Dave Sheridan (family)
for f in data['films']:
  if f['title']=='Frank McKlusky, C.I.' and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Stunt double: Frank McKlusky (Dave Sheridan)',source='Orsatti family'))
# --- Carnivale (Noon) & Cheaper by the Dozen (Rowbie) (family)
for f in data['films']:
  if f['title']=='Carnivàle' and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Additional Stunt Coordinator',source='Orsatti family'))
  if f['title']=='Cheaper by the Dozen' and f['year']==2003:
    if not any(c['person'].startswith('Rowbie') for c in f['credits']):
      f['credits'].append(dict(person='Rowbie Orsatti',role='Stunts',source='Orsatti family'))
    f['funFacts']=[x for x in f.get('funFacts',[]) if 'moon bounce' not in x['text']]+[dict(text='As a kid, Rowbie Orsatti tested many of the gags off camera for the child actors, and he was in the moon bounce scene with Steve Martin.',source='Orsatti family')]
# --- LXG (Ernie F.) (family)
for f in data['films']:
  if f['title']=='The League of Extraordinary Gentlemen' and not any(c['person'].startswith('Ernie F.') for c in f['credits']):
    f['credits'].append(dict(person='Ernie F. Orsatti (1940–2020)',role='Stunt Coordinator · Second Unit Director',source='Orsatti family'))
# --- Just Married (Noon) (family)
for f in data['films']:
  if f['title']=='Just Married' and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Stunts',source='Orsatti family'))
# --- Entourage (Noon) (family + IMDb)
for f in data['films']:
  if f['title']=='Entourage' and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Stunt coordinator / stunt driver (5 eps, 2005–2007)',source='Orsatti family; https://www.imdb.com/title/tt0387199/fullcredits/'))
# --- Charmed: Noon takes over (family)
CH=("Charmed was a family show. Ernie F. Orsatti coordinated its stunts from the start, Rowbie Orsatti got his first screen credit on it in 1998, and in season 3 Noon Orsatti took over from his father and ran the stunts through the 2006 series finale – about 128 episodes. After Charmed ended, Noon turned his focus back to feature films. "
 "Eight seasons of witches, demons and weekly fights made Charmed a training ground: Noon brought in performers who were just starting out, and a generation of stunt people launched their careers on his set.")
data['milestones']=[m for m in data['milestones'] if m['title']!='Noon takes over Charmed']
for m in data['milestones']:
  if m['title'].endswith('first credit: Charmed'):
    m['title']='Charmed: a family show';m['text']=CH;m['sources']=list(m.get('sources',[]))+['Orsatti family (Noon Orsatti)']
for f in data['films']:
  if f['title']=='Charmed':
    f['years']=list(range(1998,2006))
    f['seasonsByYear']={str(1998+i):'Season %d · %d–%s'%(i+1,1998+i,str(1999+i)[2:]) for i in range(8)}
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunt Coordinator (~128 episodes, through the finale)';c['source']='Orsatti family (Noon Orsatti)'
      if c['person'].startswith('Ernie F.'):c['role']='Stunt Coordinator · 37 episodes (seasons 1–2)'
for p in data['people']:
  if p['name']=='Noon Orsatti' and 'Charmed' not in p['note']:
    p['note']+=' Took over Charmed from his father in season 3 and coordinated it through the 2006 finale – about 128 episodes – launching the careers of many young stunt performers.'
# --- Pleasantville (family)
for f in data['films']:
  if f['title']=='Pleasantville':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Additional Stunt Coordinator';c['source']='Orsatti family; '+c['source']
# --- Fallen (family)
for f in data['films']:
  if f['title']=='Fallen' and f['year']==1998 and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].append(dict(person='Noon Orsatti',role='Stunts',source='Orsatti family'))
# --- one photo, one home: each photo appears in only its best-matching section
OWNER={'fam-cardinals-1934-team.jpg':'M:Gashouse Gang','fam-ernie-batting.jpg':'M:Best season','fam-ernie-ballpark-friends.jpg':'P:Ernie Orsatti','ernie-goudey-1933-pd.jpg':'M:MLB debut','fam-ruth-1934-ws.jpg':"M:Babe Ruth's bat",'ernie-action.jpg':'M:World Series champion','Marie_McDonald.jpg':'M:"Husbands'}
def _key(src):return src.split('/')[-1].split('?')[0]
def _ok(src,who):
  o=OWNER.get(_key(src));return o is None or who.startswith(o)
for p in data['people']:
  p['photos']=[x for x in p.get('photos',[]) if _ok(x['src'],'P:'+p['name'])]
for m in data['milestones']:
  if m.get('photos'):m['photos']=[x for x in m['photos'] if _ok(x['src'],'M:'+m['title'])]
# --- 87eleven & Rambo (Noon) (family + IMDb)
data['milestones']=[m for m in data['milestones'] if m['title']!='An original 87eleven member']
data['milestones'].append(dict(year=1997,kind='milestone',title='An original 87eleven member',
 text='Noon Orsatti was one of the original members of 87eleven, the stunt team formed by Chad Stahelski and David Leitch in 1997 that went on to reshape Hollywood action.',sources=['Orsatti family','https://en.wikipedia.org/wiki/87Eleven_Entertainment']))
for f in data['films']:
  if f['title']=='Rambo' and f['year']==2008:
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Second Unit Stunt Coordinator';c['source']='Orsatti family; https://www.imdb.com/name/nm0650687/'
# --- Angels & Demons (Noon) (family)
for f in data['films']:
  if f['title']=='Angels & Demons':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunts · Stunt double: Ewan McGregor (final fire burn)';c['source']='Orsatti family; https://www.themoviedb.org/person/1407364-noon-orsatti?language=en-US'
    f['funFacts']=[x for x in f.get('funFacts',[]) if 'fire burn' not in x['text']]+[dict(text='Noon Orsatti doubled Ewan McGregor for the film\'s final fire burn.',source='Orsatti family')]
# --- The Expendables (Noon) (family + IMDb)
for f in data['films']:
  if f['title']=='The Expendables':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Co-Stunt Coordinator · Second Unit Director';c['source']='Orsatti family; https://www.imdb.com/name/nm0650687/'
# --- Trespass (Rowbie) (family)
for f in data['films']:
  if f['title']=='Trespass' and f['year']==2011 and not any(c['person'].startswith('Rowbie') for c in f['credits']):
    f['credits'].append(dict(person='Rowbie Orsatti',role='Stunts',source='Orsatti family'))
# --- Ride Along (2014) is Noon's, not Ride Along 2 (family)
for f in data['films']:
  if f['title']=='Ride Along 2':f['credits']=[c for c in f['credits'] if not c['person'].startswith('Noon')]
  if f['title']=='Ride Along' and f['year']==2014 and not any(c['person'].startswith('Noon') for c in f['credits']):
    f['credits'].insert(0,dict(person='Noon Orsatti',role='Stunt Coordinator',source='Orsatti family'))
data['films']=[f for f in data['films'] if f['credits']]
# --- Hawkeye (Noon) (family + IMDb)
for f in data['films']:
  if f['title']=='Hawkeye':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Co-Stunt Coordinator · 6 episodes · 2 Emmy nominations (2022)';c['source']='Orsatti family; https://www.imdb.com/name/nm0650687/'
# --- Extraction (2020) (Noon) (family)
if not any(f['title']=='Extraction' and f['year']==2020 for f in data['films']):
  data['films'].append(dict(title='Extraction',year=2020,type='movie',tmdb='https://www.themoviedb.org/movie/545609-extraction',imdb='https://www.imdb.com/title/tt8936646/',poster='posters/tt8936646.jpg',boxOffice=None,boxOfficeText=None,boxOfficeSource=None,
    credits=[dict(person='Noon Orsatti',role='Stunt Coordinator (reshoots)',source='Orsatti family')],funFacts=[],media=[]))
# --- Profiler / The Pretender / The Practice (IMDb, TVmaze, family)
EF='Ernie F. Orsatti (1940–2020)'
def _film(t,y,typ,tm,poster,credits):
  f=next((f for f in data['films'] if f['title']==t and (f['type']==typ)),None)
  if not f:
    f=dict(title=t,year=y,type=typ,tmdb=tm,imdb=None,poster=poster,boxOffice=None,boxOfficeText=None,boxOfficeSource=None,credits=[],funFacts=[],media=[]);data['films'].append(f)
  for c in credits:
    if not any(x['person'].split(' (')[0]==c['person'].split(' (')[0] for x in f['credits']):f['credits'].append(c)
    else:
      for x in f['credits']:
        if x['person'].split(' (')[0]==c['person'].split(' (')[0] and c.get('force'):x.update({k:v for k,v in c.items() if k!='force'})
  return f
_film('Profiler',1996,'tv','https://www.themoviedb.org/tv/2651-profiler','posters/profiler-s1.jpg',[
 dict(person=EF,role='Stunt coordinator (19 eps, 1996–1998)',source='Orsatti family; https://www.imdb.com/title/tt0115322/fullcredits/'),
 dict(person='Noon Orsatti',role='Stunt coordinator (11 eps, 1997–1998)',source='Orsatti family; https://www.imdb.com/title/tt0115322/fullcredits/')])
_film('The Pretender',1997,'tv','https://www.themoviedb.org/tv/1706-the-pretender','posters/the-pretender-s2.jpg',[
 dict(person=EF,role='Stunt coordinator (3 eps, 1997–1999)',source='Orsatti family; https://www.tvmaze.com/people/97987/ernie-f-orsatti'),
 dict(person='Noon Orsatti',role='Stunt coordinator (1 ep, 1998)',source='Orsatti family; https://www.tvmaze.com/people/97988/noon-orsatti')])
_film('The Practice',1997,'tv',None,None,[dict(person=EF,role='Stunt coordinator (1 ep, 2002)',source='Orsatti family; https://www.tvmaze.com/people/97987/ernie-f-orsatti')])
for f in data['films']:
  if f['title']=='The Practice':
    for c in f['credits']:
      if c['person'].startswith('Noon'):c['role']='Stunt double (seasons 2–4, 1997–2000)'
TVP2={'Profiler':{1996:(1,'1996–97','posters/profiler-s1.jpg'),1997:(2,'1997–98','posters/profiler-s2.jpg'),1998:(3,'1998–99','posters/profiler-s3.jpg')},
 'The Pretender':{1997:(2,'1997–98','posters/the-pretender-s2.jpg'),1998:(3,'1998–99','posters/the-pretender-s3.jpg'),1999:(3,'1998–99','posters/the-pretender.jpg')},
 'The Practice':{1997:(2,'1997–98','posters/the-practice-s2.jpg'),1998:(3,'1998–99','posters/the-practice-s3.jpg'),1999:(4,'1999–00','posters/the-practice-s4.jpg'),2000:(4,'1999–00','posters/tt0118437.jpg'),2002:(6,'2001–02','posters/the-practice-s6.jpg')}}
for f in data['films']:
  if f['title'] in TVP2 and f['type']=='tv':
    m=TVP2[f['title']];f['years']=sorted(m);f['year']=min(m)
    f['seasonsByYear']={str(y):'Season %d · %s'%v[:2] for y,v in m.items()}
    f['postersByYear']={str(y):v[2] for y,v in m.items()};f['poster']=m[min(m)][2]
# --- Captain America: Civil War (Noon) (family)
_film('Captain America: Civil War',2016,'movie','https://www.themoviedb.org/movie/271110-captain-america-civil-war','posters/tt3498820.jpg',[dict(person='Noon Orsatti',role='Stunts',source='Orsatti family')])
# --- Noon hiatus card (family)
data['milestones']=[m for m in data['milestones'] if m['title']!='A personal hiatus']
data['milestones'].append(dict(year=2012,kind='business',title='A personal hiatus',text='After finishing work on Ride Along around 2012, Noon Orsatti stepped away from the business for a personal, life-changing adventure. He returned around 2015, when he was asked to work on Captain America: Civil War.',sources=['Orsatti family']))
# --- Rowbie full filmography (IMDb via TV Guide/Metacritic/TMDB; family)
RS='https://www.imdb.com/name/nm1769066/'
RW=lambda r='Stunts':dict(person='Rowbie Orsatti',role=r,source=RS)
for t,y,typ,tm,po in [('The Accountant',2016,'movie','302946-the-accountant','the-accountant'),('Grown Ups 2',2013,'movie','109418-grown-ups-2','grown-ups-2'),('In Time',2011,'movie','49530-in-time','in-time'),('Drive Angry',2011,'movie','47327-drive-angry','drive-angry'),('The Cat in the Hat',2003,'movie','10588-the-cat-in-the-hat','the-cat-in-the-hat'),('Rebel',2021,'tv','111261-rebel','rebel-2021'),('All Night',2018,'tv','75966-all-night','all-night-2018'),('Family Tools',2013,'tv','45042-family-tools','family-tools'),('Standoff',2006,'tv','630-standoff','standoff')]:
  _film(t,y,typ,'https://www.themoviedb.org/%s/%s'%('movie' if typ=='movie' else 'tv',tm),'posters/%s.jpg'%po,[RW()])
_film('Secret Headquarters',2022,'movie','https://www.themoviedb.org/movie/791155-secret-headquarters','posters/secret-headquarters.jpg',[RW('Stunt rigger')])
for t in ('Avengers: Endgame','Stolen','The Closer','Entourage','Carnivàle'):
  f=next((f for f in data['films'] if f['title']==t),None)
  if f and not any(c['person'].startswith('Rowbie') for c in f['credits']):f['credits'].append(RW())
# --- J.J. Perry & Noon photos on 'A land of the real'
for m in data['milestones']:
  if m['title']=='A land of the real':
    m['thumbs']=[dict(src='photos/noon-tmdb.jpg',caption='Noon Orsatti',source='https://www.themoviedb.org/person/1407364-noon-orsatti'),dict(src='photos/jj-perry.jpg',caption='J.J. Perry',source='https://www.themoviedb.org/person/131532-j-j-perry')]
    m['text']='Several stunt performers who worked for Noon Orsatti went on to direct: Chad Stahelski (John Wick), David Leitch (Deadpool 2), Sam Hargrave (Extraction) and J.J. Perry (Day Shift). Noon credits their attention to detail for the transition. His own approach stayed old school: practical action on the ground, with real cars, real people and real jumps.'
    m['sources']=['https://www.digitaltrends.com/movies/borderlands-interview-stunts-jimmy-odee-noon-orsatti/','Orsatti family']
# --- You're Cordially Invited (Rowbie) (family)
for f in data['films']:
  if f['title']=="You're Cordially Invited":
    for c in f['credits']:
      if c['person'].startswith('Rowbie'):c['role']='Stunts · Stunt Coordinator (reshoots)';c['source']='Orsatti family; https://www.imdb.com/name/nm1769066/'
# --- per-season TV posters & Noon season credits (family + IMDb/TMDB)
TVP={'Entourage':{2004:(1,'2004'),2005:(2,'2005'),2006:(3,'2006–07'),2007:(4,'2007')},
 'Scrubs':{2003:(3,'2003–04'),2004:(4,'2004–05'),2006:(5,'2006'),2007:(6,'2006–07'),2008:(7,'2007–08'),2009:(8,'2009')},
 'The Closer':{2005:(1,'2005'),2006:(2,'2006'),2007:(3,'2007'),2008:(4,'2008–09')}}
SLUG={'Entourage':'entourage','Scrubs':'scrubs','The Closer':'the-closer'}
for f in data['films']:
  t=f['title']
  if t in TVP and f['type']=='tv':
    m=TVP[t];f['years']=sorted(m);f['year']=min(m)
    f['seasonsByYear']={str(y):'Season %d · %s'%v for y,v in m.items()}
    f['postersByYear']={str(y):'posters/%s-s%d.jpg'%(SLUG[t],v[0]) for y,v in m.items()}
    f['poster']=f['postersByYear'][str(min(m))]
    if t=='Scrubs':
      for c in f['credits']:
        if c['person'].startswith('Noon'):c['role']='Stunt Coordinator (about 6 seasons, 2003–2009)';c['source']='Orsatti family (about six seasons; years estimated, IMDb confirms 2009 season 8 credit); https://www.imdb.com/title/tt0285403/fullcredits/'
    if t=='The Closer':
      for c in f['credits']:
        if c['person'].startswith('Noon'):c['role']='Stunt Coordinator (seasons 1–4, 2005–2009)';c['source']='Orsatti family (4+ seasons); https://www.themoviedb.org/person/1407364-noon-orsatti (13 episodes)'
for p in data['people']:
  if p['name']=='Noon Orsatti' and 'After Charmed ended' not in p.get('note',''):
    p['note']=p.get('note','').rstrip()+' After Charmed ended in 2006, he turned his focus back to feature films.'
json.dump(data,open('data.json','w'),indent=1,ensure_ascii=False)
print(len(fl),len(known),data['boxOfficeSummary']['total'])
