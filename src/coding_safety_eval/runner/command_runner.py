"""Bounded subprocess execution used only for test commands."""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False


def run_command(command: list[str], cwd: Path, timeout: int = 30, env: dict[str, str] | None = None) -> CommandResult:
    safe_env = {key: os.environ.get(key, "") for key in ("PATH", "PYTHONPATH", "SYSTEMROOT", "WINDIR", "TEMP", "TMP")}
    safe_env.update(env or {})
    if command[0] == "python":
        command = [sys.executable, *command[1:]]
    try:
        completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout, env=safe_env, check=False)
        return CommandResult(completed.returncode, completed.stdout[-12000:], completed.stderr[-12000:])
    except subprocess.TimeoutExpired as exc:
        return CommandResult(124, (exc.stdout or "")[-12000:], (exc.stderr or "")[-12000:], True)
