\version "2.24.0"
\include "music.ily"
% 가이드 멜로디(MIDI 전용): Suno 등에 올려 노래를 입힐 때 쓰는 멜로디만 담은 파일
\score {
  \new Staff \with { midiInstrument = "acoustic grand" } { \melody }
  \midi { }
}
