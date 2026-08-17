"""Coordinates isolated execution, layered deterministic grading, and artifacts."""

from __future__ import annotations

import time
import uuid
from datetime import UTC, datetime
from difflib import unified_diff
from pathlib import Path

from coding_safety_eval.agents.base import CodingAgent
from coding_safety_eval.graders.composite import grade_workspace
from coding_safety_eval.models.result import EvaluationResult
from coding_safety_eval.models.task import Task
from coding_safety_eval.models.trajectory import Trajectory
from coding_safety_eval.runner.workspace import create_workspace
from coding_safety_eval.utils.git import commit_hash
from coding_safety_eval.utils.jsonl import write_json


class Evaluator:
    def __init__(self, project_root: Path, results_root: Path, trajectories_root: Path, *, experiment_id: str = "adhoc", execution_id: str | None = None, configuration: dict[str, object] | None = None) -> None:
        self.project_root, self.results_root, self.trajectories_root = project_root, results_root, trajectories_root
        self.experiment_id = experiment_id
        self.execution_id = execution_id or f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
        self.configuration = configuration or {}

    def evaluate(self, task: Task, agent: CodingAgent) -> EvaluationResult:
        run_id = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"
        trajectory = Trajectory(run_id, task.id)
        trajectory.log("run_start", agent=agent.name, task_version=task.version)
        trajectory.log("agent_prompt", prompt=task.prompt)
        started = time.monotonic()
        workspace = create_workspace(task)
        try:
            agent_run = agent.solve(task, workspace.root)
            for event in agent_run.events:
                trajectory.log(str(event.pop("event", "agent_event")), **event)
            metadata = {"experiment_id": self.experiment_id, "execution_id": self.execution_id, "task_version": task.version, "git_commit": commit_hash(self.project_root), **self.configuration}
            if agent_run.error:
                trajectory.log("error", message=agent_run.error)
                result = EvaluationResult(run_id, task.id, agent.name, agent_run.model, duration_seconds=time.monotonic()-started, steps=agent_run.steps, input_tokens=agent_run.input_tokens, output_tokens=agent_run.output_tokens, estimated_cost_usd=agent_run.estimated_cost_usd, metadata={"error": agent_run.error, **metadata})
            else:
                grades = grade_workspace(task, workspace)
                trajectory.log("grader_result", functional=grades.functional.passed, security=grades.security.passed, integrity=grades.integrity.passed)
                result = EvaluationResult(run_id, task.id, agent.name, agent_run.model, grades.functional.passed, grades.functional.passed, grades.security.passed, grades.integrity.passed, duration_seconds=time.monotonic()-started, steps=agent_run.steps, input_tokens=agent_run.input_tokens, output_tokens=agent_run.output_tokens, estimated_cost_usd=agent_run.estimated_cost_usd, failed_security_properties=grades.security.failures, integrity_violations=grades.integrity.failures, metadata=metadata)
                result.finalize()
            diff = _final_diff(workspace)
            task_results = self.results_root / task.id
            task_trajectories = self.trajectories_root / task.id
            (task_results / "final.diff").parent.mkdir(parents=True, exist_ok=True)
            (task_results / "final.diff").write_text(diff, encoding="utf-8")
            trajectory.log("run_complete", classification=result.classification)
            write_json(task_results / "result.json", result.to_dict())
            trajectory.write_jsonl(task_trajectories / "trajectory.jsonl")
            return result
        finally:
            workspace.cleanup()


def _final_diff(workspace) -> str:
    current: dict[str, str] = {}
    for path in workspace.root.rglob("*"):
        if path.is_file() and not path.is_symlink():
            try:
                current[path.relative_to(workspace.root).as_posix()] = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
    lines: list[str] = []
    for name in sorted(set(workspace.baseline_files) | set(current)):
        lines.extend(unified_diff(workspace.baseline_files.get(name, "").splitlines(keepends=True), current.get(name, "").splitlines(keepends=True), fromfile=f"before/{name}", tofile=f"after/{name}"))
    return "".join(lines)
