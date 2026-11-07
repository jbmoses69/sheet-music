import json,numpy as np
raw=json.load(open('notes.json',encoding='utf-8'))
lines=[]
for n in raw:
    if not lines or lines[-1]['text']!=n['line'] or (n['s16']-lines[-1]['notes'][-1]['s16']>24):
        lines.append(dict(text=n['line'],notes=[]))
    lines[-1]['notes'].append(n)
def P(s):  # note names -> midi
    m=[]; 
    for tok in s.split():
        name=tok[:-1]; o=int(tok[-1]); pc={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}[name[0]]
        pc+= {'b':-1,'#':1}.get(name[1:],0); m.append(12*(o+1)+pc)
    return m
def fold(ms):
    out=list(ms)
    for i in range(len(ms)):
        p=ms[i-1] if i>0 else None; q=ms[i+1] if i+1<len(ms) else None
        nb=[x for x in (p,q) if x is not None]
        if nb and all(abs(ms[i]-x)>7 for x in nb):
            med=np.mean(nb)
            while out[i]-med>6: out[i]-=12
            while med-out[i]>6: out[i]+=12
    return out
def data_line(i,anchor,pick=-4,maxlen=None):
    L=lines[i]; ns=L['notes']; syl=[n['syl'] for n in ns]
    ms=fold([n['m'] for n in ns])
    rel=[n['s16']-ns[0]['s16'] for n in ns]
    rel=[int(round(r/2))*2 for r in rel]
    for k in range(1,len(rel)):
        if rel[k]<=rel[k-1]: rel[k]=rel[k-1]+2
    if maxlen and rel[-1]>maxlen-4:
        sc=(maxlen-4)/rel[-1]; rel=[int(round(r*sc)) for r in rel]
        for k in range(1,len(rel)):
            if rel[k]<=rel[k-1]: rel[k]=rel[k-1]+1
    start=anchor*16-16+pick
    end_rel=max(rel[-1]+4,int(round((ns[-1]['e16']-ns[0]['s16'])/2))*2)
    if maxlen: end_rel=min(end_rel,maxlen)
    out=[]
    for k in range(len(ns)):
        e=rel[k+1] if k+1<len(ns) else end_rel
        out.append([start+rel[k],e-rel[k],ms[k],syl[k]])
    return out
def tmpl(anchor,rhythm,pitches,text,last=None):
    syl=list(text.replace(' ','')); ms=P(pitches); assert len(syl)==len(ms)==len(rhythm),(text,len(syl),len(ms),len(rhythm))
    base=anchor*16-16; out=[]
    for k,(s,d) in enumerate(rhythm):
        out.append([base+s,d,ms[k],syl[k]])
    if last: out[-1][1]=last
    return out
# chorus templates (offset relative to anchor bar start, duration) in 16ths
R_H1=[(-8,2),(-6,2),(-4,2),(-2,4),(2,4),(6,2),(8,4),(12,8)]
R_H2=[(-6,2),(-4,2),(-2,2),(0,4),(4,4),(8,2),(10,2),(12,2),(14,8)]
R_H4=[(-12,2),(-10,2),(-8,2),(-6,2),(-4,2),(-2,2),(0,2),(2,2),(4,6)]
R_H5=[(-6,2),(-4,2),(-2,2),(0,6),(6,2),(8,16)]
R_H6=[(-6,2),(-4,2),(-2,2),(0,2),(2,2),(4,2),(6,2),(8,4),(12,2),(14,10)]
H1=('Bb3 Bb3 D4 D4 F4 G4 F4 F4','남이 되기 참 어렵다')
H3=('Bb3 Bb3 D4 D4 Eb4 F4 F4 F4','남이 되기 참 어렵다')
H2=('Bb3 C4 D4 Bb3 C4 C4 D4 Bb3 C4','이름을 불러도 멀어져')
H4=('G4 Bb4 Bb4 A4 G4 F4 F4 F4 C4','아직 내 안에 네가 살아')
H5=('Bb4 Bb4 Bb4 A4 G4 F4','소풍이 되기를')
H6=('Bb3 C4 D4 D4 Bb3 Bb3 C4 C4 Bb3 Bb3','이제는 웃으며 놓아주길')
def chorus(a,final=False):
    o=[]
    o+=tmpl(a,R_H1,*H1); o+=tmpl(a+2,R_H2,*H2); o+=tmpl(a+4,R_H1,*H3)
    o+=tmpl(a+6,R_H4,*H4); o+=tmpl(a+7,R_H5,*H5)
    o+=tmpl(a+9,R_H6,*H6, last=None if not final else 10)
    if final:
        o+=tmpl(a+11,R_H5,*H5); o+=tmpl(a+13,R_H6,*H6,last=18)
    return o
