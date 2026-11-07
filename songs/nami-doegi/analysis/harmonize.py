import json,numpy as np,librosa
M=json.load(open('song_model.json',encoding='utf-8')); mel=M['mel']; NB=80
sr=22050;hop=512
y,_=librosa.load('sep/htdemucs/song/no_vocals.wav',sr=sr)
C=librosa.feature.chroma_cqt(y=librosa.effects.harmonic(y),sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C2'),n_octaves=5)
q=np.load('quarters.npy'); fr=librosa.time_to_frames(q,sr=sr,hop_length=hop)
PCN={'c':0,'d':2,'e':4,'f':5,'g':7,'a':9,'b':11}
def pc(n): return (PCN[n[0]]+(-1 if n[1:]=='es' else 1 if n[1:]=='is' else 0))%12
QI={'':[0,4,7],'maj7':[0,4,7,11],'m7':[0,3,7,10],'7':[0,4,7,10],'sus4':[0,5,7],'m':[0,3,7]}
TENS={'':[2,9],'maj7':[2,9],'m7':[2,5],'7':[2,9],'sus4':[2,10],'m':[2,5]}
CANDS=['bes','bes:maj7','bes/d','c:m7','d:m7','ees','ees:maj7','f','f:sus4','f/a','g:m7','d:7','c:7','g:7','ees/f']
def parse(c):
    r,_,b=c.partition('/'); root,_,qq=r.partition(':')
    if c=='ees/f': return pc('ees'),'',pc('f')
    return pc(root),qq,(pc(b) if b else pc(root))
def tones(c):
    r,qq,b=parse(c); return {(r+i)%12 for i in QI[qq]}
def tens(c):
    r,qq,b=parse(c); return {(r+i)%12 for i in TENS[qq]}
def tmpl(c):
    r,qq,b=parse(c); t=np.zeros(12)
    for k,i in enumerate(QI[qq]): t[(r+i)%12]+=[1,.9,.8,.6][k]
    t[b]+=0.5; return t/np.linalg.norm(t)
T={c:tmpl(c) for c in CANDS}
H=NB*2
chroma_sim=np.zeros((H,len(CANDS)))
for h in range(H):
    qa=1+2*h; qb=min(qa+2,len(fr)-1)
    if qa>=len(fr)-1: chroma_sim[h]=0.5; continue
    v=C[:,fr[qa]:fr[qb]].mean(1); v=v/(np.linalg.norm(v)+1e-9)
    chroma_sim[h]=[v@T[c] for c in CANDS]
mfit=np.zeros((H,len(CANDS)))
for s,d,m,syl in mel:
    for x in range(s,s+d):
        h=x//8
        if h<0 or h>=H: continue
        w=(2.0 if x%4==0 else 0.6 if x%2==0 else 0.3)*(1.5 if x==s else 1.0)
        for j,c in enumerate(CANDS):
            p=m%12
            mfit[h,j]+=w*(1 if p in tones(c) else 0.15 if p in tens(c) else -1.2)
# normalize mfit per half
mf=np.where(np.abs(mfit).max(1,keepdims=True)>0,mfit/ (np.abs(mfit).max(1,keepdims=True)+1e-9),0)
FUN={'bes':'I','bes:maj7':'I','bes/d':'I','c:m7':'ii','d:m7':'iii','ees':'IV','ees:maj7':'IV','f':'V','f:sus4':'V','f/a':'V','g:m7':'vi','d:7':'V/vi','c:7':'V/V','g:7':'V/ii','ees/f':'V'}
GOOD={('V','I'),('ii','V'),('IV','V'),('vi','IV'),('vi','ii'),('I','IV'),('I','vi'),('iii','vi'),('V/vi','vi'),('V/V','V'),('V/ii','ii'),('IV','I'),('I','V'),('V','vi'),('iii','IV'),('I','ii'),('IV','ii'),('ii','IV')}
def trans(a,b,h):
    if a==b: return 0.35 if h%2==1 else 0.05   # sustain across half->half within bar favoured
    fa,fb=FUN[CANDS[a]],FUN[CANDS[b]]
    sc=0.25 if (fa,fb) in GOOD else -0.05
    if fa==fb: sc=0.1
    if h%2==1: sc-=0.18  # changing mid-bar costs a bit
    if CANDS[b] in ('c:7','g:7','d:7') and FUN[CANDS[b]]!='V/vi': sc-=0.05
    return sc
prior=np.array([0.05 if c in ('bes','ees','f','g:m7','c:m7','d:m7') else 0 for c in CANDS])
E=0.55*chroma_sim+0.45*mf+prior
def viterbi(hs):
    n=len(CANDS); dp=E[hs[0]].copy(); bp=[]
    for k in range(1,len(hs)):
        h=hs[k]; best=np.zeros(n); arg=np.zeros(n,int)
        for b in range(n):
            vals=[dp[a]+trans(a,b,h) for a in range(n)]
            arg[b]=int(np.argmax(vals)); best[b]=max(vals)+E[h,b]
        dp=best; bp.append(arg)
    path=[int(np.argmax(dp))]
    for arg in reversed(bp): path.append(int(arg[path[-1]]))
    return [CANDS[i] for i in reversed(path)]
res=viterbi(list(range(H)))
# unify repeated choruses: average emissions over chorus repetitions (anchors 21,42,62) for 11 bars
def segH(a,n): return [h for h in range((a-1)*2,(a-1+n)*2)]
reps=[segH(21,11),segH(42,11),segH(62,11)]
Eavg=np.mean([E[r] for r in reps],axis=0)
for r in reps: E[r]=Eavg
res=viterbi(list(range(H)))
# force final bar tonic
res[-1]=res[-2]='bes'
bars=[]
for b in range(NB):
    a,c=res[2*b],res[2*b+1]
    bars.append([a] if a==c else [a,c])
# print with melody fit check
bad=0
for b in range(NB):
    print(b+1,' '.join(bars[b]))
M['bars']=bars; json.dump(M,open('song_model.json','w',encoding='utf-8'),ensure_ascii=False)
