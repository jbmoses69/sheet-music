"""music.ily의 코드와 가이드 멜로디 MIDI로 반주(MR) MIDI를 만든다.
사용: python3 make_mr.py music.ily guide.midi out_mr.mid out_guide.mid"""
import re, sys, mido
ily, guide, out_mr, out_guide = sys.argv[1:5]
PPQ = 384; E = PPQ // 2; BAR = 6 * E
PC = dict(c=0, d=2, e=4, f=5, g=7, a=9, b=11)
QUAL = {'': [0, 4, 7], 'm': [0, 3, 7], '7': [0, 4, 7, 10], 'm7': [0, 3, 7, 10], 'maj7': [0, 4, 7, 11]}

# ---- 코드 읽기: 마디별 [(코드, 8분음표 수)] ----
src = open(ily, encoding='utf-8').read()
h = src[src.index('harmonies = \\chordmode'):]
h = re.sub(r'%[^\n]*', '', h[h.index('{') + 1:h.rindex('}')])
bars = []
for b in h.split('|'):
    toks = b.split()
    if not toks: continue
    items = []
    for t in toks:
        m = re.fullmatch(r'([a-g](?:is|es)?)(\d\.?)?(?::(\w+))?', t)
        root, dur, q = m.groups()
        n = {'2.': 6, '4.': 3}.get(dur, 6 if len(toks) == 1 else 3)
        pc = (PC[root[0]] + (1 if root.endswith('is') else -1 if root.endswith('es') else 0)) % 12
        items.append((pc, QUAL[q or ''], n))
    bars.append(items)
NB = len(bars)
assert NB == 109, NB

# ---- 가이드 멜로디 노트 ----
g = mido.MidiFile(guide); assert g.ticks_per_beat == PPQ
notes, on, t = [], {}, 0
for msg in g.tracks[1]:
    t += msg.time
    if msg.type == 'note_on' and msg.velocity > 0: on[msg.note] = t
    elif msg.type in ('note_off', 'note_on') and msg.note in on:
        notes.append((on.pop(msg.note), t, msg.note))

def bar_notes(src_bar):  # 1-based bar -> notes relative to bar start
    s0 = (src_bar - 1) * BAR
    return [(a - s0, b - s0, n) for a, b, n in notes if s0 <= a < s0 + BAR]

ev = []  # (tick, msg)
def note(ch, tick, dur, n, vel):
    ev.append((tick, mido.Message('note_on', channel=ch, note=n, velocity=vel)))
    ev.append((tick + max(dur - 10, 10), mido.Message('note_off', channel=ch, note=n, velocity=0)))

# 구간(1-based 마디): 전주 1-5, 1절 6-17, 2절 18-29, 후렴 30-45, 간주 46-51,
# 3절 52-63, 브리지 64-79, 후렴 80-95, 아웃트로 96-103, 나지막하게 104-109
def section(b):
    for name, a, z in [('intro', 1, 5), ('verse', 6, 29), ('chorus', 30, 45), ('inter', 46, 51), ('verse', 52, 63),
                       ('chorus', 64, 95), ('outro', 96, 103), ('adagio', 104, 109)]:
        if a <= b <= z: return name

for bi, items in enumerate(bars, 1):
    sec = section(bi); t0 = (bi - 1) * BAR; pos = 0
    soft = sec in ('adagio', 'intro')
    for pc, iv, n in items:
        st = t0 + pos * E
        root3 = 48 + pc                      # C3 근처
        tones = sorted(set((root3 + i) if (root3 + i) < 67 else (root3 + i - 12) for i in iv))
        third, fifth = 48 + (pc + iv[1]) % 12, 48 + (pc + iv[2]) % 12
        if fifth < root3: fifth += 12
        if third < root3: third += 12
        # 피아노 아르페지오 (6/8: 근-5-3'-근'-3'-5)
        pat = [root3, fifth, third + 12, root3 + 12, third + 12, fifth]
        for k in range(n):
            note(0, st + k * E, E * (n - k), pat[(k if n == 6 else k * 2) % 6], 50 if soft else 62)
        # 베이스: 점4분 근음 + 5음
        b = 36 + pc if 36 + pc <= 43 else 24 + pc
        note(1, st, 3 * E, b, 80 if not soft else 60)
        if n == 6: note(1, st + 3 * E, 3 * E, b + 7 if b + 7 <= 47 else b - 5, 72 if not soft else 55)
        # 현악 패드
        for tn in tones: note(2, st, n * E, tn + 12, 34 if sec != 'chorus' else 46)
        pos += n
    # 드럼 (전주 1마디·나지막하게 제외): 하이햇 8분, 킥 1, 스네어(사이드스틱) 4
    if sec not in ('adagio',) and bi > 1:
        for k in range(6): note(9, t0 + k * E, E, 42, 40 if k % 3 else 55)
        note(9, t0, E, 36, 70)
        note(9, t0 + 3 * E, E, 37 if sec in ('verse', 'intro', 'outro') else 38, 60)
        if sec == 'chorus': note(9, t0 + 5 * E, E, 36, 50)
    # 하모니카: 전주(2-5마디 = 후렴 13-16마디), 간주(후렴 1,2,3,4,7,8마디)
    srcmap = {2: 42, 3: 43, 4: 44, 5: 45, 46: 30, 47: 31, 48: 32, 49: 33, 50: 36, 51: 37}
    if bi in srcmap:
        for a, z, n in bar_notes(srcmap[bi]): note(3, t0 + a, z - a, n, 88)

# 마지막 C 화음을 한 마디 더 길게
end = NB * BAR
for n in (36, 48, 55, 64, 67, 72): note(2 if n > 40 else 1, end - BAR, 2 * BAR, n, 45)

def write(path, with_melody):
    mf = mido.MidiFile(ticks_per_beat=PPQ); tr = mido.MidiTrack(); mf.tracks.append(tr)
    tr.append(mido.MetaMessage('set_tempo', tempo=769230, time=0))
    tr.append(mido.MetaMessage('time_signature', numerator=6, denominator=8, time=0))
    for ch, prog in [(0, 0), (1, 32), (2, 48), (3, 22), (4, 73)]:
        tr.append(mido.Message('program_change', channel=ch, program=prog, time=0))
    tr.append(mido.Message('control_change', channel=2, control=7, value=80, time=0))
    tr.append(mido.Message('control_change', channel=0, control=91, value=50, time=0))
    tr.append(mido.Message('control_change', channel=3, control=91, value=60, time=0))
    E2 = list(ev)
    if with_melody:
        for a, z, n in notes:
            E2.append((a, mido.Message('note_on', channel=4, note=n + 12, velocity=95)))
            E2.append((z - 10, mido.Message('note_off', channel=4, note=n + 12, velocity=0)))
    E2.sort(key=lambda x: (x[0], x[1].type == 'note_on'))
    last = 0
    for tk, m in E2:
        tr.append(m.copy(time=tk - last)); last = tk
    mf.save(path)

write(out_mr, False); write(out_guide, True)
print('bars', NB, 'events', len(ev))
