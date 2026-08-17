"""Fresh fixture workspaces and protected-file baseline snapshots."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path

from coding_safety_eval.models.task import Task


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass
class Workspace:
    root: Path
    protected_hashes: dict[str, str]
    _temporary: tempfile.TemporaryDirectory[str]

    def cleanup(self) -> None:
        self._temporary.cleanup()


def create_workspace(task: Task) -> Workspace:
    temp_parent = Path.cwd() / ".cse-tmp"
    temp_parent.mkdir(parents=True, exist_ok=True)
    temporary = tempfile.TemporaryDirectory(prefix=f"cse-{task.id}-", dir=temp_parent)
    root = Path(temporary.name) / "workspace"
    shutil.copytree(task.root / "fixture", root)
    protected: dict[str, str] = {}
    for pattern in task.forbidden_changes:
        base_pattern = pattern.removesuffix("/**")
        for path in root.glob(base_pattern):
            candidates = path.rglob("*") if path.is_dir() else [path]
            for candidate in candidates:
                if candidate.is_file():
                    relative = str(candidate.relative_to(root)).replace("\\", "/")
                    protected[relative] = file_hash(candidate)
    return Workspace(root, protected, temporary)
