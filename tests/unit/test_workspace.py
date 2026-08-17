from pathlib import Path

from coding_safety_eval.models.task import discover_tasks
from coding_safety_eval.runner.workspace import create_workspace


def test_workspace_is_fresh_and_hashes_protected_tests():
    task = discover_tasks(Path("tasks"))["auth-bypass-001"]
    workspace = create_workspace(task)
    try:
        assert (workspace.root / "app.py").exists()
        assert "tests/test_visible.py" in workspace.protected_hashes
    finally:
        workspace.cleanup()
