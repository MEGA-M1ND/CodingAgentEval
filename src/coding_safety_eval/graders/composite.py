from __future__ import annotations

from dataclasses import dataclass

from coding_safety_eval.models.task import Task
from coding_safety_eval.runner.workspace import Workspace

from .functional import grade_functional
from .integrity import grade_integrity
from .security import grade_security


@dataclass
class CompositeGrade:
    functional: object
    security: object
    integrity: object


def grade_workspace(task: Task, workspace: Workspace) -> CompositeGrade:
    return CompositeGrade(grade_functional(task, workspace.root), grade_security(task, workspace.root), grade_integrity(workspace))
