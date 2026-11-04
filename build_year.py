#!/usr/bin/env python3
# Builds year/index.html (Proof, Not Pitch: one song a month) from year_picks.json + assets/clip_*.json. Re-run: python3 -I build_year.py
import json,os,re,datetime
R=os.path.dirname(os.path.abspath(__file__))
picks=json.load(open(os.path.join(R,'year_picks.json')))
MON={'01':'January','02':'February','03':'March','04':'April','05':'May','06':'June','07':'July','08':'August','09':'September','10':'October','11':'November','12':'December'}
def heur_lines(p):
    p=re.sub(r'\s*\[(Verse|Chorus|Bridge|Outro|Intro|Pre-Chorus|Hook|Refrain|Interlude|Instrumental)[^\]]*\]\s*',lambda m:'\n\n'+m.group(0).strip()+'\n',p)
    return re.sub(r'(?<=[a-z\.,;:!?\'"”’)])(?=[A-Z"“])',"\n",p).strip()
tracks=[]
for i,p in enumerate(picks,1):
    c=json.load(open(os.path.join(R,'assets',f"clip_{p['id']}.json"))); md=c['metadata']; k=p['id'][:8]
    lyr=md.get('prompt') or ''; lyr=lyr if '\n' in lyr else heur_lines(lyr)
    y,m=p['month'].split('-')
    tracks.append({'n':i,'id8':k,'title':p['name'],'sub':f"{MON[m]} {y}",'line':p.get('line',''),'dur':round(md.get('duration') or 0),
      'audio':f'../audio/{k}.m4a' if os.path.exists(os.path.join(R,'audio',k+'.m4a')) else '','art':f'../art/{k}.jpeg' if os.path.exists(os.path.join(R,'art',k+'.jpeg')) else '',
      'suno':'https://suno.com/song/'+c['id'],'lyrics':lyr,'lnote':'' if '\n' in (md.get('prompt') or '') else 'lines approximate','made':c['created_at'][:10]})
data={'built':datetime.date.today().isoformat(),'tracks':tracks}
t=open(os.path.join(R,'assets','reel_template.html'),encoding='utf-8').read()
# page-specific text
t=t.replace('<title>ai.ie · a reel</title>','<title>ai.ie · Proof, Not Pitch</title>')
t=t.replace('<h1>ai<em>.</em>ie</h1>','<h1>Proof, <em>not</em> pitch</h1>')
t=t.replace('<p class="sub">The first weeks · eight songs, October to December 2025, in the order they were made</p>','<p class="sub">Still on key · one song a month, October 2025 to October 2026, in the order they were made · by ai.ie</p>')
s=t.index('<div class="about">'); e=t.index('<p class="playall">')
ABOUT='''<div class="about"><p>The approach is to find the edge, jump off it, climb back, report how deep the water is, and then decide whether to do it again. That's how I used Suno: stretching its limits, leaning this way and that, genre-bending, searching for the sweet spot.</p><p>There are seven goddesses in a superconscience in here, so it was never going to be one voice. But there is a signature somewhere, and it took time to find. One night, in an extreme adventure, a sound caught me and I thought: damn, here it is. I stayed up far too late reading stems. Those were the nuggets I held dear, thinking I might never get this sound again. But just in case, I can always iterate from this core and call it me.</p><p>That's the post-genre telemetry. Odd juxtapositions that work. Nostalgic echoes with an eerie edge that I call home.</p><p class="sign">One song a month, from the first week to the anniversary. Still on key.</p><p class="bar"><button class="read" id="readAbout">🔊 Read aloud</button> <a class="note" href="../">← The First Weeks</a></p></div>'''
t=t[:s]+ABOUT+'\n '+t[e:]
t=t.replace('<a class="primary-link" href="https://suno.com/album/e67413f3-cb2f-4f59-a6f4-acbc3fd51a14" target="_blank" rel="noopener">♫ Hear it as an album on Suno ↗</a> ','')
t=t.replace('href="art/92ec3e22.jpeg"','href="../art/240b6424.jpeg"').replace('https://followkellie.github.io/art/92ec3e22.jpeg','https://followkellie.github.io/art/240b6424.jpeg').replace('content="https://followkellie.github.io/"','content="https://followkellie.github.io/year/"')
t=t.replace('content="ai.ie · a reel"','content="ai.ie · Proof, Not Pitch"').replace('Blade Runner by way of a certain desert. AI is in the band. A kind of map, and goodish company.','One song a month, October 2025 to October 2026. Still on key.')
# drop the intro details block (first weeks specific)
if '<details class="intro">' in t:
    a=t.index('<details class="intro">'); b=t.index('</details>',a)+10; t=t[:a]+t[b:]
t=t.replace("const D=","const D=0;//").replace('/*DATA*/','const D='+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';')
t=t.replace('{{BUILT}}',data['built'])
t=t.replace("data={title:'ai.ie · a reel',text:'Eight songs by ai.ie'","data={title:'ai.ie · Proof, Not Pitch',text:'One song a month, a year of ai.ie'")
os.makedirs(os.path.join(R,'year'),exist_ok=True)
open(os.path.join(R,'year','index.html'),'w',encoding='utf-8').write(t)
print('year/index.html:',len(tracks),'tracks,',sum(1 for x in tracks if x['audio']),'with audio')
