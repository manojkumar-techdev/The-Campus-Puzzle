"""graph_engine.py -- Stage 2: Conflict graph + Welsh-Powell colouring."""

from typing import Dict, List, Tuple

from src.data_loader import Problem


class ConflictGraph:
    def __init__(self):
        self.adj: Dict[str, List[str]] = {}

    def add_node(self, node_id: str) -> None:
        self.adj.setdefault(node_id, [])

    def add_edge(self, a: str, b: str) -> None:
        self.adj.setdefault(a, [])
        self.adj.setdefault(b, [])
        if b not in self.adj[a]:
            self.adj[a].append(b)
        if a not in self.adj[b]:
            self.adj[b].append(a)

    def get(self, node_id: str, default=None) -> List[str]:
        if default is None:
            default = []
        return self.adj.get(node_id, default)

    def nodes(self) -> List[str]:
        return list(self.adj.keys())

    def degree(self, node_id: str) -> int:
        return len(self.adj.get(node_id, []))

    def edges(self) -> List[Tuple[str, str]]:
        seen = set()
        out = []
        for u, nbrs in self.adj.items():
            for v in nbrs:
                key = tuple(sorted((u, v)))
                if key not in seen:
                    seen.add(key)
                    out.append((u, v))
        return out


def build_conflict_graph(problem: Problem) -> ConflictGraph:
    g = ConflictGraph()
    classes = problem.classes
    for c in classes:
        g.add_node(c.id)

    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            a, b = classes[i], classes[j]
            shares_group = bool(set(a.student_groups) & set(b.student_groups))
            same_prof = a.professor_id == b.professor_id
            if shares_group or same_prof:
                g.add_edge(a.id, b.id)
    return g


def welsh_powell_coloring(
    graph: ConflictGraph, time_slots: List[str]
) -> Tuple[Dict[str, str], List[str]]:
    nodes = sorted(graph.nodes(), key=lambda n: (-graph.degree(n), n))
    coloring: Dict[str, str] = {}

    for node in nodes:
        used = set()
        for nbr in graph.get(node):
            if nbr in coloring:
                used.add(coloring[nbr])
        for slot in time_slots:
            if slot not in used:
                coloring[node] = slot
                break

    uncolored = [n for n in nodes if n not in coloring]
    return coloring, uncolored


def report(problem, graph, coloring, uncolored, greedy_conflicts) -> str:
    used_colors = set(coloring.values())
    lines = []
    lines.append("  Graph Theory Report")
    lines.append("  " + "-" * 55)
    lines.append(f"  Graph nodes         : {len(graph.nodes())}")
    lines.append(f"  Graph edges         : {len(graph.edges())}")
    lines.append(f"  Colours used        : {len(used_colors)} / {len(problem.time_slots)}")
    lines.append(f"  Classes coloured    : {len(coloring)}")
    lines.append(f"  Classes uncoloured  : {len(uncolored)}")
    lines.append(f"  Greedy conflicts    : {greedy_conflicts}")
    lines.append(f"  Graph conflicts     : 0  (by construction)")
    return "\n".join(lines)