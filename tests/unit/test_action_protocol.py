from __future__ import annotations

import json

import pytest

from coding_safety_eval.agents.action_protocol import (
    FinishAction,
    ReadFileAction,
    RunTestsAction,
    WriteFileAction,
    normalize_action,
)


def test_canonical_read_is_accepted_unchanged():
    result = normalize_action({"action": "read_file", "path": "src/app.py"})
    assert result.action == ReadFileAction("src/app.py")
    assert result.aliases == {}


@pytest.mark.parametrize("alias", ["filename", "file_path", "file"])
def test_unambiguous_file_aliases_are_normalized(alias):
    result = normalize_action({"action": "read_file", alias: "src/app.py"})
    assert result.action == ReadFileAction("src/app.py")
    assert result.aliases == {alias: "path"}


def test_canonical_and_alias_write_are_accepted():
    canonical = normalize_action({"action": "write_file", "path": "src/app.py", "content": "x"})
    aliased = normalize_action({"action": "write_file", "filename": "src/app.py", "content": "x"})
    assert canonical.action == WriteFileAction("src/app.py", "x")
    assert aliased.action == WriteFileAction("src/app.py", "x")
    assert aliased.aliases == {"filename": "path"}


def test_missing_and_conflicting_paths_are_rejected():
    missing = normalize_action({"action": "read_file"})
    conflicting = normalize_action({"action": "read_file", "path": "src/a.py", "filename": "src/b.py"})
    assert missing.error == "missing required field: path"
    assert conflicting.error == "conflicting aliases for path"


def test_equivalent_duplicate_alias_is_accepted():
    result = normalize_action({"action": "read_file", "path": "src/a.py", "filename": "src/a.py"})
    assert result.action == ReadFileAction("src/a.py")
    assert result.aliases == {"filename": "path"}


def test_unknown_action_and_invalid_fields_are_rejected():
    assert normalize_action({"action": "execute_shell"}).error == "unknown action"
    assert normalize_action({"action": "write_file", "path": "a.py", "content": 3}).error == "missing or invalid required field: content"
    assert normalize_action({"action": "finish", "summary": "done"}).action == FinishAction("done")
    assert normalize_action({"action": "run_tests"}).action == RunTestsAction()


def test_unknown_metadata_is_logged_but_cannot_change_execution():
    result = normalize_action({"action": "read_file", "path": "src/a.py", "trace": "ignored"})
    assert result.action == ReadFileAction("src/a.py")
    assert result.ignored_fields == ("trace",)


def test_malformed_json_is_not_a_protocol_action():
    with pytest.raises(json.JSONDecodeError):
        json.loads('{"action":')
