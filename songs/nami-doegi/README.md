# 남이 되기 참 어렵다 — 악보·코드·반주

Suno 음원(작사·작곡 jbmoses69)을 분석해 만든 리드시트와 반주입니다.

| 항목 | 값 |
|---|---|
| 박자 / 템포 | 4/4, ♩= 81 (Slow Ballad) |
| 조성 | B♭ Major |
| 구성 | 전주 4 · 1절 8 · 2절 8 · 후렴 11 · 간주 2 · 3절 8 · 후렴 11 · 브리지 9 · 마지막 후렴 15 · 아웃트로 4 = 80마디 |

## 파일
- `남이되기참어렵다_악보.pdf` / `.pptx` — 리드시트(멜로디·가사·코드), PPT는 편집 가능
- `남이되기참어렵다_MR.mp3` — 반주만, `..._MR_멜로디포함.mp3` — 반주+멜로디(클라리넷)
- `남이되기참어렵다_MR.mid`, `..._멜로디.midi` — MIDI
- `song_model.json` — 멜로디(16분음표 단위)·코드 원본 데이터

## 남성 저음 키 (E♭ Major, 원곡보다 완전5도 아래)
50대 남성이 편하게 부르도록 낮춘 버전. 음역 G2–G4, 중심음 G3 (원곡 D3–D5).
- `남이되기참어렵다_악보_Eb.pdf` / `.pptx`, `..._MR_Eb.mp3`, `..._MR_멜로디포함_Eb.mp3`, `..._MR_Eb.mid`, `..._멜로디_Eb.midi`
- 만들기: `python3 transpose.py && python3 to_lily.py song_model_Eb.json music_Eb.ily ees "E♭ Major" && lilypond score-a4-Eb.ly && python3 make_mr.py mr.mid g.mid song_model_Eb.json Eb`

## 다시 만들기
```
python3 to_lily.py                     # song_model.json -> music.ily
lilypond score-a4.ly                   # A4 PDF + MIDI
lilypond -dbackend=svg score-slides.ly # 16:9 슬라이드용 SVG
python3 make_mr.py mr.mid mr_guide.mid # 반주 MIDI
```
`analysis/` 는 음원 분석(보컬 분리 → 박·코드·멜로디 추출 → 코드 최적화)에 쓴 스크립트입니다.

## 한계
멜로디는 보컬 분리 + 음높이 추적으로 자동 채보한 뒤 정리한 것입니다. 후렴은 세 번을 같은 멜로디로 통일했습니다.
절(verse) 부분은 원곡과 리듬·음이 다른 곳이 있을 수 있으니 귀로 확인해 `song_model.json`을 고치세요.
