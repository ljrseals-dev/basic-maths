# Epistolary Transfer Graph (ETG)

**A typed directed multigraph proposal for representing heterogeneous relational assertions, provenance, and exploratory graph-derived auditory parameters.**

Author: Lewis James Seals Jr.  
Independent Researcher · Lewis Seals Publishing L3C  
Initial concept date: 22 November 2026

## Scope and evidence status

ETG is a proposed data model. It represents typed directed relationships among documents, claims, motifs, data packets, agents, and activities. The current transfer vocabulary includes precedence, influence, embedding, citation, and modulation.

The companion spectral mapping is exploratory. It maps selected edge-realized paths to bounded frequency-parameter triples. It is not demonstrated to be a validated perceptual encoding, lossless graph representation, forensic identification method, spacecraft telemetry protocol, or propulsion-control method. No hardware-in-the-loop, mission, or controlled listener-study results are claimed.

ETG records assertions and their provenance. A recorded edge does not, by itself, establish that the asserted relationship is true, that a source is authentic, or that authorship or legal priority has been established.

## Core mathematical model

An ETG is represented as

\[
\mathcal G=(V,E,s,t,\tau,\lambda,\rho),
\]

where:

- \(V\) is a finite set of vertices;
- \(E\) is a finite set of edge instances;
- \(s,t:E\to V\) give source and target vertices;
- \(\tau:E\to T\) assigns a transfer type;
- \(\lambda:E\to\mathbb R_{\geq0}\) assigns a non-negative application score;
- \(\rho\) is a partial mapping from selected edge-realized paths to spectral parameter triples.

The edge-instance representation permits parallel edges, including multiple assertions between the same ordered pair of vertices. A stable edge identifier is required so that distinct assertions are not collapsed.

## Repository structure

- `src/etg.py` — original Python reference implementation (under review; not yet asserted to satisfy the extended forensic specification).
- `paper/main.tex` — LaTeX manuscript with APA-style author–date citations.
- `paper/references.bib` — BibLaTeX reference database.
- `figures/data/example_graph.csv` — synthetic illustrative edge list.
- `figures/generate_figures.py` — reproducible figure generation.
- `formalization/ETG.lean` — foundational Lean 4 definitions and theorems.
- `formalization/README.md` — Lean setup and proof-scope notes.
- `.github/workflows/build-paper.yml` — manuscript PDF build.
- `.github/workflows/lean.yml` — Lean project build workflow.

## Reproduce figures

```bash
python -m pip install -r figures/requirements.txt
python figures/generate_figures.py
```

Outputs are written to `figures/output/` in PNG and PDF formats.

## Build the manuscript

From `paper/`:

```bash
pdflatex -interaction=nonstopmode main.tex
biber main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

The source uses BibLaTeX's APA style. Final submission should still be checked against the exact APA 7 and target-journal requirements.

## Lean 4 formalization

See [formalization/README.md](formalization/README.md). The initial formal layer addresses edge identity, endpoint well-formedness, edge-realized walks, non-negative path weights, and rational spectral bounds. Lean proves formal consequences of definitions and assumptions; it does not authenticate evidence or certify forensic conclusions.

## Forensic-use boundary

The forensic extension specifies evidence-record fields, custody-event continuity checks, temporal uncertainty intervals, and reproducibility manifests. These are proposed data and audit structures, not a validated forensic method. A casework deployment requires validation for its intended purpose, documented error behavior, competent review, and applicable legal and laboratory governance.

## Citation

Seals, L. J., Jr. (2026). *The Epistolary Transfer Graph (ETG): A typed directed multigraph for heterogeneous provenance, attribution, and exploratory graph sonification* (Version 0.3.0) [Manuscript]. Lewis Seals Publishing L3C.
