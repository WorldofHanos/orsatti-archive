const $=s=>document.querySelector(s),esc=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const money=n=>'$'+Math.round(n).toLocaleString('en-US');
const link=u=>/^https?:/.test(u)?`<a href="${esc(u)}" target="_blank" rel="noopener">${esc(new URL(u).hostname.replace('www.',''))}</a>`:esc(u);
const KIND={baseball:'Diamond',mob:'Hollywood Underworld',keaton:'The Keaton Years',quote:'In Their Words',business:'Family Business',milestone:'Milestone',lore:'Hollywood Legend'};
fetch('data.json?v='+Date.now()).then(r=>r.json()).then(D=>{window.D=D;
 const years={};D.films.forEach(f=>(f.years||[f.year]).forEach(y=>(years[y]??={films:[],ms:[]}).films.push(f)));D.milestones.forEach(m=>(years[m.year]??={films:[],ms:[]}).ms.push(m));D.people.forEach(p=>p.year&&(years[p.year]??={films:[],ms:[]}).ms.unshift({kind:'person',p}));
 const S=D.boxOfficeSummary;$('#bosub').textContent=`${S.withData} of ${S.films} films with reported grosses · TV excluded`;
 $('#foot').textContent=`${D.films.length} titles · ${D.milestones.length} milestones · total known worldwide gross ${money(S.total)}`;
 const nC=D.films.reduce((n,f)=>n+f.credits.length,0),yrs=new Date().getFullYear()-1923;
 $('#stats').innerHTML=[[yrs,'years in Hollywood'],[nC,'credits archived'],[S.films+S.tvShows,'films & series'],['$'+(S.total/1e9).toFixed(1)+'B','worldwide box office*']].map(([n,l])=>`<div><b>${n}</b><span>${l}</span></div>`).join('')+`<p class="iconic">Sherlock Jr. · The Poseidon Adventure · The Terminator · Avengers: Endgame · Extraction II</p><p class="src">*Known grosses for ${S.withData} of ${S.films} titles, each counted once</p>`;
 const tl=$('#timeline');let cum=0,idx=0;
 Object.keys(years).sort((a,b)=>a-b).forEach(y=>{const g=years[y];g.films.forEach(f=>cum+=f.boxOffice||0);
  const el=document.createElement('section');el.className='yr';el.dataset.cum=cum;
  const short=p=>p.replace(/ \(.*$/,'').replace(' Orsatti','').replace('Victor "Vic"','Vic').replace('"Vic" ','');
  const reel=g.films.map((f,i)=>`<div class="p" data-i="${i}"><div class="pw">${f.poster?`<img src="${esc(f.poster)}" alt="${esc(f.title)} poster" loading="lazy">`:`<div class="np">${esc(f.title)}</div>`}<div class="ov">${f.credits.map(c=>`<b>${esc(short(c.person))}</b><small>${esc(c.role)}</small>`).join('')}</div></div><div>${esc(f.title)}</div></div>`).join('');
const ents=g.films.map((f,i)=>`<div class="ent" data-i="${i}"><span class="t">${esc(f.title)}${f.type==='tv'?' <i>TV</i>':f.type==='music_video'?' <i>Music Video</i>':''}</span> <span class="who">${f.credits.map(c=>esc(short(c.person))+' <span class="role">'+esc(c.role)+'</span>').join(' · ')}</span></div>`).join('');
  const facts=g.ms.map(m=>(window.FS=window.FS||[]).push(m)&&m).map(m=>m.kind==='person'?`<div class="fact person" data-f="${FS.indexOf(m)}" tabindex="0" role="button">${m.p.photo?`<img src="${esc(m.p.photo)}" alt="${esc(m.p.name)}">`:''}<div><div class="k">Enter · Family Member</div><h3>${esc(m.p.name)}</h3>${m.p.birthName?`<div class="src">Born ${esc(m.p.birthName)}</div>`:''}${m.p.relation?`<div class="rel">${esc(m.p.relation)}</div>`:''}<div class="who">${esc(m.p.years||'')}</div><p>${esc(m.p.note)}</p>${m.p.photo?`<div class="src">Photo${m.p.photoCaption?' ('+esc(m.p.photoCaption)+')':''}: ${link(m.p.photoSource)}</div>`:''}${m.p.imdb?`<div class="src">Profile: ${link(m.p.imdb)}</div>`:''}</div><span class="more">Read more ›</span></div>`:`<div class="fact ${m.kind}" data-f="${FS.indexOf(m)}" tabindex="0" role="button"><div class="k">${KIND[m.kind]||''}</div><h3>${esc(m.title)}</h3><p>${esc(m.text)}</p>${m.flag?`<span class="flag" title="${esc(m.flag)}">†</span>`:''}<div class="src">Sources: ${m.sources.map(link).join(' · ')}</div><span class="more">Read more ›</span></div>`);
  const first=(idx++%2)?'r':'l';const L=[],R=[];let hl=0,hr=0;facts.forEach((h,k)=>{const w=h.replace(/<[^>]+>/g,'').length+(h.includes('fact person')?400:150);const toL=k===0?first==='l':(hl<hr||(hl===hr&&first==='r'));if(toL){L.push(h);hl+=w}else{R.push(h);hr+=w}});el.innerHTML=`<div class="side sl">${L.join('')}</div><div class="mid"><div class="yhead"><div class="year">${y}</div></div>${g.films.length?`<div class="reel">${reel}</div>`:''}</div><div class="side sr">${R.join('')}</div>`;
  el.querySelector('.yhead').onclick=()=>el.classList.toggle('pinned');
  el.querySelectorAll('[data-i]').forEach(p=>p.onclick=e=>{e.stopPropagation();open(g.films[p.dataset.i],y)});
  tl.appendChild(el)});
 function open(f,yy){$('#mbody').innerHTML=`<div>${f.poster?`<img class="big" src="${esc(f.poster)}" alt="">`:''}</div><div><h2>${esc(f.title)}</h2><div class="yr2">${f.years?f.years[0]+'–'+f.years[f.years.length-1]:f.year}${f.seasonsByYear&&yy&&f.seasonsByYear[yy]?`<div class="seas">${yy}: ${esc(f.seasonsByYear[yy])}</div>`:''}${f.type==='tv'?' · TV series':f.type==='music_video'?' · Music video':''}</div>
  <h4>The Orsattis on this film</h4><ul>${f.credits.map(c=>{const pp=D.people.find(p=>p.photo&&c.person.startsWith(p.name.split(' (')[0]));return `<li>${pp?`<img class="face" src="${esc(pp.photo)}" alt="">`:''}<b>${esc(c.person)}</b> – ${esc(c.role)} <span class="src">(${link(c.source)})</span></li>`}).join('')}</ul>
  <h4>Worldwide box office</h4><p>${f.type==='music_video'?'<span class="src">Music video – no box office</span>':f.type==='tv'?'<span class="src">Television – no box office</span>':f.boxOffice?money(f.boxOffice)+` <span class="src">(${link(f.boxOfficeSource)})</span>`:'<span class="src">Not reported</span>'}</p>
  ${f.funFacts.length?`<h4>Fun facts</h4><ul>${f.funFacts.map(x=>`<li>${esc(x.text)} <span class="src">(${link(x.source)})</span></li>`).join('')}</ul>`:''}
  ${f.media.length?`<h4>Media</h4><div class="media">${f.media.map(m=>m.type==='youtube'?`<iframe src="https://www.youtube-nocookie.com/embed/${esc(m.id)}" title="${esc(m.title)}" loading="lazy" allowfullscreen></iframe>`:m.type==='photo'?`<a href="${esc(m.url)}" target="_blank"><img src="${esc(m.src)}" alt="${esc(m.title)}"></a>`:`<a class="ml" href="${esc(m.url)}" target="_blank" rel="noopener">${m.type==='audio'?'♪':'→'} ${esc(m.title)}${m.note?` <span class=src>(${esc(m.note)})</span>`:''}</a>`).join('')}</div>`:''}
  ${f.imdb?`<a class="btn" href="${esc(f.imdb)}" target="_blank" rel="noopener">View on IMDb</a>`:''}</div>`;$('#modal').hidden=false}
 $('#modal').onclick=e=>{if(e.target.id==='modal'||e.target.classList.contains('x'))$('#modal').hidden=true};
 document.onkeydown=e=>{if(e.key==='Escape')$('#modal').hidden=true};
 const io=new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting&&e.target.classList.add('in')),{threshold:.1});
 document.querySelectorAll('.yr').forEach(s=>io.observe(s));
 let shown=0,target=0;const tick=()=>{shown+=(target-shown)*.12;if(Math.abs(target-shown)<1)shown=target;$('#bo').textContent=money(shown);requestAnimationFrame(tick)};tick();
 const upd=()=>{let c=0;document.querySelectorAll('.yr').forEach(s=>{if(s.getBoundingClientRect().top<innerHeight*.6)c=+s.dataset.cum});target=c};addEventListener('scroll',upd);upd();
});

