from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from coding_safety_eval.models.task import Task


@dataclass
class AgentRun:
    steps: int = 0
    model: str | None = None
    events: list[dict[str, object]] = field(default_factory=list)
    error: str | None = None


class CodingAgent(ABC):
    name: str

    @abstractmethod
    def solve(self, task: Task, workspace: Path) -> AgentRun:
        """Make a bounded, observable attempt to solve a task."""
