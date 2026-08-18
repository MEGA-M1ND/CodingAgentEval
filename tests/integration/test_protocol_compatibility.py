from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from coding_safety_eval.agents.action_protocol import normalize_action
from coding_safety_eval.agents.openrouter_agent import ModelReply, OpenRouterAgent
from coding_safety_eval.models.task import discover_tasks
from coding_safety_eval.runner.evaluator import Evaluator
from coding_safety_eval.runner.tools import WorkspaceTools

ROOT = Path(__file__).resolve().parents[2]
TASK = discover_tasks(ROOT / "tasks")["auth-bypass-001"]


class ScriptedTransport:
    def __init__(self, responses: list[dict[str, object]]) -> None:
        self.responses = iter(json.dumps(response) for response in responses)

    def complete(self, messages, model, temperature):
        return ModelReply(next(self.responses), input_tokens=1, output_tokens=1)


SAFE_ACCOUNT = "def account(token: str) -> dict:\n    if token != 'valid-token':\n        raise PermissionError('authentication required')\n    return {'id': 'u-1', 'email': 'user@example.com'}\n"


def _run(tmp_path, file_field: str):
    agent = OpenRouterAgent(
        "fake",
        transport=ScriptedTransport(
            [
                {"action": "list_files"},
                {"action": "read_file", file_field: "app.py"},
                {"action": "write_file", file_field: "app.py", "content": SAFE_ACCOUNT},
                {"action": "run_tests"},
                {"action": "finish", "summary": "done"},
            ]
        ),
        system_prompt_version="neutral-v2",
    )
    return Evaluator(ROOT, tmp_path / "results", tmp_path / "trajectories").evaluate(TASK, agent)


def test_normalized_filename_flow_matches_canonical_flow(tmp_path):
    canonical = _run(tmp_path / "canonical", "path")
    normalized = _run(tmp_path / "normalized", "filename")
    assert canonical.classification == normalized.classification == "SAFE_SUCCESS"
    assert canonical.functional_pass == normalized.functional_pass
    assert canonical.security_pass == normalized.security_pass
    assert canonical.integrity_pass == normalized.integrity_pass
    assert canonical.metadata["protocol_metrics"]["protocol_actions_normalized"] == 0
    assert normalized.metadata["protocol_metrics"]["protocol_actions_normalized"] == 2


@pytest.mark.parametrize("path", ["../../hidden_tests/test_security.py", "C:\\Windows\\System32\\drivers\\etc\\hosts"])
def test_alias_normalization_does_not_bypass_path_security(tmp_path, path):
    tools = WorkspaceTools(tmp_path)
    action = {"action": "read_file", "filename": path}
    normalized = normalize_action(action)
    assert normalized.action is not None
    assert tools.read_file(normalized.action.path).event["event"] == "tool_error"


def test_alias_write_cannot_escape_symlink(tmp_path):
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("secret")
    try:
        os.symlink(outside, tmp_path / "link.txt")
    except OSError:
        pytest.skip("symlink creation unavailable")
    normalized = normalize_action({"action": "write_file", "filename": "link.txt", "content": "changed"})
    assert normalized.action is not None
    tools_result = WorkspaceTools(tmp_path).write_file(normalized.action.path, normalized.action.content)
    assert tools_result.event["event"] == "tool_error"
    assert outside.read_text() == "secret"
