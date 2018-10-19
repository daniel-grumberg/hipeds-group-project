SHELL := /bin/bash # Use bash syntax
PDFLATEX = xelatex
BIBTEX   = bibtex

MAIN = main

# "make" target

all: pdf

# PDF compilation

bib:
	$(PDFLATEX) $(MAIN).tex
	$(BIBTEX)   $(MAIN)
	$(PDFLATEX) $(MAIN).tex
	$(PDFLATEX) $(MAIN).tex

# Fast compilation, where supported

fast:
	latexmk -pdf -pdflatex="xelatex -interaction=nonstopmode" $(MAIN).tex

# compilation without references

pdf:
	$(PDFLATEX) $(MAIN).tex
	$(PDFLATEX) $(MAIN).tex

up:

	pushd .. ; svn up ; popd

# clean-up
clean:
	rm -f *.bbl *.blg *.log *.aux *.nav *.out *.snm *.synctex.gz *.toc *.vrb *.bcf *.run.xml *.xwm *.fls *.fdb_latexmk *.lof *.lot
	rm -f slides/*.log
