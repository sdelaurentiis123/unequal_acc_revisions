# Submission directory — Overleaf-ready

This directory contains everything needed to compile the paper, and nothing else.

## Contents

- `main.tex` — manuscript source
- `main.bib` — bibliography
- 14 figure PDFs referenced by `\includegraphics` in `main.tex`

## Compile

Standalone (Docker, MNRAS class via TeX Live):

```
docker run --rm -v "$PWD":/work -w /work texlive/texlive:latest bash -c '
  pdflatex main.tex && bibtex main && pdflatex main.tex && pdflatex main.tex
'
```

Or upload the directory contents to a fresh Overleaf project.

## Last verified

Builds cleanly to a 15-page PDF (~2 MB). One harmless bib warning about
an extra `journal` field on `dorazio_2013`.