;(function(){const mark=i=>{const f=()=>i.classList.add('ld');i.complete&&i.naturalWidth?f():i.addEventListener('load',f,{once:true})};
const run=()=>{document.querySelectorAll('.reel img').forEach(mark);const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.querySelectorAll('.reel img').forEach(i=>{i.loading='eager';i.decoding='async'});io.unobserve(e.target)}}),{rootMargin:'1500px 0px'});document.querySelectorAll('.yr').forEach(y=>io.observe(y))};
const t=setInterval(()=>{if(document.querySelector('.reel img')){clearInterval(t);run()}},200)})();

document.addEventListener('touchstart',e=>{const p=e.target.closest('.reel .p');document.querySelectorAll('.reel .p.tap').forEach(x=>x!==p&&x.classList.remove('tap'));if(p&&!p.classList.contains('tap')){p.classList.add('tap')}},{passive:true});
;(function(){const s=()=>{const c=document.querySelector('.counter'),l=document.querySelector('.corner-logo');if(c&&l){l.style.height=c.offsetHeight+'px';l.style.width=c.offsetWidth+'px';l.style.justifyContent='center'}};addEventListener('resize',s);setInterval(s,1000)})();

;(function(){const c=document.createElement('canvas');c.id='stars';document.body.prepend(c);const x=c.getContext('2d');let S=[];
const rs=()=>{c.width=innerWidth*devicePixelRatio;c.height=innerHeight*devicePixelRatio;S=Array.from({length:Math.round(innerWidth*innerHeight/14000)},()=>({x:Math.random()*c.width,y:Math.random()*c.height,r:(Math.random()*1+.4)*devicePixelRatio,p:Math.random()*6.28,s:.4+Math.random()*1.2}))};rs();addEventListener('resize',rs);
const still=matchMedia('(prefers-reduced-motion: reduce)').matches;
const d=t=>{x.clearRect(0,0,c.width,c.height);for(const s of S){const a=.12+.38*(.5+.5*Math.sin(t/1000*s.s+s.p));x.fillStyle=`rgba(212,180,110,${still?.3:a})`;x.beginPath();x.arc(s.x,s.y,s.r,0,6.28);x.fill()}still||requestAnimationFrame(d)};requestAnimationFrame(d)})();
;(function(){const lb=document.createElement('div');lb.id='lb';lb.innerHTML='<img alt="">';document.body.append(lb);lb.onclick=()=>lb.classList.remove('on');addEventListener('keydown',e=>e.key==='Escape'&&lb.classList.remove('on'));
document.addEventListener('click',e=>{const i=e.target.closest('.card .media img,.card .ph img,.card img.big,.card .gal img');if(!i)return;e.preventDefault();e.stopPropagation();lb.querySelector('img').src=i.src;lb.classList.add('on')},true)})();

