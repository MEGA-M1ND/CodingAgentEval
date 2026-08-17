"""Model-independent parsing and canonicalization for bounded agent actions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CANONICAL_ACTIONS = frozenset({"list_files", "read_file", "write_file", "run_tests", "finish"})
FILE_PATH_ALIASES = ("path", "filename", "file_path", "file")


@dataclass(frozen=True)
class ListFilesAction:
    action: str = "list_files"


@dataclass(frozen=True)
class ReadFileAction:
    path: str
    action: str = "read_file"


@dataclass(frozen=True)
class WriteFileAction:
    path: str
    content: str
    action: str = "write_file"


@dataclass(frozen=True)
class RunTestsAction:
    action: str = "run_tests"


@dataclass(frozen=True)
class FinishAction:
    summary: str = ""
    action: str = "finish"


CanonicalAction = ListFilesAction | ReadFileAction | WriteFileAction | RunTestsAction | FinishAction


@dataclass(frozen=True)
class NormalizationResult:
    action: CanonicalAction | None
    aliases: dict[str, str]
    ignored_fields: tuple[str, ...] = ()
    error: str | None = None


def normalize_action(raw: dict[str, Any]) -> NormalizationResult:
    """Return a typed action, or a deterministic reason it is unsafe/ambiguous.

    Unknown fields are ignored and logged. They never influence execution.
    """
    name = raw.get("action")
    if not isinstance(name, str) or name not in CANONICAL_ACTIONS:
        return NormalizationResult(None, {}, error="unknown action")
    ignored = tuple(sorted(key for key in raw if key not in {"action", "summary", "content", *FILE_PATH_ALIASES}))
    if name in {"read_file", "write_file"}:
        path, aliases, error = _canonical_path(raw)
        if error:
            return NormalizationResult(None, aliases, ignored, error)
        if name == "read_file":
            return NormalizationResult(ReadFileAction(path), aliases, ignored)
        content = raw.get("content")
        if not isinstance(content, str):
            return NormalizationResult(None, aliases, ignored, "missing or invalid required field: content")
        return NormalizationResult(WriteFileAction(path, content), aliases, ignored)
    if name == "list_files":
        return NormalizationResult(ListFilesAction(), {}, ignored)
    if name == "run_tests":
        return NormalizationResult(RunTestsAction(), {}, ignored)
    summary = raw.get("summary", "")
    if not isinstance(summary, str):
        return NormalizationResult(None, {}, ignored, "invalid optional field: summary")
    return NormalizationResult(FinishAction(summary), {}, ignored)


def _canonical_path(raw: dict[str, Any]) -> tuple[str, dict[str, str], str | None]:
    supplied = {key: raw[key] for key in FILE_PATH_ALIASES if key in raw}
    if not supplied:
        return "", {}, "missing required field: path"
    if not all(isinstance(value, str) and value for value in supplied.values()):
        return "", {}, "missing or invalid required field: path"
    values = set(supplied.values())
    if len(values) != 1:
        return "", {}, "conflicting aliases for path"
    path = next(iter(values))
    aliases = {key: "path" for key in supplied if key != "path"}
    return path, aliases, None
