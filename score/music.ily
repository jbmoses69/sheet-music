
\header {
  title = \markup \fontsize #4 \bold "그 때는 몰랐습니다"
  subtitle = \markup \fontsize #1 \italic "Slow Rock"
  composer = "작곡/작사 미상"
  meter = \markup \bold "6/8 박자,  ♩.= 52 (느리고 무겁게)"
}

global = {
  \key c \major
  \time 6/8
  \tempo 4. = 52
}

% 멜로디 파트
melody = \relative c' {
  \global
  
  % 전주 (Intro) - 하모니카 느낌의 잔잔한 선율
  R2.*5 \bar "||" \break
  
  % Verse 1
  \resetRelativeOctave c' e4 e8 e4 g8 | e4 d8 c4. | a4 c8 c4 e8 | g4. r4. | \break
  a4 a8 g4 e8 | d4 c8 d4. | f4 f8 e4 d8 | g2. | \break
  c,4 d8 e4 g8 | a4 g8 e4. | d4 c8 d4. | c2. \bar "||" \break
  
  % Verse 2
  \resetRelativeOctave c' e4 e8 e4 g8 | e4 d8 c4. | a4 c8 c4 e8 | g4. r4. | \break
  a4 a8 g4 e8 | d4 c8 d4. | f4 f8 e4 d8 | g2. | \break
  c,4 d8 e4 g8 | a4 g8 e4. | d4 c8 d4. | c2. \bar "||" \break
  
  % Chorus
  \resetRelativeOctave c'' a4 a8 a4 b8 | c4 b8 a4. | a4 b8 c4 d8 | g,4. r4. | \break
  a4 a8 a4 b8 | c4 b8 a4. | a4 b8 c4 d8 | g,2. | \break
  g4 g8 g4 e8 | e4 d8 c4. | a4 c8 c4 d8 | f4. r4. | \break
  e4 e8 e4 d8 | d4 c8 d4. | d4. e4 d8 | c2. \bar "||" \break
  
  % 간주 (Interlude)
  R2.*6 \bar "||" \break
  
  % Verse 3
  \resetRelativeOctave c' e4 e8 e4 g8 | e4 d8 c4. | a4 c8 c4 e8 | g4. r4. | \break
  a4 a8 g4 e8 | d4 c8 d4. | f4 f8 e4 d8 | g2. | \break
  c,4 d8 e4 g8 | a4 g8 e4. | d4 c8 d4. | c2. \bar "||" \break
  
  % Bridge
  \resetRelativeOctave c'' a4 a8 a4 b8 | c4 b8 a4. | a4 b8 c4 d8 | g,4. r4. | \break
  a4 a8 a4 b8 | c4 b8 a4. | a4 b8 c4 d8 | g,2. | \break
  gis4 gis8 gis4 b8 | a4 g8 e4. | a4 a8 a4 g8 | g4. r4. | \break
  f4 f8 f4 g8 | a4 g8 f4. | d4 d8 e4 f8 | g2. \bar "||" \break
  
  % Chorus (반복)
  \resetRelativeOctave c'' a4 a8 a4 b8 | c4 b8 a4. | a4 b8 c4 d8 | g,4. r4. | \break
  a4 a8 a4 b8 | c4 b8 a4. | a4 b8 c4 d8 | g,2. | \break
  g4 g8 g4 e8 | e4 d8 c4. | a4 c8 c4 d8 | f4. r4. | \break
  e4 e8 e4 d8 | d4 c8 d4. | d4. e4 d8 | c2. \bar "||" \break
  
  % Outro
  \resetRelativeOctave c'' a4 a8 g4 e8 | g4. r4. | f4 f8 e4 c8 | d4. r4. | \break
  a'4 a8 g4 e8 | g4. r4. | f4 f8 g4 a8 | g2. \bar "||" \break
  
  % 나지막하게 (Adagio)
  f4. r4 f8 | f4. r4 f8 | e2. | \break
  d4. e4 d8 | d4. e4 d8 | c2.\fermata \bar "|."
}

