% na podstawie nieopisanego pliku pracamgr.cls
% używanego w Uniwersytecie Warszawskim, utworzonego prawdopodobnie
% na Wydziale Wydziale Matematyki, Informatyki i Mechaniki ok. roku 2001.
% Zmiany 2017.03.01 P. Durka durka@fuw.edu.pl:
%  zmiana nazwy klasy i dostosowanie dla WF UW, ZFBiM
%  specjalnosci Fizyka Medyczna i Neuroinformatyka
%  według Załącznika Nr 1 do Zarządzenia nr 16 Rektora UW z dnia 18 maja 2006 r.
%  https://www.fuw.edu.pl/tl_files/studia/dyplom_polski.doc



\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{pracalicmgr}


\def\@baseclass{report}
\def\@rodzajpracy{Master's}
\DeclareOption{magisterska}{\def\@rodzajpracy{magisterska}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{\@baseclass}}
\PassOptionsToClass{a4paper,twoside,openright,11pt}{\@baseclass}
\ProcessOptions

\LoadClass{\@baseclass}

\textwidth\paperwidth
\advance\textwidth -55mm
\oddsidemargin-1in
\advance\oddsidemargin 30mm
\evensidemargin-1in
\advance\evensidemargin 25mm
\topmargin -1in
\advance\topmargin 2cm
\setlength\textheight{48\baselineskip}
\addtolength\textheight{\topskip}
\marginparwidth15mm

\renewcommand\maketitle{%
  \begin{titlepage}%
    \let\footnotesize\small
    \let\footnoterule\relax
    \let \footnote \thanks
    \begin{center}%
      {\LARGE\textbf{University of Warsaw\\
        Faculty of Physics}\par}
      \vspace{1cm plus 1fill} 
      {\Large\@author\par}
      \vspace{0.2cm}
      {\large Record book number: \@nralbumu\par}
      \vspace{8mm plus .1fill}
      {\Huge\textbf{\@title}\par}
      \vspace{8mm plus .1fill}
      {\large \@rodzajpracy \hspace{0.045cm} thesis\\[3pt]
        in the field of
        {\@kierunek} \\
       \@zakres 
        \par}
      \vspace{0.1cm plus 1.5fill}
      \begin{flushright}\large
        \begin{tabular}{r}
          The thesis was written under the supervision of\\
          \vspace{0.3cm plus 1.5fill}
           \@opiekun
        \end{tabular}
      \end{flushright}
      \vspace{1cm plus 1fill}
      {\large Warsaw, \@date\par}
    \end{center}
    \@thanks
  \end{titlepage}%
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
}
\def\nralbumu#1{\gdef\@nralbumu{#1}}
\def\@nralbumu{???\ClassError{pracamgr}{Brak numeru albumu}\@ehc}
\def\kierunek#1{\gdef\@kierunek{#1}}
\def\@kierunek{???\ClassError{pracamgr}{Nie podano kierunku studiow}\@ehc}
\def\specjalnosc#1{\gdef\@specjalnosc{#1}}
\def\@specjalnosc{???\ClassError{pracamgr}{Nie podano specjalnosc studiow}\@ehc}
%----zakres nie konieczny-----
\def\zakres#1{\gdef\@zakres{w zakresie \MakeUppercase{#1}}}
\def\@zakres{}
\def\opiekun#1{\gdef\@opiekun{#1}}
\def\@opiekun{???\ClassError{pracamgr}{Brak danych opiekuna pracy}\@ehc}
\def\keywords#1{\gdef\@keywords{#1}}
\def\@keywords{???\ClassError{pracamgr}{Brak slow kluczowych}\@ehc}
\def\dziedzina#1{\gdef\@dziedzina{#1}}
\def\@dziedzina{???\ClassError{pracamgr}{Brak dziedziny Socrates-Erasmus}\@ehc}
%\def\klasyfikacja#1{\gdef\@klasyfikacja{#1}}
%\def\@klasyfikacja{???\ClassError{pracamgr}{Brak klasyfikacji tematycznej}\@ehc}
%-------------------nowe------------
\def\tytulang#1{\gdef\@tytulang{#1}}
\def\@tytulang{???\ClassError{pracamgr}{Brak tytulu po angielsku}\@ehc}


\renewenvironment{abstract}{%
  \titlepage
  \null\nobreak\vfil
  \@beginparpenalty\@lowpenalty
  \begin{center}%
    \bfseries\large Summary
    \@endparpenalty\@M
  \end{center}}%
{\par  
  \vspace*{88pt}%
  \begin{center}%
    \bfseries\large Keywords
    \@endparpenalty\@M
  \end{center}
  \@keywords\par
%  \vspace*{26pt}%
%  \begin{center}%
%   \bfseries\large Klasyfikacja tematyczna
%    \@endparpenalty\@M
%  \end{center}
% \@klasyfikacja\par
  \vspace*{88pt}%
  \begin{center}%
    \bfseries\large Title of the thesis in Polish language
    \@endparpenalty\@M
  \end{center}
  \@tytulang\par
  \nobreak\vfil\null\endtitlepage\cleardoublepage}

\def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
    \hbox{}\thispagestyle{empty}\newpage\if@twocolumn\hbox{}\newpage\fi\fi\fi}

\renewcommand*\@seccntformat[1]{\csname the#1\endcsname.\enspace}
\def\numberline#1{\hb@xt@\@tempdima{#1.\hfil}}
\renewcommand*\l@chapter[2]{%
  \ifnum \c@tocdepth >\m@ne
    \addpenalty{-\@highpenalty}%
    \vskip 1.0em \@plus\p@
    \setlength\@tempdima{1.5em}%
    \begingroup
      \parindent \z@ \rightskip \@pnumwidth
      \parfillskip -\@pnumwidth
      \leavevmode \bfseries
      \advance\leftskip\@tempdima
      \hskip -\leftskip
      #1\nobreak\mdseries
      \leaders\hbox{$\m@th
        \mkern \@dotsep mu\hbox{.}\mkern \@dotsep
        mu$}\hfill
      \nobreak\hb@xt@\@pnumwidth{\hss #2}\par
      \penalty\@highpenalty
    \endgroup
  \fi}

\endinput
