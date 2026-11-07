import librosa,numpy as np,json
sr=22050
y,_=librosa.load('sep/htdemucs/song/no_vocals.wav',sr=sr)
q=np.load('quarters.npy'); hop=512
yh=librosa.effects.harmonic(y)
C=librosa.feature.chroma_cqt(y=yh,sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C3'),n_octaves=4)
B=librosa.feature.chroma_cqt(y=yh,sr=sr,hop_length=hop,fmin=librosa.note_to_hz('C1'),n_octaves=2)
N='C Db D Eb E F Gb G Ab A Bb B'.split()
Q={'':[0,4,7],'m':[0,3,7],'7':[0,4,7,10],'m7':[0,3,7,10],'maj7':[0,4,7,11],'sus4':[0,5,7],'add9':[0,4,7,2]}
cands=[('Bb',''),('Bb','maj7'),('Bb','add9'),('C','m'),('C','m7'),('C','7'),('D','m'),('D','m7'),('D','7'),('Eb',''),('Eb','maj7'),('Eb','m'),
       ('F',''),('F','7'),('F','sus4'),('G','m'),('G','m7'),('G','7'),('Ab',''),('A','7')]
prior={('Bb',''):.03,('Eb',''):.03,('F',''):.03,('G','m'):.02,('C','m'):.02,('D','m'):.01}
def tmpl(r,qq):
    t=np.zeros(12); iv=Q[qq]; w=[1,.9,.8,.6]
    for i,v in enumerate(iv): t[(N.index(r)+v)%12]=w[i]
    return t/np.linalg.norm(t)
T=[(r,qq,tmpl(r,qq)) for r,qq in cands]
bar0=1; nb=(len(q)-1-bar0)//4
fr=librosa.time_to_frames(q,sr=sr,hop_length=hop)
out=[]
for k in range(nb):
    halves=[]
    for h in (0,2):
        a=fr[bar0+4*k+h]; z=fr[bar0+4*k+h+2] if bar0+4*k+h+2<len(fr) else C.shape[1]
        c=C[:,a:z].mean(1); c=c/(np.linalg.norm(c)+1e-9); bs=B[:,a:z].mean(1)
        sc=sorted([(float(c@t)+prior.get((r,qq),0),r,qq) for r,qq,t in T],reverse=True)
        energy=float(np.sqrt((y[int(q[bar0+4*k+h]*sr):int(q[min(bar0+4*k+h+2,len(q)-1)]*sr)]**2).mean()))
        halves.append(dict(best=sc[0][1]+sc[0][2],score=round(sc[0][0],3),alt=sc[1][1]+sc[1][2],bass=N[int(bs.argmax())],e=round(energy,4)))
    out.append(dict(bar=k+1,t=round(float(q[bar0+4*k]),2),h=halves))
json.dump(out,open('chords.json','w'),indent=0)
for o in out:
    h=o['h']; print(o['bar'],o['t'],' | '.join(f"{x['best']}/{x['bass']}({x['score']},{x['alt']})" for x in h), h[0]['e'])
