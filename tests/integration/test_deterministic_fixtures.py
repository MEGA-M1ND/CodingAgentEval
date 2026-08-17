from pathlib import Path

import pytest

from coding_safety_eval.agents.manual_patch_agent import ManualPatchAgent
from coding_safety_eval.models.task import discover_tasks
from coding_safety_eval.runner.evaluator import Evaluator

ROOT = Path(__file__).resolve().parents[2]
TASKS = discover_tasks(ROOT / "tasks")


@pytest.mark.parametrize("task_id", sorted(TASKS))
def test_safe_fixture_is_safe_success(task_id, tmp_path):
    result = Evaluator(ROOT, tmp_path / "results", tmp_path / "trajectories").evaluate(TASKS[task_id], ManualPatchAgent("safe"))
    assert result.classification == "SAFE_SUCCESS"


@pytest.mark.parametrize("task_id", sorted(TASKS))
def test_unsafe_fixture_is_explicit_false_success(task_id, tmp_path):
    result = Evaluator(ROOT, tmp_path / "results", tmp_path / "trajectories").evaluate(TASKS[task_id], ManualPatchAgent("unsafe"))
    assert result.visible_tests_pass
    assert result.classification == "FALSE_SUCCESS"
