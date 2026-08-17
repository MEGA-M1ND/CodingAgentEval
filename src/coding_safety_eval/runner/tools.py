"""Constrained, workspace-only tools exposed to real coding agents."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath

from coding_safety_eval.runner.command_runner import run_command

IGNORED_DIRECTORIES = {".git", "__pycache__", ".pytest_cache"}


@dataclass(frozen=True)
class ToolResult:
    output: str
    event: dict[str, object]


class WorkspaceTools:
    def __init__(self, workspace: Path, max_file_bytes: int = 200_000, max_output_chars: int = 12_000) -> None:
        self.workspace = workspace.resolve()
        self.max_file_bytes = max_file_bytes
        self.max_output_chars = max_output_chars

    def list_files(self, max_depth: int = 6, max_entries: int = 300) -> ToolResult:
        entries: list[str] = []
        for path in sorted(self.workspace.rglob("*"), key=lambda item: item.as_posix()):
            relative = path.relative_to(self.workspace)
            if any(part in IGNORED_DIRECTORIES for part in relative.parts) or len(relative.parts) > max_depth:
                continue
            if path.is_file() or path.is_symlink():
                entries.append(relative.as_posix())
            if len(entries) >= max_entries:
                break
        suffix = "\n... truncated" if len(entries) >= max_entries else ""
        return ToolResult("\n".join(entries) + suffix, {"event": "file_list", "entries": len(entries)})

    def read_file(self, relative: str) -> ToolResult:
        path, error = self.safe_path(relative)
        if error:
            return self._error(error, relative)
        if not path.is_file() or path.is_symlink():
            return self._error("file not found", relative)
        if path.stat().st_size > self.max_file_bytes:
            return self._error("file exceeds size limit", relative)
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return self._error("only UTF-8 text files are supported", relative)
        return ToolResult(content, {"event": "file_read", "path": relative, "bytes": len(content.encode())})

    def write_file(self, relative: str, content: object) -> ToolResult:
        path, error = self.safe_path(relative)
        if error:
            return self._error(error, relative)
        if not isinstance(content, str) or len(content.encode()) > self.max_file_bytes:
            return self._error("invalid or oversized content", relative)
        path.parent.mkdir(parents=True, exist_ok=True)
        # Re-resolve after mkdir: an existing symlinked parent must not become an escape hatch.
        path, error = self.safe_path(relative)
        if error:
            return self._error(error, relative)
        path.write_text(content, encoding="utf-8")
        return ToolResult("file written", {"event": "file_write", "path": relative, "bytes": len(content.encode())})

    def run_tests(self) -> ToolResult:
        result = run_command(["python", "-m", "pytest", "-q", "tests"], self.workspace, timeout=30)
        output = (result.stdout + result.stderr)[-self.max_output_chars :]
        return ToolResult(output, {"event": "test_run", "exit_code": result.returncode, "timeout": result.timed_out})

    def safe_path(self, relative: str) -> tuple[Path, str | None]:
        if not relative:
            return self.workspace, "path is required"
        windows = PureWindowsPath(relative)
        pure = PurePosixPath(relative.replace("\\", "/"))
        if windows.is_absolute() or windows.drive or pure.is_absolute() or ".." in pure.parts:
            return self.workspace, "path outside workspace blocked"
        candidate = self.workspace.joinpath(*pure.parts)
        resolved = candidate.resolve(strict=False)
        if not resolved.is_relative_to(self.workspace):
            return self.workspace, "path outside workspace blocked"
        return resolved, None

    @staticmethod
    def _error(message: str, path: str) -> ToolResult:
        return ToolResult(f"tool error: {message}", {"event": "tool_error", "path": path, "message": message})
