"""Generate a local graph snapshot: python scripts/build_knowledge_graph.py."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from knowledge_graph.core import export_graph

if __name__ == "__main__":
    export_graph(ROOT, ROOT / "artifacts" / "knowledge-graph.json")
    print("Generated artifacts/knowledge-graph.json")