% 가사 파트
words = \lyricmode {
  % Verse 1
  그 -- 대 -- 와 기 -- 쁨 -- 을 나 -- 누 -- 고 
  나 --란 -- 히 웃 -- 던 유 -- 채 -- 꽃 길 
  홀 -- 로 되 -- 어 서 보 -- 니 
  그 봄 -- 날 -- 이 너 -- 무 잔 -- 인 -- 하 -- 오 
  바 -- 보 같 -- 은 나 -- 는 그 때 -- 는 몰 -- 랐 -- 습 -- 니 -- 다
  
  % Verse 2
  그 -- 대 손 가 -- 만 -- 히 맞 -- 잡 -- 고 
  보 -- 폭 -- 을 맞 -- 추 -- 던 벚 -- 꽃 길 -- 은 
  꽃 -- 비 되 -- 어 흩 -- 어 -- 지 -- 는데 
  그 -- 대 없 -- 는 바 -- 람 왜 이 -- 리 시 -- 린 -- 지 
  그 걸 -- 음 -- 걸 -- 음 -- 이 기 -- 적 -- 인 줄 왜 몰 -- 랐 -- 을 -- 까 -- 요
  
  % Chorus
  내 입 -- 술 -- 이 지 -- 은 죄 -- 가 너 -- 무 -- 나 -- 도 무 -- 거 -- 워 -- 서 
  단 한 번 -- 의 말 -- 실 -- 수 -- 로 칠 년 우 -- 주 -- 를 깨 -- 뜨 -- 렸 -- 네 
  나 -- 를 용 -- 서 하 -- 지 마 -- 오 나 -- 를 원 -- 망 하 -- 오 마 -- 는 
  눈 -- 부 -- 시 -- 던 그 눈 -- 빛 -- 이 낙 -- 인 될 줄 은 
  그 때 -- 는 정 -- 말 몰 -- 랐 -- 습 -- 니 -- 다
  
  % Verse 3
  그 -- 대 떠 -- 나 -- 간 빈 -- 자 -- 리 
  단 -- 풍 -- 잎 붉 -- 게 멍 -- 드 -- 는 -- 데 
  낙 -- 엽 -- 처 -- 럼 쌓 -- 인 상 -- 흔 -- 은 내 온 삶 -- 을 다 덮 -- 었 -- 네 
  시 -- 린 겨 -- 울 은 -- 하 아 -- 래 나 홀 -- 로 멈 -- 췄 -- 습 -- 니 -- 다
  
  % Bridge
  한 몸 -- 처 -- 럼 아 -- 끼 -- 었 -- 던 내 정 -- 인 -- 을 내가 아 -- 프 -- 게 해 
  미 -- 안 -- 하 -- 다 말 -- 하 -- 기 -- 조 -- 차 염 -- 치 -- 없 -- 는 이 못 -- 난 밤 -- 에 
  되 -- 돌 -- 릴 수 -- 만 있 -- 다 -- 면 내 심 -- 장 -- 을 바 -- 쳐 -- 서 -- 라 -- 도 
  그 모 -- 진 시 -- 간 -- 을 전 -- 부 다 지 -- 우 -- 고 싶 -- 으 -- 오
  
  % Chorus
  내 입 -- 술 -- 이 지 -- 은 죄 -- 가 너 -- 무 -- 나 -- 도 무 -- 거 -- 워 -- 서 
  단 한 번 -- 의 말 -- 실 -- 수 -- 로 칠 년 우 -- 주 -- 를 깨 -- 뜨 -- 렸 -- 네 
  나 -- 를 용 -- 서 하 -- 지 마 -- 오 나 -- 를 원 -- 망 하 -- 오 마 -- 는 
  눈 -- 부 -- 시 -- 던 그 눈 -- 빛 -- 이 낙 -- 인 될 줄 은 
  그 때 -- 는 정 -- 말 몰 -- 랐 -- 습 -- 니 -- 다
  
  % Outro
  그 찬 -- 란 -- 했 -- 던 은 -- 혜 -- 를 
  내 손 -- 으 -- 로 깨 -- 뜨 -- 리 -- 고 
  홀 -- 로 남 -- 은 이 봄 -- 날 -- 에 
  목 -- 놓 -- 아 불 -- 러 보 -- 오 
  
  미 -- 안 합 -- 니 -- 다... 내 정 -- 인 이 -- 여... 
  그 때 -- 는 내 -- 가... 너 -- 무 어 -- 리 -- 석 -- 었 -- 습 -- 니 -- 다.
}

% 코드 파트 (마디마다 정리: 1마디 = 2. , 반 마디는 4. (예: d4.:m7))
harmonies = \chordmode {
  % Intro (5)
  c2. | c | d:m7 | g:7 | c |
  % Verse 1 (12)
  c2. | c | a:m | e:m | a:m7 | d:m7 | f:maj7 | g:7 | c | a:m | d4.:m7 g:7 | c2. |
  % Verse 2 (12)
  c2. | c | a:m | e:m | a:m7 | d:m7 | f:maj7 | g:7 | c | a:m | d4.:m7 g:7 | c2. |
  % Chorus (16)
  a2.:m | f | d:m7 | g | a:m | f | d:m7 | g:7 |
  c | a:m | f | d:m7 | c | d:m7 | g:7 | c |
  % Interlude (6)
  a2.:m | f | d:m7 | g | d:m7 | g:7 |
  % Verse 3 (12)
  c2. | c | a:m | e:m | a:m7 | d:m7 | f:maj7 | g:7 | c | a:m | d4.:m7 g:7 | c2. |
  % Bridge (16)
  a2.:m | f | d:m7 | g | a:m | f | d:m7 | g:7 |
  e:7 | a:m | f | c | d:m7 | f | d:m7 | g:7 |
  % Chorus (16)
  a2.:m | f | d:m7 | g | a:m | f | d:m7 | g:7 |
  c | a:m | f | d:m7 | c | d:m7 | g:7 | c |
  % Outro (8)
  a2.:m7 | c | f:maj7 | g | a:m7 | c | f4. g | g2. |
  % 나지막하게 (6)
  f2. | f:m | c | d:m7 | g:7 | c |
}
