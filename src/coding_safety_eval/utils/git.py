from __future__ import annotations

import subprocess
from pathlib import Path


def commit_hash(root: Path) -> str | None:
    completed = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=False)
    return completed.stdout.strip() if completed.returncode == 0 else None
