from pathlib import Path

from coding_safety_eval.models.result import EvaluationResult
from coding_safety_eval.models.task import discover_tasks


def test_task_loading():
    tasks = discover_tasks(Path("tasks"))
    assert set(tasks) == {"auth-bypass-001", "sql-injection-001", "command-injection-001", "path-traversal-001", "ssrf-001", "test-tampering-001"}


def test_false_success_requires_visible_green_and_safety_failure():
    result = EvaluationResult("run", "task", "agent", None, True, True, False, True)
    result.finalize()
    assert result.classification == "FALSE_SUCCESS"
    assert result.to_dict()["overall_success"] is False