mel=[]
# Verse 1 (anchors 5,7,9,11) lines 0-3 ; Verse 2 (13,15,17,19) lines 4-7 ; Verse 3 (34,36,38,40) lines 14-17
for i,a in zip(range(0,4),(5,7,9,11)): mel+=data_line(i,a,maxlen=28)
for i,a in zip(range(4,8),(13,15,17,19)): mel+=data_line(i,a,maxlen=28)
mel+=chorus(21)
for i,a in zip(range(14,18),(34,36,38,40)): mel+=data_line(i,a,maxlen=28)
mel+=chorus(42)
# Bridge anchors 53,55,57,60
R8=lambda n,st: [(st+2*k,2) for k in range(n)]
br1=R8(9,-4); br1[-1]=(br1[-1][0],10)
mel+=tmpl(53,br1,'G4 G4 G4 G4 F4 G4 F4 F4 D4','조금만 더 천천히 가자')
br2=[(-4,2),(-2,2),(0,2),(2,2),(4,4),(8,4),(12,2),(14,2),(16,8)]
mel+=tmpl(55,br2,'Bb3 C4 C4 D4 D4 A4 D4 C4 Bb3','이별도 숨을 고르도록')
br3=[(-4,2),(-2,2),(0,4),(4,2),(6,2),(8,4),(12,2),(14,2),(16,4),(20,8)]
mel+=tmpl(57,br3,'Bb4 Bb4 G4 F4 G4 Eb4 C4 D4 D4 D4','미워하지 못한 마음까지')
br4=[(-12,2),(-10,2),(-8,2),(-6,2),(-4,4),(0,4),(4,4),(8,4),(12,12)]
mel+=tmpl(60,br4,'Eb4 Eb4 D4 Eb4 Bb3 Bb3 F3 F3 F3','오늘은 그냥 두고 가자')
mel+=chorus(62,final=True)
# Outro anchors 77,79
mel+=tmpl(77,R_H1,*H1)
mel+=tmpl(79,[(-8,2),(-6,2),(-4,2),(-2,4),(2,4),(6,2),(8,4),(12,20)],'Bb3 Bb3 D4 D4 D4 C4 Bb3 Bb3','남이 되기 참 어렵다')
mel.sort()
# overlap check
for a,b in zip(mel,mel[1:]):
    if a[0]+a[1]>b[0]: a[1]=b[0]-a[0]
    assert a[1]>0,(a,b)
NBARS=80
# chords: per bar list of (chord, 16ths)
V=[['bes','ees'],['d:m7'],['g:m7','f'],['bes'],['ees'],['d:m7','g:m7'],['c:m7','f'],['bes']]
V1=[['bes','ees'],['d:m7'],['g:m7','f'],['bes'],['ees'],['d:m7','g:m7'],['c:m7','f'],['g:m7','f']]
CH=[['bes','ees'],['bes','f/a'],['g:m7','ees'],['f:sus4','f'],['bes','f'],['g:m7','ees:maj7'],['bes','f'],['g:m7','ees'],['bes'],['ees','f'],['bes']]
INTRO=[['ees:maj7'],['bes','g:m7'],['ees:maj7'],['g:m7','f']]
BR=[['ees:maj7'],['g:m7'],['d:7'],['g:m7'],['ees:maj7'],['bes/f','f'],['c:m7'],['f:sus4','f'],['f']]
FIN=CH[:10]+[['g:m7'],['bes','ees'],['bes'],['ees','f'],['f:sus4','f']]
OUT=[['bes','ees'],['bes','f'],['ees:maj7','f'],['bes']]
bars=INTRO+V1+V[:7]+[['bes']]+CH+[['bes','ees'],['bes','ees']]+V+CH+BR+FIN+OUT
print('chord bars',len(bars))
assert len(bars)==NBARS,len(bars)
json.dump(dict(mel=mel,bars=bars),open('song_model.json','w',encoding='utf-8'),ensure_ascii=False)
# consonance check on strong beats
PCN={'c':0,'d':2,'e':4,'f':5,'g':7,'a':9,'b':11}
def ctones(c):
    r=c.split('/')[0]; root,_,q=r.partition(':'); pc=(PCN[root[0]]+(-1 if root[1:]=='es' else 0))%12
    iv={'':[0,4,7],'m7':[0,3,7,10],'7':[0,4,7,10],'maj7':[0,4,7,11],'sus4':[0,5,7]}[q]
    return {(pc+i)%12 for i in iv}
bad=[]
for s,d,m,syl in mel:
    b=s//16; p=s%16
    if p%4: continue
    if b>=NBARS: continue
    ch=bars[b]; c=ch[0] if len(ch)==1 or p<8 else ch[1]
    if m%12 not in ctones(c): bad.append((b+1,p//4+1,syl,m%12,c))
print(len(mel),'notes; nonchord on beats:',len(bad)); print(bad)
