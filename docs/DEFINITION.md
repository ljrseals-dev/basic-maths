# Formal definition of the Epistolary Transfer Graph

## 1. Motivation

Formal letters asserting mathematical or scientific precedence, and the transfer of ideas between agents, are normally treated as unstructured text.  
Spacecraft telemetry and generative music systems require structured, low-bandwidth, robust encodings.  

The Epistolary Transfer Graph (ETG) supplies a single combinatorial object that can serve both communities.

## 2. Signature

An ETG is a 5-tuple \( G = (V, E, \tau, \lambda, \rho) \) where:

- \( V \) is a finite set of vertices.
- \( E \) is a finite set of directed multi-edges.
- \( \tau : E \to T \) assigns each edge a transfer type from a finite alphabet \( T \).
- \( \lambda : E \to \mathbb{R}_{\ge 0} \) assigns a non-negative strength (or musical interval weight).
- \( \rho \) is a deterministic nasal-resonance map from cycles (or distinguished paths) of \( G \) into a spectral/formant space.

## 3. Nasal resonance layer (the novel component)

Given a cycle \( C = (v_0, v_1, \dots, v_{k-1}) \), compute a cryptographic fingerprint of the ordered vertex identifiers.  
Map selected bytes of the fingerprint into three formant frequencies lying in the classic nasalised speech / musical formant bands:

- F1 ∈ [200, 600] Hz  
- F2 ∈ [800, 2000] Hz  
- F3 ∈ [2200, 4000] Hz  

Amplitude is modulated by the total transfer strength along the cycle.  

The resulting triple + amplitude can be:

- synthesised as a sustained nasalised vowel or chord, or  
- used as a continuous-wave modulation signature for a reaction-control thruster or low-power interstellar beacon.

Because the map is deterministic and collision-resistant under the chosen hash, two independent implementations of an ETG that agree on the cycle will radiate identical spectral signatures.

## 4. Design invariants

- Vertices are first-class citizens (a letter is not merely an edge label).
- Multiple typed transfers between the same pair of claims are permitted.
- The nasal layer never requires floating-point search; it is pure combinatorial + hash.
- The object admits a natural Lean formalisation (future work).

## 5. Relation to prior art

No existing graph formalism simultaneously:

1. treats formal letters / precedence claims as vertices,
2. carries typed multi-edges for mathematical transfer,
3. and supplies a canonical, hash-driven nasal-formant spectral layer intended for both music and spacecraft propulsion/telemetry.

That combination is the novelty claim of the ETG (22 November 2026).
