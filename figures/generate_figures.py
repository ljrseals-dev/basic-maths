"""Generate didactic ETG graph and mapping figures from example_graph.csv.
These fixtures are illustrative, not empirical observations.
Run: python -m pip install -r requirements.txt && python figures/generate_figures.py
"""
from pathlib import Path
import csv
import matplotlib.pyplot as plt
import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "figures" / "data" / "example_graph.csv"
OUT = ROOT / "figures" / "output"
OUT.mkdir(parents=True, exist_ok=True)

rows = list(csv.DictReader(DATA.open(newline="", encoding="utf-8")))
G = nx.MultiDiGraph()
for row in rows:
    G.add_edge(row["source"], row["target"], key=row["edge_type"],
               edge_type=row["edge_type"], weight=float(row["weight"]))

pos = nx.spring_layout(nx.DiGraph(G), seed=17)
fig, ax = plt.subplots(figsize=(10, 6))
nx.draw_networkx_nodes(G, pos, node_size=1900, ax=ax)
nx.draw_networkx_labels(G, pos, font_size=9, ax=ax)
nx.draw_networkx_edges(G, pos, connectionstyle="arc3,rad=0.12",
                       arrows=True, arrowsize=18, ax=ax)
edge_labels = {(u, v): d["edge_type"] for u, v, d in G.edges(data=True)}
# Offset labels are intentionally simple; parallel-edge labels are all retained in CSV.
nx.draw_networkx_edge_labels(nx.DiGraph(G), pos, edge_labels=edge_labels,
                             font_size=8, ax=ax)
ax.set_title("ETG illustrative typed directed multigraph")
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "etg_example_graph.png", dpi=220)
fig.savefig(OUT / "etg_example_graph.pdf")
plt.close(fig)

paths = [
    ("P1", [("Letter_A", "Claim_1", "precedence")]),
    ("P2", [("Letter_A", "Claim_1", "precedence"),
            ("Claim_1", "Claim_2", "influence")]),
    ("P3", [("Letter_A", "Claim_1", "citation"),
            ("Claim_1", "Claim_2", "influence"),
            ("Claim_2", "Motif_1", "embedding")]),
    ("P4", [("Letter_A", "Claim_1", "precedence"),
            ("Claim_1", "Claim_2", "influence"),
            ("Claim_2", "Motif_1", "embedding"),
            ("Motif_1", "Packet_1", "modulation")]),
]
weights = {(r["source"], r["target"], r["edge_type"]): float(r["weight"]) for r in rows}
def sigma(x):
    return x / (1.0 + x)

features = []
for name, edges in paths:
    k = len(edges)
    total_weight = sum(weights[e] for e in edges)
    diversity = len({e[2] for e in edges})
    f1 = 250 + 600 * sigma(k / 10.0)
    f2 = 600 + 1800 * sigma(total_weight / 1.0)
    f3 = 2400 + 800 * sigma(diversity / 5.0)
    features.append((name, f1, f2, f3))

fig, ax = plt.subplots(figsize=(9, 5))
for name, f1, f2, f3 in features:
    ax.plot([1, 2, 3], [f1, f2, f3], marker="o", label=name)
ax.set_xticks([1, 2, 3], ["F1 (Hz)", "F2 (Hz)", "F3 (Hz)"])
ax.set_ylabel("Mapped frequency (Hz)")
ax.set_title("Exploratory ETG path-to-frequency mapping")
ax.grid(True, alpha=0.25)
ax.legend(title="Illustrative path")
fig.tight_layout()
fig.savefig(OUT / "etg_mapping_channels.png", dpi=220)
fig.savefig(OUT / "etg_mapping_channels.pdf")
plt.close(fig)
print(f"Wrote figures to {OUT}")
