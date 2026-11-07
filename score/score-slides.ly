\version "2.24.0"
\include "music.ily"

% 16:9 슬라이드용 페이지 (13.333in x 7.5in), 한 페이지 = 한 슬라이드
\paper {
  paper-width = 13.333\in  paper-height = 7.5\in
  top-margin = 0.45\in  bottom-margin = 0.35\in
  left-margin = 0.6\in  right-margin = 0.6\in
  indent = 0  print-page-number = ##f
  oddFooterMarkup = ##f  evenFooterMarkup = ##f
  oddHeaderMarkup = ##f  evenHeaderMarkup = ##f
  ragged-last-bottom = ##t
  system-system-spacing.basic-distance = #16
  #(define fonts (set-global-fonts #:roman "NanumGothic" #:sans "NanumGothic"))
}
#(set-global-staff-size 22)
\score {
  <<
    \new ChordNames { \set chordChanges = ##f \harmonies }
    \new Staff { \melody }
    \addlyrics { \words }
  >>
  \layout { }
  
}
