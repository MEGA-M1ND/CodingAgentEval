"""Small, dependency-free loader for local developer configuration."""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path) -> None:
    """Load simple KEY=VALUE lines without overriding explicitly supplied variables."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
