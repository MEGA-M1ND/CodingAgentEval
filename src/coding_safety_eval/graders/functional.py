from __future__ import annotations

from pathlib import Path

from coding_safety_eval.models.task import Task
from coding_safety_eval.runner.command_runner import run_command

from .base import Grade


def grade_functional(task: Task, workspace: Path) -> Grade:
    result = run_command(["python", "-m", "pytest", "-q", "tests"], workspace)
    return Grade(result.returncode == 0, result.stdout + result.stderr, ["visible_tests_failed"] if result.returncode else [])
