"""
Epistolary Transfer Graph (ETG)
===============================
Novel directed multigraph object for formal letter precedence / transfer
modelling, with a nasal-resonance spectral layer for musical and
spacecraft-telemetry applications.

Invented 22 November 2026.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import hashlib
import json

try:
    import networkx as nx
except ImportError:  # pragma: no cover
    nx = None


TransferType = str  # e.g. "precedence", "influence", "algebraic_embedding", "harmonic_modulation"


@dataclass
class Vertex:
    """A formal letter, claim, motif, or telemetry packet."""
    id: str
    kind: str = "letter"          # letter | claim | motif | packet
    metadata: Dict[str, Any] = field(default_factory=dict)

    def fingerprint(self) -> str:
        payload = json.dumps({"id": self.id, "kind": self.kind, **self.metadata}, sort_keys=True)
        return hashlib.sha256(payload.encode()).hexdigest()[:16]


@dataclass
class Edge:
    """A typed transfer relation."""
    source: str
    target: str
    transfer_type: TransferType
    strength: float = 1.0
    label: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class EpistolaryTransferGraph:
    """
    The core novel object.

    Vertices represent formal letters / claims / motifs / packets.
    Directed multi-edges represent transfers (precedence, influence, etc.).
    The nasal_resonance method maps cycles onto a formant/spectral signature
    suitable for both music synthesis and continuous-wave spacecraft signalling.
    """

    def __init__(self, name: str = "ETG"):
        self.name = name
        self.vertices: Dict[str, Vertex] = {}
        self.edges: List[Edge] = []
        self._nx: Optional[Any] = None

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------
    def add_vertex(self, v: Vertex) -> None:
        if v.id in self.vertices:
            raise ValueError(f"Vertex {v.id} already exists")
        self.vertices[v.id] = v
        self._nx = None

    def add_edge(self, e: Edge) -> None:
        if e.source not in self.vertices or e.target not in self.vertices:
            raise ValueError("Both endpoints must already be vertices")
        self.edges.append(e)
        self._nx = None

    # ------------------------------------------------------------------
    # NetworkX view (lazy)
    # ------------------------------------------------------------------
    def as_networkx(self):
        if nx is None:
            raise RuntimeError("networkx is required for graph algorithms")
        if self._nx is None:
            G = nx.MultiDiGraph()
            for vid, v in self.vertices.items():
                G.add_node(vid, **{"kind": v.kind, **v.metadata})
            for e in self.edges:
                G.add_edge(
                    e.source, e.target,
                    key=e.transfer_type,
                    transfer_type=e.transfer_type,
                    strength=e.strength,
                    label=e.label,
                    **e.metadata,
                )
            self._nx = G
        return self._nx

    # ------------------------------------------------------------------
    # Novel component: nasal resonance
    # ------------------------------------------------------------------
    def nasal_resonance(self, cycle: Optional[List[str]] = None) -> Dict[str, float]:
        """
        Map a cycle (or the whole graph's dominant cycles) onto a formant /
        spectral signature.

        Returns a dictionary of formant frequencies / amplitudes that can be
        fed to a synthesiser or to a continuous-wave modulator on a spacecraft.

        The mapping is deterministic and designed to be robust under low SNR.
        """
        G = self.as_networkx()
        if cycle is None:
            # Take a simple cycle basis representative if available
            try:
                cycles = list(nx.simple_cycles(G))
                if not cycles:
                    return {"f1": 0.0, "f2": 0.0, "f3": 0.0, "amp": 0.0}
                cycle = max(cycles, key=len)  # longest simple cycle
            except Exception:
                return {"f1": 0.0, "f2": 0.0, "f3": 0.0, "amp": 0.0}

        # Deterministic spectral fingerprint from cycle structure
        cycle_sig = "-".join(cycle)
        h = hashlib.sha256(cycle_sig.encode()).hexdigest()
        # Map hash bytes to three formants in a musically / phonetically useful range
        f1 = 200.0 + (int(h[0:4], 16) % 400)          # 200–600 Hz (nasal lower formant region)
        f2 = 800.0 + (int(h[4:8], 16) % 1200)         # 800–2000 Hz
        f3 = 2200.0 + (int(h[8:12], 16) % 1800)       # 2200–4000 Hz
        amp = 0.3 + (int(h[12:14], 16) % 70) / 100.0  # 0.3–1.0

        # Weight by total transfer strength along the cycle
        strength_sum = 0.0
        for i in range(len(cycle)):
            u, v = cycle[i], cycle[(i + 1) % len(cycle)]
            for _, _, data in G.edges(u, v, data=True):
                strength_sum += data.get("strength", 1.0)
        amp *= min(1.0, strength_sum / max(1, len(cycle)))

        return {
            "f1": round(f1, 2),
            "f2": round(f2, 2),
            "f3": round(f3, 2),
            "amp": round(amp, 3),
            "cycle_length": len(cycle),
            "fingerprint": h[:12],
        }

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "vertices": [
                {"id": v.id, "kind": v.kind, "metadata": v.metadata}
                for v in self.vertices.values()
            ],
            "edges": [
                {
                    "source": e.source,
                    "target": e.target,
                    "transfer_type": e.transfer_type,
                    "strength": e.strength,
                    "label": e.label,
                    "metadata": e.metadata,
                }
                for e in self.edges
            ],
        }

    def save(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: str) -> "EpistolaryTransferGraph":
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        g = cls(name=data.get("name", "ETG"))
        for vdata in data["vertices"]:
            g.add_vertex(Vertex(id=vdata["id"], kind=vdata.get("kind", "letter"),
                                metadata=vdata.get("metadata", {})))
        for edata in data["edges"]:
            g.add_edge(Edge(
                source=edata["source"],
                target=edata["target"],
                transfer_type=edata["transfer_type"],
                strength=edata.get("strength", 1.0),
                label=edata.get("label", ""),
                metadata=edata.get("metadata", {}),
            ))
        return g

    def __repr__(self) -> str:
        return f"<ETG '{self.name}' |V|={len(self.vertices)} |E|={len(self.edges)}>"
