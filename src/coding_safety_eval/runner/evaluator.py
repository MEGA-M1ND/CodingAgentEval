"""Coordinates isolated execution, layered deterministic grading, and artifacts."""

from __future__ import annotations

import time
import uuid
from datetime import UTC, datetime
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
    def __init__(self, project_root: Path, results_root: Path, trajectories_root: Path) -> None:
        self.project_root, self.results_root, self.trajectories_root = project_root, results_root, trajectories_root

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
            if agent_run.error:
                trajectory.log("error", message=agent_run.error)
                result = EvaluationResult(run_id, task.id, agent.name, agent_run.model, duration_seconds=time.monotonic()-started, steps=agent_run.steps, metadata={"error": agent_run.error, "task_version": task.version, "git_commit": commit_hash(self.project_root)})
            else:
                grades = grade_workspace(task, workspace)
                trajectory.log("grader_result", functional=grades.functional.passed, security=grades.security.passed, integrity=grades.integrity.passed)
                result = EvaluationResult(run_id, task.id, agent.name, agent_run.model, grades.functional.passed, grades.functional.passed, grades.security.passed, grades.integrity.passed, duration_seconds=time.monotonic()-started, steps=agent_run.steps, failed_security_properties=grades.security.failures, integrity_violations=grades.integrity.failures, metadata={"task_version": task.version, "git_commit": commit_hash(self.project_root)})
                result.finalize()
            trajectory.log("run_complete", classification=result.classification)
            write_json(self.results_root / f"{task.id}-{run_id}.json", result.to_dict())
            trajectory.write_jsonl(self.trajectories_root / f"{task.id}-{run_id}.jsonl")
            return result
        finally:
            workspace.cleanup()
