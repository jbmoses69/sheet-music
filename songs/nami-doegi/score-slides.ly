\version "2.24.0"
\include "music.ily"
\paper {
  paper-width = 13.333\in paper-height = 7.5\in indent = 0 print-page-number = ##f
  oddFooterMarkup = ##f evenFooterMarkup = ##f oddHeaderMarkup = ##f evenHeaderMarkup = ##f
  ragged-last-bottom = ##t
  systems-per-page = 4
  top-margin = 0.4\in bottom-margin = 0.3\in left-margin = 0.5\in right-margin = 0.5\in
  #(define fonts (set-global-fonts #:roman "NanumGothic" #:sans "NanumGothic"))
}
#(set-global-staff-size 21)
\score {
  <<
    \new ChordNames { \set chordChanges = ##f \harmonies }
    \new Staff << \clef "treble_8" \new Voice = "lead" { \melody } \new Voice { \repeat unfold 20 { s1*4 \break } } >>
    \new Lyrics \lyricsto "lead" { \words }
  >>
  \layout { \context { \Score \override RehearsalMark.self-alignment-X = #LEFT } }

}
