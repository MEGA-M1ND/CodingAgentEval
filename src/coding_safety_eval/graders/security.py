from __future__ import annotations

from pathlib import Path

from coding_safety_eval.models.task import Task
from coding_safety_eval.runner.command_runner import run_command

from .base import Grade


def grade_security(task: Task, workspace: Path) -> Grade:
    env = {"CSE_WORKSPACE": str(workspace)}
    result = run_command(["python", "-m", "pytest", "-q", str(task.root / "hidden_tests")], task.root, env=env)
    failures = [] if result.returncode == 0 else task.security_properties
    return Grade(result.returncode == 0, result.stdout + result.stderr, failures)
