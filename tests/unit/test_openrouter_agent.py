from pathlib import Path

from coding_safety_eval.agents.openrouter_agent import OpenRouterAgent
from coding_safety_eval.models.task import discover_tasks


def test_action_parser_accepts_only_structured_actions():
    actions, error = OpenRouterAgent._parse_actions('{"actions":[{"action":"finish","summary":"done"}]}')
    assert error is None
    assert actions[0]["action"] == "finish"


def test_workspace_escape_and_protected_write_are_blocked(tmp_path):
    agent = OpenRouterAgent("test")
    task = discover_tasks(Path("tasks"))["auth-bypass-001"]
    _, event, _ = agent._execute_action({"action": "write_file", "path": "../outside.py", "content": "x"}, task, tmp_path)
    assert event["event"] == "error"
    _, event, _ = agent._execute_action({"action": "write_file", "path": "tests/test_visible.py", "content": "x"}, task, tmp_path)
    assert event["message"] == "protected path"
