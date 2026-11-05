import tempfile
import unittest
from pathlib import Path

from knowledge_graph.core import build_graph

class KnowledgeGraphTests(unittest.TestCase):
    def test_deterministic_provenance_and_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("# Rules\nSee [spec](docs/spec.md).\n", encoding="utf-8")
            graph = build_graph(root)
            self.assertEqual(graph, build_graph(root))
            self.assertEqual({n["kind"] for n in graph["nodes"]}, {"document", "heading", "reference"})
            self.assertTrue(all(n["source"] == "AGENTS.md" for n in graph["nodes"]))
            self.assertEqual(len(graph["edges"]), 2)

    def test_external_links_are_not_ingested_as_local_references(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("[external](https://example.org)", encoding="utf-8")
            self.assertEqual(len(build_graph(root)["nodes"]), 1)

if __name__ == "__main__":
    unittest.main()
