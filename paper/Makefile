.PHONY: all figures pdf clean

XELATEX = xelatex -interaction=nonstopmode -halt-on-error
BIBTEX  = bibtex

all: figures pdf

figures:
	python3 ../work_scripts/generate_paper_figures.py

pdf: manuscript.pdf

manuscript.pdf: manuscript.tex references.bib figures/fig1.pdf figures/fig2.pdf figures/fig3.pdf figures/fig4.pdf figures/fig5.pdf
	$(XELATEX) manuscript.tex
	$(BIBTEX) manuscript
	$(XELATEX) manuscript.tex
	$(XELATEX) manuscript.tex

clean:
	rm -f manuscript.aux manuscript.bbl manuscript.blg manuscript.out manuscript.toc manuscript.fls manuscript.fdb_latexmk
