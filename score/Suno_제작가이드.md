# 그 때는 몰랐습니다 — Suno 제작 가이드

## 1. Style (스타일) 칸에 붙여넣기
Korean ballad, slow rock 6/8, 52 BPM, C major, male vocalist in his 50s, low warm baritone, husky and slightly raspy voice, restrained and sorrowful delivery, nostalgic storytelling, harmonica intro and interlude, acoustic guitar arpeggio, soft piano, brushed drums, string pad, 1980s Korean folk-ballad mood

## 2. Exclude styles (제외) 칸
female vocals, autotune, EDM, rap, trap, fast tempo

## 3. 멜로디를 악보대로 맞추려면
- Suno에서 **Upload Audio(오디오 업로드) → Cover** 로 `그때는몰랐습니다_가이드멜로디.mp3` 를 올리고,
  위 Style과 아래 Lyrics를 넣으면 악보 멜로디를 따라 부르게 됩니다.
- 업로드 없이 만들면 Suno가 멜로디를 새로 지어서 악보와 달라집니다.

## 3-1. 반주(MR) 파일
- `그때는몰랐습니다_MR.mp3` : 반주만 (피아노 아르페지오·베이스·현악·드럼, 전주/간주 하모니카)
- `그때는몰랐습니다_MR_가이드멜로디포함.mp3` : 반주 + 멜로디(플루트) — Suno Cover 업로드나 노래 연습용
- `그때는몰랐습니다_MR.mid` : 반주 MIDI (GarageBand·큐베이스 등에서 악기 바꾸기)
- 다시 만들기: `python3 tools/make_mr.py music.ily <가이드 MIDI> out_mr.mid out_guide.mid`

## 4. Lyrics (가사) 칸에 붙여넣기
```
[Intro - harmonica, 5 bars]

[Verse 1]
그대와 기쁨을 나누고
나란히 웃던 유채꽃 길
홀로 되어 서 보니
그 봄날이 너무 잔인하오
바보 같은 나는 그 때는 몰랐습니다

[Verse 2]
그대 손 가만히 맞잡고
보폭을 맞추던 벚꽃 길은
꽃비 되어 흩어지는데
그대 없는 바람 왜 이리 시린지
그 걸음걸음이 기적인 줄 왜 몰랐을까요

[Chorus]
내 입술이 지은 죄가 너무나도 무거워서
단 한 번의 말실수로 칠 년 우주를 깨뜨렸네
나를 용서 하지 마오 나를 원망 하오 마는
눈부시던 그 눈빛이 낙인 될 줄 은
그 때는 정말 몰랐습니다

[Interlude - harmonica solo]

[Verse 3]
그대 떠나간 빈자리
단풍잎 붉게 멍드는데
낙엽처럼 쌓인 상흔은 내 온 삶을 다 덮었네
시린 겨울 은하 아래 나 홀로 멈췄습니다

[Bridge]
한 몸처럼 아끼었던 내 정인을 내가 아프게 해
미안하다 말하기조차 염치없는 이 못난 밤에
되돌릴 수만 있다면 내 심장을 바쳐서라도
그 모진 시간을 전부 다 지우고 싶으오

[Chorus]
내 입술이 지은 죄가 너무나도 무거워서
단 한 번의 말실수로 칠 년 우주를 깨뜨렸네
나를 용서 하지 마오 나를 원망 하오 마는
눈부시던 그 눈빛이 낙인 될 줄 은
그 때는 정말 몰랐습니다

[Outro]
그 찬란했던 은혜를
내 손으로 깨뜨리고
홀로 남은 이 봄날에
목놓아 불러 보오

[Soft spoken, fade]
미안 합니다... 내 정인 이여...
그 때는 내가... 너무 어리석었습니다.
```
