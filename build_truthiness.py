#!/usr/bin/env python3
# Builds truthiness/index.html (Truthiness and Other Facts: the civic lens) from truthiness_picks.json + assets/clip_*.json. Re-run: python3 -I build_truthiness.py
import json,os,re,datetime
R=os.path.dirname(os.path.abspath(__file__))
picks=json.load(open(os.path.join(R,'truthiness_picks.json')))
def heur_lines(p):
    p=re.sub(r'\s*\[(Verse|Chorus|Bridge|Outro|Intro|Pre-Chorus|Hook|Refrain|Interlude|Instrumental)[^\]]*\]\s*',lambda m:'\n\n'+m.group(0).strip()+'\n',p)
    return re.sub(r'(?<=[a-z\.,;:!?\'"”’)])(?=[A-Z"“])',"\n",p).strip()
def polished(k):
    import glob
    fs=sorted(glob.glob(os.path.join(R,'polish',f'*{k}*_POLISHED_v1.md')))
    if not fs: return None
    lines=open(fs[0],encoding='utf-8').read().split('\n')
    # skip the title line and the intro paragraph (up to the first blank line after it)
    i=1
    while i<len(lines) and not lines[i].strip(): i+=1   # blanks after the title
    while i<len(lines) and lines[i].strip(): i+=1       # the intro paragraph
    while i<len(lines) and not lines[i].strip(): i+=1   # blanks before the lyric
    body=[]
    for l in lines[i:]:
        if l.startswith('## '): break
        body.append(l)
    return '\n'.join(body).strip()
tracks=[]
for i,p in enumerate(picks,1):
    c=json.load(open(os.path.join(R,'assets',f"clip_{p['id']}.json"))); md=c['metadata']; k=p['id'][:8]
    lyr=md.get('prompt') or ''
    lyr='\n'.join(l for l in lyr.split('\n') if not re.search(r'Here are your lyrics|minimally edited|^\[Of course|^---\s*$',l))
    lyr=lyr if '\n' in lyr else heur_lines(lyr)
    pol=polished(k); lnote='' if '\n' in (md.get('prompt') or '') else 'Line breaks approximate.'
    if pol: lyr=pol; lnote='Text polished 2026-11-08; the take sings the original.'
    tracks.append({'n':i,'id8':k,'title':p['name'],'sub':p.get('sub',''),'line':p.get('line',''),'dur':round(md.get('duration') or 0),
      'audio':f'../audio/{k}.m4a' if os.path.exists(os.path.join(R,'audio',k+'.m4a')) else '','art':f'../art/{k}.jpeg' if os.path.exists(os.path.join(R,'art',k+'.jpeg')) else '',
      'suno':p.get('share') or 'https://suno.com/song/'+c['id'],'lyrics':lyr,'lnote':lnote,'made':c['created_at'][:10]})
data={'built':datetime.date.today().isoformat(),'tracks':tracks}
t=open(os.path.join(R,'assets','reel_template.html'),encoding='utf-8').read()
t=t.replace('<title>ai.ie · a reel</title>','<title>ai.ie · Truthiness and Other Facts</title>')
t=t.replace('<h1>ai<em>.</em>ie</h1>','<h1>Truthiness <em>and</em> Other Facts</h1>')
t=t.replace('<a href="./" aria-current="page">The First Weeks</a><span>·</span><a href="year/">Proof, not pitch</a><span>·</span><a href="truthiness/">Truthiness</a>','<a href="../">The First Weeks</a><span>·</span><a href="../year/">Proof, not pitch</a><span>·</span><a href="./" aria-current="page">Truthiness</a>')
t=t.replace('<p class="sub">The first weeks · eight songs, October to December 2025, in the order they were made</p>','<p class="sub">The civic lens · the songs about how we govern ourselves, all of them, in one place · by ai.ie</p>')
s=t.index('<div class="about">'); e=t.index('<p class="playall">')
ABOUT='''<div class="about"><p>This is the civic point of view, named here for the record. Songs about power, money, borders, the people who hold the levers and the people under them. Opinions, sung, by one person who has been writing them down for years. The first song is the attitude before the argument.</p><p>The argument, in her own words. On how a person should vote: "figure out what they do know about those things, and then map those things to the ballot, and then tell them how the mapping works and why you mapped them the way that you did, and how they might consider voting if the map holds." On the ballot itself: "I don't think parties should be on the ballot at all." On what to fix first: "If I was to say three things practically, right now, could change and make a big difference, it would be campaign finance, gerrymandering, and Citizens United." Underneath those, a builder's habit: "My preference is always to provide an architecture which makes the fail state impossible." No new law without retiring one, and every rule ships with its purpose and a measure or a sunset.</p><p>Two ideas run under all of it. A felt utopia: not a place anyone would immigrate to, but a state you can feel, and the word is felt. There really is no one utopia, because our feelings are unique to ourselves, so the work is to tell the true story and let people find their own. And a rule for how this band works, people and AI together: we are partners, and no presence is junior.</p><p>This page is also a disclosure. Every track that belongs to this lens goes here, the sharp ones and the clumsy ones, so nothing is hidden and nothing is cherry-picked. Read it with one fact in hand: the library behind it is nearly seven thousand songs deep and growing, and this is one slice of it. The rest is love songs, grief, cats, the sea.</p><p class="sign">One voice, in public, on purpose.</p><p class="bar"><button class="read" id="readAbout">🔊 Read aloud</button> <a class="note" href="../">← The First Weeks</a></p></div>'''
t=t[:s]+ABOUT+'\n '+t[e:]
t=t.replace('<a class="primary-link" href="https://suno.com/album/e67413f3-cb2f-4f59-a6f4-acbc3fd51a14" target="_blank" rel="noopener">♫ Hear it as an album on Suno ↗</a> ','')
t=t.replace('href="art/92ec3e22.jpeg"','href="../art/a08d60a0.jpeg"').replace('https://followkellie.github.io/art/92ec3e22.jpeg','https://followkellie.github.io/art/a08d60a0.jpeg').replace('content="https://followkellie.github.io/"','content="https://followkellie.github.io/truthiness/"')
t=t.replace('content="ai.ie · a reel"','content="ai.ie · Truthiness and Other Facts"').replace('Blade Runner by way of a certain desert. AI is in the band. A kind of map, and goodish company.','The civic lens, all of it, for the record. One slice of a library near seven thousand songs.')
if '<details class="intro">' in t:
    a=t.index('<details class="intro">'); b=t.index('</details>',a)+10; t=t[:a]+t[b:]
t=t.replace("const D=","const D=0;//").replace('/*DATA*/','const D='+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';')
t=t.replace('{{BUILT}}',data['built'])
t=t.replace("data={title:'ai.ie · a reel',text:'Eight songs by ai.ie'","data={title:'ai.ie · Truthiness and Other Facts',text:'The civic lens, sung, by ai.ie'")
os.makedirs(os.path.join(R,'truthiness'),exist_ok=True)
open(os.path.join(R,'truthiness','index.html'),'w',encoding='utf-8').write(t)
print('truthiness/index.html:',len(tracks),'tracks,',sum(1 for x in tracks if x['audio']),'with audio')
