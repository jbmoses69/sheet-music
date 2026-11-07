"""song_model.json -> 4/4 발라드 반주 MIDI (MR, MR+멜로디)
사용: python3 make_mr.py out_mr.mid out_guide.mid"""
import json,sys,os,mido
D=os.path.dirname(os.path.abspath(__file__))
M=json.load(open(os.path.join(D,'song_model.json'),encoding='utf-8'))
mel,bars=M['mel'],M['bars']; NB=len(bars)
PPQ=480; S16=PPQ//4; BAR=16*S16; TEMPO=mido.bpm2tempo(81)
PCN={'c':0,'d':2,'e':4,'f':5,'g':7,'a':9,'b':11}
def pc(n): return (PCN[n[0]]+(-1 if n[1:]=='es' else 1 if n[1:]=='is' else 0))%12
QI={'':[0,4,7],'maj7':[0,4,7,11],'m7':[0,3,7,10],'7':[0,4,7,10],'sus4':[0,5,7],'m':[0,3,7]}
def chord(c):
    r,_,b=c.partition('/'); root,_,q=r.partition(':')
    rp=pc(root); return rp,[(rp+i)%12 for i in QI[q]],(pc(b) if b else rp)
# 구간별 강약 (마디 1-based)
def sec(b):
    for name,a,z in [('intro',1,4),('v1',5,12),('v2',13,20),('ch',21,31),('inter',32,33),('v3',34,41),('ch',42,52),
                     ('br',53,60),('pre',61,61),('fin_soft',62,65),('fin',66,75),('stop',76,76),('outro',77,80)]:
        if a<=b<=z: return name
LV={'intro':(.55,0,0,.5),'v1':(.6,0,0,.55),'v2':(.7,.75,.45,.6),'ch':(.8,.9,.8,.8),'inter':(.6,.6,.3,.6),'v3':(.7,.8,.5,.65),
    'br':(.75,.85,.65,.75),'pre':(.6,.7,.0,.7),'fin_soft':(.6,.0,.0,.65),'fin':(.85,.95,.9,.85),'stop':(.5,0,0,.6),'outro':(.6,.6,.0,.6)}
ev=[]
def note(ch,t,d,n,v):
    v=max(1,min(127,int(v)))
    ev.append((t,1,mido.Message('note_on',channel=ch,note=n,velocity=v)))
    ev.append((t+max(d-20,20),0,mido.Message('note_off',channel=ch,note=n,velocity=0)))
def near(p,lo):  # pitch class p at or above lo
    n=lo+((p-lo)%12); return n
for bi,b in enumerate(bars,1):
    s=sec(bi); pv,bv,dv,sv=LV[s]; t0=(bi-1)*BAR
    halves=[(b[0],0,16)] if len(b)==1 else [(b[0],0,8),(b[1],8,8)]
    for c,off,ln in halves:
        rp,tones,bass=chord(c); st=t0+off*S16
        # 피아노: 8분 아르페지오 (근음-5-8-3/9-8-5 ...)
        root=near(rp,43); fifth=near(tones[2],root+1); third=near(tones[1],root+12)
        top=near(tones[-1],third+1) if len(tones)>3 else root+12
        pat=[root,fifth,root+12,third,top,third,root+12,fifth]
        for k in range(ln//2):
            note(0,st+k*2*S16,2*S16*(2 if k==ln//2-1 else 1),pat[k%8],(62 if k%4==0 else 50)*pv/0.7)
        # 현악 패드 (화음 전체 길게)
        for i,tn in enumerate(sorted(near(x,55) for x in tones)):
            note(2,st,ln*S16,tn,40*sv/0.7)
        # 베이스: 1박 근음(혹은 지정 베이스), 3박/반마디 5음 또는 근음
        if bv:
            bn=near(bass,28)
            note(1,st,(6 if ln==16 else 6)*S16,bn,82*bv)
            note(1,st+6*S16,2*S16,bn,60*bv)
            if ln==16:
                f5=near(tones[2],28)
                note(1,st+8*S16,6*S16,bn if s in('v2','v3') else f5,74*bv)
                note(1,st+14*S16,2*S16,bn,58*bv)
    # 드럼
    if dv:
        for k in range(8): note(9,t0+k*2*S16,S16,42,(52 if k%2==0 else 36)*dv)
        note(9,t0,S16,36,90*dv); note(9,t0+10*S16,S16,36,70*dv)
        sn=37 if s in ('v2','v3') else 38
        note(9,t0+4*S16,S16,sn,80*dv); note(9,t0+12*S16,S16,sn,84*dv)
        if bi in (21,42,53,66,77): note(9,t0,4*S16,49,90)
    if bi in (31,52,75) : note(9,t0+12*S16,S16,38,60); note(9,t0+14*S16,S16,38,70)
# 마지막 화음 페르마타: 1마디 더
end=NB*BAR
for n in (34,46,53,58,62,65,70): note(2 if n>40 else 1,end-BAR//2,BAR+BAR//2,n,55)
def write(path,with_mel):
    mf=mido.MidiFile(ticks_per_beat=PPQ); tr=mido.MidiTrack(); mf.tracks.append(tr)
    tr.append(mido.MetaMessage('set_tempo',tempo=TEMPO,time=0))
    tr.append(mido.MetaMessage('time_signature',numerator=4,denominator=4,time=0))
    tr.append(mido.MetaMessage('key_signature',key='Bb',time=0))
    for ch,prog in ((0,0),(1,33),(2,49),(4,71)): tr.append(mido.Message('program_change',channel=ch,program=prog,time=0))
    for ch,cc,v in ((0,91,55),(2,91,70),(2,7,85),(4,91,60),(1,7,100)): tr.append(mido.Message('control_change',channel=ch,control=cc,value=v,time=0))
    E=list(ev)
    if with_mel:
        for s,d,m,syl in mel:
            t=s*S16; E.append((t,1,mido.Message('note_on',channel=4,note=m+12,velocity=96)))
            E.append((t+d*S16-20,0,mido.Message('note_off',channel=4,note=m+12,velocity=0)))
    E.sort(key=lambda x:(x[0],x[1])); last=0
    for t,_,m in E: tr.append(m.copy(time=t-last)); last=t
    mf.save(path)
write(sys.argv[1],False); write(sys.argv[2],True)
print('bars',NB,'events',len(ev))
