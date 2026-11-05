import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_template import validate


class TemplateTests(unittest.TestCase):
    def test_contract(self):
        self.assertTrue(validate())


if __name__ == "__main__":
    unittest.main()
