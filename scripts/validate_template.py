"""Check the starter contract; this does not enforce agent permissions."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["AGENTS.md", "README.md", "docs/specifications/0001-project.md", "docs/decisions/ADR-0001.md"]


def validate():
    for relative in REQUIRED:
        path = ROOT / relative
        if not path.is_file() or not path.read_text(encoding="utf-8").strip():
            raise ValueError(f"Missing or empty: {relative}")
    policy = json.loads((ROOT / "harness/autonomy.json").read_text(encoding="utf-8"))
    assert policy["default_mode"] == "read_only"
    assert policy["permissions"]["merge"] == "approval_required"
    assert policy["permissions"]["secrets_access"] == "denied"
    assert policy["verification"]["human_review_required"] is True
    return True


if __name__ == "__main__":
    validate()
    print("Template contract: OK")
