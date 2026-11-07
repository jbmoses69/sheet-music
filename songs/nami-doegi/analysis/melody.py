import librosa,numpy as np,json
d=np.load('f0.npz'); f0,t,rms=d['f0'],d['t'],d['rms']
sr=16000;hop=160
y,_=librosa.load('sep/htdemucs/song/vocals.wav',sr=sr)
oenv=librosa.onset.onset_strength(y=y,sr=sr,hop_length=hop)
midi=librosa.hz_to_midi(f0)
q=np.load('quarters.npy')
qi=np.arange(len(q))
def pos16(time):  # time -> 16th index from bar1 downbeat (q[1])
    return (np.interp(time,q,qi,left=None,right=None)-1)*4 if time<=q[-1] else (len(q)-2+ (time-q[-1])/np.median(np.diff(q)))*4
lyr=[l for l in open('lyrics.txt',encoding='utf-8').read().split('\n') if l and not l.startswith('[')]
# phrase -> lines mapping (phrase index list per line), by hand from analysis
phr=[(12.46,16.10),(18.30,22.29),(24.22,29.0),(29.0,34.29),(36.80,40.41),(42.00,47.02),(48.86,53.6),(53.6,58.58),
 (60.04,64.53),(66.23,70.54),(72.11,76.63),(77.20,81.4),(81.4,85.93),(87.38,92.18),
 (100.09,103.72),(105.35,109.86),(111.40,117.00),(117.57,121.97),
 (123.46,127.93),(129.64,133.79),(135.53,140.04),(140.58,144.8),(144.8,149.27),(150.76,155.44),
 (156.44,161.60),(162.85,167.03),(168.74,176.24),(176.76,181.76),
 (183.82,188.32),(190.04,194.18),(195.91,200.38),(200.97,204.87),(205.35,209.62),(211.15,215.77),(217.39,221.73),(223.26,228.92),
 (230.29,233.64),(236.33,239.60)]
assert len(phr)==len(lyr),(len(phr),len(lyr))
SCALE={10,0,2,3,5,7,9}
def snap(m):
    r=int(round(m))
    if r%12 in SCALE: return r
    return min([r-1,r+1],key=lambda x:(x%12 not in SCALE,abs(x-m)))
notes=[]
for (s,e),line in zip(phr,lyr):
    syl=[c for c in line.replace(' ','')]
    n=len(syl)
    m=(t>=s)&(t<=e)
    # refine start/end from rms
    idx=np.where(m)[0]
    # candidate onsets: peaks in onset env + pitch jumps
    sm=np.copy(midi); 
    pj=np.zeros_like(oenv); dm=np.abs(np.diff(np.nan_to_num(sm,nan=0)))
    dm=np.where(dm>12,0,dm); pj[1:len(dm)+1]=np.minimum(dm,3)/3
    score=oenv/ (oenv[idx].max()+1e-9)+0.6*pj[:len(oenv)]
    cand=librosa.util.peak_pick(score,pre_max=4,post_max=4,pre_avg=8,post_avg=8,delta=0.05,wait=6)
    cand=[c for c in cand if s+0.09<t[c]<e-0.12]
    cand=sorted(cand,key=lambda c:-score[c])
    chosen=[]
    for c in cand:
        if all(abs(t[c]-t[x])>0.13 for x in chosen): chosen.append(c)
        if len(chosen)==n-1: break
    on=[s]+sorted(t[c] for c in chosen)
    # if not enough, split longest gaps evenly
    while len(on)<n:
        gaps=np.diff(on+[e]); k=int(np.argmax(gaps)); on.insert(k+1,on[k]+gaps[k]/2)
    on.append(e)
    for i in range(n):
        a,b=on[i],on[i+1]
        seg=midi[(t>=a)&(t<a+max((b-a)*0.7,0.06))]
        seg=seg[~np.isnan(seg)]
        p=np.median(seg) if len(seg) else np.nan
        notes.append(dict(t0=a,t1=b,p=p,syl=syl[i],line=line))
# fill nan pitches with neighbor
for i,nt in enumerate(notes):
    if np.isnan(nt['p']):
        nb=[x['p'] for x in notes[max(0,i-2):i+3] if not np.isnan(x['p'])]; nt['p']=np.median(nb)
# octave sanity: keep within 50..72
for nt in notes:
    while nt['p']<50: nt['p']+=12
    while nt['p']>72: nt['p']-=12
    nt['m']=snap(nt['p']); nt['s16']=int(round(pos16(nt['t0']))); nt['e16']=int(round(pos16(nt['t1'])))
json.dump(notes,open('notes.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
cur=None
for nt in notes:
    if nt['line']!=cur: cur=nt['line']; print('\n'+cur, end=': ')
    print(f"{nt['syl']}{librosa.midi_to_note(nt['m'],unicode=False)}@{nt['s16']//16+1}.{nt['s16']%16}", end=' ')
