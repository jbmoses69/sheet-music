\version "2.24.0"
\include "music.ily"
\paper {
  top-margin = 12\mm bottom-margin = 12\mm left-margin = 15\mm right-margin = 15\mm
  #(define fonts (set-global-fonts #:roman "NanumGothic" #:sans "NanumGothic"))
}
#(set-global-staff-size 19)
\score {
  <<
    \new ChordNames { \set chordChanges = ##f \harmonies }
    \new Staff \with { instrumentName = "Vocal" } << \clef "treble_8" \new Voice = "lead" { \melody } >>
    \new Lyrics \lyricsto "lead" { \words }
  >>
  \layout { \context { \Score \override RehearsalMark.self-alignment-X = #LEFT } }
  \midi { }
}
