"""song_model.json을 완전5도 아래(B♭ -> E♭)로 옮긴다: python3 transpose.py"""
import json,os
D=os.path.dirname(os.path.abspath(__file__))
M=json.load(open(os.path.join(D,'song_model.json'),encoding='utf-8'))
MAP={'bes':'ees','c':'f','d':'g','ees':'aes','f':'bes','g':'c','a':'d','b':'e'}
def tc(c):
    r,_,b=c.partition('/'); root,_,q=r.partition(':')
    return MAP[root]+(':'+q if q else '')+('/'+MAP[b] if b else '')
M['mel']=[[s,d,m-7,syl] for s,d,m,syl in M['mel']]
M['bars']=[[tc(c) for c in bar] for bar in M['bars']]
json.dump(M,open(os.path.join(D,'song_model_Eb.json'),'w',encoding='utf-8'),ensure_ascii=False)
print(M['bars'][20:31])
