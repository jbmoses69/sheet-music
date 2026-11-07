\version "2.24.0"
\include "music.ily"

\paper {
  top-margin = 15\mm  bottom-margin = 15\mm
  left-margin = 20\mm right-margin = 20\mm
  #(define fonts (set-global-fonts #:roman "NanumGothic" #:sans "NanumGothic"))
}
\score {
  <<
    \new ChordNames { \set chordChanges = ##f \harmonies }
    \new Staff { \melody }
    \addlyrics { \words }
  >>
  \layout { }
  \midi { }
}