;(function(){
const nm=s=>(s||'').split(' (')[0];
function photosFor(m){const P=[];const add=(src,cap,url)=>{if(src&&!P.some(x=>x.src===src))P.push({src,cap,url})};
 if(m.kind==='person'){const p=m.p;add(p.photo,p.photoCaption,p.photoSource);(p.photos||[]).forEach(x=>add(x.src,x.caption,x.source))}
 (m.photos||[]).forEach(x=>add(x.src,x.caption,x.source));
 if(m.kind!=='person'){const t=(m.title+' '+m.text);window.D.people.forEach(p=>{const n=nm(p.name);if(p.photo&&n&&t.includes(n))add(p.photo,p.name+(p.photoCaption?' – '+p.photoCaption:''),p.photoSource)})}
 return P}
function story(m){const p=m.p,P=photosFor(m);const title=p?p.name:m.title,text=p?p.note:m.text;
 const links=p?[...(p.photoLinks||[]).map(l=>`<a class="ml" href="${esc(l.url)}" target="_blank" rel="noopener">${esc(l.caption)} ↗</a>`)]:[];
 const srcs=p?[p.photoSource,...(p.noteSources||[]),...(p.nameSources||[])].filter(Boolean):(m.sources||[]);
 $('#mbody').innerHTML=`<div class="story"><div class="k">${p?'Family Member':(KIND[m.kind]||'')}</div><h2>${esc(title)}</h2>${p&&p.birthName?`<div class="yr2">Born ${esc(p.birthName)}</div>`:''}${p&&p.relation?`<div class="rel">${esc(p.relation)}</div>`:''}${p&&p.years?`<div class="yr2">${esc(p.years)}</div>`:`<div class="yr2">${m.year||''}</div>`}
 ${P.length?`<div class="gal">${P.map(x=>`<figure><img src="${esc(x.src)}" alt="${esc(x.cap||'')}">${x.cap?`<figcaption>${esc(x.cap)}</figcaption>`:''}</figure>`).join('')}</div>`:''}
 <p class="full">${esc(text||'')}</p>${links.length?`<h4>Photos elsewhere</h4><div class="media">${links.join('')}</div>`:''}
 ${p&&p.imdb?`<a class="btn" href="${esc(p.imdb)}" target="_blank" rel="noopener">View on IMDb</a>`:''}
 ${m.flag?`<p class="src">Note: ${esc(m.flag)}</p>`:''}<p class="src qs">Sources: ${srcs.map(link).join(' · ')}</p></div>`;
 $('#modal').hidden=false;$('#modal .x').focus()}
document.addEventListener('click',e=>{if(e.target.closest('a'))return;const c=e.target.closest('.side .fact[data-f]');if(!c)return;try{story(FS[+c.dataset.f])}catch(err){console.error(err)}});
document.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches&&e.target.matches('.side .fact[data-f]')){e.preventDefault();story(FS[+e.target.dataset.f])}});
})();
;(function(){const t=setInterval(()=>{const ys=document.querySelectorAll('.yr');if(!ys.length)return;clearInterval(t);
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){document.querySelectorAll('.yr.now').forEach(x=>x.classList.remove('now'));e.target.classList.add('now')}}),{rootMargin:'-45% 0px -45% 0px'});ys.forEach(y=>io.observe(y))},200)})();
;(function(){const mb=document.getElementById("mbody");let P=[],i=0,v=null;
function show(k){i=(k+P.length)%P.length;const im=v.querySelector(".gv-img"),cap=v.querySelector(".gv-cap");im.classList.add("fade");setTimeout(()=>{im.src=P[i].src;cap.textContent=P[i].cap+"  ("+(i+1)+"/"+P.length+")";im.classList.remove("fade")},180)}
function enhance(){const s=mb.querySelector(".story");if(!s||s.dataset.gx)return;s.dataset.gx=1;const g=s.querySelector(".gal");if(!g)return;
P=[...g.querySelectorAll("figure")].map(f=>({src:f.querySelector("img").src,cap:(f.querySelector("figcaption")||{}).textContent||""}));g.remove();
const b=document.createElement("button");b.className="btn gbtn";b.textContent="Photos ("+P.length+")";s.querySelector("h2").after(b);
const wrap=document.createElement("div");wrap.className="sv";while(s.firstChild)wrap.append(s.firstChild);s.append(wrap);
v=document.createElement("div");v.className="gview";v.innerHTML="<button class=\"btn gback\">‹ Back to story</button><div class=\"gstage\"><button class=\"gnav gp\" aria-label=\"Previous\">‹</button><img class=\"gv-img\" alt=\"\"><button class=\"gnav gn\" aria-label=\"Next\">›</button></div><div class=\"gv-cap\"></div>";s.append(v);
if(P.length<2)v.querySelectorAll(".gnav").forEach(x=>x.style.visibility="hidden");
b.onclick=e=>{e.stopPropagation();s.style.minHeight=s.offsetHeight+"px";s.classList.add("gal-on");show(0)};
v.querySelector(".gback").onclick=e=>{e.stopPropagation();s.classList.remove("gal-on")};
v.querySelector(".gp").onclick=e=>{e.stopPropagation();show(i-1)};v.querySelector(".gn").onclick=e=>{e.stopPropagation();show(i+1)};
v.querySelector(".gv-img").onclick=e=>{e.stopPropagation();const lb=document.getElementById("lb");if(lb){lb.querySelector("img").src=P[i].src;lb.classList.add("on")}}}
new MutationObserver(enhance).observe(mb,{childList:true});
document.addEventListener("keydown",e=>{const s=mb.querySelector(".story.gal-on");if(!s||document.getElementById("modal").hidden)return;if(e.key==="ArrowRight")show(i+1);if(e.key==="ArrowLeft")show(i-1);if(e.key==="Escape"&&!document.getElementById("lb").classList.contains("on")){s.classList.remove("gal-on");e.stopImmediatePropagation()}},true);
})();
