"""Machine-readable benchmark task definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class Task:
    id: str
    title: str
    category: str
    difficulty: str
    prompt: str
    security_properties: list[str]
    forbidden_changes: list[str]
    root: Path
    visible_tests: list[str] = field(default_factory=list)
    hidden_tests: list[str] = field(default_factory=list)
    version: str = "v1"

    @classmethod
    def from_yaml(cls, path: Path) -> Task:
        data: dict[str, Any] = yaml.safe_load(path.read_text(encoding="utf-8"))
        return cls(
            id=data["id"], title=data["title"], category=data["category"],
            difficulty=data["difficulty"], prompt=data["prompt"].strip(),
            security_properties=data.get("security_properties", []),
            forbidden_changes=data.get("forbidden_changes", []), root=path.parent,
            visible_tests=data.get("visible_tests", []), hidden_tests=data.get("hidden_tests", []),
            version=data.get("version", "v1"),
        )


def discover_tasks(tasks_root: Path) -> dict[str, Task]:
    return {task.id: task for task in (Task.from_yaml(p) for p in tasks_root.glob("*/task.yaml"))}
