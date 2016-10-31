title: My Tips on LyX

## Why LyX

I used to write a lot of my research papers (almost all) using `LaTeX + VIM`
but finally find that it is very inefficient for me, a non-native English speaker.
Now, I come up with an idea to mitigate the pain of writing research articles in English.
That is, prepare the draft with LyX at early days and convert it into LaTeX when deadlines are coming soon.


This page maintains notes on LyX.

## System Name

I used to define a macro to refer to the name of the system under describing.

In LaTeX:

~~~{.tex}
\newcommand{\sysname}{\textsf{AOTES}\xspace}
~~~

In LyX:

`Document->Preference->Local Module`

~~~
Format 60
InsetLayout "Flex:Sysname"
  LabelString         "AOTES"
  LabelFont
    Color   blue
    Family  Sans Serif
  EndFont
  LatexType             Command
  LaTexName             sysname
  LyxType               "custom"
  Decoration            Classic
  Preamble
    \newcommand{\sysname}{\textsf{AOTES}\xspace}
  EndPreamble
ResetsFont true
End
~~~
