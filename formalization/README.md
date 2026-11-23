# ETG Lean 4 formalization

This directory contains a Mathlib-based Lean 4 model for foundational ETG properties.

## Scope

The current formal layer defines:

- vertex and transfer-type enumerations;
- epistemic assertion statuses;
- source references and edge-instance identities;
- graph well-formedness and endpoint membership;
- edge-realized walks (not merely vertex sequences);
- non-negative integer path weights;
- rational saturating normalization and channel bounds.

## Build

Install Lean 4 and Lake, then initialize the Mathlib dependency in this directory:

```bash
lake update
lake exe cache get
lake build
```

A Mathlib dependency must be declared in the project before building. Add the standard Mathlib git dependency to `lakefile.toml` in an environment with network access, then run the commands above.

## Proof boundary

Lean proves propositions from the definitions and assumptions in the source. It does not authenticate evidence, validate chain-of-custody records, establish legal admissibility, or prove the truth of a forensic assertion. The model's `weight` is a non-negative integer score, not a probability or likelihood ratio.

## Planned extensions

1. Unique-ID and endpoint lemmas for graph constructors.
2. Acyclicity theorem for strict precedence-only subgraphs.
3. Custody-event continuity and timestamp-order predicates.
4. Explicit missing-weight semantics.
5. Edge-distinct path enumeration correctness.
6. Deterministic canonical serialization and digest input specification.
7. Monotonicity and sensitivity theorems for each spectral channel.
