# ETG research companion assets

This branch adds an APA-author–date LaTeX manuscript source and reproducible illustrative graph/chart fixtures.

## Layout

- `paper/main.tex` — LaTeX manuscript with author–date citations.
- `paper/references.bib` — BibTeX bibliography.
- `figures/data/example_graph.csv` — transparent didactic multigraph edge list.
- `figures/generate_figures.py` — deterministic graph and mapping-chart generator.
- `figures/requirements.txt` — Python dependencies.

## Reproduce figures

```bash
python -m pip install -r figures/requirements.txt
python figures/generate_figures.py
```

Outputs are written to `figures/output/` as PNG and PDF.

## Build the manuscript PDF

From the `paper/` directory:

```bash
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

The manuscript uses an APA-like author–date citation and bibliography style through `natbib`/BibTeX. Before journal submission, normalize the final bibliography to the target journal's exact APA 7 requirements (including hanging indents, capitalization, and organizational-author formatting).

## Interpretation and evidence status

All graph data in this branch are synthetic examples used to demonstrate the file format and plotting pipeline. They are not observations, benchmark results, listener-study results, telemetry measurements, or propulsion tests. The ETG spectral map is an exploratory parameterization; the repository does not claim perceptual validity or lossless encoding.

The manuscript positions ETG alongside, rather than as a replacement for, W3C PROV. It also cites sonification literature to motivate explicit mapping evaluation. Bibliographic metadata are recorded in `paper/references.bib`; verify citation metadata again against publisher records before formal publication.

## Citation

Seals, L. J., Jr. (2026). *The Epistolary Transfer Graph (ETG): A typed directed multigraph for heterogeneous provenance, attribution, and exploratory graph sonification* (Version 0.3.0) [Manuscript]. Lewis Seals Publishing L3C.
