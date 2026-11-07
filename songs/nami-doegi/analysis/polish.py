import json
M=json.load(open('song_model.json',encoding='utf-8')); b=M['bars']
fix={36:['f','f:sus4'],61:['f','bes/f'],76:['f:sus4','bes/f'],1:['ees:maj7'],2:['bes','g:m7'],3:['ees:maj7'],4:['ees/f'],31:['bes'],52:['bes'],72:['g:m7'],
     77:['bes','ees:maj7'],78:['g:m7'],79:['ees:maj7','f:sus4'],80:['bes']}
for k,v in fix.items(): b[k-1]=v
M['bars']=b; json.dump(M,open('song_model.json','w',encoding='utf-8'),ensure_ascii=False)
PCN={'c':0,'d':2,'e':4,'f':5,'g':7,'a':9,'b':11}
def pc(n): return (PCN[n[0]]+(-1 if n[1:]=='es' else 0))%12
QI={'':[0,4,7],'maj7':[0,4,7,11],'m7':[0,3,7,10],'7':[0,4,7,10],'sus4':[0,5,7]}
TE={'':[2,9],'maj7':[2,9],'m7':[2,5],'7':[2,9],'sus4':[2,10]}
def ct(c,T):
    if c=='ees/f': return {3,7,10,5} if T==QI else {0,2}
    r=c.split('/')[0]; root,_,q=r.partition(':'); return {(pc(root)+i)%12 for i in T[q]}
bad=[]
for s,d,m,syl in M['mel']:
    bb=s//16;p=s%16
    if p%4 or bb>=80: continue
    ch=b[bb]; c=ch[0] if len(ch)==1 or p<8 else ch[1]
    if m%12 not in ct(c,QI): bad.append((bb+1,p//4+1,syl,'tension' if m%12 in ct(c,TE) else 'AVOID',c))
print('beat notes not chord tones:',len(bad)); print([x for x in bad if x[3]=='AVOID'])
