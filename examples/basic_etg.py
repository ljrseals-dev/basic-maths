#!/usr/bin/env python3
"""
Minimal working example of the Epistolary Transfer Graph.

Models a simplified formal precedence letter as vertices and transfer edges,
then computes the novel nasal-resonance spectral signature.
"""

import sys
sys.path.insert(0, "../src")

from etg import EpistolaryTransferGraph, Vertex, Edge

def main():
    g = EpistolaryTransferGraph(name="PrecedenceLetter-2026-11-21")

    # Vertices represent statements / claims inside a formal letter
    g.add_vertex(Vertex("L0", kind="letter", metadata={"date": "2026-11-21", "author": "REG"}))
    g.add_vertex(Vertex("C1", kind="claim", metadata={"topic": "prime_fluctuations"}))
    g.add_vertex(Vertex("C2", kind="claim", metadata={"topic": "centered_prime_power"}))
    g.add_vertex(Vertex("C3", kind="claim", metadata={"topic": "reciprocal_cancellation"}))
    g.add_vertex(Vertex("C4", kind="claim", metadata={"topic": "exact_prime_counting"}))
    g.add_vertex(Vertex("C5", kind="claim", metadata={"topic": "jacobian_algebraic"}))

    # Transfer edges (precedence / influence / algebraic)
    g.add_edge(Edge("L0", "C1", "precedence", strength=0.9, label="dated 31 Dec 2025"))
    g.add_edge(Edge("L0", "C2", "precedence", strength=0.85, label="22 Aug 2026"))
    g.add_edge(Edge("L0", "C3", "precedence", strength=0.8, label="22 Aug 2026"))
    g.add_edge(Edge("L0", "C4", "precedence", strength=0.88, label="13 Oct 2026"))
    g.add_edge(Edge("L0", "C5", "algebraic_embedding", strength=0.95, label="3+sqrt(10)"))
    g.add_edge(Edge("C1", "C2", "influence", strength=0.7))
    g.add_edge(Edge("C2", "C3", "influence", strength=0.65))
    g.add_edge(Edge("C5", "C1", "harmonic_modulation", strength=0.6))

    print(g)
    print("\nNasal resonance of the dominant cycle:")
    sig = g.nasal_resonance()
    for k, v in sig.items():
        print(f"  {k}: {v}")

    g.save("sample_precedence_letter.json")
    print("\nSaved sample_precedence_letter.json")

if __name__ == "__main__":
    main()
