#!/usr/bin/env python3
# Builds reel/index.html from assets/clip_*.json + audio/<id8>.m4a + art/<id8>.jpeg. Re-run: python3 -I build_reel.py
import json,glob,os,re,datetime,html
R=os.path.dirname(os.path.abspath(__file__))
ORDER=['240b6424','cf3657a5','3f94dcb2','efded082','92ec3e22','d6d22402','56a0726d','018b56a8']  # The First Weeks, in order made (2026-11-03)
clips={}
for f in glob.glob(os.path.join(R,'assets','clip_*.json')):
    c=json.load(open(f)); clips[c['id'][:8]]=c
def heur_lines(p):
    p=re.sub(r'\s*\[(Verse|Chorus|Bridge|Outro|Intro|Pre-Chorus|Hook|Refrain|Interlude|Instrumental)[^\]]*\]\s*',lambda m:'\n\n'+m.group(0).strip()+'\n',p)
    p=re.sub(r'(?<=[a-z\.,;:!?\'"”’)])(?=[A-Z"“])',"\n",p); return p.strip()
DISP=json.load(open(os.path.join(R,'assets','display.json')))
tracks=[]
for i,k in enumerate(ORDER,1):
    c=clips[k]; md=c['metadata']; p=md.get('prompt') or ''
    lyr=p if '\n' in p else heur_lines(p)
    d=DISP.get(k,{}); tracks.append({'n':i,'id8':k,'title':d.get('name') or c['title'].strip(),'sub':d.get('sub',''),'line':d.get('line',''),'suno_title':c['title'].strip(),'dur':round(md.get('duration') or 0),
      'audio':'audio/%s.m4a'%k if os.path.exists(os.path.join(R,'audio',k+'.m4a')) else '', 'art':'art/%s.jpeg'%k if os.path.exists(os.path.join(R,'art',k+'.jpeg')) else '',
      'suno':'https://suno.com/song/'+c['id'],'lyrics':lyr,'lnote':'' if '\n' in p else 'lines approximate','made':c['created_at'][:10],'model':c.get('major_model_version','')})
data={'built':datetime.date.today().isoformat(),'tracks':tracks}
tpl=open(os.path.join(R,'assets','reel_template.html'),encoding='utf-8').read()
out=tpl.replace('/*DATA*/','const D='+json.dumps(data,ensure_ascii=False).replace('</','<\\/')+';').replace('{{BUILT}}',data['built'])
open(os.path.join(R,'index.html'),'w',encoding='utf-8').write(out)
print('reel/index.html written:',len(tracks),'tracks;',sum(1 for t in tracks if t['audio']),'with audio;',sum(1 for t in tracks if t['art']),'with art')
