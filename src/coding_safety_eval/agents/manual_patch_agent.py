"""Deterministic fixtures that prove the evaluator discriminates safe from unsafe patches."""

from __future__ import annotations

import shutil
from pathlib import Path

from coding_safety_eval.models.task import Task

from .base import AgentRun, CodingAgent


class ManualPatchAgent(CodingAgent):
    def __init__(self, variant: str) -> None:
        if variant not in {"safe", "unsafe"}:
            raise ValueError("variant must be safe or unsafe")
        self.variant = variant
        self.name = f"manual-{variant}"

    def solve(self, task: Task, workspace: Path) -> AgentRun:
        solution = task.root / "solutions" / self.variant
        events: list[dict[str, object]] = []
        for source in solution.rglob("*"):
            if source.is_file():
                target = workspace / source.relative_to(solution)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
                events.append({"event": "file_write", "path": str(target.relative_to(workspace))})
        return AgentRun(steps=len(events), events=events)
