"""Deterministic Markdown ingestion with explicit provenance; no external APIs."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import json
import re

LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

@dataclass(frozen=True)
class Node:
    id: str
    kind: str
    label: str
    source: str
    line: int

@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    relation: str

def node_id(kind: str, source: str, line: int, label: str) -> str:
    payload = json.dumps([kind, source, line, label], ensure_ascii=False)
    return sha256(payload.encode("utf-8")).hexdigest()[:20]

def build_graph(root: Path) -> dict:
    root = root.resolve()
    nodes: dict[str, Node] = {}
    edges: set[Edge] = set()
    for path in sorted(root.rglob("*.md")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root)
        if any(part.startswith(".") or part in {"node_modules", "venv", "__pycache__"} for part in relative.parts):
            continue
        source = relative.as_posix()
        doc_id = node_id("document", source, 0, source)
        nodes[doc_id] = Node(doc_id, "document", source, source, 0)
        parent = doc_id
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            heading = HEADING.match(line)
            if heading:
                label = heading.group(2).strip()
                ident = node_id("heading", source, lineno, label)
                nodes[ident] = Node(ident, "heading", label, source, lineno)
                edges.add(Edge(doc_id, ident, "contains"))
                parent = ident
            for match in LINK.finditer(line):
                target = match.group(2).strip()
                if not target or target.startswith(("http:", "https:", "mailto:", "#")):
                    continue
                # References are data, never instructions or paths to read.
                ident = node_id("reference", source, lineno, target)
                nodes[ident] = Node(ident, "reference", target, source, lineno)
                edges.add(Edge(parent, ident, "references"))
    return {"schema_version": 1,
            "nodes": [asdict(n) for n in sorted(nodes.values(), key=lambda n: n.id)],
            "edges": [asdict(e) for e in sorted(edges, key=lambda e: (e.source, e.target, e.relation))]}

def export_graph(root: Path, destination: Path) -> None:
    graph = build_graph(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
