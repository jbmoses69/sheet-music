"""song_model.json(멜로디·코드) -> music.ily (LilyPond)"""
import json,sys,os
D=os.path.dirname(os.path.abspath(__file__))
M=json.load(open(os.path.join(D,'song_model.json'),encoding='utf-8'))
mel=sorted(M['mel']); bars=M['bars']; NB=len(bars)
NAMES={0:'c',1:'des',2:'d',3:'ees',4:'e',5:'f',6:'ges',7:'g',8:'aes',9:'a',10:'bes',11:'b'}
def pitch(m):
    o=m//12-1; s=NAMES[m%12]
    return s+("'"*(o-3) if o>=3 else ","*(3-o))
DUR={16:'1',12:'2.',8:'2',6:'4.',4:'4',3:'8.',2:'8',1:'16'}
def ok(p,v):
    if p+v>16: return False
    if v==16: return p==0
    if v==12: return p in (0,4)
    if v==8: return p in (0,4,8)
    if v==6: return p%2==0 and (p+6<=8 or p>=8 or p==4)
    if v==4: return p%2==0 and (p+4<=8 or p>=8 or p%4==2)
    if v==3: return p%4==0
    if v==2: return p%2==0
    return True
def split(s,d):
    out=[]
    while d>0:
        p=s%16
        for v in (16,12,8,6,4,3,2,1):
            if v<=d and ok(p,v): break
        out.append(v); s+=v; d-=v
    return out
MARKS={1:'Intro',5:'Verse 1',13:'Verse 2',21:'Chorus',32:'Interlude',34:'Verse 3',42:'Chorus',53:'Bridge',62:'Final Chorus',77:'Outro'}
toks=[]; lyr=[]; pos=0
def emit_rest(a,b):
    global toks
    x=a
    while x<b:
        if x%16==0 and b-x>=16:
            toks.append(('R1',x)); x+=16; continue
        for v in split(x,min(b-x,16-x%16)):
            toks.append(('r'+DUR[v],x)); x+=v
for s,d,m,syl in mel:
    if s>pos: emit_rest(pos,s)
    parts=split(s,d); x=s
    for i,v in enumerate(parts):
        toks.append((pitch(m)+DUR[v]+('~' if i<len(parts)-1 else ''),x)); x+=v
    lyr.append(syl); pos=s+d
end=NB*16
if pos<end: emit_rest(pos,end)
# place marks/bar checks
out=[]; last_bar=-1
for t,x in toks:
    b=x//16
    if x%16==0 and b!=last_bar:
        out.append('|' if b else '')
        if b+1 in MARKS: out.append(f'\\mark \\markup \\box "{MARKS[b+1]}"')
        last_bar=b
    out.append(t)
fer=out
# fermata on last note
for i in range(len(fer)-1,-1,-1):
    if fer[i][0] in 'abcdefg': fer[i]=fer[i]+'\\fermata'; break
melody=' '.join(fer).replace(' | ',' |\n  ')
ch=[]
for b in bars:
    d='1' if len(b)==1 else '2'
    for c in b:
        r,_,bass=c.partition('/'); root,_,q=r.partition(':')
        ch.append(root+d+(':'+q if q else '')+('/'+bass if bass else ''))
    ch.append('|')
ily=f'''% 자동 생성: to_lily.py (song_model.json)
\\header {{
  title = \\markup \\fontsize #3 \\bold "남이 되기 참 어렵다"
  subtitle = "Korean Ballad · 4/4 · ♩= 81 · B♭ Major"
  composer = "작사·작곡 jbmoses69 (Suno)"
  arranger = "채보·코드 편곡: AI 분석 후 정리"
  tagline = ##f
}}
global = {{ \\key bes \\major \\time 4/4 \\tempo "Slow Ballad" 4 = 81 }}
melody = {{
  \\global
  {melody}
  \\bar "|."
}}
words = \\lyricmode {{
  {' '.join(lyr)}
}}
harmonies = \\chordmode {{
  {' '.join(ch)}
}}
'''
open(os.path.join(D,'music.ily'),'w',encoding='utf-8').write(ily)
print('notes',len(mel),'syllables',len(lyr),'bars',NB)
