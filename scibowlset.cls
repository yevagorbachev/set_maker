% Class for Science Bowl question sets
% Requried: After \begin{document}, \newcounter{qnumber}\stepcounter{qnumber}

\ProvidesClass{scibowlset}

\LoadClass[11pt,letterpaper]{article}

\usepackage[letterpaper, portrait, margin=1in]{geometry}
\usepackage[overload]{textcase}
\usepackage{mathptmx}
\nofiles
\setlength\parindent{0pt}

\def \title #1{\def \@title{#1}}
\def \ta #1{\def \@ta{#1}}
\def \bn #1{\def \@bn{#1}}


\newcommand{\switchfour}[5]{
    \ifcase #5
        \or #1
        \or #2
        \or #3
        \or #4
    \fi
}

\newcommand{\numtoletter}[1]{
    \switchfour{W}{X}{Y}{Z}{#1}
}

\newcommand{\mc}[5] {
    % \mc {<choice w text>}{<choice x text>}{<choice y text>}{<choice z text>}{<correct choice index from 1>}
    W) #1
    \\ X) #2
    \\ Y) #3
    \\ Z) #4
    \\\\ ANSWER: \numtoletter{#5}) \MakeUppercase{\switchfour{#1}{#2}{#3}{#4}{#5}}
}

\newcommand{\sa}[1] {
    ANSWER: \MakeUppercase{#1}
}

\newcommand{\question}[5] {
    % \question{<number>}{<subject>}{<format>}{<question text>}{<answer(s)>}
    #1) \MakeUppercase{#2 }--{ \em #3}\hphantom{0} #4
    \\\\ #5
}

\newenvironment{pair}{
    \begin{minipage}{\textwidth}
    % REQUIRED:
    % \ta{\question{\theqnumber}{...}}
    % \bn{\question{\theqnumber}{...}}
} {
    \begin{center}{\bf TOSS-UP}\end{center}
    \@ta \\
    \begin{center}{\bf BONUS}\end{center}
    \@bn \\
    \begin{center}\underline{\hspace{4in}}\end{center}
    \end{minipage}
    \stepcounter{qnumber}
}